"""
AIPayloadBuildingStage: Constructs the AI payload for classification.

This stage builds the payload that will be sent to the AI provider for
classification, including grid context for adjacent cells.
"""

import logging

from template_sense.ai_payload_schema import build_ai_payload
from template_sense.errors import ExtractionError
from template_sense.pipeline.stages.base import PipelineContext, PipelineStage

logger = logging.getLogger(__name__)


class AIPayloadBuildingStage(PipelineStage):
    """
    Stage 5: Build AI payload.

    Constructs the payload for AI classification including sheet summary,
    field dictionary, and grid for adjacent cell context. Sets context.ai_payload.

    Raises:
        ExtractionError: If payload construction fails
    """

    def execute(self, context: PipelineContext) -> PipelineContext:
        """Execute AI payload building stage."""
        logger.info("Stage 5: Building AI payload")

        if context.sheet_summary is None or context.grid is None:
            raise ExtractionError(
                extraction_type="ai_payload",
                reason="Sheet summary or grid not set in context",
            )

        try:
            # Build structured field dictionary for AI payload
            structured_field_dict = {
                "headers": context.header_field_dictionary,
                "columns": context.column_field_dictionary,
            }

            context.ai_payload = build_ai_payload(
                sheet_summary=context.sheet_summary,
                field_dictionary=structured_field_dict,
                grid=context.grid,  # Pass grid for adjacent cell context (BAT-53)
            )
            logger.info("AI payload built successfully")
        except Exception as e:
            logger.error("Failed to build AI payload: %s", str(e))
            if context.workbook:
                context.workbook.close()
            raise ExtractionError(
                extraction_type="ai_payload",
                reason=f"Failed to build AI payload: {str(e)}",
            ) from e

        logger.info("Stage 5: AI payload building complete")
        return context


__all__ = ["AIPayloadBuildingStage"]
