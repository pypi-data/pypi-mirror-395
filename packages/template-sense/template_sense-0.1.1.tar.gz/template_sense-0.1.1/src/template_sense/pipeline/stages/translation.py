"""
TranslationStage: Translates labels to target language.

This stage collects all labels from classified headers and columns, translates
them to the target language (English by default), and builds a translation map.
"""

import logging

from template_sense.ai.translation import TranslatedLabel, translate_labels
from template_sense.constants import DEFAULT_TARGET_LANGUAGE
from template_sense.errors import AIProviderError
from template_sense.pipeline.stages.base import PipelineContext, PipelineStage
from template_sense.recovery.error_recovery import RecoveryEvent, RecoverySeverity

logger = logging.getLogger(__name__)


class TranslationStage(PipelineStage):
    """
    Stage 7: Translate labels.

    Collects all labels from classified headers and columns, translates them
    to the target language, and builds a translation map. Sets context.translation_map.

    Uses error recovery if translation fails (falls back to original text).
    """

    def execute(self, context: PipelineContext) -> PipelineContext:
        """Execute translation stage."""
        logger.info("Stage 7: Translating labels")

        if context.ai_provider is None:
            logger.warning("AI provider not set, skipping translation")
            return context

        # Collect all labels from headers and columns
        all_labels: list[str] = []

        for header in context.classified_headers:
            if header.raw_label:
                all_labels.append(header.raw_label)

        for column in context.classified_columns:
            if column.raw_label:
                all_labels.append(column.raw_label)

        # Deduplicate labels
        unique_labels = list(set(all_labels))
        logger.info("Collected %d unique labels for translation", len(unique_labels))

        # Translate if there are labels
        if unique_labels:
            try:
                translated_labels = translate_labels(
                    ai_provider=context.ai_provider,
                    labels=unique_labels,
                    source_language=None,  # Auto-detect
                    target_language=DEFAULT_TARGET_LANGUAGE,
                )

                # Build translation map
                for translated in translated_labels:
                    context.translation_map[translated.original_text] = translated

                logger.info("Translated %d labels", len(translated_labels))

            except AIProviderError as e:
                logger.error("Translation failed: %s", str(e))
                context.recovery_events.append(
                    RecoveryEvent(
                        severity=RecoverySeverity.ERROR,
                        stage="translation",
                        message=f"Translation failed: {str(e)}",
                        metadata={"error_type": "AIProviderError"},
                    )
                )

                # Build fallback translation map (use original text as translated)
                for label in unique_labels:
                    context.translation_map[label] = TranslatedLabel(
                        original_text=label,
                        translated_text=label,
                        target_language=DEFAULT_TARGET_LANGUAGE,
                    )

                logger.info("Using fallback translations (original text)")

        logger.info("Stage 7: Translation complete")
        return context


__all__ = ["TranslationStage"]
