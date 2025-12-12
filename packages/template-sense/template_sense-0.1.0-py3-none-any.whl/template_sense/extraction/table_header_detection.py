"""
Table header row detection for Template Sense.

This module implements heuristic-based detection of table header rows within
detected table candidate blocks. It identifies which row contains column labels
(e.g., "Item", "Quantity", "Price") without attempting semantic classification.

IMPORTANT: This module uses ONLY structural patterns (text density, cell consistency).
It does NOT:
- Call any AI services
- Perform semantic classification of column meanings
- Interpret field names or values
- Use hardcoded field names or keywords

This module DOES:
- Identify the most likely header row within a table block
- Score rows based on text density, cell consistency, and positioning
- Return structured output ready for AI consumption
- Support multilingual content (content-agnostic)

Functions:
    score_row_as_header: Score a single row's likelihood of being a table header
    detect_table_header_row: Main entry point for header row detection

Usage Example:
    from template_sense.extraction.table_candidates import detect_table_candidate_blocks
    from template_sense.extraction.table_header_detection import detect_table_header_row
    from template_sense.extraction.sheet_extractor import extract_raw_grid
    from template_sense.file_loader import load_excel_file
    from template_sense.adapters.excel_adapter import ExcelWorkbook

    raw_workbook = load_excel_file(Path("invoice.xlsx"))
    workbook = ExcelWorkbook(raw_workbook)
    grid = extract_raw_grid(workbook, "Sheet1")

    table_blocks = detect_table_candidate_blocks(grid)
    for block in table_blocks:
        header_info = detect_table_header_row(block)
        if header_info:
            print(f"Header row: {header_info.row_index}, values: {header_info.values}")
"""

import logging
from dataclasses import dataclass
from typing import Any

from template_sense.constants import DEFAULT_TABLE_HEADER_MIN_SCORE
from template_sense.extraction.table_candidates import TableCandidateBlock

# Set up module logger
logger = logging.getLogger(__name__)


@dataclass
class TableHeaderInfo:
    """
    Represents a detected table header row.

    A table header row contains column labels (e.g., "Item", "Quantity", "Price")
    that describe the meaning of each column in the table.

    Attributes:
        row_index: Absolute row index (1-based, Excel convention) in the original sheet
        col_start: Starting column index (1-based) of the header
        col_end: Ending column index (1-based) of the header
        values: List of raw header cell values (in column order)
        score: Confidence score (0.0-1.0) indicating likelihood this is the header row
        detected_pattern: Description of detection heuristic (e.g., "first_row_text_dense")
    """

    row_index: int
    col_start: int
    col_end: int
    values: list[Any]
    score: float
    detected_pattern: str


def _calculate_text_density(row: list[Any]) -> float:
    """
    Calculate the ratio of text (non-numeric) cells to non-empty cells.

    Header rows are typically text-heavy (column labels like "Item", "Quantity").
    Data rows tend to have more numbers.

    Args:
        row: List of cell values

    Returns:
        Text density ratio (0.0-1.0)
    """
    non_empty_cells = [cell for cell in row if cell not in (None, "")]

    if not non_empty_cells:
        return 0.0

    text_count = 0
    for cell in non_empty_cells:
        # String values that aren't purely numeric
        if isinstance(cell, str):
            try:
                float(cell.strip())
                # It's a numeric string, don't count as text
            except (ValueError, AttributeError):
                # It's text
                text_count += 1
        # Non-numeric types (dates, booleans, etc. are considered "text" for headers)
        elif not isinstance(cell, int | float):
            text_count += 1

    return text_count / len(non_empty_cells)


def _calculate_cell_density(row: list[Any]) -> float:
    """
    Calculate the ratio of non-empty cells to total cells in a row.

    Header rows tend to be densely populated (most columns have labels).

    Args:
        row: List of cell values

    Returns:
        Density ratio (0.0-1.0)
    """
    if not row:
        return 0.0

    non_empty_count = sum(1 for cell in row if cell not in (None, ""))
    return non_empty_count / len(row)


def _has_consistent_cell_length(row: list[Any]) -> bool:
    """
    Check if row has cells with consistent character lengths.

    Header cells tend to be similar in length (e.g., "Item", "Price", "Total").
    Data rows often have varied lengths (e.g., "Widget X", 10, 25.50, 255.00).

    Args:
        row: List of cell values

    Returns:
        True if cells have consistent length, False otherwise
    """
    non_empty_cells = [cell for cell in row if cell not in (None, "")]

    if len(non_empty_cells) < 2:
        return False

    lengths = [len(str(cell)) for cell in non_empty_cells]
    avg_length = sum(lengths) / len(lengths)

    # Check if most cells are within 50% of average length
    consistent_count = sum(1 for length in lengths if abs(length - avg_length) <= avg_length * 0.5)

    return consistent_count / len(lengths) >= 0.7


def _is_all_caps_or_title_case(text: str) -> bool:
    """
    Check if text is all caps or title case.

    Headers often use special casing: "ITEM", "QTY", "Item Name", "Unit Price".

    Args:
        text: Text to check

    Returns:
        True if all caps or title case, False otherwise
    """
    if not isinstance(text, str) or len(text.strip()) == 0:
        return False

    text = text.strip()

    # All caps (at least 2 letters)
    if text.isupper() and sum(1 for c in text if c.isalpha()) >= 2:
        return True

    # Title case (each word starts with capital)
    words = text.split()
    if len(words) > 0:
        title_case_words = sum(1 for word in words if word and word[0].isupper())
        return title_case_words / len(words) >= 0.7

    return False


def score_row_as_header(row: list[Any], row_index: int, is_first_row: bool) -> float:
    """
    Score a single row's likelihood of being a table header row.

    This function uses ONLY field-agnostic structural heuristics. It does NOT
    check for specific field names or keywords.

    Scoring criteria (all field-agnostic):
    - High text density (>70% text) → +0.4 (headers are text labels)
    - Moderate text density (40-70% text) → +0.2
    - High cell density (>70% filled) → +0.3 (headers are complete)
    - Consistent cell length → +0.2 (header labels are similar length)
    - First row in table → +0.2 (headers usually first)
    - Special casing (all caps/title case) → +0.1 (headers often formatted)
    - Very low text density (<30%) → -0.4 (likely data row)
    - All numeric → -0.5 (definitely not header)

    Args:
        row: List of cell values (Any type: str, int, float, datetime, None, etc.)
        row_index: 1-based row index (for logging/debugging)
        is_first_row: True if this is the first row in the table block

    Returns:
        Score from 0.0 to 1.0 (clamped)
    """
    score = 0.0
    pattern_details = []

    # Count non-empty cells
    non_empty_cells = [cell for cell in row if cell not in (None, "")]

    if not non_empty_cells:
        return 0.0  # Empty row

    # Calculate metrics
    text_density = _calculate_text_density(row)
    cell_density = _calculate_cell_density(row)
    has_consistent_length = _has_consistent_cell_length(row)

    # Heuristic 1: High text density (headers are text labels, not numbers)
    if text_density > 0.7:
        score += 0.4
        pattern_details.append("high_text_density")
    elif text_density >= 0.4:
        score += 0.2
        pattern_details.append("moderate_text_density")
    elif text_density < 0.3:
        # Very low text density - likely a data row
        score -= 0.4
        pattern_details.append("low_text_density")

    # Heuristic 2: All numeric check (definitely not a header)
    if text_density == 0.0:
        score -= 0.5
        pattern_details.append("all_numeric")

    # Heuristic 3: High cell density (headers are usually complete)
    if cell_density > 0.7:
        score += 0.3
        pattern_details.append("high_cell_density")

    # Heuristic 4: Consistent cell length (header labels are similar)
    if has_consistent_length:
        score += 0.2
        pattern_details.append("consistent_length")

    # Heuristic 5: First row bonus (headers are usually first)
    if is_first_row:
        score += 0.2
        pattern_details.append("first_row")

    # Heuristic 6: Special casing (all caps or title case)
    special_casing_count = sum(
        1 for cell in non_empty_cells if isinstance(cell, str) and _is_all_caps_or_title_case(cell)
    )
    if special_casing_count > 0 and special_casing_count / len(non_empty_cells) >= 0.5:
        score += 0.1
        pattern_details.append("special_casing")

    # Clamp score to 0.0-1.0 range
    score = max(0.0, min(1.0, score))

    logger.debug(
        "Row %d scored %.2f as header candidate (patterns: %s, "
        "text_density: %.2f, cell_density: %.2f, cells: %d)",
        row_index,
        score,
        ", ".join(pattern_details) if pattern_details else "none",
        text_density,
        cell_density,
        len(non_empty_cells),
    )

    return score


def detect_table_header_row(
    table_block: TableCandidateBlock,
    min_score: float = DEFAULT_TABLE_HEADER_MIN_SCORE,
) -> TableHeaderInfo | None:
    """
    Detect the most likely table header row within a table candidate block.

    This function analyzes all rows in the table block and identifies which row
    is most likely to contain column labels (e.g., "Item", "Quantity", "Price").

    Important: This function does NOT perform semantic classification. It only
    identifies structural patterns that suggest a header row.

    Args:
        table_block: TableCandidateBlock from table candidate detection
        min_score: Minimum score threshold (0.0-1.0) for header row. Default: 0.6

    Returns:
        TableHeaderInfo if a header row is found above threshold, None otherwise

    Raises:
        ValueError: If min_score is not in range 0.0-1.0

    Example:
        >>> from template_sense.extraction.table_candidates import detect_table_candidate_blocks
        >>> blocks = detect_table_candidate_blocks(grid)
        >>> header_info = detect_table_header_row(blocks[0])
        >>> if header_info:
        ...     print(f"Header at row {header_info.row_index}: {header_info.values}")
        Header at row 5: ['Item', 'Quantity', 'Price', 'Amount']
    """
    # Validate inputs
    if not 0.0 <= min_score <= 1.0:
        raise ValueError(f"min_score must be in range 0.0-1.0, got {min_score}")

    logger.info(
        "Detecting table header row in block R%d:R%d (min_score=%.2f)",
        table_block.row_start,
        table_block.row_end,
        min_score,
    )

    # Extract grid data from table block content
    # Reconstruct rows from content tuples (row_idx, col_idx, value)
    row_data: dict[int, dict[int, Any]] = {}

    for row_idx, col_idx, value in table_block.content:
        if row_idx not in row_data:
            row_data[row_idx] = {}
        row_data[row_idx][col_idx] = value

    # Build normalized rows (list of lists) for scoring
    rows_to_score = []
    for row_idx in range(table_block.row_start, table_block.row_end + 1):
        # Build row with proper column range
        row = []
        for col_idx in range(table_block.col_start, table_block.col_end + 1):
            cell_value = row_data.get(row_idx, {}).get(col_idx, None)
            row.append(cell_value)

        rows_to_score.append((row_idx, row))

    if not rows_to_score:
        logger.info("No rows to score in table block")
        return None

    # Score each row
    best_score = 0.0
    best_row_idx = None
    best_row_values = None

    for idx, (row_idx, row) in enumerate(rows_to_score):
        is_first_row = idx == 0
        score = score_row_as_header(row, row_idx, is_first_row)

        logger.debug("Row %d scored %.2f as header", row_idx, score)

        if score > best_score:
            best_score = score
            best_row_idx = row_idx
            best_row_values = row

    # Check if best score meets threshold
    if best_score < min_score:
        logger.info(
            "No header row found above threshold (best score: %.2f < %.2f)",
            best_score,
            min_score,
        )
        return None

    # Determine primary detection pattern
    text_density = _calculate_text_density(best_row_values)
    cell_density = _calculate_cell_density(best_row_values)
    is_first = best_row_idx == table_block.row_start

    if is_first and text_density > 0.7:
        pattern = "first_row_text_dense"
    elif text_density > 0.7:
        pattern = "high_text_density"
    elif is_first and cell_density > 0.7:
        pattern = "first_row_dense"
    else:
        pattern = "text_and_density"

    logger.info(
        "Detected header row at R%d (score: %.2f, pattern: %s)",
        best_row_idx,
        best_score,
        pattern,
    )

    return TableHeaderInfo(
        row_index=best_row_idx,
        col_start=table_block.col_start,
        col_end=table_block.col_end,
        values=best_row_values,
        score=best_score,
        detected_pattern=pattern,
    )


__all__ = [
    "TableHeaderInfo",
    "score_row_as_header",
    "detect_table_header_row",
]
