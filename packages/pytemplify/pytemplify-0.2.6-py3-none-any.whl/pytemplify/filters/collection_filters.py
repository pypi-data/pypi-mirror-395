"""Collection manipulation filters for Jinja2 templates (lists, dicts, sets)."""

from typing import Any, Callable, Dict, List


def flatten(value: List[Any], levels: int = 1) -> List[Any]:
    """
    Flatten nested lists to specified depth.

    Args:
        value: List to flatten
        levels: Number of levels to flatten (default: 1, use -1 for complete flattening)

    Example:
        {{ [[1, 2], [3, 4]] | flatten }} -> [1, 2, 3, 4]
        {{ [[[1]], [[2]], [[3]]] | flatten(2) }} -> [1, 2, 3]
    """

    def _flatten_recursive(lst: List[Any], remaining_levels: int) -> List[Any]:
        if remaining_levels == 0:
            return lst

        result = []
        for item in lst:
            if isinstance(item, (list, tuple)):
                if remaining_levels == -1:
                    result.extend(_flatten_recursive(list(item), -1))
                else:
                    result.extend(_flatten_recursive(list(item), remaining_levels - 1))
            else:
                result.append(item)
        return result

    if not isinstance(value, (list, tuple)):
        return [value]

    return _flatten_recursive(list(value), levels)


def unique(value: List[Any]) -> List[Any]:
    """
    Remove duplicate items from list while preserving order.

    Example:
        {{ [1, 2, 2, 3, 1] | unique }} -> [1, 2, 3]
        {{ ["a", "b", "a"] | unique }} -> ["a", "b"]
    """
    seen = set()
    result = []
    for item in value:
        # Handle unhashable types
        try:
            if item not in seen:
                seen.add(item)
                result.append(item)
        except TypeError:
            # For unhashable types, use list comparison
            if item not in result:
                result.append(item)
    return result


def chunk(value: List[Any], size: int) -> List[List[Any]]:
    """
    Split list into chunks of specified size.

    Example:
        {{ [1, 2, 3, 4, 5] | chunk(2) }} -> [[1, 2], [3, 4], [5]]
        {{ range(10) | list | chunk(3) }} -> [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    """
    if size <= 0:
        raise ValueError("Chunk size must be positive")

    return [value[i : i + size] for i in range(0, len(value), size)]


def pluck(value: List[Dict[str, Any]], key: str) -> List[Any]:
    """
    Extract values for a specific key from list of dictionaries.

    Example:
        {{ users | pluck("name") }} -> ["Alice", "Bob", "Charlie"]
        {{ items | pluck("id") }} -> [1, 2, 3]
    """
    result = []
    for item in value:
        if isinstance(item, dict):
            result.append(item.get(key))
        elif hasattr(item, key):
            result.append(getattr(item, key))
        else:
            result.append(None)
    return result


def where(value: List[Dict[str, Any]], key: str, test_value: Any = None) -> List[Dict[str, Any]]:
    """
    Filter list of dictionaries by key/value.

    Args:
        value: List to filter
        key: Key to check
        test_value: Value to match (if None, checks for truthy values)

    Example:
        {{ users | where("active", true) }} -> [users where active=true]
        {{ items | where("status") }} -> [items where status is truthy]
    """
    result = []
    for item in value:
        if isinstance(item, dict):
            item_value = item.get(key)
        else:
            if hasattr(item, key):
                item_value = getattr(item, key)
            else:
                continue

        if test_value is None:
            if item_value:
                result.append(item)
        elif item_value == test_value:
            result.append(item)

    return result


def sort_by(value: List[Any], key: str, reverse: bool = False) -> List[Any]:
    """
    Sort list of objects/dicts by a specific attribute/key.

    Example:
        {{ users | sort_by("age") }} -> [users sorted by age]
        {{ items | sort_by("price", reverse=true) }} -> [items sorted by price descending]
    """

    def get_sort_key(item):
        if isinstance(item, dict):
            return item.get(key)
        if hasattr(item, key):
            return getattr(item, key)
        return None

    return sorted(value, key=get_sort_key, reverse=reverse)


def group_by(value: List[Any], key: str) -> Dict[Any, List[Any]]:
    """
    Group list items by a specific key/attribute.

    Example:
        {{ users | group_by("role") }} -> {"admin": [...], "user": [...]}
        {{ items | group_by("category") }} -> {"electronics": [...], "books": [...]}
    """
    result: Dict[Any, List[Any]] = {}

    for item in value:
        if isinstance(item, dict):
            group_key = item.get(key)
        elif hasattr(item, key):
            group_key = getattr(item, key)
        else:
            group_key = None

        if group_key not in result:
            result[group_key] = []
        result[group_key].append(item)

    return result


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge multiple dictionaries (later dicts override earlier ones).

    Example:
        {{ merge_dicts({"a": 1}, {"b": 2}, {"a": 3}) }} -> {"a": 3, "b": 2}
    """
    result = {}
    for d in dicts:
        if isinstance(d, dict):
            result.update(d)
    return result


def dict_keys(value: Dict[str, Any]) -> List[str]:
    """
    Get list of dictionary keys.

    Example:
        {{ {"a": 1, "b": 2} | dict_keys }} -> ["a", "b"]
    """
    if not isinstance(value, dict):
        return []
    return list(value.keys())


def dict_values(value: Dict[str, Any]) -> List[Any]:
    """
    Get list of dictionary values.

    Example:
        {{ {"a": 1, "b": 2} | dict_values }} -> [1, 2]
    """
    if not isinstance(value, dict):
        return []
    return list(value.values())


def dict_items(value: Dict[str, Any]) -> List[tuple]:
    """
    Get list of dictionary (key, value) tuples.

    Example:
        {{ {"a": 1, "b": 2} | dict_items }} -> [("a", 1), ("b", 2)]
    """
    if not isinstance(value, dict):
        return []
    return list(value.items())


def zip_lists(*lists: List[Any]) -> List[tuple]:
    """
    Zip multiple lists together.

    Example:
        {{ zip_lists([1, 2, 3], ["a", "b", "c"]) }} -> [(1, "a"), (2, "b"), (3, "c")]
    """
    return list(zip(*lists))


def index_of(value: List[Any], item: Any) -> int:
    """
    Get index of item in list (-1 if not found).

    Example:
        {{ [1, 2, 3] | index_of(2) }} -> 1
        {{ ["a", "b"] | index_of("c") }} -> -1
    """
    try:
        return value.index(item)
    except (ValueError, AttributeError):
        return -1


def compact(value: List[Any]) -> List[Any]:
    """
    Remove falsy values (None, False, 0, "", [], {}) from list.

    Example:
        {{ [1, None, 2, False, 3, "", 4] | compact }} -> [1, 2, 3, 4]
    """
    return [item for item in value if item]


def intersection(list1: List[Any], list2: List[Any]) -> List[Any]:
    """
    Get intersection of two lists (common elements).

    Example:
        {{ [1, 2, 3] | intersection([2, 3, 4]) }} -> [2, 3]
    """
    return list(set(list1) & set(list2))


def difference(list1: List[Any], list2: List[Any]) -> List[Any]:
    """
    Get difference of two lists (elements in first but not second).

    Example:
        {{ [1, 2, 3] | difference([2, 3, 4]) }} -> [1]
    """
    return list(set(list1) - set(list2))


def union(list1: List[Any], list2: List[Any]) -> List[Any]:
    """
    Get union of two lists (all unique elements from both).

    Example:
        {{ [1, 2, 3] | union([3, 4, 5]) }} -> [1, 2, 3, 4, 5]
    """
    return list(set(list1) | set(list2))


def get_collection_filters() -> Dict[str, Callable]:
    """Get all collection filters."""
    return {
        "flatten": flatten,
        "unique": unique,
        "chunk": chunk,
        "pluck": pluck,
        "where": where,
        "sort_by": sort_by,
        "group_by": group_by,
        "merge_dicts": merge_dicts,
        "dict_keys": dict_keys,
        "dict_values": dict_values,
        "dict_items": dict_items,
        "zip_lists": zip_lists,
        "index_of": index_of,
        "compact": compact,
        "intersection": intersection,
        "difference": difference,
        "union": union,
    }
