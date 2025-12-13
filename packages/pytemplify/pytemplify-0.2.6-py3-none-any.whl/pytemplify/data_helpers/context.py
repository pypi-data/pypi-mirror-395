"""Helper context for managing helper lifecycle and references."""

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type

from pytemplify.data_helpers.proxy import DictProxy
from pytemplify.data_helpers.smart_dict import SmartDataDict

if TYPE_CHECKING:
    from pytemplify.data_helpers.base import DataHelper


class HelperContext:
    """
    Context object passed to all helpers during wrapping.

    Provides access to root data, parent data, and helper registry for
    cross-level queries and helper-to-helper communication.

    Attributes:
        root_data: The top-level data dictionary
        parent_data: The parent-level data dictionary (None at root level)
        helper_classes: List of available helper classes
    """

    def __init__(
        self,
        root_data: dict,
        helper_classes: List[Type["DataHelper"]],
        parent_data: Optional[dict] = None,
    ):
        self.root_data = root_data
        self.parent_data = parent_data
        self.helper_classes = helper_classes
        self._helper_cache: Dict[int, "DataHelper"] = {}  # Cache helpers by data id

    def create_child_context(self, parent_data: dict) -> "HelperContext":
        """
        Create a child context for nested data.

        Args:
            parent_data: The parent dictionary that will become the parent reference

        Returns:
            New HelperContext with updated parent reference
        """
        return HelperContext(
            root_data=self.root_data,
            helper_classes=self.helper_classes,
            parent_data=parent_data,
        )

    def match_helper(self, data: dict) -> Optional[Type["DataHelper"]]:
        """
        Find the first helper class that matches the given data.

        Args:
            data: Dictionary to match against helper classes

        Returns:
            Matching helper class or None if no match found
        """
        for helper_class in self.helper_classes:
            if helper_class.matches(data):
                return helper_class
        return None

    def create_helper(self, data: dict) -> Optional["DataHelper"]:
        """
        Create a helper instance for the given data.

        Uses caching to avoid creating multiple instances for the same data object.

        Args:
            data: Dictionary to create helper for

        Returns:
            Helper instance or None if no matching helper found
        """
        data_id = id(data)
        if data_id in self._helper_cache:
            return self._helper_cache[data_id]

        helper_class = self.match_helper(data)
        if helper_class:
            # Create SmartDataDict for the helper to use
            smart_data = SmartDataDict(data, self)
            try:
                # Try with smart_data parameter (new signature)
                helper_instance = helper_class(data, self, smart_data=smart_data)
            except TypeError:
                # Fallback for helpers with old signature (data, context only)
                helper_instance = helper_class(data, self)
                # Manually set _data to smart_data for consistency
                helper_instance._data = smart_data  # pylint: disable=protected-access
            self._helper_cache[data_id] = helper_instance
            return helper_instance

        return None

    def wrap(self, value: Any, parent_data: Optional[dict] = None) -> Any:
        """
        Wrap a value with appropriate helpers.

        This is used internally by SmartDataDict and DictProxy for automatic wrapping.

        Args:
            value: Value to wrap (can be dict, list, or primitive)
            parent_data: Optional parent data reference for nested wrapping

        Returns:
            Wrapped value (DictProxy for dicts, list of wrapped items for lists, or original value)
        """
        if isinstance(value, dict):
            # Create child context with parent reference
            child_context = self.create_child_context(parent_data or self.parent_data or self.root_data)
            return DictProxy(value, child_context)

        if isinstance(value, list):
            # Wrap each item in the list
            return [self.wrap(item, parent_data) for item in value]

        # Primitive value - return as-is
        return value
