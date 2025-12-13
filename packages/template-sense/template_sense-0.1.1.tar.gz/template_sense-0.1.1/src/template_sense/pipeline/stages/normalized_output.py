"""
NormalizedOutputStage: Builds normalized JSON output from canonical template.

This stage converts the canonical template into the normalized JSON structure
that will be returned to the caller.
"""

import logging

from template_sense.errors import ExtractionError
from template_sense.output.normalized_output_builder import build_normalized_output
from template_sense.pipeline.stages.base import PipelineContext, PipelineStage

logger = logging.getLogger(__name__)


class NormalizedOutputStage(PipelineStage):
    """
    Stage 11: Normalized output building.

    Converts the canonical template into normalized JSON output.
    Sets context.normalized_output.

    Raises:
        ExtractionError: If output building fails
    """

    def execute(self, context: PipelineContext) -> PipelineContext:
        """Execute normalized output building stage."""
        logger.info("Stage 11: Building normalized output")

        if context.canonical_template is None:
            raise ExtractionError(
                extraction_type="normalized_output",
                reason="Canonical template not set in context",
            )

        try:
            context.normalized_output = build_normalized_output(context.canonical_template)
            logger.info("Normalized output built successfully")
        except Exception as e:
            logger.error("Normalized output building failed: %s", str(e))
            if context.workbook:
                context.workbook.close()
            raise ExtractionError(
                extraction_type="normalized_output",
                reason=f"Failed to build normalized output: {str(e)}",
            ) from e

        logger.info("Stage 11: Normalized output building complete")
        return context


__all__ = ["NormalizedOutputStage"]
