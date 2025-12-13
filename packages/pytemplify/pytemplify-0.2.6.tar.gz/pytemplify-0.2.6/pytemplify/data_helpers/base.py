"""Base class for data helper extensions."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    from pytemplify.data_helpers.context import HelperContext
    from pytemplify.data_helpers.smart_dict import SmartDataDict


class DataHelper(ABC):
    """
    Base class for dictionary data helper extensions.

    Subclass this to add computed properties and methods to dictionary data.
    Helpers are automatically applied when data structure matches the pattern
    defined in the matches() method.

    Example:
        class CompanyHelpers(DataHelper):
            @staticmethod
            def matches(data: dict) -> bool:
                return "company_name" in data and "offices" in data

            @property
            def employee_count(self):
                # Access nested data - automatically wrapped!
                return sum(len(office._data.employees) for office in self._data.offices)

            @property
            def total_cost(self):
                # Cross-helper communication - OfficeHelpers applied automatically
                return sum(office.total_salary_cost for office in self._data.offices)

    Attributes:
        _raw_data: Unwrapped original dictionary data
        _data: SmartDataDict that auto-wraps nested values
        _context: HelperContext for accessing root/parent data
    """

    def __init__(self, data: dict, context: "HelperContext" = None, *, smart_data: Union["SmartDataDict", dict] = None):
        """
        Initialize the data helper.

        Args:
            data: Dictionary data (unwrapped)
            context: Optional HelperContext for cross-level queries
            smart_data: Pre-created SmartDataDict or dict for _data attribute (keyword-only)
        """
        self._raw_data = data  # Unwrapped original data
        self._context = context
        # Use provided smart_data or fallback to raw data
        self._data: Union["SmartDataDict", dict] = smart_data if smart_data is not None else data

    @property
    def _root_data(self) -> dict:
        """
        Access root-level data for cross-level queries.

        Returns:
            The top-level dictionary in the data hierarchy

        Example:
            class EmployeeHelpers(DataHelper):
                @property
                def company_name(self):
                    # Access root data from nested employee object
                    return self._root_data.get("company_name", "Unknown")
        """
        if self._context:
            return self._context.root_data
        return self._raw_data

    @property
    def _parent_data(self) -> Any:
        """
        Access parent-level data.

        Returns:
            The parent dictionary in the data hierarchy, or None if at root level

        Example:
            class EmployeeHelpers(DataHelper):
                @property
                def office_city(self):
                    # Access parent office data
                    if self._parent_data:
                        return self._parent_data.get("city", "Unknown")
                    return "Unknown"
        """
        if self._context:
            return self._context.parent_data
        return None

    @staticmethod
    @abstractmethod
    def matches(data: dict) -> bool:
        """
        Return True if this helper should be applied to the given data.

        This method is used for automatic helper matching based on data structure.
        Define a pattern that uniquely identifies when this helper should be used.

        Args:
            data: Dictionary to check

        Returns:
            True if this helper applies to the data, False otherwise

        Example:
            @staticmethod
            def matches(data: dict) -> bool:
                # Match if dict has company-specific fields
                return "company_name" in data and "offices" in data
        """
