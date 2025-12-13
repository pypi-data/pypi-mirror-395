"""Helper utilities for the DAY2 CLI."""

from datetime import datetime
from typing import Optional, Union


def format_datetime_string(
    datetime_value: Optional[Union[str, datetime]],
    format_str: str = "%Y-%m-%d %H:%M:%S",
) -> str:
    """Format a datetime string or datetime object to a more readable format.

    Args:
        datetime_value: ISO 8601 datetime string or datetime object (e.g., "2025-09-04T12:05:47.102332Z")
        format_str: Format string for strftime (default: "%Y-%m-%d %H:%M:%S")

    Returns:
        Formatted datetime string or "N/A" if input is None or invalid

    Examples:
        >>> format_datetime_string("2025-09-04T12:05:47.102332Z")
        "2025-09-04 12:05:47"
        >>> format_datetime_string(None)
        "N/A"
    """
    if not datetime_value:
        return "N/A"

    # If it's already a datetime object, format it directly
    if isinstance(datetime_value, datetime):
        return datetime_value.strftime(format_str)

    # If it's a string, parse it first
    try:
        # Handle ISO format with timezone
        if isinstance(datetime_value, str):
            if datetime_value.endswith("Z"):
                datetime_value = datetime_value[:-1] + "+00:00"
            dt = datetime.fromisoformat(datetime_value)
            return dt.strftime(format_str)
    except (ValueError, AttributeError):
        pass

    return "N/A"
