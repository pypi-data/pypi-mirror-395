"""Cross-platform file URI generation utilities.

Provides clickable file URIs for both Windows and Linux that work in modern IDEs
like VSCode, PyCharm, and terminal emulators.
"""

from pathlib import Path, PureWindowsPath
from typing import Optional
from urllib.parse import quote


class FileUriBuilder:
    r"""Builds clickable file URIs for error messages (cross-platform).

    File URI Format:
    - Linux:   file:///path/to/file.yaml:line:column
    - Windows: file:///C:/path/to/file.yaml:line:column

    Supports:
    - Line numbers
    - Column numbers (optional)
    - URL encoding for special characters
    - Both Windows (C:\) and Linux (/) path formats
    """

    @staticmethod
    def create_uri(file_path: Path, line: Optional[int] = None, column: Optional[int] = None) -> str:
        """Create a clickable file URI.

        Args:
            file_path: Path to file (will be converted to absolute)
            line: Optional line number (1-indexed)
            column: Optional column number (1-indexed)

        Returns:
            Clickable file URI string

        Examples:
            >>> FileUriBuilder.create_uri(Path("/home/user/config.yaml"), line=42)
            'file:///home/user/config.yaml:42'

            >>> FileUriBuilder.create_uri(Path("C:\\Users\\test\\config.yaml"), line=10, column=5)
            'file:///C:/Users/test/config.yaml:10:5'
        """
        # Detect Windows-style paths and preserve them even on non-Windows hosts.
        if FileUriBuilder._looks_like_windows_path(str(file_path)):
            windows_path = PureWindowsPath(str(file_path))
            path_str = windows_path.as_posix()
        else:
            abs_path = file_path.resolve()
            path_str = abs_path.as_posix()

        # URL encode the path (preserve slashes and colons)
        encoded_path = quote(path_str, safe="/:")

        # Build URI based on platform
        if encoded_path.startswith("/"):
            # Unix-style absolute path: /path/to/file
            uri = f"file://{encoded_path}"
        else:
            # Windows-style path: C:/path/to/file
            uri = f"file:///{encoded_path}"

        # Append line number if provided
        if line is not None:
            uri += f":{line}"

            # Append column number if provided
            if column is not None:
                uri += f":{column}"

        return uri

    @staticmethod
    def _looks_like_windows_path(path_str: str) -> bool:
        """Heuristic to detect Windows paths regardless of host OS."""
        return len(path_str) >= 2 and path_str[1] == ":" and path_str[0].isalpha() or path_str.startswith("\\\\")

    @staticmethod
    def create_uri_from_string(path_str: str, line: Optional[int] = None, column: Optional[int] = None) -> str:
        """Create URI from path string.

        Args:
            path_str: Path string (may be relative or absolute)
            line: Optional line number
            column: Optional column number

        Returns:
            Clickable file URI string
        """
        # Handle special cases
        if not path_str or path_str.startswith("Inline"):
            # Can't create URI for inline content
            return path_str

        # Convert to Path and create URI
        path = Path(path_str)

        # If relative, convert to absolute
        if not path.is_absolute():
            path = path.resolve()

        return FileUriBuilder.create_uri(path, line, column)

    @staticmethod
    def format_error_with_uri(
        message: str,
        file_path: Path,
        line: Optional[int] = None,
        column: Optional[int] = None,
        context: Optional[str] = None,
    ) -> str:
        """Format error message with clickable file URI.

        Args:
            message: Error message
            file_path: Path to file where error occurred
            line: Optional line number
            column: Optional column number
            context: Optional context string (e.g., "Schema validation")

        Returns:
            Formatted error message with clickable URI

        Example Output:
            Schema validation failed: 'name' is a required property
                ↳ file:///home/user/config.yaml:42:10
        """
        uri = FileUriBuilder.create_uri(file_path, line, column)

        if context:
            formatted = f"{context}: {message}\n    ↳ {uri}"
        else:
            formatted = f"{message}\n    ↳ {uri}"

        return formatted


def extract_line_from_json_path(file_path: Path, json_path: tuple) -> Optional[int]:
    """Extract line number from file based on JSON path.

    This is a best-effort attempt to find the line number in the source file
    where a specific JSON/YAML path exists.

    Args:
        file_path: Path to JSON/YAML file
        json_path: Tuple of keys/indices representing path (e.g., ('servers', 0, 'hostname'))

    Returns:
        Line number (1-indexed) or None if not found

    Note:
        This is approximate - YAML/JSON libraries don't preserve source locations.
        For precise line numbers, consider using ruamel.yaml or similar.
    """
    if not file_path.exists() or not json_path:
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Build search pattern from JSON path
        # For path like ('servers', 0, 'hostname'), search for "hostname"
        if json_path:
            search_key = str(json_path[-1])

            # Search for the key in the file
            for line_num, line in enumerate(lines, start=1):
                if search_key in line:
                    return line_num

        return None

    except (OSError, UnicodeDecodeError):
        return None
