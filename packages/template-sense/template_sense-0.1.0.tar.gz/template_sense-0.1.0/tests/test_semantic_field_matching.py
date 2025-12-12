"""
Unit tests for semantic field matching module.

These tests use mocked AI responses to avoid dependencies on:
- Actual AI provider API calls
- Test files like CO.xlsx that won't be committed

CO.xlsx validation should be done via E2E tests or manual testing.
"""

import json
from unittest.mock import Mock

import pytest

from template_sense.ai_providers.interface import AIProvider
from template_sense.errors import AIProviderError
from template_sense.mapping.semantic_field_matching import (
    SemanticMatchResult,
    _build_semantic_matching_prompt,
    semantic_match_field,
    semantic_match_fields_batch,
)

# ============================================================
# Fixtures
# ============================================================


@pytest.fixture
def mock_ai_provider():
    """Create a mock AI provider for testing."""
    provider = Mock(spec=AIProvider)
    provider.provider_name = "openai"
    provider.model = "gpt-4"

    # Mock the generate_text method (provider-agnostic interface)
    provider.generate_text = Mock()

    return provider


@pytest.fixture
def sample_field_dictionary():
    """Sample canonical field dictionary for testing."""
    return {
        "invoice_number": ["Invoice Number", "Invoice No", "Inv #", "請求書番号"],
        "shipper": ["Shipper", "Sender", "From", "Consignor", "荷送人"],
        "consignee": ["Consignee", "Receiver", "To", "Recipient", "荷受人"],
        "etd": ["ETD", "Estimated Time of Departure", "Departure Date"],
        "product_name": ["Product Name", "Item Name", "Description", "商品名"],
        "item_number": ["Item Number", "Item No", "Item #", "SKU"],
    }


# ============================================================
# Test: Prompt Building
# ============================================================


def test_build_semantic_matching_prompt(sample_field_dictionary):
    """Test that prompt is correctly formatted with field dictionary."""
    prompt = _build_semantic_matching_prompt(
        translated_label="FROM",
        field_dictionary=sample_field_dictionary,
        best_fuzzy_score=33.3,
    )

    # Check key sections are present
    assert "FROM" in prompt
    assert "33.3%" in prompt
    assert "shipper" in prompt
    assert "consignee" in prompt
    assert "Determine if the label is semantically equivalent" in prompt
    assert "JSON only" in prompt


# ============================================================
# Test: Semantic Matching for Headers (High Confidence)
# ============================================================


def test_semantic_match_from_to_shipper(mock_ai_provider, sample_field_dictionary):
    """Test: FROM → shipper with high AI confidence (≥0.9)."""
    # Mock AI response content
    mock_response_json = json.dumps(
        {
            "canonical_key": "shipper",
            "confidence": 0.95,
            "reasoning": "'FROM' indicates sender/shipper in logistics context",
        }
    )
    mock_ai_provider.generate_text.return_value = mock_response_json

    result = semantic_match_field(
        translated_label="FROM",
        field_dictionary=sample_field_dictionary,
        ai_provider=mock_ai_provider,
        best_fuzzy_score=33.3,
        confidence_threshold=0.7,
    )

    # Assertions
    assert result.canonical_key == "shipper"
    assert result.semantic_confidence == 0.95
    assert result.reasoning == "'FROM' indicates sender/shipper in logistics context"
    assert result.translated_text == "FROM"
    assert result.fuzzy_fallback_score == 33.3


def test_semantic_match_to_to_consignee(mock_ai_provider, sample_field_dictionary):
    """Test: TO → consignee with high AI confidence (≥0.9)."""
    mock_response = json.dumps(
        {
            "canonical_key": "consignee",
            "confidence": 0.93,
            "reasoning": "'TO' indicates receiver/consignee in logistics context",
        }
    )
    mock_ai_provider.generate_text.return_value = mock_response

    result = semantic_match_field(
        translated_label="TO",
        field_dictionary=sample_field_dictionary,
        ai_provider=mock_ai_provider,
        best_fuzzy_score=40.0,
        confidence_threshold=0.7,
    )

    assert result.canonical_key == "consignee"
    assert result.semantic_confidence == 0.93
    assert result.fuzzy_fallback_score == 40.0


def test_semantic_match_shipment_day_to_etd(mock_ai_provider, sample_field_dictionary):
    """Test: SHIPMENT DAY → etd with good AI confidence (≥0.8)."""
    mock_response = json.dumps(
        {
            "canonical_key": "etd",
            "confidence": 0.85,
            "reasoning": "Shipment day represents departure date (ETD)",
        }
    )
    mock_ai_provider.generate_text.return_value = mock_response

    result = semantic_match_field(
        translated_label="SHIPMENT DAY",
        field_dictionary=sample_field_dictionary,
        ai_provider=mock_ai_provider,
        best_fuzzy_score=52.6,
        confidence_threshold=0.7,
    )

    assert result.canonical_key == "etd"
    assert result.semantic_confidence == 0.85
    assert result.fuzzy_fallback_score == 52.6


# ============================================================
# Test: Semantic Matching for Columns
# ============================================================


def test_semantic_match_items_to_product_name(mock_ai_provider, sample_field_dictionary):
    """Test: Items → product_name (column field)."""
    mock_response = json.dumps(
        {
            "canonical_key": "product_name",
            "confidence": 0.88,
            "reasoning": "'Items' refers to product/item descriptions in invoice tables",
        }
    )
    mock_ai_provider.generate_text.return_value = mock_response

    result = semantic_match_field(
        translated_label="Items",
        field_dictionary=sample_field_dictionary,
        ai_provider=mock_ai_provider,
        best_fuzzy_score=45.0,
        confidence_threshold=0.7,
    )

    assert result.canonical_key == "product_name"
    assert result.semantic_confidence == 0.88


def test_semantic_match_item_no_to_item_number(mock_ai_provider, sample_field_dictionary):
    """Test: Item/NO → item_number (column field with slash)."""
    mock_response = json.dumps(
        {
            "canonical_key": "item_number",
            "confidence": 0.91,
            "reasoning": "'Item/NO' is a common abbreviation for item number",
        }
    )
    mock_ai_provider.generate_text.return_value = mock_response

    result = semantic_match_field(
        translated_label="Item/NO",
        field_dictionary=sample_field_dictionary,
        ai_provider=mock_ai_provider,
        best_fuzzy_score=55.0,
        confidence_threshold=0.7,
    )

    assert result.canonical_key == "item_number"
    assert result.semantic_confidence == 0.91


# ============================================================
# Test: Threshold Behavior
# ============================================================


def test_semantic_match_below_threshold_rejected(mock_ai_provider, sample_field_dictionary):
    """Test: Low AI confidence (<0.7) is rejected."""
    mock_response = json.dumps(
        {
            "canonical_key": "shipper",
            "confidence": 0.65,  # Below threshold
            "reasoning": "Possible but uncertain match",
        }
    )
    mock_ai_provider.generate_text.return_value = mock_response

    result = semantic_match_field(
        translated_label="SENDER",
        field_dictionary=sample_field_dictionary,
        ai_provider=mock_ai_provider,
        best_fuzzy_score=45.0,
        confidence_threshold=0.7,
    )

    # Should return None for canonical_key when below threshold
    assert result.canonical_key is None
    assert result.semantic_confidence == 0.65


def test_semantic_match_no_match_response(mock_ai_provider, sample_field_dictionary):
    """Test: AI returns null for no semantic match."""
    mock_response = json.dumps(
        {
            "canonical_key": None,
            "confidence": 0.0,
            "reasoning": "No semantic equivalence found",
        }
    )
    mock_ai_provider.generate_text.return_value = mock_response

    result = semantic_match_field(
        translated_label="RANDOM_FIELD",
        field_dictionary=sample_field_dictionary,
        ai_provider=mock_ai_provider,
        best_fuzzy_score=35.0,
        confidence_threshold=0.7,
    )

    assert result.canonical_key is None
    assert result.semantic_confidence == 0.0


# ============================================================
# Test: Response Parsing
# ============================================================


def test_semantic_match_handles_markdown_code_blocks(mock_ai_provider, sample_field_dictionary):
    """Test: Correctly parses AI response wrapped in markdown code blocks."""
    mock_response = """```json
{
  "canonical_key": "shipper",
  "confidence": 0.92,
  "reasoning": "FROM indicates shipper"
}
```"""
    mock_ai_provider.generate_text.return_value = mock_response

    result = semantic_match_field(
        translated_label="FROM",
        field_dictionary=sample_field_dictionary,
        ai_provider=mock_ai_provider,
        best_fuzzy_score=33.3,
        confidence_threshold=0.7,
    )

    assert result.canonical_key == "shipper"
    assert result.semantic_confidence == 0.92


def test_semantic_match_handles_plain_code_blocks(mock_ai_provider, sample_field_dictionary):
    """Test: Correctly parses AI response with plain ``` blocks."""
    mock_response = """```
{
  "canonical_key": "consignee",
  "confidence": 0.90,
  "reasoning": "TO indicates consignee"
}
```"""
    mock_ai_provider.generate_text.return_value = mock_response

    result = semantic_match_field(
        translated_label="TO",
        field_dictionary=sample_field_dictionary,
        ai_provider=mock_ai_provider,
        best_fuzzy_score=40.0,
        confidence_threshold=0.7,
    )

    assert result.canonical_key == "consignee"
    assert result.semantic_confidence == 0.90


def test_semantic_match_handles_invalid_json(mock_ai_provider, sample_field_dictionary):
    """Test: Gracefully handles invalid JSON response."""
    mock_response = "This is not valid JSON"
    mock_ai_provider.generate_text.return_value = mock_response

    result = semantic_match_field(
        translated_label="FROM",
        field_dictionary=sample_field_dictionary,
        ai_provider=mock_ai_provider,
        best_fuzzy_score=33.3,
        confidence_threshold=0.7,
    )

    # Should return no match with error reasoning
    assert result.canonical_key is None
    assert result.semantic_confidence == 0.0
    assert "Failed to parse AI response" in result.reasoning


# ============================================================
# Test: Error Handling
# ============================================================


def test_semantic_match_handles_ai_provider_error(mock_ai_provider, sample_field_dictionary):
    """Test: Gracefully handles AIProviderError."""
    # Make the generate_text call raise an error
    mock_ai_provider.generate_text.side_effect = AIProviderError(
        provider_name="openai",
        error_details="API rate limit exceeded",
    )

    result = semantic_match_field(
        translated_label="FROM",
        field_dictionary=sample_field_dictionary,
        ai_provider=mock_ai_provider,
        best_fuzzy_score=33.3,
        confidence_threshold=0.7,
    )

    # Should return no match with error reasoning
    assert result.canonical_key is None
    assert result.semantic_confidence == 0.0
    assert "API call failed" in result.reasoning


def test_semantic_match_handles_unexpected_error(mock_ai_provider, sample_field_dictionary):
    """Test: Gracefully handles unexpected exceptions."""
    mock_ai_provider.classify_fields.side_effect = RuntimeError("Unexpected error")

    result = semantic_match_field(
        translated_label="FROM",
        field_dictionary=sample_field_dictionary,
        ai_provider=mock_ai_provider,
        best_fuzzy_score=33.3,
        confidence_threshold=0.7,
    )

    assert result.canonical_key is None
    assert result.semantic_confidence == 0.0
    assert "Unexpected error" in result.reasoning


# ============================================================
# Test: Batch Processing
# ============================================================


def test_batch_semantic_matching(mock_ai_provider, sample_field_dictionary):
    """Test: Batch process multiple unmatched fields."""
    # Mock AI responses for each call using side_effect
    responses = [
        json.dumps({"canonical_key": "shipper", "confidence": 0.95, "reasoning": "FROM = shipper"}),
        json.dumps(
            {"canonical_key": "consignee", "confidence": 0.93, "reasoning": "TO = consignee"}
        ),
        json.dumps({"canonical_key": "etd", "confidence": 0.85, "reasoning": "SHIPMENT DAY = ETD"}),
    ]
    mock_ai_provider.generate_text.side_effect = responses

    unmatched = [
        ("FROM", 33.3),
        ("TO", 40.0),
        ("SHIPMENT DAY", 52.6),
    ]

    results = semantic_match_fields_batch(
        unmatched_labels=unmatched,
        field_dictionary=sample_field_dictionary,
        ai_provider=mock_ai_provider,
        confidence_threshold=0.7,
    )

    assert len(results) == 3
    assert results[0].canonical_key == "shipper"
    assert results[1].canonical_key == "consignee"
    assert results[2].canonical_key == "etd"


def test_batch_semantic_matching_partial_matches(mock_ai_provider, sample_field_dictionary):
    """Test: Batch processing with some matches and some failures."""
    responses = [
        json.dumps({"canonical_key": "shipper", "confidence": 0.95, "reasoning": "FROM = shipper"}),
        json.dumps({"canonical_key": None, "confidence": 0.0, "reasoning": "No match"}),
    ]
    mock_ai_provider.generate_text.side_effect = responses

    unmatched = [
        ("FROM", 33.3),
        ("UNKNOWN", 35.0),
    ]

    results = semantic_match_fields_batch(
        unmatched_labels=unmatched,
        field_dictionary=sample_field_dictionary,
        ai_provider=mock_ai_provider,
        confidence_threshold=0.7,
    )

    assert len(results) == 2
    assert results[0].canonical_key == "shipper"
    assert results[1].canonical_key is None


# ============================================================
# Test: Integration with Feature Flags (Constants)
# ============================================================


def test_semantic_matching_uses_constants_defaults():
    """Test: Verify default values from constants are used correctly."""
    from template_sense.constants import (
        SEMANTIC_MATCHING_CONFIDENCE_THRESHOLD,
        SEMANTIC_MATCHING_TIMEOUT_SECONDS,
    )

    # Verify constants exist and have expected values
    assert SEMANTIC_MATCHING_CONFIDENCE_THRESHOLD == 0.7
    assert SEMANTIC_MATCHING_TIMEOUT_SECONDS == 10


# ============================================================
# Test: Dataclass Structure
# ============================================================


def test_semantic_match_result_dataclass():
    """Test: SemanticMatchResult dataclass structure."""
    result = SemanticMatchResult(
        original_text="FROM",
        translated_text="FROM",
        canonical_key="shipper",
        semantic_confidence=0.95,
        reasoning="FROM indicates shipper",
        fuzzy_fallback_score=33.3,
    )

    assert result.original_text == "FROM"
    assert result.translated_text == "FROM"
    assert result.canonical_key == "shipper"
    assert result.semantic_confidence == 0.95
    assert result.reasoning == "FROM indicates shipper"
    assert result.fuzzy_fallback_score == 33.3
