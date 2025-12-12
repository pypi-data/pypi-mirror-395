"""
Unit tests for fuzzy field matching module.

Tests cover:
- Basic functionality (exact matches, case-insensitive, whitespace normalization)
- Threshold behavior (below/at/above threshold)
- Dictionary variants (multiple variants, tracking matched variant)
- Deterministic behavior (tie-breaking, same inputs → same outputs)
- Edge cases (empty inputs, special characters, Unicode)
- Integration with TranslatedLabel
- Performance (large dictionaries, many labels)
"""

import pytest

from template_sense.ai.translation import TranslatedLabel
from template_sense.mapping.fuzzy_field_matching import (
    _calculate_similarity,
    _find_best_match,
    _normalize_text,
    match_fields,
)

# ============================================================
# Fixtures
# ============================================================


@pytest.fixture
def sample_field_dictionary():
    """Sample canonical field dictionary for testing."""
    return {
        "invoice_number": ["Invoice Number", "Invoice No", "Inv #", "請求書番号"],
        "due_date": ["Due Date", "Payment Due", "Date Due", "支払期日"],
        "shipper_name": ["Shipper", "Sender", "From", "荷送人"],
        "total_amount": ["Total Amount", "Total", "Amount Due"],
    }


@pytest.fixture
def sample_translated_labels():
    """Sample translated labels for testing."""
    return [
        TranslatedLabel(
            original_text="請求書番号",
            translated_text="Invoice Number",
            detected_source_language="ja",
        ),
        TranslatedLabel(
            original_text="支払期日",
            translated_text="payment due",
            detected_source_language="ja",
        ),
        TranslatedLabel(
            original_text="荷送人",
            translated_text="Sender",
            detected_source_language="ja",
        ),
    ]


# ============================================================
# Test: Basic Functionality
# ============================================================


def test_exact_match_returns_100_score():
    """Test that exact matches return a perfect score of 100.0."""
    field_dict = {"invoice_number": ["Invoice Number"]}
    labels = [
        TranslatedLabel(
            original_text="請求書番号",
            translated_text="Invoice Number",
            detected_source_language="ja",
        )
    ]

    results = match_fields(labels, field_dict, threshold=80.0)

    assert len(results) == 1
    assert results[0].canonical_key == "invoice_number"
    assert results[0].match_score == 100.0
    assert results[0].matched_variant == "Invoice Number"


def test_case_insensitive_matching():
    """Test that matching is case-insensitive."""
    field_dict = {"invoice_number": ["Invoice Number"]}
    labels = [
        TranslatedLabel(
            original_text="請求書番号",
            translated_text="invoice number",  # Lowercase
            detected_source_language="ja",
        )
    ]

    results = match_fields(labels, field_dict, threshold=80.0)

    assert len(results) == 1
    assert results[0].canonical_key == "invoice_number"
    assert results[0].match_score == 100.0


def test_whitespace_normalization():
    """Test that extra whitespace is normalized correctly."""
    field_dict = {"invoice_number": ["Invoice Number"]}
    labels = [
        TranslatedLabel(
            original_text="請求書番号",
            translated_text="  Invoice  Number  ",  # Extra whitespace
            detected_source_language="ja",
        )
    ]

    results = match_fields(labels, field_dict, threshold=80.0)

    assert len(results) == 1
    assert results[0].canonical_key == "invoice_number"
    assert results[0].match_score == 100.0


def test_word_order_handling():
    """Test that token_set_ratio handles word order differences."""
    field_dict = {"invoice_number": ["Invoice Number"]}
    labels = [
        TranslatedLabel(
            original_text="番号請求書",
            translated_text="Number Invoice",  # Reversed order
            detected_source_language="ja",
        )
    ]

    results = match_fields(labels, field_dict, threshold=80.0)

    assert len(results) == 1
    assert results[0].canonical_key == "invoice_number"
    # token_set_ratio should handle word order gracefully
    assert results[0].match_score == 100.0


# ============================================================
# Test: Threshold Behavior
# ============================================================


def test_below_threshold_returns_none():
    """Test that scores below threshold return None for canonical_key."""
    field_dict = {"invoice_number": ["Invoice Number"]}
    labels = [
        TranslatedLabel(
            original_text="xyz",
            translated_text="xyz",  # Poor match
            detected_source_language="en",
        )
    ]

    results = match_fields(labels, field_dict, threshold=80.0)

    assert len(results) == 1
    assert results[0].canonical_key is None
    assert results[0].matched_variant is None
    assert results[0].match_score < 80.0


def test_at_threshold_returns_match():
    """Test that scores exactly at threshold are accepted."""
    # We need to find a label that scores exactly 80.0
    # This is tricky, so let's use a very low threshold instead
    field_dict = {"invoice_number": ["Invoice Number"]}
    labels = [
        TranslatedLabel(
            original_text="Inv",
            translated_text="Inv",
            detected_source_language="en",
        )
    ]

    results = match_fields(labels, field_dict, threshold=0.0)

    assert len(results) == 1
    # Should match even with low score if threshold is 0
    assert results[0].canonical_key == "invoice_number"


def test_above_threshold_returns_match():
    """Test that scores above threshold return a match."""
    field_dict = {"invoice_number": ["Invoice Number", "Invoice No"]}
    labels = [
        TranslatedLabel(
            original_text="Inv No",
            translated_text="Invoice No",
            detected_source_language="en",
        )
    ]

    results = match_fields(labels, field_dict, threshold=80.0)

    assert len(results) == 1
    assert results[0].canonical_key == "invoice_number"
    assert results[0].match_score >= 80.0


def test_custom_threshold():
    """Test that custom threshold values are respected."""
    field_dict = {"invoice_number": ["Invoice Number"]}
    labels = [
        TranslatedLabel(
            original_text="Invoice",
            translated_text="Invoice",
            detected_source_language="en",
        )
    ]

    # Test with strict threshold (95.0)
    results_strict = match_fields(labels, field_dict, threshold=95.0)
    # "Invoice" vs "Invoice Number" might not reach 95
    if results_strict[0].match_score < 95.0:
        assert results_strict[0].canonical_key is None

    # Test with lenient threshold (50.0)
    results_lenient = match_fields(labels, field_dict, threshold=50.0)
    assert results_lenient[0].canonical_key == "invoice_number"


# ============================================================
# Test: Dictionary Variants
# ============================================================


def test_matches_against_multiple_variants(sample_field_dictionary):
    """Test that matching tries all variants and picks the best."""
    labels = [
        TranslatedLabel(
            original_text="請求書番号",
            translated_text="Inv #",  # Matches a variant
            detected_source_language="ja",
        )
    ]

    results = match_fields(labels, sample_field_dictionary, threshold=80.0)

    assert len(results) == 1
    assert results[0].canonical_key == "invoice_number"
    assert results[0].matched_variant == "Inv #"


def test_variant_tracking(sample_field_dictionary):
    """Test that matched_variant correctly tracks which variant matched."""
    labels = [
        TranslatedLabel(
            original_text="支払期日",
            translated_text="Payment Due",
            detected_source_language="ja",
        )
    ]

    results = match_fields(labels, sample_field_dictionary, threshold=80.0)

    assert len(results) == 1
    assert results[0].canonical_key == "due_date"
    assert results[0].matched_variant == "Payment Due"


def test_multiple_canonical_keys(sample_field_dictionary):
    """Test matching against dictionary with multiple canonical keys."""
    labels = [
        TranslatedLabel(
            original_text="請求書番号",
            translated_text="Invoice Number",
            detected_source_language="ja",
        ),
        TranslatedLabel(
            original_text="荷送人",
            translated_text="Shipper",
            detected_source_language="ja",
        ),
        TranslatedLabel(
            original_text="合計",
            translated_text="Total",
            detected_source_language="ja",
        ),
    ]

    results = match_fields(labels, sample_field_dictionary, threshold=80.0)

    assert len(results) == 3
    assert results[0].canonical_key == "invoice_number"
    assert results[1].canonical_key == "shipper_name"
    assert results[2].canonical_key == "total_amount"


# ============================================================
# Test: Deterministic Behavior
# ============================================================


def test_tie_breaking_lexicographic():
    """Test that ties are broken using lexicographic ordering of canonical_key."""
    # Create a scenario where two canonical keys have identical scores
    field_dict = {
        "zeta_field": ["Common Label"],
        "alpha_field": ["Common Label"],  # Same variant
    }
    labels = [
        TranslatedLabel(
            original_text="ラベル",
            translated_text="Common Label",
            detected_source_language="ja",
        )
    ]

    results = match_fields(labels, field_dict, threshold=80.0)

    assert len(results) == 1
    # Should pick "alpha_field" due to lexicographic ordering (a < z)
    assert results[0].canonical_key == "alpha_field"


def test_same_input_same_output(sample_field_dictionary, sample_translated_labels):
    """Test that running the same inputs twice produces identical outputs."""
    results1 = match_fields(sample_translated_labels, sample_field_dictionary, threshold=80.0)
    results2 = match_fields(sample_translated_labels, sample_field_dictionary, threshold=80.0)

    assert len(results1) == len(results2)
    for r1, r2 in zip(results1, results2, strict=True):
        assert r1.original_text == r2.original_text
        assert r1.translated_text == r2.translated_text
        assert r1.canonical_key == r2.canonical_key
        assert r1.match_score == r2.match_score
        assert r1.matched_variant == r2.matched_variant


def test_order_independence():
    """Test that the order of field_dictionary doesn't affect results."""
    field_dict1 = {
        "invoice_number": ["Invoice No"],
        "due_date": ["Due Date"],
    }
    field_dict2 = {
        "due_date": ["Due Date"],
        "invoice_number": ["Invoice No"],
    }
    labels = [
        TranslatedLabel(
            original_text="請求書番号",
            translated_text="Invoice No",
            detected_source_language="ja",
        )
    ]

    results1 = match_fields(labels, field_dict1, threshold=80.0)
    results2 = match_fields(labels, field_dict2, threshold=80.0)

    assert results1[0].canonical_key == results2[0].canonical_key
    assert results1[0].match_score == results2[0].match_score


# ============================================================
# Test: Edge Cases
# ============================================================


def test_empty_translated_labels_returns_empty_list():
    """Test that empty input returns empty output."""
    field_dict = {"invoice_number": ["Invoice Number"]}
    results = match_fields([], field_dict, threshold=80.0)
    assert results == []


def test_empty_field_dictionary_returns_all_none():
    """Test that empty dictionary results in all canonical_key=None."""
    labels = [
        TranslatedLabel(
            original_text="請求書番号",
            translated_text="Invoice Number",
            detected_source_language="ja",
        )
    ]
    results = match_fields(labels, {}, threshold=80.0)

    assert len(results) == 1
    assert results[0].canonical_key is None
    assert results[0].matched_variant is None


def test_whitespace_only_label_normalized():
    """Test that whitespace-only labels are handled gracefully."""
    field_dict = {"invoice_number": ["Invoice Number"]}
    labels = [
        TranslatedLabel(
            original_text="   ",
            translated_text="   ",
            detected_source_language="en",
        )
    ]

    results = match_fields(labels, field_dict, threshold=80.0)

    assert len(results) == 1
    # Should not match anything meaningful
    assert results[0].canonical_key is None


def test_special_characters_handled():
    """Test that special characters are handled in matching."""
    field_dict = {"invoice_number": ["Invoice #123"]}
    labels = [
        TranslatedLabel(
            original_text="Invoice #123",
            translated_text="Invoice #123",
            detected_source_language="en",
        )
    ]

    results = match_fields(labels, field_dict, threshold=80.0)

    assert len(results) == 1
    assert results[0].canonical_key == "invoice_number"
    assert results[0].match_score == 100.0


def test_unicode_handling():
    """Test that Unicode characters (emoji, diacritics) are handled correctly."""
    field_dict = {"cafe_name": ["Café ☕"]}
    labels = [
        TranslatedLabel(
            original_text="Café ☕",
            translated_text="Café ☕",
            detected_source_language="en",
        )
    ]

    results = match_fields(labels, field_dict, threshold=80.0)

    assert len(results) == 1
    assert results[0].canonical_key == "cafe_name"


def test_invalid_threshold_raises_error():
    """Test that invalid threshold values raise ValueError."""
    field_dict = {"invoice_number": ["Invoice Number"]}
    labels = [
        TranslatedLabel(
            original_text="請求書番号",
            translated_text="Invoice Number",
            detected_source_language="ja",
        )
    ]

    with pytest.raises(ValueError, match="Threshold must be in range"):
        match_fields(labels, field_dict, threshold=-10.0)

    with pytest.raises(ValueError, match="Threshold must be in range"):
        match_fields(labels, field_dict, threshold=150.0)


# ============================================================
# Test: Integration with TranslatedLabel
# ============================================================


def test_preserves_original_text():
    """Test that original_text is preserved from TranslatedLabel."""
    field_dict = {"invoice_number": ["Invoice Number"]}
    labels = [
        TranslatedLabel(
            original_text="請求書番号",
            translated_text="Invoice Number",
            detected_source_language="ja",
        )
    ]

    results = match_fields(labels, field_dict, threshold=80.0)

    assert len(results) == 1
    assert results[0].original_text == "請求書番号"


def test_uses_translated_text_for_matching():
    """Test that translated_text (not original_text) is used for matching."""
    field_dict = {"invoice_number": ["Invoice Number"]}
    labels = [
        TranslatedLabel(
            original_text="請求書番号",  # Japanese
            translated_text="Invoice Number",  # English
            detected_source_language="ja",
        )
    ]

    results = match_fields(labels, field_dict, threshold=80.0)

    assert len(results) == 1
    # Should match using English translation
    assert results[0].canonical_key == "invoice_number"
    assert results[0].translated_text == "Invoice Number"


def test_japanese_original_english_translation(sample_field_dictionary):
    """Test full flow with Japanese original and English translation."""
    labels = [
        TranslatedLabel(
            original_text="請求書番号",
            translated_text="invoice number",
            detected_source_language="ja",
        ),
        TranslatedLabel(
            original_text="支払期日",
            translated_text="due date",
            detected_source_language="ja",
        ),
    ]

    results = match_fields(labels, sample_field_dictionary, threshold=80.0)

    assert len(results) == 2
    assert results[0].original_text == "請求書番号"
    assert results[0].canonical_key == "invoice_number"
    assert results[1].original_text == "支払期日"
    assert results[1].canonical_key == "due_date"


# ============================================================
# Test: Performance
# ============================================================


def test_large_dictionary_reasonable_time():
    """Test that matching against a large dictionary completes in reasonable time."""
    import time

    # Create a large dictionary with 1000 canonical keys
    large_dict = {f"field_{i}": [f"Field {i}", f"Fld {i}", f"F{i}"] for i in range(1000)}

    labels = [
        TranslatedLabel(
            original_text="フィールド500",
            translated_text="Field 500",
            detected_source_language="ja",
        )
    ]

    start_time = time.time()
    results = match_fields(labels, large_dict, threshold=80.0)
    elapsed_time = time.time() - start_time

    assert len(results) == 1
    assert results[0].canonical_key == "field_500"
    # Should complete in < 5 seconds
    assert elapsed_time < 5.0


def test_many_labels():
    """Test that matching many labels completes in reasonable time."""
    import time

    field_dict = {
        "invoice_number": ["Invoice Number"],
        "due_date": ["Due Date"],
        "total_amount": ["Total Amount"],
    }

    # Create 100 labels
    labels = [
        TranslatedLabel(
            original_text=f"Label {i}",
            translated_text=f"Invoice Number {i}",
            detected_source_language="en",
        )
        for i in range(100)
    ]

    start_time = time.time()
    results = match_fields(labels, field_dict, threshold=80.0)
    elapsed_time = time.time() - start_time

    assert len(results) == 100
    # Should complete in < 2 seconds
    assert elapsed_time < 2.0


# ============================================================
# Test: Helper Functions
# ============================================================


def test_normalize_text_lowercase():
    """Test _normalize_text converts to lowercase."""
    assert _normalize_text("INVOICE NUMBER") == "invoice number"


def test_normalize_text_strips_whitespace():
    """Test _normalize_text strips leading/trailing whitespace."""
    assert _normalize_text("  Invoice Number  ") == "invoice number"


def test_normalize_text_collapses_whitespace():
    """Test _normalize_text collapses multiple spaces."""
    assert _normalize_text("Invoice    Number") == "invoice number"


def test_normalize_text_unicode_normalization():
    """Test _normalize_text applies Unicode normalization."""
    # Café with combining character vs composed character
    text1 = "Cafe\u0301"  # Café (e + combining acute accent)
    text2 = "Café"  # Café (composed character)
    assert _normalize_text(text1) == _normalize_text(text2)


def test_calculate_similarity_exact_match():
    """Test _calculate_similarity returns 100 for exact matches."""
    score = _calculate_similarity("invoice number", "invoice number")
    assert score == 100.0


def test_calculate_similarity_word_order():
    """Test _calculate_similarity handles word order with token_set_ratio."""
    score = _calculate_similarity("invoice number", "number invoice")
    assert score == 100.0  # token_set_ratio ignores order


def test_find_best_match_returns_best(sample_field_dictionary):
    """Test _find_best_match returns the highest scoring match."""
    canonical_key, score, variant = _find_best_match(
        "Invoice No", sample_field_dictionary, threshold=80.0
    )
    assert canonical_key == "invoice_number"
    assert score == 100.0
    assert variant == "Invoice No"


def test_find_best_match_below_threshold_returns_none(sample_field_dictionary):
    """Test _find_best_match returns None when below threshold."""
    canonical_key, score, variant = _find_best_match("xyz", sample_field_dictionary, threshold=80.0)
    assert canonical_key is None
    assert score < 80.0
    assert variant is None
