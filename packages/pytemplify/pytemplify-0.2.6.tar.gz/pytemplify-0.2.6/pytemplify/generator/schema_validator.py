"""Schema validation utilities with clickable error URIs.

This module provides JSON Schema validation for extra_data configuration files,
with cross-platform clickable file URIs in error messages.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Optional

import jsonschema

from pytemplify.exceptions import TemplateConfigError
from pytemplify.file_uri_utils import FileUriBuilder, extract_line_from_json_path

logger = logging.getLogger(__name__)


class SchemaValidationError(NamedTuple):
    """Represents a single schema validation error with location info."""

    message: str
    json_path: tuple  # Path in JSON structure (e.g., ('servers', 0, 'hostname'))
    file_path: Optional[Path]
    line: Optional[int]
    column: Optional[int]

    def to_string(self) -> str:
        """Convert to formatted error string with clickable URI."""
        path_str = ".".join(str(x) for x in self.json_path) if self.json_path else "(root)"
        error_msg = f"at '{path_str}': {self.message}"

        if self.file_path:
            uri = FileUriBuilder.create_uri(self.file_path, self.line, self.column)
            return f"{error_msg}\n    ↳ {uri}"

        return error_msg


class SchemaValidator:
    """Validates data against JSON Schema with clickable error URIs.

    Features:
    - Schema caching for performance
    - Meta-validation of schemas
    - Clickable file URIs in error messages
    - Cross-platform path handling
    """

    def __init__(self, base_path: Path):
        """Initialize validator.

        Args:
            base_path: Base directory for resolving relative schema paths
        """
        self.base_path = base_path
        self._schema_cache: Dict[Path, Dict[str, Any]] = {}

    def validate(
        self,
        data: Any,
        schema_path: Path,
        data_file_path: Optional[Path] = None,
        context: str = "",  # pylint: disable=unused-argument
    ) -> List[SchemaValidationError]:
        """Validate data against schema with detailed error reporting.

        Args:
            data: Data to validate
            schema_path: Path to JSON Schema file (must be absolute)
            data_file_path: Optional path to the data file (for clickable URIs)
            context: Context string for error messages (e.g., "extra_data key 'deployment'")

        Returns:
            List of SchemaValidationError objects (empty if valid)

        Raises:
            TemplateConfigError: If schema file cannot be loaded
        """
        # Load schema (with caching)
        schema = self._load_schema(schema_path)

        # Validate
        validator = jsonschema.Draft7Validator(schema)
        errors = sorted(validator.iter_errors(data), key=lambda e: e.path)

        # Convert to SchemaValidationError objects with line numbers
        validation_errors = []
        for error in errors:
            # Extract line number from data file if available
            line = None
            if data_file_path and error.path:
                line = extract_line_from_json_path(data_file_path, tuple(error.path))

            validation_error = SchemaValidationError(
                message=error.message,
                json_path=tuple(error.path),
                file_path=data_file_path,
                line=line,
                column=None,  # JSON Schema doesn't provide column info
            )
            validation_errors.append(validation_error)

        return validation_errors

    def validate_and_format_errors(
        self,
        data: Any,
        schema_path: Path,
        data_file_path: Optional[Path] = None,
        context: str = "",
    ) -> List[str]:
        """Validate and return formatted error strings.

        Args:
            data: Data to validate
            schema_path: Path to JSON Schema file
            data_file_path: Optional path to the data file
            context: Context string for error messages

        Returns:
            List of formatted error messages with clickable URIs
        """
        errors = self.validate(data, schema_path, data_file_path, context)

        formatted_errors = []
        for error in errors:
            error_str = error.to_string()
            if context:
                error_str = f"{context}: {error_str}"
            formatted_errors.append(error_str)

        return formatted_errors

    def _load_schema(self, schema_path: Path) -> Dict[str, Any]:
        """Load schema file with caching and meta-validation.

        Args:
            schema_path: Absolute path to schema file

        Returns:
            Parsed schema dictionary

        Raises:
            TemplateConfigError: If schema cannot be loaded (with clickable URI)
        """
        # Check cache
        if schema_path in self._schema_cache:
            return self._schema_cache[schema_path]

        # Validate path
        if not schema_path.exists():
            uri = FileUriBuilder.create_uri(schema_path)
            raise TemplateConfigError(f"Schema file not found\n    ↳ {uri}")

        if not schema_path.is_file():
            uri = FileUriBuilder.create_uri(schema_path)
            raise TemplateConfigError(f"Schema path is not a file\n    ↳ {uri}")

        # Load and cache
        try:
            with open(schema_path, "r", encoding="utf-8") as f:
                schema = json.load(f)

            # Meta-validate the schema itself
            try:
                jsonschema.Draft7Validator.check_schema(schema)
            except jsonschema.SchemaError as exc:
                uri = FileUriBuilder.create_uri(schema_path)
                raise TemplateConfigError(f"Invalid JSON Schema: {exc}\n    ↳ {uri}") from exc

            self._schema_cache[schema_path] = schema
            logger.debug("Loaded and cached schema from %s", schema_path)
            return schema

        except json.JSONDecodeError as exc:
            # JSON syntax error - include line and column
            uri = FileUriBuilder.create_uri(schema_path, line=exc.lineno, column=exc.colno)
            raise TemplateConfigError(f"Failed to parse schema file: {exc.msg}\n    ↳ {uri}") from exc
        except (OSError, IOError) as exc:
            uri = FileUriBuilder.create_uri(schema_path)
            raise TemplateConfigError(f"Failed to read schema file: {exc}\n    ↳ {uri}") from exc
