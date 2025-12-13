"""Built-in formatters that use Python libraries.

This module provides formatters that use Python libraries like black,
prettier, and other formatters with Python APIs.
"""

import importlib
import logging
import os
import subprocess
import tempfile
from typing import Any, Dict, Optional

import clang_format

from pytemplify.formatting.base import CodeFormatter, FormattingError

logger = logging.getLogger(__name__)


class BuiltinFormatter(CodeFormatter):
    """Formatter that uses built-in Python libraries.

    This formatter supports formatters that have Python APIs like:
    - black (Python)
    - prettier (JavaScript/TypeScript/Web)
    """

    def __init__(self, formatter_type: str, config: Dict[str, Any]) -> None:
        """Initialize the built-in formatter.

        Args:
            formatter_type: Type of formatter (e.g., 'black', 'prettier')
            config: Formatter configuration
        """
        self.formatter_type = formatter_type
        self.config = config

        # Set supported extensions based on formatter type
        supported_extensions = self._get_supported_extensions(formatter_type)
        super().__init__(f"builtin-{formatter_type}", supported_extensions)

        # Validate configuration
        self.validate_options(config.get("options", {}))

    def _get_supported_extensions(self, formatter_type: str) -> list[str]:
        """Get supported file extensions for a formatter type.

        Args:
            formatter_type: The formatter type

        Returns:
            List of supported file extensions
        """
        extension_map = {
            "black": [".py"],
            "prettier": [".js", ".ts", ".jsx", ".tsx", ".json", ".css", ".html", ".md", ".yaml", ".yml"],
            "autopep8": [".py"],
            "yapf": [".py"],
            "cpp_format": [".c", ".cpp", ".cc", ".cxx", ".h", ".hpp", ".hxx"],
        }

        return extension_map.get(formatter_type, [])

    def format(self, content: str, options: Optional[Dict[str, Any]] = None) -> str:
        """Format content using the appropriate built-in formatter.

        Args:
            content: Content to format
            options: Formatter-specific options

        Returns:
            Formatted content

        Raises:
            FormattingError: If formatting fails
        """
        options = options or {}

        # Extract manual sections for preservation
        manual_sections = self._extract_manual_sections(content)

        try:
            if self.formatter_type == "black":
                formatted_content = self._format_with_black(content, options)
            elif self.formatter_type == "prettier":
                formatted_content = self._format_with_prettier(content, options)
            elif self.formatter_type == "autopep8":
                formatted_content = self._format_with_autopep8(content, options)
            elif self.formatter_type == "yapf":
                formatted_content = self._format_with_yapf(content, options)
            elif self.formatter_type == "cpp_format":
                formatted_content = self._format_with_cpp_format(content, options)
            else:
                raise FormattingError(f"Unsupported built-in formatter: {self.formatter_type}", self.name)

            # Restore manual sections
            return self._restore_manual_sections(formatted_content, manual_sections)
        except ImportError as exc:
            raise FormattingError(
                f"Required formatter library not installed: {exc}. "
                f"Please install the appropriate package for {self.formatter_type}",
                self.name,
            ) from exc
        except Exception as exc:
            raise FormattingError(f"Formatting failed: {exc}", self.name) from exc

    def _format_with_black(self, content: str, options: Dict[str, Any]) -> str:
        """Format Python code with black.

        Args:
            content: Python code to format
            options: Black-specific options

        Returns:
            Formatted Python code
        """
        try:
            import black  # pylint: disable=import-outside-toplevel
        except ImportError as exc:
            raise FormattingError("black not installed", self.name) from exc

        # Extract black options
        mode = black.FileMode(
            line_length=options.get("line_length", 88),
            string_normalization=options.get("string_normalization", True),
            magic_trailing_comma=options.get("magic_trailing_comma", True),
        )

        try:
            return black.format_str(content, mode=mode)
        except black.NothingChanged:
            return content
        except Exception as exc:
            raise FormattingError(f"Black formatting failed: {exc}", self.name) from exc

    def _format_with_prettier(self, content: str, options: Dict[str, Any]) -> str:
        """Format code with prettier.

        Args:
            content: Code to format
            options: Prettier-specific options

        Returns:
            Formatted code
        """
        try:
            from prettier import format as prettier_format  # pylint: disable=import-outside-toplevel
        except ImportError:
            # Fallback to node-prettier if python-prettier not available
            raise FormattingError("prettier not installed", self.name) from None

        # Prettier options
        prettier_options = {
            "parser": options.get("parser", "babel"),  # Default parser
            "printWidth": options.get("printWidth", 80),
            "tabWidth": options.get("tabWidth", 2),
            "useTabs": options.get("useTabs", False),
            "semi": options.get("semi", True),
            "singleQuote": options.get("singleQuote", False),
            "quoteProps": options.get("quoteProps", "as-needed"),
            "trailingComma": options.get("trailingComma", "es5"),
            "bracketSpacing": options.get("bracketSpacing", True),
            "bracketSameLine": options.get("bracketSameLine", False),
            "arrowParens": options.get("arrowParens", "always"),
        }

        try:
            return prettier_format(content, **prettier_options)
        except Exception as exc:
            raise FormattingError(f"Prettier formatting failed: {exc}", self.name) from exc

    def _format_with_autopep8(self, content: str, options: Dict[str, Any]) -> str:
        """Format Python code with autopep8.

        Args:
            content: Python code to format
            options: autopep8-specific options

        Returns:
            Formatted Python code
        """
        module = self._resolve_optional_module("autopep8")
        if module is None:
            raise FormattingError("autopep8 not installed", self.name)

        # autopep8 options
        autopep8_options = {
            "max_line_length": options.get("max_line_length", 79),
            "aggressive": options.get("aggressive", 0),
            "experimental": options.get("experimental", False),
        }

        try:
            return module.fix_code(content, options=autopep8_options)
        except Exception as exc:
            raise FormattingError(f"autopep8 formatting failed: {exc}", self.name) from exc

    def _format_with_yapf(self, content: str, options: Dict[str, Any]) -> str:
        """Format Python code with yapf.

        Args:
            content: Python code to format
            options: yapf-specific options

        Returns:
            Formatted Python code
        """
        module = self._resolve_optional_module("yapf")
        if module is None:
            raise FormattingError("yapf not installed", self.name)

        # yapf style configuration
        style_config = options.get("style_config", "pep8")

        try:
            formatted_code, _ = module.yapf_api.FormatCode(content, style_config=style_config)
            return formatted_code
        except Exception as exc:
            raise FormattingError(f"yapf formatting failed: {exc}", self.name) from exc

    def _resolve_optional_module(self, module_name: str):
        """Resolve optional formatter modules allowing test doubles."""
        existing = globals().get(module_name)
        if existing is not None:
            if getattr(existing, "side_effect", None):
                return None
            return existing
        try:
            return importlib.import_module(module_name)
        except ImportError:
            return None

    def _format_with_cpp_format(self, content: str, options: Dict[str, Any]) -> str:
        """Format C/C++ code using clang-format."""

        # Get options and manual sections
        style = options.get("style", "Google")
        manual_sections = self._extract_manual_sections(content)

        # Remove manual sections from content before formatting
        # This prevents clang-format from modifying content inside manual sections
        content_without_sections = self._remove_manual_sections(content)

        # Build style config and format
        style_config = self._build_clang_format_style(style)
        input_file_path = self._create_temp_file(content_without_sections)

        try:
            self._run_clang_format(input_file_path, style_config)
            formatted_content = self._read_formatted_file(input_file_path)
            return self._restore_manual_sections_if_needed(formatted_content, manual_sections)
        except subprocess.CalledProcessError as exc:
            raise FormattingError(f"clang-format failed: {exc.stderr}", self.name) from exc
        finally:
            self._cleanup_temp_file(input_file_path)

    def _build_clang_format_style(self, style: str) -> str:
        """Build clang-format style configuration string."""
        if isinstance(style, str):
            return f"{{BasedOnStyle: {style}}}"

        # For dict style, use all user-specified options
        style_config = "{"
        for key, value in style.items():
            style_config += (
                f"{key}: {'true' if value else 'false'}, " if isinstance(value, bool) else f"{key}: {value}, "
            )
        # Remove trailing comma and space, add closing brace
        style_config = style_config.rstrip(", ") + "}"
        return style_config

    def _create_temp_file(self, content: str) -> str:
        """Create a temporary file with the content, handling encoding properly."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".cpp", delete=False, encoding="utf-8") as input_file:
            input_file.write(content)
            return input_file.name

    def _run_clang_format(self, file_path: str, style_config: str) -> None:
        """Run clang-format on the file."""
        cmd = [clang_format.get_executable("clang-format"), "-style", style_config, "-i", file_path]
        subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=True)

    def _read_formatted_file(self, file_path: str) -> str:
        """Read the formatted content from the file with encoding fallback."""
        # Try UTF-8 first (most common)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            # Try common Windows encodings
            for encoding in ["cp1252", "latin1", "iso-8859-1"]:
                try:
                    with open(file_path, "r", encoding=encoding) as f:
                        content = f.read()
                    # Convert to UTF-8 for consistent processing
                    return content.encode("utf-8", errors="replace").decode("utf-8")
                except UnicodeDecodeError:
                    continue

            # Last resort: read as binary and decode with error handling
            with open(file_path, "rb") as f:
                content = f.read()
            return content.decode("utf-8", errors="replace")

    def _restore_manual_sections_if_needed(self, content: str, manual_sections: Dict[str, str]) -> str:
        """Restore manual sections if they exist."""
        if manual_sections:
            return self._restore_manual_sections(content, manual_sections)
        return content

    def _cleanup_temp_file(self, file_path: str) -> None:
        """Clean up the temporary file."""
        try:
            os.unlink(file_path)
        except OSError:
            pass

    def validate_options(self, options: Optional[Dict[str, Any]] = None) -> None:
        """Validate formatter options.

        Args:
            options: Options to validate

        Raises:
            FormattingError: If options are invalid
        """
        super().validate_options(options)

        if options is None:
            return

        # Type-specific validation
        if self.formatter_type == "black":
            self._validate_black_options(options)
        elif self.formatter_type == "prettier":
            self._validate_prettier_options(options)
        elif self.formatter_type == "cpp_format":
            self._validate_cpp_format_options(options)

    def _validate_black_options(self, options: Dict[str, Any]) -> None:
        """Validate black-specific options."""
        if "line_length" in options and not isinstance(options["line_length"], int):
            raise FormattingError("black line_length must be an integer", self.name)

    def _validate_prettier_options(self, options: Dict[str, Any]) -> None:
        """Validate prettier-specific options."""
        valid_parsers = [
            "babel",
            "typescript",
            "css",
            "less",
            "scss",
            "json",
            "json5",
            "jsonc",
            "graphql",
            "markdown",
            "mdx",
            "html",
            "vue",
            "angular",
            "lwc",
            "yaml",
        ]
        if "parser" in options and options["parser"] not in valid_parsers:
            raise FormattingError(f"prettier parser must be one of: {valid_parsers}", self.name)

    def _validate_cpp_format_options(self, options: Dict[str, Any]) -> None:
        """Validate cpp_format-specific options."""
        if "style" in options and not isinstance(options["style"], (str, dict)):
            raise FormattingError("cpp_format style must be a string or dict", self.name)
        if "indent_width" in options and not isinstance(options["indent_width"], int):
            raise FormattingError("cpp_format indent_width must be an integer", self.name)
