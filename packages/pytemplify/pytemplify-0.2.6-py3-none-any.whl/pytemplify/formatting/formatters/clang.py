"""Clang-format C/C++ code formatter implementation."""

import logging
from typing import Any, Dict, Optional

from pytemplify.formatting.base import FormattingError
from pytemplify.formatting.command import CommandFormatter

logger = logging.getLogger(__name__)


class ClangFormatFormatter(CommandFormatter):
    """Clang-format C/C++ code formatter.

    Uses clang-format command-line tool to format C/C++ code.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize Clang-format formatter.

        Args:
            config: Formatter configuration
        """
        config = config or {}

        # Set default command if not provided
        if "command" not in config:
            config["command"] = "clang-format ${input} > ${output}"

        # Set supported extensions
        config["extensions"] = [".c", ".cpp", ".cc", ".cxx", ".h", ".hpp", ".hxx"]

        super().__init__(config)

    def validate_options(self, options: Optional[Dict[str, Any]] = None) -> None:
        """Validate Clang-format-specific options.

        Args:
            options: Options to validate

        Raises:
            FormattingError: If options are invalid
        """
        super().validate_options(options)

        if options is None:
            return

        # Validate style option
        if "style" in options:
            style = options["style"]
            valid_styles = ["LLVM", "Google", "Chromium", "Mozilla", "WebKit", "Microsoft", "GNU", "file", "inherit"]
            if style not in valid_styles and not style.startswith("{"):
                raise FormattingError(f"style must be one of: {valid_styles} or a JSON style object", self.name)

        # Validate boolean options
        boolean_options = ["fallback-style", "sort-includes", "verbose"]
        for option in boolean_options:
            if option in options and not isinstance(options[option], bool):
                raise FormattingError(f"{option} must be a boolean", self.name)

        # Validate integer options
        integer_options = ["column-limit", "tab-width", "indent-width", "continuation-indent-width"]
        for option in integer_options:
            if option in options:
                value = options[option]
                if not isinstance(value, int) or value < 0:
                    raise FormattingError(f"{option} must be a non-negative integer", self.name)
