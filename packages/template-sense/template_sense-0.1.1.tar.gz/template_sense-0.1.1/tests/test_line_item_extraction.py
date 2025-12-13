"""
Unit tests for row-level line item extraction via AI.

Tests cover:
- Well-formed AI responses
- Malformed/invalid responses
- Empty responses
- Partial successes (some items valid, some invalid)
- Provider errors
- Edge cases (subtotal rows, empty columns, etc.)
"""

from unittest.mock import Mock

import pytest

from template_sense.ai.line_item_extraction import (
    ExtractedLineItem,
    extract_line_items,
)
from template_sense.ai_providers.interface import AIProvider
from template_sense.errors import AIProviderError


@pytest.fixture
def mock_provider():
    """Create a mock AIProvider for testing."""
    provider = Mock(spec=AIProvider)
    provider.provider_name = "test-provider"
    provider.model = "test-model"
    return provider


@pytest.fixture
def sample_payload():
    """Sample AI payload for testing."""
    return {
        "table_candidates": [
            {
                "table_index": 0,
                "header_row": {
                    "row_index": 5,
                    "columns": ["Item", "Quantity", "Price", "Total"],
                },
                "column_classifications": [
                    {"col_index": 0, "canonical_key": "product_name"},
                    {"col_index": 1, "canonical_key": "quantity"},
                    {"col_index": 2, "canonical_key": "unit_price"},
                    {"col_index": 3, "canonical_key": "total_price"},
                ],
                "sample_data_rows": [
                    ["Widget A", 5, 10.00, 50.00],
                    ["Widget B", 3, 15.00, 45.00],
                    ["Subtotal", None, None, 95.00],
                ],
            }
        ],
        "field_dictionary": {
            "product_name": ["Item", "Product", "商品名"],
            "quantity": ["Quantity", "Qty", "数量"],
            "unit_price": ["Price", "Unit Price", "単価"],
            "total_price": ["Total", "Amount", "合計"],
        },
    }


class TestExtractLineItemsSuccess:
    """Tests for successful line item extraction scenarios."""

    def test_extract_line_items_well_formed(self, mock_provider, sample_payload):
        """Test successful extraction with well-formed AI response."""
        # Mock AI provider response
        mock_provider.classify_fields.return_value = {
            "line_items": [
                {
                    "table_index": 0,
                    "row_index": 6,
                    "line_number": 1,
                    "columns": {
                        "product_name": "Widget A",
                        "quantity": 5,
                        "unit_price": 10.00,
                        "total_price": 50.00,
                    },
                    "is_subtotal": False,
                    "model_confidence": 0.95,
                },
                {
                    "table_index": 0,
                    "row_index": 7,
                    "line_number": 2,
                    "columns": {
                        "product_name": "Widget B",
                        "quantity": 3,
                        "unit_price": 15.00,
                        "total_price": 45.00,
                    },
                    "is_subtotal": False,
                    "model_confidence": 0.93,
                },
            ]
        }

        # Call extract_line_items
        result = extract_line_items(mock_provider, sample_payload)

        # Assertions
        assert len(result) == 2
        assert all(isinstance(item, ExtractedLineItem) for item in result)

        # Check first item
        assert result[0].table_index == 0
        assert result[0].row_index == 6
        assert result[0].line_number == 1
        assert result[0].columns["product_name"] == "Widget A"
        assert result[0].columns["quantity"] == 5
        assert result[0].is_subtotal is False
        assert result[0].model_confidence == 0.95

        # Check second item
        assert result[1].row_index == 7
        assert result[1].line_number == 2
        assert result[1].columns["product_name"] == "Widget B"

        # Verify provider was called with correct payload
        mock_provider.classify_fields.assert_called_once_with(sample_payload, context="line_items")

    def test_optional_fields_present(self, mock_provider, sample_payload):
        """Test extraction with all optional fields present."""
        mock_provider.classify_fields.return_value = {
            "line_items": [
                {
                    "table_index": 0,
                    "row_index": 6,
                    "line_number": 1,
                    "columns": {"product_name": "Widget A"},
                    "is_subtotal": False,
                    "model_confidence": 0.88,
                    "metadata": {
                        "extraction_method": "pattern_match",
                        "cell_formats": ["text", "number", "currency"],
                    },
                }
            ]
        }

        result = extract_line_items(mock_provider, sample_payload)

        assert len(result) == 1
        assert result[0].model_confidence == 0.88
        assert result[0].metadata is not None
        assert result[0].metadata["extraction_method"] == "pattern_match"
        assert "cell_formats" in result[0].metadata

    def test_optional_fields_absent(self, mock_provider, sample_payload):
        """Test extraction when optional fields are missing."""
        mock_provider.classify_fields.return_value = {
            "line_items": [
                {
                    "table_index": 0,
                    "row_index": 6,
                    "line_number": None,  # Optional field explicitly None
                    "columns": {"product_name": "Widget A"},
                    # No is_subtotal, model_confidence, or metadata
                }
            ]
        }

        result = extract_line_items(mock_provider, sample_payload)

        assert len(result) == 1
        assert result[0].line_number is None
        assert result[0].is_subtotal is False  # Default value
        assert result[0].model_confidence is None
        assert result[0].metadata is None

    def test_empty_columns_dict(self, mock_provider, sample_payload):
        """Test extraction with empty columns dictionary."""
        mock_provider.classify_fields.return_value = {
            "line_items": [
                {
                    "table_index": 0,
                    "row_index": 6,
                    "line_number": 1,
                    "columns": {},  # Empty but valid
                }
            ]
        }

        result = extract_line_items(mock_provider, sample_payload)

        assert len(result) == 1
        assert result[0].columns == {}
        assert isinstance(result[0].columns, dict)


class TestExtractLineItemsErrors:
    """Tests for error handling in line item extraction."""

    def test_response_not_dict(self, mock_provider, sample_payload):
        """Test error when response is not a dict."""
        mock_provider.classify_fields.return_value = ["not", "a", "dict"]

        with pytest.raises(AIProviderError) as exc_info:
            extract_line_items(mock_provider, sample_payload)

        assert "expected dict response" in str(exc_info.value).lower()
        assert exc_info.value.provider_name == "test-provider"

    def test_missing_line_items_key(self, mock_provider, sample_payload):
        """Test error when response is missing 'line_items' key."""
        mock_provider.classify_fields.return_value = {
            "some_other_key": []  # Missing 'line_items' key
        }

        with pytest.raises(AIProviderError) as exc_info:
            extract_line_items(mock_provider, sample_payload)

        assert "missing required 'line_items' key" in str(exc_info.value).lower()
        assert exc_info.value.provider_name == "test-provider"
        assert exc_info.value.request_type == "classify_fields"

    def test_line_items_not_list(self, mock_provider, sample_payload):
        """Test error when 'line_items' value is not a list."""
        mock_provider.classify_fields.return_value = {
            "line_items": "not a list"  # Should be a list
        }

        with pytest.raises(AIProviderError) as exc_info:
            extract_line_items(mock_provider, sample_payload)

        assert "'line_items' must be a list" in str(exc_info.value).lower()

    def test_provider_exception(self, mock_provider, sample_payload):
        """Test handling when AI provider raises an error."""
        mock_provider.classify_fields.side_effect = AIProviderError(
            provider_name="test-provider",
            error_details="API rate limit exceeded",
            request_type="classify_fields",
        )

        with pytest.raises(AIProviderError) as exc_info:
            extract_line_items(mock_provider, sample_payload)

        assert "API rate limit exceeded" in str(exc_info.value)

    def test_provider_unexpected_error(self, mock_provider, sample_payload):
        """Test handling when provider raises unexpected error."""
        mock_provider.classify_fields.side_effect = ValueError("Unexpected error")

        with pytest.raises(AIProviderError) as exc_info:
            extract_line_items(mock_provider, sample_payload)

        assert "Unexpected error" in str(exc_info.value)
        assert exc_info.value.provider_name == "test-provider"


class TestExtractLineItemsPartialSuccess:
    """Tests for partial success scenarios (some items parse, some don't)."""

    def test_some_valid_some_invalid(self, mock_provider, sample_payload):
        """Test partial success when some items are valid, others invalid."""
        mock_provider.classify_fields.return_value = {
            "line_items": [
                # Valid item
                {
                    "table_index": 0,
                    "row_index": 6,
                    "line_number": 1,
                    "columns": {"product_name": "Widget A"},
                    "model_confidence": 0.95,
                },
                # Invalid item (missing required table_index)
                {
                    "row_index": 7,
                    "line_number": 2,
                    "columns": {"product_name": "Widget B"},
                },
                # Valid item
                {
                    "table_index": 0,
                    "row_index": 8,
                    "line_number": 3,
                    "columns": {"product_name": "Widget C"},
                    "model_confidence": 0.88,
                },
            ]
        }

        # Should return only the 2 valid items
        result = extract_line_items(mock_provider, sample_payload)

        assert len(result) == 2
        assert result[0].columns["product_name"] == "Widget A"
        assert result[1].columns["product_name"] == "Widget C"

    def test_invalid_confidence_range(self, mock_provider, sample_payload):
        """Test handling of confidence scores outside valid range."""
        mock_provider.classify_fields.return_value = {
            "line_items": [
                {
                    "table_index": 0,
                    "row_index": 6,
                    "line_number": 1,
                    "columns": {"product_name": "Widget A"},
                    "model_confidence": 1.5,  # Out of range [0.0, 1.0]
                }
            ]
        }

        result = extract_line_items(mock_provider, sample_payload)

        assert len(result) == 1
        # Invalid confidence should be set to None
        assert result[0].model_confidence is None

    def test_missing_required_field(self, mock_provider, sample_payload):
        """Test handling when required field is missing."""
        mock_provider.classify_fields.return_value = {
            "line_items": [
                # Missing 'columns' field (required)
                {
                    "table_index": 0,
                    "row_index": 6,
                    "line_number": 1,
                    # Missing columns
                }
            ]
        }

        # Should skip the invalid item
        result = extract_line_items(mock_provider, sample_payload)

        assert len(result) == 0

    def test_invalid_metadata_type(self, mock_provider, sample_payload):
        """Test handling when metadata is not a dict."""
        mock_provider.classify_fields.return_value = {
            "line_items": [
                {
                    "table_index": 0,
                    "row_index": 6,
                    "line_number": 1,
                    "columns": {"product_name": "Widget A"},
                    "metadata": "not a dict",  # Invalid type
                }
            ]
        }

        result = extract_line_items(mock_provider, sample_payload)

        assert len(result) == 1
        # Invalid metadata should be set to None
        assert result[0].metadata is None

    def test_non_dict_item(self, mock_provider, sample_payload):
        """Test handling when an item is not a dict."""
        mock_provider.classify_fields.return_value = {
            "line_items": [
                # Valid item
                {
                    "table_index": 0,
                    "row_index": 6,
                    "line_number": 1,
                    "columns": {"product_name": "Widget A"},
                },
                # Invalid: not a dict
                "invalid item",
                # Valid item
                {
                    "table_index": 0,
                    "row_index": 7,
                    "line_number": 2,
                    "columns": {"product_name": "Widget B"},
                },
            ]
        }

        result = extract_line_items(mock_provider, sample_payload)

        # Should return only the 2 valid items
        assert len(result) == 2
        assert result[0].columns["product_name"] == "Widget A"
        assert result[1].columns["product_name"] == "Widget B"

    def test_negative_indices(self, mock_provider, sample_payload):
        """Test that negative indices are rejected."""
        mock_provider.classify_fields.return_value = {
            "line_items": [
                {
                    "table_index": -1,  # Invalid: negative
                    "row_index": 6,
                    "line_number": 1,
                    "columns": {"product_name": "Widget A"},
                }
            ]
        }

        result = extract_line_items(mock_provider, sample_payload)

        # Should skip the invalid item
        assert len(result) == 0


class TestExtractLineItemsEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_subtotal_row_detection(self, mock_provider, sample_payload):
        """Test extraction of subtotal rows."""
        mock_provider.classify_fields.return_value = {
            "line_items": [
                {
                    "table_index": 0,
                    "row_index": 6,
                    "line_number": 1,
                    "columns": {"product_name": "Widget A", "total_price": 50.00},
                    "is_subtotal": False,
                },
                {
                    "table_index": 0,
                    "row_index": 7,
                    "line_number": None,  # Subtotals typically don't have line numbers
                    "columns": {"product_name": "Subtotal", "total_price": 95.00},
                    "is_subtotal": True,
                },
            ]
        }

        result = extract_line_items(mock_provider, sample_payload)

        assert len(result) == 2
        assert result[0].is_subtotal is False
        assert result[1].is_subtotal is True
        assert result[1].line_number is None

    def test_none_line_number(self, mock_provider, sample_payload):
        """Test handling of None line_number (valid case)."""
        mock_provider.classify_fields.return_value = {
            "line_items": [
                {
                    "table_index": 0,
                    "row_index": 6,
                    "line_number": None,  # Valid: no line number column
                    "columns": {"product_name": "Widget A"},
                }
            ]
        }

        result = extract_line_items(mock_provider, sample_payload)

        assert len(result) == 1
        assert result[0].line_number is None

    def test_large_row_indices(self, mock_provider, sample_payload):
        """Test with very large row index values."""
        mock_provider.classify_fields.return_value = {
            "line_items": [
                {
                    "table_index": 999,
                    "row_index": 10000,
                    "line_number": 5000,
                    "columns": {"product_name": "Widget A"},
                    "model_confidence": 0.95,
                }
            ]
        }

        result = extract_line_items(mock_provider, sample_payload)

        assert len(result) == 1
        assert result[0].table_index == 999
        assert result[0].row_index == 10000
        assert result[0].line_number == 5000

    def test_empty_line_items_list(self, mock_provider, sample_payload):
        """Test extraction with empty line_items list."""
        mock_provider.classify_fields.return_value = {"line_items": []}

        result = extract_line_items(mock_provider, sample_payload)

        assert result == []
        assert isinstance(result, list)

    def test_zero_indices(self, mock_provider, sample_payload):
        """Test with zero index values (valid)."""
        mock_provider.classify_fields.return_value = {
            "line_items": [
                {
                    "table_index": 0,
                    "row_index": 0,
                    "line_number": 0,
                    "columns": {"product_name": "Widget A"},
                }
            ]
        }

        result = extract_line_items(mock_provider, sample_payload)

        assert len(result) == 1
        assert result[0].table_index == 0
        assert result[0].row_index == 0
        assert result[0].line_number == 0

    def test_boundary_confidence_values(self, mock_provider, sample_payload):
        """Test confidence values at boundaries (0.0 and 1.0)."""
        mock_provider.classify_fields.return_value = {
            "line_items": [
                {
                    "table_index": 0,
                    "row_index": 6,
                    "line_number": 1,
                    "columns": {"product_name": "Widget A"},
                    "model_confidence": 0.0,  # Minimum valid
                },
                {
                    "table_index": 0,
                    "row_index": 7,
                    "line_number": 2,
                    "columns": {"product_name": "Widget B"},
                    "model_confidence": 1.0,  # Maximum valid
                },
            ]
        }

        result = extract_line_items(mock_provider, sample_payload)

        assert len(result) == 2
        assert result[0].model_confidence == 0.0
        assert result[1].model_confidence == 1.0

    def test_complex_column_value_types(self, mock_provider, sample_payload):
        """Test with various column value types (numbers, booleans, None, etc.)."""
        mock_provider.classify_fields.return_value = {
            "line_items": [
                {
                    "table_index": 0,
                    "row_index": 6,
                    "line_number": 1,
                    "columns": {
                        "product_name": "Widget A",
                        "quantity": 10,
                        "unit_price": 15.99,
                        "is_taxable": True,
                        "discount": None,
                    },
                }
            ]
        }

        result = extract_line_items(mock_provider, sample_payload)

        assert len(result) == 1
        assert result[0].columns["product_name"] == "Widget A"
        assert result[0].columns["quantity"] == 10
        assert result[0].columns["unit_price"] == 15.99
        assert result[0].columns["is_taxable"] is True
        assert result[0].columns["discount"] is None

    def test_invalid_is_subtotal_type(self, mock_provider, sample_payload):
        """Test handling when is_subtotal is not a boolean."""
        mock_provider.classify_fields.return_value = {
            "line_items": [
                {
                    "table_index": 0,
                    "row_index": 6,
                    "line_number": 1,
                    "columns": {"product_name": "Widget A"},
                    "is_subtotal": "yes",  # Invalid: should be bool
                }
            ]
        }

        # Should skip the invalid item due to type error
        result = extract_line_items(mock_provider, sample_payload)

        assert len(result) == 0

    def test_invalid_confidence_type(self, mock_provider, sample_payload):
        """Test handling of non-numeric confidence scores."""
        mock_provider.classify_fields.return_value = {
            "line_items": [
                {
                    "table_index": 0,
                    "row_index": 6,
                    "line_number": 1,
                    "columns": {"product_name": "Widget A"},
                    "model_confidence": "high",  # Invalid type
                }
            ]
        }

        result = extract_line_items(mock_provider, sample_payload)

        assert len(result) == 1
        # Invalid confidence should be set to None
        assert result[0].model_confidence is None

    def test_columns_not_dict(self, mock_provider, sample_payload):
        """Test error when columns is not a dict."""
        mock_provider.classify_fields.return_value = {
            "line_items": [
                {
                    "table_index": 0,
                    "row_index": 6,
                    "line_number": 1,
                    "columns": ["not", "a", "dict"],  # Invalid: should be dict
                }
            ]
        }

        # Should skip the invalid item
        result = extract_line_items(mock_provider, sample_payload)

        assert len(result) == 0
