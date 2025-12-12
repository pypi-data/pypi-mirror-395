"""
FileLoadingStage: Loads Excel workbook and selects sheet.

This stage loads the Excel file into memory and selects the first visible
sheet for processing.
"""

import logging

from template_sense.adapters.excel_adapter import ExcelWorkbook
from template_sense.errors import ExtractionError, FileValidationError
from template_sense.file_loader import load_excel_file
from template_sense.pipeline.stages.base import PipelineContext, PipelineStage

logger = logging.getLogger(__name__)


class FileLoadingStage(PipelineStage):
    """
    Stage 2: Load Excel file and select sheet.

    Loads the workbook and selects the first visible sheet for processing.
    Sets context.workbook and context.sheet_name.

    Raises:
        FileValidationError: If file cannot be loaded
        ExtractionError: If no visible sheets are found
    """

    def execute(self, context: PipelineContext) -> PipelineContext:
        """Execute file loading stage."""
        logger.info("Stage 2: Loading Excel file")

        # Load workbook
        try:
            raw_workbook = load_excel_file(context.file_path)
            context.workbook = ExcelWorkbook(raw_workbook)
            logger.info("Workbook loaded successfully")
        except FileValidationError:
            logger.error("File validation failed during loading")
            raise
        except Exception as e:
            logger.error("Unexpected error loading workbook: %s", str(e))
            raise FileValidationError(
                reason=f"Failed to load workbook: {str(e)}",
                file_path=str(context.file_path),
            ) from e

        # Select first visible sheet
        try:
            context.sheet_name = self._select_sheet(context.workbook)
        except ExtractionError:
            logger.error("No visible sheets found")
            context.workbook.close()
            raise

        logger.info("Stage 2: File loading complete")
        return context

    def _select_sheet(self, workbook: ExcelWorkbook) -> str:
        """
        Select the first visible sheet from the workbook.

        Args:
            workbook: ExcelWorkbook instance

        Returns:
            Name of the first visible sheet

        Raises:
            ExtractionError: If no visible sheets are found
        """
        sheet_names = workbook.get_sheet_names()

        if not sheet_names:
            raise ExtractionError(
                extraction_type="sheet_selection",
                reason="No visible sheets found in workbook",
            )

        selected_sheet = sheet_names[0]
        logger.info("Selected sheet: '%s' (first visible sheet)", selected_sheet)
        return selected_sheet


__all__ = ["FileLoadingStage"]
