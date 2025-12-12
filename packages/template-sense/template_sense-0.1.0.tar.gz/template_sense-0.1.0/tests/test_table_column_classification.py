"""
Unit tests for table column classification via AI.

Tests cover:
- Well-formed AI responses
- Malformed/invalid responses
- Empty responses
- Partial successes (some columns valid, some invalid)
- Provider errors
"""

from unittest.mock import Mock

import pytest

from template_sense.ai.table_column_classification import (
    ClassifiedTableColumn,
    classify_table_columns,
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
        "sheet_name": "Invoice Template",
        "header_candidates": [],
        "table_candidates": [
            {
                "header_row": {
                    "cells": [
                        {"col": 2, "value": "Item Code"},
                        {"col": 3, "value": "Description"},
                        {"col": 4, "value": "Quantity"},
                    ]
                },
                "sample_data_rows": [
                    ["ABC123", "Widget A", 10],
                    ["DEF456", "Widget B", 20],
                ],
            }
        ],
        "field_dictionary": {
            "item_code": ["Item Code", "Product Code", "商品コード"],
            "item_description": ["Description", "Item Name", "商品名"],
            "quantity": ["Quantity", "Qty", "数量"],
        },
    }


class TestClassifyTableColumnsSuccess:
    """Tests for successful table column classification scenarios."""

    def test_classify_columns_well_formed_response(self, mock_provider, sample_payload):
        """Test successful classification with well-formed AI response."""
        # Mock AI provider response
        mock_provider.classify_fields.return_value = {
            "columns": [
                {
                    "raw_label": "Item Code",
                    "raw_position": 0,
                    "table_block_index": 0,
                    "row_index": 5,
                    "col_index": 2,
                    "sample_values": ["ABC123", "DEF456"],
                    "model_confidence": 0.95,
                },
                {
                    "raw_label": "Description",
                    "raw_position": 1,
                    "table_block_index": 0,
                    "row_index": 5,
                    "col_index": 3,
                    "sample_values": ["Widget A", "Widget B"],
                    "model_confidence": 0.92,
                },
                {
                    "raw_label": "Quantity",
                    "raw_position": 2,
                    "table_block_index": 0,
                    "row_index": 5,
                    "col_index": 4,
                    "sample_values": [10, 20],
                    "model_confidence": 0.88,
                },
            ]
        }

        # Call classify_table_columns
        result = classify_table_columns(mock_provider, sample_payload)

        # Assertions
        assert len(result) == 3
        assert all(isinstance(col, ClassifiedTableColumn) for col in result)

        # Check first column
        assert result[0].raw_label == "Item Code"
        assert result[0].raw_position == 0
        assert result[0].table_block_index == 0
        assert result[0].row_index == 5
        assert result[0].col_index == 2
        assert result[0].sample_values == ["ABC123", "DEF456"]
        assert result[0].model_confidence == 0.95
        assert result[0].canonical_key is None  # Not yet mapped

        # Check second column
        assert result[1].raw_label == "Description"
        assert result[1].raw_position == 1
        assert result[1].sample_values == ["Widget A", "Widget B"]

        # Check third column
        assert result[2].raw_label == "Quantity"
        assert result[2].sample_values == [10, 20]

        # Verify provider was called with correct payload and context
        mock_provider.classify_fields.assert_called_once_with(sample_payload, context="columns")

    def test_classify_columns_with_metadata(self, mock_provider, sample_payload):
        """Test classification with optional metadata field."""
        mock_provider.classify_fields.return_value = {
            "columns": [
                {
                    "raw_label": "Item Code",
                    "raw_position": 0,
                    "table_block_index": 0,
                    "row_index": 5,
                    "col_index": 2,
                    "sample_values": ["ABC123", "DEF456"],
                    "model_confidence": 0.95,
                    "metadata": {
                        "column_type": "alphanumeric",
                        "pattern_detected": "^[A-Z]{3}\\d{3}$",
                    },
                }
            ]
        }

        result = classify_table_columns(mock_provider, sample_payload)

        assert len(result) == 1
        assert result[0].metadata is not None
        assert result[0].metadata["column_type"] == "alphanumeric"
        assert "pattern_detected" in result[0].metadata

    def test_classify_columns_without_confidence(self, mock_provider, sample_payload):
        """Test classification when model doesn't provide confidence scores."""
        mock_provider.classify_fields.return_value = {
            "columns": [
                {
                    "raw_label": "Item Code",
                    "raw_position": 0,
                    "table_block_index": 0,
                    "row_index": 5,
                    "col_index": 2,
                    "sample_values": ["ABC123", "DEF456"],
                    # No model_confidence field
                }
            ]
        }

        result = classify_table_columns(mock_provider, sample_payload)

        assert len(result) == 1
        assert result[0].model_confidence is None

    def test_classify_columns_with_none_label(self, mock_provider, sample_payload):
        """Test classification when label is None (no clear header detected)."""
        mock_provider.classify_fields.return_value = {
            "columns": [
                {
                    "raw_label": None,  # No label detected
                    "raw_position": 0,
                    "table_block_index": 0,
                    "row_index": 5,
                    "col_index": 2,
                    "sample_values": ["ABC123", "DEF456"],
                    "model_confidence": 0.75,
                }
            ]
        }

        result = classify_table_columns(mock_provider, sample_payload)

        assert len(result) == 1
        assert result[0].raw_label is None
        assert result[0].sample_values == ["ABC123", "DEF456"]

    def test_classify_columns_empty_sample_values(self, mock_provider, sample_payload):
        """Test classification with empty sample values list."""
        mock_provider.classify_fields.return_value = {
            "columns": [
                {
                    "raw_label": "Item Code",
                    "raw_position": 0,
                    "table_block_index": 0,
                    "row_index": 5,
                    "col_index": 2,
                    "sample_values": [],  # Empty but valid
                    "model_confidence": 0.85,
                }
            ]
        }

        result = classify_table_columns(mock_provider, sample_payload)

        assert len(result) == 1
        assert result[0].sample_values == []

    def test_classify_columns_empty_response(self, mock_provider, sample_payload):
        """Test classification with empty columns list."""
        mock_provider.classify_fields.return_value = {"columns": []}

        result = classify_table_columns(mock_provider, sample_payload)

        assert result == []
        assert isinstance(result, list)

    def test_classify_columns_multiple_tables(self, mock_provider, sample_payload):
        """Test classification with columns from multiple tables."""
        mock_provider.classify_fields.return_value = {
            "columns": [
                # Table 0, Column 0
                {
                    "raw_label": "Item Code",
                    "raw_position": 0,
                    "table_block_index": 0,
                    "row_index": 5,
                    "col_index": 2,
                    "sample_values": ["ABC123"],
                    "model_confidence": 0.95,
                },
                # Table 0, Column 1
                {
                    "raw_label": "Quantity",
                    "raw_position": 1,
                    "table_block_index": 0,
                    "row_index": 5,
                    "col_index": 3,
                    "sample_values": [10],
                    "model_confidence": 0.90,
                },
                # Table 1, Column 0
                {
                    "raw_label": "Date",
                    "raw_position": 0,
                    "table_block_index": 1,
                    "row_index": 20,
                    "col_index": 1,
                    "sample_values": ["2025-01-15"],
                    "model_confidence": 0.88,
                },
            ]
        }

        result = classify_table_columns(mock_provider, sample_payload)

        assert len(result) == 3
        assert result[0].table_block_index == 0
        assert result[1].table_block_index == 0
        assert result[2].table_block_index == 1


class TestClassifyTableColumnsErrors:
    """Tests for error handling in table column classification."""

    def test_classify_columns_missing_columns_key(self, mock_provider, sample_payload):
        """Test error when response is missing 'columns' key."""
        mock_provider.classify_fields.return_value = {"some_other_key": []}  # Missing 'columns' key

        with pytest.raises(AIProviderError) as exc_info:
            classify_table_columns(mock_provider, sample_payload)

        assert "missing required 'columns' key" in str(exc_info.value).lower()
        assert exc_info.value.provider_name == "test-provider"
        assert exc_info.value.request_type == "classify_fields"

    def test_classify_columns_non_dict_response(self, mock_provider, sample_payload):
        """Test error when response is not a dict."""
        mock_provider.classify_fields.return_value = ["not", "a", "dict"]

        with pytest.raises(AIProviderError) as exc_info:
            classify_table_columns(mock_provider, sample_payload)

        assert "expected dict response" in str(exc_info.value).lower()

    def test_classify_columns_columns_not_list(self, mock_provider, sample_payload):
        """Test error when 'columns' value is not a list."""
        mock_provider.classify_fields.return_value = {"columns": "not a list"}  # Should be a list

        with pytest.raises(AIProviderError) as exc_info:
            classify_table_columns(mock_provider, sample_payload)

        assert "'columns' must be a list" in str(exc_info.value).lower()

    def test_classify_columns_provider_raises_error(self, mock_provider, sample_payload):
        """Test handling when AI provider raises an error."""
        mock_provider.classify_fields.side_effect = AIProviderError(
            provider_name="test-provider",
            error_details="API rate limit exceeded",
            request_type="classify_fields",
        )

        with pytest.raises(AIProviderError) as exc_info:
            classify_table_columns(mock_provider, sample_payload)

        assert "API rate limit exceeded" in str(exc_info.value)

    def test_classify_columns_provider_raises_unexpected_error(self, mock_provider, sample_payload):
        """Test handling when provider raises unexpected error."""
        mock_provider.classify_fields.side_effect = ValueError("Unexpected error")

        with pytest.raises(AIProviderError) as exc_info:
            classify_table_columns(mock_provider, sample_payload)

        assert "Unexpected error" in str(exc_info.value)
        assert exc_info.value.provider_name == "test-provider"


class TestClassifyTableColumnsPartialSuccess:
    """Tests for partial success scenarios (some columns parse, some don't)."""

    def test_classify_columns_partial_valid_columns(self, mock_provider, sample_payload):
        """Test partial success when some columns are valid, others invalid."""
        mock_provider.classify_fields.return_value = {
            "columns": [
                # Valid column
                {
                    "raw_label": "Item Code",
                    "raw_position": 0,
                    "table_block_index": 0,
                    "row_index": 5,
                    "col_index": 2,
                    "sample_values": ["ABC123"],
                    "model_confidence": 0.95,
                },
                # Invalid column (missing required fields)
                {
                    "raw_label": "Description",
                    # Missing raw_position, table_block_index, row_index, col_index, sample_values
                },
                # Valid column
                {
                    "raw_label": "Quantity",
                    "raw_position": 2,
                    "table_block_index": 0,
                    "row_index": 5,
                    "col_index": 4,
                    "sample_values": [10, 20],
                    "model_confidence": 0.88,
                },
            ]
        }

        # Should return only the 2 valid columns
        result = classify_table_columns(mock_provider, sample_payload)

        assert len(result) == 2
        assert result[0].raw_label == "Item Code"
        assert result[1].raw_label == "Quantity"

    def test_classify_columns_missing_sample_values(self, mock_provider, sample_payload):
        """Test that missing sample_values field is rejected."""
        mock_provider.classify_fields.return_value = {
            "columns": [
                {
                    "raw_label": "Item Code",
                    "raw_position": 0,
                    "table_block_index": 0,
                    "row_index": 5,
                    "col_index": 2,
                    # Missing sample_values (required)
                    "model_confidence": 0.95,
                }
            ]
        }

        result = classify_table_columns(mock_provider, sample_payload)

        # Should skip the invalid column
        assert len(result) == 0

    def test_classify_columns_invalid_sample_values_type(self, mock_provider, sample_payload):
        """Test that non-list sample_values is rejected."""
        mock_provider.classify_fields.return_value = {
            "columns": [
                {
                    "raw_label": "Item Code",
                    "raw_position": 0,
                    "table_block_index": 0,
                    "row_index": 5,
                    "col_index": 2,
                    "sample_values": "not a list",  # Invalid type
                    "model_confidence": 0.95,
                }
            ]
        }

        result = classify_table_columns(mock_provider, sample_payload)

        # Should skip the invalid column
        assert len(result) == 0

    def test_classify_columns_invalid_confidence_range(self, mock_provider, sample_payload):
        """Test handling of confidence scores outside valid range."""
        mock_provider.classify_fields.return_value = {
            "columns": [
                {
                    "raw_label": "Item Code",
                    "raw_position": 0,
                    "table_block_index": 0,
                    "row_index": 5,
                    "col_index": 2,
                    "sample_values": ["ABC123"],
                    "model_confidence": 1.5,  # Out of range [0.0, 1.0]
                }
            ]
        }

        result = classify_table_columns(mock_provider, sample_payload)

        assert len(result) == 1
        # Invalid confidence should be set to None
        assert result[0].model_confidence is None

    def test_classify_columns_invalid_confidence_type(self, mock_provider, sample_payload):
        """Test handling of non-numeric confidence scores."""
        mock_provider.classify_fields.return_value = {
            "columns": [
                {
                    "raw_label": "Item Code",
                    "raw_position": 0,
                    "table_block_index": 0,
                    "row_index": 5,
                    "col_index": 2,
                    "sample_values": ["ABC123"],
                    "model_confidence": "high",  # Invalid type
                }
            ]
        }

        result = classify_table_columns(mock_provider, sample_payload)

        assert len(result) == 1
        assert result[0].model_confidence is None

    def test_classify_columns_negative_coordinates(self, mock_provider, sample_payload):
        """Test that negative coordinates are rejected."""
        mock_provider.classify_fields.return_value = {
            "columns": [
                {
                    "raw_label": "Item Code",
                    "raw_position": -1,  # Invalid: negative
                    "table_block_index": 0,
                    "row_index": 5,
                    "col_index": 2,
                    "sample_values": ["ABC123"],
                    "model_confidence": 0.95,
                }
            ]
        }

        result = classify_table_columns(mock_provider, sample_payload)

        # Should skip the invalid column
        assert len(result) == 0

    def test_classify_columns_negative_table_block_index(self, mock_provider, sample_payload):
        """Test that negative table_block_index is rejected."""
        mock_provider.classify_fields.return_value = {
            "columns": [
                {
                    "raw_label": "Item Code",
                    "raw_position": 0,
                    "table_block_index": -1,  # Invalid: negative
                    "row_index": 5,
                    "col_index": 2,
                    "sample_values": ["ABC123"],
                }
            ]
        }

        result = classify_table_columns(mock_provider, sample_payload)

        # Should skip the invalid column
        assert len(result) == 0

    def test_classify_columns_non_dict_column(self, mock_provider, sample_payload):
        """Test handling when a column is not a dict."""
        mock_provider.classify_fields.return_value = {
            "columns": [
                # Valid column
                {
                    "raw_label": "Item Code",
                    "raw_position": 0,
                    "table_block_index": 0,
                    "row_index": 5,
                    "col_index": 2,
                    "sample_values": ["ABC123"],
                },
                # Invalid: not a dict
                "invalid column",
                # Valid column
                {
                    "raw_label": "Quantity",
                    "raw_position": 2,
                    "table_block_index": 0,
                    "row_index": 5,
                    "col_index": 4,
                    "sample_values": [10],
                },
            ]
        }

        result = classify_table_columns(mock_provider, sample_payload)

        # Should return only the 2 valid columns
        assert len(result) == 2
        assert result[0].raw_label == "Item Code"
        assert result[1].raw_label == "Quantity"

    def test_classify_columns_invalid_metadata_type(self, mock_provider, sample_payload):
        """Test handling when metadata is not a dict."""
        mock_provider.classify_fields.return_value = {
            "columns": [
                {
                    "raw_label": "Item Code",
                    "raw_position": 0,
                    "table_block_index": 0,
                    "row_index": 5,
                    "col_index": 2,
                    "sample_values": ["ABC123"],
                    "metadata": "not a dict",  # Invalid type
                }
            ]
        }

        result = classify_table_columns(mock_provider, sample_payload)

        assert len(result) == 1
        # Invalid metadata should be set to None
        assert result[0].metadata is None


class TestClassifyTableColumnsEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_classify_columns_large_coordinates(self, mock_provider, sample_payload):
        """Test with very large coordinate values."""
        mock_provider.classify_fields.return_value = {
            "columns": [
                {
                    "raw_label": "Item Code",
                    "raw_position": 100,
                    "table_block_index": 999,
                    "row_index": 10000,
                    "col_index": 500,
                    "sample_values": ["ABC123"],
                    "model_confidence": 0.95,
                }
            ]
        }

        result = classify_table_columns(mock_provider, sample_payload)

        assert len(result) == 1
        assert result[0].raw_position == 100
        assert result[0].table_block_index == 999
        assert result[0].row_index == 10000
        assert result[0].col_index == 500

    def test_classify_columns_zero_coordinates(self, mock_provider, sample_payload):
        """Test with zero coordinate values (valid)."""
        mock_provider.classify_fields.return_value = {
            "columns": [
                {
                    "raw_label": "Item Code",
                    "raw_position": 0,
                    "table_block_index": 0,
                    "row_index": 0,
                    "col_index": 0,
                    "sample_values": ["ABC123"],
                    "model_confidence": 0.95,
                }
            ]
        }

        result = classify_table_columns(mock_provider, sample_payload)

        assert len(result) == 1
        assert result[0].raw_position == 0
        assert result[0].table_block_index == 0
        assert result[0].row_index == 0
        assert result[0].col_index == 0

    def test_classify_columns_boundary_confidence_values(self, mock_provider, sample_payload):
        """Test confidence values at boundaries (0.0 and 1.0)."""
        mock_provider.classify_fields.return_value = {
            "columns": [
                {
                    "raw_label": "Column 1",
                    "raw_position": 0,
                    "table_block_index": 0,
                    "row_index": 5,
                    "col_index": 2,
                    "sample_values": ["Value 1"],
                    "model_confidence": 0.0,  # Minimum valid
                },
                {
                    "raw_label": "Column 2",
                    "raw_position": 1,
                    "table_block_index": 0,
                    "row_index": 5,
                    "col_index": 3,
                    "sample_values": ["Value 2"],
                    "model_confidence": 1.0,  # Maximum valid
                },
            ]
        }

        result = classify_table_columns(mock_provider, sample_payload)

        assert len(result) == 2
        assert result[0].model_confidence == 0.0
        assert result[1].model_confidence == 1.0

    def test_classify_columns_complex_sample_value_types(self, mock_provider, sample_payload):
        """Test with various sample value types (strings, numbers, booleans, None)."""
        mock_provider.classify_fields.return_value = {
            "columns": [
                {
                    "raw_label": "Mixed Values",
                    "raw_position": 0,
                    "table_block_index": 0,
                    "row_index": 5,
                    "col_index": 2,
                    "sample_values": ["text", 123, 45.67, True, None],
                    "model_confidence": 0.85,
                }
            ]
        }

        result = classify_table_columns(mock_provider, sample_payload)

        assert len(result) == 1
        assert result[0].sample_values == ["text", 123, 45.67, True, None]

    def test_classify_columns_unicode_labels(self, mock_provider, sample_payload):
        """Test with Unicode/non-English labels."""
        mock_provider.classify_fields.return_value = {
            "columns": [
                {
                    "raw_label": "商品コード",  # Japanese
                    "raw_position": 0,
                    "table_block_index": 0,
                    "row_index": 5,
                    "col_index": 2,
                    "sample_values": ["ABC123", "DEF456"],
                    "model_confidence": 0.92,
                },
                {
                    "raw_label": "数量",  # Japanese
                    "raw_position": 1,
                    "table_block_index": 0,
                    "row_index": 5,
                    "col_index": 3,
                    "sample_values": [10, 20],
                    "model_confidence": 0.88,
                },
            ]
        }

        result = classify_table_columns(mock_provider, sample_payload)

        assert len(result) == 2
        assert result[0].raw_label == "商品コード"
        assert result[1].raw_label == "数量"
