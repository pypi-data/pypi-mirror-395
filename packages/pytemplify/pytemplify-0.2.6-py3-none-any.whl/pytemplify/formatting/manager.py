"""Formatter manager for coordinating code formatting operations.

This module provides the FormatterManager class that coordinates
all formatting operations based on configuration and file types.
"""

import logging
from pathlib import Path
from typing import Any, Dict, Optional

from pytemplify.formatting.base import CodeFormatter, FormattingError

logger = logging.getLogger(__name__)


class FormatterManager:
    """Manages code formatters and coordinates formatting operations.

    This class is responsible for:
    - Loading formatter configurations
    - Creating and caching formatter instances
    - Selecting appropriate formatters for file types
    - Coordinating the formatting process
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize the formatter manager.

        Args:
            config: Formatting configuration dictionary
        """
        self.config = config or {}
        self.formatters: Dict[str, CodeFormatter] = {}
        self._formatter_cache: Dict[str, CodeFormatter] = {}

        # Load formatters if config is provided
        if self.config:
            self._load_formatters()

    def _load_formatters(self) -> None:
        """Load and initialize formatters from configuration."""
        if not self.config.get("enabled", False):
            logger.debug("Formatting is disabled")
            return

        formatters_config = self.config.get("formatters", {})

        for file_pattern, formatter_config in formatters_config.items():
            if not formatter_config.get("enabled", True):
                continue

            formatter_type = formatter_config.get("type")
            if not formatter_type:
                logger.warning("No type specified for formatter %s", file_pattern)
                continue

            try:
                formatter = self._create_formatter(formatter_type, formatter_config)
                if formatter:
                    # Store formatter by file pattern
                    self.formatters[file_pattern] = formatter
                    logger.debug("Loaded formatter %s for pattern %s", formatter_type, file_pattern)
            except (ImportError, FormattingError, ValueError, TypeError) as exc:
                # Formatter creation errors - log warning but continue loading other formatters
                logger.warning("Failed to create formatter %s: %s", formatter_type, exc)

    def _create_formatter(self, formatter_type: str, config: Dict[str, Any]) -> Optional[CodeFormatter]:
        """Create a formatter instance based on type and configuration.

        Args:
            formatter_type: Type of formatter to create
            config: Formatter configuration

        Returns:
            Configured formatter instance or None if creation fails
        """
        # Import here to avoid circular imports
        from pytemplify.formatting.builtin import BuiltinFormatter  # pylint: disable=import-outside-toplevel
        from pytemplify.formatting.command import CommandFormatter  # pylint: disable=import-outside-toplevel

        try:
            if formatter_type == "command":
                return CommandFormatter(config)
            # Assume it's a built-in formatter
            return BuiltinFormatter(formatter_type, config)
        except (ImportError, FormattingError, ValueError, TypeError, AttributeError) as exc:
            # Formatter instantiation errors - log and return None
            logger.warning("Failed to create %s formatter: %s", formatter_type, exc)
            return None

    def get_formatter_for_file(self, file_path: str) -> Optional[CodeFormatter]:
        """Get the appropriate formatter for a given file.

        Args:
            file_path: Path to the file to format

        Returns:
            Formatter instance or None if no formatter matches
        """
        if not self.config.get("enabled", False):
            return None

        # Check ignore patterns first
        if self._should_ignore_file(file_path):
            return None

        # Find matching formatter
        for pattern, formatter in self.formatters.items():
            if self._matches_pattern(file_path, pattern):
                return formatter

        return None

    def _matches_pattern(self, file_path: str, pattern: str) -> bool:
        """Check if a file path matches a formatter pattern.

        Args:
            file_path: Path to check
            pattern: Pattern to match against (supports | for multiple extensions)

        Returns:
            True if the file matches the pattern
        """
        file_path_obj = Path(file_path)
        file_ext = file_path_obj.suffix.lower()

        # Split pattern on | for multiple extensions
        extensions = [ext.strip().lower() for ext in pattern.split("|")]

        return file_ext in extensions

    def _should_ignore_file(self, file_path: str) -> bool:
        """Check if a file should be ignored based on ignore patterns.

        Args:
            file_path: Path to check

        Returns:
            True if the file should be ignored
        """
        ignore_patterns = self.config.get("defaults", {}).get("ignore_patterns", [])

        for pattern in ignore_patterns:
            if pattern.startswith("*."):
                # Glob pattern like *.min.js
                suffix = pattern[1:]  # Remove *
                if file_path.endswith(suffix):
                    return True
            elif "*" in pattern:
                # More complex glob patterns - simplified check
                if pattern.replace("*", "") in file_path:
                    return True

        return False

    def format_content(self, content: str, file_path: str) -> str:
        """Format content for the given file path.

        Args:
            content: Content to format
            file_path: Path to the file being formatted

        Returns:
            Formatted content (or original content if no formatter applies)

        Raises:
            FormattingError: If formatting fails and no fallback is available
        """
        formatter = self.get_formatter_for_file(file_path)
        if not formatter:
            return content

        try:
            # Check if manual sections should be preserved
            preserve_manual = self.config.get("defaults", {}).get("preserve_manual_sections", True)

            if preserve_manual:
                # Extract manual sections before formatting
                manual_sections = formatter._extract_manual_sections(content)  # pylint: disable=protected-access

                # Format the content
                formatted_content = formatter.format(content, self._get_formatter_options(file_path))

                # Restore manual sections
                if manual_sections:
                    formatted_content = formatter._restore_manual_sections(  # pylint: disable=protected-access
                        formatted_content, manual_sections
                    )

                return formatted_content
            # Format without manual section preservation
            return formatter.format(content, self._get_formatter_options(file_path))

        except (OSError, IOError, UnicodeDecodeError) as exc:
            # File system or encoding errors - wrap as FormattingError
            formatter_name = formatter.name if formatter else "unknown"
            raise FormattingError(str(exc), formatter_name, file_path) from exc
        except (TypeError, ValueError, AttributeError) as exc:
            # Formatter execution errors - wrap as FormattingError
            formatter_name = formatter.name if formatter else "unknown"
            raise FormattingError(str(exc), formatter_name, file_path) from exc

    def _get_formatter_options(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Get formatter options for a specific file.

        Args:
            file_path: Path to the file

        Returns:
            Formatter options dictionary or None
        """
        # Find the formatter config for this file
        for pattern in self.formatters:
            if self._matches_pattern(file_path, pattern):
                # Find the config for this pattern
                formatters_config = self.config.get("formatters", {})
                return formatters_config.get(pattern, {}).get("options", {})

        return None

    def is_enabled(self) -> bool:
        """Check if formatting is enabled globally.

        Returns:
            True if formatting is enabled
        """
        return self.config.get("enabled", False)
