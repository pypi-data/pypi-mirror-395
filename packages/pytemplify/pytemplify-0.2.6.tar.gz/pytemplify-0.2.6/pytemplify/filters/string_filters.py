"""String manipulation filters for Jinja2 templates."""

import re
import textwrap
from typing import Callable, Dict


def camelcase(value: str) -> str:
    """
    Convert string to camelCase.

    Example:
        {{ "hello_world" | camelcase }} -> "helloWorld"
        {{ "hello-world" | camelcase }} -> "helloWorld"
        {{ "hello world" | camelcase }} -> "helloWorld"
    """
    # Split on non-alphanumeric characters
    words = re.split(r"[^a-zA-Z0-9]+", str(value))
    if not words:
        return ""
    # First word lowercase, rest title case
    return words[0].lower() + "".join(word.capitalize() for word in words[1:] if word)


def pascalcase(value: str) -> str:
    """
    Convert string to PascalCase.

    Example:
        {{ "hello_world" | pascalcase }} -> "HelloWorld"
        {{ "hello-world" | pascalcase }} -> "HelloWorld"
        {{ "hello world" | pascalcase }} -> "HelloWorld"
    """
    # Split on non-alphanumeric characters
    words = re.split(r"[^a-zA-Z0-9]+", str(value))
    return "".join(word.capitalize() for word in words if word)


def snakecase(value: str) -> str:
    """
    Convert string to snake_case.

    Example:
        {{ "HelloWorld" | snakecase }} -> "hello_world"
        {{ "helloWorld" | snakecase }} -> "hello_world"
        {{ "hello-world" | snakecase }} -> "hello_world"
    """
    # Insert underscore before uppercase letters
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", str(value))
    # Insert underscore before uppercase letters followed by lowercase
    s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
    # Replace spaces and hyphens with underscores
    s3 = re.sub(r"[\s-]+", "_", s2)
    return s3.lower()


def kebabcase(value: str) -> str:
    """
    Convert string to kebab-case.

    Example:
        {{ "HelloWorld" | kebabcase }} -> "hello-world"
        {{ "helloWorld" | kebabcase }} -> "hello-world"
        {{ "hello_world" | kebabcase }} -> "hello-world"
    """
    return snakecase(value).replace("_", "-")


def screamingsnakecase(value: str) -> str:
    """
    Convert string to SCREAMING_SNAKE_CASE.

    Example:
        {{ "HelloWorld" | screamingsnakecase }} -> "HELLO_WORLD"
        {{ "helloWorld" | screamingsnakecase }} -> "HELLO_WORLD"
        {{ "hello-world" | screamingsnakecase }} -> "HELLO_WORLD"
    """
    return snakecase(value).upper()


def normalize(value: str) -> str:
    """
    Normalize string to be safe for filenames and URLs.
    Converts to lowercase, replaces spaces/special chars with underscores.

    Example:
        {{ "Hello World!" | normalize }} -> "hello_world"
        {{ "/api/v1/users" | normalize }} -> "api_v1_users"
    """
    # Replace non-alphanumeric characters with underscores
    normalized = re.sub(r"[^a-zA-Z0-9]+", "_", str(value))
    # Remove leading/trailing underscores
    normalized = normalized.strip("_")
    return normalized.lower()


def slugify(value: str) -> str:
    """
    Convert string to URL-friendly slug.

    Example:
        {{ "Hello World!" | slugify }} -> "hello-world"
        {{ "  Product #123  " | slugify }} -> "product-123"
    """
    # Convert to lowercase and replace spaces with hyphens
    slug = str(value).lower().strip()
    # Replace non-alphanumeric characters (except hyphens) with hyphens
    slug = re.sub(r"[^a-z0-9-]+", "-", slug)
    # Remove multiple consecutive hyphens
    slug = re.sub(r"-+", "-", slug)
    # Remove leading/trailing hyphens
    return slug.strip("-")


def indent_custom(value: str, width: int = 4, first: bool = False, blank: bool = False) -> str:
    """
    Indent text with custom options (extends Jinja2's indent filter).

    Args:
        value: Text to indent
        width: Number of spaces to indent (default: 4)
        first: Whether to indent the first line (default: False)
        blank: Whether to indent blank lines (default: False)

    Example:
        {{ "line1\nline2" | indent_custom(4) }} -> "line1\n    line2"
        {{ "line1\nline2" | indent_custom(4, first=true) }} -> "    line1\n    line2"
    """
    lines = str(value).splitlines(keepends=True)
    indent_str = " " * width
    result = []

    for i, line in enumerate(lines):
        is_first = i == 0
        is_blank = line.strip() == ""

        # Skip indenting based on conditions
        if is_first and not first:
            result.append(line)
        elif is_blank and not blank:
            result.append(line)
        else:
            result.append(indent_str + line)

    return "".join(result)


def remove_prefix(value: str, prefix: str) -> str:
    """
    Remove prefix from string if it exists.

    Example:
        {{ "HelloWorld" | remove_prefix("Hello") }} -> "World"
        {{ "test_value" | remove_prefix("test_") }} -> "value"
    """
    value_str = str(value)
    if value_str.startswith(prefix):
        return value_str[len(prefix) :]
    return value_str


def remove_suffix(value: str, suffix: str) -> str:
    """
    Remove suffix from string if it exists.

    Example:
        {{ "HelloWorld" | remove_suffix("World") }} -> "Hello"
        {{ "test.txt" | remove_suffix(".txt") }} -> "test"
    """
    value_str = str(value)
    if value_str.endswith(suffix):
        return value_str[: -len(suffix)]
    return value_str


def wrap_text(value: str, width: int = 80, break_long_words: bool = True) -> str:
    """
    Wrap text to specified width.

    Args:
        value: Text to wrap
        width: Maximum line width (default: 80)
        break_long_words: Whether to break words longer than width (default: True)

    Example:
        {{ long_text | wrap_text(40) }}
    """
    return textwrap.fill(str(value), width=width, break_long_words=break_long_words)


def truncate_custom(value: str, length: int, end: str = "...") -> str:
    """
    Truncate string to specified length with custom ending.

    Example:
        {{ "Hello World" | truncate_custom(8) }} -> "Hello..."
        {{ "Hello World" | truncate_custom(8, end=">>") }} -> "Hello>>"
    """
    value_str = str(value)
    if len(value_str) <= length:
        return value_str
    return value_str[: length - len(end)] + end


def regex_replace(value: str, pattern: str, replacement: str, count: int = 0) -> str:
    r"""
    Replace using regular expressions.

    Args:
        value: String to process
        pattern: Regular expression pattern
        replacement: Replacement string
        count: Maximum number of replacements (0 = all, default)

    Example:
        {{ "test123" | regex_replace(r'\d+', 'NUM') }} -> "testNUM"
        {{ "a1b2c3" | regex_replace(r'\d', 'X', count=2) }} -> "aXbXc3"
    """
    return re.sub(pattern, replacement, str(value), count=count)


def regex_search(value: str, pattern: str) -> bool:
    r"""
    Check if pattern matches anywhere in string.

    Example:
        {{ "test123" | regex_search(r'\d+') }} -> True
        {{ "test" | regex_search(r'\d+') }} -> False
    """
    return bool(re.search(pattern, str(value)))


def regex_findall(value: str, pattern: str) -> list:
    r"""
    Find all matches of pattern in string.

    Example:
        {{ "test 123 hello 456" | regex_findall(r'\d+') }} -> ["123", "456"]
    """
    return re.findall(pattern, str(value))


def quote_string(value: str, quote_char: str = '"') -> str:
    """
    Wrap string in quotes, escaping any quotes inside.

    Example:
        {{ 'hello' | quote_string }} -> '"hello"'
        {{ "it's" | quote_string("'") }} -> "'it\\'s'"
    """
    escaped = str(value).replace(quote_char, "\\" + quote_char)
    return f"{quote_char}{escaped}{quote_char}"


def get_string_filters() -> Dict[str, Callable]:
    """Get all string filters."""
    return {
        "camelcase": camelcase,
        "pascalcase": pascalcase,
        "snakecase": snakecase,
        "kebabcase": kebabcase,
        "screamingsnakecase": screamingsnakecase,
        "normalize": normalize,
        "slugify": slugify,
        "indent_custom": indent_custom,
        "remove_prefix": remove_prefix,
        "remove_suffix": remove_suffix,
        "wrap_text": wrap_text,
        "truncate_custom": truncate_custom,
        "regex_replace": regex_replace,
        "regex_search": regex_search,
        "regex_findall": regex_findall,
        "quote_string": quote_string,
    }
