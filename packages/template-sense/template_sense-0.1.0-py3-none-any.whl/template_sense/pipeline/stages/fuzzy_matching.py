"""
FuzzyMatchingStage: Performs fuzzy matching to canonical field dictionary.

This stage matches translated labels from headers and columns to the canonical
field dictionary using fuzzy matching algorithms.
"""

import logging

from template_sense.ai.translation import TranslatedLabel
from template_sense.constants import DEFAULT_AUTO_MAPPING_THRESHOLD, DEFAULT_TARGET_LANGUAGE
from template_sense.mapping.fuzzy_field_matching import match_fields
from template_sense.pipeline.stages.base import PipelineContext, PipelineStage
from template_sense.recovery.error_recovery import RecoveryEvent, RecoverySeverity

logger = logging.getLogger(__name__)


def get_translated_labels(
    items: list,
    translation_map: dict[str, TranslatedLabel],
    label_attr: str = "raw_label",
) -> list[TranslatedLabel]:
    """
    Get translated labels with fallback for missing translations.

    Args:
        items: List of classified items (headers or columns)
        translation_map: Map of original text to TranslatedLabel
        label_attr: Attribute name to extract from items (default: "raw_label")

    Returns:
        List of TranslatedLabel objects with fallback for missing translations
    """
    result = []
    for item in items:
        label = getattr(item, label_attr)
        if not label:
            continue

        translated = translation_map.get(
            label,
            TranslatedLabel(
                original_text=label,
                translated_text=label,
                target_language=DEFAULT_TARGET_LANGUAGE,
            ),
        )
        result.append(translated)
    return result


class FuzzyMatchingStage(PipelineStage):
    """
    Stage 8: Fuzzy matching.

    Performs fuzzy matching of translated labels against the canonical field
    dictionary. Sets context.header_match_results and context.column_match_results.

    Uses error recovery if matching fails.
    """

    def execute(self, context: PipelineContext) -> PipelineContext:
        """Execute fuzzy matching stage."""
        logger.info("Stage 8: Performing fuzzy matching")

        if context.ai_provider is None:
            logger.warning("AI provider not set, skipping fuzzy matching")
            return context

        # Match header fields
        header_translated_labels = get_translated_labels(
            items=context.classified_headers, translation_map=context.translation_map
        )

        if header_translated_labels:
            try:
                context.header_match_results = match_fields(
                    translated_labels=header_translated_labels,
                    field_dictionary=context.header_field_dictionary,
                    threshold=DEFAULT_AUTO_MAPPING_THRESHOLD,
                    ai_provider=context.ai_provider,  # Pass AI provider for semantic matching
                )
                logger.info(
                    "Matched %d header fields (threshold=%.1f)",
                    len(context.header_match_results),
                    DEFAULT_AUTO_MAPPING_THRESHOLD,
                )
            except Exception as e:
                logger.error("Header fuzzy matching failed: %s", str(e))
                context.recovery_events.append(
                    RecoveryEvent(
                        severity=RecoverySeverity.ERROR,
                        stage="fuzzy_matching",
                        message=f"Header fuzzy matching failed: {str(e)}",
                        metadata={"error_type": type(e).__name__},
                    )
                )

        # Match column fields
        column_translated_labels = get_translated_labels(
            items=context.classified_columns, translation_map=context.translation_map
        )

        if column_translated_labels:
            try:
                context.column_match_results = match_fields(
                    translated_labels=column_translated_labels,
                    field_dictionary=context.column_field_dictionary,
                    threshold=DEFAULT_AUTO_MAPPING_THRESHOLD,
                    ai_provider=context.ai_provider,  # Pass AI provider for semantic matching
                )
                logger.info(
                    "Matched %d column fields (threshold=%.1f)",
                    len(context.column_match_results),
                    DEFAULT_AUTO_MAPPING_THRESHOLD,
                )
            except Exception as e:
                logger.error("Column fuzzy matching failed: %s", str(e))
                context.recovery_events.append(
                    RecoveryEvent(
                        severity=RecoverySeverity.ERROR,
                        stage="fuzzy_matching",
                        message=f"Column fuzzy matching failed: {str(e)}",
                        metadata={"error_type": type(e).__name__},
                    )
                )

        logger.info("Stage 8: Fuzzy matching complete")
        return context


__all__ = ["FuzzyMatchingStage"]
