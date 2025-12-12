"""
MetadataStage: Builds pipeline metadata and closes workbook.

This stage calculates timing, builds metadata, closes the workbook, and
prepares the final context for return.
"""

import logging
import time

from template_sense.constants import PIPELINE_VERSION
from template_sense.pipeline.stages.base import PipelineContext, PipelineStage

logger = logging.getLogger(__name__)


class MetadataStage(PipelineStage):
    """
    Stage 12: Metadata building.

    Calculates pipeline timing, builds metadata dictionary, and closes the workbook.
    Sets context.metadata and closes context.workbook.
    """

    def execute(self, context: PipelineContext) -> PipelineContext:
        """Execute metadata building stage."""
        logger.info("Stage 12: Building metadata and preparing final output")

        # Calculate timing
        end_time = time.perf_counter()
        timing_ms = int((end_time - context.start_time) * 1000)

        # Build metadata (only essential fields for Tako)
        context.metadata = {
            "sheet_name": context.sheet_name,
        }

        # Log internal metrics (not exposed in API response)
        if context.ai_provider:
            logger.debug(
                "Built pipeline metadata: sheet_name=%s, ai_provider=%s, ai_model=%s, "
                "pipeline_version=%s, timing_ms=%d (internal only)",
                context.sheet_name,
                context.ai_provider.config.provider,
                context.ai_provider.config.model or "default",
                PIPELINE_VERSION,
                timing_ms,
            )
        else:
            logger.debug(
                "Built pipeline metadata: sheet_name=%s, pipeline_version=%s, "
                "timing_ms=%d (internal only)",
                context.sheet_name,
                PIPELINE_VERSION,
                timing_ms,
            )

        # Close workbook
        if context.workbook:
            context.workbook.close()
            logger.debug("Workbook closed")

        logger.info("=== Pipeline completed successfully ===")
        logger.info("Total time: %d ms", timing_ms)
        logger.info("Recovery events: %d", len(context.recovery_events))
        logger.info("Stage 12: Metadata building complete")

        return context


__all__ = ["MetadataStage"]
