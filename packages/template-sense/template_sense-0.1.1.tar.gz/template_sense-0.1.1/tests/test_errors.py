"""Tests for custom exception hierarchy."""

import pytest

from template_sense.errors import (
    AIProviderError,
    ExtractionError,
    FileValidationError,
    MappingError,
    NormalizationError,
    TemplateSenseError,
    TranslationError,
    UnsupportedFileTypeError,
)


class TestBaseException:
    """Tests for the base TemplateSenseError exception."""

    def test_base_exception_can_be_raised(self):
        """Test that base exception can be raised and caught."""
        with pytest.raises(TemplateSenseError) as exc_info:
            raise TemplateSenseError("Test error")

        assert str(exc_info.value) == "Test error"

    def test_base_exception_catches_all_subclasses(self):
        """Test that base exception catches all Template Sense errors."""
        with pytest.raises(TemplateSenseError):
            raise FileValidationError("Test file error")

        with pytest.raises(TemplateSenseError):
            raise ExtractionError("header", "Test extraction error")


class TestFileValidationError:
    """Tests for FileValidationError exception."""

    def test_error_without_file_path(self):
        """Test error message without file path."""
        error = FileValidationError("File is empty")

        assert "File validation failed: File is empty" in str(error)
        assert error.reason == "File is empty"
        assert error.filename is None

    def test_error_with_file_path(self):
        """Test error message with file path."""
        error = FileValidationError("Invalid format", "/path/to/invoice_template.xlsx")

        assert "File validation failed: Invalid format" in str(error)
        assert "(file: invoice_template.xlsx)" in str(error)
        assert error.reason == "Invalid format"
        assert error.filename == "invoice_template.xlsx"

    def test_path_sanitization(self):
        """Test that full paths are sanitized to basename only."""
        # Unix-style path
        error = FileValidationError("Test", "/usr/local/data/sensitive/file.xlsx")
        assert error.filename == "file.xlsx"
        assert "/usr/local" not in str(error)

        # Test with another Unix path to verify sanitization works consistently
        error = FileValidationError("Test", "/tmp/test_data/invoice.xlsx")
        assert error.filename == "invoice.xlsx"
        assert "/tmp" not in str(error)
        assert "test_data" not in str(error)

    def test_inherits_from_base(self):
        """Test that FileValidationError inherits from TemplateSenseError."""
        error = FileValidationError("Test")
        assert isinstance(error, TemplateSenseError)


class TestUnsupportedFileTypeError:
    """Tests for UnsupportedFileTypeError exception."""

    def test_error_with_default_supported_types(self):
        """Test error message with default supported types."""
        error = UnsupportedFileTypeError(".csv")

        assert "Unsupported file type: .csv" in str(error)
        assert "Expected: .xlsx" in str(error)
        assert error.file_extension == ".csv"
        assert error.supported_types is None

    def test_error_with_custom_supported_types(self):
        """Test error message with custom supported types list."""
        error = UnsupportedFileTypeError(".pdf", [".xlsx", ".xls"])

        assert "Unsupported file type: .pdf" in str(error)
        assert "Expected: .xlsx, .xls" in str(error)
        assert error.file_extension == ".pdf"
        assert error.supported_types == [".xlsx", ".xls"]

    def test_inherits_from_base(self):
        """Test that UnsupportedFileTypeError inherits from TemplateSenseError."""
        error = UnsupportedFileTypeError(".txt")
        assert isinstance(error, TemplateSenseError)


class TestExtractionError:
    """Tests for ExtractionError exception."""

    def test_error_with_all_context(self):
        """Test error message with all context parameters."""
        error = ExtractionError("header", "No bold text found", row_index=5)

        assert "Failed to extract header" in str(error)
        assert "No bold text found" in str(error)
        assert "(row 5)" in str(error)
        assert error.extraction_type == "header"
        assert error.reason == "No bold text found"
        assert error.row_index == 5

    def test_error_with_partial_context(self):
        """Test error message with partial context."""
        error = ExtractionError("table")

        assert "Failed to extract table" in str(error)
        assert error.extraction_type == "table"
        assert error.reason is None
        assert error.row_index is None

    def test_error_with_reason_only(self):
        """Test error message with reason but no row index."""
        error = ExtractionError("header", "Empty region")

        assert "Failed to extract header: Empty region" in str(error)
        assert error.reason == "Empty region"
        assert error.row_index is None

    def test_one_based_row_indexing(self):
        """Test that row index uses 1-based indexing (Excel convention)."""
        error = ExtractionError("header", row_index=1)
        assert "(row 1)" in str(error)
        assert error.row_index == 1

    def test_unicode_text_in_reason(self):
        """Test that Unicode/Japanese text is preserved in reason."""
        error = ExtractionError("header", "ヘッダーが見つかりません", row_index=3)

        assert "ヘッダーが見つかりません" in str(error)
        assert error.reason == "ヘッダーが見つかりません"

    def test_inherits_from_base(self):
        """Test that ExtractionError inherits from TemplateSenseError."""
        error = ExtractionError("header")
        assert isinstance(error, TemplateSenseError)


class TestAIProviderError:
    """Tests for AIProviderError exception."""

    def test_error_with_all_parameters(self):
        """Test error message with all parameters."""
        error = AIProviderError("openai", "Rate limit exceeded", request_type="classify_field")

        assert "AI provider 'openai' request failed" in str(error)
        assert "(classify_field)" in str(error)
        assert "Rate limit exceeded" in str(error)
        assert error.provider_name == "openai"
        assert error.error_details == "Rate limit exceeded"
        assert error.request_type == "classify_field"

    def test_error_with_partial_parameters(self):
        """Test error message with partial parameters."""
        error = AIProviderError("anthropic")

        assert "AI provider 'anthropic' request failed" in str(error)
        assert error.provider_name == "anthropic"
        assert error.error_details is None
        assert error.request_type is None

    def test_provider_agnostic_design(self):
        """Test that error works with any provider name."""
        providers = ["openai", "anthropic", "custom_provider"]

        for provider in providers:
            error = AIProviderError(provider, "Test error")
            assert provider in str(error)
            assert error.provider_name == provider

    def test_inherits_from_base(self):
        """Test that AIProviderError inherits from TemplateSenseError."""
        error = AIProviderError("openai")
        assert isinstance(error, TemplateSenseError)


class TestTranslationError:
    """Tests for TranslationError exception."""

    def test_error_with_all_parameters(self):
        """Test error message with all parameters."""
        error = TranslationError("請求書番号", "Dictionary lookup failed", source_language="ja")

        assert "Translation failed for text: '請求書番号'" in str(error)
        assert "(language: ja)" in str(error)
        assert "Dictionary lookup failed" in str(error)
        assert error.source_text == "請求書番号"
        assert error.reason == "Dictionary lookup failed"
        assert error.source_language == "ja"

    def test_japanese_text_preservation(self):
        """Test that Japanese text is preserved correctly."""
        japanese_texts = ["請求書", "荷送人", "合計金額"]

        for text in japanese_texts:
            error = TranslationError(text)
            assert text in str(error)
            assert error.source_text == text

    def test_error_with_minimal_parameters(self):
        """Test error message with minimal parameters."""
        error = TranslationError("invoice_number")

        assert "Translation failed for text: 'invoice_number'" in str(error)
        assert error.source_text == "invoice_number"
        assert error.reason is None
        assert error.source_language is None

    def test_inherits_from_base(self):
        """Test that TranslationError inherits from TemplateSenseError."""
        error = TranslationError("test")
        assert isinstance(error, TemplateSenseError)


class TestMappingError:
    """Tests for MappingError exception."""

    def test_error_with_all_parameters(self):
        """Test error message with all parameters."""
        error = MappingError("請求書番号", "No fuzzy match found", confidence_score=65.5)

        assert "Mapping failed for field: '請求書番号'" in str(error)
        assert "(confidence: 65.5)" in str(error)
        assert "No fuzzy match found" in str(error)
        assert error.field_name == "請求書番号"
        assert error.reason == "No fuzzy match found"
        assert error.confidence_score == 65.5

    def test_japanese_field_name_preservation(self):
        """Test that Japanese field names are preserved."""
        error = MappingError("荷送人名", confidence_score=50.0)

        assert "荷送人名" in str(error)
        assert error.field_name == "荷送人名"

    def test_error_with_minimal_parameters(self):
        """Test error message with minimal parameters."""
        error = MappingError("unknown_field")

        assert "Mapping failed for field: 'unknown_field'" in str(error)
        assert error.field_name == "unknown_field"
        assert error.reason is None
        assert error.confidence_score is None

    def test_confidence_score_formatting(self):
        """Test that confidence scores are formatted to 1 decimal place."""
        error = MappingError("field", confidence_score=75.123456)
        assert "(confidence: 75.1)" in str(error)

    def test_inherits_from_base(self):
        """Test that MappingError inherits from TemplateSenseError."""
        error = MappingError("test")
        assert isinstance(error, TemplateSenseError)


class TestNormalizationError:
    """Tests for NormalizationError exception."""

    def test_error_with_all_parameters(self):
        """Test error message with all parameters."""
        error = NormalizationError("Invalid data type", field_name="invoice_number")

        assert "Normalization failed: Invalid data type" in str(error)
        assert "(field: invoice_number)" in str(error)
        assert error.reason == "Invalid data type"
        assert error.field_name == "invoice_number"

    def test_error_with_minimal_parameters(self):
        """Test error message with minimal parameters."""
        error = NormalizationError("Schema mismatch")

        assert "Normalization failed: Schema mismatch" in str(error)
        assert error.reason == "Schema mismatch"
        assert error.field_name is None

    def test_inherits_from_base(self):
        """Test that NormalizationError inherits from TemplateSenseError."""
        error = NormalizationError("test")
        assert isinstance(error, TemplateSenseError)


class TestExceptionChaining:
    """Tests for exception chaining with 'from e' pattern."""

    def test_exception_chaining_preserves_cause(self):
        """Test that 'from e' pattern preserves the original exception."""
        original_error = ValueError("Original error")

        try:
            try:
                raise original_error
            except ValueError as e:
                raise TemplateSenseError("Wrapped error") from e
        except TemplateSenseError as wrapped:
            assert wrapped.__cause__ is original_error
            assert isinstance(wrapped.__cause__, ValueError)

    def test_chaining_with_specific_exceptions(self):
        """Test exception chaining with specific Template Sense exceptions."""
        original_error = OSError("File not found")

        try:
            try:
                raise original_error
            except OSError as e:
                raise FileValidationError("Cannot read file", "/tmp/test.xlsx") from e
        except FileValidationError as wrapped:
            assert wrapped.__cause__ is original_error
            assert "Cannot read file" in str(wrapped)
            assert wrapped.filename == "test.xlsx"
