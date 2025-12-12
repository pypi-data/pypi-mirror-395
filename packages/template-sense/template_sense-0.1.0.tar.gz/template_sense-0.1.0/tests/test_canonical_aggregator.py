"""
Unit tests for canonical template aggregator.

Tests the aggregation logic that merges all pipeline outputs (extraction,
AI classification, translation, and fuzzy matching) into a unified canonical
template representation.
"""

import pytest

from template_sense.ai.header_classification import ClassifiedHeaderField
from template_sense.ai.line_item_extraction import ExtractedLineItem
from template_sense.ai.table_column_classification import ClassifiedTableColumn
from template_sense.extraction.header_candidates import HeaderCandidateBlock
from template_sense.extraction.table_candidates import TableCandidateBlock
from template_sense.mapping.fuzzy_field_matching import FieldMatchResult
from template_sense.output.canonical_aggregator import (
    CanonicalTemplate,
    CanonicalTemplateInput,
    build_canonical_template,
)

# ============================================================================
# Test Fixtures and Factory Functions
# ============================================================================


def create_header_candidate_block(
    row_start: int = 1,
    row_end: int = 5,
    col_start: int = 1,
    col_end: int = 4,
    score: float = 0.8,
) -> HeaderCandidateBlock:
    """Factory function to create test HeaderCandidateBlock."""
    return HeaderCandidateBlock(
        row_start=row_start,
        row_end=row_end,
        col_start=col_start,
        col_end=col_end,
        content=[(1, 1, "Invoice No:"), (1, 2, "INV-001")],
        label_value_pairs=[("Invoice No", "INV-001", 1, 1)],
        score=score,
        detected_pattern="key_value_pairs",
    )


def create_table_candidate_block(
    row_start: int = 10,
    row_end: int = 15,
    col_start: int = 1,
    col_end: int = 5,
    score: float = 0.9,
) -> TableCandidateBlock:
    """Factory function to create test TableCandidateBlock."""
    return TableCandidateBlock(
        row_start=row_start,
        row_end=row_end,
        col_start=col_start,
        col_end=col_end,
        content=[(10, 1, "Product"), (10, 2, "Qty")],
        score=score,
        detected_pattern="column_consistency",
    )


def create_classified_header(
    raw_label: str = "Invoice Number",
    raw_value: str = "INV-001",
    block_index: int = 0,
    row_index: int = 1,
    col_index: int = 2,
    confidence: float = 0.95,
) -> ClassifiedHeaderField:
    """Factory function to create test ClassifiedHeaderField."""
    return ClassifiedHeaderField(
        canonical_key=None,  # Will be populated by mapping layer
        raw_label=raw_label,
        raw_value=raw_value,
        block_index=block_index,
        row_index=row_index,
        col_index=col_index,
        model_confidence=confidence,
        metadata={},
    )


def create_classified_column(
    raw_label: str = "Product Name",
    raw_position: int = 0,
    table_block_index: int = 0,
    row_index: int = 10,
    col_index: int = 1,
    confidence: float = 0.92,
) -> ClassifiedTableColumn:
    """Factory function to create test ClassifiedTableColumn."""
    return ClassifiedTableColumn(
        canonical_key=None,  # Will be populated by mapping layer
        raw_label=raw_label,
        raw_position=raw_position,
        table_block_index=table_block_index,
        row_index=row_index,
        col_index=col_index,
        sample_values=["Widget A", "Widget B", "Widget C"],
        model_confidence=confidence,
        metadata={},
    )


def create_extracted_line_item(
    table_index: int = 0,
    row_index: int = 11,
    line_number: int = 1,
    columns: dict = None,
    is_subtotal: bool = False,
    confidence: float = 0.88,
) -> ExtractedLineItem:
    """Factory function to create test ExtractedLineItem."""
    if columns is None:
        columns = {"product_name": "Widget A", "quantity": 10}
    return ExtractedLineItem(
        table_index=table_index,
        row_index=row_index,
        line_number=line_number,
        columns=columns,
        is_subtotal=is_subtotal,
        model_confidence=confidence,
        metadata={},
    )


def create_field_match_result(
    original_text: str = "Invoice Number",
    translated_text: str = "Invoice Number",
    canonical_key: str = "invoice_number",
    match_score: float = 100.0,
    matched_variant: str = "Invoice Number",
) -> FieldMatchResult:
    """Factory function to create test FieldMatchResult."""
    return FieldMatchResult(
        original_text=original_text,
        translated_text=translated_text,
        canonical_key=canonical_key,
        match_score=match_score,
        matched_variant=matched_variant,
    )


# ============================================================================
# Test Cases
# ============================================================================


def test_build_canonical_template_simple_case():
    """Test aggregation with simple case: 2 headers, 1 table with 2 columns, 3 line items."""
    # Setup inputs
    sheet_name = "Sheet1"

    # Header candidate blocks
    header_blocks = [create_header_candidate_block()]

    # Table candidate blocks
    table_blocks = [create_table_candidate_block()]

    # Classified headers
    classified_headers = [
        create_classified_header(raw_label="Invoice Number", raw_value="INV-001"),
        create_classified_header(
            raw_label="Invoice Date", raw_value="2025-01-15", row_index=2, col_index=2
        ),
    ]

    # Classified columns
    classified_columns = [
        create_classified_column(raw_label="Product Name", raw_position=0, col_index=1),
        create_classified_column(raw_label="Quantity", raw_position=1, col_index=2),
    ]

    # Line items
    line_items = [
        create_extracted_line_item(row_index=11, line_number=1),
        create_extracted_line_item(row_index=12, line_number=2),
        create_extracted_line_item(row_index=13, line_number=3),
    ]

    # Match results
    header_matches = [
        create_field_match_result(original_text="Invoice Number", canonical_key="invoice_number"),
        create_field_match_result(
            original_text="Invoice Date",
            translated_text="Invoice Date",
            canonical_key="invoice_date",
            matched_variant="Invoice Date",
        ),
    ]

    column_matches = [
        create_field_match_result(
            original_text="Product Name",
            translated_text="Product Name",
            canonical_key="product_name",
            matched_variant="Product Name",
        ),
        create_field_match_result(
            original_text="Quantity",
            translated_text="Quantity",
            canonical_key="quantity",
            matched_variant="Qty",
            match_score=95.0,
        ),
    ]

    # Execute
    result = build_canonical_template(
        CanonicalTemplateInput(
            sheet_name=sheet_name,
            header_candidate_blocks=header_blocks,
            table_candidate_blocks=table_blocks,
            classified_headers=classified_headers,
            classified_columns=classified_columns,
            extracted_line_items=line_items,
            header_match_results=header_matches,
            column_match_results=column_matches,
        )
    )

    # Verify structure
    assert isinstance(result, CanonicalTemplate)
    assert result.sheet_name == "Sheet1"

    # Verify header fields
    assert len(result.header_fields) == 2
    assert result.total_header_fields == 2
    assert result.matched_header_fields == 2
    assert result.unmatched_header_fields == 0

    # Check first header field
    header1 = result.header_fields[0]
    assert header1.canonical_key == "invoice_number"
    assert header1.original_label == "Invoice Number"
    assert header1.translated_label == "Invoice Number"
    assert header1.value == "INV-001"
    assert header1.ai_confidence == 0.95
    assert header1.fuzzy_match_score == 100.0
    assert header1.matched_variant == "Invoice Number"

    # Verify tables
    assert len(result.tables) == 1
    assert result.total_tables == 1

    table = result.tables[0]
    assert table.table_block_index == 0
    assert table.row_start == 10
    assert table.row_end == 15
    assert table.heuristic_score == 0.9
    assert table.detected_pattern == "column_consistency"

    # Verify columns
    assert len(table.columns) == 2
    col1 = table.columns[0]
    assert col1.canonical_key == "product_name"
    assert col1.original_label == "Product Name"
    assert col1.column_position == 0
    assert col1.ai_confidence == 0.92
    assert col1.fuzzy_match_score == 100.0

    # Verify line items
    assert len(table.line_items) == 3
    assert result.total_line_items == 3

    item1 = table.line_items[0]
    assert item1.row_index == 11
    assert item1.line_number == 1
    assert item1.is_subtotal is False
    assert item1.ai_confidence == 0.88


def test_build_canonical_template_empty_inputs():
    """Test aggregation with empty inputs (valid edge case)."""
    result = build_canonical_template(
        CanonicalTemplateInput(
            sheet_name="EmptySheet",
            header_candidate_blocks=[],
            table_candidate_blocks=[],
            classified_headers=[],
            classified_columns=[],
            extracted_line_items=[],
            header_match_results=[],
            column_match_results=[],
        )
    )

    # Verify structure
    assert isinstance(result, CanonicalTemplate)
    assert result.sheet_name == "EmptySheet"

    # Verify everything is empty
    assert len(result.header_fields) == 0
    assert len(result.tables) == 0
    assert result.total_header_fields == 0
    assert result.matched_header_fields == 0
    assert result.unmatched_header_fields == 0
    assert result.total_tables == 0
    assert result.total_line_items == 0


def test_build_canonical_template_unmatched_fields():
    """Test aggregation when classified headers have NO corresponding match results."""
    # Setup: headers with no matches
    classified_headers = [
        create_classified_header(raw_label="Unknown Field 1", raw_value="Value 1"),
        create_classified_header(raw_label="Unknown Field 2", raw_value="Value 2"),
    ]

    result = build_canonical_template(
        CanonicalTemplateInput(
            sheet_name="Sheet1",
            header_candidate_blocks=[create_header_candidate_block()],
            table_candidate_blocks=[],
            classified_headers=classified_headers,
            classified_columns=[],
            extracted_line_items=[],
            header_match_results=[],  # No matches!
            column_match_results=[],
        )
    )

    # Verify unmatched headers
    assert result.total_header_fields == 2
    assert result.matched_header_fields == 0
    assert result.unmatched_header_fields == 2

    # Check that canonical_key is None
    for header in result.header_fields:
        assert header.canonical_key is None
        assert header.fuzzy_match_score is None
        assert header.matched_variant is None
        assert header.translated_label is None  # No match = no translation


def test_build_canonical_template_multiple_tables():
    """Test aggregation with 3 tables, each with different columns and line items."""
    # Setup 3 table blocks
    table_blocks = [
        create_table_candidate_block(row_start=10, row_end=15),
        create_table_candidate_block(row_start=20, row_end=25),
        create_table_candidate_block(row_start=30, row_end=35),
    ]

    # Columns for each table
    classified_columns = [
        # Table 0
        create_classified_column(raw_label="Product", table_block_index=0, col_index=1),
        create_classified_column(raw_label="Qty", table_block_index=0, col_index=2),
        # Table 1
        create_classified_column(raw_label="Service", table_block_index=1, col_index=1),
        create_classified_column(raw_label="Hours", table_block_index=1, col_index=2),
        # Table 2
        create_classified_column(raw_label="Charge Type", table_block_index=2, col_index=1),
    ]

    # Line items for each table
    line_items = [
        # Table 0
        create_extracted_line_item(table_index=0, row_index=11),
        create_extracted_line_item(table_index=0, row_index=12),
        # Table 1
        create_extracted_line_item(table_index=1, row_index=21),
        # Table 2 (no line items)
    ]

    result = build_canonical_template(
        CanonicalTemplateInput(
            sheet_name="MultiTable",
            header_candidate_blocks=[],
            table_candidate_blocks=table_blocks,
            classified_headers=[],
            classified_columns=classified_columns,
            extracted_line_items=line_items,
            header_match_results=[],
            column_match_results=[],  # No matches for simplicity
        )
    )

    # Verify table count
    assert result.total_tables == 3
    assert len(result.tables) == 3

    # Verify table 0
    table0 = result.tables[0]
    assert table0.table_block_index == 0
    assert len(table0.columns) == 2
    assert len(table0.line_items) == 2

    # Verify table 1
    table1 = result.tables[1]
    assert table1.table_block_index == 1
    assert len(table1.columns) == 2
    assert len(table1.line_items) == 1

    # Verify table 2 (no line items)
    table2 = result.tables[2]
    assert table2.table_block_index == 2
    assert len(table2.columns) == 1
    assert len(table2.line_items) == 0

    # Verify total line items
    assert result.total_line_items == 3


def test_build_canonical_template_preserves_metadata():
    """Test that all metadata (AI confidence, fuzzy scores, block indices) is preserved."""
    classified_headers = [
        create_classified_header(
            raw_label="Invoice Number",
            raw_value="INV-123",
            block_index=5,
            row_index=3,
            col_index=7,
            confidence=0.87,
        )
    ]

    header_matches = [
        create_field_match_result(
            original_text="Invoice Number",
            canonical_key="invoice_number",
            match_score=92.5,
            matched_variant="Inv No",
        )
    ]

    result = build_canonical_template(
        CanonicalTemplateInput(
            sheet_name="Sheet1",
            header_candidate_blocks=[create_header_candidate_block()],
            table_candidate_blocks=[],
            classified_headers=classified_headers,
            classified_columns=[],
            extracted_line_items=[],
            header_match_results=header_matches,
            column_match_results=[],
        )
    )

    # Verify all metadata preserved
    header = result.header_fields[0]
    assert header.canonical_key == "invoice_number"
    assert header.original_label == "Invoice Number"
    assert header.value == "INV-123"
    assert header.heuristic_block_index == 5
    assert header.ai_confidence == 0.87
    assert header.fuzzy_match_score == 92.5
    assert header.matched_variant == "Inv No"
    assert header.row_index == 3
    assert header.col_index == 7


def test_build_canonical_template_coordinates():
    """Test that 1-based coordinates are preserved correctly."""
    classified_headers = [
        create_classified_header(row_index=5, col_index=10),
    ]

    classified_columns = [
        create_classified_column(table_block_index=0, row_index=15, col_index=3),
    ]

    table_blocks = [
        create_table_candidate_block(row_start=10, row_end=20, col_start=1, col_end=5),
    ]

    result = build_canonical_template(
        CanonicalTemplateInput(
            sheet_name="Sheet1",
            header_candidate_blocks=[create_header_candidate_block()],
            table_candidate_blocks=table_blocks,
            classified_headers=classified_headers,
            classified_columns=classified_columns,
            extracted_line_items=[],
            header_match_results=[],
            column_match_results=[],
        )
    )

    # Verify header coordinates
    header = result.header_fields[0]
    assert header.row_index == 5
    assert header.col_index == 10

    # Verify table coordinates
    table = result.tables[0]
    assert table.row_start == 10
    assert table.row_end == 20
    assert table.col_start == 1
    assert table.col_end == 5

    # Verify column coordinates
    column = table.columns[0]
    assert column.row_index == 15
    assert column.col_index == 3


def test_build_canonical_template_deterministic_output():
    """Test that same inputs produce identical outputs (deterministic)."""
    # Setup identical inputs
    sheet_name = "Sheet1"
    header_blocks = [create_header_candidate_block()]
    table_blocks = [create_table_candidate_block()]
    classified_headers = [create_classified_header()]
    classified_columns = [create_classified_column()]
    line_items = [create_extracted_line_item()]
    header_matches = [create_field_match_result()]
    column_matches = [
        create_field_match_result(original_text="Product Name", canonical_key="product_name")
    ]

    # Run twice
    result1 = build_canonical_template(
        CanonicalTemplateInput(
            sheet_name=sheet_name,
            header_candidate_blocks=header_blocks,
            table_candidate_blocks=table_blocks,
            classified_headers=classified_headers,
            classified_columns=classified_columns,
            extracted_line_items=line_items,
            header_match_results=header_matches,
            column_match_results=column_matches,
        )
    )

    result2 = build_canonical_template(
        CanonicalTemplateInput(
            sheet_name=sheet_name,
            header_candidate_blocks=header_blocks,
            table_candidate_blocks=table_blocks,
            classified_headers=classified_headers,
            classified_columns=classified_columns,
            extracted_line_items=line_items,
            header_match_results=header_matches,
            column_match_results=column_matches,
        )
    )

    # Verify outputs are identical
    assert result1.sheet_name == result2.sheet_name
    assert result1.total_header_fields == result2.total_header_fields
    assert result1.matched_header_fields == result2.matched_header_fields
    assert result1.total_tables == result2.total_tables
    assert result1.total_line_items == result2.total_line_items

    # Check header fields match
    assert len(result1.header_fields) == len(result2.header_fields)
    for h1, h2 in zip(result1.header_fields, result2.header_fields, strict=True):
        assert h1.canonical_key == h2.canonical_key
        assert h1.original_label == h2.original_label
        assert h1.value == h2.value

    # Check tables match
    assert len(result1.tables) == len(result2.tables)
    for t1, t2 in zip(result1.tables, result2.tables, strict=True):
        assert t1.table_block_index == t2.table_block_index
        assert len(t1.columns) == len(t2.columns)
        assert len(t1.line_items) == len(t2.line_items)


def test_build_canonical_template_invalid_inputs():
    """Test that invalid inputs raise ValueError with clear messages."""
    # Test empty sheet_name
    with pytest.raises(ValueError, match="sheet_name must be a non-empty string"):
        build_canonical_template(
            CanonicalTemplateInput(
                sheet_name="",
                header_candidate_blocks=[],
                table_candidate_blocks=[],
                classified_headers=[],
                classified_columns=[],
                extracted_line_items=[],
                header_match_results=[],
                column_match_results=[],
            )
        )

    # Test None sheet_name
    with pytest.raises(ValueError, match="sheet_name must be a non-empty string"):
        build_canonical_template(
            CanonicalTemplateInput(
                sheet_name=None,
                header_candidate_blocks=[],
                table_candidate_blocks=[],
                classified_headers=[],
                classified_columns=[],
                extracted_line_items=[],
                header_match_results=[],
                column_match_results=[],
            )
        )

    # Test None list parameters
    with pytest.raises(ValueError, match="header_candidate_blocks cannot be None"):
        build_canonical_template(
            CanonicalTemplateInput(
                sheet_name="Sheet1",
                header_candidate_blocks=None,
                table_candidate_blocks=[],
                classified_headers=[],
                classified_columns=[],
                extracted_line_items=[],
                header_match_results=[],
                column_match_results=[],
            )
        )

    with pytest.raises(ValueError, match="classified_headers cannot be None"):
        build_canonical_template(
            CanonicalTemplateInput(
                sheet_name="Sheet1",
                header_candidate_blocks=[],
                table_candidate_blocks=[],
                classified_headers=None,
                classified_columns=[],
                extracted_line_items=[],
                header_match_results=[],
                column_match_results=[],
            )
        )


def test_build_canonical_template_with_subtotal_line_items():
    """Test that subtotal line items are correctly identified and aggregated."""
    line_items = [
        create_extracted_line_item(row_index=11, line_number=1, is_subtotal=False),
        create_extracted_line_item(row_index=12, line_number=2, is_subtotal=False),
        create_extracted_line_item(
            row_index=13,
            line_number=None,
            columns={"label": "Subtotal", "amount": 1000},
            is_subtotal=True,
        ),
    ]

    result = build_canonical_template(
        CanonicalTemplateInput(
            sheet_name="Sheet1",
            header_candidate_blocks=[],
            table_candidate_blocks=[create_table_candidate_block()],
            classified_headers=[],
            classified_columns=[],
            extracted_line_items=line_items,
            header_match_results=[],
            column_match_results=[],
        )
    )

    # Verify line items
    assert result.total_line_items == 3
    table = result.tables[0]
    assert len(table.line_items) == 3

    # Check subtotal flag
    assert table.line_items[0].is_subtotal is False
    assert table.line_items[1].is_subtotal is False
    assert table.line_items[2].is_subtotal is True
    assert table.line_items[2].line_number is None


def test_build_canonical_template_column_sample_values():
    """Test that column sample values are preserved correctly."""
    classified_columns = [
        create_classified_column(
            raw_label="Product",
            raw_position=0,
            table_block_index=0,
        )
    ]

    # The factory creates sample_values by default
    result = build_canonical_template(
        CanonicalTemplateInput(
            sheet_name="Sheet1",
            header_candidate_blocks=[],
            table_candidate_blocks=[create_table_candidate_block()],
            classified_headers=[],
            classified_columns=classified_columns,
            extracted_line_items=[],
            header_match_results=[],
            column_match_results=[],
        )
    )

    # Verify sample values preserved
    table = result.tables[0]
    column = table.columns[0]
    assert column.sample_values == ["Widget A", "Widget B", "Widget C"]
    assert column.column_position == 0
