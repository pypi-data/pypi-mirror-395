"""
Translation layer for non-English labels via AI.

This module provides translation functionality for field labels extracted from
invoice templates. It takes non-English labels (e.g., Japanese, Chinese) and
translates them into English for downstream canonical field mapping.

The translation layer is provider-agnostic and works with any AIProvider
implementation that supports the translate_text() method.

Architecture Position: AI Analysis → **Translation** → Mapping → Output

Example Usage:
    >>> from template_sense.ai_providers.factory import get_ai_provider
    >>> from template_sense.ai.translation import translate_labels
    >>>
    >>> ai_provider = get_ai_provider()
    >>> labels = ["請求書番号", "発行日", "荷送人名"]
    >>> translations = translate_labels(
    ...     ai_provider=ai_provider,
    ...     labels=labels,
    ...     source_language=None,  # Auto-detect
    ...     target_language="en"
    ... )
    >>> for t in translations:
    ...     print(f"{t.original_text} → {t.translated_text}")
    請求書番号 → invoice number
    発行日 → issue date
    荷送人名 → shipper name
"""

import logging
from dataclasses import dataclass
from typing import Any

from template_sense.ai_providers.interface import AIProvider
from template_sense.constants import DEFAULT_TARGET_LANGUAGE
from template_sense.errors import AIProviderError

# Set up module logger
logger = logging.getLogger(__name__)


@dataclass
class TranslatedLabel:
    """
    Represents a translated label with metadata.

    This dataclass stores the result of AI-based translation, including the
    original text, translated text, detected source language, and optional
    confidence scores.

    Attributes:
        original_text: The original label text before translation (Unicode preserved).
        translated_text: The translated text in the target language.
        detected_source_language: Auto-detected source language code (e.g., "ja", "zh").
                                 None if source language was explicitly provided or
                                 detection was not performed.
        target_language: Target language code (e.g., "en").
        model_confidence: AI confidence score (0.0-1.0), if provided by the model.
                         None if the provider doesn't return confidence scores.
        metadata: Optional provider-specific or additional translation metadata.

    Example:
        >>> label = TranslatedLabel(
        ...     original_text="請求書番号",
        ...     translated_text="invoice number",
        ...     detected_source_language="ja",
        ...     target_language="en",
        ...     model_confidence=0.95,
        ...     metadata={"provider": "openai"}
        ... )
    """

    original_text: str
    translated_text: str
    detected_source_language: str | None = None
    target_language: str = DEFAULT_TARGET_LANGUAGE
    model_confidence: float | None = None
    metadata: dict[str, Any] | None = None


def _deduplicate_labels(labels: list[str]) -> tuple[list[str], dict[str, list[int]]]:
    """
    Deduplicate labels and track their original positions.

    This helper function removes duplicate labels to avoid redundant API calls,
    while maintaining a mapping from each unique label to its original positions
    in the input list.

    Args:
        labels: List of labels (may contain duplicates)

    Returns:
        Tuple of:
        - unique_labels: List of unique labels (order preserved by first appearance)
        - position_map: Dict mapping each unique label to list of original indices

    Example:
        >>> labels = ["Invoice No", "Date", "Invoice No", "Total"]
        >>> unique, pos_map = _deduplicate_labels(labels)
        >>> print(unique)
        ['Invoice No', 'Date', 'Total']
        >>> print(pos_map)
        {'Invoice No': [0, 2], 'Date': [1], 'Total': [3]}
    """
    unique_labels: list[str] = []
    position_map: dict[str, list[int]] = {}

    for idx, label in enumerate(labels):
        if label not in position_map:
            unique_labels.append(label)
            position_map[label] = [idx]
        else:
            position_map[label].append(idx)

    logger.debug(f"Deduplicated {len(labels)} labels to {len(unique_labels)} unique labels")

    return unique_labels, position_map


def translate_labels(
    ai_provider: AIProvider,
    labels: list[str],
    source_language: str | None = None,
    target_language: str = DEFAULT_TARGET_LANGUAGE,
) -> list[TranslatedLabel]:
    """
    Translate field labels using AI provider.

    This function takes a list of labels (which may contain duplicates and non-English
    text) and translates them using the provided AI provider. It automatically
    deduplicates labels to minimize API calls and handles partial failures gracefully.

    Behavior:
    1. Validate inputs (empty list check)
    2. Deduplicate labels internally (efficiency)
    3. Loop over unique labels:
       - Call ai_provider.translate_text() for each
       - Handle individual failures (fallback to original)
    4. Map results back to original positions
    5. Log summary statistics

    Args:
        ai_provider: Configured AIProvider instance
        labels: List of labels to translate (may contain duplicates)
        source_language: Explicit source language code (e.g., "ja", "zh").
                        If None, AI provider will auto-detect.
        target_language: Target language code (default: "en")

    Returns:
        List of TranslatedLabel objects (same order/length as input)

    Raises:
        AIProviderError: If provider request fails completely
        TranslationError: For critical translation failures

    Example:
        >>> from template_sense.ai_providers.factory import get_ai_provider
        >>> ai_provider = get_ai_provider()
        >>> labels = ["請求書番号", "AWB NO", "受取人"]
        >>> translations = translate_labels(ai_provider, labels)
        >>> for t in translations:
        ...     print(f"{t.original_text} → {t.translated_text}")
        請求書番号 → invoice number
        AWB NO → air waybill number
        受取人 → consignee
    """
    # Validate inputs
    if not labels:
        logger.debug("Empty label list provided for translation")
        return []

    logger.debug(
        f"Starting translation of {len(labels)} labels using {ai_provider.provider_name} "
        f"(source: {source_language or 'auto-detect'}, target: {target_language})"
    )

    # Deduplicate labels to reduce API calls
    unique_labels, position_map = _deduplicate_labels(labels)

    # Translate unique labels
    translations_map: dict[str, TranslatedLabel] = {}
    successful_count = 0
    failed_count = 0

    for label in unique_labels:
        try:
            # Call AI provider to translate text
            translated_text = ai_provider.translate_text(
                text=label,
                source_lang=source_language or "auto",  # "auto" for auto-detection
                target_lang=target_language,
            )

            # Create TranslatedLabel object
            translations_map[label] = TranslatedLabel(
                original_text=label,
                translated_text=translated_text,
                detected_source_language=source_language,  # Will be None if auto-detect
                target_language=target_language,
                model_confidence=None,  # Provider may not return confidence
                metadata={"provider": ai_provider.provider_name},
            )

            successful_count += 1
            logger.debug(f"Successfully translated: '{label}' → '{translated_text}'")

        except AIProviderError as e:
            # Log warning and fallback to original text
            logger.warning(
                f"Translation failed for label '{label}': {e.error_details}. "
                f"Using original text as fallback."
            )
            translations_map[label] = TranslatedLabel(
                original_text=label,
                translated_text=label,  # Fallback to original
                detected_source_language=source_language,
                target_language=target_language,
                model_confidence=None,
                metadata={
                    "provider": ai_provider.provider_name,
                    "error": "Translation failed, using original text",
                },
            )
            failed_count += 1

        except Exception as e:
            # Catch unexpected errors
            logger.warning(
                f"Unexpected error translating label '{label}': {str(e)}. "
                f"Using original text as fallback."
            )
            translations_map[label] = TranslatedLabel(
                original_text=label,
                translated_text=label,  # Fallback to original
                detected_source_language=source_language,
                target_language=target_language,
                model_confidence=None,
                metadata={
                    "provider": ai_provider.provider_name,
                    "error": f"Unexpected error: {str(e)}",
                },
            )
            failed_count += 1

    # Map results back to original positions
    result: list[TranslatedLabel] = []
    for label in labels:
        if label in translations_map:
            result.append(translations_map[label])
        else:
            # This should never happen due to our deduplication logic,
            # but handle it defensively
            logger.error(f"Label '{label}' missing from translations_map. Using fallback.")
            result.append(
                TranslatedLabel(
                    original_text=label,
                    translated_text=label,
                    detected_source_language=source_language,
                    target_language=target_language,
                    model_confidence=None,
                    metadata={"error": "Missing from translation results"},
                )
            )

    # Log summary statistics
    logger.info(
        f"Translation complete: {successful_count} successful, {failed_count} failed "
        f"(total unique: {len(unique_labels)}, total labels: {len(labels)})"
    )

    return result


__all__ = ["TranslatedLabel", "translate_labels"]
