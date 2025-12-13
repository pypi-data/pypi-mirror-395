"""Black Python code formatter implementation."""

import logging
from typing import Any, Dict, Optional

from pytemplify.formatting.base import CodeFormatter, FormattingError

logger = logging.getLogger(__name__)


class BlackFormatter(CodeFormatter):
    """Black Python code formatter.

    Uses the black library to format Python code with opinionated defaults.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize Black formatter.

        Args:
            config: Formatter configuration
        """
        config = config or {}
        super().__init__("black", [".py"])

        # Validate configuration
        self.validate_options(config.get("options", {}))

    def format(self, content: str, options: Optional[Dict[str, Any]] = None) -> str:
        """Format Python code with Black.

        Args:
            content: Python code to format
            options: Black-specific options

        Returns:
            Formatted Python code

        Raises:
            FormattingError: If formatting fails
        """
        options = options or {}

        try:
            import black  # pylint: disable=import-outside-toplevel
        except ImportError as exc:
            raise FormattingError("black not installed. Install with: pip install black", self.name) from exc

        # Extract Black options
        line_length = options.get("line_length", 88)
        string_normalization = options.get("string_normalization", True)
        magic_trailing_comma = options.get("magic_trailing_comma", True)

        # Create Black FileMode
        mode = black.FileMode(
            line_length=line_length,
            string_normalization=string_normalization,
            magic_trailing_comma=magic_trailing_comma,
        )

        try:
            # Format the code
            formatted_code = black.format_str(content, mode=mode)
            return formatted_code
        except black.NothingChanged:
            # Code was already properly formatted
            return content
        except Exception as exc:
            raise FormattingError(f"Black formatting failed: {exc}", self.name) from exc

    def validate_options(self, options: Optional[Dict[str, Any]] = None) -> None:
        """Validate Black-specific options.

        Args:
            options: Options to validate

        Raises:
            FormattingError: If options are invalid
        """
        super().validate_options(options)

        if options is None:
            return

        # Validate line_length
        if "line_length" in options:
            line_length = options["line_length"]
            if not isinstance(line_length, int) or line_length < 1:
                raise FormattingError("line_length must be a positive integer", self.name)

        # Validate boolean options
        boolean_options = ["string_normalization", "magic_trailing_comma"]
        for option in boolean_options:
            if option in options and not isinstance(options[option], bool):
                raise FormattingError(f"{option} must be a boolean", self.name)
