"""
AIClassificationStage: Performs AI-based classification of fields and line items.

This stage uses batch classification to combine three AI tasks into a single API call:
1. Header field classification
2. Table column classification
3. Line item extraction

Uses error recovery to handle AI provider failures gracefully.
"""

import logging
from typing import Any

from template_sense.ai.header_classification import (
    ClassifiedHeaderField,
    _parse_header_field,
)
from template_sense.ai.line_item_extraction import (
    ExtractedLineItem,
    _parse_line_item,
)
from template_sense.ai.table_column_classification import (
    ClassifiedTableColumn,
    _parse_table_column,
)
from template_sense.errors import AIProviderError
from template_sense.pipeline.stages.base import PipelineContext, PipelineStage
from template_sense.recovery.error_recovery import RecoveryEvent, RecoverySeverity

logger = logging.getLogger(__name__)


class AIClassificationStage(PipelineStage):
    """
    Stage 6: AI-based classification (batch mode).

    Performs three AI classification tasks in a single batch API call:
    - Header fields (context.classified_headers)
    - Table columns (context.classified_columns)
    - Line items (context.extracted_line_items)

    Uses error recovery to continue processing if the batch call fails.
    """

    def execute(self, context: PipelineContext) -> PipelineContext:
        """Execute AI classification stage using batch classification."""
        logger.info("Stage 6: AI batch classification")

        if context.ai_provider is None or context.ai_payload is None:
            logger.error("AI provider or payload not set in context")
            # This should not happen if previous stages ran correctly
            return context

        # Execute batch classification
        try:
            logger.info("Calling batch classify_all_fields")
            batch_results = context.ai_provider.classify_all_fields(
                payload=context.ai_payload,
                contexts=["headers", "columns", "line_items"],
            )
            logger.info("Batch classification completed successfully")

            # Parse headers
            context.classified_headers = self._parse_headers(batch_results.get("headers", []))
            logger.info("Classified %d header fields", len(context.classified_headers))

            # Parse columns
            context.classified_columns = self._parse_columns(batch_results.get("columns", []))
            logger.info("Classified %d table columns", len(context.classified_columns))

            # Parse line items
            context.extracted_line_items = self._parse_line_items(
                batch_results.get("line_items", [])
            )
            logger.info("Extracted %d line items", len(context.extracted_line_items))

        except AIProviderError as e:
            logger.error("Batch classification failed: %s", str(e))
            context.recovery_events.append(
                RecoveryEvent(
                    severity=RecoverySeverity.ERROR,
                    stage="ai_classification",
                    message=f"Batch classification failed: {str(e)}",
                    metadata={"error_type": "AIProviderError"},
                )
            )

        logger.info("Stage 6: AI classification complete")
        return context

    def _parse_headers(self, headers_list: list[dict[str, Any]]) -> list[ClassifiedHeaderField]:
        """
        Parse headers list from batch response.

        Args:
            headers_list: List of header field dicts from AI response

        Returns:
            List of ClassifiedHeaderField instances
        """
        classified = []
        for i, header_dict in enumerate(headers_list):
            try:
                field = _parse_header_field(header_dict, i)
                classified.append(field)
            except (KeyError, TypeError, ValueError) as e:
                logger.warning("Failed to parse header field at index %d: %s", i, str(e))
                # Continue processing remaining items
        return classified

    def _parse_columns(self, columns_list: list[dict[str, Any]]) -> list[ClassifiedTableColumn]:
        """
        Parse columns list from batch response.

        Args:
            columns_list: List of column dicts from AI response

        Returns:
            List of ClassifiedTableColumn instances
        """
        classified = []
        for i, column_dict in enumerate(columns_list):
            try:
                column = _parse_table_column(column_dict, i)
                classified.append(column)
            except (KeyError, TypeError, ValueError) as e:
                logger.warning("Failed to parse table column at index %d: %s", i, str(e))
                # Continue processing remaining items
        return classified

    def _parse_line_items(self, line_items_list: list[dict[str, Any]]) -> list[ExtractedLineItem]:
        """
        Parse line items list from batch response.

        Args:
            line_items_list: List of line item dicts from AI response

        Returns:
            List of ExtractedLineItem instances
        """
        extracted = []
        for i, item_dict in enumerate(line_items_list):
            try:
                item = _parse_line_item(item_dict, i)
                extracted.append(item)
            except (KeyError, TypeError, ValueError) as e:
                logger.warning("Failed to parse line item at index %d: %s", i, str(e))
                # Continue processing remaining items
        return extracted


__all__ = ["AIClassificationStage"]
