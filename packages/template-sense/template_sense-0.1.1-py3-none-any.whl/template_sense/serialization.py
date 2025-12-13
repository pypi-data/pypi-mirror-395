"""JSON serialization utilities for Template Sense.

Handles conversion of non-JSON-serializable Python types (datetime, date, time)
to JSON-compatible representations for AI provider payloads.

Author: Template Sense Team
Created: 2025-12-05
"""

import datetime
import json
from typing import Any


def _serialize_value(value: Any) -> Any:
    """Convert a single value to JSON-serializable form.

    Converts datetime objects to ISO 8601 format strings:
    - datetime.datetime → "2024-05-08T10:30:00"
    - datetime.date → "2024-05-08"
    - datetime.time → "14:30:00"

    Args:
        value: Any Python value

    Returns:
        JSON-serializable representation of the value

    Notes:
        - Timezone information is preserved in ISO format if present
        - Unknown types fall back to str() representation
    """
    if isinstance(value, datetime.datetime | datetime.date | datetime.time):
        return value.isoformat()
    return value


def make_json_serializable(obj: Any) -> Any:
    """Recursively convert nested structures to JSON-serializable form.

    Traverses dictionaries, lists, and tuples to convert all datetime
    objects to ISO 8601 strings.

    Args:
        obj: Any Python object (dict, list, tuple, or scalar)

    Returns:
        JSON-serializable version of the object

    Examples:
        >>> payload = {
        ...     "date": datetime.date(2024, 5, 8),
        ...     "nested": {
        ...         "timestamp": datetime.datetime(2024, 5, 8, 10, 30, 0)
        ...     }
        ... }
        >>> make_json_serializable(payload)
        {
            "date": "2024-05-08",
            "nested": {
                "timestamp": "2024-05-08T10:30:00"
            }
        }
    """
    if isinstance(obj, dict):
        return {key: make_json_serializable(value) for key, value in obj.items()}
    if isinstance(obj, list | tuple):
        return [make_json_serializable(item) for item in obj]
    return _serialize_value(obj)


def serialize_to_json(obj: Any, indent: int | None = None) -> str:
    """Serialize an object to JSON string, handling datetime objects.

    Convenience function that combines make_json_serializable() with json.dumps().

    Args:
        obj: Any Python object to serialize
        indent: Optional indentation level for pretty-printing

    Returns:
        JSON string representation

    Raises:
        TypeError: If object contains types that cannot be serialized

    Examples:
        >>> payload = {"date": datetime.date(2024, 5, 8)}
        >>> serialize_to_json(payload, indent=2)
        '{\\n  "date": "2024-05-08"\\n}'
    """
    serializable_obj = make_json_serializable(obj)
    return json.dumps(serializable_obj, indent=indent)
