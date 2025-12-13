"""Formatting filters for Jinja2 templates (dates, numbers, etc.)."""

import html
import json
from datetime import datetime
from typing import Any, Callable, Dict, Optional

try:
    import yaml

    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def format_number(value: float, decimals: int = 2, thousands_sep: str = ",") -> str:
    """
    Format number with thousands separator and decimals.

    Args:
        value: Number to format
        decimals: Number of decimal places (default: 2)
        thousands_sep: Thousands separator character (default: ",")

    Example:
        {{ 1234567.89 | format_number }} -> "1,234,567.89"
        {{ 1234567.89 | format_number(0) }} -> "1,234,568"
        {{ 1234567.89 | format_number(2, " ") }} -> "1 234 567.89"
    """
    # Format with decimals
    formatted = f"{float(value):,.{decimals}f}"

    # Replace comma with custom separator if needed
    if thousands_sep != ",":
        formatted = formatted.replace(",", thousands_sep)

    return formatted


def format_bytes(value: int, precision: int = 2) -> str:
    """
    Format bytes to human-readable size.

    Example:
        {{ 1024 | format_bytes }} -> "1.00 KB"
        {{ 1048576 | format_bytes }} -> "1.00 MB"
        {{ 1073741824 | format_bytes(1) }} -> "1.0 GB"
    """
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = float(value)
    unit_index = 0

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    return f"{size:.{precision}f} {units[unit_index]}"


def format_percentage(value: float, decimals: int = 2, multiply: bool = True) -> str:
    """
    Format number as percentage.

    Args:
        value: Number to format
        decimals: Number of decimal places (default: 2)
        multiply: Whether to multiply by 100 (default: True, for 0.5 -> 50%)

    Example:
        {{ 0.1234 | format_percentage }} -> "12.34%"
        {{ 50 | format_percentage(multiply=false) }} -> "50.00%"
    """
    if multiply:
        value = float(value) * 100
    return f"{float(value):.{decimals}f}%"


def format_date(value: Any, format_str: str = "%Y-%m-%d") -> str:
    """
    Format datetime object or timestamp.

    Args:
        value: datetime object, timestamp, or ISO string
        format_str: strftime format string (default: "%Y-%m-%d")

    Example:
        {{ now() | format_date }} -> "2024-10-11"
        {{ timestamp | format_date("%Y-%m-%d %H:%M:%S") }} -> "2024-10-11 14:30:00"
        {{ "2024-10-11" | format_date("%B %d, %Y") }} -> "October 11, 2024"
    """
    if isinstance(value, datetime):
        dt = value
    elif isinstance(value, (int, float)):
        dt = datetime.fromtimestamp(value)
    elif isinstance(value, str):
        # Try to parse ISO format
        try:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return str(value)
    else:
        return str(value)

    return dt.strftime(format_str)


def format_currency(value: float, symbol: str = "$", position: str = "before") -> str:
    """
    Format number as currency.

    Args:
        value: Amount to format
        symbol: Currency symbol (default: "$")
        position: Symbol position "before" or "after" (default: "before")

    Example:
        {{ 1234.56 | format_currency }} -> "$1,234.56"
        {{ 1234.56 | format_currency("€", "after") }} -> "1,234.56€"
    """
    formatted_value = format_number(value, decimals=2)

    if position == "after":
        return f"{formatted_value}{symbol}"
    return f"{symbol}{formatted_value}"


def format_ordinal(value: int) -> str:
    """
    Convert number to ordinal (1st, 2nd, 3rd, etc.).

    Example:
        {{ 1 | format_ordinal }} -> "1st"
        {{ 22 | format_ordinal }} -> "22nd"
        {{ 103 | format_ordinal }} -> "103rd"
    """
    value = int(value)
    if 10 <= value % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(value % 10, "th")
    return f"{value}{suffix}"


def format_phone(value: str, format_str: str = "({area}) {prefix}-{line}") -> str:
    """
    Format phone number.

    Args:
        value: Phone number digits
        format_str: Format string with placeholders (default: "({area}) {prefix}-{line}")

    Example:
        {{ "1234567890" | format_phone }} -> "(123) 456-7890"
        {{ "1234567890" | format_phone("{area}-{prefix}-{line}") }} -> "123-456-7890"
    """
    # Remove non-digit characters
    digits = "".join(c for c in str(value) if c.isdigit())

    if len(digits) >= 10:
        area = digits[-10:-7]
        prefix = digits[-7:-4]
        line = digits[-4:]
        return format_str.format(area=area, prefix=prefix, line=line)
    return str(value)


def pad_left(value: str, width: int, fillchar: str = " ") -> str:
    """
    Pad string on the left to specified width.

    Example:
        {{ "5" | pad_left(3, "0") }} -> "005"
        {{ "test" | pad_left(10) }} -> "      test"
    """
    return str(value).rjust(width, fillchar)


def pad_right(value: str, width: int, fillchar: str = " ") -> str:
    """
    Pad string on the right to specified width.

    Example:
        {{ "5" | pad_right(3, "0") }} -> "500"
        {{ "test" | pad_right(10) }} -> "test      "
    """
    return str(value).ljust(width, fillchar)


def format_json(value: Any, indent: Optional[int] = 2) -> str:
    """
    Format value as pretty-printed JSON.

    Args:
        value: Value to format as JSON
        indent: Indentation level (default: 2, None for compact)

    Example:
        {{ {"key": "value"} | format_json }} -> formatted JSON string
    """
    return json.dumps(value, indent=indent, ensure_ascii=False)


def format_yaml(value: Any) -> str:
    """
    Format value as YAML (requires PyYAML).

    Example:
        {{ {"key": "value"} | format_yaml }}
    """
    if HAS_YAML:
        return yaml.dump(value, default_flow_style=False, allow_unicode=True)
    # Fallback if PyYAML not installed
    return str(value)


def format_xml_escape(value: str) -> str:
    """
    Escape XML special characters.

    Example:
        {{ "<tag>value</tag>" | format_xml_escape }} -> "&lt;tag&gt;value&lt;/tag&gt;"
    """
    return html.escape(str(value), quote=True)


def format_sql_escape(value: str) -> str:
    """
    Escape single quotes for SQL strings.

    Example:
        {{ "O'Brien" | format_sql_escape }} -> "O''Brien"
    """
    return str(value).replace("'", "''")


def get_formatting_filters() -> Dict[str, Callable]:
    """Get all formatting filters."""
    return {
        "format_number": format_number,
        "format_bytes": format_bytes,
        "format_percentage": format_percentage,
        "format_date": format_date,
        "format_currency": format_currency,
        "format_ordinal": format_ordinal,
        "format_phone": format_phone,
        "pad_left": pad_left,
        "pad_right": pad_right,
        "format_json": format_json,
        "format_yaml": format_yaml,
        "format_xml_escape": format_xml_escape,
        "format_sql_escape": format_sql_escape,
    }
