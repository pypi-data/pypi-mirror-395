"""
Template rendering helper module for Jinja2 templates.

This module provides functionality for:
- Rendering templates with preservation of manual sections
- Handling template injection
- Managing template folders with automatic searching and conversion
- Support for preserving user-modified sections in regenerated files
"""

import logging
import re
from pathlib import Path
from typing import Any, Callable, Dict, List, Set, Tuple, Type, Union

from jinja2 import Environment, FileSystemLoader, StrictUndefined, Template, UndefinedError

from pytemplify.exceptions import TemplateRendererException
from pytemplify.manual_sections import ManualSectionManager, RenderContext

logger = logging.getLogger(__name__)


class ValidationContext:  # pylint: disable=too-few-public-methods
    """Context for injection validation containing template data and rendering context."""

    def __init__(self, template_str: str, pattern_match: re.Match, render_context: RenderContext):
        self.template_str = template_str
        self.pattern_match = pattern_match
        self.render_context = render_context
        self.remaining_content = template_str[pattern_match.end() :]
        self.pattern_offset = pattern_match.end()


def _strip_template_suffix(filename: str, suffixes: Set[str]) -> str:
    """
    Strip template suffix from filename and determine output extension.

    This function handles both simple extensions (.j2, .jinja2) and complex patterns
    like _c.j2, _h.j2, etc. For complex patterns, it extracts the target extension
    from the pattern (e.g., _c.j2 -> .c).

    Args:
        filename: The filename to process
        suffixes: List of suffix patterns (e.g., ['.j2', '_c.j2', '_h.j2'])

    Returns:
        The filename with template suffix removed and appropriate output extension

    Examples:
        _strip_template_suffix("main_c.j2", ["_c.j2"]) -> "main.c"
        _strip_template_suffix("header_h.j2", ["_h.j2"]) -> "header.h"
        _strip_template_suffix("config.j2", [".j2"]) -> "config"
    """
    for suffix in suffixes:
        if filename.endswith(suffix):
            base = filename[: -len(suffix)]

            # Handle complex patterns like _c.j2 -> .c, _h.j2 -> .h
            if suffix.startswith("_") and "_" in suffix:
                # Extract the target extension from the pattern
                # Pattern: _<ext>.j2 where <ext> is the desired output extension
                parts = suffix.split("_")
                if len(parts) >= 2:
                    # Get the extension part (e.g., 'c' from '_c.j2')
                    target_ext = parts[1].split(".")[0]
                    return f"{base}.{target_ext}"

            # Handle simple extensions like .j2, .jinja2 -> keep original
            return base

    return filename


class TemplateRenderer:
    """
    Template rendering helper class for Jinja2 templates.

    This class provides functionality to:
    - Render templates from strings or files
    - Preserve manually edited sections between template renders
    - Inject content into existing files using regex patterns
    - Process template directories to generate output directories
    """

    # Manual section handling - initialized in __init__
    _manual_section_manager = None

    # Keep these as class attributes for backwards compatibility
    MANUAL_SECTION_START = ManualSectionManager.DEFAULT_START_MARKER
    MANUAL_SECTION_END = ManualSectionManager.DEFAULT_END_MARKER
    MANUAL_SECTION_ID = ManualSectionManager.MANUAL_SECTION_ID
    # Note: Regex patterns are now instance-specific, these class attributes
    # will use default markers
    MANUAL_SECTION_PATTERN = re.compile(
        rf"{MANUAL_SECTION_START}: ({MANUAL_SECTION_ID}(?:\s|$))(.*?){MANUAL_SECTION_END}",
        re.DOTALL,
    )
    MANUAL_SECTION_CHECK_PATTERN = re.compile(
        rf"{MANUAL_SECTION_START}.*?{MANUAL_SECTION_END}",
        re.DOTALL,
    )

    INJECTION_TAG_START = "<!--"
    INJECTION_TAG_END = "-->"
    INJECTION_PATTERN = rf"{INJECTION_TAG_START} injection-pattern: " rf"(?P<name>[a-zA-Z0-9_-]+) {INJECTION_TAG_END}"
    INJECTION_STRING_START = f"{INJECTION_TAG_START} injection-string-start {INJECTION_TAG_END}"
    INJECTION_STRING_END = f"{INJECTION_TAG_START} injection-string-end {INJECTION_TAG_END}"

    # Default template suffixes for backward compatibility
    DEFAULT_TEMPLATE_SUFFIXES: Set[str] = {".j2", ".jinja2", ".inj"}

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(
        self,
        data: Any,
        data_name: str = "",
        filters: Dict[str, Callable] = None,
        auto_register_filters: bool = True,
        dry_run: bool = False,
        manual_section_config: Dict[str, str] = None,
    ) -> None:
        """
        Initialize the TemplateRenderer with data for template rendering.

        Args:
            data: Object or dictionary containing the data for rendering
            data_name: If provided, data will be accessible in templates as data_name.attribute
            filters: Optional dictionary of custom Jinja2 filters
            auto_register_filters: Automatically register built-in filters (default: True)
            dry_run: If True, simulate file writing without making changes (default: False)
            manual_section_config: Configuration for manual sections (start_marker, end_marker)

        Raises:
            ValueError: If data is not a dictionary or object with __dict__ attribute
        """
        self._dry_run = dry_run
        self._manual_section_manager = ManualSectionManager(**(manual_section_config or {}))
        self._env = Environment(keep_trailing_newline=True, undefined=StrictUndefined)
        if not isinstance(data, dict) and not hasattr(data, "__dict__"):
            raise ValueError("Object or dictionary expected")
        self._data: Dict[str, Any] = {data_name: data} if data_name else data
        self.add_data({"raise_exception": self._raise_exception})

        # Initialize formatter manager (will be set later if formatting is enabled)
        self._formatter_manager = None

        # Auto-register built-in filters
        if auto_register_filters:
            # pylint: disable=import-outside-toplevel
            from pytemplify.filters import get_all_filters
            from pytemplify.filters.utility_filters import coalesce, ternary, uuid_generate

            self.add_filters(get_all_filters())
            # Add utility functions as global functions (not just filters)
            self.add_data({"ternary": ternary, "coalesce": coalesce, "uuid_generate": uuid_generate})

        # Add custom filters (these can override built-in filters if needed)
        if filters:
            self.add_filters(filters)

    def _raise_exception(self, message: str) -> None:
        """Raise exception with message"""
        raise TemplateRendererException("", 1, message)

    def _check_manual_section_ids(self, data_string: str, data_name: str, context: RenderContext = None) -> List[str]:
        """
        Check manual section ids for invalid or duplicated ids.

        Delegates to ManualSectionManager for the actual validation.
        """
        return self._manual_section_manager.check_section_ids(data_string, data_name, context)

    def _check_manual_section_structure(self, data_string: str, data_name: str, context: RenderContext = None) -> None:
        """
        Check manual section structure for completeness and nesting.

        Delegates to ManualSectionManager for the actual validation.
        """
        self._manual_section_manager.check_section_structure(data_string, data_name, context)

    def _validate_manual_sections(
        self,
        temp: str,
        rendered: str,
        prev_rendered: str,
        context: RenderContext = None,
        output_file: str = None,
    ) -> None:
        """
        Validate manual sections in template, current rendered and previously rendered.

        Delegates to ManualSectionManager for comprehensive validation.

        Args:
            temp: Template string
            rendered: Rendered content
            prev_rendered: Previously rendered content
            context: Render context for error reporting
            output_file: Output file path for logging new manual sections

        Raises:
            pytemplify.exceptions.ManualSectionError: If manual section validation fails
        """
        # ManualSectionManager raises ManualSectionError from exceptions module
        # when validation fails - we let it propagate naturally
        self._manual_section_manager.validate_sections(temp, rendered, prev_rendered, context, output_file)

    def add_types(self, *custom_types: Union[Type, Callable]) -> None:
        """
        Add types as global variables to the Jinja environment
        This is useful to make enum variants accessible
        """
        type_map = {ty.__name__: ty for ty in custom_types}
        self._env.globals.update(type_map)

    def add_data(self, data: Dict[str, Any]) -> None:
        """
        Add dictionary data to the Jinja environment
        """
        self._env.globals.update(**data)

    def add_filters(self, filters: Dict[str, Callable]) -> None:
        """
        Add custom filters to the Jinja2 environment

        Args:
            filters: Dictionary mapping filter names to filter functions
        """
        self._env.filters.update(filters)

    def set_env_options(self, **options: Any) -> None:
        """
        Set Jinja2 environment options.

        This method allows you to configure multiple Jinja2 environment options at once,
        such as trim_blocks, lstrip_blocks, autoescape, etc.

        Args:
            **options: Keyword arguments representing Jinja2 environment options

        Example:
            renderer.set_env_options(
                trim_blocks=True,
                lstrip_blocks=True,
                autoescape=False
            )

        Common options:
            - trim_blocks: Remove first newline after template tag
            - lstrip_blocks: Strip leading spaces/tabs from start of line to block
            - autoescape: Enable automatic escaping of variables
            - keep_trailing_newline: Keep trailing newline at end of template
        """
        for key, value in options.items():
            if hasattr(self._env, key):
                setattr(self._env, key, value)
            else:
                raise ValueError(f"Invalid Jinja2 environment option: {key}")

    def _extract_jinja2_location(self, exc, default_filename, default_lineno=1):
        """Extract filename and lineno from Jinja2 exception or its cause/context."""
        for err in (
            exc,
            getattr(exc, "__cause__", None),
            getattr(exc, "__context__", None),
        ):
            if err is not None:
                filename = getattr(err, "filename", None)
                lineno = getattr(err, "lineno", None)
                if filename is not None and lineno is not None:
                    return filename, lineno
        return default_filename, default_lineno

    def _find_error_line(self, template_str: str, exc: Exception) -> int:
        """
        Try to find the line number where an error occurred in the template.

        Args:
            template_str: The template string
            exc: The exception that was raised

        Returns:
            Line number where error likely occurred, or 0 if not found
        """
        error_msg = str(exc)

        # Special handling for UndefinedError (missing variables)
        if isinstance(exc, UndefinedError):
            match = re.search(r"'(.+)' is undefined", error_msg)
            if match:
                missing_var = match.group(1)
                for idx, line in enumerate(template_str.splitlines(), 1):
                    if f"{{{{ {missing_var} }}}}" in line or f"{{{{{missing_var}}}}}" in line:
                        return idx

        # General approach: look for keywords from the error message in template lines
        # This helps with method call errors, attribute errors, etc.
        error_keywords = self._extract_error_keywords(error_msg)
        if error_keywords:
            # Find the line with the most keyword matches (best match)
            # This prevents returning the first line that happens to contain common keywords like 'length'
            best_line = 0
            best_match_count = 0
            for idx, line in enumerate(template_str.splitlines(), 1):
                match_count = sum(1 for keyword in error_keywords if keyword in line)
                if match_count > best_match_count:
                    best_match_count = match_count
                    best_line = idx
            if best_line > 0:
                return best_line

        # Fallback: if no keywords found in error message, use template method names
        # This helps when the error message is generic but we can still locate method calls
        template_methods = self._find_template_methods(template_str)
        if template_methods:
            # Find the line with the most method matches (best match)
            best_line = 0
            best_match_count = 0
            for idx, line in enumerate(template_str.splitlines(), 1):
                match_count = sum(1 for method in template_methods if method in line)
                if match_count > best_match_count:
                    best_match_count = match_count
                    best_line = idx
            if best_line > 0:
                return best_line

        return 0  # Could not determine line number

    def _extract_error_keywords(self, error_msg: str) -> List[str]:
        """
        Extract relevant keywords from an error message that might help locate
        the error in the template.
        """
        keywords = []

        # Look for method names (e.g., "getter_expression")
        method_match = re.search(r"(\w+)\s*\(\)", error_msg)
        if method_match:
            keywords.append(method_match.group(1))

        # Look for attribute names (e.g., "specialValueADAS_Long_AebAxReqDetailedState")
        # Match identifiers that are likely to be unique in the template
        identifier_matches = re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]{3,}\b", error_msg)
        for identifier in identifier_matches:
            # Filter out common English words and focus on technical identifiers
            if not identifier.lower() in {
                "must",
                "have",
                "defined",
                "call",
                "error",
                "exception",
                "missing",
                "generic",
                "message",
            }:
                keywords.append(identifier)

        return keywords

    def _find_template_methods(self, template_str: str) -> List[str]:
        """
        Extract method names from template expressions to help locate errors
        when the error message doesn't contain useful keywords.
        """
        # Find all method calls in Jinja2 expressions: {{ obj.method() }}
        method_pattern = re.compile(r"{{\s*[\w.]*\.(\w+)\s*\([^}]*\)\s*}}")
        methods = []
        for match in method_pattern.finditer(template_str):
            methods.append(match.group(1))
        return methods

    def __render_from_string(self, template_str: str, template_path: str = "", context: RenderContext = None) -> str:
        """Render template from string with filename set correctly in case of exception"""

        name = f'Inline template: "{template_str}"' if not template_path else str(template_path)
        if context is None:
            context = RenderContext(name, 1)
        else:
            context.update(filename=name)

        global_vars = self._env.make_globals(None)
        template_class: Type[Template] = getattr(self._env, "template_class")
        try:
            template = template_class.from_code(
                self._env,
                self._env.compile(template_str, filename=name, name=name),
                global_vars,
                None,
            )
            return template.render(**self._data)
        except Exception as exc:
            filename, lineno = self._extract_jinja2_location(exc, name)
            context.update(filename=filename, lineno=lineno)

            # If Jinja2 didn't provide line info, try to find it ourselves
            if lineno == 1:  # Default lineno means no line info was found
                detected_lineno = self._find_error_line(template_str, exc)
                if detected_lineno:
                    context.update(lineno=detected_lineno)

            raise TemplateRendererException(context.filename, context.lineno, str(exc)) from exc

    def render_string(
        self,
        temp: str,
        prev_rendered_string: str = "",
        template_path: str = "",
        context: RenderContext = None,
        output_file: str = None,
    ) -> str:
        """
        Render template string; preserve manual sections if they exist
        `template_path` is shown in the exception when Jinja2 fails. If it is `None`,
        the exception will instead print the entire template.

        Args:
            temp: Template string
            prev_rendered_string: Previously rendered content
            template_path: Template file path for error reporting
            context: Render context
            output_file: Output file path for logging new manual sections
        """
        if context is None:
            context = RenderContext(template_path or "inline", 1)
        rendered_string = self.__render_from_string(temp, template_path, context)
        self._validate_manual_sections(temp, rendered_string, prev_rendered_string, context, output_file)

        # Restore manual sections using centralized ManualSectionManager
        if prev_rendered_string:
            sections = self._manual_section_manager.extract_sections(prev_rendered_string)
            if sections:
                manager = self._manual_section_manager
                rendered_string = manager.restore_sections(rendered_string, sections)

        return rendered_string

    def _validate_injection_start_tag(self, val_ctx: ValidationContext) -> re.Match:
        """Find and validate injection-string-start tag."""
        pattern_lineno = val_ctx.template_str[: val_ctx.pattern_match.start()].count("\n") + 1

        start_match = re.search(re.escape(self.INJECTION_STRING_START), val_ctx.remaining_content)
        if not start_match:
            val_ctx.render_context.update(lineno=pattern_lineno)
            raise TemplateRendererException(
                val_ctx.render_context.filename,
                val_ctx.render_context.lineno,
                f"Missing '{self.INJECTION_STRING_START}' after injection pattern",
            )

        return start_match

    def _validate_injection_end_tag(self, val_ctx: ValidationContext, start_match: re.Match) -> None:
        """Find and validate injection-string-end tag."""
        end_match = re.search(re.escape(self.INJECTION_STRING_END), val_ctx.remaining_content[start_match.end() :])
        if not end_match:
            start_pos_in_template = val_ctx.pattern_offset + start_match.start()
            start_lineno = val_ctx.template_str[:start_pos_in_template].count("\n") + 1
            val_ctx.render_context.update(lineno=start_lineno)
            raise TemplateRendererException(
                val_ctx.render_context.filename,
                val_ctx.render_context.lineno,
                f"Missing '{self.INJECTION_STRING_END}' after '{self.INJECTION_STRING_START}'",
            )

    def _validate_injection_pattern_block(
        self, template_str: str, pattern_match: re.Match, context: RenderContext
    ) -> None:
        """Validate a single injection pattern block."""

        # Create validation context to reduce parameter passing
        val_ctx = ValidationContext(template_str, pattern_match, context)

        # Find and validate start tag
        start_match = self._validate_injection_start_tag(val_ctx)

        # Find and validate end tag
        self._validate_injection_end_tag(val_ctx, start_match)

    def _validate_injection_syntax(self, template_str: str, context: RenderContext = None) -> None:
        """
        Validate the complete syntax of an injection file before processing.

        Args:
            template_str: The template string to validate
            context: Render context for error reporting

        Raises:
            TemplateRendererException: If injection file syntax is invalid
        """
        if context is None:
            context = RenderContext("inline", 1)

        injection_patterns = list(re.finditer(self.INJECTION_PATTERN, template_str))
        for pattern_match in injection_patterns:
            self._validate_injection_pattern_block(template_str, pattern_match, context)

    def inject_string(
        self,
        temp: str,
        prev_rendered_string: str,
        template_path: str = "",
        context: RenderContext = None,
    ) -> str:
        """
        Render template & inject content to the previous rendered string.

        This method processes injection patterns in the template and applies them
        to matching sections in the previous rendered string.

        Args:
            temp: The template string containing injection patterns
            prev_rendered_string: The previously rendered string to modify
            template_path: Optional path to the template (for error reporting)

        Returns:
            The modified string with injections applied

        Raises:
            TemplateRendererException: If injection patterns are invalid
        """
        if context is None:
            context = RenderContext(template_path or "inline", 1)

        # Validate injection syntax before rendering
        self._validate_injection_syntax(temp, context)

        rendered_string = self.__render_from_string(temp, template_path, context)
        modifications: List[Tuple[int, int, str]] = []

        for match in re.finditer(self.INJECTION_PATTERN, rendered_string):
            label = match.group("name")
            section_bodies = rendered_string[match.end() :].split(self.INJECTION_STRING_START)
            pattern_text = section_bodies[0].strip()
            # validate the regex pattern
            try:
                re.compile(pattern_text)
            except re.error as e:
                # compute lineno from match position in rendered_string
                lineno = rendered_string[: match.start()].count("\n") + 1
                if context:
                    context.update(lineno=lineno)
                raise TemplateRendererException(
                    context.filename,
                    context.lineno,
                    f"Invalid regex pattern '{pattern_text}': {e}",
                ) from e
            # validate if 'injection' named capture group exists
            if "(?P<injection>" not in pattern_text:
                lineno = rendered_string[: match.start()].count("\n") + 1
                if context:
                    context.update(lineno=lineno)
                raise TemplateRendererException(
                    context.filename,
                    context.lineno,
                    f"Invalid regex pattern '{pattern_text}': no 'injection' named capture group",
                )
            injection_string = section_bodies[1].split(self.INJECTION_STRING_END)[0]
            self._apply_injections(prev_rendered_string, pattern_text, injection_string, modifications)
            if not modifications:
                logger.warning("Failed to inject '%s':\n%s", label, pattern_text)

        return self._apply_modifications(prev_rendered_string, modifications)

    def _apply_injections(
        self,
        prev_rendered_string: str,
        pattern_text: str,
        injection_string: str,
        modifications: List[Tuple[int, int, str]],
    ) -> None:
        """
        Apply injections based on the pattern and injection string.

        Args:
            prev_rendered_string: The previously rendered string to modify
            pattern_text: The regex pattern to match in the string
            injection_string: The string to inject
            modifications: List to collect the modifications (start, end, replacement)
        """
        for m in re.finditer(pattern_text, prev_rendered_string):
            injection_start = m.start("injection")
            injection_end = m.end("injection")
            modifications.append((injection_start, injection_end, injection_string))

    def _apply_modifications(self, prev_rendered_string: str, modifications: List[Tuple[int, int, str]]) -> str:
        """
        Apply modifications to the previous rendered string.

        Args:
            prev_rendered_string: The string to modify
            modifications: List of tuples (start, end, replacement)

        Returns:
            The modified string with all replacements applied
        """
        modifications.sort(key=lambda x: x[0])
        modified_buffer = []
        last_pos = 0

        for injection_start, injection_end, injection_string in modifications:
            modified_buffer.append(prev_rendered_string[last_pos:injection_start])
            modified_buffer.append(injection_string)
            last_pos = injection_end

        # append the remaining part of the original string
        modified_buffer.append(prev_rendered_string[last_pos:])

        return "".join(modified_buffer)

    def render_file(
        self,
        temp_filepath: Union[Path, str],
        prev_rendered_string: str = "",
        context: RenderContext = None,
    ) -> str:
        """
        Render template with given template file path; preserve manual sections if they exist
        """
        temp_filepath = Path(temp_filepath)
        if not isinstance(temp_filepath, Path):
            temp_filepath = Path(temp_filepath)
        if context is None:
            context = RenderContext(str(temp_filepath), 1)
        with temp_filepath.open(mode="r", encoding="utf-8") as temp_file:
            temp_string = temp_file.read()
            rendered_string = self.render_string(temp_string, prev_rendered_string, str(temp_filepath), context)
        return rendered_string

    def _is_text_file(self, filepath: Path) -> bool:
        """
        Check if the file is a text file by attempting to read it as UTF-8.

        Args:
            filepath: Path to the file to check

        Returns:
            True if file can be read as UTF-8 text (empty files allowed), False otherwise
        """
        try:
            content = filepath.read_bytes()
            if b"\x00" in content:
                return False
            content.decode("utf-8")
            return True
        except (UnicodeDecodeError, IOError):
            return False

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def generate_file(
        self,
        temp_filepath: Union[Path, str],
        output_filepath: Union[Path, str],
        only_template_files: bool = True,
        template_suffixes: Set[str] = None,
        context: RenderContext = None,
    ) -> None:
        """
        Render the given template file and generate the output file.

        This method handles different template types:
        - .j2 files: Jinja2 templates that get rendered
        - .inj files: Templates for injecting content into existing files
        - Other files: Can be copied as-is depending on only_template_files flag

        Special feature: Empty output filenames (rendered as "") are skipped.
        This allows conditional file generation through template naming, e.g.:
        {{"interface" if temp_data.has_interface else ""}}.hpp.j2

        Args:
            temp_filepath: Path to the template file
            output_filepath: Path to the output file
            only_template_files: When True, only render files with template suffixes
            template_suffixes: List of template suffix patterns. Defaults to [".j2", ".jinja2", ".inj"]
                Examples: [".j2", "_c.j2", "_h.j2"] for C/C++ files
            context: Optional render context for error reporting

        Raises:
            TemplateRendererException: If injection target doesn't exist
        """
        if template_suffixes is None:
            template_suffixes = self.DEFAULT_TEMPLATE_SUFFIXES

        temp_filepath = Path(temp_filepath)
        output_filepath = Path(output_filepath)

        # Initialize context if not provided
        if context is None:
            context = RenderContext(str(temp_filepath), 1)

        output_filename = output_filepath.stem
        if not output_filename:
            logger.info("skip output filename: %s", output_filepath)
            return
        if not self._is_text_file(temp_filepath):
            logger.error("Invalid template file: %s", temp_filepath)
            return

        temp_string = self._read_file(temp_filepath)
        if temp_filepath.suffix == ".inj" and temp_string == "":
            logger.info("skip empty injection template: %s", temp_filepath)
            return
        self._env.loader = FileSystemLoader(temp_filepath.parent)
        prev_rendered_string = self._read_file(output_filepath) if output_filepath.exists() else ""

        # Check if this is a template file based on suffixes
        is_template_file = any(str(temp_filepath).endswith(suffix) for suffix in template_suffixes)

        if temp_filepath.suffix == ".inj":
            if not prev_rendered_string:
                context.update(filename=str(output_filepath), lineno=1)
                raise TemplateRendererException(
                    context.filename,
                    context.lineno,
                    f"{output_filepath} is required for injection",
                )
            rendered_string = self.inject_string(temp_string, prev_rendered_string, str(temp_filepath), context)
        elif not is_template_file and only_template_files:
            rendered_string = temp_string
        else:
            rendered_string = self.render_string(
                temp_string, prev_rendered_string, str(temp_filepath), context, output_file=str(output_filepath)
            )

        output_filepath.parent.mkdir(parents=True, exist_ok=True)
        self._write_file(output_filepath, rendered_string)
        logger.info("=> %s generated!", output_filepath)

    def _read_file(self, filepath: Path) -> str:
        """
        Read the content of a file.

        Args:
            filepath: Path to the file to read

        Returns:
            The file content as string, or empty string if file doesn't exist
        """
        if filepath.exists():
            with filepath.open(mode="r", encoding="utf-8") as file:
                return file.read()
        return ""

    def set_formatter_manager(self, formatter_manager) -> None:
        """
        Set the formatter manager for code formatting.

        Args:
            formatter_manager: FormatterManager instance or None to disable formatting
        """
        self._formatter_manager = formatter_manager

    def _write_file(self, filepath: Path, content: str) -> None:
        """
        Write content to a file, applying formatting if enabled.

        Args:
            filepath: Path to the file to write
            content: Content to write to the file
        """
        if self._dry_run:
            logger.info("[DRY-RUN] Would write to %s", filepath)
            return

        # Apply formatting if formatter manager is available and enabled
        if self._formatter_manager and self._formatter_manager.is_enabled():
            try:
                content = self._formatter_manager.format_content(content, str(filepath))
                logger.debug("Applied formatting to %s", filepath)
            except (OSError, IOError) as exc:
                # File system errors during formatting
                logger.error("File error during formatting of %s: %s", filepath, exc)
                raise  # Re-raise file system errors as they indicate serious issues
            except Exception as exc:  # pylint: disable=broad-exception-caught
                # Formatting errors - log but continue with unformatted content
                # This allows generation to continue even if formatting fails
                logger.warning("Formatting failed for %s: %s", filepath, exc)
                # Continue with unformatted content as fallback

        with filepath.open(mode="w", encoding="utf-8") as file:
            file.write(content)

    def generate(
        self,
        temp_path: Union[Path, str],
        output_dir: Union[Path, str],
        only_template_files: bool = True,
        template_suffixes: Set[str] = None,
    ) -> None:
        """
        Main function to render template files and generate output files.

        This function handles both file and directory templates. For directories,
        it recursively processes all files and subdirectories.

        Args:
            temp_path: Path to the template file or directory
            output_dir: Path to the output directory
            only_template_files: When True, only render files with template suffixes
                but still copy other files from the template folder
            template_suffixes: List of template suffix patterns. Defaults to [".j2", ".jinja2", ".inj"]
                Examples: [".j2", "_c.j2", "_h.j2"] for C/C++ files

        Raises:
            FileNotFoundError: If the template path doesn't exist
        """
        if template_suffixes is None:
            template_suffixes = self.DEFAULT_TEMPLATE_SUFFIXES

        temp_path = Path(temp_path)
        if not temp_path.exists():
            temp_path = Path(self.render_string(str(temp_path)))
        output_dir = Path(output_dir)

        if temp_path.exists():
            if temp_path.is_file():
                output_filename = _strip_template_suffix(self.render_string(str(temp_path.name)), template_suffixes)
                if output_filename:
                    output_filepath = output_dir / output_filename
                    self.generate_file(temp_path, output_filepath, only_template_files, template_suffixes)
            elif temp_path.is_dir():
                filename_pattern = "*"
                temp_files = [file for file in temp_path.rglob(filename_pattern) if file.is_file()]
                for temp_filepath in temp_files:
                    # render folder or file name in Path and remove template suffix
                    output_filename = _strip_template_suffix(
                        self.render_string(str(temp_filepath.name)), template_suffixes
                    )
                    if output_filename:
                        output_filepath = Path(
                            _strip_template_suffix(
                                self.render_string(str(temp_filepath)),
                                template_suffixes,
                            )
                        )
                        output_filepath = output_dir / output_filepath.relative_to(temp_path)
                        self.generate_file(temp_filepath, output_filepath, only_template_files, template_suffixes)
        else:
            raise FileNotFoundError(f"File not found: {temp_path}")
