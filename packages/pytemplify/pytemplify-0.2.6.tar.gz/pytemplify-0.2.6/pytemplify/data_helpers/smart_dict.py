"""Smart dictionary wrapper that automatically wraps nested values."""

from typing import TYPE_CHECKING, Any, Iterator, KeysView, List, Tuple

if TYPE_CHECKING:
    from pytemplify.data_helpers.context import HelperContext


class SmartDataDict:
    """
    Dictionary wrapper that automatically wraps nested values with helpers.

    This class provides transparent access to dictionary data while automatically
    wrapping any nested dictionaries or lists with appropriate helpers.

    When a helper accesses self._data["key"] or self._data.key, the value is
    automatically wrapped if it's a dict or list, enabling seamless helper chaining.

    Attributes:
        _raw_data: The underlying dictionary (unwrapped)
        _context: HelperContext for wrapping nested values
    """

    def __init__(self, data: dict, context: "HelperContext"):
        self._raw_data = data
        self._context = context

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get value by key, automatically wrapping nested structures.

        Args:
            key: Dictionary key to access
            default: Default value if key not found

        Returns:
            Wrapped value if it's a dict/list, otherwise the raw value
        """
        if key in self._raw_data:
            return self._wrap_value(self._raw_data[key])
        return default

    def __getitem__(self, key: str) -> Any:
        """
        Get value by key using bracket notation, automatically wrapping.

        Args:
            key: Dictionary key to access

        Returns:
            Wrapped value if it's a dict/list, otherwise the raw value

        Raises:
            KeyError: If key not found
        """
        return self._wrap_value(self._raw_data[key])

    def __getattr__(self, name: str) -> Any:
        """
        Get value by attribute access, automatically wrapping.

        This allows self._data.key syntax instead of self._data["key"].

        Args:
            name: Attribute name (maps to dict key)

        Returns:
            Wrapped value if it's a dict/list, otherwise the raw value

        Raises:
            AttributeError: If key not found
        """
        # Avoid recursion for private attributes
        if name.startswith("_"):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

        if name in self._raw_data:
            return self._wrap_value(self._raw_data[name])
        raise AttributeError(f"No key '{name}' in data")

    def _wrap_value(self, value: Any) -> Any:
        """
        Wrap a value with appropriate helpers.

        Args:
            value: Value to wrap

        Returns:
            Wrapped value (DictProxy for dicts, wrapped list for lists, or original value)
        """
        return self._context.wrap(value, parent_data=self._raw_data)

    # Dictionary-like interface

    def keys(self) -> KeysView[str]:
        """Return dictionary keys."""
        return self._raw_data.keys()

    def values(self) -> List[Any]:
        """Return dictionary values (wrapped)."""
        return [self._wrap_value(v) for v in self._raw_data.values()]

    def items(self) -> List[Tuple[str, Any]]:
        """Return dictionary items as (key, wrapped_value) pairs."""
        return [(k, self._wrap_value(v)) for k, v in self._raw_data.items()]

    def __contains__(self, key: str) -> bool:
        """Check if key exists in dictionary."""
        return key in self._raw_data

    def __iter__(self) -> Iterator[str]:
        """Iterate over dictionary keys."""
        return iter(self._raw_data)

    def __len__(self) -> int:
        """Return number of items in dictionary."""
        return len(self._raw_data)

    def __repr__(self) -> str:
        """String representation of SmartDataDict."""
        return f"SmartDataDict({self._raw_data!r})"
