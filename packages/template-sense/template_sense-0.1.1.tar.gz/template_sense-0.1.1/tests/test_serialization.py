"""Tests for serialization utilities.

Author: Template Sense Team
Created: 2025-12-05
"""

import datetime
import json

from template_sense.serialization import (
    _serialize_value,
    make_json_serializable,
    serialize_to_json,
)


class TestSerializeValue:
    """Tests for _serialize_value function."""

    def test_datetime_to_iso_string(self):
        """Test datetime.datetime converts to ISO 8601 format."""
        dt = datetime.datetime(2024, 5, 8, 10, 30, 0)
        result = _serialize_value(dt)
        assert result == "2024-05-08T10:30:00"

    def test_date_to_iso_string(self):
        """Test datetime.date converts to ISO 8601 format."""
        d = datetime.date(2024, 5, 8)
        result = _serialize_value(d)
        assert result == "2024-05-08"

    def test_time_to_iso_string(self):
        """Test datetime.time converts to ISO 8601 format."""
        t = datetime.time(14, 30, 0)
        result = _serialize_value(t)
        assert result == "14:30:00"

    def test_datetime_with_microseconds(self):
        """Test datetime with microseconds preserves precision."""
        dt = datetime.datetime(2024, 5, 8, 10, 30, 0, 123456)
        result = _serialize_value(dt)
        assert result == "2024-05-08T10:30:00.123456"

    def test_primitive_types_unchanged(self):
        """Test that primitive types pass through unchanged."""
        assert _serialize_value("hello") == "hello"
        assert _serialize_value(123) == 123
        assert _serialize_value(45.67) == 45.67
        assert _serialize_value(True) is True
        assert _serialize_value(None) is None

    def test_list_unchanged(self):
        """Test that lists pass through unchanged (recursion handled by make_json_serializable)."""
        original = [1, 2, 3]
        result = _serialize_value(original)
        assert result is original  # Same object reference


class TestMakeJsonSerializable:
    """Tests for make_json_serializable function."""

    def test_nested_dict_with_datetime(self):
        """Test nested dictionaries with datetime objects."""
        obj = {
            "date": datetime.date(2024, 5, 8),
            "nested": {"timestamp": datetime.datetime(2024, 5, 8, 10, 30, 0)},
        }
        result = make_json_serializable(obj)
        expected = {
            "date": "2024-05-08",
            "nested": {"timestamp": "2024-05-08T10:30:00"},
        }
        assert result == expected

    def test_list_with_datetime(self):
        """Test lists containing datetime objects."""
        obj = [datetime.date(2024, 5, 8), "text", 123]
        result = make_json_serializable(obj)
        expected = ["2024-05-08", "text", 123]
        assert result == expected

    def test_tuple_with_datetime(self):
        """Test tuples containing datetime objects."""
        obj = (datetime.time(14, 30, 0), "text")
        result = make_json_serializable(obj)
        expected = ["14:30:00", "text"]  # Tuples convert to lists
        assert result == expected

    def test_ai_payload_structure(self):
        """Test realistic AI payload structure with datetime values."""
        payload = {
            "header_fields": [
                {"label": "Invoice Date", "value": datetime.date(2024, 5, 8)},
                {"label": "Due Date", "value": datetime.date(2024, 6, 8)},
            ],
            "table_data": {
                "headers": ["Item", "Date"],
                "sample_rows": [
                    ["Widget", datetime.datetime(2024, 5, 1, 9, 0, 0)],
                    ["Gadget", datetime.datetime(2024, 5, 2, 10, 30, 0)],
                ],
            },
        }
        result = make_json_serializable(payload)
        expected = {
            "header_fields": [
                {"label": "Invoice Date", "value": "2024-05-08"},
                {"label": "Due Date", "value": "2024-06-08"},
            ],
            "table_data": {
                "headers": ["Item", "Date"],
                "sample_rows": [
                    ["Widget", "2024-05-01T09:00:00"],
                    ["Gadget", "2024-05-02T10:30:00"],
                ],
            },
        }
        assert result == expected

    def test_empty_structures(self):
        """Test empty dictionaries and lists."""
        assert make_json_serializable({}) == {}
        assert make_json_serializable([]) == []

    def test_deeply_nested_structure(self):
        """Test deeply nested structures with datetime."""
        obj = {
            "level1": {
                "level2": {
                    "level3": {
                        "date": datetime.date(2024, 5, 8),
                        "list": [datetime.time(14, 30, 0)],
                    }
                }
            }
        }
        result = make_json_serializable(obj)
        expected = {"level1": {"level2": {"level3": {"date": "2024-05-08", "list": ["14:30:00"]}}}}
        assert result == expected


class TestSerializeToJson:
    """Tests for serialize_to_json function."""

    def test_simple_dict_with_datetime(self):
        """Test basic dictionary serialization."""
        obj = {"date": datetime.date(2024, 5, 8)}
        result = serialize_to_json(obj)
        parsed = json.loads(result)
        assert parsed == {"date": "2024-05-08"}

    def test_json_string_formatting_with_indent(self):
        """Test JSON string output with indentation."""
        obj = {"date": datetime.date(2024, 5, 8), "time": datetime.time(14, 30, 0)}
        result = serialize_to_json(obj, indent=2)
        # Should be pretty-printed
        assert "\n" in result
        assert "  " in result
        # Should be valid JSON
        parsed = json.loads(result)
        assert parsed == {"date": "2024-05-08", "time": "14:30:00"}

    def test_json_string_formatting_without_indent(self):
        """Test JSON string output without indentation."""
        obj = {"date": datetime.date(2024, 5, 8)}
        result = serialize_to_json(obj)
        # Should be compact (no newlines)
        assert "\n" not in result
        assert result == '{"date": "2024-05-08"}'

    def test_complex_payload(self):
        """Test complex nested payload serialization."""
        payload = {
            "metadata": {"created": datetime.datetime(2024, 5, 8, 10, 30, 0)},
            "items": [
                {"date": datetime.date(2024, 5, 1)},
                {"date": datetime.date(2024, 5, 2)},
            ],
        }
        result = serialize_to_json(payload, indent=2)
        parsed = json.loads(result)
        expected = {
            "metadata": {"created": "2024-05-08T10:30:00"},
            "items": [{"date": "2024-05-01"}, {"date": "2024-05-02"}],
        }
        assert parsed == expected
