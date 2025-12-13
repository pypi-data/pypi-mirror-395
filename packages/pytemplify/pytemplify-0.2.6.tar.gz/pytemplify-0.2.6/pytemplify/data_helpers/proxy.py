"""Dictionary proxy that wraps data with helper methods and properties."""

from functools import cached_property
from typing import TYPE_CHECKING, Any, Iterator, KeysView, List, Tuple

from pytemplify.data_helpers.smart_dict import SmartDataDict

if TYPE_CHECKING:
    from pytemplify.data_helpers.base import DataHelper
    from pytemplify.data_helpers.context import HelperContext


class DictProxy:
    """
    Proxy wrapper for dictionaries that provides access to helper methods and properties.

    This class wraps a dictionary and applies matching helper classes to provide
    computed properties and methods. Helper properties/methods take precedence over
    original dictionary keys.

    The proxy acts like a dictionary but automatically applies helpers when accessing values.

    Attributes:
        _data: The underlying dictionary
        _context: HelperContext for managing helpers
        _helper: Matched helper instance (if any)
    """

    def __init__(self, data: dict, context: "HelperContext"):
        """
        Initialize the DictProxy.

        Args:
            data: Dictionary to wrap
            context: HelperContext for helper management
        """
        object.__setattr__(self, "_raw_dict_data", data)
        object.__setattr__(self, "_context", context)
        # Find and create matching helper
        object.__setattr__(self, "_helper", context.create_helper(data))
        # Cache for SmartDataDict (created on first access)
        object.__setattr__(self, "_smart_data_cache", None)

    def __getattr__(self, name: str) -> Any:
        """
        Get attribute with priority: helper properties/methods > dict keys.

        Args:
            name: Attribute/key name

        Returns:
            Value from helper or dictionary (wrapped if necessary)

        Raises:
            AttributeError: If name not found in helper or dictionary
        """
        # Avoid recursion for most internal attributes
        if name.startswith("_") and name not in ("_data", "_raw_data"):
            return object.__getattribute__(self, name)

        helper = object.__getattribute__(self, "_helper")
        data = object.__getattribute__(self, "_raw_dict_data")
        context = object.__getattribute__(self, "_context")

        # Special case: accessing _data or _raw_data
        if name == "_data":
            # Return the helper's SmartDataDict if helper exists
            if helper is not None:
                return helper._data
            # If no helper, create and cache a SmartDataDict for consistent interface
            smart_cache = object.__getattribute__(self, "_smart_data_cache")
            if smart_cache is None:
                smart_cache = SmartDataDict(data, context)
                object.__setattr__(self, "_smart_data_cache", smart_cache)
            return smart_cache

        if name == "_raw_data":
            # Always return raw data
            return data

        # Priority 1: Check helper properties/methods (higher priority)
        if helper is not None:
            helper_class = type(helper)
            helper_attr = getattr(helper_class, name, None)

            if helper_attr is not None:
                # Handle @property
                if isinstance(helper_attr, property):
                    value = helper_attr.fget(helper)
                    # Wrap the returned value if it's a dict/list
                    return context.wrap(value, parent_data=data)

                # Handle @cached_property
                if isinstance(helper_attr, cached_property):
                    # cached_property handles caching automatically
                    value = getattr(helper, name)
                    # Wrap the returned value if it's a dict/list
                    return context.wrap(value, parent_data=data)

                # Handle regular methods
                if callable(helper_attr):
                    method = getattr(helper, name)

                    # Return a wrapper that wraps the result
                    def wrapped_method(*args, **kwargs):
                        result = method(*args, **kwargs)
                        return context.wrap(result, parent_data=data)

                    return wrapped_method

        # Priority 2: Check original dict keys (lower priority)
        if name in data:
            value = data[name]
            return context.wrap(value, parent_data=data)

        # Not found anywhere
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __getitem__(self, key: str) -> Any:
        """
        Dictionary-style access.

        Note: This checks dict keys FIRST (unlike __getattr__ which checks helpers first).
        This maintains expected dictionary behavior for bracket notation.

        Args:
            key: Dictionary key

        Returns:
            Wrapped value

        Raises:
            KeyError: If key not found
        """
        data = object.__getattribute__(self, "_raw_dict_data")
        context = object.__getattribute__(self, "_context")

        if key in data:
            value = data[key]
            return context.wrap(value, parent_data=data)

        raise KeyError(key)

    def __setattr__(self, name: str, value: Any) -> None:
        """Prevent attribute assignment (read-only proxy)."""
        raise AttributeError(f"'{type(self).__name__}' object attribute '{name}' is read-only")

    def __setitem__(self, key: str, value: Any) -> None:
        """Prevent item assignment (read-only proxy)."""
        raise TypeError(f"'{type(self).__name__}' object does not support item assignment")

    def __contains__(self, key: str) -> bool:
        """Check if key exists in dictionary."""
        data = object.__getattribute__(self, "_raw_dict_data")
        return key in data

    def __iter__(self) -> Iterator[str]:
        """Iterate over dictionary keys."""
        data = object.__getattribute__(self, "_raw_dict_data")
        return iter(data)

    def __len__(self) -> int:
        """Return number of items in dictionary."""
        data = object.__getattribute__(self, "_raw_dict_data")
        return len(data)

    def keys(self) -> KeysView[str]:
        """Return dictionary keys."""
        data = object.__getattribute__(self, "_raw_dict_data")
        return data.keys()

    def values(self) -> List[Any]:
        """Return wrapped dictionary values."""
        data = object.__getattribute__(self, "_raw_dict_data")
        context = object.__getattribute__(self, "_context")
        return [context.wrap(v, parent_data=data) for v in data.values()]

    def items(self) -> List[Tuple[str, Any]]:
        """Return dictionary items as (key, wrapped_value) pairs."""
        data = object.__getattribute__(self, "_raw_dict_data")
        context = object.__getattribute__(self, "_context")
        return [(k, context.wrap(v, parent_data=data)) for k, v in data.items()]

    def get(self, key: str, default: Any = None) -> Any:
        """Get value by key with default."""
        data = object.__getattribute__(self, "_raw_dict_data")
        context = object.__getattribute__(self, "_context")

        if key in data:
            return context.wrap(data[key], parent_data=data)
        return default

    def __repr__(self) -> str:
        """String representation."""
        data = object.__getattribute__(self, "_raw_dict_data")
        helper = object.__getattribute__(self, "_helper")
        helper_name = type(helper).__name__ if helper else "None"
        return f"DictProxy({data!r}, helper={helper_name})"

    def __str__(self) -> str:
        """String representation."""
        data = object.__getattribute__(self, "_raw_dict_data")
        return str(data)

    # Support for isinstance checks
    def __class_getitem__(cls, _item):
        """Support for generic type hints."""
        return cls
