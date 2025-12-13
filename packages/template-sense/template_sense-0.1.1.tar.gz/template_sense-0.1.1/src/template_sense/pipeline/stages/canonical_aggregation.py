"""
CanonicalAggregationStage: Builds canonical template from classified results.

This stage aggregates all classification, translation, and matching results
into a canonical template structure.
"""

import logging
from typing import Any

from template_sense.errors import ExtractionError
from template_sense.extraction.header_candidates import HeaderCandidateBlock
from template_sense.extraction.table_candidates import TableCandidateBlock
from template_sense.output.canonical_aggregator import (
    CanonicalTemplateInput,
    build_canonical_template,
)
from template_sense.pipeline.stages.base import PipelineContext, PipelineStage

logger = logging.getLogger(__name__)


def _convert_header_blocks(header_blocks_dict: list[dict[str, Any]]) -> list[HeaderCandidateBlock]:
    """
    Convert header block dicts from sheet_summary to HeaderCandidateBlock dataclasses.

    Args:
        header_blocks_dict: List of header block dictionaries from sheet_summary

    Returns:
        List of HeaderCandidateBlock dataclass instances
    """
    blocks = []
    for block_dict in header_blocks_dict:
        block = HeaderCandidateBlock(
            row_start=block_dict["row_start"],
            row_end=block_dict["row_end"],
            col_start=block_dict["col_start"],
            col_end=block_dict["col_end"],
            content=block_dict["content"],
            label_value_pairs=block_dict.get("label_value_pairs", []),
            score=block_dict["score"],
            detected_pattern=block_dict["detected_pattern"],
        )
        blocks.append(block)
    return blocks


def _convert_table_blocks(table_blocks_dict: list[dict[str, Any]]) -> list[TableCandidateBlock]:
    """
    Convert table block dicts from sheet_summary to TableCandidateBlock dataclasses.

    Args:
        table_blocks_dict: List of table block dictionaries from sheet_summary

    Returns:
        List of TableCandidateBlock dataclass instances
    """
    blocks = []
    for block_dict in table_blocks_dict:
        block = TableCandidateBlock(
            row_start=block_dict["row_start"],
            row_end=block_dict["row_end"],
            col_start=block_dict["col_start"],
            col_end=block_dict["col_end"],
            content=block_dict["content"],
            score=block_dict["score"],
            detected_pattern=block_dict["detected_pattern"],
        )
        blocks.append(block)
    return blocks


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
            # Extract blocks from sheet_summary
            sheet_summary = context.sheet_summary or {}
            header_blocks_dict = sheet_summary.get("header_blocks", [])
            table_blocks_dict = sheet_summary.get("table_blocks", [])

            # Convert dicts to dataclasses
            header_candidate_blocks = _convert_header_blocks(header_blocks_dict)
            table_candidate_blocks = _convert_table_blocks(table_blocks_dict)

            logger.debug(
                "Converted %d header blocks and %d table blocks from sheet_summary",
                len(header_candidate_blocks),
                len(table_candidate_blocks),
            )

            context.canonical_template = build_canonical_template(
                CanonicalTemplateInput(
                    sheet_name=context.sheet_name,
                    header_candidate_blocks=header_candidate_blocks,
                    table_candidate_blocks=table_candidate_blocks,
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
