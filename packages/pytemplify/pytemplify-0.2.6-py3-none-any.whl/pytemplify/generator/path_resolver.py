"""Cross-platform path resolution utilities for template configuration.

This module provides utilities for resolving file paths in template configurations,
handling Windows and Linux path differences transparently.
"""

import logging
import os
import re
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class PathResolver:
    r"""Cross-platform path resolution utility.

    Handles Windows and Linux path differences transparently:
    - Path separators (\ vs /)
    - Drive letters (C:\ on Windows)
    - Environment variables (%VAR% and ${VAR})
    - Home directory expansion (~)
    - Absolute vs relative path detection

    All paths are resolved relative to a base directory (typically config.yaml's parent).
    """

    def __init__(self, base_path: Path):
        """Initialize path resolver.

        Args:
            base_path: Base directory for resolving relative paths (e.g., config.yaml's directory)
        """
        self.base_path = base_path.resolve()  # Always work with absolute paths

    def resolve(self, path_str: str, must_exist: bool = False) -> Path:
        """Resolve path string to absolute Path object.

        Resolution order:
        1. Expand environment variables (both ${VAR} and %VAR% on Windows)
        2. Expand home directory (~)
        3. Normalize path separators
        4. Convert to absolute path if relative
        5. Resolve symlinks and '..' references

        Args:
            path_str: Path string (may contain env vars, ~, relative/absolute)
            must_exist: If True, validate that resolved path exists

        Returns:
            Absolute Path object with normalized separators

        Raises:
            FileNotFoundError: If must_exist=True and path doesn't exist
            ValueError: If path string is empty or invalid

        Examples:
            >>> resolver = PathResolver(Path("/project/generator"))
            >>> resolver.resolve("configs/db.yaml")
            Path('/project/generator/configs/db.yaml')

            >>> resolver.resolve("${HOME}/configs/db.yaml")  # Linux
            Path('/home/user/configs/db.yaml')

            >>> resolver.resolve("%USERPROFILE%\\configs\\db.yaml")  # Windows
            Path('C:/Users/user/configs/db.yaml')

            >>> resolver.resolve("C:\\configs\\db.yaml")  # Windows absolute
            Path('C:/configs/db.yaml')
        """
        if not path_str or not path_str.strip():
            raise ValueError("Path string cannot be empty")

        raw_path = path_str.strip()
        # Normalize Windows separators on non-Windows hosts so existence checks work.
        if os.sep != "\\" and "\\" in raw_path:
            raw_path = raw_path.replace("\\", "/")
        # Expand Windows-style %VAR% on non-Windows platforms for parity
        raw_path = self._expand_windows_env_vars(raw_path)

        # Step 1: Expand environment variables
        # os.path.expandvars handles both ${VAR} (Unix) and %VAR% (Windows)
        expanded = os.path.expandvars(raw_path)

        # Step 2: Expand home directory (~)
        # Path.expanduser() works on both Windows and Linux
        expanded = Path(expanded).expanduser()

        # Step 3: Create Path object (normalizes separators automatically)
        # Path uses native separators internally but displays consistently
        path = Path(expanded)

        # Step 4: Convert to absolute if relative
        # Path.is_absolute() correctly handles:
        #   - Windows: C:\path, C:/path, \\server\share
        #   - Linux: /path
        if not path.is_absolute():
            path = self.base_path / path

        # Step 5: Resolve symlinks, '..' and '.' references
        # Path.resolve() normalizes the path completely
        try:
            resolved = path.resolve()
        except (OSError, RuntimeError) as exc:
            # Can fail on Windows with very long paths or invalid characters
            logger.warning("Failed to resolve path '%s': %s", path, exc)
            resolved = path.absolute()

        # Step 6: Validate existence if required
        if must_exist and not resolved.exists():
            raise FileNotFoundError(f"Path does not exist: {resolved}")

        return resolved

    @staticmethod
    def _expand_windows_env_vars(path_str: str) -> str:
        """Expand %VAR% environment markers for cross-platform behavior."""
        pattern = re.compile(r"%(?P<name>[A-Za-z0-9_]+)%")

        def repl(match: re.Match) -> str:
            name = match.group("name")
            return os.environ.get(name, match.group(0))

        return pattern.sub(repl, path_str)

    def resolve_with_fallback(self, path_str: str, fallback_paths: Optional[list] = None) -> Optional[Path]:
        """Resolve path with fallback options.

        Tries to resolve the primary path, and if it doesn't exist,
        tries each fallback path in order.

        Args:
            path_str: Primary path string
            fallback_paths: List of fallback path strings to try

        Returns:
            First resolved path that exists, or None if none exist
        """
        try:
            resolved = self.resolve(path_str, must_exist=True)
            return resolved
        except FileNotFoundError:
            pass

        # Try fallbacks
        if fallback_paths:
            for fallback in fallback_paths:
                try:
                    resolved = self.resolve(fallback, must_exist=True)
                    logger.debug("Using fallback path: %s", resolved)
                    return resolved
                except FileNotFoundError:
                    continue

        return None

    @staticmethod
    def normalize_for_display(path: Path) -> str:
        """Normalize path for display (always use forward slashes).

        This ensures consistent display across platforms while maintaining
        correct internal representation.

        Args:
            path: Path object

        Returns:
            String representation with forward slashes
        """
        return path.as_posix()

    @staticmethod
    def is_windows_path(path_str: str) -> bool:
        r"""Check if path string appears to be a Windows path.

        Detects:
        - Drive letters: C:\, D:/
        - UNC paths: \\server\share

        Args:
            path_str: Path string to check

        Returns:
            True if appears to be Windows path format
        """
        path_str = path_str.strip()

        # Check for drive letter (C:\ or C:/)
        if len(path_str) >= 2 and path_str[1] == ":":
            return path_str[0].isalpha()

        # Check for UNC path (\\server\share)
        if path_str.startswith("\\\\"):
            return True

        return False

    @staticmethod
    def validate_path_string(path_str: str) -> tuple[bool, Optional[str]]:
        """Validate path string for illegal characters.

        Args:
            path_str: Path string to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not path_str or not path_str.strip():
            return False, "Path string cannot be empty"

        # Check for null bytes (illegal on all platforms)
        if "\0" in path_str:
            return False, "Path cannot contain null bytes"

        # Windows illegal characters (enforced cross-platform)
        illegal_chars = '<>"|?*'
        for char in illegal_chars:
            if char in path_str:
                return False, f"Path contains illegal character: {char}"

        return True, None
