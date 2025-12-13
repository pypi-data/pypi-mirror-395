"""Base code generator for pytemplify.

This module provides the base code generation functionality using Jinja2 templates.
It supports both arbitrary data structures and structured DataDictionary objects.
"""

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Union

from pytemplify.exceptions import BaseGeneratorError, FormattingError
from pytemplify.renderer import TemplateRenderer

from .generation_helpers import (
    DictAttrWrapper,
    EnhancedTemplateRenderer,
    NestedIterationHandler,
    TemplateIterationContext,
    TemplateSetFilter,
)
from .renderer_configurator import RendererConfigurator
from .template_config import TemplateConfig, TemplateConfigError
from .utils import get_nested_attr_or_key
from .validation_integration import ValidationIntegration

# ========================================================================
# BaseCodeGenerator - Main abstract base class for code generators
# ========================================================================


class BaseCodeGenerator(ABC):  # pylint: disable=too-many-instance-attributes
    """Base code generator for pytemplify."""

    def __init__(
        self,
        template_config_filepath: Optional[Path] = None,
        template_filter: Optional[TemplateSetFilter] = None,
        flatten_data: bool = True,
    ) -> None:
        """Initialize BaseCodeGenerator.

        Args:
            template_config_filepath: Optional path to template configuration YAML.
                                     If not provided, must be specified in generate().
            template_filter: Optional filter for template sets
            flatten_data: If True, flattens dd dictionary into root context for easier access

        Example:
            # Traditional: config at init
            gen = MyGenerator(template_config_filepath=Path("templates.yaml"))
            gen.generate()

            # Lazy: config at generate()
            gen = MyGenerator()  # No config!
            gen.generate(template_config_filepath=Path("templates.yaml"))
        """
        # Config is now optional - will be loaded lazily if not provided
        self.template_config = TemplateConfig(template_config_filepath) if template_config_filepath else None
        self._default_config_filepath = template_config_filepath

        self.logger = self._get_logger()
        self.enhanced_renderer = EnhancedTemplateRenderer(self.logger)
        self.iteration_handler = NestedIterationHandler()
        self.template_filter = template_filter
        self.flatten_data = flatten_data
        self._validation = ValidationIntegration(self.logger)

    def _get_logger(self):
        """Get logger instance."""
        return logging.getLogger(__name__)

    # Reserved context keys that should never be overridden by flattened data
    RESERVED_CONTEXT_KEYS = {"dd", "dd_raw", "helpers", "globals", "gg"}

    def _flatten_dict_to_context(self, data: Any) -> Dict[str, Any]:
        """Flatten dictionary data for direct template access.

        Args:
            data: Dictionary or data helper object to flatten

        Returns:
            Flattened dictionary with top-level keys accessible directly.
            Reserved keys (dd, dd_raw, helpers, globals, gg) are excluded.
        """
        if not isinstance(data, dict):
            # Handle data helper objects - try to get raw data
            if hasattr(data, "_raw_data"):
                # Accessing a protected member is necessary to support
                # compatible data helper objects which expose raw data
                # via a private attribute.
                data = data._raw_data  # pylint: disable=protected-access
            elif hasattr(data, "__dict__"):
                data = data.__dict__
            else:
                return {}

        flattened = {}
        conflicts = []

        for key, value in data.items():
            # Check for conflicts with reserved keys
            if key in self.RESERVED_CONTEXT_KEYS:
                conflicts.append(key)
                # Skip this key - reserved keys always win
                continue

            # Flatten all other top-level keys
            # Simple values, lists, and dicts all become accessible at root level
            # This allows {{ project_name }}, {{ services }}, etc.
            flattened[key] = value

        # Log warnings for any conflicts found
        if conflicts:
            # Use lazy formatting to avoid constructing the message when logging
            # is disabled.
            self.logger.warning(
                "Data flattening: Skipped %d key(s) that conflict with reserved names: %s. "
                "These keys are only accessible via dd.%s namespace.",
                len(conflicts),
                ", ".join(conflicts),
                conflicts[0],
            )

        return flattened

    def _get_base_template_context(self) -> Dict[str, Any]:
        """Get base template context with extra_data from template config."""
        # Start with extra_data from template configuration
        if self.template_config and hasattr(self.template_config, "extra_data"):
            context = self.template_config.extra_data.copy()
        else:
            context = {}
        return context

    @abstractmethod
    def _get_template_context(self) -> Dict[str, Any]:
        """Get the template context data."""

    @abstractmethod
    def _get_success_message(self) -> str:
        """Get the success message to display after generation."""

    def _get_template_filters(self) -> Dict[str, Any]:
        """Get custom Jinja2 filters."""
        return {
            "capitalize_first": self._capitalize_first_filter,
            "split": self._split_filter,
        }

    def _get_jinja_env_options(self) -> Dict[str, Any]:
        """Get Jinja2 environment options.

        Override this in subclasses to customize Jinja2 environment behavior.
        These options control how templates are processed and rendered.

        Returns:
            Dictionary of Jinja2 environment options (default: empty dict)

        Common options:
            - trim_blocks (bool): Remove first newline after template tag
            - lstrip_blocks (bool): Strip leading spaces/tabs from start of line to block
            - autoescape (bool): Enable automatic escaping of variables
            - keep_trailing_newline (bool): Keep trailing newline at end of template

        Example:
            class MyGenerator(GenericCodeGenerator):
                def _get_jinja_env_options(self) -> Dict[str, Any]:
                    return {
                        "trim_blocks": True,
                        "lstrip_blocks": True,
                        "autoescape": False
                    }
        """
        return {}

    def _capitalize_first_filter(self, text: str) -> str:
        """Custom Jinja2 filter to capitalize the first letter of a string."""
        if not text:
            return text
        return text[0].upper() + text[1:] if len(text) > 1 else text.upper()

    def _split_filter(self, text: str, delimiter: Optional[str] = None) -> List[str]:
        """Custom Jinja2 filter to split a string by delimiter."""
        if not text:
            return []
        return text.split(delimiter)

    def _render_template_string(self, template_string: str, context: Dict[str, Any]) -> str:
        """Render a template string using pytemplify."""
        renderer = TemplateRenderer(context, "", filters=self._get_template_filters())
        return renderer.render_string(template_string)

    def _resolve_template_folder(self, template_folder_str: str, context: Dict[str, Any]) -> Path:
        """Resolve template folder path, rendering if it contains variables."""
        if "{" in template_folder_str:
            return Path(self._render_template_string(template_folder_str, context))
        return Path(template_folder_str)

    def _get_template_folder_from_set(self, template_set: Dict[str, Any]) -> str:
        """Get template folder from template set."""
        # Support new simplified field name
        if "folder" in template_set:
            return template_set["folder"]
        # Backward compatibility with old field name
        if "template_folder" in template_set:
            return template_set["template_folder"]

        # Provide helpful error with template name
        template_name = template_set.get("name", "<unnamed>")
        raise ValueError(
            f"Template set '{template_name}' is missing required 'folder' field.\n"
            f"Please add 'folder: <path>' to your template configuration.\n"
            f"Example: folder: 'templates/my_template'"
        )

    def _get_output_folder_from_set(self, template_set: Dict[str, Any]) -> Optional[str]:
        """Get output folder from template set."""
        # Support new simplified field name
        if "output" in template_set:
            return template_set["output"]
        # Backward compatibility with old field name
        if "output_folder" in template_set:
            return template_set["output_folder"]
        return None

    def _create_iteration_context(
        self,
        template_set: Dict[str, Any],
        context: Dict[str, Any],
        output_base_dir: Optional[Path],
    ) -> TemplateIterationContext:
        """Create template iteration context."""
        # Resolve template folder using new field name support
        template_folder_str = self._get_template_folder_from_set(template_set)
        template_folder = self._resolve_template_folder(template_folder_str, context)

        # Resolve output directory
        output_dir = self._resolve_output_dir(output_base_dir, template_set, context)

        # Add output_dir to globals
        enhanced_globals = {
            **context.get("globals", {}),
            "output_dir": str(output_dir),
        }
        enhanced_context = {**context, "globals": enhanced_globals}

        return TemplateIterationContext(template_set, enhanced_context, template_folder, output_dir)

    def _resolve_output_dir(
        self,
        output_base_dir: Optional[Path],
        template_set: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Path:
        """Resolve output directory for a given template set."""
        if output_base_dir is None:
            # Default to template config file's parent directory
            # This makes more sense than cwd() - generate relative to config
            if self.template_config and self.template_config.yaml_path:
                output_base_dir = self.template_config.yaml_path.parent
            else:
                output_base_dir = Path.cwd()
        else:
            output_base_dir = output_base_dir.resolve()

        output_folder_str = self._get_output_folder_from_set(template_set)
        if output_folder_str:
            # Render the output folder template string
            rendered_output_folder = self._render_template_string(output_folder_str, context)

            if Path(rendered_output_folder).is_absolute():
                output_dir = Path(rendered_output_folder)
            else:
                output_dir = output_base_dir / rendered_output_folder
        else:
            output_dir = output_base_dir
        return output_dir

    def _generate_iteration_contexts(
        self, output_base_dir: Optional[Path], context_root: Dict[str, Any]
    ) -> Iterator[TemplateIterationContext]:
        """Generate iteration contexts for all template sets."""
        if self.template_filter:
            self.logger.info("Template filtering is active")

        for info in self.template_config.get_templates_with_iteration(context_root):
            template_set = info["template_set"]
            template_name = template_set.get("name", "<unnamed>")

            # Apply template filtering
            if self.template_filter and not self.template_filter.should_include(template_name):
                continue

            globals_data = info["globals"]
            iteration_type = info["iteration_type"]
            iteration_data = info["iteration_data"]

            if iteration_type == "static":
                # Static template - generate once
                context = {**context_root, "globals": globals_data, "gg": globals_data}
                yield self._create_iteration_context(template_set, context, output_base_dir)

            elif iteration_type == "simple":
                # Simple iteration - handle with optional condition
                yield from self._handle_simple_iteration(
                    template_set,
                    globals_data,
                    iteration_data,
                    context_root,
                    output_base_dir,
                )

            elif iteration_type == "nested":
                # Nested iteration - handle with optional condition
                yield from self._handle_nested_iteration(
                    template_set,
                    globals_data,
                    iteration_data,
                    context_root,
                    output_base_dir,
                )

            elif iteration_type == "array":
                # Array iteration - handle multiple simple iterations
                yield from self._handle_array_iteration(
                    template_set,
                    globals_data,
                    iteration_data,
                    context_root,
                    output_base_dir,
                )

    def _handle_simple_iteration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        template_set: Dict[str, Any],
        globals_data: Dict[str, Any],
        iteration_data: Dict[str, Any],
        context_root: Dict[str, Any],
        output_base_dir: Optional[Path],
    ) -> Iterator[TemplateIterationContext]:
        """Handle simple iteration with optional condition."""
        var = iteration_data["var"]
        items = iteration_data["items"]
        condition = iteration_data.get("condition")

        for item in items:
            context = {**context_root, "globals": globals_data, "gg": globals_data, var: item}

            # Apply condition if specified
            if condition is None or self._evaluate_condition(condition, context):
                yield self._create_iteration_context(template_set, context, output_base_dir)

    def _handle_nested_iteration(  # pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-locals
        self,
        template_set: Dict[str, Any],
        globals_data: Dict[str, Any],
        iteration_data: Dict[str, Any],
        context_root: Dict[str, Any],
        output_base_dir: Optional[Path],
    ) -> Iterator[TemplateIterationContext]:
        """Handle nested iteration with optional condition."""
        outer_var = iteration_data["outer_var"]
        outer_items = iteration_data["outer_items"]
        inner_var = iteration_data["inner_var"]
        inner_expr = iteration_data["inner_expr"]
        condition = iteration_data.get("condition")

        for outer_item in outer_items:
            outer_context = {**context_root, "globals": globals_data, "gg": globals_data, outer_var: outer_item}

            # Evaluate inner collection in the context of outer item
            inner_items = self.iteration_handler.evaluate_collection(inner_expr, outer_context)

            for inner_item in inner_items:
                inner_context = {**outer_context, inner_var: inner_item}

                # Apply condition if specified
                if condition is None or self._evaluate_condition(condition, inner_context):
                    yield self._create_iteration_context(template_set, inner_context, output_base_dir)

    def _handle_array_iteration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        template_set: Dict[str, Any],
        globals_data: Dict[str, Any],
        iteration_data: Dict[str, Any],
        context_root: Dict[str, Any],
        output_base_dir: Optional[Path],
    ) -> Iterator[TemplateIterationContext]:
        """Handle array iteration (multiple simple iterations combined)."""
        for iteration in iteration_data["iterations"]:
            var = iteration["var"]
            items = iteration["items"]
            condition = iteration.get("condition")

            for item in items:
                context = {**context_root, "globals": globals_data, "gg": globals_data, var: item}

                # Apply condition if specified
                if condition is None or self._evaluate_condition(condition, context):
                    yield self._create_iteration_context(template_set, context, output_base_dir)

    def _evaluate_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        """Evaluate a condition expression in the given context."""
        try:
            # Try to parse simple attribute access patterns
            if " " in condition:
                # Complex condition, use eval (necessary for dynamic conditions)
                # Wrap context to support dot notation with dict objects (e.g., service.category)
                wrapped_context = DictAttrWrapper.wrap_context(context)
                safe_globals = {"__builtins__": {}}
                return bool(eval(condition, safe_globals, wrapped_context))  # pylint: disable=eval-used

            # Simple attribute access, use safe getter
            result = get_nested_attr_or_key(context, condition)
            return bool(result) if result is not None else False

        except (AttributeError, KeyError, TypeError) as exc:
            # Expected errors when evaluating conditions with missing/wrong data
            self.logger.debug("Condition '%s' evaluated to False: %s", condition, exc)
            return False
        except (SyntaxError, NameError) as exc:
            # Invalid condition syntax
            self.logger.warning("Invalid condition syntax '%s': %s", condition, exc)
            return False

    def _prepare_generation(self, **_kwargs) -> Dict[str, Any]:
        """Prepare for generation with optional runtime configuration.

        Override this in subclasses to dynamically modify helpers, context,
        or other settings based on generation parameters.

        Args:
            **kwargs: Arbitrary keyword arguments passed from generate()

        Returns:
            Dictionary with optional keys:
                - "additional_helpers": List of DataHelper classes to add
                - "additional_context": Dict of extra template context vars
                - "data_filter": Callable to filter/transform data before generation

        Example:
            def _prepare_generation(self, **kwargs):
                mode = kwargs.get("mode", "default")
                if mode == "transmitter":
                    return {
                        "additional_helpers": [TransmitterHelpers],
                        "additional_context": {"mode": "tx"},
                        "data_filter": lambda d: {"messages": d["transmit_msgs"]}
                    }
                return {}
        """
        return {}

    def _build_generation_context(self, generation_config: Dict[str, Any]) -> Dict[str, Any]:
        """Build context for generation, applying generation_config modifications.

        Args:
            generation_config: Config from _prepare_generation()

        Returns:
            Complete context for template generation
        """
        # Get base context from subclass
        context = self._get_template_context()

        # Add globals if available (for string rendering - generate() adds these during iteration)
        if self.template_config and hasattr(self.template_config, "yaml_data"):
            globals_data = self.template_config.yaml_data.get("globals", {})
            if globals_data:
                context["globals"] = globals_data
                context["gg"] = globals_data

        # Add additional context if provided
        additional_context = generation_config.get("additional_context", {})
        if additional_context:
            context.update(additional_context)

        return context

    def _load_and_setup_config(self, template_config_filepath: Optional[Path]) -> Optional[TemplateConfig]:
        """Load and setup template configuration.

        Args:
            template_config_filepath: Config filepath to load, or None to use default

        Returns:
            Original config if switching configs, None otherwise
        """
        config_to_use = template_config_filepath or self._default_config_filepath

        # Validate that we have a config
        if not config_to_use:
            raise BaseGeneratorError(
                "No template configuration provided. "
                "Either pass template_config_filepath to __init__() or to generate()."
            )

        original_config = None

        if template_config_filepath:
            # Config provided at generate() time
            needs_lazy_init = not self.template_config
            if self.template_config:
                # Save existing config for restoration
                original_config = self.template_config

            # Load the new/first config
            self.template_config = TemplateConfig(template_config_filepath)
            self.template_config.load()

            # Handle lazy init or config switch
            if needs_lazy_init and hasattr(self, "_initialize_with_config"):
                self._initialize_with_config(config_already_loaded=True)  # pylint: disable=no-member
            else:
                self._setup_formatting()
        else:
            # Using default config from init
            if not self.template_config:
                raise BaseGeneratorError(
                    "Template config not initialized.\n"
                    "Please provide template_config_filepath when creating the generator:\n"
                    "  GenericCodeGenerator(data, template_config_filepath='templates.yaml')\n"
                    "Or pass it to the generate() method:\n"
                    "  generator.generate(template_config_filepath='templates.yaml')"
                )

            # Ensure config is loaded
            if not hasattr(self.template_config, "yaml_data") or not self.template_config.yaml_data:
                self.template_config.load()

            self._setup_formatting()

        # Check for config errors
        if self.template_config.errors:
            error_count = len(self.template_config.errors)
            error_list = "\n  - ".join(self.template_config.errors)
            raise TemplateConfigError(f"Template configuration has {error_count} error(s):\n  - {error_list}")

        return original_config

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def generate(
        self,
        output_base_dir: Optional[Path] = None,
        template_config_filepath: Optional[Path] = None,
        run_validation: Optional[bool] = None,
        fail_fast_validation: Optional[bool] = None,
        dry_run: bool = False,
        **kwargs,
    ) -> None:
        """Generate code files based on template configuration.

        Args:
            output_base_dir: Optional base directory for output files
            template_config_filepath: Template config to use for this generation.
                                     Required if not provided in __init__.
                                     If provided, overrides the init config for
                                     this generation only.
            run_validation: Override validation setting from templates.yaml.
                           None = use YAML config, True = force validation,
                           False = skip validation
            fail_fast_validation: Stop validation on first failure.
                                 Overrides YAML config if provided.
            dry_run: If True, simulate file generation without writing to disk.
            **kwargs: Additional keyword arguments passed to
                     _prepare_generation() hook

        Raises:
            BaseGeneratorError: If no template config is available
            ValidationError: If validation is enabled and fails

        Examples:
            # Pattern 1: Config at init, simple generate
            gen = MyGenerator(
                data,
                template_config_filepath=Path("templates.yaml")
            )
            gen.generate(Path("./output"))

            # Pattern 2: Config at generate (lazy init)
            gen = MyGenerator(data)
            gen.generate(
                Path("./output"),
                template_config_filepath=Path("templates.yaml")
            )

            # Pattern 3: Multiple generations with different configs
            gen = MyGenerator(data)
            gen.generate(
                Path("./out1"),
                template_config_filepath=Path("config1.yaml"),
                mode="tx"
            )
            gen.generate(
                Path("./out2"),
                template_config_filepath=Path("config2.yaml"),
                mode="rx"
            )

            # Pattern 4: Default config with override
            gen = MyGenerator(
                data,
                template_config_filepath=Path("default.yaml")
            )
            gen.generate(Path("./out1"))  # Uses default.yaml
            gen.generate(
                Path("./out2"),
                template_config_filepath=Path("special.yaml")
            )

            # Pattern 5: With validation control
            gen.generate(Path("./out"), run_validation=True)
            gen.generate(Path("./out"), run_validation=False)
        """
        original_config = None

        try:
            # Load and setup configuration
            original_config = self._load_and_setup_config(template_config_filepath)

            # Convert output directory to absolute path early
            # (ensures validation can find it regardless of working directory)
            if output_base_dir:
                output_base_dir = output_base_dir.resolve()

            # Call hook to prepare for generation (allows dynamic behavior)
            generation_config = self._prepare_generation(**kwargs)

            # Apply generation config (helpers, context modifications, etc.)
            context_root = self._build_generation_context(generation_config)

            # Process all template sets and collect output directories
            output_directories = set()
            for iteration_context in self._generate_iteration_contexts(output_base_dir, context_root):
                self.enhanced_renderer.render_with_patterns(
                    iteration_context,
                    self._get_template_filters(),
                    dry_run=dry_run,
                    manual_section_config=self.template_config.manual_sections_config,
                )
                # Track where files were actually generated
                # Resolve to normalize paths (remove .. and .)
                output_directories.add(iteration_context.output_dir.resolve())

            self.logger.info(self._get_success_message())

            # Run validation if configured - use actual output directories
            self._validation.run_validation_if_configured(
                self.template_config,
                output_directories,
                run_validation=run_validation,
                fail_fast_validation=fail_fast_validation,
                context=context_root,
            )

        except (TemplateConfigError, BaseGeneratorError):
            raise
        except (OSError, IOError) as exc:
            raise BaseGeneratorError(f"File system error during generation: {exc}") from exc
        except Exception as exc:
            raise BaseGeneratorError(f"Unexpected error during generation: {exc}") from exc
        finally:
            # Restore original config if we switched
            if original_config:
                self.template_config = original_config
                self._setup_formatting()

    # ========================================================================
    # STRING RENDERING METHODS - Render templates to strings without file output
    # ========================================================================

    def render_template_to_string(
        self, template_string: str, template_config_filepath: Optional[Path] = None, **kwargs
    ) -> str:
        """Render a template string using the generator's data context without writing to file.

        This method reuses all the context-building logic (helpers, extra_data, flattening)
        but returns the rendered string directly instead of generating files.

        Available in all subclasses of BaseCodeGenerator (GenericCodeGenerator, custom generators, etc.).

        Args:
            template_string: The Jinja2 template string to render
            template_config_filepath: Optional template configuration file (for extra_data, globals, helpers).
                                     If not provided, uses the config from __init__.
            **kwargs: Additional arguments passed to _prepare_generation() hook

        Returns:
            The rendered string

        Raises:
            BaseGeneratorError: If no template config is available or rendering fails
            TemplateConfigError: If template config has errors

        Example:
            >>> # Works with any BaseCodeGenerator subclass
            >>> generator = GenericCodeGenerator(
            ...     data={"project_name": "MyAPI", "version": "1.0.0"},
            ...     template_config_filepath=Path("templates.yaml")
            ... )
            >>> result = generator.render_template_to_string(
            ...     "# {{ dd.project_name }} v{{ dd.version }}"
            ... )
            >>> print(result)
            # MyAPI v1.0.0
        """
        original_config = None
        try:
            # Load and setup configuration if needed
            original_config = self._load_and_setup_config(template_config_filepath)

            # Prepare generation context (applies additional helpers, filters, etc.)
            generation_config = self._prepare_generation(**kwargs)

            # Build the complete template context
            context = self._build_generation_context(generation_config)

            # Create a TemplateRenderer with the context
            filters = self._get_template_filters()
            renderer = self.enhanced_renderer.create_renderer(context, filters)

            # Apply Jinja2 environment options if configured
            jinja_env_options = self._get_jinja_env_options()
            if self.template_config and hasattr(self.template_config, "jinja_env") and self.template_config.jinja_env:
                jinja_env_options = {**self.template_config.jinja_env, **jinja_env_options}
            if jinja_env_options:
                renderer.set_env_options(**jinja_env_options)

            # Render the template string
            rendered = renderer.render_string(template_string)

            return rendered

        except (TemplateConfigError, BaseGeneratorError):
            raise
        except (OSError, IOError) as exc:
            raise BaseGeneratorError(f"File system error during template rendering: {exc}") from exc
        except Exception as exc:
            raise BaseGeneratorError(f"Unexpected error during template rendering: {exc}") from exc
        finally:
            # Restore original config if we switched
            if original_config:
                self.template_config = original_config
                self._setup_formatting()

    def render_template_file_to_string(
        self, template_filepath: Union[Path, str], template_config_filepath: Optional[Path] = None, **kwargs
    ) -> str:
        """Render a template file using the generator's data context without writing to file.

        The template file path can be absolute or relative to the template config file directory.

        Available in all subclasses of BaseCodeGenerator (GenericCodeGenerator, custom generators, etc.).

        Args:
            template_filepath: Path to the Jinja2 template file (absolute or relative to config file)
            template_config_filepath: Optional template configuration file.
                                     If not provided, uses the config from __init__.
            **kwargs: Additional arguments passed to _prepare_generation()

        Returns:
            The rendered string

        Raises:
            BaseGeneratorError: If no template config is available or rendering fails
            TemplateConfigError: If template config has errors
            FileNotFoundError: If template file doesn't exist

        Example:
            >>> # Works with any BaseCodeGenerator subclass
            >>> generator = GenericCodeGenerator(
            ...     data={"user": "Alice"},
            ...     template_config_filepath=Path("config/templates.yaml")
            ... )
            >>> # Relative path (relative to config/templates.yaml)
            >>> result = generator.render_template_file_to_string("templates/email/welcome.j2")
            >>> # Absolute path
            >>> result = generator.render_template_file_to_string(Path("/tmp/custom_template.j2"))
        """
        try:
            # Resolve template path
            resolved_path = self._resolve_template_path(template_filepath, template_config_filepath)

            # Check if template file exists
            if not resolved_path.exists():
                raise FileNotFoundError(f"Template file not found: {resolved_path}")

            # Read the template file
            template_string = resolved_path.read_text(encoding="utf-8")

            # Render using the string rendering method (DRY - reuse existing logic)
            return self.render_template_to_string(template_string, template_config_filepath, **kwargs)

        except (TemplateConfigError, BaseGeneratorError, FileNotFoundError):
            raise
        except (OSError, IOError) as exc:
            raise BaseGeneratorError(f"File system error reading template file: {exc}") from exc
        except Exception as exc:
            raise BaseGeneratorError(f"Unexpected error reading template file: {exc}") from exc

    def _resolve_template_path(
        self, template_filepath: Union[Path, str], template_config_filepath: Optional[Path] = None
    ) -> Path:
        """Resolve template file path (absolute or relative to config file).

        This is a helper method to keep path resolution logic in one place (DRY principle).

        Args:
            template_filepath: Path to template file (absolute or relative)
            template_config_filepath: Optional template config filepath for relative resolution

        Returns:
            Resolved absolute Path object

        Raises:
            BaseGeneratorError: If cannot resolve relative path without config
        """
        template_filepath = Path(template_filepath)

        # If already absolute, return as-is
        if template_filepath.is_absolute():
            return template_filepath

        # Resolve relative paths against template config location
        config_to_use = template_config_filepath or self._default_config_filepath

        if not config_to_use:
            raise BaseGeneratorError(
                "Cannot resolve relative template path without a template configuration file. "
                "Either provide an absolute path or ensure template_config_filepath is set."
            )

        # Resolve relative to the template config directory
        config_path = Path(config_to_use)
        if config_path.is_file():
            return config_path.parent / template_filepath

        # If config_to_use is a directory (shouldn't happen normally), use it directly
        return config_path / template_filepath

    def _setup_formatting(self) -> None:
        """Set up code formatting and Jinja2 environment options.

        This method configures both:
        1. Code formatting (if enabled in configuration)
        2. Jinja2 environment options (via _get_jinja_env_options hook)
        """
        formatter_manager = None

        # Setup formatter if enabled in config
        if self.template_config:
            format_config = self.template_config.format_config
            if format_config and format_config.get("enabled", False):
                try:
                    # Import here to avoid circular imports and make formatting optional
                    from pytemplify.formatting.manager import (  # pylint: disable=import-outside-toplevel
                        FormatterManager,
                    )

                    formatter_manager = FormatterManager(format_config)
                    self.logger.info("Code formatting enabled")

                except ImportError as exc:
                    # Formatting dependencies not installed
                    self.logger.warning("Formatting dependencies not available: %s", exc)
                except FormattingError as exc:
                    # Formatting configuration error - log but continue
                    self.logger.warning("Failed to configure formatting: %s", exc)

        # Always configure renderer (for both formatting and env options)
        self._configure_renderer_formatting(formatter_manager)

    def _configure_renderer_formatting(self, formatter_manager) -> None:
        """Configure the renderer to use formatting and environment options.

        Uses RendererConfigurator helper to inject formatter and Jinja2 options.

        Environment options precedence (highest to lowest):
        1. Hook method (_get_jinja_env_options)
        2. YAML configuration (jinja_env section)

        Args:
            formatter_manager: Optional FormatterManager instance for code formatting
        """
        hook_options = self._get_jinja_env_options()
        RendererConfigurator.configure_renderer(
            self.enhanced_renderer, formatter_manager, self.template_config, hook_options
        )
