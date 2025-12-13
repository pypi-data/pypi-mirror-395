"""Main public API for wrapping data with helpers."""

from typing import List, Type

from pytemplify.data_helpers.base import DataHelper
from pytemplify.data_helpers.context import HelperContext
from pytemplify.data_helpers.ordering import sort_helpers_by_specificity
from pytemplify.data_helpers.proxy import DictProxy


def wrap_with_helpers(data: dict, helpers: List[Type[DataHelper]], auto_order: bool = True) -> DictProxy:
    """
    Wrap dictionary data with helper extensions.

    This is the main entry point for the data_helpers system. It wraps a dictionary
    with helper classes that add computed properties and methods based on data structure
    matching.

    Args:
        data: Dictionary data to wrap
        helpers: List of DataHelper classes to apply
        auto_order: If True (default), automatically sort helpers by specificity.
                   Most specific helpers are checked first. Set to False to preserve
                   the order you provide.

    Returns:
        DictProxy with helpers applied, providing access to both original data
        and helper-provided properties/methods

    Raises:
        TypeError: If data is not a dictionary

    Example:
        from pytemplify.data_helpers import wrap_with_helpers, DataHelper

        class CompanyHelpers(DataHelper):
            @staticmethod
            def matches(data: dict) -> bool:
                return "company_name" in data

            @property
            def employee_count(self):
                return len(self._data.employees)

        # Automatic ordering (recommended)
        wrapped = wrap_with_helpers(company_data, [CompanyHelpers])

        # Manual ordering (if you need specific order)
        wrapped = wrap_with_helpers(company_data, [Helper1, Helper2], auto_order=False)

        print(wrapped.employee_count)  # Uses CompanyHelpers.employee_count

        # Use with TemplateRenderer
        from pytemplify.renderer import TemplateRenderer
        renderer = TemplateRenderer(data={"company": wrapped})
        output = renderer.render_string("{{ company.company_name }}: {{ company.employee_count }} employees")

    Notes:
        - Helpers are matched based on their matches() method
        - With auto_order=True, more specific helpers are checked first automatically
        - Helper properties/methods take precedence over dict keys when using attribute access
        - Nested dicts and lists are automatically wrapped recursively
        - Multiple helpers can be registered; first match wins
        - Helpers can access other helpers through automatic wrapping
    """
    if not isinstance(data, dict):
        raise TypeError(f"Expected dict, got {type(data).__name__}")

    if not helpers:
        # No helpers provided - just return a proxy without helpers
        # This still provides consistent interface
        context = HelperContext(root_data=data, helper_classes=[])
        return DictProxy(data, context)

    # Automatically sort helpers by specificity (most specific first)
    if auto_order:
        helpers = sort_helpers_by_specificity(helpers)

    # Create context and wrap
    context = HelperContext(root_data=data, helper_classes=helpers)
    return DictProxy(data, context)
