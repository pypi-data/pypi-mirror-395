"""Generic data-driven code generator for pytemplify.

This module provides a concrete implementation of the base code generator
for arbitrary data structures (typically loaded from JSON).
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, Union

from pytemplify.data_helpers import DataHelper, HelperLoader, wrap_with_helpers
from pytemplify.exceptions import BaseGeneratorError, HelperLoaderError
from pytemplify.generator.template_config import TemplateConfigError

from .base_generator import BaseCodeGenerator, TemplateSetFilter

logger = logging.getLogger(__name__)


class GenericCodeGenerator(BaseCodeGenerator):
    """Generic data-driven code generator with data_helpers support.

    This class handles code generation from arbitrary data structures using
    Jinja2 templates. The data is accessible in templates via the 'dd' key.
    Supports data_helpers for enhanced template capabilities.

    Can be used directly or extended for custom generators.

    Attributes:
        data: Dictionary containing arbitrary data (potentially wrapped)
        raw_data: Original unwrapped data (also used for dynamic re-wrapping)
        helpers: List of DataHelper classes applied to data
    """

    def __init__(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        data: Dict[str, Any],
        template_config_filepath: Optional[Path] = None,
        template_filter: Optional[TemplateSetFilter] = None,
        helpers: Optional[List[Type[DataHelper]]] = None,
        helper_specs: Optional[List[str]] = None,
        helper_discovery_paths: Optional[List[Union[str, Path]]] = None,
        flatten_data: Optional[bool] = None,
    ) -> None:
        """Initialize GenericCodeGenerator with optional data_helpers support.

        Args:
            data: Dictionary containing arbitrary data
            template_config_filepath: Optional path to template config file.
                                     If not provided, must be specified in generate().
            template_filter: Optional filter for template sets
            helpers: Optional list of DataHelper classes to apply
            helper_specs: Optional list of helper specifications (module.Class)
            helper_discovery_paths: Optional paths to discover helpers from
            flatten_data: If True, flattens dd dict into root context. If None, uses YAML config.

        Note:
            Precedence: CLI flatten_data > YAML config > default (True)
            Helper precedence: helpers > _get_helpers_list() > helper_specs >
                              helper_discovery_paths > YAML config

        Example:
            # Traditional pattern
            gen = GenericCodeGenerator(data, Path("templates.yaml"))
            gen.generate()

            # Lazy pattern - reusable for multiple configs
            gen = GenericCodeGenerator(data, helpers=[MyHelpers])
            gen.generate(Path("out1"), template_config_filepath=Path("config1.yaml"))
            gen.generate(Path("out2"), template_config_filepath=Path("config2.yaml"))
        """
        # Initialize base class (config is now optional)
        super().__init__(template_config_filepath, template_filter, flatten_data if flatten_data is not None else True)

        # Store raw data and config preferences
        self.raw_data = data  # Also used for dynamic re-wrapping
        self.helpers: List[Type[DataHelper]] = []
        self._explicit_flatten_data = flatten_data
        # Group helper configuration into a dict to reduce instance attributes
        self._helper_config = {
            "explicit": helpers,
            "specs": helper_specs,
            "discovery_paths": helper_discovery_paths,
        }

        # Only initialize with config if provided
        if template_config_filepath:
            self._initialize_with_config()
        else:
            # Lazy mode - defer initialization until generate()
            logger.info("Template config not provided - will be loaded at generate() time")
            # Set minimal defaults
            self.data = data
            self._base_helpers = []

    def _initialize_with_config(self, config_already_loaded: bool = False) -> None:
        """Initialize helpers and data wrapping with loaded config.

        Called either from __init__ (if config provided) or from generate() (lazy mode).

        Args:
            config_already_loaded: If True, skip loading config (already done)
        """
        # Load template config to access YAML helpers configuration
        if not config_already_loaded:
            try:
                self.template_config.load()
            except TemplateConfigError as exc:
                logger.warning("TemplateConfig.load() failed, continuing without YAML helpers: %s", exc)
                self.template_config.yaml_data = {}
                self.template_config.errors.append(str(exc))

        # Validate data (hook for subclasses)
        self._validate_data(self.raw_data)

        # Transform data (hook for subclasses)
        self.raw_data = self._transform_data(self.raw_data)

        # Collect helpers from all sources
        all_helpers = self._collect_all_helpers()

        # Remove duplicates while preserving order
        seen = set()
        unique_helpers = []
        for helper in all_helpers:
            if helper not in seen:
                seen.add(helper)
                unique_helpers.append(helper)

        self.helpers = unique_helpers
        if self.helpers:
            self.helpers = HelperLoader.validate_helpers(self.helpers, self.raw_data)
            logger.info("Using %d validated data helpers", len(self.helpers))

        # Apply flatten_data precedence: CLI > YAML config > default (True)
        if self._explicit_flatten_data is not None:
            self.flatten_data = self._explicit_flatten_data
        else:
            # Use YAML config value if available
            if self.template_config and hasattr(self.template_config, "flatten_data"):
                self.flatten_data = self.template_config.flatten_data

        # Wrap data with helpers if any are available
        if self.helpers:
            self.data = wrap_with_helpers(self.raw_data, self.helpers)
            logger.info("Data wrapped with helpers - enhanced properties available in templates")
        else:
            self.data = self.raw_data
            logger.info("No data helpers applied - using raw data")

        # Store base helpers for dynamic additions later
        self._base_helpers = self.helpers.copy() if self.helpers else []

        # Setup formatting
        self._setup_formatting()

    #  ========================================================================
    # HOOK METHODS - Override these in subclasses for customization
    # ========================================================================

    def _get_helpers_list(self) -> List[Type[DataHelper]]:
        """Return list of DataHelper classes to apply to data.

        Override this in subclasses to provide domain-specific helpers.
        This is called during initialization and has higher precedence than
        helper_specs and helper_discovery_paths, but lower than constructor helpers.

        Returns:
            List of DataHelper classes (default: empty list)

        Example:
            class MyProjectGenerator(GenericCodeGenerator):
                def _get_helpers_list(self):
                    return [ProjectHelpers, ServiceHelpers, ModuleHelpers]
        """
        return []

    def _validate_data(self, data: Dict[str, Any]) -> None:
        """Validate loaded data before processing.

        Override this in subclasses to add custom validation logic.
        Called before data transformation and helper application.

        Args:
            data: The data to validate

        Raises:
            BaseGeneratorError: If validation fails

        Example:
            def _validate_data(self, data: Dict[str, Any]) -> None:
                required = ["project_name", "version"]
                missing = [f for f in required if f not in data]
                if missing:
                    raise BaseGeneratorError(f"Missing fields: {missing}")
        """
        # Default: no validation

    def _transform_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform data before wrapping with helpers.

        Override this in subclasses to add defaults, normalize structure,
        or perform any data transformations. Called after validation but
        before helper application.

        Args:
            data: The data to transform

        Returns:
            Transformed data

        Example:
            def _transform_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
                # Add defaults
                data.setdefault("version", "1.0.0")
                data.setdefault("author", "Unknown")
                # Normalize nested structures
                for service in data.get("services", []):
                    service.setdefault("enabled", True)
                return data
        """
        return data

    def _get_additional_context(self) -> Dict[str, Any]:
        """Return additional context variables for templates.

        Override this in subclasses to add custom template variables
        beyond dd, dd_raw, globals, etc.

        Returns:
            Dictionary of additional context variables (default: empty dict)

        Example:
            def _get_additional_context(self) -> Dict[str, Any]:
                return {
                    "generated_at": datetime.now().isoformat(),
                    "generator_version": "2.0.0"
                }
        """
        return {}

    def _get_generation_name(self) -> str:
        """Return name describing what's being generated.

        Used in success messages. Override to customize.

        Returns:
            Name of what's being generated (default: "Generic code")

        Example:
            def _get_generation_name(self) -> str:
                return f"{self.raw_data.get('project_name', 'project')} code"
        """
        return "Generic code"

    # ========================================================================
    # INTERNAL HELPER METHODS - Usually no need to override
    # ========================================================================

    def _collect_all_helpers(self) -> List[Type[DataHelper]]:
        """Collect helpers from all sources in precedence order.

        Precedence: constructor helpers > _get_helpers_list() > helper_specs >
                    helper_discovery_paths > YAML config

        Returns:
            List of helper classes from all sources
        """
        all_helpers = []

        # 1. Direct helper classes from constructor (highest precedence)
        explicit_helpers = self._helper_config.get("explicit")
        if explicit_helpers:
            all_helpers.extend(explicit_helpers)
            logger.info("Added %d direct helper classes", len(explicit_helpers))

        # 2. Helpers from _get_helpers_list() override method
        subclass_helpers = self._get_helpers_list()
        if subclass_helpers:
            all_helpers.extend(subclass_helpers)
            logger.info("Added %d helpers from _get_helpers_list()", len(subclass_helpers))

        # 3. Helper specifications
        all_helpers.extend(self._load_helpers_from_specs(self._helper_config.get("specs")))

        # 4. Discovery paths
        all_helpers.extend(self._load_helpers_from_discovery_paths(self._helper_config.get("discovery_paths")))

        # 5. YAML configuration helpers (loaded in _load_yaml_helpers)
        yaml_helpers = self._load_yaml_helpers()
        all_helpers.extend(yaml_helpers)

        return all_helpers

    def _load_helpers_from_specs(self, helper_specs: Optional[List[str]]) -> List[Type[DataHelper]]:
        """Load helpers from specification strings.

        Args:
            helper_specs: List of helper specifications (module.Class format)

        Returns:
            List of loaded DataHelper classes
        """
        helpers = []
        if not helper_specs:
            return helpers

        for spec in helper_specs:
            try:
                spec_helpers = HelperLoader.load_helpers_from_string(spec)
                helpers.extend(spec_helpers)
                logger.info("Loaded %d helpers from spec: %s", len(spec_helpers), spec)
            except (ImportError, AttributeError, HelperLoaderError) as exc:
                # Helper loading errors - log warning but continue with other helpers
                logger.warning("Failed to load helpers from spec '%s': %s", spec, exc)

        return helpers

    def _load_helpers_from_discovery_paths(
        self, discovery_paths: Optional[List[Union[str, Path]]]
    ) -> List[Type[DataHelper]]:
        """Load helpers from discovery paths.

        Args:
            discovery_paths: List of directory paths to search for helpers

        Returns:
            List of discovered DataHelper classes
        """
        if not discovery_paths:
            return []

        # Resolve relative paths against template config location
        resolved_paths = []
        for path in discovery_paths:
            if isinstance(path, str) and not Path(path).is_absolute():
                # Only resolve against template config if we have one
                if self.template_config and hasattr(self.template_config, "yaml_path"):
                    resolved_path = self.template_config.yaml_path.parent / path
                    resolved_paths.append(str(resolved_path))
                else:
                    # No template config yet - use path as-is
                    resolved_paths.append(path)
            else:
                resolved_paths.append(path)

        try:
            discovered = HelperLoader.discover_helpers(resolved_paths)
            if discovered:
                logger.info("Discovered %d helpers from paths", len(discovered))
            return discovered
        except (ImportError, OSError, IOError, HelperLoaderError) as exc:
            # Helper discovery errors - log warning but continue
            logger.warning("Helper discovery failed: %s", exc)
            return []

    def _load_yaml_helpers(self) -> List[Type[DataHelper]]:
        """Load helpers from YAML configuration if present."""
        yaml_helpers = []

        # Can't load YAML helpers if we don't have a config yet
        if not self.template_config or not hasattr(self.template_config, "yaml_data"):
            return yaml_helpers

        try:
            # Access the already loaded template config
            config = self.template_config.yaml_data
            data_helpers_config = config.get("data_helpers", {})

            # Load from helper specifications
            helper_specs = data_helpers_config.get("helpers", [])
            yaml_helpers.extend(self._load_helpers_from_specs(helper_specs))

            # Load from discovery paths
            discovery_paths = data_helpers_config.get("discovery_paths", [])
            # Resolve relative paths against template config location
            resolved_paths = []
            for path in discovery_paths:
                if isinstance(path, str) and not Path(path).is_absolute():
                    resolved_path = self.template_config.yaml_path.parent / path
                    resolved_paths.append(str(resolved_path))
                else:
                    resolved_paths.append(path)
            yaml_helpers.extend(self._load_helpers_from_discovery_paths(resolved_paths))

        except (KeyError, TypeError, AttributeError) as exc:
            # YAML config parsing errors - log warning but continue
            logger.warning("Failed to load helpers from YAML config: %s", exc)

        return yaml_helpers

    @classmethod
    def from_json_file(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        cls,
        json_filepath: Path,
        template_config_filepath: Path,
        template_filter: Optional[TemplateSetFilter] = None,
        helpers: Optional[List[Type[DataHelper]]] = None,
        helper_specs: Optional[List[str]] = None,
        helper_discovery_paths: Optional[List[Union[str, Path]]] = None,
    ) -> "GenericCodeGenerator":
        """Create GenericCodeGenerator from JSON file with optional data_helpers.

        Args:
            json_filepath: Path to JSON data file
            template_config_filepath: Path to template config file
            template_filter: Optional filter for template sets
            helpers: Optional list of DataHelper classes to apply
            helper_specs: Optional list of helper specifications (module.Class)
            helper_discovery_paths: Optional paths to discover helpers from

        Returns:
            GenericCodeGenerator instance

        Raises:
            BaseGeneratorError: If JSON file cannot be loaded
        """
        try:
            with open(json_filepath, "r", encoding="utf-8") as json_file:
                json_data = json.load(json_file)
            return cls(
                json_data, template_config_filepath, template_filter, helpers, helper_specs, helper_discovery_paths
            )
        except (json.JSONDecodeError, IOError) as exc:
            raise BaseGeneratorError(f"Failed to load JSON file {json_filepath}: {exc}") from exc

    def _build_generation_context(self, generation_config: Dict[str, Any]) -> Dict[str, Any]:
        """Build context for generation with dynamic helper support.

        Overrides BaseCodeGenerator to support dynamic helper addition and data filtering.

        Args:
            generation_config: Config from _prepare_generation()

        Returns:
            Complete context for template generation
        """
        # Handle additional helpers by re-wrapping data
        additional_helpers = generation_config.get("additional_helpers", [])
        if additional_helpers:
            # Combine base helpers with additional ones
            all_helpers = self._base_helpers + additional_helpers
            # Validate additional helpers before using them
            validated_helpers = HelperLoader.validate_helpers(all_helpers, self.raw_data)
            # Re-wrap data with combined helpers
            if validated_helpers:
                self.data = wrap_with_helpers(self.raw_data, validated_helpers)
                # Update self.helpers for context building
                self.helpers = validated_helpers
                logger.info(
                    "Data re-wrapped with %d helpers (%d base + %d additional)",
                    len(validated_helpers),
                    len(self._base_helpers),
                    len(additional_helpers),
                )

        # Apply data filter if provided
        data_filter = generation_config.get("data_filter")
        if data_filter and callable(data_filter):
            # Filter/transform the data - use raw data for filtering
            filtered_data = data_filter(self.raw_data)
            # Re-wrap filtered data with all helpers
            all_helpers = self._base_helpers + additional_helpers
            if all_helpers:
                # Validate helpers with filtered data
                validated_helpers = HelperLoader.validate_helpers(all_helpers, filtered_data)
                self.data = wrap_with_helpers(filtered_data, validated_helpers)
                # Update self.helpers for context building
                self.helpers = validated_helpers
            else:
                self.data = filtered_data
            logger.info("Data filtered for generation")

        # Call parent to build context with additional context
        return super()._build_generation_context(generation_config)

    def _get_template_context(self) -> Dict[str, Any]:
        """Get template context with data accessible via 'dd' key.

        Returns:
            Template context with:
            - dd: Main data (wrapped with helpers if available)
            - dd_raw: Original unwrapped data (for edge cases)
            - helpers: Information about applied helpers
            - flattened data keys (if flatten_data=True): Direct access to top-level data
            - Additional context from _get_additional_context() hook
        """
        base_context = self._get_base_template_context()

        # Start with base context
        context = {
            **base_context,
        }

        # If flattening is enabled, add flattened data first
        # This allows {{ project_name }} instead of {{ dd.project_name }}
        if self.flatten_data:
            flattened = self._flatten_dict_to_context(self.data)
            context.update(flattened)

        # Always add dd namespace for explicit access
        context["dd"] = self.data
        context["dd_raw"] = self.raw_data

        # Add helper information for advanced template usage
        if self.helpers:
            context["helpers"] = {
                "applied": [h.__name__ for h in self.helpers if h and hasattr(h, "__name__")],
                "count": len(self.helpers),
                "enabled": True,
            }
        else:
            context["helpers"] = {
                "applied": [],
                "count": 0,
                "enabled": False,
            }

        # Add additional context from subclass hook
        additional = self._get_additional_context()
        context.update(additional)

        return context

    def _get_success_message(self) -> str:
        """Get success message for generic generation."""
        # Use _get_generation_name() hook
        name = self._get_generation_name()
        if self.helpers:
            return f"{name} generation completed successfully with {len(self.helpers)} data helpers!"
        return f"{name} generation completed successfully!"
