"""
Built-in filters for TemplateRenderer.

This package provides a collection of useful Jinja2 filters that extend
the built-in Jinja2 filters. Filters are organized by category:

- string_filters: String manipulation and transformation
- collection_filters: List, dict, and set operations
- formatting_filters: Data formatting (dates, numbers, etc.)
- utility_filters: Common utility operations

All filters are automatically registered when TemplateRenderer is initialized.
"""

from typing import Callable, Dict

from pytemplify.filters.collection_filters import get_collection_filters
from pytemplify.filters.formatting_filters import get_formatting_filters
from pytemplify.filters.string_filters import get_string_filters
from pytemplify.filters.utility_filters import get_utility_filters


def get_all_filters() -> Dict[str, Callable]:
    """
    Get all built-in filters from all categories.

    Returns:
        Dictionary mapping filter names to filter functions
    """
    filters: Dict[str, Callable] = {}

    # Collect filters from all modules
    filters.update(get_string_filters())
    filters.update(get_collection_filters())
    filters.update(get_formatting_filters())
    filters.update(get_utility_filters())

    return filters


__all__ = [
    "get_all_filters",
    "get_string_filters",
    "get_collection_filters",
    "get_formatting_filters",
    "get_utility_filters",
]
