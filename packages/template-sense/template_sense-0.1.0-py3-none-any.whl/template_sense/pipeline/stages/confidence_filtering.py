"""
ConfidenceFilteringStage: Filters results by confidence thresholds.

This stage generates recovery events for fields that fall below confidence
thresholds (AI confidence and fuzzy match score).
"""

import logging

from template_sense.constants import MIN_AI_CONFIDENCE_WARNING, MIN_FUZZY_MATCH_WARNING
from template_sense.pipeline.stages.base import PipelineContext, PipelineStage
from template_sense.recovery.error_recovery import (
    filter_by_ai_confidence,
    filter_by_fuzzy_match_score,
)

logger = logging.getLogger(__name__)


class ConfidenceFilteringStage(PipelineStage):
    """
    Stage 9: Confidence filtering.

    Filters classified fields and match results by confidence thresholds,
    generating recovery events for low-confidence items. Appends events to
    context.recovery_events.
    """

    def execute(self, context: PipelineContext) -> PipelineContext:
        """Execute confidence filtering stage."""
        logger.info("Stage 9: Filtering by confidence thresholds")

        # Filter headers by AI confidence
        _, header_ai_events = filter_by_ai_confidence(
            fields=context.classified_headers,
            min_confidence=MIN_AI_CONFIDENCE_WARNING,
        )
        context.recovery_events.extend(header_ai_events)
        logger.info("Generated %d AI confidence warnings for headers", len(header_ai_events))

        # Filter columns by AI confidence
        _, column_ai_events = filter_by_ai_confidence(
            fields=context.classified_columns,
            min_confidence=MIN_AI_CONFIDENCE_WARNING,
        )
        context.recovery_events.extend(column_ai_events)
        logger.info("Generated %d AI confidence warnings for columns", len(column_ai_events))

        # Filter header matches by fuzzy score
        _, header_fuzzy_events = filter_by_fuzzy_match_score(
            fields=context.header_match_results,
            min_score=MIN_FUZZY_MATCH_WARNING,
        )
        context.recovery_events.extend(header_fuzzy_events)
        logger.info("Generated %d fuzzy match warnings for headers", len(header_fuzzy_events))

        # Filter column matches by fuzzy score
        _, column_fuzzy_events = filter_by_fuzzy_match_score(
            fields=context.column_match_results,
            min_score=MIN_FUZZY_MATCH_WARNING,
        )
        context.recovery_events.extend(column_fuzzy_events)
        logger.info("Generated %d fuzzy match warnings for columns", len(column_fuzzy_events))

        logger.info("Stage 9: Confidence filtering complete")
        return context


__all__ = ["ConfidenceFilteringStage"]
