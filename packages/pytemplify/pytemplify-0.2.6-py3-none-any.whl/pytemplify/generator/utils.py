"""Utility functions for the generator module."""

import logging
import os
from pathlib import Path
from typing import Any, List


def get_logger() -> logging.Logger:
    """Get logger instance for generator operations."""
    return logging.getLogger(__name__)


def get_nested_attr_or_key(obj: Any, path: str) -> Any:
    """Get nested attribute or dictionary key using dot notation.

    Args:
        obj: The object to traverse
        path: Dot-separated path (e.g., 'dd.devices', 'globals.project')

    Returns:
        The value at the specified path, or None if not found
    """
    current = obj
    for part in path.split("."):
        try:
            # Prioritize dictionary key access over attribute access
            if isinstance(current, dict) and part in current:
                current = current[part]
            elif hasattr(current, part):
                current = getattr(current, part)
            else:
                return None
        except (AttributeError, KeyError, TypeError):
            return None
    return current


def resolve_path_or_glob(path_str: str, base_path: Path) -> List[Path]:
    """Resolve path or glob pattern relative to base path.

    Args:
        path_str: Path string that may contain glob patterns
        base_path: Base directory to resolve relative paths from

    Returns:
        List of resolved Path objects
    """
    # Allow templated paths (e.g., Jinja placeholders) to pass through for later resolution.
    if "{{" in path_str and "}}" in path_str:
        return [base_path / path_str]

    if os.path.isabs(path_str):
        path = Path(path_str)
    else:
        path = base_path / path_str

    # If it's a simple path (no glob patterns), return as-is
    if "*" not in str(path) and "?" not in str(path) and "[" not in str(path):
        return [path] if path.exists() else []

    # Handle glob patterns
    parent = path.parent
    pattern = path.name

    if parent.exists():
        return list(parent.glob(pattern))
    return []
