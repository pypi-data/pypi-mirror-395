"""
Unit tests for header field classification via AI.

Tests cover:
- Well-formed AI responses
- Malformed/invalid responses
- Empty responses
- Partial successes (some fields valid, some invalid)
- Provider errors
"""

from unittest.mock import Mock

import pytest

from template_sense.ai.header_classification import (
    ClassifiedHeaderField,
    classify_header_fields,
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
        "header_candidates": [
            {
                "row": 1,
                "col": 1,
                "label": "Invoice Number",
                "value": "INV-12345",
                "score": 0.95,
            },
            {
                "row": 2,
                "col": 1,
                "label": "Date",
                "value": "2025-01-15",
                "score": 0.90,
            },
        ],
        "table_candidates": [],
        "field_dictionary": {
            "invoice_number": ["Invoice Number", "Invoice No", "請求書番号"],
            "invoice_date": ["Date", "Invoice Date", "日付"],
        },
    }


class TestClassifyHeaderFieldsSuccess:
    """Tests for successful header classification scenarios."""

    def test_classify_headers_well_formed_response(self, mock_provider, sample_payload):
        """Test successful classification with well-formed AI response."""
        # Mock AI provider response
        mock_provider.classify_fields.return_value = {
            "headers": [
                {
                    "raw_label": "Invoice Number",
                    "raw_value": "INV-12345",
                    "block_index": 0,
                    "row_index": 1,
                    "col_index": 1,
                    "model_confidence": 0.95,
                },
                {
                    "raw_label": "Date",
                    "raw_value": "2025-01-15",
                    "block_index": 0,
                    "row_index": 2,
                    "col_index": 1,
                    "model_confidence": 0.90,
                },
            ]
        }

        # Call classify_header_fields
        result = classify_header_fields(mock_provider, sample_payload)

        # Assertions
        assert len(result) == 2
        assert all(isinstance(field, ClassifiedHeaderField) for field in result)

        # Check first field
        assert result[0].raw_label == "Invoice Number"
        assert result[0].raw_value == "INV-12345"
        assert result[0].block_index == 0
        assert result[0].row_index == 1
        assert result[0].col_index == 1
        assert result[0].model_confidence == 0.95
        assert result[0].canonical_key is None  # Not yet mapped

        # Check second field
        assert result[1].raw_label == "Date"
        assert result[1].raw_value == "2025-01-15"
        assert result[1].model_confidence == 0.90

        # Verify provider was called with correct payload and context
        mock_provider.classify_fields.assert_called_once_with(sample_payload, context="headers")

    def test_classify_headers_with_metadata(self, mock_provider, sample_payload):
        """Test classification with optional metadata field."""
        mock_provider.classify_fields.return_value = {
            "headers": [
                {
                    "raw_label": "Invoice Number",
                    "raw_value": "INV-12345",
                    "block_index": 0,
                    "row_index": 1,
                    "col_index": 1,
                    "model_confidence": 0.95,
                    "metadata": {
                        "detection_method": "pattern_match",
                        "confidence_breakdown": {"label": 0.97, "value": 0.93},
                    },
                }
            ]
        }

        result = classify_header_fields(mock_provider, sample_payload)

        assert len(result) == 1
        assert result[0].metadata is not None
        assert result[0].metadata["detection_method"] == "pattern_match"
        assert "confidence_breakdown" in result[0].metadata

    def test_classify_headers_without_confidence(self, mock_provider, sample_payload):
        """Test classification when model doesn't provide confidence scores."""
        mock_provider.classify_fields.return_value = {
            "headers": [
                {
                    "raw_label": "Invoice Number",
                    "raw_value": "INV-12345",
                    "block_index": 0,
                    "row_index": 1,
                    "col_index": 1,
                    # No model_confidence field
                }
            ]
        }

        result = classify_header_fields(mock_provider, sample_payload)

        assert len(result) == 1
        assert result[0].model_confidence is None

    def test_classify_headers_with_none_label(self, mock_provider, sample_payload):
        """Test classification when label is None (no clear label detected)."""
        mock_provider.classify_fields.return_value = {
            "headers": [
                {
                    "raw_label": None,  # No label detected
                    "raw_value": "INV-12345",
                    "block_index": 0,
                    "row_index": 1,
                    "col_index": 1,
                    "model_confidence": 0.75,
                }
            ]
        }

        result = classify_header_fields(mock_provider, sample_payload)

        assert len(result) == 1
        assert result[0].raw_label is None
        assert result[0].raw_value == "INV-12345"

    def test_classify_headers_empty_response(self, mock_provider, sample_payload):
        """Test classification with empty headers list."""
        mock_provider.classify_fields.return_value = {"headers": []}

        result = classify_header_fields(mock_provider, sample_payload)

        assert result == []
        assert isinstance(result, list)


class TestClassifyHeaderFieldsErrors:
    """Tests for error handling in header classification."""

    def test_classify_headers_missing_headers_key(self, mock_provider, sample_payload):
        """Test error when response is missing 'headers' key."""
        mock_provider.classify_fields.return_value = {"some_other_key": []}  # Missing 'headers' key

        with pytest.raises(AIProviderError) as exc_info:
            classify_header_fields(mock_provider, sample_payload)

        assert "missing required 'headers' key" in str(exc_info.value).lower()
        assert exc_info.value.provider_name == "test-provider"
        assert exc_info.value.request_type == "classify_fields"

    def test_classify_headers_non_dict_response(self, mock_provider, sample_payload):
        """Test error when response is not a dict."""
        mock_provider.classify_fields.return_value = ["not", "a", "dict"]

        with pytest.raises(AIProviderError) as exc_info:
            classify_header_fields(mock_provider, sample_payload)

        assert "expected dict response" in str(exc_info.value).lower()

    def test_classify_headers_headers_not_list(self, mock_provider, sample_payload):
        """Test error when 'headers' value is not a list."""
        mock_provider.classify_fields.return_value = {"headers": "not a list"}  # Should be a list

        with pytest.raises(AIProviderError) as exc_info:
            classify_header_fields(mock_provider, sample_payload)

        assert "'headers' must be a list" in str(exc_info.value).lower()

    def test_classify_headers_provider_raises_error(self, mock_provider, sample_payload):
        """Test handling when AI provider raises an error."""
        mock_provider.classify_fields.side_effect = AIProviderError(
            provider_name="test-provider",
            error_details="API rate limit exceeded",
            request_type="classify_fields",
        )

        with pytest.raises(AIProviderError) as exc_info:
            classify_header_fields(mock_provider, sample_payload)

        assert "API rate limit exceeded" in str(exc_info.value)

    def test_classify_headers_provider_raises_unexpected_error(self, mock_provider, sample_payload):
        """Test handling when provider raises unexpected error."""
        mock_provider.classify_fields.side_effect = ValueError("Unexpected error")

        with pytest.raises(AIProviderError) as exc_info:
            classify_header_fields(mock_provider, sample_payload)

        assert "Unexpected error" in str(exc_info.value)
        assert exc_info.value.provider_name == "test-provider"


class TestClassifyHeaderFieldsPartialSuccess:
    """Tests for partial success scenarios (some fields parse, some don't)."""

    def test_classify_headers_partial_valid_fields(self, mock_provider, sample_payload):
        """Test partial success when some fields are valid, others invalid."""
        mock_provider.classify_fields.return_value = {
            "headers": [
                # Valid field
                {
                    "raw_label": "Invoice Number",
                    "raw_value": "INV-12345",
                    "block_index": 0,
                    "row_index": 1,
                    "col_index": 1,
                    "model_confidence": 0.95,
                },
                # Invalid field (missing required coordinates)
                {
                    "raw_label": "Date",
                    "raw_value": "2025-01-15",
                    # Missing block_index, row_index, col_index
                },
                # Valid field
                {
                    "raw_label": "Amount",
                    "raw_value": "1000.00",
                    "block_index": 0,
                    "row_index": 3,
                    "col_index": 1,
                    "model_confidence": 0.88,
                },
            ]
        }

        # Should return only the 2 valid fields
        result = classify_header_fields(mock_provider, sample_payload)

        assert len(result) == 2
        assert result[0].raw_label == "Invoice Number"
        assert result[1].raw_label == "Amount"

    def test_classify_headers_invalid_confidence_range(self, mock_provider, sample_payload):
        """Test handling of confidence scores outside valid range."""
        mock_provider.classify_fields.return_value = {
            "headers": [
                {
                    "raw_label": "Invoice Number",
                    "raw_value": "INV-12345",
                    "block_index": 0,
                    "row_index": 1,
                    "col_index": 1,
                    "model_confidence": 1.5,  # Out of range [0.0, 1.0]
                }
            ]
        }

        result = classify_header_fields(mock_provider, sample_payload)

        assert len(result) == 1
        # Invalid confidence should be set to None
        assert result[0].model_confidence is None

    def test_classify_headers_invalid_confidence_type(self, mock_provider, sample_payload):
        """Test handling of non-numeric confidence scores."""
        mock_provider.classify_fields.return_value = {
            "headers": [
                {
                    "raw_label": "Invoice Number",
                    "raw_value": "INV-12345",
                    "block_index": 0,
                    "row_index": 1,
                    "col_index": 1,
                    "model_confidence": "high",  # Invalid type
                }
            ]
        }

        result = classify_header_fields(mock_provider, sample_payload)

        assert len(result) == 1
        assert result[0].model_confidence is None

    def test_classify_headers_negative_coordinates(self, mock_provider, sample_payload):
        """Test that negative coordinates are rejected."""
        mock_provider.classify_fields.return_value = {
            "headers": [
                {
                    "raw_label": "Invoice Number",
                    "raw_value": "INV-12345",
                    "block_index": -1,  # Invalid: negative
                    "row_index": 1,
                    "col_index": 1,
                    "model_confidence": 0.95,
                }
            ]
        }

        result = classify_header_fields(mock_provider, sample_payload)

        # Should skip the invalid field
        assert len(result) == 0

    def test_classify_headers_non_dict_field(self, mock_provider, sample_payload):
        """Test handling when a field is not a dict."""
        mock_provider.classify_fields.return_value = {
            "headers": [
                # Valid field
                {
                    "raw_label": "Invoice Number",
                    "raw_value": "INV-12345",
                    "block_index": 0,
                    "row_index": 1,
                    "col_index": 1,
                },
                # Invalid: not a dict
                "invalid field",
                # Valid field
                {
                    "raw_label": "Date",
                    "raw_value": "2025-01-15",
                    "block_index": 0,
                    "row_index": 2,
                    "col_index": 1,
                },
            ]
        }

        result = classify_header_fields(mock_provider, sample_payload)

        # Should return only the 2 valid fields
        assert len(result) == 2
        assert result[0].raw_label == "Invoice Number"
        assert result[1].raw_label == "Date"

    def test_classify_headers_invalid_metadata_type(self, mock_provider, sample_payload):
        """Test handling when metadata is not a dict."""
        mock_provider.classify_fields.return_value = {
            "headers": [
                {
                    "raw_label": "Invoice Number",
                    "raw_value": "INV-12345",
                    "block_index": 0,
                    "row_index": 1,
                    "col_index": 1,
                    "metadata": "not a dict",  # Invalid type
                }
            ]
        }

        result = classify_header_fields(mock_provider, sample_payload)

        assert len(result) == 1
        # Invalid metadata should be set to None
        assert result[0].metadata is None


class TestClassifyHeaderFieldsEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_classify_headers_large_coordinates(self, mock_provider, sample_payload):
        """Test with very large coordinate values."""
        mock_provider.classify_fields.return_value = {
            "headers": [
                {
                    "raw_label": "Invoice Number",
                    "raw_value": "INV-12345",
                    "block_index": 999,
                    "row_index": 10000,
                    "col_index": 500,
                    "model_confidence": 0.95,
                }
            ]
        }

        result = classify_header_fields(mock_provider, sample_payload)

        assert len(result) == 1
        assert result[0].block_index == 999
        assert result[0].row_index == 10000
        assert result[0].col_index == 500

    def test_classify_headers_zero_coordinates(self, mock_provider, sample_payload):
        """Test with zero coordinate values (valid)."""
        mock_provider.classify_fields.return_value = {
            "headers": [
                {
                    "raw_label": "Invoice Number",
                    "raw_value": "INV-12345",
                    "block_index": 0,
                    "row_index": 0,
                    "col_index": 0,
                    "model_confidence": 0.95,
                }
            ]
        }

        result = classify_header_fields(mock_provider, sample_payload)

        assert len(result) == 1
        assert result[0].block_index == 0
        assert result[0].row_index == 0
        assert result[0].col_index == 0

    def test_classify_headers_boundary_confidence_values(self, mock_provider, sample_payload):
        """Test confidence values at boundaries (0.0 and 1.0)."""
        mock_provider.classify_fields.return_value = {
            "headers": [
                {
                    "raw_label": "Field 1",
                    "raw_value": "Value 1",
                    "block_index": 0,
                    "row_index": 1,
                    "col_index": 1,
                    "model_confidence": 0.0,  # Minimum valid
                },
                {
                    "raw_label": "Field 2",
                    "raw_value": "Value 2",
                    "block_index": 0,
                    "row_index": 2,
                    "col_index": 1,
                    "model_confidence": 1.0,  # Maximum valid
                },
            ]
        }

        result = classify_header_fields(mock_provider, sample_payload)

        assert len(result) == 2
        assert result[0].model_confidence == 0.0
        assert result[1].model_confidence == 1.0

    def test_classify_headers_complex_value_types(self, mock_provider, sample_payload):
        """Test with various value types (numbers, booleans, etc.)."""
        mock_provider.classify_fields.return_value = {
            "headers": [
                {
                    "raw_label": "Numeric Value",
                    "raw_value": 12345,
                    "block_index": 0,
                    "row_index": 1,
                    "col_index": 1,
                },
                {
                    "raw_label": "Boolean Value",
                    "raw_value": True,
                    "block_index": 0,
                    "row_index": 2,
                    "col_index": 1,
                },
                {
                    "raw_label": "None Value",
                    "raw_value": None,
                    "block_index": 0,
                    "row_index": 3,
                    "col_index": 1,
                },
            ]
        }

        result = classify_header_fields(mock_provider, sample_payload)

        assert len(result) == 3
        assert result[0].raw_value == 12345
        assert result[1].raw_value is True
        assert result[2].raw_value is None
