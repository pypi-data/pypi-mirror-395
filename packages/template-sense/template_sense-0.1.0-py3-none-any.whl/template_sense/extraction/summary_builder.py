"""
Sheet structure summary builder for Template Sense.

This module aggregates outputs from header detection, table detection, and table
header row detection into a single, compact, AI-ready JSON structure. The summary
builder produces normalized, minimal representations suitable for AI consumption
without sending full sheet grids.

This module does NOT:
- Call any AI services
- Perform semantic classification
- Modify or interpret field values
- Include unnecessary grid data

This module DOES:
- Aggregate detection results from multiple modules
- Normalize coordinates and data structures
- Validate block consistency
- Filter out low-scoring or empty blocks
- Return deterministic, JSON-serializable outputs

Functions:
    build_sheet_summary: Main entry point for building sheet structure summary
    normalize_header_blocks: Convert HeaderCandidateBlock list to JSON dicts
    normalize_table_blocks: Convert TableCandidateBlock list to JSON dicts

Usage Example:
    from pathlib import Path
    from template_sense.file_loader import load_excel_file
    from template_sense.adapters.excel_adapter import ExcelWorkbook
    from template_sense.extraction.summary_builder import build_sheet_summary

    # Load workbook
    raw_workbook = load_excel_file(Path("invoice.xlsx"))
    workbook = ExcelWorkbook(raw_workbook)

    # Build summary
    summary = build_sheet_summary(workbook, sheet_name="Sheet1")
    print(summary)
    # {
    #     "sheet_name": "Sheet1",
    #     "header_blocks": [...],
    #     "table_blocks": [...]
    # }
"""

import logging
from typing import Any

from template_sense.adapters.excel_adapter import ExcelWorkbook
from template_sense.constants import DEFAULT_CONFIDENCE_THRESHOLD
from template_sense.errors import ExtractionError
from template_sense.extraction.header_candidates import (
    HeaderCandidateBlock,
    detect_header_candidate_blocks,
)
from template_sense.extraction.sheet_extractor import extract_raw_grid
from template_sense.extraction.table_candidates import (
    TableCandidateBlock,
    detect_table_candidate_blocks,
)
from template_sense.extraction.table_header_detection import (
    TableHeaderInfo,
    detect_table_header_row,
)

# Set up module logger
logger = logging.getLogger(__name__)


def _validate_block_coordinates(
    block: HeaderCandidateBlock | TableCandidateBlock,
) -> bool:
    """
    Validate that block coordinates are consistent and valid.

    Checks:
    - row_start <= row_end
    - col_start <= col_end
    - All coordinates > 0 (1-based Excel convention)
    - Block has non-empty content

    Args:
        block: HeaderCandidateBlock or TableCandidateBlock to validate

    Returns:
        True if coordinates are valid, False otherwise
    """
    # Check row coordinates
    if block.row_start > block.row_end:
        logger.warning(
            "Invalid block coordinates: row_start (%d) > row_end (%d)",
            block.row_start,
            block.row_end,
        )
        return False

    # Check column coordinates
    if block.col_start > block.col_end:
        logger.warning(
            "Invalid block coordinates: col_start (%d) > col_end (%d)",
            block.col_start,
            block.col_end,
        )
        return False

    # Check all coordinates are positive (1-based)
    if block.row_start < 1 or block.col_start < 1:
        logger.warning(
            "Invalid block coordinates: coordinates must be >= 1 (1-based), "
            "got row_start=%d, col_start=%d",
            block.row_start,
            block.col_start,
        )
        return False

    # Check block has content
    if not block.content:
        logger.warning("Invalid block: content is empty")
        return False

    return True


def _convert_value_to_primitive(value: Any) -> Any:
    """
    Convert value to JSON-serializable Python primitive.

    Ensures no openpyxl objects or non-serializable types leak through.
    Handles datetime, date, time, and other special types.

    Args:
        value: Value to convert (any type)

    Returns:
        JSON-serializable primitive (str, int, float, bool, None, list, dict)
    """
    # None is already primitive
    if value is None:
        return None

    # Basic primitives
    if isinstance(value, str | int | float | bool):
        return value

    # Handle datetime objects (convert to ISO string)
    if hasattr(value, "isoformat"):
        return value.isoformat()

    # Lists and dicts (recursively convert)
    if isinstance(value, list):
        return [_convert_value_to_primitive(item) for item in value]

    if isinstance(value, dict):
        return {key: _convert_value_to_primitive(val) for key, val in value.items()}

    # Fallback: convert to string
    logger.debug(
        "Converting non-primitive value of type %s to string: %s",
        type(value).__name__,
        repr(value),
    )
    return str(value)


def normalize_header_blocks(
    blocks: list[HeaderCandidateBlock],
    min_score: float = DEFAULT_CONFIDENCE_THRESHOLD,
) -> list[dict[str, Any]]:
    """
    Convert HeaderCandidateBlock dataclasses to JSON-serializable dicts.

    Validates coordinates, filters by score, and ensures all values are primitives.
    Returns normalized, AI-ready header block representations.

    Args:
        blocks: List of HeaderCandidateBlock instances from detection
        min_score: Minimum score threshold (0.0-1.0) to include blocks. Default: 0.7

    Returns:
        List of normalized header block dicts, sorted by row_start.
        Each dict contains:
        - row_start: int (1-based)
        - row_end: int (1-based)
        - col_start: int (1-based)
        - col_end: int (1-based)
        - content: list of [row, col, value] tuples (all primitives)
        - label_value_pairs: list of {label, value, row, col} dicts
        - score: float
        - detected_pattern: str

    Example:
        >>> blocks = detect_header_candidate_blocks(grid)
        >>> normalized = normalize_header_blocks(blocks)
        >>> print(normalized[0])
        {
            "row_start": 1,
            "row_end": 3,
            "col_start": 1,
            "col_end": 5,
            "content": [[1, 1, "Invoice: 12345"], [2, 1, "Date: 2024-01-01"]],
            "label_value_pairs": [
                {"label": "Invoice", "value": "12345", "row": 1, "col": 1},
                ...
            ],
            "score": 0.85,
            "detected_pattern": "key_value_and_keywords"
        }
    """
    logger.debug(
        "Normalizing %d header blocks (min_score=%.2f)",
        len(blocks),
        min_score,
    )

    normalized_blocks = []

    for block in blocks:
        # Validate coordinates
        if not _validate_block_coordinates(block):
            logger.warning(
                "Skipping header block at R%d:R%d due to invalid coordinates",
                block.row_start,
                block.row_end,
            )
            continue

        # Filter by score
        if block.score < min_score:
            logger.debug(
                "Skipping header block at R%d:R%d with score %.2f (below threshold %.2f)",
                block.row_start,
                block.row_end,
                block.score,
                min_score,
            )
            continue

        # Convert content tuples to primitives
        normalized_content = [
            [row, col, _convert_value_to_primitive(value)] for row, col, value in block.content
        ]

        # Convert label_value_pairs to dicts with primitives
        normalized_pairs = [
            {
                "label": _convert_value_to_primitive(label),
                "value": _convert_value_to_primitive(value),
                "row": row,
                "col": col,
            }
            for label, value, row, col in block.label_value_pairs
        ]

        normalized_block = {
            "row_start": block.row_start,
            "row_end": block.row_end,
            "col_start": block.col_start,
            "col_end": block.col_end,
            "content": normalized_content,
            "label_value_pairs": normalized_pairs,
            "score": round(block.score, 3),  # Round to 3 decimal places for consistency
            "detected_pattern": block.detected_pattern,
        }

        normalized_blocks.append(normalized_block)
        logger.debug(
            "Normalized header block at R%d:R%d (score: %.2f, pattern: %s)",
            block.row_start,
            block.row_end,
            block.score,
            block.detected_pattern,
        )

    # Sort by row_start for deterministic output
    normalized_blocks.sort(key=lambda b: b["row_start"])

    logger.info(
        "Normalized %d header blocks (filtered %d below threshold)",
        len(normalized_blocks),
        len(blocks) - len(normalized_blocks),
    )

    return normalized_blocks


def normalize_table_blocks(
    table_blocks: list[TableCandidateBlock],
    table_headers: dict[int, TableHeaderInfo | None],
    min_score: float = DEFAULT_CONFIDENCE_THRESHOLD,
) -> list[dict[str, Any]]:
    """
    Convert TableCandidateBlock dataclasses to JSON-serializable dicts.

    Validates coordinates, merges with detected header rows, filters by score,
    and ensures all values are primitives. Returns normalized, AI-ready table
    block representations.

    Args:
        table_blocks: List of TableCandidateBlock instances from detection
        table_headers: Dict mapping table row_start to TableHeaderInfo (or None)
        min_score: Minimum score threshold (0.0-1.0) to include blocks. Default: 0.7

    Returns:
        List of normalized table block dicts, sorted by row_start.
        Each dict contains:
        - row_start: int (1-based)
        - row_end: int (1-based)
        - col_start: int (1-based)
        - col_end: int (1-based)
        - header_row: dict or None (if header detected)
        - content: list of [row, col, value] tuples (all primitives)
        - score: float
        - detected_pattern: str

    Example:
        >>> table_blocks = detect_table_candidate_blocks(grid)
        >>> headers = {block.row_start: detect_table_header_row(block) for block in table_blocks}
        >>> normalized = normalize_table_blocks(table_blocks, headers)
        >>> print(normalized[0])
        {
            "row_start": 10,
            "row_end": 15,
            "col_start": 1,
            "col_end": 4,
            "header_row": {
                "row_index": 10,
                "values": ["Item", "Quantity", "Price", "Amount"],
                "score": 0.92,
                "detected_pattern": "first_row_text_dense"
            },
            "content": [[10, 1, "Item"], [10, 2, "Quantity"], ...],
            "score": 0.78,
            "detected_pattern": "high_numeric_density"
        }
    """
    logger.debug(
        "Normalizing %d table blocks (min_score=%.2f)",
        len(table_blocks),
        min_score,
    )

    normalized_blocks = []

    for block in table_blocks:
        # Validate coordinates
        if not _validate_block_coordinates(block):
            logger.warning(
                "Skipping table block at R%d:R%d due to invalid coordinates",
                block.row_start,
                block.row_end,
            )
            continue

        # Filter by score
        if block.score < min_score:
            logger.debug(
                "Skipping table block at R%d:R%d with score %.2f (below threshold %.2f)",
                block.row_start,
                block.row_end,
                block.score,
                min_score,
            )
            continue

        # Convert content tuples to primitives
        normalized_content = [
            [row, col, _convert_value_to_primitive(value)] for row, col, value in block.content
        ]

        # Get header info for this table (if detected)
        header_info = table_headers.get(block.row_start)
        normalized_header = None

        if header_info:
            normalized_header = {
                "row_index": header_info.row_index,
                "col_start": header_info.col_start,
                "col_end": header_info.col_end,
                "values": [_convert_value_to_primitive(val) for val in header_info.values],
                "score": round(header_info.score, 3),
                "detected_pattern": header_info.detected_pattern,
            }
            logger.debug(
                "Table block at R%d:R%d has header row at R%d (score: %.2f)",
                block.row_start,
                block.row_end,
                header_info.row_index,
                header_info.score,
            )

        normalized_block = {
            "row_start": block.row_start,
            "row_end": block.row_end,
            "col_start": block.col_start,
            "col_end": block.col_end,
            "header_row": normalized_header,
            "content": normalized_content,
            "score": round(block.score, 3),  # Round to 3 decimal places for consistency
            "detected_pattern": block.detected_pattern,
        }

        normalized_blocks.append(normalized_block)
        logger.debug(
            "Normalized table block at R%d:R%d (score: %.2f, pattern: %s, has_header: %s)",
            block.row_start,
            block.row_end,
            block.score,
            block.detected_pattern,
            normalized_header is not None,
        )

    # Sort by row_start for deterministic output
    normalized_blocks.sort(key=lambda b: b["row_start"])

    logger.info(
        "Normalized %d table blocks (filtered %d below threshold)",
        len(normalized_blocks),
        len(table_blocks) - len(normalized_blocks),
    )

    return normalized_blocks


def build_sheet_summary(
    workbook: ExcelWorkbook,
    sheet_name: str | None = None,
    min_score: float = DEFAULT_CONFIDENCE_THRESHOLD,
) -> dict[str, Any]:
    """
    Build a complete, AI-ready sheet structure summary.

    This is the main entry point for aggregating header detection, table detection,
    and table header row detection into a single normalized JSON structure.

    The summary is compact, minimal, and deterministic:
    - Only includes structures scoring above min_score
    - All coordinates are validated and consistent
    - All values are JSON-serializable primitives
    - Output is sorted for deterministic ordering

    Orchestration flow:
    1. Extract raw grid from sheet
    2. Detect table candidate blocks
    3. Detect header candidate blocks (using table exclusion approach)
    4. Detect table header rows for each table block
    5. Normalize and aggregate into summary dict

    Args:
        workbook: ExcelWorkbook instance to analyze
        sheet_name: Name of sheet to analyze. If None, uses first visible sheet.
        min_score: Minimum score threshold (0.0-1.0) for including blocks. Default: 0.7

    Returns:
        Summary dict with structure:
        {
            "sheet_name": str,
            "header_blocks": list[dict],
            "table_blocks": list[dict]
        }

    Raises:
        ValueError: If min_score is not in range 0.0-1.0
        ExtractionError: If sheet doesn't exist or extraction fails

    Example:
        >>> from template_sense.file_loader import load_excel_file
        >>> from template_sense.adapters.excel_adapter import ExcelWorkbook
        >>> raw_wb = load_excel_file(Path("invoice.xlsx"))
        >>> wb = ExcelWorkbook(raw_wb)
        >>> summary = build_sheet_summary(wb)
        >>> print(f"Found {len(summary['header_blocks'])} header blocks")
        >>> print(f"Found {len(summary['table_blocks'])} table blocks")
    """
    # Validate min_score
    if not 0.0 <= min_score <= 1.0:
        raise ValueError(f"min_score must be in range 0.0-1.0, got {min_score}")

    # Get sheet name (use first visible sheet if not specified)
    if sheet_name is None:
        visible_sheets = workbook.get_sheet_names()
        if not visible_sheets:
            raise ExtractionError(
                extraction_type="sheet",
                reason="No visible sheets found in workbook",
            )
        sheet_name = visible_sheets[0]
        logger.info("No sheet_name specified, using first visible sheet: '%s'", sheet_name)

    logger.info(
        "Building sheet structure summary for '%s' (min_score=%.2f)",
        sheet_name,
        min_score,
    )

    # Step 1: Extract raw grid
    logger.debug("Step 1/5: Extracting raw grid from sheet '%s'", sheet_name)
    grid = extract_raw_grid(workbook, sheet_name)

    if not grid:
        logger.info("Sheet '%s' is empty, returning empty summary", sheet_name)
        return {
            "sheet_name": sheet_name,
            "header_blocks": [],
            "table_blocks": [],
        }

    logger.debug("Extracted grid with %d rows", len(grid))

    # Step 2: Detect table candidate blocks
    logger.debug("Step 2/5: Detecting table candidate blocks")
    table_blocks = detect_table_candidate_blocks(grid, min_score=min_score)
    logger.info("Detected %d table candidate blocks", len(table_blocks))

    # Step 3: Detect header candidate blocks (using table exclusion approach)
    logger.debug("Step 3/5: Detecting header candidate blocks (table exclusion)")
    header_blocks = detect_header_candidate_blocks(
        grid,
        min_score=min_score,
        table_blocks=table_blocks,  # Use table exclusion approach
    )
    logger.info("Detected %d header candidate blocks", len(header_blocks))

    # Step 4: Detect table header rows for each table block
    logger.debug("Step 4/5: Detecting table header rows")
    table_headers: dict[int, TableHeaderInfo | None] = {}

    for table_block in table_blocks:
        header_info = detect_table_header_row(table_block, min_score=min_score)
        table_headers[table_block.row_start] = header_info

        if header_info:
            logger.debug(
                "Detected header row at R%d for table block R%d:R%d",
                header_info.row_index,
                table_block.row_start,
                table_block.row_end,
            )
        else:
            logger.debug(
                "No header row detected for table block R%d:R%d",
                table_block.row_start,
                table_block.row_end,
            )

    # Step 5: Normalize and aggregate
    logger.debug("Step 5/5: Normalizing and aggregating results")

    normalized_headers = normalize_header_blocks(header_blocks, min_score=min_score)
    normalized_tables = normalize_table_blocks(table_blocks, table_headers, min_score=min_score)

    summary = {
        "sheet_name": sheet_name,
        "header_blocks": normalized_headers,
        "table_blocks": normalized_tables,
    }

    logger.info(
        "Sheet structure summary complete for '%s': %d header blocks, %d table blocks",
        sheet_name,
        len(normalized_headers),
        len(normalized_tables),
    )

    return summary


__all__ = [
    "build_sheet_summary",
    "normalize_header_blocks",
    "normalize_table_blocks",
]
