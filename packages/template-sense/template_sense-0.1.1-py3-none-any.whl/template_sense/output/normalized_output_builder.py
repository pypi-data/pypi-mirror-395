"""
Normalized Output Builder for Template Sense.

This module transforms the internal canonical template representation into a
normalized, public-facing JSON output that Tako's backend can consume directly.

Architecture Position: Extraction → AI → Translation → Mapping → Aggregation → **OUTPUT**

This module does NOT:
- Call any AI services
- Perform any data transformation beyond serialization
- Make external API calls
- Modify input data

This module DOES:
- Convert internal dataclasses to JSON-serializable dicts
- Partition headers into matched/unmatched groups
- Filter out internal metrics (confidence scores, matching variants, detection info)
- Preserve essential fields for Tako processing and template export
- Produce deterministic, versioned output
- Ensure complete JSON serialization compatibility

Functions:
    build_normalized_output: Main transformation function that converts CanonicalTemplate to JSON dict

Usage Example:
    from template_sense.output.normalized_output_builder import build_normalized_output

    output = build_normalized_output(canonical_template)
    json.dumps(output)  # Ready for API response
"""

import logging
from typing import Any

from template_sense.constants import OUTPUT_SCHEMA_VERSION
from template_sense.output.canonical_aggregator import (
    CanonicalHeaderField,
    CanonicalLineItem,
    CanonicalTable,
    CanonicalTableColumn,
    CanonicalTemplate,
)

# Set up module logger
logger = logging.getLogger(__name__)


def _serialize_header_field(field: CanonicalHeaderField) -> dict[str, Any]:
    """
    Convert a CanonicalHeaderField to a JSON-serializable dict.

    Args:
        field: CanonicalHeaderField instance to serialize.

    Returns:
        dict: JSON-serializable representation of the header field.

    Example:
        >>> field = CanonicalHeaderField(
        ...     canonical_key="invoice_number",
        ...     original_label="請求書番号",
        ...     translated_label="Invoice Number",
        ...     value="INV-12345",
        ...     heuristic_block_index=0,
        ...     ai_confidence=0.95,
        ...     fuzzy_match_score=87.5,
        ...     matched_variant="Invoice No",
        ...     row_index=1,
        ...     col_index=2,
        ...     metadata={}
        ... )
        >>> result = _serialize_header_field(field)
        >>> result["canonical_key"]
        'invoice_number'
    """
    result = {
        "canonical_key": field.canonical_key,
        "original_label": field.original_label,
        "translated_label": field.translated_label,
        "value": field.value,
        "location": {"row": field.row_index, "col": field.col_index},
    }

    # Only include metadata if non-empty
    if field.metadata:
        result["metadata"] = field.metadata

    return result


def _serialize_table_column(column: CanonicalTableColumn) -> dict[str, Any]:
    """
    Convert a CanonicalTableColumn to a JSON-serializable dict.

    Args:
        column: CanonicalTableColumn instance to serialize.

    Returns:
        dict: JSON-serializable representation of the table column.

    Example:
        >>> column = CanonicalTableColumn(
        ...     canonical_key="product_name",
        ...     original_label="商品名",
        ...     translated_label="Product Name",
        ...     column_position=0,
        ...     sample_values=["Widget A", "Widget B"],
        ...     ai_confidence=0.9,
        ...     fuzzy_match_score=92.0,
        ...     matched_variant="Product",
        ...     row_index=5,
        ...     col_index=1,
        ...     metadata={}
        ... )
        >>> result = _serialize_table_column(column)
        >>> result["canonical_key"]
        'product_name'
    """
    result = {
        "canonical_key": column.canonical_key,
        "original_label": column.original_label,
        "translated_label": column.translated_label,
        "column_position": column.column_position,
        "sample_values": column.sample_values,
        "location": {"row": column.row_index, "col": column.col_index},
    }

    # Only include metadata if non-empty
    if column.metadata:
        result["metadata"] = column.metadata

    return result


def _serialize_line_item(item: CanonicalLineItem) -> dict[str, Any]:
    """
    Convert a CanonicalLineItem to a JSON-serializable dict.

    Args:
        item: CanonicalLineItem instance to serialize.

    Returns:
        dict: JSON-serializable representation of the line item.

    Example:
        >>> item = CanonicalLineItem(
        ...     row_index=6,
        ...     line_number=1,
        ...     columns={"product_name": "Widget A", "quantity": 5},
        ...     is_subtotal=False,
        ...     ai_confidence=0.88,
        ...     metadata={}
        ... )
        >>> result = _serialize_line_item(item)
        >>> result["row_index"]
        6
    """
    result = {
        "row_index": item.row_index,
        "line_number": item.line_number,
        "columns": item.columns,
        "is_subtotal": item.is_subtotal,
    }

    # Only include metadata if non-empty
    if item.metadata:
        result["metadata"] = item.metadata

    return result


def _serialize_table(table: CanonicalTable, table_index: int) -> dict[str, Any]:
    """
    Convert a CanonicalTable to a JSON-serializable dict.

    Args:
        table: CanonicalTable instance to serialize.
        table_index: Index of this table in the tables list.

    Returns:
        dict: JSON-serializable representation of the table.

    Example:
        >>> table = CanonicalTable(
        ...     table_block_index=0,
        ...     row_start=5,
        ...     row_end=10,
        ...     col_start=1,
        ...     col_end=5,
        ...     columns=[...],
        ...     line_items=[...],
        ...     heuristic_score=0.9,
        ...     detected_pattern="numeric_density",
        ...     metadata={}
        ... )
        >>> result = _serialize_table(table, 0)
        >>> result["table_index"]
        0
    """
    # Serialize columns
    serialized_columns = [_serialize_table_column(col) for col in table.columns]

    # Serialize line items
    serialized_line_items = [_serialize_line_item(item) for item in table.line_items]

    result = {
        "table_index": table_index,
        "location": {
            "row_start": table.row_start,
            "row_end": table.row_end,
            "col_start": table.col_start,
            "col_end": table.col_end,
        },
        "columns": serialized_columns,
        "line_items": serialized_line_items,
    }

    # Only include metadata if non-empty
    if table.metadata:
        result["metadata"] = table.metadata

    return result


def _partition_headers(
    header_fields: list[CanonicalHeaderField],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """
    Partition header fields into matched and unmatched groups.

    A header is considered "matched" if it has a non-None canonical_key.

    Args:
        header_fields: List of CanonicalHeaderField instances.

    Returns:
        tuple: (matched_headers, unmatched_headers) as lists of serialized dicts.

    Example:
        >>> headers = [
        ...     CanonicalHeaderField(canonical_key="invoice_number", ...),  # matched
        ...     CanonicalHeaderField(canonical_key=None, ...),  # unmatched
        ... ]
        >>> matched, unmatched = _partition_headers(headers)
        >>> len(matched)
        1
        >>> len(unmatched)
        1
    """
    matched: list[dict[str, Any]] = []
    unmatched: list[dict[str, Any]] = []

    for field in header_fields:
        serialized = _serialize_header_field(field)

        if field.canonical_key is not None:
            matched.append(serialized)
        else:
            unmatched.append(serialized)

    return matched, unmatched


def build_normalized_output(
    canonical_template: CanonicalTemplate,
    version: str = OUTPUT_SCHEMA_VERSION,
) -> dict[str, Any]:
    """
    Convert a CanonicalTemplate to a normalized, public-facing JSON output.

    This is the final transformation step that converts the internal canonical
    representation to the public API output format that Tako consumes.

    The output is guaranteed to be JSON-serializable (no custom types) and
    includes versioning for backwards compatibility.

    Args:
        canonical_template: CanonicalTemplate instance to convert.
        version: Output schema version string (default: OUTPUT_SCHEMA_VERSION from constants).

    Returns:
        dict: JSON-serializable output with the following structure:
            {
                "version": str,
                "sheet_name": str,
                "headers": {
                    "matched": list[dict],
                    "unmatched": list[dict]
                },
                "tables": list[dict],
                "summary": {
                    "total_header_fields": int,
                    "matched_header_fields": int,
                    "unmatched_header_fields": int,
                    "total_tables": int,
                    "total_line_items": int
                },
                "metadata": dict
            }

    Raises:
        ValueError: If canonical_template is None.

    Example:
        >>> from template_sense.output.canonical_aggregator import CanonicalTemplate
        >>> template = CanonicalTemplate(
        ...     sheet_name="Sheet1",
        ...     header_fields=[...],
        ...     tables=[...],
        ...     total_header_fields=5,
        ...     matched_header_fields=3,
        ...     unmatched_header_fields=2,
        ...     total_tables=1,
        ...     total_line_items=10,
        ...     metadata={}
        ... )
        >>> output = build_normalized_output(template)
        >>> output["version"]
        '1.0'
        >>> output["sheet_name"]
        'Sheet1'
        >>> import json
        >>> json.dumps(output)  # Verify JSON-serializable
    """
    # Input validation
    if canonical_template is None:
        raise ValueError("canonical_template cannot be None")

    logger.info(
        f"Building normalized output for sheet '{canonical_template.sheet_name}': "
        f"{canonical_template.total_header_fields} headers, "
        f"{canonical_template.total_tables} tables, "
        f"{canonical_template.total_line_items} line items"
    )

    # Partition headers into matched/unmatched
    matched_headers, unmatched_headers = _partition_headers(canonical_template.header_fields)

    logger.debug(
        f"Partitioned headers: {len(matched_headers)} matched, "
        f"{len(unmatched_headers)} unmatched"
    )

    # Serialize tables
    serialized_tables = [
        _serialize_table(table, idx) for idx, table in enumerate(canonical_template.tables)
    ]

    logger.debug(f"Serialized {len(serialized_tables)} tables")

    # Build summary statistics
    summary = {
        "total_header_fields": canonical_template.total_header_fields,
        "matched_header_fields": canonical_template.matched_header_fields,
        "unmatched_header_fields": canonical_template.unmatched_header_fields,
        "total_tables": canonical_template.total_tables,
        "total_line_items": canonical_template.total_line_items,
    }

    # Build final output
    output = {
        "version": version,
        "sheet_name": canonical_template.sheet_name,
        "headers": {
            "matched": matched_headers,
            "unmatched": unmatched_headers,
        },
        "tables": serialized_tables,
        "summary": summary,
        "metadata": canonical_template.metadata,
    }

    logger.info(
        f"Successfully built normalized output: version={version}, "
        f"matched={len(matched_headers)}, unmatched={len(unmatched_headers)}, "
        f"tables={len(serialized_tables)}"
    )

    return output
