"""
Data helper extension system for pytemplify.

This module provides a powerful way to add computed properties and methods to dictionary
data without modifying the original data structure. Helpers are automatically applied
based on data structure matching and support nested dictionaries, cross-level queries,
and helper-to-helper communication.

Key Features:
    - Automatic helper matching based on data structure
    - Computed properties and methods for dictionaries
    - Nested data wrapping with automatic helper application
    - Cross-level data access (root and parent references)
    - Helper ordering by specificity for predictable behavior
    - Multiple helper loading strategies (direct, specs, discovery, YAML)
    - Read-only proxies to prevent accidental data modification

Basic Example:
    from pytemplify.data_helpers import wrap_with_helpers, DataHelper

    class CompanyHelpers(DataHelper):
        @staticmethod
        def matches(data: dict) -> bool:
            return "company_name" in data and "employees" in data

        @property
        def employee_count(self) -> int:
            return len(self._data.employees)

        @property
        def average_salary(self) -> float:
            salaries = [emp.salary for emp in self._data.employees]
            return sum(salaries) / len(salaries) if salaries else 0.0

    wrapped = wrap_with_helpers(company_data, [CompanyHelpers])
    print(wrapped.employee_count)  # Uses helper property
    print(wrapped.average_salary)  # Computed from nested data

Integration with TemplateRenderer:
    from pytemplify import TemplateRenderer
    from pytemplify.data_helpers import wrap_with_helpers

    # Wrap data with helpers
    wrapped_data = wrap_with_helpers(company_data, [CompanyHelpers])

    # Use in templates
    renderer = TemplateRenderer(data={"company": wrapped_data})
    output = renderer.render_string(
        "{{ company.company_name }}: {{ company.employee_count }} employees"
    )

Advanced Features:
    - Helper loading from modules: HelperLoader.load_helpers_from_string("module.Helper")
    - Helper discovery from directories: HelperLoader.discover_helpers(["./helpers/"])
    - Automatic ordering by specificity: sort_helpers_by_specificity(helper_classes)
    - Cross-level queries: Access root_data and parent_data from nested helpers
    - Helper validation: HelperLoader.validate_helpers(helpers, sample_data)

See individual class documentation for detailed usage patterns.
"""

from pytemplify.data_helpers.base import DataHelper
from pytemplify.data_helpers.loader import HelperLoader, HelperLoaderError
from pytemplify.data_helpers.wrapper import wrap_with_helpers

__all__ = ["DataHelper", "wrap_with_helpers", "HelperLoader", "HelperLoaderError"]
