"""
Unit tests for analyzer.py - Public API entry point.

Tests the extract_template_structure() function with mocked pipeline.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from template_sense.ai_providers.config import AIConfig
from template_sense.analyzer import extract_template_structure
from template_sense.errors import (
    AIProviderError,
    ExtractionError,
    FileValidationError,
    InvalidFieldDictionaryError,
    UnsupportedFileTypeError,
)

# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def valid_field_dictionary() -> dict[str, dict[str, str]]:
    """Sample Tako canonical field dictionary."""
    return {
        "headers": {
            "invoice_number": "Invoice number",
            "shipper_name": "Shipper",
            "invoice_date": "Invoice date",
            "total_amount": "Total amount",
        },
        "columns": {
            "product_name": "Product name",
            "quantity": "Quantity",
            "price": "Price",
        },
    }


@pytest.fixture
def mock_pipeline_output() -> dict:
    """Sample pipeline output structure."""
    return {
        "normalized_output": {
            "header_fields": [
                {
                    "canonical_key": "invoice_number",
                    "detected_label": "Invoice No",
                    "cell_value": "INV-12345",
                    "location": {"row": 2, "column": 1},
                    "confidence": 0.95,
                    "fuzzy_match_score": 100.0,
                }
            ],
            "table_columns": [
                {
                    "canonical_key": "item_description",
                    "detected_label": "Description",
                    "column_index": 0,
                    "confidence": 0.92,
                    "fuzzy_match_score": 95.0,
                }
            ],
            "line_items": [],
        },
        "recovery_events": [
            {
                "severity": "warning",
                "stage": "fuzzy_matching",
                "message": "Low fuzzy match score for field 'Total Amount'",
                "field_identifier": "total_amount",
                "confidence_score": 75.0,
                "metadata": {"original_score": 75.0},
            }
        ],
        "metadata": {
            "sheet_name": "Invoice",
            "ai_provider": "openai",
            "ai_model": "gpt-4",
            "pipeline_version": "1.0",
            "timing_ms": 1234,
        },
    }


@pytest.fixture
def mock_ai_config() -> AIConfig:
    """Sample AIConfig object."""
    return AIConfig(provider="openai", model="gpt-4", api_key="test-key")


# ============================================================================
# Test Category 1: Valid Inputs
# ============================================================================


@patch("template_sense.analyzer.run_extraction_pipeline")
def test_extract_with_string_path(
    mock_pipeline: MagicMock,
    valid_field_dictionary: dict,
    mock_pipeline_output: dict,
) -> None:
    """Test extraction with string file path."""
    # Setup
    mock_pipeline.return_value = mock_pipeline_output
    file_path = "test_invoice.xlsx"

    # Execute
    result = extract_template_structure(file_path, valid_field_dictionary)

    # Verify
    assert result == mock_pipeline_output
    assert "normalized_output" in result
    assert "recovery_events" in result
    assert "metadata" in result

    # Verify pipeline was called with Path object
    mock_pipeline.assert_called_once()
    call_args = mock_pipeline.call_args
    assert isinstance(call_args[1]["file_path"], Path)
    assert call_args[1]["field_dictionary"] == valid_field_dictionary
    assert call_args[1]["ai_config"] is None


@patch("template_sense.analyzer.run_extraction_pipeline")
def test_extract_with_path_object(
    mock_pipeline: MagicMock,
    valid_field_dictionary: dict,
    mock_pipeline_output: dict,
) -> None:
    """Test extraction with Path object input."""
    # Setup
    mock_pipeline.return_value = mock_pipeline_output
    file_path = Path("test_invoice.xlsx")

    # Execute
    result = extract_template_structure(file_path, valid_field_dictionary)

    # Verify
    assert result == mock_pipeline_output
    mock_pipeline.assert_called_once()
    call_args = mock_pipeline.call_args
    assert call_args[1]["file_path"] == file_path


@patch("template_sense.analyzer.run_extraction_pipeline")
def test_extract_with_custom_ai_config(
    mock_pipeline: MagicMock,
    valid_field_dictionary: dict,
    mock_pipeline_output: dict,
    mock_ai_config: AIConfig,
) -> None:
    """Test extraction with custom AIConfig."""
    # Setup
    mock_pipeline.return_value = mock_pipeline_output
    file_path = "test_invoice.xlsx"

    # Execute
    result = extract_template_structure(file_path, valid_field_dictionary, ai_config=mock_ai_config)

    # Verify
    assert result == mock_pipeline_output
    mock_pipeline.assert_called_once()
    call_args = mock_pipeline.call_args
    assert call_args[1]["ai_config"] == mock_ai_config


@patch("template_sense.analyzer.run_extraction_pipeline")
def test_extract_verifies_return_structure(
    mock_pipeline: MagicMock,
    valid_field_dictionary: dict,
    mock_pipeline_output: dict,
) -> None:
    """Test that return structure contains all required keys."""
    # Setup
    mock_pipeline.return_value = mock_pipeline_output

    # Execute
    result = extract_template_structure("test.xlsx", valid_field_dictionary)

    # Verify structure
    assert "normalized_output" in result
    assert "recovery_events" in result
    assert "metadata" in result

    # Verify normalized_output structure
    assert "header_fields" in result["normalized_output"]
    assert "table_columns" in result["normalized_output"]
    assert "line_items" in result["normalized_output"]

    # Verify metadata structure
    assert "sheet_name" in result["metadata"]
    assert "ai_provider" in result["metadata"]
    assert "ai_model" in result["metadata"]
    assert "pipeline_version" in result["metadata"]
    assert "timing_ms" in result["metadata"]


# ============================================================================
# Test Category 2: Input Validation
# ============================================================================


@patch("template_sense.analyzer.run_extraction_pipeline")
def test_extract_nonexistent_file_raises_error(
    mock_pipeline: MagicMock,
    valid_field_dictionary: dict,
) -> None:
    """Test that non-existent file raises FileValidationError."""
    # Setup
    mock_pipeline.side_effect = FileValidationError(
        reason="File not found",
        file_path="nonexistent.xlsx",
    )

    # Execute & Verify
    with pytest.raises(FileValidationError) as exc_info:
        extract_template_structure("nonexistent.xlsx", valid_field_dictionary)

    assert "File not found" in str(exc_info.value)


@patch("template_sense.analyzer.run_extraction_pipeline")
def test_extract_invalid_extension_raises_error(
    mock_pipeline: MagicMock,
    valid_field_dictionary: dict,
) -> None:
    """Test that invalid file extension raises UnsupportedFileTypeError."""
    # Setup
    mock_pipeline.side_effect = UnsupportedFileTypeError(
        file_extension=".csv",
        supported_types=[".xlsx", ".xls"],
    )

    # Execute & Verify
    with pytest.raises(UnsupportedFileTypeError) as exc_info:
        extract_template_structure("test.csv", valid_field_dictionary)

    assert ".csv" in str(exc_info.value)


@patch("template_sense.analyzer.run_extraction_pipeline")
def test_extract_empty_path_raises_error(
    mock_pipeline: MagicMock,
    valid_field_dictionary: dict,
) -> None:
    """Test that empty file path raises FileValidationError."""
    # Setup
    mock_pipeline.side_effect = FileValidationError(
        reason="File path is empty",
        file_path="",
    )

    # Execute & Verify
    with pytest.raises(FileValidationError) as exc_info:
        extract_template_structure("", valid_field_dictionary)

    assert "File path is empty" in str(exc_info.value)


@patch("template_sense.analyzer.run_extraction_pipeline")
def test_extract_invalid_field_dict_not_dict_raises_error(
    mock_pipeline: MagicMock,
) -> None:
    """Test that invalid field dictionary (not a dict) raises error."""
    # Setup
    mock_pipeline.side_effect = InvalidFieldDictionaryError(
        reason="Field dictionary must be a dict",
        field_dictionary="not_a_dict",
    )

    # Execute & Verify
    with pytest.raises(InvalidFieldDictionaryError) as exc_info:
        extract_template_structure("test.xlsx", "not_a_dict")  # type: ignore

    assert "must be a dict" in str(exc_info.value)


@patch("template_sense.analyzer.run_extraction_pipeline")
def test_extract_invalid_field_dict_empty_raises_error(
    mock_pipeline: MagicMock,
) -> None:
    """Test that empty field dictionary raises error."""
    # Setup
    mock_pipeline.side_effect = InvalidFieldDictionaryError(
        reason="Field dictionary cannot be empty",
        field_dictionary={},
    )

    # Execute & Verify
    with pytest.raises(InvalidFieldDictionaryError) as exc_info:
        extract_template_structure("test.xlsx", {})

    assert "cannot be empty" in str(exc_info.value)


# ============================================================================
# Test Category 3: Error Handling
# ============================================================================


@patch("template_sense.analyzer.run_extraction_pipeline")
def test_extract_reraises_file_validation_error(
    mock_pipeline: MagicMock,
    valid_field_dictionary: dict,
) -> None:
    """Test that FileValidationError is re-raised unchanged."""
    # Setup
    original_error = FileValidationError(
        reason="Cannot read file",
        file_path="corrupt.xlsx",
    )
    mock_pipeline.side_effect = original_error

    # Execute & Verify
    with pytest.raises(FileValidationError) as exc_info:
        extract_template_structure("corrupt.xlsx", valid_field_dictionary)

    # Verify it's the same error object
    assert exc_info.value is original_error


@patch("template_sense.analyzer.run_extraction_pipeline")
def test_extract_reraises_extraction_error(
    mock_pipeline: MagicMock,
    valid_field_dictionary: dict,
) -> None:
    """Test that ExtractionError is re-raised unchanged."""
    # Setup
    original_error = ExtractionError(
        extraction_type="sheet_selection",
        reason="No visible sheets found",
    )
    mock_pipeline.side_effect = original_error

    # Execute & Verify
    with pytest.raises(ExtractionError) as exc_info:
        extract_template_structure("test.xlsx", valid_field_dictionary)

    # Verify it's the same error object
    assert exc_info.value is original_error


@patch("template_sense.analyzer.run_extraction_pipeline")
def test_extract_reraises_ai_provider_error(
    mock_pipeline: MagicMock,
    valid_field_dictionary: dict,
) -> None:
    """Test that AIProviderError is re-raised unchanged."""
    # Setup
    original_error = AIProviderError(
        provider_name="openai",
        error_details="API key invalid",
        request_type="classify_fields",
    )
    mock_pipeline.side_effect = original_error

    # Execute & Verify
    with pytest.raises(AIProviderError) as exc_info:
        extract_template_structure("test.xlsx", valid_field_dictionary)

    # Verify it's the same error object
    assert exc_info.value is original_error


@patch("template_sense.analyzer.run_extraction_pipeline")
def test_extract_wraps_unexpected_exception(
    mock_pipeline: MagicMock,
    valid_field_dictionary: dict,
) -> None:
    """Test that unexpected exceptions are wrapped in ExtractionError."""
    # Setup
    unexpected_error = RuntimeError("Unexpected internal error")
    mock_pipeline.side_effect = unexpected_error

    # Execute & Verify
    with pytest.raises(ExtractionError) as exc_info:
        extract_template_structure("test.xlsx", valid_field_dictionary)

    # Verify it's wrapped
    assert "Unexpected error during template analysis" in str(exc_info.value)
    assert exc_info.value.__cause__ is unexpected_error


# ============================================================================
# Test Category 4: Integration Behavior
# ============================================================================


@patch("template_sense.analyzer.run_extraction_pipeline")
def test_extract_calls_pipeline_with_correct_arguments(
    mock_pipeline: MagicMock,
    valid_field_dictionary: dict,
    mock_pipeline_output: dict,
    mock_ai_config: AIConfig,
) -> None:
    """Test that pipeline is called with correct arguments."""
    # Setup
    mock_pipeline.return_value = mock_pipeline_output
    file_path = "test_invoice.xlsx"

    # Execute
    extract_template_structure(file_path, valid_field_dictionary, ai_config=mock_ai_config)

    # Verify
    mock_pipeline.assert_called_once()
    call_args = mock_pipeline.call_args

    # Check keyword arguments
    assert "file_path" in call_args[1]
    assert "field_dictionary" in call_args[1]
    assert "ai_config" in call_args[1]

    # Check values
    assert isinstance(call_args[1]["file_path"], Path)
    assert str(call_args[1]["file_path"]) == file_path
    assert call_args[1]["field_dictionary"] == valid_field_dictionary
    assert call_args[1]["ai_config"] == mock_ai_config


@patch("template_sense.analyzer.run_extraction_pipeline")
def test_extract_returns_pipeline_output_unchanged(
    mock_pipeline: MagicMock,
    valid_field_dictionary: dict,
    mock_pipeline_output: dict,
) -> None:
    """Test that pipeline output is returned unchanged."""
    # Setup
    mock_pipeline.return_value = mock_pipeline_output

    # Execute
    result = extract_template_structure("test.xlsx", valid_field_dictionary)

    # Verify - should be exact same object
    assert result is mock_pipeline_output
    assert result == mock_pipeline_output
