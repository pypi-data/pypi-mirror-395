"""Centralized exception hierarchy for pytemplify.

This module defines all custom exceptions used throughout the pytemplify package.
All exceptions inherit from PyTemplifyError for easy catching of all pytemplify-specific errors.
"""

import os
import re
from pathlib import Path
from urllib.parse import quote

from pytemplify.file_uri_utils import FileUriBuilder


class PyTemplifyError(Exception):
    """Base exception for all pytemplify errors."""


class TemplateError(PyTemplifyError):
    """Base exception for template-related errors."""


class TemplateRendererException(TemplateError):
    """Exception raised during template rendering with clickable file URI encoding.

    This exception includes file and line number information for better error reporting,
    with support for clickable file URIs in IDEs.
    """

    def __init__(self, filename: str, lineno: int, message: str):
        """Initialize TemplateRendererException.

        Args:
            filename: Template file where error occurred
            lineno: Line number where error occurred
            message: Error message
        """
        # Create main error message with clickable file URI
        formatted_message = self._format_error_message(filename, lineno, message)
        super().__init__(formatted_message)
        self.filename = filename
        self.lineno = lineno
        self.message = message

    def _format_error_message(self, filename: str, lineno: int, message: str) -> str:
        """Format error message with clickable file URI for consistency."""
        if not filename:
            return f'"":{lineno}: {message}'

        # Check if this is an inline template (special case - no file URI needed)
        if filename.startswith("Inline template:"):
            return f"{filename}:{lineno}: {message}"

        # Check if this is a Windows path (with drive letter like C:\ or C:/)
        # Match pattern: drive letter + colon (+ optional slash/backslash)
        is_windows_path = bool(re.match(r"^[a-zA-Z]:[/\\]", filename))

        # Convert relative paths to absolute paths for consistent handling
        # But preserve Windows paths even when running on non-Windows systems
        if not is_windows_path and not os.path.isabs(filename):
            filename = os.path.abspath(filename)

        # Always use file URI for consistency and clickability
        file_uri = self._create_file_uri(filename, lineno)
        return f"{message}\n    ↳ {file_uri}"

    def _create_file_uri(self, filename: str, lineno: int) -> str:
        """Create a clickable file URI with proper URL encoding."""
        # Check if this is a Windows path (with drive letter like C:\ or C:/)
        # Match pattern: drive letter + colon (+ optional slash/backslash)
        is_windows_path = bool(re.match(r"^[a-zA-Z]:[/\\]", filename))

        # Convert to absolute path if needed, but preserve Windows paths
        if is_windows_path or os.path.isabs(filename):
            abs_path = filename
        else:
            abs_path = os.path.abspath(filename)

        # Convert Windows backslashes to forward slashes for URI compatibility
        # File URIs always use forward slashes, even on Windows
        abs_path = abs_path.replace("\\", "/")

        # URL encode the path for proper file URI format
        # Keep forward slashes and colons (for drive letters) unencoded
        encoded_path = quote(abs_path, safe="/:")

        # Create file URI with proper format
        # Windows: file:///C:/path/to/file:lineno
        # Unix: file:///path/to/file:lineno
        # Add third slash for absolute paths
        if encoded_path.startswith("/"):
            # Unix-style absolute path
            file_uri = f"file://{encoded_path}:{lineno}"
        else:
            # Windows-style path with drive letter (C:/...)
            file_uri = f"file:///{encoded_path}:{lineno}"

        return file_uri

    def get_file_uri(self) -> str:
        """Get clickable file URI for IDEs.

        Returns:
            File URI in format file://path:line or empty string if no location info
        """
        if self.filename and self.lineno:
            return self._create_file_uri(self.filename, self.lineno)
        return ""


class ManualSectionError(TemplateRendererException):
    """Exception raised when MANUAL SECTION validation fails.

    This occurs when there are issues with section structure,
    duplicate section IDs, or incompatible manual sections.
    """

    def __init__(self, filename: str, lineno: int, message: str = "MANUAL SECTION validation failed"):
        """Initialize ManualSectionError.

        Args:
            filename: File where manual section error occurred
            lineno: Line number where error occurred
            message: Error message describing the validation failure
        """
        super().__init__(filename, lineno, message)


class TemplateConfigError(TemplateError):
    """Exception raised for invalid template configuration.

    Supports optional clickable file URIs for better IDE integration.
    """

    def __init__(self, message: str, file_path=None, line=None):
        """Initialize TemplateConfigError.

        Args:
            message: Error message
            file_path: Optional path to file where error occurred (Path object)
            line: Optional line number
        """
        # Only add URI if file_path is provided
        if file_path:
            # Ensure file_path is a Path object
            if not isinstance(file_path, Path):
                file_path = Path(file_path)

            uri = FileUriBuilder.create_uri(file_path, line)
            full_message = f"{message}\n    ↳ {uri}"
        else:
            full_message = message

        super().__init__(full_message)
        self.file_path = file_path
        self.line = line


class GeneratorError(PyTemplifyError):
    """Base exception for generator errors."""


class BaseGeneratorError(GeneratorError):
    """Exception raised during code generation."""


class FormattingError(PyTemplifyError):
    """Exception raised during code formatting.

    This can be used to indicate formatting failures that should not stop generation.
    """


class ValidationError(PyTemplifyError):
    """Exception raised during validation.

    Attributes:
        validator_name: Name of the validator that raised the error
    """

    def __init__(self, message: str, validator_name: str = ""):
        """Initialize ValidationError.

        Args:
            message: Error message
            validator_name: Name of validator that failed
        """
        self.validator_name = validator_name
        super().__init__(message)


class HelperError(PyTemplifyError):
    """Base exception for data helper errors."""


class HelperLoaderError(HelperError):
    """Exception raised when loading data helpers fails."""
