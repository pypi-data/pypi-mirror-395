"""Base classes for code formatters.

This module defines the abstract base class for all code formatters
and provides common functionality for formatter implementations.
"""

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional

from pytemplify.manual_sections import ManualSectionManager

logger = logging.getLogger(__name__)


class FormattingError(Exception):
    """Raised when code formatting fails."""

    def __init__(self, message: str, formatter_name: str = "", file_path: str = "") -> None:
        self.formatter_name = formatter_name
        self.file_path = file_path
        super().__init__(f"Formatting failed with {formatter_name}: {message}")


class CodeFormatter(ABC):
    """Abstract base class for code formatters.

    All formatters must implement the format method and provide
    basic validation and file type support checking.
    """

    # Shared manual section manager for all formatters
    _manual_section_manager = ManualSectionManager()

    def __init__(self, name: str, supported_extensions: list[str]) -> None:
        """Initialize the formatter.

        Args:
            name: Human-readable name of the formatter
            supported_extensions: List of file extensions this formatter supports
        """
        self.name = name
        self.supported_extensions = supported_extensions

    @abstractmethod
    def format(self, content: str, options: Optional[Dict[str, Any]] = None) -> str:
        """Format the given content.

        Args:
            content: The content to format
            options: Formatter-specific options

        Returns:
            The formatted content

        Raises:
            FormattingError: If formatting fails
        """
        pass  # pylint: disable=unnecessary-pass

    def supports_file(self, file_path: str) -> bool:
        """Check if this formatter supports the given file.

        Args:
            file_path: Path to the file to check

        Returns:
            True if the formatter supports this file type
        """
        file_ext = Path(file_path).suffix.lower()
        return file_ext in self.supported_extensions

    def validate_options(self, options: Optional[Dict[str, Any]] = None) -> None:
        """Validate formatter options.

        Args:
            options: Options to validate

        Raises:
            FormattingError: If options are invalid
        """
        if options is None:
            return

        # Basic validation - can be overridden by subclasses
        if not isinstance(options, dict):
            raise FormattingError(f"Options must be a dictionary, got {type(options)}", self.name)

    def _extract_manual_sections(self, content: str) -> Dict[str, str]:
        """Extract manual sections from content for preservation.

        Delegates to ManualSectionManager for consistent behavior.

        Args:
            content: The content to extract sections from

        Returns:
            Dictionary mapping section IDs to their content
        """
        return self._manual_section_manager.extract_sections(content)

    def _restore_manual_sections(self, content: str, sections: Dict[str, str]) -> str:
        """Restore manual sections into formatted content.

        Delegates to ManualSectionManager for consistent behavior.

        Args:
            content: The formatted content
            sections: Dictionary of section ID to section content

        Returns:
            Content with manual sections restored
        """
        return self._manual_section_manager.restore_sections(content, sections)

    def _remove_manual_sections(self, content: str) -> str:
        """Remove manual sections from content.

        This is useful before formatting to prevent formatters from modifying
        the content inside manual sections.

        Delegates to ManualSectionManager for consistent behavior.

        Args:
            content: The content with manual sections

        Returns:
            Content with manual sections removed
        """
        return self._manual_section_manager.remove_sections(content)
