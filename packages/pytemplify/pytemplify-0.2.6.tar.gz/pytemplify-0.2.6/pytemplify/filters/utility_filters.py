"""Utility filters for Jinja2 templates (common operations and helpers)."""

import base64
import hashlib
import os
import random
import string
import uuid
from typing import Any, Callable, Dict, Optional

# Pytemplify custom namespace UUID for deterministic UUID generation
# Generated from "com.github.pytemplify" using DNS namespace
PYTEMPLIFY_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "com.github.pytemplify")


def default_if_none(value: Any, default: Any = "") -> Any:
    """
    Return default value if input is None (more explicit than Jinja's default).

    Example:
        {{ None | default_if_none("N/A") }} -> "N/A"
        {{ "" | default_if_none("N/A") }} -> ""
        {{ False | default_if_none("N/A") }} -> False
    """
    return default if value is None else value


def coalesce(*values: Any) -> Any:
    """
    Return first non-None value from arguments.

    Example:
        {{ coalesce(None, None, "first", "second") }} -> "first"
        {{ coalesce(None, 0, 5) }} -> 0
    """
    for value in values:
        if value is not None:
            return value
    return None


def ternary(condition: bool, true_value: Any, false_value: Any) -> Any:
    """
    Ternary operator (condition ? true_value : false_value).

    Example:
        {{ ternary(age >= 18, "Adult", "Minor") }}
        {{ ternary(count > 0, "items", "no items") }}
    """
    return true_value if condition else false_value


def type_name(value: Any) -> str:
    """
    Get type name of value.

    Example:
        {{ "hello" | type_name }} -> "str"
        {{ 123 | type_name }} -> "int"
        {{ [1, 2, 3] | type_name }} -> "list"
    """
    return type(value).__name__


def is_list(value: Any) -> bool:
    """
    Check if value is a list.

    Example:
        {{ [1, 2, 3] | is_list }} -> True
        {{ "test" | is_list }} -> False
    """
    return isinstance(value, list)


def is_dict(value: Any) -> bool:
    """
    Check if value is a dictionary.

    Example:
        {{ {"key": "value"} | is_dict }} -> True
        {{ [1, 2] | is_dict }} -> False
    """
    return isinstance(value, dict)


def is_string(value: Any) -> bool:
    """
    Check if value is a string.

    Example:
        {{ "hello" | is_string }} -> True
        {{ 123 | is_string }} -> False
    """
    return isinstance(value, str)


def is_number(value: Any) -> bool:
    """
    Check if value is a number (int or float).

    Example:
        {{ 123 | is_number }} -> True
        {{ 45.67 | is_number }} -> True
        {{ "123" | is_number }} -> False
    """
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def is_even(value: int) -> bool:
    """
    Check if number is even.

    Example:
        {{ 4 | is_even }} -> True
        {{ 5 | is_even }} -> False
    """
    return int(value) % 2 == 0


def is_odd(value: int) -> bool:
    """
    Check if number is odd.

    Example:
        {{ 5 | is_odd }} -> True
        {{ 4 | is_odd }} -> False
    """
    return int(value) % 2 != 0


def hash_md5(value: str) -> str:
    """
    Generate MD5 hash of string.

    Example:
        {{ "hello" | hash_md5 }} -> "5d41402abc4b2a76b9719d911017c592"
    """
    return hashlib.md5(str(value).encode()).hexdigest()


def hash_sha256(value: str) -> str:
    """
    Generate SHA256 hash of string.

    Example:
        {{ "hello" | hash_sha256 }} -> "2cf24dba5fb0a30e..."
    """
    return hashlib.sha256(str(value).encode()).hexdigest()


def b64encode(value: str) -> str:
    """
    Base64 encode string.

    Example:
        {{ "hello" | b64encode }} -> "aGVsbG8="
    """
    return base64.b64encode(str(value).encode()).decode()


def b64decode(value: str) -> str:
    """
    Base64 decode string.

    Example:
        {{ "aGVsbG8=" | b64decode }} -> "hello"
    """
    try:
        return base64.b64decode(str(value)).decode()
    except (ValueError, TypeError):  # More specific exceptions
        return str(value)


def random_string(length: int = 10, charset: str = "alphanumeric") -> str:
    """
    Generate random string.

    Args:
        length: Length of string (default: 10)
        charset: Character set - "alphanumeric", "alpha", "numeric", "hex" (default: "alphanumeric")

    Example:
        {{ random_string(8) }} -> "aB3xYz7Q"
        {{ random_string(6, "numeric") }} -> "482759"
    """
    charsets = {
        "alphanumeric": string.ascii_letters + string.digits,
        "alpha": string.ascii_letters,
        "numeric": string.digits,
        "hex": string.hexdigits.lower(),
    }

    chars = charsets.get(charset, charsets["alphanumeric"])
    return "".join(random.choice(chars) for _ in range(length))


def random_int(min_val: int = 0, max_val: int = 100) -> int:
    """
    Generate random integer in range.

    Example:
        {{ random_int(1, 10) }} -> random number between 1 and 10
    """
    return random.randint(min_val, max_val)


def uuid_generate(value: Optional[str] = None, namespace: Optional[str] = None) -> str:
    """
    Generate UUID with optional value and namespace for deterministic UUIDs.

    Args:
        value: Optional value/name string to generate deterministic UUID
               (when used as filter, this is the piped value)
        namespace: Optional namespace - "dns"/"url"/"oid"/"x500"/"pytemplify" or custom UUID string
                   (default: "pytemplify" if value provided)

    Example:
        {{ uuid_generate() }} -> Random UUID4
        {{ uuid_generate("my_service") }} -> Deterministic UUID5 with pytemplify namespace
        {{ uuid_generate("my_service", "url") }} -> Deterministic UUID5 with URL namespace
        {{ uuid_generate("my_service", "dns") }} -> Deterministic UUID5 with DNS namespace
        {{ "my_service" | uuid_generate }} -> Deterministic UUID5 with pytemplify namespace (as filter)
        {{ "my_service" | uuid_generate("url") }} -> Deterministic UUID5 with URL namespace (as filter)
    """
    # If no value provided, generate random UUID4
    if not value:
        return str(uuid.uuid4())

    # Map standard namespace names
    namespace_map = {
        "dns": uuid.NAMESPACE_DNS,
        "url": uuid.NAMESPACE_URL,
        "oid": uuid.NAMESPACE_OID,
        "x500": uuid.NAMESPACE_X500,
        "pytemplify": PYTEMPLIFY_NAMESPACE,
    }

    # Determine the namespace UUID to use
    if namespace:
        # Namespace explicitly provided
        if namespace.lower() in namespace_map:
            ns_uuid = namespace_map[namespace.lower()]
        else:
            # Try to parse as UUID string
            try:
                ns_uuid = uuid.UUID(namespace)
            except ValueError:
                # If invalid, use namespace as seed for UUID5 with pytemplify namespace
                ns_uuid = uuid.uuid5(PYTEMPLIFY_NAMESPACE, namespace)
    else:
        # Default to pytemplify custom namespace
        ns_uuid = PYTEMPLIFY_NAMESPACE

    # Generate deterministic UUID5
    return str(uuid.uuid5(ns_uuid, value))


def abs_value(value: float) -> float:
    """
    Get absolute value of number.

    Example:
        {{ -5 | abs_value }} -> 5
        {{ 3.14 | abs_value }} -> 3.14
    """
    return abs(value)


def clamp(value: float, min_val: float, max_val: float) -> float:
    """
    Clamp value between min and max.

    Example:
        {{ 15 | clamp(0, 10) }} -> 10
        {{ -5 | clamp(0, 10) }} -> 0
        {{ 5 | clamp(0, 10) }} -> 5
    """
    return max(min_val, min(value, max_val))


def bool_to_string(value: bool, true_str: str = "true", false_str: str = "false") -> str:
    """
    Convert boolean to custom string representation.

    Example:
        {{ True | bool_to_string }} -> "true"
        {{ False | bool_to_string("yes", "no") }} -> "no"
    """
    return true_str if value else false_str


def file_extension(value: str) -> str:
    """
    Get file extension from filename or path.

    Example:
        {{ "document.pdf" | file_extension }} -> "pdf"
        {{ "/path/to/file.txt" | file_extension }} -> "txt"
    """
    return os.path.splitext(str(value))[1].lstrip(".")


def file_basename(value: str) -> str:
    """
    Get filename without path.

    Example:
        {{ "/path/to/file.txt" | file_basename }} -> "file.txt"
    """
    return os.path.basename(str(value))


def file_dirname(value: str) -> str:
    """
    Get directory path from file path.

    Example:
        {{ "/path/to/file.txt" | file_dirname }} -> "/path/to"
    """
    return os.path.dirname(str(value))


def safe_divide(dividend: float, divisor: float, default: float = 0.0) -> float:
    """
    Divide with safe handling of division by zero.

    Example:
        {{ 10 | safe_divide(2) }} -> 5.0
        {{ 10 | safe_divide(0) }} -> 0.0
        {{ 10 | safe_divide(0, default=-1) }} -> -1.0
    """
    try:
        return float(dividend) / float(divisor)
    except (ZeroDivisionError, ValueError):
        return default


def map_value(value: Any, mapping: Dict[Any, Any], default: Optional[Any] = None) -> Any:
    """
    Map value using dictionary lookup.

    Example:
        {{ "red" | map_value({"red": "#FF0000", "blue": "#0000FF"}) }} -> "#FF0000"
        {{ "green" | map_value({"red": "#FF0000"}, default="unknown") }} -> "unknown"
    """
    return mapping.get(value, default)


def get_attr(obj: Any, attr_name: str, default: Any = None) -> Any:
    """
    Safely get attribute from object.

    Example:
        {{ user | get_attr("email", "no-email@example.com") }}
    """
    return getattr(obj, attr_name, default)


def get_item(obj: Any, key: Any, default: Any = None) -> Any:
    """
    Safely get item from dict/list.

    Example:
        {{ data | get_item("key", "default_value") }}
        {{ items | get_item(0, "no items") }}
    """
    try:
        return obj[key]
    except (KeyError, IndexError, TypeError):
        return default


def get_formatting_filters() -> Dict[str, Callable]:
    """Get all utility filters."""
    return {
        "default_if_none": default_if_none,
        "coalesce": coalesce,
        "ternary": ternary,
        "type_name": type_name,
        "is_list": is_list,
        "is_dict": is_dict,
        "is_string": is_string,
        "is_number": is_number,
        "is_even": is_even,
        "is_odd": is_odd,
        "hash_md5": hash_md5,
        "hash_sha256": hash_sha256,
        "b64encode": b64encode,
        "b64decode": b64decode,
        "random_string": random_string,
        "random_int": random_int,
        "uuid_generate": uuid_generate,
        "abs_value": abs_value,
        "clamp": clamp,
        "bool_to_string": bool_to_string,
        "file_extension": file_extension,
        "file_basename": file_basename,
        "file_dirname": file_dirname,
        "safe_divide": safe_divide,
        "map_value": map_value,
        "get_attr": get_attr,
        "get_item": get_item,
    }


# Alias for backward compatibility
get_utility_filters = get_formatting_filters
