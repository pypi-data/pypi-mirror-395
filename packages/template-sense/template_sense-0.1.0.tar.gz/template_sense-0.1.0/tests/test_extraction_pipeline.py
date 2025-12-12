"""
Unit tests for the extraction pipeline.

This test module validates the end-to-end extraction pipeline orchestration
with mocked AI provider responses. Tests cover happy paths, error scenarios,
and recovery events.
"""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from template_sense.ai.header_classification import ClassifiedHeaderField
from template_sense.ai.table_column_classification import ClassifiedTableColumn
from template_sense.ai_providers.config import AIConfig
from template_sense.errors import (
    AIProviderError,
    FileValidationError,
    InvalidFieldDictionaryError,
)
from template_sense.pipeline.extraction_pipeline import run_extraction_pipeline


@pytest.fixture
def simple_field_dictionary():
    """Simple field dictionary for testing."""
    return {
        "headers": {
            "invoice_number": "Invoice number",
            "due_date": "Due date",
            "shipper_name": "Shipper name",
        },
        "columns": {
            "item_name": "Item name",
            "quantity": "Quantity",
            "unit_price": "Unit price",
            "amount": "Amount",
        },
    }


@pytest.fixture
def mock_ai_provider():
    """Mock AI provider with standard responses."""
    mock_provider = Mock()
    mock_provider.config.provider = "openai"
    mock_provider.config.model = "gpt-4"

    # Mock classify_header_fields response
    mock_provider.classify_fields.return_value = [
        {
            "canonical_key": None,
            "raw_label": "Invoice Number",
            "raw_value": "INV-12345",
            "block_index": 0,
            "row_index": 1,
            "col_index": 1,
            "model_confidence": 0.95,
        },
        {
            "canonical_key": None,
            "raw_label": "Due Date",
            "raw_value": "2024-12-31",
            "block_index": 0,
            "row_index": 2,
            "col_index": 1,
            "model_confidence": 0.90,
        },
    ]

    # Mock classify_columns response
    mock_provider.classify_columns.return_value = [
        {
            "canonical_key": None,
            "raw_label": "Item Name",
            "raw_position": 0,
            "table_block_index": 0,
            "row_index": 5,
            "col_index": 1,
            "sample_values": ["Product A", "Product B"],
            "model_confidence": 0.88,
        },
        {
            "canonical_key": None,
            "raw_label": "Quantity",
            "raw_position": 1,
            "table_block_index": 0,
            "row_index": 5,
            "col_index": 2,
            "sample_values": [10, 20],
            "model_confidence": 0.92,
        },
    ]

    # Mock extract_line_items response
    mock_provider.extract_line_items.return_value = []

    # Mock translate_text response
    mock_provider.translate_text.return_value = {
        "translations": [
            {"original": "Invoice Number", "translated": "Invoice Number", "language": "en"},
            {"original": "Due Date", "translated": "Due Date", "language": "en"},
        ]
    }

    return mock_provider


# ============================================================
# Test 1: Happy Path
# ============================================================


def test_happy_path_with_mocked_ai(simple_field_dictionary, tmp_path):
    """Test successful pipeline execution with mocked AI provider."""
    # Use existing test fixture
    fixture_path = Path("tests/fixtures/simple_invoice.xlsx")

    # Skip if fixture doesn't exist
    if not fixture_path.exists():
        pytest.skip("Test fixture not found")

    # Mock the entire pipeline with minimal AI interactions
    with patch("template_sense.ai_providers.factory.get_ai_provider") as mock_get_provider:
        # Create mock provider
        mock_provider = Mock()
        mock_provider.config.provider = "openai"
        mock_provider.config.model = "gpt-4"

        mock_get_provider.return_value = mock_provider

        # Mock all AI classification functions to return empty lists
        with (
            patch(
                "template_sense.ai.header_classification.classify_header_fields"
            ) as mock_classify_headers,
            patch(
                "template_sense.ai.table_column_classification.classify_table_columns"
            ) as mock_classify_columns,
            patch(
                "template_sense.ai.line_item_extraction.extract_line_items"
            ) as mock_extract_items,
            patch("template_sense.ai.translation.translate_labels") as mock_translate,
        ):
            # Set return values
            mock_classify_headers.return_value = []
            mock_classify_columns.return_value = []
            mock_extract_items.return_value = []
            mock_translate.return_value = []

            # Create explicit AI config to avoid environment variable dependency
            ai_config = AIConfig(
                provider="openai",
                api_key="test-api-key",
                model="gpt-4",
            )

            # Run pipeline
            result = run_extraction_pipeline(
                file_path=fixture_path,
                field_dictionary=simple_field_dictionary,
                ai_config=ai_config,
            )

            # Verify result structure
            assert "normalized_output" in result
            assert "recovery_events" in result
            assert "metadata" in result

            # Verify metadata (only sheet_name after cleanup)
            metadata = result["metadata"]
            assert "sheet_name" in metadata
            # Internal metrics removed: ai_provider, ai_model, pipeline_version, timing_ms
            assert "ai_provider" not in metadata
            assert "ai_model" not in metadata
            assert "pipeline_version" not in metadata
            assert "timing_ms" not in metadata

            # Verify recovery events is a list
            assert isinstance(result["recovery_events"], list)


# ============================================================
# Test 2: File Not Found
# ============================================================


def test_file_not_found(simple_field_dictionary):
    """Test pipeline with nonexistent file."""
    nonexistent_path = Path("tests/fixtures/does_not_exist.xlsx")

    with pytest.raises(FileValidationError) as exc_info:
        run_extraction_pipeline(
            file_path=nonexistent_path,
            field_dictionary=simple_field_dictionary,
        )

    assert "File not found" in str(exc_info.value)


# ============================================================
# Test 3: Invalid File Format
# ============================================================


def test_invalid_file_format(simple_field_dictionary):
    """Test pipeline with invalid file format."""
    # Use existing invalid format fixture
    invalid_path = Path("tests/fixtures/invalid_format.txt")

    # Skip if fixture doesn't exist
    if not invalid_path.exists():
        pytest.skip("Test fixture not found")

    with pytest.raises(FileValidationError) as exc_info:
        run_extraction_pipeline(
            file_path=invalid_path,
            field_dictionary=simple_field_dictionary,
        )

    assert "Unsupported file format" in str(exc_info.value)


# ============================================================
# Test 4: Empty Workbook
# ============================================================


def test_empty_workbook(simple_field_dictionary, tmp_path):
    """Test pipeline with empty workbook."""
    # This test would require creating an empty Excel file
    # For now, we'll skip it as it's complex to set up
    pytest.skip("Empty workbook test requires complex fixture setup")


# ============================================================
# Test 5: AI Provider Failure (Complete)
# ============================================================


@pytest.mark.skip(
    reason="TODO (BAT-58): Update test for stage-based architecture - needs stage-level mocking"
)
def test_ai_provider_complete_failure(simple_field_dictionary):
    """Test pipeline continues when AI provider fails completely."""
    fixture_path = Path("tests/fixtures/simple_invoice.xlsx")

    # Skip if fixture doesn't exist
    if not fixture_path.exists():
        pytest.skip("Test fixture not found")

    with patch("template_sense.ai_providers.factory.get_ai_provider") as mock_get_provider:
        mock_provider = Mock()
        mock_provider.config.provider = "openai"
        mock_provider.config.model = "gpt-4"
        mock_get_provider.return_value = mock_provider

        # Make all AI classification functions raise errors
        with (
            patch(
                "template_sense.ai.header_classification.classify_header_fields"
            ) as mock_classify_headers,
            patch(
                "template_sense.ai.table_column_classification.classify_table_columns"
            ) as mock_classify_columns,
            patch(
                "template_sense.ai.line_item_extraction.extract_line_items"
            ) as mock_extract_items,
            patch("template_sense.ai.translation.translate_labels") as mock_translate,
        ):
            # Raise AIProviderError for all functions
            mock_classify_headers.side_effect = AIProviderError(
                provider_name="openai",
                error_details="API request failed",
            )
            mock_classify_columns.side_effect = AIProviderError(
                provider_name="openai",
                error_details="API request failed",
            )
            mock_extract_items.side_effect = AIProviderError(
                provider_name="openai",
                error_details="API request failed",
            )
            mock_translate.return_value = []

            # Create explicit AI config to avoid environment variable dependency
            ai_config = AIConfig(
                provider="openai",
                api_key="test-api-key",
                model="gpt-4",
            )

            # Pipeline should still complete
            result = run_extraction_pipeline(
                file_path=fixture_path,
                field_dictionary=simple_field_dictionary,
                ai_config=ai_config,
            )

            # Should have recovery events with ERROR severity
            assert len(result["recovery_events"]) > 0

            error_events = [e for e in result["recovery_events"] if e["severity"] == "error"]
            assert len(error_events) > 0

            # Should still return valid structure
            assert "normalized_output" in result
            assert "metadata" in result


# ============================================================
# Test 6: Partial AI Response (Low Confidence)
# ============================================================


@pytest.mark.skip(
    reason="TODO (BAT-58): Update test for stage-based architecture - needs stage-level mocking"
)
def test_partial_ai_response_low_confidence(simple_field_dictionary):
    """Test pipeline with low confidence AI results."""
    fixture_path = Path("tests/fixtures/simple_invoice.xlsx")

    # Skip if fixture doesn't exist
    if not fixture_path.exists():
        pytest.skip("Test fixture not found")

    with patch("template_sense.ai_providers.factory.get_ai_provider") as mock_get_provider:
        mock_provider = Mock()
        mock_provider.config.provider = "openai"
        mock_provider.config.model = "gpt-4"
        mock_get_provider.return_value = mock_provider

        with (
            patch(
                "template_sense.ai.header_classification.classify_header_fields"
            ) as mock_classify_headers,
            patch(
                "template_sense.ai.table_column_classification.classify_table_columns"
            ) as mock_classify_columns,
            patch(
                "template_sense.ai.line_item_extraction.extract_line_items"
            ) as mock_extract_items,
            patch("template_sense.ai.translation.translate_labels") as mock_translate,
        ):
            # Return low confidence results
            mock_classify_headers.return_value = [
                ClassifiedHeaderField(
                    canonical_key=None,
                    raw_label="Invoice Number",
                    raw_value="INV-12345",
                    block_index=0,
                    row_index=1,
                    col_index=1,
                    model_confidence=0.3,  # Low confidence
                )
            ]

            mock_classify_columns.return_value = [
                ClassifiedTableColumn(
                    canonical_key=None,
                    raw_label="Item Name",
                    raw_position=0,
                    table_block_index=0,
                    row_index=5,
                    col_index=1,
                    sample_values=["Product A"],
                    model_confidence=0.4,  # Low confidence
                )
            ]

            mock_extract_items.return_value = []
            mock_translate.return_value = []

            # Create explicit AI config to avoid environment variable dependency
            ai_config = AIConfig(
                provider="openai",
                api_key="test-api-key",
                model="gpt-4",
            )

            # Run pipeline
            result = run_extraction_pipeline(
                file_path=fixture_path,
                field_dictionary=simple_field_dictionary,
                ai_config=ai_config,
            )

            # Should have warning events for low confidence
            warning_events = [e for e in result["recovery_events"] if e["severity"] == "warning"]
            assert len(warning_events) > 0

            # Fields should still be included in output
            assert "normalized_output" in result


# ============================================================
# Test 7: Metadata Validation
# ============================================================


def test_metadata_validation(simple_field_dictionary):
    """Test that metadata contains all required fields."""
    fixture_path = Path("tests/fixtures/simple_invoice.xlsx")

    # Skip if fixture doesn't exist
    if not fixture_path.exists():
        pytest.skip("Test fixture not found")

    with patch("template_sense.ai_providers.factory.get_ai_provider") as mock_get_provider:
        mock_provider = Mock()
        mock_provider.config.provider = "anthropic"
        mock_provider.config.model = "claude-3-sonnet"
        mock_get_provider.return_value = mock_provider

        with (
            patch(
                "template_sense.ai.header_classification.classify_header_fields",
                return_value=[],
            ),
            patch(
                "template_sense.ai.table_column_classification.classify_table_columns",
                return_value=[],
            ),
            patch(
                "template_sense.ai.line_item_extraction.extract_line_items",
                return_value=[],
            ),
            patch(
                "template_sense.ai.translation.translate_labels",
                return_value=[],
            ),
        ):
            # Create explicit AI config to avoid environment variable dependency
            ai_config = AIConfig(
                provider="anthropic",
                api_key="test-api-key",
                model="claude-3-sonnet",
            )

            result = run_extraction_pipeline(
                file_path=fixture_path,
                field_dictionary=simple_field_dictionary,
                ai_config=ai_config,
            )

            # Verify metadata structure (only sheet_name after cleanup)
            metadata = result["metadata"]
            assert "sheet_name" in metadata
            # Internal metrics removed: ai_provider, ai_model, pipeline_version, timing_ms
            assert "ai_provider" not in metadata
            assert "ai_model" not in metadata
            assert "pipeline_version" not in metadata
            assert "timing_ms" not in metadata

            # Verify sheet_name has a value
            assert isinstance(metadata["sheet_name"], str)
            assert len(metadata["sheet_name"]) > 0


# ============================================================
# Test 8: Invalid Field Dictionary
# ============================================================


def test_invalid_field_dictionary_not_dict():
    """Test pipeline with field dictionary that's not a dict."""
    fixture_path = Path("tests/fixtures/simple_invoice.xlsx")

    with pytest.raises(InvalidFieldDictionaryError):
        run_extraction_pipeline(
            file_path=fixture_path,
            field_dictionary="not a dict",  # type: ignore
        )


def test_invalid_field_dictionary_empty():
    """Test pipeline with empty field dictionary."""
    fixture_path = Path("tests/fixtures/simple_invoice.xlsx")

    with pytest.raises(InvalidFieldDictionaryError):
        run_extraction_pipeline(
            file_path=fixture_path,
            field_dictionary={},
        )


def test_invalid_field_dictionary_wrong_value_type():
    """Test pipeline with field dictionary with wrong value type."""
    fixture_path = Path("tests/fixtures/simple_invoice.xlsx")

    with pytest.raises(InvalidFieldDictionaryError):
        run_extraction_pipeline(
            file_path=fixture_path,
            field_dictionary={"invoice_number": "not a list"},  # type: ignore
        )


def test_invalid_field_dictionary_empty_list():
    """Test pipeline with field dictionary with empty list values."""
    fixture_path = Path("tests/fixtures/simple_invoice.xlsx")

    with pytest.raises(InvalidFieldDictionaryError):
        run_extraction_pipeline(
            file_path=fixture_path,
            field_dictionary={"invoice_number": []},
        )
