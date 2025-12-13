"""Cross-platform file loading utilities for configuration files.

This module provides a plugin-based system for loading different file formats
(JSON, YAML, TOML) with consistent error handling across Windows and Linux.

SOLID Principles:
- SRP: Each loader handles one file format
- OCP: New formats can be added without modifying existing code
- LSP: All loaders implement FileFormatLoader interface
- DIP: High-level code depends on FileFormatLoader abstraction
"""

import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


class FileFormatLoader(ABC):
    """Abstract base for file format loaders (Open/Closed Principle)."""

    @abstractmethod
    def can_load(self, file_path: Path) -> bool:
        """Check if this loader can handle the file.

        Args:
            file_path: Path object (already resolved and absolute)

        Returns:
            True if this loader can handle the file format
        """

    @abstractmethod
    def load(self, file_path: Path) -> Any:
        """Load and parse the file.

        Args:
            file_path: Absolute Path object

        Returns:
            Parsed data structure

        Raises:
            OSError: If file cannot be read (cross-platform)
            ValueError: If file format is invalid
        """


class JsonLoader(FileFormatLoader):
    """Loads JSON files (cross-platform)."""

    def can_load(self, file_path: Path) -> bool:
        """Check if file has .json extension."""
        return file_path.suffix.lower() == ".json"

    def load(self, file_path: Path) -> Any:
        """Load JSON file with proper encoding.

        Uses UTF-8 encoding explicitly for cross-platform consistency.
        Handles both CRLF (Windows) and LF (Linux) line endings.
        """
        try:
            with open(file_path, "r", encoding="utf-8", newline=None) as f:
                # newline=None handles both \r\n and \n automatically
                return json.load(f)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON syntax in {file_path}: {exc}") from exc
        except (OSError, IOError) as exc:
            # OSError covers: PermissionError, FileNotFoundError, etc.
            raise OSError(f"Cannot read file {file_path}: {exc}") from exc
        except UnicodeDecodeError as exc:
            raise ValueError(f"File is not valid UTF-8: {file_path}: {exc}") from exc


class YamlLoader(FileFormatLoader):
    """Loads YAML files (cross-platform)."""

    def can_load(self, file_path: Path) -> bool:
        """Check if file has .yaml or .yml extension."""
        return file_path.suffix.lower() in {".yaml", ".yml"}

    def load(self, file_path: Path) -> Any:
        """Load YAML file with proper encoding.

        Uses UTF-8 encoding explicitly for cross-platform consistency.
        yaml.safe_load handles line ending differences automatically.
        """
        try:
            with open(file_path, "r", encoding="utf-8", newline=None) as f:
                return yaml.safe_load(f)
        except yaml.YAMLError as exc:
            raise ValueError(f"Invalid YAML syntax in {file_path}: {exc}") from exc
        except (OSError, IOError) as exc:
            raise OSError(f"Cannot read file {file_path}: {exc}") from exc
        except UnicodeDecodeError as exc:
            raise ValueError(f"File is not valid UTF-8: {file_path}: {exc}") from exc


class TomlLoader(FileFormatLoader):
    """Loads TOML files (cross-platform)."""

    def can_load(self, file_path: Path) -> bool:
        """Check if file has .toml extension."""
        return file_path.suffix.lower() == ".toml"

    def load(self, file_path: Path) -> Any:
        """Load TOML file with proper encoding.

        TOML spec requires UTF-8 encoding.
        Uses binary mode as required by tomli/tomllib.
        """
        try:
            # Try Python 3.11+ built-in first
            try:
                import tomllib  # pylint: disable=import-outside-toplevel

                toml_lib = tomllib
            except ImportError:
                # Fall back to tomli for Python < 3.11
                try:
                    import tomli  # pylint: disable=import-outside-toplevel

                    toml_lib = tomli  # type: ignore
                except ImportError as exc:
                    raise ValueError(
                        "TOML support requires 'tomli' package for Python < 3.11. Install it with: pip install tomli"
                    ) from exc

            # TOML libraries require binary mode
            with open(file_path, "rb") as f:
                return toml_lib.load(f)

        except UnicodeDecodeError as exc:
            raise ValueError(f"File is not valid UTF-8: {file_path}: {exc}") from exc
        except (ValueError, TypeError) as exc:
            # tomli raises these for invalid TOML
            raise ValueError(f"Invalid TOML syntax in {file_path}: {exc}") from exc
        except (OSError, IOError) as exc:
            raise OSError(f"Cannot read file {file_path}: {exc}") from exc


class FileFormatRegistry:
    """Registry for file format loaders (Dependency Inversion Principle)."""

    def __init__(self):
        self._loaders: list[FileFormatLoader] = []
        self._register_defaults()

    def _register_defaults(self):
        """Register default loaders."""
        self.register(JsonLoader())
        self.register(YamlLoader())
        self.register(TomlLoader())

    def register(self, loader: FileFormatLoader):
        """Register a new format loader.

        Args:
            loader: FileFormatLoader instance
        """
        self._loaders.append(loader)

    def load_file(self, file_path: Path, format_hint: str = "auto") -> Any:
        """Load file using appropriate loader.

        Args:
            file_path: Absolute Path object (already resolved)
            format_hint: Format hint ('json', 'yaml', 'toml', 'auto')

        Returns:
            Parsed data structure

        Raises:
            ValueError: If no loader can handle the file or format is invalid
            OSError: If file cannot be read
        """
        # Validate file exists and is regular file
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if not file_path.is_file():
            raise OSError(f"Path is not a regular file: {file_path}")

        # If format specified, try to match by extension override
        if format_hint != "auto":
            # Create temporary path with desired extension for matching
            test_path = file_path.with_suffix(f".{format_hint}")
            for loader in self._loaders:
                if loader.can_load(test_path):
                    logger.debug("Loading %s as %s format", file_path, format_hint)
                    return loader.load(file_path)

        # Auto-detect from extension
        for loader in self._loaders:
            if loader.can_load(file_path):
                logger.debug("Auto-detected format for %s", file_path)
                return loader.load(file_path)

        # No loader found
        supported = [".json", ".yaml", ".yml", ".toml"]
        raise ValueError(f"No loader found for file: {file_path} " f"(supported extensions: {', '.join(supported)})")


# Singleton instance
_file_format_registry = FileFormatRegistry()


def get_file_format_registry() -> FileFormatRegistry:
    """Get the global file format registry."""
    return _file_format_registry
