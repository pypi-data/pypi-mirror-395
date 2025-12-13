"""
JSON Schema validator for pytemplify.

This validator validates JSON files against JSON schemas. It supports both
inline schemas and external schema files.

SOLID Principles:
    - SRP: Single responsibility - validate JSON against schemas
    - OCP: Open for extension through options
    - LSP: Substitutable for BaseValidator
    - DIP: Depends on abstractions (BaseValidator)

DRY Principle:
    - Reuses BaseValidator pattern matching logic
    - Reuses existing file reading utilities
"""

import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from pytemplify.validation.base import BaseValidator, ValidationResult

logger = logging.getLogger(__name__)


class JSONSchemaValidator(BaseValidator):
    """
    Validates JSON files against JSON schemas (SOLID: SRP, LSP).

    Responsibilities:
        - Discover JSON files to validate
        - Load and parse JSON files
        - Validate against JSON schemas
        - Report validation errors with context

    DRY: Reuses BaseValidator pattern matching logic.
    """

    # Default patterns for JSON file discovery
    DEFAULT_JSON_PATTERNS = ["*.json"]

    def __init__(self, config):
        """
        Initialize JSON Schema validator.

        Args:
            config: ValidatorConfig instance

        Options supported:
            - schema_file: Path to JSON schema file (required if schema not provided)
            - schema: Inline JSON schema dictionary (required if schema_file not provided)
            - strict: Strict validation mode (default: True)
            - allow_additional_properties: Allow additional properties (default: False)
            - validate_formats: Validate format strings (default: True)

        Note: jsonschema package is optional. If not installed, validator will
              skip validation with a warning.
        """
        super().__init__(config)

        # Set default patterns if not specified
        if not self.config.patterns:
            self.config.patterns.extend(self.DEFAULT_JSON_PATTERNS)

        # Check for jsonschema package
        self._jsonschema_available = self._check_jsonschema_available()

        # Load schema
        self._schema = self._load_schema()

    def _check_jsonschema_available(self) -> bool:
        """
        Check if jsonschema package is available.

        Returns:
            True if jsonschema is available, False otherwise
        """
        try:
            import jsonschema  # pylint: disable=import-outside-toplevel,unused-import

            _ = jsonschema  # Use it to avoid unused warning
            return True
        except ImportError:
            self._logger.warning(
                "jsonschema package not installed. "
                "Install it with: pip install jsonschema\n"
                "Validation will be skipped."
            )
            return False

    def _load_schema(self) -> Optional[Dict[str, Any]]:
        """
        Load JSON schema from config.

        Returns:
            JSON schema dictionary or None if not available

        Raises:
            ValueError: If neither schema nor schema_file is provided
        """
        # Check for inline schema
        if "schema" in self.config.options:
            schema = self.config.options["schema"]
            self._logger.debug("Using inline schema")
            return schema

        # Check for schema file
        if "schema_file" in self.config.options:
            schema_file = Path(self.config.options["schema_file"])
            if not schema_file.exists():
                raise ValueError(f"Schema file not found: {schema_file}")

            try:
                with open(schema_file, encoding="utf-8") as f:
                    schema = json.load(f)
                self._logger.info("Loaded schema from %s", schema_file)
                return schema
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in schema file {schema_file}: {e}") from e

        # No schema provided
        raise ValueError("Either 'schema' or 'schema_file' must be provided in validator options")

    def discover(self, output_dir: Path) -> List[Path]:
        """
        Discover JSON files in the output directory.

        Args:
            output_dir: Directory to search for JSON files

        Returns:
            List of JSON file paths
        """
        self._logger.info("Discovering JSON files in %s", output_dir)

        json_files = []
        for pattern in self.config.patterns:
            # Search recursively for JSON files
            matches = list(output_dir.rglob(pattern))
            json_files.extend(matches)
            self._logger.debug("Pattern '%s' found %d files", pattern, len(matches))

        # Remove duplicates while preserving order
        seen = set()
        unique_files = []
        for file_path in json_files:
            if file_path not in seen:
                seen.add(file_path)
                unique_files.append(file_path)

        self._logger.info("Discovered %d JSON files", len(unique_files))
        return unique_files

    def validate(
        self, target: Path, context: Optional[Dict[str, Any]] = None
    ) -> ValidationResult:  # pylint: disable=unused-argument
        """
        Validate a single JSON file against the schema.

        Args:
            target: JSON file path
            context: Optional context (unused for JSON validation)

        Returns:
            ValidationResult with validation results
        """
        start_time = time.time()
        file_name = target.name

        self._logger.info("Validating JSON file: %s", file_name)

        # Skip if jsonschema not available
        if not self._jsonschema_available:
            return ValidationResult(
                validator_name=self.config.name,
                target_name=file_name,
                success=False,
                message="jsonschema package not installed",
                details="Install with: pip install jsonschema",
                file_path=target,
                errors=["jsonschema not available"],
                duration_seconds=time.time() - start_time,
            )

        try:
            # Load JSON file
            json_data = self._load_json_file(target)

            # Validate against schema
            validation_errors = self._validate_against_schema(json_data)

            duration = time.time() - start_time

            if not validation_errors:
                return ValidationResult(
                    validator_name=self.config.name,
                    target_name=file_name,
                    success=True,
                    message=f"JSON file '{file_name}' is valid",
                    details=f"Validated against schema in {duration:.3f}s",
                    file_path=target,
                    duration_seconds=duration,
                )

            error_details = "\n".join([f"  - {err}" for err in validation_errors])
            return ValidationResult(
                validator_name=self.config.name,
                target_name=file_name,
                success=False,
                message=f"JSON validation failed for '{file_name}'",
                details=f"Errors:\n{error_details}",
                file_path=target,
                errors=validation_errors,
                duration_seconds=duration,
            )

        except Exception as e:  # pylint: disable=broad-exception-caught
            duration = time.time() - start_time
            self._logger.error("Validation failed for %s: %s", file_name, e)
            return ValidationResult(
                validator_name=self.config.name,
                target_name=file_name,
                success=False,
                message=f"Validation error for '{file_name}'",
                details=str(e),
                file_path=target,
                errors=[str(e)],
                duration_seconds=duration,
            )

    def _load_json_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Load and parse JSON file.

        Args:
            file_path: Path to JSON file

        Returns:
            Parsed JSON data

        Raises:
            ValueError: If file cannot be read or parsed
        """
        try:
            with open(file_path, encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}") from e
        except Exception as e:  # pylint: disable=broad-exception-caught
            raise ValueError(f"Failed to read file: {e}") from e

    def _validate_against_schema(self, json_data: Dict[str, Any]) -> List[str]:
        """
        Validate JSON data against the schema.

        Args:
            json_data: Parsed JSON data

        Returns:
            List of validation error messages (empty if valid)
        """
        import jsonschema  # pylint: disable=import-outside-toplevel
        from jsonschema import Draft7Validator  # pylint: disable=import-outside-toplevel

        # Create validator with options
        validator_class = Draft7Validator
        format_checker = None

        if self.config.options.get("validate_formats", True):
            format_checker = jsonschema.FormatChecker()

        # Modify schema based on options
        schema = self._schema.copy() if self._schema else {}

        if not self.config.options.get("allow_additional_properties", False):
            if "additionalProperties" not in schema:
                schema["additionalProperties"] = False

        # Create validator
        validator = validator_class(schema, format_checker=format_checker)

        # Collect errors
        errors = []
        for error in validator.iter_errors(json_data):
            # Format error message with path
            path = ".".join(str(p) for p in error.absolute_path) if error.absolute_path else "root"
            errors.append(f"At '{path}': {error.message}")

        return errors

    def cleanup(self, output_dir: Path) -> None:
        """
        Clean up validation artifacts.

        JSON validation doesn't create artifacts, so this is a no-op.

        Args:
            output_dir: Directory where validation was run
        """
        # No cleanup needed for JSON validation
