"""Prettier code formatter implementation."""

import logging
from typing import Any, Dict, Optional

from pytemplify.formatting.base import CodeFormatter, FormattingError

logger = logging.getLogger(__name__)


class PrettierFormatter(CodeFormatter):
    """Prettier code formatter.

    Uses the prettier library to format various web languages including
    JavaScript, TypeScript, JSON, CSS, HTML, and Markdown.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize Prettier formatter.

        Args:
            config: Formatter configuration
        """
        config = config or {}
        super().__init__(
            "prettier",
            [
                ".js",
                ".jsx",
                ".ts",
                ".tsx",
                ".json",
                ".jsonc",
                ".css",
                ".scss",
                ".less",
                ".html",
                ".xml",
                ".md",
                ".yaml",
                ".yml",
            ],
        )

        # Validate configuration
        self.validate_options(config.get("options", {}))

    def format(self, content: str, options: Optional[Dict[str, Any]] = None) -> str:
        """Format code with Prettier.

        Args:
            content: Code to format
            options: Prettier-specific options

        Returns:
            Formatted code

        Raises:
            FormattingError: If formatting fails
        """
        options = options or {}

        try:
            from prettier import format as prettier_format  # pylint: disable=import-outside-toplevel
        except ImportError as exc:
            raise FormattingError("prettier not installed. Install with: pip install prettier", self.name) from exc

        # Build Prettier options
        prettier_options = self._build_prettier_options(options)

        try:
            # Format the code
            formatted_code = prettier_format(content, **prettier_options)
            return formatted_code
        except Exception as exc:
            raise FormattingError(f"Prettier formatting failed: {exc}", self.name) from exc

    def _build_prettier_options(self, options: Dict[str, Any]) -> Dict[str, Any]:
        """Build Prettier options dictionary.

        Args:
            options: User-provided options

        Returns:
            Options dictionary for prettier.format()
        """
        # Default options
        prettier_options = {
            "printWidth": 80,
            "tabWidth": 2,
            "useTabs": False,
            "semi": True,
            "singleQuote": False,
            "quoteProps": "as-needed",
            "trailingComma": "es5",
            "bracketSpacing": True,
            "bracketSameLine": False,
            "arrowParens": "always",
            "endOfLine": "lf",
        }

        # Override with user options
        prettier_options.update(options)

        # Handle parser option specially - determine from file extension if not specified
        if "parser" not in prettier_options:
            # This will be set by prettier based on file content, but we can provide hints
            pass

        return prettier_options

    def validate_options(self, options: Optional[Dict[str, Any]] = None) -> None:
        """Validate Prettier-specific options.

        Args:
            options: Options to validate

        Raises:
            FormattingError: If options are invalid
        """
        super().validate_options(options)

        if options is None:
            return

        # Validate numeric options
        self._validate_numeric_options(options)

        # Validate boolean options
        self._validate_boolean_options(options)

        # Validate enum options
        self._validate_enum_options(options)

    def _validate_numeric_options(self, options: Dict[str, Any]) -> None:
        """Validate numeric options."""
        # Validate printWidth
        if "printWidth" in options:
            print_width = options["printWidth"]
            if not isinstance(print_width, int) or print_width < 1:
                raise FormattingError("printWidth must be a positive integer", self.name)

        # Validate tabWidth
        if "tabWidth" in options:
            tab_width = options["tabWidth"]
            if not isinstance(tab_width, int) or tab_width < 1:
                raise FormattingError("tabWidth must be a positive integer", self.name)

    def _validate_boolean_options(self, options: Dict[str, Any]) -> None:
        """Validate boolean options."""
        boolean_options = [
            "useTabs",
            "semi",
            "singleQuote",
            "bracketSpacing",
            "bracketSameLine",
            "jsxSingleQuote",
            "vueIndentScriptAndStyle",
        ]
        for option_name in boolean_options:
            if option_name in options and not isinstance(options[option_name], bool):
                raise FormattingError(f"{option_name} must be a boolean", self.name)

    def _validate_enum_options(self, options: Dict[str, Any]) -> None:
        """Validate enum options."""
        # Validate quoteProps
        if "quoteProps" in options:
            valid_quote_props = ["as-needed", "consistent", "preserve"]
            if options["quoteProps"] not in valid_quote_props:
                raise FormattingError(f"quoteProps must be one of: {valid_quote_props}", self.name)

        # Validate trailingComma
        if "trailingComma" in options:
            valid_trailing_comma = ["es5", "none", "all"]
            if options["trailingComma"] not in valid_trailing_comma:
                raise FormattingError(f"trailingComma must be one of: {valid_trailing_comma}", self.name)

        # Validate arrowParens
        if "arrowParens" in options:
            valid_arrow_parens = ["avoid", "always"]
            if options["arrowParens"] not in valid_arrow_parens:
                raise FormattingError(f"arrowParens must be one of: {valid_arrow_parens}", self.name)

        # Validate endOfLine
        if "endOfLine" in options:
            valid_end_of_line = ["auto", "lf", "crlf", "cr"]
            if options["endOfLine"] not in valid_end_of_line:
                raise FormattingError(f"endOfLine must be one of: {valid_end_of_line}", self.name)
