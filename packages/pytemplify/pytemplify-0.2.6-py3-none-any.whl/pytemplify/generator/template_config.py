"""Template configuration for pytemplify generator.

This module provides template configuration functionality for code generation,
handling YAML template files and their validation against schema.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List

import jsonschema
import yaml

from pytemplify.exceptions import TemplateConfigError
from pytemplify.file_uri_utils import FileUriBuilder

from .config_file_loader import get_file_format_registry
from .path_resolver import PathResolver
from .schema_validator import SchemaValidator
from .utils import get_nested_attr_or_key, resolve_path_or_glob


def get_schema_path() -> str:
    """Return the absolute path to the templates-schema.json file."""
    return str(Path(__file__).parent / "templates-schema.json")


class TemplateConfig:  # pylint: disable=too-many-instance-attributes
    """Configuration for template files.

    Attributes:
        yaml_path: Path to the .templates.yaml file
        schema_path: Path to the templates schema file
        errors: List of validation errors
        yaml_data: Parsed YAML data
        extra_data: Additional data loaded from extra_data files
        flatten_data: Whether to flatten data for direct template access
        format_config: Formatting configuration
    """

    def __init__(self, config_filepath: Path) -> None:
        """Initialize TemplateConfig.

        Args:
            config_filepath: Path to the .templates.yaml file
        """
        self.yaml_path: Path = Path(config_filepath).resolve()  # Always resolve to absolute path
        self.schema_path: str = get_schema_path()
        self.errors: List[str] = []
        self.yaml_data: Dict[str, Any] = {}
        self.extra_data: Dict[str, Any] = {}
        self.flatten_data: bool = True  # Default value
        self.format_config: Dict[str, Any] = {}  # Formatting configuration
        self.jinja_env_config: Dict[str, Any] = {}  # Jinja2 environment configuration
        self.manual_sections_config: Dict[str, str] = {}  # Manual sections configuration

        # Initialize cross-platform path resolver
        self.path_resolver = PathResolver(self.yaml_path.parent)

        # Helper utilities (initialized during _load_extra_data)
        self._file_registry = None
        self._schema_validator = None
        self._logger = None

    def load(self) -> None:
        """Load and validate the .templates.yaml file against the schema."""
        self.yaml_data = self._safe_load_yaml(self.yaml_path)
        schema = self._safe_load_json(self.schema_path)
        self.errors = self._validate_yaml(schema, self.yaml_data)
        self._append_extra_data_key_errors(self.yaml_data)

        # Load format configuration early (before template validation)
        self.format_config = self.yaml_data.get("format", {})

        # Load Jinja2 environment configuration
        self.jinja_env_config = self.yaml_data.get("jinja_env", {})

        # Load manual sections configuration
        self.manual_sections_config = self.yaml_data.get("manual_sections", {})

        # Load flatten_data setting from YAML (default to True if not specified)
        self.flatten_data = self.yaml_data.get("flatten_data", True)

        # If there are schema validation errors, skip resolving template
        # folders to allow callers/tests to inspect errors without raising
        # file-system related exceptions.
        if self.errors:
            # If errors relate to data_helpers section, treat as fatal
            if any("data_helpers" in e for e in self.errors):
                raise TemplateConfigError("Invalid data_helpers configuration: " + "; ".join(self.errors))
            return

        # Validate data_helpers section explicitly (schema doesn't cover it)
        self._validate_data_helpers_section(self.yaml_data)

        # Resolve all template_folder entries to Path objects
        self._resolve_template_folders()

        # Load extra data files if specified
        self.extra_data = self._load_extra_data()

    def _resolve_template_folders(self) -> None:
        """Resolve all template folder entries to Path objects as per rules."""
        for template in self.yaml_data.get("templates", []):
            folder = template.get("folder")
            if folder is None:
                continue
            resolved_paths = resolve_path_or_glob(folder, self.yaml_path.parent)
            if not resolved_paths:
                raise TemplateConfigError(
                    f"No template file or directory found for: {folder} " f"(resolved relative to {self.yaml_path})"
                )
            resolved_path = resolved_paths[0]

            if "folder" in template:
                template["folder"] = str(resolved_path)

            # Skip exists() check if path contains Jinja2 {{}} syntax
            if "{{" in str(resolved_path) and "}}" in str(resolved_path):
                continue
            if not Path(resolved_path).exists():
                raise TemplateConfigError(f"Resolved template path does not exist: {resolved_path}")

    @staticmethod
    def _safe_load_yaml(path: Path) -> Dict[str, Any]:
        """Safely load YAML file and return its contents."""
        try:
            with open(path, "r", encoding="utf-8") as yaml_file:
                return yaml.safe_load(yaml_file)
        except Exception as exc:
            raise TemplateConfigError(f"Failed to load YAML: {exc}") from exc

    @staticmethod
    def _safe_load_json(path: str) -> Dict[str, Any]:
        """Safely load JSON file and return its contents."""
        try:
            with open(path, "r", encoding="utf-8") as schema_file:
                return json.load(schema_file)
        except Exception as exc:
            raise TemplateConfigError(f"Failed to load schema: {exc}") from exc

    @staticmethod
    def _validate_yaml(schema: Dict[str, Any], yaml_data: Dict[str, Any]) -> List[str]:
        """Validate YAML data against schema and return error list."""
        validator = jsonschema.Draft7Validator(schema)
        errors = sorted(validator.iter_errors(yaml_data), key=lambda e: e.path)
        return [f"Schema error at '{'.'.join(str(x) for x in e.path)}': {e.message}" for e in errors]

    def _append_extra_data_key_errors(self, yaml_data: Dict[str, Any]) -> None:
        """Append explicit errors for extra_data entries missing a key."""
        extra_data_entries = yaml_data.get("extra_data", [])
        for idx, entry in enumerate(extra_data_entries):
            if isinstance(entry, dict) and "key" not in entry:
                self.errors.append(f"Schema error at 'extra_data[{idx}]': 'key' is a required property")

    def _load_extra_data(self) -> Dict[str, Any]:
        """Load additional data sources with cross-platform support.

        Supports:
        - External files (JSON/YAML/TOML with format auto-detection)
        - Inline dictionary data
        - Optional JSON Schema validation
        - Windows and Linux path formats
        - Clickable file URIs in error messages

        Returns:
            Dictionary containing loaded data from all extra_data sources

        Raises:
            TemplateConfigError: If required files cannot be loaded or validation fails
        """
        logger = logging.getLogger(__name__)
        extra_data = {}
        extra_data_configs = self.yaml_data.get("extra_data", [])

        # Initialize utilities (stored as instance vars for helper methods)
        self._file_registry = get_file_format_registry()
        self._schema_validator = SchemaValidator(self.yaml_path.parent)
        self._logger = logger

        for config in extra_data_configs:
            key = self._validate_extra_data_key(config, extra_data)

            # Handle inline data vs external file data
            if "value" in config:
                data = self._load_inline_data(config, key)
            elif "path" in config:
                data = self._load_external_file_data(config, key)
                if data is None:  # Optional file not found or skipped
                    continue
            else:
                raise TemplateConfigError(f"Extra data entry for key '{key}' must have either 'value' or 'path' field")

            extra_data[key] = data

        if extra_data:
            logger.info("Loaded %d extra data source(s): %s", len(extra_data), ", ".join(extra_data.keys()))

        return extra_data

    def _validate_extra_data_key(self, config: Dict[str, Any], existing_keys: Dict[str, Any]) -> str:
        """Validate extra_data key doesn't conflict with reserved keys or duplicates.

        Args:
            config: Extra data configuration entry
            existing_keys: Already loaded extra data keys

        Returns:
            Validated key string

        Raises:
            TemplateConfigError: If validation fails
        """
        key = config.get("key")

        if not key:
            raise TemplateConfigError("Extra data entry missing required 'key' field")

        # Reserved keys that cannot be used for extra data
        reserved_keys = {"dd", "globals", "device", "message", "signal", "group"}

        if key in reserved_keys:
            raise TemplateConfigError(
                f"Extra data key '{key}' conflicts with reserved key. "
                f"Reserved keys are: {', '.join(sorted(reserved_keys))}"
            )

        if key in existing_keys:
            raise TemplateConfigError(
                f"Duplicate extra data key '{key}'. Keys must be unique across all extra_data entries."
            )

        return key

    def _load_inline_data(self, config: Dict[str, Any], key: str) -> Any:
        """Load and validate inline data from config.

        Args:
            config: Extra data configuration entry
            key: Data key

        Returns:
            Loaded and validated data

        Raises:
            TemplateConfigError: If validation fails
        """
        if "path" in config:
            raise TemplateConfigError(f"Extra data entry for key '{key}' cannot have both 'value' and 'path' fields")

        data = config["value"]

        # Validate against schema if provided
        schema_path_str = config.get("schema")
        if schema_path_str:
            self._validate_data_with_schema(data, schema_path_str, key, data_file_path=None)

        self._logger.debug("Loaded inline extra data as '%s'", key)
        return data

    def _load_external_file_data(self, config: Dict[str, Any], key: str) -> Any:
        """Load and validate data from external file.

        Args:
            config: Extra data configuration entry
            key: Data key

        Returns:
            Loaded and validated data, or None if optional file not found

        Raises:
            TemplateConfigError: If required file cannot be loaded or validation fails
        """
        path_str = config["path"]
        required = config.get("required", True)
        format_hint = config.get("format", "auto")
        schema_path_str = config.get("schema")

        # Resolve and validate file path
        data_path = self._resolve_and_validate_file_path(path_str, key, required)
        if data_path is None:  # Optional file not found
            return None

        # Load file data
        data = self._load_file_with_error_handling(data_path, format_hint, required)
        if data is None:  # Optional file failed to load
            return None

        # Validate against schema if provided
        if schema_path_str:
            self._validate_data_with_schema(data, schema_path_str, key, data_file_path=data_path)

        self._logger.debug(
            "Loaded extra data from %s as '%s' (format: %s)",
            self.path_resolver.normalize_for_display(data_path),
            key,
            format_hint,
        )
        return data

    def _resolve_and_validate_file_path(self, path_str: str, key: str, required: bool) -> Path:
        """Resolve and validate file path exists and is a regular file.

        Args:
            path_str: Path string from config
            key: Data key (for error messages)
            required: Whether file is required

        Returns:
            Resolved Path object, or None if optional file not found

        Raises:
            TemplateConfigError: If required file is invalid
        """
        # Resolve data file path (cross-platform)
        try:
            data_path = self.path_resolver.resolve(path_str, must_exist=False)
        except ValueError as exc:
            raise TemplateConfigError(f"Invalid path for extra_data key '{key}': {exc}") from exc

        # Check file exists
        if not data_path.exists():
            if required:
                uri = FileUriBuilder.create_uri(data_path)
                raise TemplateConfigError(f"Required extra data file not found\n    ↳ {uri}")
            self._logger.debug("Optional extra data file not found, skipping: %s", data_path)
            return None

        # Validate it's a regular file
        if not data_path.is_file():
            if required:
                uri = FileUriBuilder.create_uri(data_path)
                raise TemplateConfigError(f"Extra data path is not a regular file\n    ↳ {uri}")
            self._logger.warning("Extra data path is not a regular file, skipping: %s", data_path)
            return None

        return data_path

    def _load_file_with_error_handling(self, data_path: Path, format_hint: str, required: bool) -> Any:
        """Load file with comprehensive error handling.

        Args:
            data_path: Path to data file
            format_hint: Format hint ('json', 'yaml', 'toml', or 'auto')
            required: Whether file is required

        Returns:
            Loaded data, or None if optional file failed to load

        Raises:
            TemplateConfigError: If required file cannot be loaded
        """
        try:
            return self._file_registry.load_file(data_path, format_hint)
        except json.JSONDecodeError as exc:
            # JSON syntax error - include line and column
            uri = FileUriBuilder.create_uri(data_path, line=exc.lineno, column=exc.colno)
            error_msg = f"Failed to parse JSON file: {exc.msg}\n    ↳ {uri}"
            if required:
                raise TemplateConfigError(error_msg) from exc
            self._logger.warning(error_msg)
            return None
        except ValueError as exc:
            # YAML/TOML syntax error
            uri = FileUriBuilder.create_uri(data_path)
            error_msg = f"Failed to parse {format_hint} file: {exc}\n    ↳ {uri}"
            if required:
                raise TemplateConfigError(error_msg) from exc
            self._logger.warning(error_msg)
            return None
        except OSError as exc:
            # File system error
            uri = FileUriBuilder.create_uri(data_path)
            error_msg = f"Failed to read file: {exc}\n    ↳ {uri}"
            if required:
                raise TemplateConfigError(error_msg) from exc
            self._logger.warning(error_msg)
            return None

    def _validate_data_with_schema(
        self, data: Any, schema_path_str: str, key: str, data_file_path: Path = None
    ) -> None:
        """Validate data against JSON Schema.

        Args:
            data: Data to validate
            schema_path_str: Path to schema file
            key: Data key (for error messages)
            data_file_path: Optional path to data file (for clickable URIs)

        Raises:
            TemplateConfigError: If validation fails or schema not found
        """
        try:
            schema_path = self.path_resolver.resolve(schema_path_str, must_exist=True)

            # Validate with optional file path for clickable URIs
            context = f"Inline extra_data key '{key}'" if data_file_path is None else f"Extra data key '{key}'"
            validation_errors = self._schema_validator.validate(data, schema_path, data_file_path, context)

            if validation_errors:
                error_messages = [e.to_string() for e in validation_errors]
                prefix = "inline extra_data" if data_file_path is None else "extra data"
                raise TemplateConfigError(
                    f"Schema validation failed for {prefix} key '{key}':\n"
                    + "\n".join(f"  - {e}" for e in error_messages)
                )

        except (FileNotFoundError, OSError) as exc:
            schema_path_resolved = self.path_resolver.resolve(schema_path_str, must_exist=False)
            uri = FileUriBuilder.create_uri(schema_path_resolved)
            raise TemplateConfigError(f"Schema file not found for key '{key}'\n    ↳ {uri}") from exc

    def _validate_data_helpers_section(self, yaml_data: Dict[str, Any]) -> None:
        """Validate the optional data_helpers section.

        Rules enforced here because JSON schema for templates does not include
        the data_helpers section used by the project tests:
        - If present, data_helpers must be an object.
        - Allowed keys: 'helpers' and 'discovery_paths' only.
        - 'helpers' must be a list of strings if present.
        - 'discovery_paths' must be a list of strings if present.

        Raises:
            TemplateConfigError: when validation fails.
        """
        if "data_helpers" not in yaml_data:
            return

        dh = yaml_data["data_helpers"]
        if not isinstance(dh, dict):
            raise TemplateConfigError("data_helpers must be an object/dictionary")

        allowed = {"helpers", "discovery_paths"}
        for key in dh.keys():
            if key not in allowed:
                raise TemplateConfigError(f"Invalid property in data_helpers: {key}")

        if "helpers" in dh:
            helpers = dh["helpers"]
            if not isinstance(helpers, list):
                raise TemplateConfigError("data_helpers.helpers must be an array of strings")
            for h in helpers:
                if not isinstance(h, str):
                    raise TemplateConfigError("Each helper spec must be a string")

        if "discovery_paths" in dh:
            dps = dh["discovery_paths"]

            if not isinstance(dps, list):
                raise TemplateConfigError("data_helpers.discovery_paths must be an array of strings")
            for p in dps:
                if not isinstance(p, str):
                    raise TemplateConfigError("Each discovery path must be a string")

    def get_templates_with_iteration(self, context: Any) -> List[Dict[str, Any]]:
        """Return templates with parsed iteration info.

        Args:
            context: Context dictionary for iteration expr evaluation

        Returns:
            List of dicts with keys: template_set, iteration_type,
            iteration_data, globals
        """
        result: List[Dict[str, Any]] = []
        globals_data = self.yaml_data.get("globals", {})

        for template_set in self.yaml_data.get("templates", []):
            # Skip disabled templates
            if not template_set.get("enabled", True):
                continue

            iterate = template_set.get("iterate")
            if iterate:
                try:
                    if isinstance(iterate, list):
                        # Array of iteration expressions
                        iteration_data = self._parse_array_iteration(iterate, context)
                    else:
                        # Single iteration expression
                        iteration_data = self._parse_iteration_expression(iterate, context)

                    result.append(
                        {
                            "template_set": template_set,
                            "iteration_type": iteration_data["type"],
                            "iteration_data": iteration_data,
                            "globals": globals_data,
                        }
                    )
                except (ValueError, TypeError, AttributeError, KeyError) as exc:
                    # Iteration parsing errors - collect and continue
                    self.errors.append(f"Invalid iterate syntax '{iterate}': {exc}")
            else:
                # Static template (no iteration)
                result.append(
                    {
                        "template_set": template_set,
                        "iteration_type": "static",
                        "iteration_data": {},
                        "globals": globals_data,
                    }
                )
        return result

    def _parse_iteration_expression(self, iterate_expr: str, context: Any) -> Dict[str, Any]:
        """Parse iteration expression into structured data.

        Supports:
        - Simple: "var in collection"
        - Conditional: "var in collection if condition"
        - Nested: "outer in collection >> inner in outer.items if condition"
        - Union: "var1 in collection1 | var2 in collection2"
        """
        if "|" in iterate_expr:
            # Union iteration (multiple simple iterations)
            return self._parse_union_iteration(iterate_expr, context)

        if ">>" in iterate_expr:
            # Nested iteration
            return self._parse_nested_iteration(iterate_expr, context)

        # Simple iteration
        return self._parse_simple_iteration(iterate_expr, context)

    def _parse_simple_iteration(self, iterate_expr: str, context: Any) -> Dict[str, Any]:
        """Parse simple iteration: 'var in collection [if condition]'"""
        # Split on ' if ' from the right to handle conditions
        if " if " in iterate_expr:
            iteration_part, condition = iterate_expr.rsplit(" if ", 1)
        else:
            iteration_part, condition = iterate_expr, None

        # Parse 'var in collection'
        var, expr = [x.strip() for x in iteration_part.split(" in ", 1)]
        iterable = get_nested_attr_or_key(context, expr)

        if iterable is None or not isinstance(iterable, list):
            raise ValueError(f"Expression '{expr}' returned non-list: {iterable}")

        return {
            "type": "simple",
            "var": var,
            "expr": expr,
            "items": iterable,
            "condition": condition.strip() if condition else None,
        }

    def _parse_nested_iteration(self, iterate_expr: str, context: Any) -> Dict[str, Any]:
        """Parse nested iteration: 'outer in collection >> inner in
        outer.items [if condition]'"""
        # Split on '>>'
        parts = iterate_expr.split(" >> ", 1)
        if len(parts) != 2:
            raise ValueError(f"Invalid nested iteration syntax: {iterate_expr}")

        outer_part = parts[0].strip()
        inner_part = parts[1].strip()

        # Parse outer iteration (simple, no condition)
        outer_var, outer_expr = [x.strip() for x in outer_part.split(" in ", 1)]
        outer_items = get_nested_attr_or_key(context, outer_expr)

        if outer_items is None or not isinstance(outer_items, list):
            raise ValueError(f"Outer expression '{outer_expr}' returned non-list: {outer_items}")

        # Parse inner iteration (may have condition)
        if " if " in inner_part:
            inner_iteration, condition = inner_part.rsplit(" if ", 1)
        else:
            inner_iteration, condition = inner_part, None

        inner_var, inner_expr = [x.strip() for x in inner_iteration.split(" in ", 1)]

        return {
            "type": "nested",
            "outer_var": outer_var,
            "outer_expr": outer_expr,
            "outer_items": outer_items,
            "inner_var": inner_var,
            "inner_expr": inner_expr,
            "condition": condition.strip() if condition else None,
        }

    def _parse_union_iteration(self, iterate_expr: str, context: Any) -> Dict[str, Any]:
        """Parse union iteration: 'var1 in collection1 | var2 in collection2'"""
        # Split on '|'
        parts = [part.strip() for part in iterate_expr.split("|")]

        iterations = []
        for part in parts:
            # Parse each part as a simple iteration
            iteration_data = self._parse_simple_iteration(part, context)
            iterations.append(iteration_data)

        return {"type": "union", "iterations": iterations}

    def _parse_array_iteration(self, iterate_array: List[str], context: Any) -> Dict[str, Any]:
        """Parse array of iteration expressions:
        ['var1 in collection1', 'var2 in collection2']"""
        iterations = []
        for iterate_expr in iterate_array:
            if isinstance(iterate_expr, str):
                # Parse each expression as a simple iteration
                # (no nested in arrays for now)
                if ">>" in iterate_expr:
                    raise ValueError(f"Nested iteration not supported in array syntax: " f"{iterate_expr}")
                iteration_data = self._parse_simple_iteration(iterate_expr, context)
                iterations.append(iteration_data)
            else:
                raise ValueError(f"Array iteration must contain strings: {iterate_expr}")

        return {"type": "array", "iterations": iterations}
