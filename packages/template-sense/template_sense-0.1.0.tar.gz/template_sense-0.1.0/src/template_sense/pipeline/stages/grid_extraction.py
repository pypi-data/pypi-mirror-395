"""
GridExtractionStage: Extracts grid data and builds sheet summary.

This stage extracts the raw grid from the selected sheet and performs heuristic
detection of headers and tables.
"""

import logging

from template_sense.errors import ExtractionError
from template_sense.extraction.sheet_extractor import extract_raw_grid
from template_sense.extraction.summary_builder import build_sheet_summary
from template_sense.pipeline.stages.base import PipelineContext, PipelineStage

logger = logging.getLogger(__name__)


class GridExtractionStage(PipelineStage):
    """
    Stage 3: Extract grid and build sheet summary.

    Extracts raw grid data from the sheet and performs heuristic detection
    of header blocks and table blocks. Sets context.grid and context.sheet_summary.

    Raises:
        ExtractionError: If grid extraction fails
    """

    def execute(self, context: PipelineContext) -> PipelineContext:
        """Execute grid extraction stage."""
        logger.info("Stage 3: Extracting grid from sheet '%s'", context.sheet_name)

        if context.workbook is None or context.sheet_name is None:
            raise ExtractionError(
                extraction_type="grid_extraction",
                reason="Workbook or sheet_name not set in context",
            )

        try:
            # Build sheet summary (includes heuristic detection)
            context.sheet_summary = build_sheet_summary(context.workbook, context.sheet_name)
            logger.info(
                "Sheet summary built: %d header blocks, %d table blocks",
                len(context.sheet_summary.get("header_blocks", [])),
                len(context.sheet_summary.get("table_blocks", [])),
            )

            # Extract raw grid for adjacent cell context (BAT-53)
            context.grid = extract_raw_grid(context.workbook, context.sheet_name)
            logger.debug("Extracted grid for adjacent cell context (%d rows)", len(context.grid))

        except ExtractionError:
            logger.error("Grid extraction failed")
            if context.workbook:
                context.workbook.close()
            raise

        logger.info("Stage 3: Grid extraction complete")
        return context


__all__ = ["GridExtractionStage"]
