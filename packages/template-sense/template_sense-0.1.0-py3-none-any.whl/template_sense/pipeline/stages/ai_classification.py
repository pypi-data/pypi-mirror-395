"""
AIClassificationStage: Performs AI-based classification of fields and line items.

This stage orchestrates three AI classification sub-tasks:
1. Header field classification
2. Table column classification
3. Line item extraction

All three use error recovery to handle AI provider failures gracefully.
"""

import logging

from template_sense.ai.header_classification import classify_header_fields
from template_sense.ai.line_item_extraction import extract_line_items
from template_sense.ai.table_column_classification import classify_table_columns
from template_sense.errors import AIProviderError
from template_sense.pipeline.stages.base import PipelineContext, PipelineStage
from template_sense.recovery.error_recovery import RecoveryEvent, RecoverySeverity

logger = logging.getLogger(__name__)


class AIClassificationStage(PipelineStage):
    """
    Stage 6: AI-based classification.

    Performs three AI classification tasks:
    - Header fields (context.classified_headers)
    - Table columns (context.classified_columns)
    - Line items (context.extracted_line_items)

    Uses error recovery to continue processing if individual tasks fail.
    """

    def execute(self, context: PipelineContext) -> PipelineContext:
        """Execute AI classification stage."""
        logger.info("Stage 6: AI classification")

        if context.ai_provider is None or context.ai_payload is None:
            logger.error("AI provider or payload not set in context")
            # This should not happen if previous stages ran correctly
            return context

        # Classify header fields
        logger.info("Stage 6a: Classifying header fields")
        try:
            context.classified_headers = classify_header_fields(
                context.ai_provider, context.ai_payload
            )
            logger.info("Classified %d header fields", len(context.classified_headers))
        except AIProviderError as e:
            logger.error("Header classification failed: %s", str(e))
            context.recovery_events.append(
                RecoveryEvent(
                    severity=RecoverySeverity.ERROR,
                    stage="ai_classification",
                    message=f"Header classification failed: {str(e)}",
                    metadata={"error_type": "AIProviderError"},
                )
            )

        # Classify table columns
        logger.info("Stage 6b: Classifying table columns")
        try:
            context.classified_columns = classify_table_columns(
                context.ai_provider, context.ai_payload
            )
            logger.info("Classified %d table columns", len(context.classified_columns))
        except AIProviderError as e:
            logger.error("Column classification failed: %s", str(e))
            context.recovery_events.append(
                RecoveryEvent(
                    severity=RecoverySeverity.ERROR,
                    stage="ai_classification",
                    message=f"Column classification failed: {str(e)}",
                    metadata={"error_type": "AIProviderError"},
                )
            )

        # Extract line items
        logger.info("Stage 6c: Extracting line items")
        try:
            context.extracted_line_items = extract_line_items(
                context.ai_provider, context.ai_payload
            )
            logger.info("Extracted %d line items", len(context.extracted_line_items))
        except AIProviderError as e:
            logger.error("Line item extraction failed: %s", str(e))
            context.recovery_events.append(
                RecoveryEvent(
                    severity=RecoverySeverity.ERROR,
                    stage="ai_classification",
                    message=f"Line item extraction failed: {str(e)}",
                    metadata={"error_type": "AIProviderError"},
                )
            )

        logger.info("Stage 6: AI classification complete")
        return context


__all__ = ["AIClassificationStage"]
