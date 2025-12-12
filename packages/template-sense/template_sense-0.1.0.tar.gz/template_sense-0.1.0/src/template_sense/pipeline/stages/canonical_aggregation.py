"""
CanonicalAggregationStage: Builds canonical template from classified results.

This stage aggregates all classification, translation, and matching results
into a canonical template structure.
"""

import logging

from template_sense.errors import ExtractionError
from template_sense.output.canonical_aggregator import (
    CanonicalTemplateInput,
    build_canonical_template,
)
from template_sense.pipeline.stages.base import PipelineContext, PipelineStage

logger = logging.getLogger(__name__)


class CanonicalAggregationStage(PipelineStage):
    """
    Stage 10: Canonical aggregation.

    Aggregates all classification and matching results into a canonical template.
    Sets context.canonical_template.

    Raises:
        ExtractionError: If canonical aggregation fails
    """

    def execute(self, context: PipelineContext) -> PipelineContext:
        """Execute canonical aggregation stage."""
        logger.info("Stage 10: Building canonical template")

        if context.sheet_name is None:
            raise ExtractionError(
                extraction_type="canonical_aggregation",
                reason="Sheet name not set in context",
            )

        try:
            # Note: build_canonical_template expects dataclasses for candidate blocks
            # For now, we pass empty lists as the conversion layer isn't needed yet
            context.canonical_template = build_canonical_template(
                CanonicalTemplateInput(
                    sheet_name=context.sheet_name,
                    header_candidate_blocks=[],  # Will be populated from sheet_summary in future
                    table_candidate_blocks=[],  # Will be populated from sheet_summary in future
                    classified_headers=context.classified_headers,
                    classified_columns=context.classified_columns,
                    extracted_line_items=context.extracted_line_items,
                    header_match_results=context.header_match_results,
                    column_match_results=context.column_match_results,
                )
            )

            logger.info("Canonical template built successfully")

        except Exception as e:
            logger.error("Canonical aggregation failed: %s", str(e))
            if context.workbook:
                context.workbook.close()
            raise ExtractionError(
                extraction_type="canonical_aggregation",
                reason=f"Failed to build canonical template: {str(e)}",
            ) from e

        logger.info("Stage 10: Canonical aggregation complete")
        return context


__all__ = ["CanonicalAggregationStage"]
