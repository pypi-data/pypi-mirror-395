"""
Custom exception hierarchy for Template Sense.

All Template Sense exceptions inherit from TemplateSenseError.
This allows callers to catch all package-specific errors with a single except clause.

Exception Categories:
- File/Input: FileValidationError, UnsupportedFileTypeError
- Processing: ExtractionError, TranslationError, MappingError, NormalizationError
- External: AIProviderError

Usage Example:
    try:
        result = analyze_template(file_path)
    except TemplateSenseError as e:
        logger.error(f"Template analysis failed: {e}")
        # All Template Sense errors are caught here
"""

from pathlib import Path


class TemplateSenseError(Exception):
    """Base exception for all Template Sense errors."""


class FileValidationError(TemplateSenseError):
    """Raised when file validation fails."""

    def __init__(self, reason: str, file_path: str | None = None):
        """
        Initialize FileValidationError.

        Args:
            reason: Description of why validation failed
            file_path: Optional file path (will be sanitized to basename only)
        """
        # Extract only filename for security (no full paths)
        filename = Path(file_path).name if file_path else None

        message = f"File validation failed: {reason}"
        if filename:
            message += f" (file: {filename})"

        super().__init__(message)
        self.reason = reason
        self.filename = filename


class UnsupportedFileTypeError(TemplateSenseError):
    """Raised when a file format is not supported."""

    def __init__(self, file_extension: str, supported_types: list[str] | None = None):
        """
        Initialize UnsupportedFileTypeError.

        Args:
            file_extension: The unsupported file extension (e.g., ".csv")
            supported_types: Optional list of supported file types
        """
        supported = ", ".join(supported_types) if supported_types else ".xlsx"
        message = f"Unsupported file type: {file_extension}. Expected: {supported}"

        super().__init__(message)
        self.file_extension = file_extension
        self.supported_types = supported_types


class ExtractionError(TemplateSenseError):
    """Raised when header or table extraction fails."""

    def __init__(
        self,
        extraction_type: str,
        reason: str | None = None,
        row_index: int | None = None,
    ):
        """
        Initialize ExtractionError.

        Args:
            extraction_type: Type of extraction ("header" or "table")
            reason: Optional description of why extraction failed
            row_index: Optional 1-based row index (Excel convention)
        """
        message = f"Failed to extract {extraction_type}"
        if reason:
            message += f": {reason}"
        if row_index is not None:
            message += f" (row {row_index})"

        super().__init__(message)
        self.extraction_type = extraction_type
        self.reason = reason
        self.row_index = row_index


class AIProviderError(TemplateSenseError):
    """Raised when an AI provider request fails."""

    def __init__(
        self,
        provider_name: str,
        error_details: str | None = None,
        request_type: str | None = None,
    ):
        """
        Initialize AIProviderError.

        Args:
            provider_name: Name of the AI provider ("openai", "anthropic", etc.)
            error_details: Optional error details from the provider
            request_type: Optional type of request ("classify_field", "translate", etc.)
        """
        message = f"AI provider '{provider_name}' request failed"
        if request_type:
            message += f" ({request_type})"
        if error_details:
            message += f": {error_details}"

        super().__init__(message)
        self.provider_name = provider_name
        self.error_details = error_details
        self.request_type = request_type


class TranslationError(TemplateSenseError):
    """Raised when translation fails."""

    def __init__(
        self,
        source_text: str,
        reason: str | None = None,
        source_language: str | None = None,
    ):
        """
        Initialize TranslationError.

        Args:
            source_text: The text that failed to translate (Unicode preserved)
            reason: Optional description of why translation failed
            source_language: Optional source language code (e.g., "ja", "en")
        """
        message = f"Translation failed for text: '{source_text}'"
        if source_language:
            message += f" (language: {source_language})"
        if reason:
            message += f": {reason}"

        super().__init__(message)
        self.source_text = source_text
        self.reason = reason
        self.source_language = source_language


class MappingError(TemplateSenseError):
    """Raised when fuzzy matching to canonical fields fails."""

    def __init__(
        self,
        field_name: str,
        reason: str | None = None,
        confidence_score: float | None = None,
    ):
        """
        Initialize MappingError.

        Args:
            field_name: The field name that failed to map (Unicode preserved)
            reason: Optional description of why mapping failed
            confidence_score: Optional fuzzy match confidence score (0.0-100.0)
        """
        message = f"Mapping failed for field: '{field_name}'"
        if confidence_score is not None:
            message += f" (confidence: {confidence_score:.1f})"
        if reason:
            message += f": {reason}"

        super().__init__(message)
        self.field_name = field_name
        self.reason = reason
        self.confidence_score = confidence_score


class NormalizationError(TemplateSenseError):
    """Raised when output normalization fails."""

    def __init__(self, reason: str, field_name: str | None = None):
        """
        Initialize NormalizationError.

        Args:
            reason: Description of why normalization failed
            field_name: Optional field name that caused the error
        """
        message = f"Normalization failed: {reason}"
        if field_name:
            message += f" (field: {field_name})"

        super().__init__(message)
        self.reason = reason
        self.field_name = field_name


class InvalidFieldDictionaryError(TemplateSenseError):
    """Raised when field dictionary validation fails."""

    def __init__(self, reason: str, field_dictionary: dict | None = None):
        """
        Initialize InvalidFieldDictionaryError.

        Args:
            reason: Description of why field dictionary is invalid
            field_dictionary: Optional field dictionary (not logged for security)
        """
        message = f"Invalid field dictionary: {reason}"

        super().__init__(message)
        self.reason = reason
        # Don't store the actual dictionary for security reasons


__all__ = [
    "TemplateSenseError",
    "FileValidationError",
    "UnsupportedFileTypeError",
    "ExtractionError",
    "AIProviderError",
    "TranslationError",
    "MappingError",
    "NormalizationError",
    "InvalidFieldDictionaryError",
]
