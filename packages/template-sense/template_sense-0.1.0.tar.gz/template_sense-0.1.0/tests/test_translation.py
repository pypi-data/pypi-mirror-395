"""
Unit tests for translation layer via AI.

Tests cover:
- TranslatedLabel dataclass creation and defaults
- Successful translation scenarios (single label, batch, with/without duplicates)
- Empty list edge case
- Already-English labels
- Provider complete failure (AIProviderError)
- Individual label failures (partial success)
- Deduplication correctness
- Position mapping accuracy
- Logging and metadata preservation

Coverage Target: 85%+
"""

from unittest.mock import Mock, patch

import pytest

from template_sense.ai.translation import (
    TranslatedLabel,
    _deduplicate_labels,
    translate_labels,
)
from template_sense.ai_providers.interface import AIProvider
from template_sense.constants import DEFAULT_TARGET_LANGUAGE
from template_sense.errors import AIProviderError

# ============================================================
# Fixtures
# ============================================================


@pytest.fixture
def mock_provider():
    """Create a mock AIProvider for testing."""
    provider = Mock(spec=AIProvider)
    provider.provider_name = "test-provider"
    provider.model = "test-model"
    return provider


@pytest.fixture
def sample_japanese_labels():
    """Sample Japanese labels for testing."""
    return ["請求書番号", "発行日", "荷送人名"]


@pytest.fixture
def sample_mixed_labels():
    """Sample multi-language labels for testing."""
    return ["請求書番号", "AWB NO", "受取人", "Invoice Date"]


@pytest.fixture
def sample_labels_with_duplicates():
    """Sample labels with duplicates for testing deduplication."""
    return ["Invoice No", "Date", "Invoice No", "Total", "Date", "Amount"]


# Mock translations dictionary
MOCK_TRANSLATIONS = {
    "請求書番号": "invoice number",
    "発行日": "issue date",
    "荷送人名": "shipper name",
    "AWB NO": "air waybill number",
    "受取人": "consignee",
    "Invoice Date": "Invoice Date",  # Already English
    "Invoice No": "Invoice Number",
    "Date": "Date",
    "Total": "Total",
    "Amount": "Amount",
}


# ============================================================
# Test Classes
# ============================================================


class TestTranslatedLabelDataclass:
    """Tests for TranslatedLabel dataclass creation and defaults."""

    def test_dataclass_creation_all_fields(self):
        """Test creating TranslatedLabel with all fields specified."""
        label = TranslatedLabel(
            original_text="請求書番号",
            translated_text="invoice number",
            detected_source_language="ja",
            target_language="en",
            model_confidence=0.95,
            metadata={"provider": "openai"},
        )

        assert label.original_text == "請求書番号"
        assert label.translated_text == "invoice number"
        assert label.detected_source_language == "ja"
        assert label.target_language == "en"
        assert label.model_confidence == 0.95
        assert label.metadata == {"provider": "openai"}

    def test_dataclass_creation_minimal_fields(self):
        """Test creating TranslatedLabel with only required fields."""
        label = TranslatedLabel(
            original_text="請求書番号",
            translated_text="invoice number",
        )

        assert label.original_text == "請求書番号"
        assert label.translated_text == "invoice number"
        assert label.detected_source_language is None
        assert label.target_language == DEFAULT_TARGET_LANGUAGE
        assert label.model_confidence is None
        assert label.metadata is None

    def test_dataclass_default_target_language(self):
        """Test that default target language is 'en'."""
        label = TranslatedLabel(
            original_text="test",
            translated_text="test",
        )

        assert label.target_language == "en"


class TestDeduplicationHelper:
    """Tests for _deduplicate_labels() helper function."""

    def test_deduplicate_no_duplicates(self):
        """Test deduplication with no duplicates."""
        labels = ["Invoice No", "Date", "Total"]
        unique, pos_map = _deduplicate_labels(labels)

        assert unique == ["Invoice No", "Date", "Total"]
        assert pos_map == {
            "Invoice No": [0],
            "Date": [1],
            "Total": [2],
        }

    def test_deduplicate_with_duplicates(self, sample_labels_with_duplicates):
        """Test deduplication with duplicates preserves order and tracks positions."""
        unique, pos_map = _deduplicate_labels(sample_labels_with_duplicates)

        # Unique labels should preserve first appearance order
        assert unique == ["Invoice No", "Date", "Total", "Amount"]

        # Position map should track all occurrences
        assert pos_map["Invoice No"] == [0, 2]
        assert pos_map["Date"] == [1, 4]
        assert pos_map["Total"] == [3]
        assert pos_map["Amount"] == [5]

    def test_deduplicate_empty_list(self):
        """Test deduplication with empty list."""
        unique, pos_map = _deduplicate_labels([])

        assert unique == []
        assert pos_map == {}

    def test_deduplicate_single_label(self):
        """Test deduplication with single label."""
        labels = ["Invoice No"]
        unique, pos_map = _deduplicate_labels(labels)

        assert unique == ["Invoice No"]
        assert pos_map == {"Invoice No": [0]}

    def test_deduplicate_all_same_label(self):
        """Test deduplication when all labels are the same."""
        labels = ["Invoice No", "Invoice No", "Invoice No"]
        unique, pos_map = _deduplicate_labels(labels)

        assert unique == ["Invoice No"]
        assert pos_map == {"Invoice No": [0, 1, 2]}


class TestTranslateLabelsSuccess:
    """Tests for successful translation scenarios."""

    def test_translate_single_label_explicit_language(self, mock_provider):
        """Test translating a single label with explicit source language."""
        mock_provider.translate_text.return_value = "invoice number"

        result = translate_labels(
            ai_provider=mock_provider,
            labels=["請求書番号"],
            source_language="ja",
            target_language="en",
        )

        # Assertions
        assert len(result) == 1
        assert isinstance(result[0], TranslatedLabel)
        assert result[0].original_text == "請求書番号"
        assert result[0].translated_text == "invoice number"
        assert result[0].detected_source_language == "ja"
        assert result[0].target_language == "en"
        assert result[0].metadata["provider"] == "test-provider"

        # Verify API was called correctly
        mock_provider.translate_text.assert_called_once_with(
            text="請求書番号",
            source_lang="ja",
            target_lang="en",
        )

    def test_translate_single_label_auto_detect(self, mock_provider):
        """Test translating a single label with auto-detect language."""
        mock_provider.translate_text.return_value = "invoice number"

        result = translate_labels(
            ai_provider=mock_provider,
            labels=["請求書番号"],
            source_language=None,  # Auto-detect
            target_language="en",
        )

        # Assertions
        assert len(result) == 1
        assert result[0].original_text == "請求書番号"
        assert result[0].translated_text == "invoice number"
        assert result[0].detected_source_language is None  # None when auto-detect

        # Verify API was called with "auto"
        mock_provider.translate_text.assert_called_once_with(
            text="請求書番号",
            source_lang="auto",
            target_lang="en",
        )

    def test_translate_batch_no_duplicates(self, mock_provider, sample_japanese_labels):
        """Test translating multiple labels without duplicates."""

        def mock_translate(text, source_lang, target_lang):
            return MOCK_TRANSLATIONS.get(text, text)

        mock_provider.translate_text.side_effect = mock_translate

        result = translate_labels(
            ai_provider=mock_provider,
            labels=sample_japanese_labels,
            source_language="ja",
            target_language="en",
        )

        # Assertions
        assert len(result) == 3
        assert result[0].translated_text == "invoice number"
        assert result[1].translated_text == "issue date"
        assert result[2].translated_text == "shipper name"

        # Verify API was called 3 times (no duplicates)
        assert mock_provider.translate_text.call_count == 3

    def test_translate_batch_with_duplicates(self, mock_provider, sample_labels_with_duplicates):
        """Test translating labels with duplicates - deduplication should reduce API calls."""

        def mock_translate(text, source_lang, target_lang):
            return MOCK_TRANSLATIONS.get(text, text)

        mock_provider.translate_text.side_effect = mock_translate

        result = translate_labels(
            ai_provider=mock_provider,
            labels=sample_labels_with_duplicates,  # 6 labels, 4 unique
            source_language=None,
            target_language="en",
        )

        # Assertions
        assert len(result) == 6  # Same length as input
        assert result[0].translated_text == "Invoice Number"  # "Invoice No"
        assert result[1].translated_text == "Date"
        assert result[2].translated_text == "Invoice Number"  # Duplicate
        assert result[3].translated_text == "Total"
        assert result[4].translated_text == "Date"  # Duplicate
        assert result[5].translated_text == "Amount"

        # Verify API was only called 4 times (deduplication worked)
        assert mock_provider.translate_text.call_count == 4

    def test_translate_already_english_labels(self, mock_provider):
        """Test translating labels that are already in English."""
        labels = ["Invoice Number", "Date", "Total"]

        def mock_translate(text, source_lang, target_lang):
            # Simulate AI returning same text for English
            return text

        mock_provider.translate_text.side_effect = mock_translate

        result = translate_labels(
            ai_provider=mock_provider,
            labels=labels,
            source_language=None,
            target_language="en",
        )

        # Assertions
        assert len(result) == 3
        assert result[0].translated_text == "Invoice Number"
        assert result[1].translated_text == "Date"
        assert result[2].translated_text == "Total"

    def test_translate_mixed_languages(self, mock_provider, sample_mixed_labels):
        """Test translating a mix of Japanese, English, and abbreviations."""

        def mock_translate(text, source_lang, target_lang):
            return MOCK_TRANSLATIONS.get(text, text)

        mock_provider.translate_text.side_effect = mock_translate

        result = translate_labels(
            ai_provider=mock_provider,
            labels=sample_mixed_labels,
            source_language=None,
            target_language="en",
        )

        # Assertions
        assert len(result) == 4
        assert result[0].translated_text == "invoice number"  # Japanese
        assert result[1].translated_text == "air waybill number"  # Abbreviation
        assert result[2].translated_text == "consignee"  # Japanese
        assert result[3].translated_text == "Invoice Date"  # Already English


class TestTranslateLabelsErrorHandling:
    """Tests for error handling scenarios."""

    def test_translate_empty_list(self, mock_provider):
        """Test translating an empty list returns empty list."""
        result = translate_labels(
            ai_provider=mock_provider,
            labels=[],
            source_language=None,
            target_language="en",
        )

        assert result == []
        # Verify API was not called
        mock_provider.translate_text.assert_not_called()

    def test_translate_provider_complete_failure(self, mock_provider):
        """Test handling when AI provider fails completely for all labels."""
        # Mock provider to raise AIProviderError for all calls
        mock_provider.translate_text.side_effect = AIProviderError(
            provider_name="test-provider",
            error_details="API timeout",
            request_type="translate",
        )

        labels = ["請求書番号", "発行日"]

        # Translation should not raise - should fallback to original text
        result = translate_labels(
            ai_provider=mock_provider,
            labels=labels,
            source_language="ja",
            target_language="en",
        )

        # Assertions - should fallback to original text
        assert len(result) == 2
        assert result[0].translated_text == "請求書番号"  # Fallback to original
        assert result[1].translated_text == "発行日"  # Fallback to original
        assert "error" in result[0].metadata
        assert "error" in result[1].metadata

    def test_translate_partial_success(self, mock_provider):
        """Test handling when some labels succeed and some fail."""
        call_count = [0]

        def mock_translate(text, source_lang, target_lang):
            call_count[0] += 1
            if call_count[0] == 2:  # Fail on second call
                raise AIProviderError(
                    provider_name="test-provider",
                    error_details="Translation failed",
                    request_type="translate",
                )
            return MOCK_TRANSLATIONS.get(text, text)

        mock_provider.translate_text.side_effect = mock_translate

        labels = ["請求書番号", "発行日", "荷送人名"]

        result = translate_labels(
            ai_provider=mock_provider,
            labels=labels,
            source_language="ja",
            target_language="en",
        )

        # Assertions
        assert len(result) == 3
        assert result[0].translated_text == "invoice number"  # Success
        assert result[1].translated_text == "発行日"  # Failed - fallback to original
        assert result[2].translated_text == "shipper name"  # Success
        assert "error" not in result[0].metadata
        assert "error" in result[1].metadata
        assert "error" not in result[2].metadata

    def test_translate_unexpected_exception(self, mock_provider):
        """Test handling unexpected exceptions during translation."""
        # Mock provider to raise unexpected exception
        mock_provider.translate_text.side_effect = ValueError("Unexpected error")

        labels = ["請求書番号"]

        # Should not raise - should fallback to original text
        result = translate_labels(
            ai_provider=mock_provider,
            labels=labels,
            source_language="ja",
            target_language="en",
        )

        # Assertions - should fallback to original text
        assert len(result) == 1
        assert result[0].translated_text == "請求書番号"
        assert "error" in result[0].metadata
        assert "Unexpected error" in result[0].metadata["error"]


class TestTranslateLabelsLoggingAndMetadata:
    """Tests for logging behavior and metadata preservation."""

    def test_translate_logs_debug_info(self, mock_provider, sample_japanese_labels):
        """Test that translation logs debug information."""

        def mock_translate(text, source_lang, target_lang):
            return MOCK_TRANSLATIONS.get(text, text)

        mock_provider.translate_text.side_effect = mock_translate

        with patch("template_sense.ai.translation.logger") as mock_logger:
            translate_labels(
                ai_provider=mock_provider,
                labels=sample_japanese_labels,
                source_language="ja",
                target_language="en",
            )

            # Verify debug logging was called
            assert mock_logger.debug.call_count > 0

    def test_translate_logs_summary_statistics(self, mock_provider, sample_japanese_labels):
        """Test that translation logs summary statistics."""

        def mock_translate(text, source_lang, target_lang):
            return MOCK_TRANSLATIONS.get(text, text)

        mock_provider.translate_text.side_effect = mock_translate

        with patch("template_sense.ai.translation.logger") as mock_logger:
            translate_labels(
                ai_provider=mock_provider,
                labels=sample_japanese_labels,
                source_language="ja",
                target_language="en",
            )

            # Verify info logging for summary was called
            mock_logger.info.assert_called()
            # Check that the info call contains "successful" and "failed"
            info_call_args = str(mock_logger.info.call_args)
            assert "successful" in info_call_args or "complete" in info_call_args

    def test_translate_logs_warnings_on_failure(self, mock_provider):
        """Test that translation logs warnings when individual translations fail."""
        mock_provider.translate_text.side_effect = AIProviderError(
            provider_name="test-provider",
            error_details="API error",
            request_type="translate",
        )

        with patch("template_sense.ai.translation.logger") as mock_logger:
            translate_labels(
                ai_provider=mock_provider,
                labels=["請求書番号"],
                source_language="ja",
                target_language="en",
            )

            # Verify warning logging was called
            mock_logger.warning.assert_called()

    def test_translate_metadata_includes_provider(self, mock_provider, sample_japanese_labels):
        """Test that metadata includes provider name."""

        def mock_translate(text, source_lang, target_lang):
            return MOCK_TRANSLATIONS.get(text, text)

        mock_provider.translate_text.side_effect = mock_translate

        result = translate_labels(
            ai_provider=mock_provider,
            labels=sample_japanese_labels,
            source_language="ja",
            target_language="en",
        )

        # All results should have provider in metadata
        for translation in result:
            assert translation.metadata is not None
            assert "provider" in translation.metadata
            assert translation.metadata["provider"] == "test-provider"


class TestTranslateLabelsEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_translate_unicode_preservation(self, mock_provider):
        """Test that Unicode characters are preserved correctly."""
        unicode_labels = ["請求書番号", "中文", "한글"]

        def mock_translate(text, source_lang, target_lang):
            # Simulate preserving Unicode in translation
            return f"translated_{text}"

        mock_provider.translate_text.side_effect = mock_translate

        result = translate_labels(
            ai_provider=mock_provider,
            labels=unicode_labels,
            source_language=None,
            target_language="en",
        )

        # Verify Unicode is preserved in original_text
        assert result[0].original_text == "請求書番号"
        assert result[1].original_text == "中文"
        assert result[2].original_text == "한글"

    def test_translate_whitespace_labels(self, mock_provider):
        """Test handling of labels with whitespace."""
        labels = ["  Invoice No  ", "Date", "Total  "]

        def mock_translate(text, source_lang, target_lang):
            return text.strip()

        mock_provider.translate_text.side_effect = mock_translate

        result = translate_labels(
            ai_provider=mock_provider,
            labels=labels,
            source_language=None,
            target_language="en",
        )

        # Original text should be preserved exactly
        assert result[0].original_text == "  Invoice No  "
        assert result[2].original_text == "Total  "

    def test_translate_default_target_language(self, mock_provider):
        """Test that default target language is used when not specified."""
        mock_provider.translate_text.return_value = "invoice number"

        result = translate_labels(
            ai_provider=mock_provider,
            labels=["請求書番号"],
            source_language="ja",
            # target_language not specified - should use default
        )

        # Verify default target language is used
        assert result[0].target_language == DEFAULT_TARGET_LANGUAGE

        # Verify API was called with default target language
        mock_provider.translate_text.assert_called_once()
        call_kwargs = mock_provider.translate_text.call_args[1]
        assert call_kwargs["target_lang"] == DEFAULT_TARGET_LANGUAGE
