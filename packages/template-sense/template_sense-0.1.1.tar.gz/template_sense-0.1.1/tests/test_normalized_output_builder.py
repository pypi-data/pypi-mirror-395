"""
Unit tests for normalized_output_builder module.

Tests cover:
1. Simple case with matched headers, tables, and line items
2. Empty template (no headers, no tables)
3. Unmatched headers only
4. Matched headers only
5. Multiple tables
6. Null value handling
7. Coordinate preservation
8. Confidence score preservation
9. Metadata preservation
10. Custom version
11. JSON serialization
12. Deterministic output
13. Subtotal line items
14. Sample values preservation
"""

import json
from typing import Any

import pytest

from template_sense.constants import OUTPUT_SCHEMA_VERSION
from template_sense.output.canonical_aggregator import (
    CanonicalHeaderField,
    CanonicalLineItem,
    CanonicalTable,
    CanonicalTableColumn,
    CanonicalTemplate,
)
from template_sense.output.normalized_output_builder import (
    _partition_headers,
    _serialize_header_field,
    _serialize_line_item,
    _serialize_table,
    _serialize_table_column,
    build_normalized_output,
)

# ============================================================
# Fixture Helpers
# ============================================================


def create_header_field(
    canonical_key: str | None = "invoice_number",
    original_label: str | None = "請求書番号",
    translated_label: str | None = "Invoice Number",
    value: Any = "INV-12345",
    heuristic_block_index: int | None = 0,
    ai_confidence: float | None = 0.95,
    fuzzy_match_score: float | None = 87.5,
    matched_variant: str | None = "Invoice No",
    row_index: int = 1,
    col_index: int = 2,
    metadata: dict[str, Any] | None = None,
) -> CanonicalHeaderField:
    """Helper to create CanonicalHeaderField instances."""
    return CanonicalHeaderField(
        canonical_key=canonical_key,
        original_label=original_label,
        translated_label=translated_label,
        value=value,
        heuristic_block_index=heuristic_block_index,
        ai_confidence=ai_confidence,
        fuzzy_match_score=fuzzy_match_score,
        matched_variant=matched_variant,
        row_index=row_index,
        col_index=col_index,
        metadata=metadata or {},
    )


def create_table_column(
    canonical_key: str | None = "product_name",
    original_label: str | None = "商品名",
    translated_label: str | None = "Product Name",
    column_position: int = 0,
    sample_values: list[Any] | None = None,
    ai_confidence: float | None = 0.9,
    fuzzy_match_score: float | None = 92.0,
    matched_variant: str | None = "Product",
    row_index: int = 5,
    col_index: int = 1,
    metadata: dict[str, Any] | None = None,
) -> CanonicalTableColumn:
    """Helper to create CanonicalTableColumn instances."""
    return CanonicalTableColumn(
        canonical_key=canonical_key,
        original_label=original_label,
        translated_label=translated_label,
        column_position=column_position,
        sample_values=sample_values if sample_values is not None else ["Widget A", "Widget B"],
        ai_confidence=ai_confidence,
        fuzzy_match_score=fuzzy_match_score,
        matched_variant=matched_variant,
        row_index=row_index,
        col_index=col_index,
        metadata=metadata or {},
    )


def create_line_item(
    row_index: int = 6,
    line_number: int | None = 1,
    columns: dict[str, Any] | None = None,
    is_subtotal: bool = False,
    ai_confidence: float | None = 0.88,
    metadata: dict[str, Any] | None = None,
) -> CanonicalLineItem:
    """Helper to create CanonicalLineItem instances."""
    return CanonicalLineItem(
        row_index=row_index,
        line_number=line_number,
        columns=columns or {"product_name": "Widget A", "quantity": 5},
        is_subtotal=is_subtotal,
        ai_confidence=ai_confidence,
        metadata=metadata or {},
    )


def create_table(
    table_block_index: int = 0,
    row_start: int = 5,
    row_end: int = 10,
    col_start: int = 1,
    col_end: int = 5,
    columns: list[CanonicalTableColumn] | None = None,
    line_items: list[CanonicalLineItem] | None = None,
    heuristic_score: float | None = 0.9,
    detected_pattern: str | None = "numeric_density",
    metadata: dict[str, Any] | None = None,
) -> CanonicalTable:
    """Helper to create CanonicalTable instances."""
    return CanonicalTable(
        table_block_index=table_block_index,
        row_start=row_start,
        row_end=row_end,
        col_start=col_start,
        col_end=col_end,
        columns=columns or [],
        line_items=line_items or [],
        heuristic_score=heuristic_score,
        detected_pattern=detected_pattern,
        metadata=metadata or {},
    )


def create_template(
    sheet_name: str = "Sheet1",
    header_fields: list[CanonicalHeaderField] | None = None,
    tables: list[CanonicalTable] | None = None,
    total_header_fields: int = 0,
    matched_header_fields: int = 0,
    unmatched_header_fields: int = 0,
    total_tables: int = 0,
    total_line_items: int = 0,
    metadata: dict[str, Any] | None = None,
) -> CanonicalTemplate:
    """Helper to create CanonicalTemplate instances."""
    return CanonicalTemplate(
        sheet_name=sheet_name,
        header_fields=header_fields or [],
        tables=tables or [],
        total_header_fields=total_header_fields,
        matched_header_fields=matched_header_fields,
        unmatched_header_fields=unmatched_header_fields,
        total_tables=total_tables,
        total_line_items=total_line_items,
        metadata=metadata or {},
    )


# ============================================================
# Test: Helper Function - _serialize_header_field
# ============================================================


def test_serialize_header_field_matched():
    """Test serialization of a matched header field with all attributes."""
    field = create_header_field()

    result = _serialize_header_field(field)

    assert result["canonical_key"] == "invoice_number"
    assert result["original_label"] == "請求書番号"
    assert result["translated_label"] == "Invoice Number"
    assert result["value"] == "INV-12345"
    assert result["location"] == {"row": 1, "col": 2}
    # Internal metrics removed: confidence, matched_variant
    assert "confidence" not in result
    assert "matched_variant" not in result
    # Empty metadata should be omitted
    assert "metadata" not in result


def test_serialize_header_field_unmatched():
    """Test serialization of an unmatched header field (no canonical_key)."""
    field = create_header_field(
        canonical_key=None,
        fuzzy_match_score=None,
        matched_variant=None,
        translated_label=None,
    )

    result = _serialize_header_field(field)

    assert result["canonical_key"] is None
    assert result["original_label"] == "請求書番号"
    assert result["translated_label"] is None
    # Internal metrics removed: confidence, matched_variant
    assert "confidence" not in result
    assert "matched_variant" not in result


def test_serialize_header_field_no_ai_confidence():
    """Test serialization when AI confidence is None."""
    field = create_header_field(ai_confidence=None)

    result = _serialize_header_field(field)

    # Internal metrics removed: confidence
    assert "confidence" not in result


def test_serialize_header_field_null_value():
    """Test serialization with None value."""
    field = create_header_field(value=None)

    result = _serialize_header_field(field)

    assert result["value"] is None


# ============================================================
# Test: Helper Function - _serialize_table_column
# ============================================================


def test_serialize_table_column_matched():
    """Test serialization of a matched table column with all attributes."""
    column = create_table_column()

    result = _serialize_table_column(column)

    assert result["canonical_key"] == "product_name"
    assert result["original_label"] == "商品名"
    assert result["translated_label"] == "Product Name"
    assert result["column_position"] == 0
    assert result["sample_values"] == ["Widget A", "Widget B"]
    assert result["location"] == {"row": 5, "col": 1}
    # Internal metrics removed: confidence, matched_variant
    assert "confidence" not in result
    assert "matched_variant" not in result
    # Empty metadata should be omitted
    assert "metadata" not in result


def test_serialize_table_column_unmatched():
    """Test serialization of an unmatched table column."""
    column = create_table_column(
        canonical_key=None,
        fuzzy_match_score=None,
        matched_variant=None,
        translated_label=None,
    )

    result = _serialize_table_column(column)

    assert result["canonical_key"] is None
    assert result["translated_label"] is None
    # Internal metrics removed: confidence, matched_variant
    assert "confidence" not in result
    assert "matched_variant" not in result


def test_serialize_table_column_empty_samples():
    """Test serialization with empty sample values."""
    column = create_table_column(sample_values=[])

    result = _serialize_table_column(column)

    assert result["sample_values"] == []


# ============================================================
# Test: Helper Function - _serialize_line_item
# ============================================================


def test_serialize_line_item_regular():
    """Test serialization of a regular line item."""
    item = create_line_item()

    result = _serialize_line_item(item)

    assert result["row_index"] == 6
    assert result["line_number"] == 1
    assert result["columns"] == {"product_name": "Widget A", "quantity": 5}
    assert result["is_subtotal"] is False
    # Internal metrics removed: confidence
    assert "confidence" not in result
    # Empty metadata should be omitted
    assert "metadata" not in result


def test_serialize_line_item_subtotal():
    """Test serialization of a subtotal line item."""
    item = create_line_item(is_subtotal=True, line_number=None)

    result = _serialize_line_item(item)

    assert result["is_subtotal"] is True
    assert result["line_number"] is None


def test_serialize_line_item_no_confidence():
    """Test serialization when AI confidence is None."""
    item = create_line_item(ai_confidence=None)

    result = _serialize_line_item(item)

    # Internal metrics removed: confidence
    assert "confidence" not in result


# ============================================================
# Test: Helper Function - _serialize_table
# ============================================================


def test_serialize_table_with_content():
    """Test serialization of a table with columns and line items."""
    columns = [
        create_table_column(canonical_key="product_name", column_position=0),
        create_table_column(canonical_key="quantity", column_position=1),
    ]
    line_items = [
        create_line_item(row_index=6, line_number=1),
        create_line_item(row_index=7, line_number=2),
    ]
    table = create_table(columns=columns, line_items=line_items)

    result = _serialize_table(table, 0)

    assert result["table_index"] == 0
    assert result["location"]["row_start"] == 5
    assert result["location"]["row_end"] == 10
    assert result["location"]["col_start"] == 1
    assert result["location"]["col_end"] == 5
    assert len(result["columns"]) == 2
    assert len(result["line_items"]) == 2
    # Internal metrics removed: detection_info
    assert "detection_info" not in result
    # Empty metadata should be omitted
    assert "metadata" not in result


def test_serialize_table_empty():
    """Test serialization of an empty table (no columns, no line items)."""
    table = create_table(columns=[], line_items=[], heuristic_score=None, detected_pattern=None)

    result = _serialize_table(table, 0)

    assert result["columns"] == []
    assert result["line_items"] == []
    # Internal metrics removed: detection_info
    assert "detection_info" not in result


# ============================================================
# Test: Helper Function - _partition_headers
# ============================================================


def test_partition_headers_mixed():
    """Test partitioning headers into matched and unmatched groups."""
    headers = [
        create_header_field(canonical_key="invoice_number", row_index=1),
        create_header_field(canonical_key=None, row_index=2),
        create_header_field(canonical_key="shipper_name", row_index=3),
    ]

    matched, unmatched = _partition_headers(headers)

    assert len(matched) == 2
    assert len(unmatched) == 1
    assert matched[0]["canonical_key"] == "invoice_number"
    assert matched[1]["canonical_key"] == "shipper_name"
    assert unmatched[0]["canonical_key"] is None


def test_partition_headers_all_matched():
    """Test partitioning when all headers are matched."""
    headers = [
        create_header_field(canonical_key="invoice_number", row_index=1),
        create_header_field(canonical_key="shipper_name", row_index=2),
    ]

    matched, unmatched = _partition_headers(headers)

    assert len(matched) == 2
    assert len(unmatched) == 0


def test_partition_headers_all_unmatched():
    """Test partitioning when all headers are unmatched."""
    headers = [
        create_header_field(canonical_key=None, row_index=1),
        create_header_field(canonical_key=None, row_index=2),
    ]

    matched, unmatched = _partition_headers(headers)

    assert len(matched) == 0
    assert len(unmatched) == 2


def test_partition_headers_empty():
    """Test partitioning an empty header list."""
    matched, unmatched = _partition_headers([])

    assert matched == []
    assert unmatched == []


# ============================================================
# Test: Main Function - build_normalized_output
# ============================================================


def test_build_normalized_output_simple_case():
    """Test simple case with 2 matched headers, 1 table, 3 line items."""
    headers = [
        create_header_field(canonical_key="invoice_number", row_index=1, col_index=1),
        create_header_field(canonical_key="shipper_name", row_index=2, col_index=1),
    ]
    columns = [
        create_table_column(
            canonical_key="product_name", column_position=0, row_index=5, col_index=1
        ),
        create_table_column(canonical_key="quantity", column_position=1, row_index=5, col_index=2),
    ]
    line_items = [
        create_line_item(row_index=6, line_number=1),
        create_line_item(row_index=7, line_number=2),
        create_line_item(row_index=8, line_number=3),
    ]
    table = create_table(columns=columns, line_items=line_items)
    template = create_template(
        sheet_name="Sheet1",
        header_fields=headers,
        tables=[table],
        total_header_fields=2,
        matched_header_fields=2,
        unmatched_header_fields=0,
        total_tables=1,
        total_line_items=3,
    )

    output = build_normalized_output(template)

    assert output["version"] == OUTPUT_SCHEMA_VERSION
    assert output["sheet_name"] == "Sheet1"
    assert len(output["headers"]["matched"]) == 2
    assert len(output["headers"]["unmatched"]) == 0
    assert len(output["tables"]) == 1
    assert len(output["tables"][0]["line_items"]) == 3
    assert output["summary"]["total_header_fields"] == 2
    assert output["summary"]["matched_header_fields"] == 2
    assert output["summary"]["total_tables"] == 1
    assert output["summary"]["total_line_items"] == 3


def test_build_normalized_output_empty_template():
    """Test empty template (no headers, no tables)."""
    template = create_template(
        sheet_name="EmptySheet",
        header_fields=[],
        tables=[],
        total_header_fields=0,
        matched_header_fields=0,
        unmatched_header_fields=0,
        total_tables=0,
        total_line_items=0,
    )

    output = build_normalized_output(template)

    assert output["version"] == OUTPUT_SCHEMA_VERSION
    assert output["sheet_name"] == "EmptySheet"
    assert output["headers"]["matched"] == []
    assert output["headers"]["unmatched"] == []
    assert output["tables"] == []
    assert output["summary"]["total_header_fields"] == 0
    assert output["summary"]["total_tables"] == 0


def test_build_normalized_output_unmatched_headers_only():
    """Test template with only unmatched headers."""
    headers = [
        create_header_field(
            canonical_key=None, fuzzy_match_score=None, matched_variant=None, row_index=1
        ),
        create_header_field(
            canonical_key=None, fuzzy_match_score=None, matched_variant=None, row_index=2
        ),
    ]
    template = create_template(
        sheet_name="Sheet1",
        header_fields=headers,
        tables=[],
        total_header_fields=2,
        matched_header_fields=0,
        unmatched_header_fields=2,
        total_tables=0,
        total_line_items=0,
    )

    output = build_normalized_output(template)

    assert len(output["headers"]["matched"]) == 0
    assert len(output["headers"]["unmatched"]) == 2
    assert output["summary"]["matched_header_fields"] == 0
    assert output["summary"]["unmatched_header_fields"] == 2


def test_build_normalized_output_matched_headers_only():
    """Test template with only matched headers."""
    headers = [
        create_header_field(canonical_key="invoice_number", row_index=1),
        create_header_field(canonical_key="shipper_name", row_index=2),
    ]
    template = create_template(
        sheet_name="Sheet1",
        header_fields=headers,
        tables=[],
        total_header_fields=2,
        matched_header_fields=2,
        unmatched_header_fields=0,
        total_tables=0,
        total_line_items=0,
    )

    output = build_normalized_output(template)

    assert len(output["headers"]["matched"]) == 2
    assert len(output["headers"]["unmatched"]) == 0
    assert output["summary"]["matched_header_fields"] == 2


def test_build_normalized_output_multiple_tables():
    """Test template with multiple tables."""
    table1 = create_table(
        table_block_index=0,
        row_start=5,
        row_end=10,
        columns=[create_table_column(column_position=0)],
        line_items=[create_line_item(row_index=6)],
    )
    table2 = create_table(
        table_block_index=1,
        row_start=15,
        row_end=20,
        columns=[create_table_column(column_position=0)],
        line_items=[create_line_item(row_index=16)],
    )
    table3 = create_table(
        table_block_index=2,
        row_start=25,
        row_end=30,
        columns=[create_table_column(column_position=0)],
        line_items=[create_line_item(row_index=26)],
    )
    template = create_template(
        sheet_name="Sheet1",
        header_fields=[],
        tables=[table1, table2, table3],
        total_header_fields=0,
        matched_header_fields=0,
        unmatched_header_fields=0,
        total_tables=3,
        total_line_items=3,
    )

    output = build_normalized_output(template)

    assert len(output["tables"]) == 3
    assert output["tables"][0]["table_index"] == 0
    assert output["tables"][1]["table_index"] == 1
    assert output["tables"][2]["table_index"] == 2
    assert output["summary"]["total_tables"] == 3


def test_build_normalized_output_null_value_handling():
    """Test handling of None values in fields."""
    headers = [
        create_header_field(
            canonical_key=None,
            original_label=None,
            translated_label=None,
            value=None,
            fuzzy_match_score=None,
            matched_variant=None,
            ai_confidence=None,
        )
    ]
    template = create_template(
        sheet_name="Sheet1",
        header_fields=headers,
        tables=[],
        total_header_fields=1,
        matched_header_fields=0,
        unmatched_header_fields=1,
        total_tables=0,
        total_line_items=0,
    )

    output = build_normalized_output(template)

    unmatched = output["headers"]["unmatched"][0]
    assert unmatched["canonical_key"] is None
    assert unmatched["original_label"] is None
    assert unmatched["translated_label"] is None
    assert unmatched["value"] is None
    # Internal metrics removed: matched_variant, confidence
    assert "matched_variant" not in unmatched
    assert "confidence" not in unmatched


def test_build_normalized_output_coordinate_preservation():
    """Test that 1-based Excel coordinates are preserved correctly."""
    header = create_header_field(row_index=10, col_index=20)
    column = create_table_column(row_index=15, col_index=3, column_position=2)
    table = create_table(
        row_start=15,
        row_end=25,
        col_start=1,
        col_end=5,
        columns=[column],
        line_items=[],
    )
    template = create_template(
        sheet_name="Sheet1",
        header_fields=[header],
        tables=[table],
        total_header_fields=1,
        matched_header_fields=1,
        unmatched_header_fields=0,
        total_tables=1,
        total_line_items=0,
    )

    output = build_normalized_output(template)

    # Check header coordinates
    matched_header = output["headers"]["matched"][0]
    assert matched_header["location"]["row"] == 10
    assert matched_header["location"]["col"] == 20

    # Check table coordinates
    table_output = output["tables"][0]
    assert table_output["location"]["row_start"] == 15
    assert table_output["location"]["row_end"] == 25
    assert table_output["location"]["col_start"] == 1
    assert table_output["location"]["col_end"] == 5

    # Check column coordinates
    column_output = table_output["columns"][0]
    assert column_output["location"]["row"] == 15
    assert column_output["location"]["col"] == 3


def test_build_normalized_output_confidence_score_preservation():
    """Test that confidence scores are no longer included in output (internal metrics removed)."""
    header = create_header_field(ai_confidence=0.85, fuzzy_match_score=92.5)
    column = create_table_column(ai_confidence=0.75, fuzzy_match_score=88.0)
    line_item = create_line_item(ai_confidence=0.91)
    table = create_table(columns=[column], line_items=[line_item])
    template = create_template(
        sheet_name="Sheet1",
        header_fields=[header],
        tables=[table],
        total_header_fields=1,
        matched_header_fields=1,
        unmatched_header_fields=0,
        total_tables=1,
        total_line_items=1,
    )

    output = build_normalized_output(template)

    # Internal metrics removed: confidence scores should not be in output
    matched_header = output["headers"]["matched"][0]
    assert "confidence" not in matched_header

    # Check column confidence removed
    column_output = output["tables"][0]["columns"][0]
    assert "confidence" not in column_output

    # Check line item confidence removed
    item_output = output["tables"][0]["line_items"][0]
    assert "confidence" not in item_output


def test_build_normalized_output_metadata_preservation():
    """Test that all metadata dicts are preserved in output."""
    header_meta = {"source": "header_ai", "provider": "openai"}
    column_meta = {"source": "column_ai", "provider": "anthropic"}
    item_meta = {"source": "item_ai"}
    table_meta = {"source": "table_heuristic"}
    template_meta = {"file_path": "/path/to/file.xlsx"}

    header = create_header_field(metadata=header_meta)
    column = create_table_column(metadata=column_meta)
    line_item = create_line_item(metadata=item_meta)
    table = create_table(columns=[column], line_items=[line_item], metadata=table_meta)
    template = create_template(
        sheet_name="Sheet1",
        header_fields=[header],
        tables=[table],
        metadata=template_meta,
        total_header_fields=1,
        matched_header_fields=1,
        unmatched_header_fields=0,
        total_tables=1,
        total_line_items=1,
    )

    output = build_normalized_output(template)

    assert output["headers"]["matched"][0]["metadata"] == header_meta
    assert output["tables"][0]["columns"][0]["metadata"] == column_meta
    assert output["tables"][0]["line_items"][0]["metadata"] == item_meta
    assert output["tables"][0]["metadata"] == table_meta
    assert output["metadata"] == template_meta


def test_build_normalized_output_custom_version():
    """Test using a custom version string."""
    template = create_template(sheet_name="Sheet1")

    output = build_normalized_output(template, version="2.0-beta")

    assert output["version"] == "2.0-beta"


def test_build_normalized_output_json_serializable():
    """Test that output is fully JSON-serializable."""
    headers = [create_header_field()]
    columns = [create_table_column()]
    line_items = [create_line_item()]
    table = create_table(columns=columns, line_items=line_items)
    template = create_template(
        sheet_name="Sheet1",
        header_fields=headers,
        tables=[table],
        total_header_fields=1,
        matched_header_fields=1,
        unmatched_header_fields=0,
        total_tables=1,
        total_line_items=1,
    )

    output = build_normalized_output(template)

    # Should not raise any exception
    json_str = json.dumps(output)
    assert isinstance(json_str, str)
    assert len(json_str) > 0

    # Verify round-trip
    parsed = json.loads(json_str)
    assert parsed["version"] == OUTPUT_SCHEMA_VERSION
    assert parsed["sheet_name"] == "Sheet1"


def test_build_normalized_output_deterministic():
    """Test that same input produces identical output (deterministic behavior)."""
    headers = [
        create_header_field(canonical_key="invoice_number", row_index=1),
        create_header_field(canonical_key="shipper_name", row_index=2),
    ]
    columns = [create_table_column()]
    line_items = [create_line_item()]
    table = create_table(columns=columns, line_items=line_items)
    template = create_template(
        sheet_name="Sheet1",
        header_fields=headers,
        tables=[table],
        total_header_fields=2,
        matched_header_fields=2,
        unmatched_header_fields=0,
        total_tables=1,
        total_line_items=1,
    )

    # Generate output twice
    output1 = build_normalized_output(template)
    output2 = build_normalized_output(template)

    # Convert to JSON for comparison (handles dict ordering)
    json1 = json.dumps(output1, sort_keys=True)
    json2 = json.dumps(output2, sort_keys=True)

    assert json1 == json2


def test_build_normalized_output_subtotal_line_items():
    """Test handling of subtotal line items (is_subtotal flag)."""
    line_items = [
        create_line_item(row_index=6, line_number=1, is_subtotal=False),
        create_line_item(row_index=7, line_number=2, is_subtotal=False),
        create_line_item(row_index=8, line_number=None, is_subtotal=True),  # Subtotal row
    ]
    table = create_table(line_items=line_items)
    template = create_template(
        sheet_name="Sheet1",
        tables=[table],
        total_header_fields=0,
        matched_header_fields=0,
        unmatched_header_fields=0,
        total_tables=1,
        total_line_items=3,
    )

    output = build_normalized_output(template)

    items = output["tables"][0]["line_items"]
    assert items[0]["is_subtotal"] is False
    assert items[1]["is_subtotal"] is False
    assert items[2]["is_subtotal"] is True
    assert items[2]["line_number"] is None


def test_build_normalized_output_sample_values_preservation():
    """Test that column sample values are preserved correctly."""
    columns = [
        create_table_column(
            canonical_key="product_name",
            sample_values=["Widget A", "Widget B", "Widget C"],
            column_position=0,
        ),
        create_table_column(
            canonical_key="quantity",
            sample_values=[5, 10, 15],
            column_position=1,
        ),
    ]
    table = create_table(columns=columns)
    template = create_template(
        sheet_name="Sheet1",
        tables=[table],
        total_header_fields=0,
        matched_header_fields=0,
        unmatched_header_fields=0,
        total_tables=1,
        total_line_items=0,
    )

    output = build_normalized_output(template)

    cols = output["tables"][0]["columns"]
    assert cols[0]["sample_values"] == ["Widget A", "Widget B", "Widget C"]
    assert cols[1]["sample_values"] == [5, 10, 15]


def test_build_normalized_output_none_template():
    """Test that None template raises ValueError."""
    with pytest.raises(ValueError, match="canonical_template cannot be None"):
        build_normalized_output(None)
