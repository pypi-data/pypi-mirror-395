"""
Canonical Template Mapping Aggregator for Template Sense.

This module merges all pipeline outputs (extraction, AI classification, translation,
and fuzzy matching) into a single unified canonical template representation that
Tako can consume.

Architecture Position: Extraction → AI → Translation → Mapping → **AGGREGATION** → Output

This module does NOT:
- Call any AI services
- Perform additional translation or fuzzy matching
- Make external API calls

This module DOES:
- Join classified components with match results
- Preserve all metadata (scores, coordinates, indices)
- Compute summary statistics
- Provide deterministic, reproducible output

Functions:
    build_canonical_template: Main aggregation function that merges all pipeline outputs

Usage Example:
    from template_sense.output.canonical_aggregator import build_canonical_template

    canonical_template = build_canonical_template(
        sheet_name="Sheet1",
        header_candidate_blocks=header_blocks,
        table_candidate_blocks=table_blocks,
        classified_headers=classified_headers,
        classified_columns=classified_columns,
        extracted_line_items=line_items,
        header_match_results=header_matches,
        column_match_results=column_matches,
    )
"""

import logging
from dataclasses import dataclass, field
from typing import Any

from template_sense.ai.header_classification import ClassifiedHeaderField
from template_sense.ai.line_item_extraction import ExtractedLineItem
from template_sense.ai.table_column_classification import ClassifiedTableColumn
from template_sense.extraction.header_candidates import HeaderCandidateBlock
from template_sense.extraction.table_candidates import TableCandidateBlock
from template_sense.mapping.fuzzy_field_matching import FieldMatchResult

# Set up module logger
logger = logging.getLogger(__name__)


@dataclass
class CanonicalTemplateInput:
    """
    Input data for canonical template building.

    This dataclass aggregates all pipeline outputs needed to build a canonical
    template, replacing the 8-parameter function signature with a single
    structured object.

    Attributes:
        sheet_name: Name of the Excel sheet (required).
        header_candidate_blocks: Header regions detected by heuristics.
        table_candidate_blocks: Table regions detected by heuristics.
        classified_headers: Header fields classified by AI.
        classified_columns: Table columns classified by AI.
        extracted_line_items: Line items extracted by AI.
        header_match_results: Fuzzy matching results for headers.
        column_match_results: Fuzzy matching results for columns.
    """

    sheet_name: str
    header_candidate_blocks: list[HeaderCandidateBlock] = field(default_factory=list)
    table_candidate_blocks: list[TableCandidateBlock] = field(default_factory=list)
    classified_headers: list[ClassifiedHeaderField] = field(default_factory=list)
    classified_columns: list[ClassifiedTableColumn] = field(default_factory=list)
    extracted_line_items: list[ExtractedLineItem] = field(default_factory=list)
    header_match_results: list[FieldMatchResult] = field(default_factory=list)
    column_match_results: list[FieldMatchResult] = field(default_factory=list)


@dataclass
class CanonicalHeaderField:
    """
    Final merged header field with all metadata.

    This dataclass represents a fully processed header field that combines
    heuristic detection, AI classification, translation, and fuzzy matching results.

    Attributes:
        canonical_key: Matched canonical field key (e.g., "invoice_number").
                      None if no fuzzy match met the threshold.
        original_label: Original label text from template (may be non-English).
                       None if no clear label was detected.
        translated_label: English translation of the label.
                         None if no translation was performed (already English).
        value: Associated value from the template (can be any type).

        # Source tracking
        heuristic_block_index: Index of HeaderCandidateBlock this field came from.
                              None if field doesn't map to a specific block.
        ai_confidence: AI classification confidence score (0.0-1.0).
                      None if provider doesn't return confidence scores.
        fuzzy_match_score: Fuzzy matching confidence score (0.0-100.0).
                          None if no fuzzy match was performed.
        matched_variant: Specific dictionary variant that matched best
                        (e.g., "Invoice No" from variants list).
                        None if no match meets threshold.

        # Coordinates (1-based Excel convention)
        row_index: Row coordinate in original grid.
        col_index: Column coordinate in original grid.

        metadata: Optional provider-specific or additional metadata.
    """

    canonical_key: str | None
    original_label: str | None
    translated_label: str | None
    value: Any

    # Source tracking
    heuristic_block_index: int | None
    ai_confidence: float | None  # 0.0-1.0
    fuzzy_match_score: float | None  # 0.0-100.0
    matched_variant: str | None

    # Coordinates (1-based)
    row_index: int
    col_index: int

    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class CanonicalTableColumn:
    """
    Final merged table column with all metadata.

    This dataclass represents a fully processed table column that combines
    AI classification, translation, and fuzzy matching results.

    Attributes:
        canonical_key: Matched canonical field key (e.g., "product_name").
                      None if no fuzzy match met the threshold.
        original_label: Original column header text from template (may be non-English).
                       None if no clear header was detected.
        translated_label: English translation of the column header.
                         None if no translation was performed (already English).
        column_position: Column position within the table (0-based).
        sample_values: List of sample data values from this column for validation.

        # Source tracking
        ai_confidence: AI classification confidence score (0.0-1.0).
                      None if provider doesn't return confidence scores.
        fuzzy_match_score: Fuzzy matching confidence score (0.0-100.0).
                          None if no fuzzy match was performed.
        matched_variant: Specific dictionary variant that matched best.
                        None if no match meets threshold.

        # Coordinates (1-based Excel convention)
        row_index: Row coordinate of column header in original grid.
        col_index: Column coordinate in original grid.

        metadata: Optional provider-specific or additional metadata.
    """

    canonical_key: str | None
    original_label: str | None
    translated_label: str | None
    column_position: int  # 0-based within table
    sample_values: list[Any]

    # Source tracking
    ai_confidence: float | None  # 0.0-1.0
    fuzzy_match_score: float | None  # 0.0-100.0
    matched_variant: str | None

    # Coordinates (1-based)
    row_index: int
    col_index: int

    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class CanonicalLineItem:
    """
    Extracted line item with canonical column mappings.

    This dataclass represents a single row of data from a table, with values
    mapped to their canonical column keys.

    Attributes:
        row_index: Row coordinate in original grid (1-based Excel convention).
        line_number: Sequential line item number if present in the data.
                    None if no explicit line number column exists.
        columns: Dict mapping canonical_key → value.
                Keys are canonical column keys (e.g., "product_name", "quantity").
                Values can be any type (str, int, float, None).
        is_subtotal: Flag indicating if this row is a subtotal/summary row.
                    True for non-item rows (section totals, headers within table).
        ai_confidence: AI extraction confidence score (0.0-1.0).
                      None if provider doesn't return confidence scores.
        metadata: Optional provider-specific or additional metadata.
    """

    row_index: int  # 1-based
    line_number: int | None
    columns: dict[str, Any]  # canonical_key → value
    is_subtotal: bool
    ai_confidence: float | None  # 0.0-1.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class CanonicalTable:
    """
    A single table within the template.

    This dataclass represents a detected table region with all its columns
    and line items, fully processed and mapped to canonical keys.

    Attributes:
        table_block_index: Index of the TableCandidateBlock this table came from.

        # Coordinates (1-based Excel convention, inclusive)
        row_start: First row of table.
        row_end: Last row of table.
        col_start: First column of table.
        col_end: Last column of table.

        # Content
        columns: List of CanonicalTableColumn objects for this table.
        line_items: List of CanonicalLineItem objects extracted from this table.

        # Source metadata
        heuristic_score: Heuristic detection confidence score (0.0-1.0).
                        None if not available.
        detected_pattern: Description of heuristic detection pattern
                         (e.g., "numeric_density", "column_consistency").
                         None if not available.

        metadata: Optional additional metadata.
    """

    table_block_index: int

    # Coordinates (1-based, inclusive)
    row_start: int
    row_end: int
    col_start: int
    col_end: int

    # Content
    columns: list[CanonicalTableColumn]
    line_items: list[CanonicalLineItem]

    # Source metadata
    heuristic_score: float | None  # 0.0-1.0
    detected_pattern: str | None

    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class CanonicalTemplate:
    """
    Final unified template structure for Tako.

    This dataclass represents the complete canonical representation of an
    invoice template, ready for JSON serialization and consumption by Tako's
    backend systems.

    Attributes:
        sheet_name: Name of the Excel sheet this template was extracted from.
        header_fields: List of all canonical header fields (metadata).
        tables: List of all canonical tables (line-item data).

        # Summary statistics
        total_header_fields: Total number of header fields detected.
        matched_header_fields: Number of header fields with canonical_key assigned.
        unmatched_header_fields: Number of header fields without canonical_key.
        total_tables: Total number of tables detected.
        total_line_items: Total number of line items across all tables.

        metadata: Optional additional metadata.
    """

    sheet_name: str
    header_fields: list[CanonicalHeaderField]
    tables: list[CanonicalTable]

    # Summary statistics
    total_header_fields: int
    matched_header_fields: int
    unmatched_header_fields: int
    total_tables: int
    total_line_items: int

    metadata: dict[str, Any] = field(default_factory=dict)


def build_canonical_template(input_data: CanonicalTemplateInput) -> CanonicalTemplate:
    """
    Merge all pipeline outputs into a unified canonical template.

    This function performs deterministic aggregation without calling AI or external
    services. It joins classified components with fuzzy match results and organizes
    them into a structured template representation.

    Args:
        input_data: CanonicalTemplateInput containing all pipeline outputs:
            - sheet_name: Name of the Excel sheet (non-empty string).
            - header_candidate_blocks: Header regions detected by heuristics.
            - table_candidate_blocks: Table regions detected by heuristics.
            - classified_headers: Header fields classified by AI.
            - classified_columns: Table columns classified by AI.
            - extracted_line_items: Line items extracted by AI.
            - header_match_results: Fuzzy matching results for headers.
            - column_match_results: Fuzzy matching results for columns.

    Returns:
        CanonicalTemplate: Unified template structure with all metadata.

    Raises:
        ValueError: If sheet_name is empty or None, or if any list parameter is None.

    Example:
        >>> from template_sense.output.canonical_aggregator import (
        ...     build_canonical_template,
        ...     CanonicalTemplateInput,
        ... )
        >>> input_data = CanonicalTemplateInput(
        ...     sheet_name="Sheet1",
        ...     header_candidate_blocks=[...],
        ...     classified_headers=[...],
        ...     classified_columns=[...],
        ... )
        >>> template = build_canonical_template(input_data)
        >>> print(f"Found {template.total_header_fields} header fields")
        >>> print(f"Matched {template.matched_header_fields} fields")
    """
    # Step 1: Input validation
    if not input_data.sheet_name or not isinstance(input_data.sheet_name, str):
        raise ValueError("sheet_name must be a non-empty string")

    if input_data.header_candidate_blocks is None:
        raise ValueError("header_candidate_blocks cannot be None (empty list is valid)")
    if input_data.table_candidate_blocks is None:
        raise ValueError("table_candidate_blocks cannot be None (empty list is valid)")
    if input_data.classified_headers is None:
        raise ValueError("classified_headers cannot be None (empty list is valid)")
    if input_data.classified_columns is None:
        raise ValueError("classified_columns cannot be None (empty list is valid)")
    if input_data.extracted_line_items is None:
        raise ValueError("extracted_line_items cannot be None (empty list is valid)")
    if input_data.header_match_results is None:
        raise ValueError("header_match_results cannot be None (empty list is valid)")
    if input_data.column_match_results is None:
        raise ValueError("column_match_results cannot be None (empty list is valid)")

    logger.info(
        f"Building canonical template for sheet '{input_data.sheet_name}': "
        f"{len(input_data.classified_headers)} headers, {len(input_data.classified_columns)} columns, "
        f"{len(input_data.extracted_line_items)} line items"
    )

    # Step 2: Build header field index (match by original label)
    # Create mapping: original_label → FieldMatchResult
    header_match_map: dict[str, FieldMatchResult] = {
        result.original_text: result for result in input_data.header_match_results
    }

    canonical_headers: list[CanonicalHeaderField] = []
    for header in input_data.classified_headers:
        # Look up fuzzy match result (if exists)
        match_result = header_match_map.get(header.raw_label) if header.raw_label else None

        canonical_header = CanonicalHeaderField(
            canonical_key=match_result.canonical_key if match_result else None,
            original_label=header.raw_label,
            translated_label=match_result.translated_text if match_result else None,
            value=header.raw_value,
            heuristic_block_index=header.block_index,
            ai_confidence=header.model_confidence,
            fuzzy_match_score=match_result.match_score if match_result else None,
            matched_variant=match_result.matched_variant if match_result else None,
            row_index=header.row_index,
            col_index=header.col_index,
            metadata=header.metadata or {},
        )
        canonical_headers.append(canonical_header)

    logger.debug(f"Created {len(canonical_headers)} canonical header fields")

    # Step 3: Build table column index (match by original label)
    # Create mapping: original_label → FieldMatchResult
    column_match_map: dict[str, FieldMatchResult] = {
        result.original_text: result for result in input_data.column_match_results
    }

    # Group columns by table_block_index
    columns_by_table: dict[int, list[CanonicalTableColumn]] = {}
    for column in input_data.classified_columns:
        # Look up fuzzy match result (if exists)
        match_result = column_match_map.get(column.raw_label) if column.raw_label else None

        canonical_column = CanonicalTableColumn(
            canonical_key=match_result.canonical_key if match_result else None,
            original_label=column.raw_label,
            translated_label=match_result.translated_text if match_result else None,
            column_position=column.raw_position,
            sample_values=column.sample_values,
            ai_confidence=column.model_confidence,
            fuzzy_match_score=match_result.match_score if match_result else None,
            matched_variant=match_result.matched_variant if match_result else None,
            row_index=column.row_index,
            col_index=column.col_index,
            metadata=column.metadata or {},
        )

        # Group by table_block_index
        if column.table_block_index not in columns_by_table:
            columns_by_table[column.table_block_index] = []
        columns_by_table[column.table_block_index].append(canonical_column)

    logger.debug(f"Grouped columns into {len(columns_by_table)} tables")

    # Step 4: Aggregate line items by table_index
    line_items_by_table: dict[int, list[CanonicalLineItem]] = {}
    for item in input_data.extracted_line_items:
        canonical_item = CanonicalLineItem(
            row_index=item.row_index,
            line_number=item.line_number,
            columns=item.columns,
            is_subtotal=item.is_subtotal,
            ai_confidence=item.model_confidence,
            metadata=item.metadata or {},
        )

        # Group by table_index
        if item.table_index not in line_items_by_table:
            line_items_by_table[item.table_index] = []
        line_items_by_table[item.table_index].append(canonical_item)

    logger.debug(f"Grouped line items into {len(line_items_by_table)} tables")

    # Step 5: Build CanonicalTable objects
    canonical_tables: list[CanonicalTable] = []
    for idx, table_block in enumerate(input_data.table_candidate_blocks):
        # Find matching columns and line items for this table
        table_columns = columns_by_table.get(idx, [])
        table_line_items = line_items_by_table.get(idx, [])

        canonical_table = CanonicalTable(
            table_block_index=idx,
            row_start=table_block.row_start,
            row_end=table_block.row_end,
            col_start=table_block.col_start,
            col_end=table_block.col_end,
            columns=table_columns,
            line_items=table_line_items,
            heuristic_score=table_block.score,
            detected_pattern=table_block.detected_pattern,
            metadata={},
        )
        canonical_tables.append(canonical_table)

    logger.debug(f"Created {len(canonical_tables)} canonical tables")

    # Step 6: Compute summary statistics
    total_header_fields = len(canonical_headers)
    matched_header_fields = sum(1 for h in canonical_headers if h.canonical_key is not None)
    unmatched_header_fields = total_header_fields - matched_header_fields
    total_tables = len(canonical_tables)
    total_line_items = sum(len(table.line_items) for table in canonical_tables)

    logger.info(
        f"Template statistics: {matched_header_fields}/{total_header_fields} headers matched, "
        f"{total_tables} tables, {total_line_items} line items"
    )

    # Step 7: Return CanonicalTemplate
    return CanonicalTemplate(
        sheet_name=input_data.sheet_name,
        header_fields=canonical_headers,
        tables=canonical_tables,
        total_header_fields=total_header_fields,
        matched_header_fields=matched_header_fields,
        unmatched_header_fields=unmatched_header_fields,
        total_tables=total_tables,
        total_line_items=total_line_items,
        metadata={},
    )
