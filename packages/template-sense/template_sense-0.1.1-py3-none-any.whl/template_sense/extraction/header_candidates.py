"""
Global header candidate detection for Template Sense.

This module implements heuristics-only detection of invoice metadata blocks
(header candidate blocks) anywhere on a sheet. Headers refer to metadata regions
like invoice numbers, dates, company names, addresses, shipper/consignee info, etc.

This module does NOT:
- Call any AI services
- Perform semantic classification
- Assume headers are at the top of the sheet

This module DOES:
- Scan the entire grid for metadata-like patterns
- Detect multiple distinct header blocks (e.g., "Bill To" and "Ship To")
- Return structured, deterministic output ready for AI consumption
- Support multilingual content (English, Japanese, etc.)

Functions:
    score_row_as_header_candidate: Score a single row's likelihood of containing metadata
    find_header_candidate_rows: Scan grid and identify high-scoring rows
    cluster_header_candidate_blocks: Group nearby rows into distinct blocks
    detect_header_candidate_blocks: Main entry point for header detection

Usage Example:
    from template_sense.extraction.sheet_extractor import extract_raw_grid
    from template_sense.extraction.header_candidates import detect_header_candidate_blocks
    from template_sense.file_loader import load_excel_file
    from template_sense.adapters.excel_adapter import ExcelWorkbook

    raw_workbook = load_excel_file(Path("invoice.xlsx"))
    workbook = ExcelWorkbook(raw_workbook)
    grid = extract_raw_grid(workbook, "Sheet1")

    blocks = detect_header_candidate_blocks(grid)
    for block in blocks:
        print(f"Header block at R{block.row_start}:R{block.row_end}, "
              f"C{block.col_start}:C{block.col_end}, score={block.score:.2f}")
"""

import logging
import re
from dataclasses import dataclass
from typing import Any

from template_sense.constants import DEFAULT_ADJACENT_CELL_RADIUS
from template_sense.extraction.table_candidates import TableCandidateBlock

# Set up module logger
logger = logging.getLogger(__name__)

# Metadata keywords for pattern detection (English and Japanese)
METADATA_KEYWORDS = {
    # English invoice/document keywords
    "invoice",
    "bill",
    "ship",
    "consignee",
    "shipper",
    "sender",
    "receiver",
    "date",
    "number",
    "total",
    "subtotal",
    "tax",
    "amount",
    "address",
    "company",
    "name",
    "to",
    "from",
    "attention",
    "reference",
    "order",
    "payment",
    "terms",
    "contact",
    "phone",
    "email",
    "fax",
    # Japanese invoice/document keywords
    "請求書",  # Invoice
    "発送",  # Shipping
    "荷受人",  # Consignee
    "荷送人",  # Shipper
    "日付",  # Date
    "番号",  # Number
    "合計",  # Total
    "小計",  # Subtotal
    "税",  # Tax
    "金額",  # Amount
    "住所",  # Address
    "会社",  # Company
    "名前",  # Name
    "宛先",  # To/Destination
    "送信元",  # From/Sender
    "注文",  # Order
    "支払",  # Payment
    "電話",  # Phone
}


@dataclass
class HeaderCandidateBlock:
    """
    Represents a detected invoice metadata block.

    A header candidate block is a region of the sheet that likely contains
    invoice metadata (as opposed to table data). Examples include company info,
    invoice numbers, dates, addresses, shipper/consignee details, etc.

    Attributes:
        row_start: First row of block (1-based, Excel convention)
        row_end: Last row of block (1-based, inclusive)
        col_start: First column of block (1-based, Excel convention)
        col_end: Last column of block (1-based, inclusive)
        content: List of (row, col, value) tuples for all non-empty cells in block
        label_value_pairs: List of detected (label, value, row, col) tuples.
                          For cells without clear labels, label will be None.
        score: Confidence score (0.0-1.0) indicating likelihood this is a header block
        detected_pattern: Description of detection pattern (e.g., "key_value_pairs",
                          "metadata_keywords")
    """

    row_start: int
    row_end: int
    col_start: int
    col_end: int
    content: list[tuple[int, int, Any]]
    label_value_pairs: list[tuple[str | None, Any, int, int]]
    score: float
    detected_pattern: str


def _contains_key_value_pattern(text: str) -> bool:
    """
    Check if text contains key-value separator patterns.

    Patterns include:
    - Colon separator: "Label: Value" or "ラベル: 値"
    - Multi-space separator: "Label    Value" (2+ spaces)

    Args:
        text: Text to check

    Returns:
        True if key-value pattern detected, False otherwise
    """
    if not isinstance(text, str):
        return False

    # Colon pattern: at least one non-whitespace char, colon, optional space, value
    if re.search(r"\S+\s*:\s*\S", text):
        return True

    # Multiple spaces pattern: word, 2+ spaces, word
    return bool(re.search(r"\S+\s{2,}\S", text))


def _contains_metadata_keyword(text: str) -> bool:
    """
    Check if text contains known metadata keywords.

    Args:
        text: Text to check (case-insensitive for English)

    Returns:
        True if metadata keyword found, False otherwise
    """
    if not isinstance(text, str):
        return False

    # Normalize for comparison (lowercase for English)
    text_lower = text.lower()

    # Check for exact keyword matches
    for keyword in METADATA_KEYWORDS:
        # For Japanese keywords, check exact match (case-sensitive)
        if any(ord(c) > 127 for c in keyword):  # Non-ASCII (likely Japanese)
            if keyword in text:
                return True
        # For English keywords, check case-insensitive
        else:
            if keyword in text_lower:
                return True

    return False


def _is_substantial_text(text: str) -> bool:
    """
    Check if text is substantial (not just a number or very short).

    This helps identify text-heavy cells that are likely metadata values
    or labels, as opposed to table cell values.

    Args:
        text: Text to check

    Returns:
        True if text is substantial, False otherwise
    """
    if not isinstance(text, str):
        return False

    text_stripped = text.strip()

    # Must have some length
    if len(text_stripped) < 2:
        return False

    # Must contain at least one letter (not pure numbers/symbols)
    return bool(re.search(r"[a-zA-Z\u3000-\u9fff]", text_stripped))


def _is_label_candidate(cell_value: Any) -> bool:
    """
    Detect if a cell value looks like a label candidate.

    Uses multiple heuristics to identify label-like cells that might need
    pairing with adjacent value cells:
    - Must be a string
    - Must be reasonably short (< 30 characters)
    - Bonus signals: ends with ":", contains metadata keywords

    Args:
        cell_value: Cell value to check

    Returns:
        True if cell looks like a label candidate, False otherwise

    Examples:
        >>> _is_label_candidate("Invoice Number:")
        True
        >>> _is_label_candidate("FROM")
        True
        >>> _is_label_candidate("This is a very long description that spans multiple lines and is too long")
        False
        >>> _is_label_candidate(12345)
        False
    """
    if not isinstance(cell_value, str):
        return False

    text = cell_value.strip()
    if not text or len(text) > 30:
        return False

    # Strong signals for label candidate:
    # 1. Ends with colon (classic label pattern)
    if text.endswith(":"):
        return True

    # 2. Contains metadata keywords
    if _contains_metadata_keyword(text):
        return True

    # 3. Short text with substantial content (letters, not just numbers)
    # This catches cases like "FROM", "TO", "DATE" without colons
    return _is_substantial_text(text) and len(text) <= 20


def _find_adjacent_value(
    grid: list[list[Any]], row_idx: int, col_idx: int, radius: int = 3
) -> tuple[Any, int] | None:
    """
    Search for a non-empty value cell adjacent to a label cell.

    Searches to the right of the label cell within a specified radius.
    Skips empty cells and returns the first non-empty cell found.

    Args:
        grid: 2D list of cell values (list of rows)
        row_idx: 1-based row index of the label cell
        col_idx: 1-based column index of the label cell
        radius: Maximum number of cells to search to the right. Default: 3

    Returns:
        Tuple of (value, column_offset) if value found, None otherwise.
        column_offset is the number of columns from label cell (1, 2, 3, etc.)

    Examples:
        >>> grid = [["Invoice:", "12345", None]]
        >>> _find_adjacent_value(grid, 1, 1, radius=3)
        ("12345", 1)
        >>> grid = [["FROM:", None, None, "TOKYO"]]
        >>> _find_adjacent_value(grid, 1, 1, radius=3)
        ("TOKYO", 3)
        >>> grid = [["TO:", None, None, None, "DUBAI"]]
        >>> _find_adjacent_value(grid, 1, 1, radius=3)
        None  # Value is beyond radius
    """
    # Convert to 0-based index for grid access
    grid_row_idx = row_idx - 1

    # Validate row exists
    if grid_row_idx < 0 or grid_row_idx >= len(grid):
        return None

    row = grid[grid_row_idx]

    # Search right from col_idx+1 up to col_idx+radius
    for offset in range(1, radius + 1):
        search_col_idx = col_idx + offset  # 1-based
        grid_col_idx = search_col_idx - 1  # 0-based

        # Check if column exists
        if grid_col_idx >= len(row):
            break  # Reached end of row

        cell = row[grid_col_idx]

        # Found non-empty cell
        if cell not in (None, ""):
            logger.debug(
                "Found adjacent value at R%dC%d (offset=%d) for label at R%dC%d: %s",
                row_idx,
                search_col_idx,
                offset,
                row_idx,
                col_idx,
                cell,
            )
            return (cell, offset)

    # No value found within radius
    logger.debug(
        "No adjacent value found for label at R%dC%d within radius=%d",
        row_idx,
        col_idx,
        radius,
    )
    return None


def _extract_label_value_from_cell(cell_value: Any) -> tuple[str | None, Any]:
    """
    Try to extract label and value from a single cell.

    Handles patterns like:
    - "Invoice Number: 12345" -> ("Invoice Number", "12345")
    - "Date : 2024-01-01" -> ("Date", "2024-01-01")
    - "FROM : NARITA" -> ("FROM", "NARITA")
    - "Company Name" -> (None, "Company Name") - value only, no label

    Args:
        cell_value: Cell value to parse

    Returns:
        Tuple of (label, value). Label is None if no clear label detected.
    """
    if not isinstance(cell_value, str):
        return (None, cell_value)

    text_stripped = cell_value.strip()

    # Try colon pattern (most common label:value separator)
    if ":" in text_stripped:
        parts = text_stripped.split(":", 1)
        if len(parts) == 2:
            label = parts[0].strip()
            value = parts[1].strip()
            # If value is empty, treat as label only
            if value:
                return (label, value)
            # Colon but no value after it, label only
            return (label, None)

    # No clear label pattern detected, return as value only
    return (None, text_stripped)


def _extract_label_value_pairs(
    grid: list[list[Any]], row_idx: int
) -> list[tuple[str | None, Any, int, int]]:
    """
    Extract label-value pairs from a row, handling multi-cell patterns.

    This function implements the enhanced pairing logic that can detect
    labels and values across multiple cells. It handles:
    1. Same-cell patterns: "Invoice: 12345" -> Existing behavior
    2. Multi-cell patterns: "Invoice:" | "12345" -> Paired across cells
    3. Multi-cell with gaps: "FROM:" | (empty) | "TOKYO" -> Paired with gap

    Algorithm:
    - Iterate through row cells left to right
    - For each cell:
      1. If already paired (as a value), skip it
      2. Try same-cell pattern first (has colon with value)
      3. If label candidate without value, search adjacent cells
      4. Create appropriate label-value pair

    Args:
        grid: 2D list of cell values (list of rows)
        row_idx: 1-based row index to process

    Returns:
        List of (label, value, row, col) tuples for all cells in the row.
        - label can be None for value-only cells
        - value can be None for label-only cells (no adjacent value found)

    Examples:
        >>> grid = [["Invoice:", "12345", "Date:", "2024-01-01"]]
        >>> _extract_label_value_pairs(grid, 1)
        [("Invoice", "12345", 1, 1), ("Date", "2024-01-01", 1, 3)]

        >>> grid = [["FROM:", None, "TOKYO", "TO:", None, None, "DUBAI"]]
        >>> _extract_label_value_pairs(grid, 1)
        [("FROM", "TOKYO", 1, 1), ("TO", "DUBAI", 1, 4)]
    """
    # Convert to 0-based index for grid access
    grid_row_idx = row_idx - 1

    if grid_row_idx < 0 or grid_row_idx >= len(grid):
        return []

    row = grid[grid_row_idx]
    pairs = []
    paired_col_indices = set()  # Track which columns have been paired as values

    for col_idx, cell in enumerate(row, start=1):
        # Skip empty cells
        if cell in (None, ""):
            continue

        # Skip cells already paired as values
        if col_idx in paired_col_indices:
            logger.debug(
                "Skipping R%dC%d - already paired as value for another label",
                row_idx,
                col_idx,
            )
            continue

        # Try same-cell pattern first (existing behavior)
        label, value = _extract_label_value_from_cell(cell)

        # Case 1: Same-cell pattern with both label and value
        if label is not None and value is not None:
            pairs.append((label, value, row_idx, col_idx))
            logger.debug(
                "Same-cell pattern at R%dC%d: label=%s, value=%s",
                row_idx,
                col_idx,
                label,
                value,
            )
            continue

        # Case 2: Label-only from same-cell pattern (ends with ":", no value after it)
        # Try to find adjacent value
        if label is not None and value is None:
            adjacent_result = _find_adjacent_value(
                grid, row_idx, col_idx, radius=DEFAULT_ADJACENT_CELL_RADIUS
            )

            if adjacent_result:
                adjacent_value, offset = adjacent_result
                value_col_idx = col_idx + offset
                pairs.append((label, adjacent_value, row_idx, col_idx))
                paired_col_indices.add(value_col_idx)
                logger.debug(
                    "Multi-cell pattern at R%dC%d: label=%s, value=%s (from C%d)",
                    row_idx,
                    col_idx,
                    label,
                    adjacent_value,
                    value_col_idx,
                )
            else:
                # No adjacent value found, keep as label-only
                pairs.append((label, None, row_idx, col_idx))
                logger.debug(
                    "Label-only at R%dC%d: label=%s (no adjacent value)",
                    row_idx,
                    col_idx,
                    label,
                )
            continue

        # Case 3: Not a same-cell pattern, check if it's a label candidate
        if _is_label_candidate(cell):
            adjacent_result = _find_adjacent_value(
                grid, row_idx, col_idx, radius=DEFAULT_ADJACENT_CELL_RADIUS
            )

            if adjacent_result:
                adjacent_value, offset = adjacent_result
                value_col_idx = col_idx + offset
                # Remove colon from label if present
                label_text = str(cell).strip().rstrip(":")
                pairs.append((label_text, adjacent_value, row_idx, col_idx))
                paired_col_indices.add(value_col_idx)
                logger.debug(
                    "Label candidate paired at R%dC%d: label=%s, value=%s (from C%d)",
                    row_idx,
                    col_idx,
                    label_text,
                    adjacent_value,
                    value_col_idx,
                )
            else:
                # Label candidate but no adjacent value
                label_text = str(cell).strip().rstrip(":")
                pairs.append((label_text, None, row_idx, col_idx))
                logger.debug(
                    "Label candidate only at R%dC%d: label=%s (no adjacent value)",
                    row_idx,
                    col_idx,
                    label_text,
                )
            continue

        # Case 4: Not a label pattern, treat as value-only
        pairs.append((None, cell, row_idx, col_idx))
        logger.debug("Value-only at R%dC%d: value=%s", row_idx, col_idx, cell)

    return pairs


def _calculate_cell_density(row: list[Any]) -> float:
    """
    Calculate the ratio of non-empty cells to total cells in a row.

    Args:
        row: List of cell values

    Returns:
        Density ratio (0.0-1.0)
    """
    if not row:
        return 0.0

    non_empty_count = sum(1 for cell in row if cell not in (None, ""))
    return non_empty_count / len(row)


def score_row_as_header_candidate(row: list[Any], row_index: int) -> float:
    """
    Score a single row's likelihood of containing invoice metadata.

    This function uses multiple heuristics to determine if a row contains
    header/metadata information rather than table data. It's designed to be
    permissive and catch various metadata patterns.

    Scoring criteria:
    - Key-value patterns (e.g., "Invoice Number: 12345") → +0.4 to +0.6
    - Metadata keywords (invoice, date, shipper, etc.) → +0.3 to +0.5
    - Substantial text content (not just numbers) → +0.2
    - Sparse cell density (10-70% filled) → +0.2 (metadata tends to be sparse)
    - Very dense rows (>85% filled) → -0.3 (likely table data)
    - Very low density (<10%) → +0.1 (single cell metadata)

    Args:
        row: List of cell values (Any type: str, int, float, datetime, None, etc.)
        row_index: 1-based row index (for logging/debugging)

    Returns:
        Score from 0.0 to 1.0 (typically clamped, but can exceed 1.0 before clamping)
    """
    score = 0.0
    pattern_details = []

    # Count non-empty cells
    non_empty_cells = [cell for cell in row if cell not in (None, "")]

    if not non_empty_cells:
        return 0.0  # Empty row

    # Calculate cell density
    density = _calculate_cell_density(row)

    # Heuristic 1: Key-value patterns (highest weight)
    key_value_count = sum(1 for cell in non_empty_cells if _contains_key_value_pattern(str(cell)))
    if key_value_count > 0:
        score += 0.6 if key_value_count >= 2 else 0.4
        pattern_details.append("key_value_patterns")

    # Heuristic 2: Metadata keywords (high weight)
    keyword_count = sum(1 for cell in non_empty_cells if _contains_metadata_keyword(str(cell)))
    if keyword_count > 0:
        score += 0.5 if keyword_count >= 2 else 0.3
        pattern_details.append("metadata_keywords")

    # Heuristic 3: Substantial text content (new - catches company names, addresses)
    substantial_text_count = sum(1 for cell in non_empty_cells if _is_substantial_text(str(cell)))
    if substantial_text_count > 0:
        score += 0.2
        pattern_details.append("substantial_text")

    # Heuristic 4: Cell density analysis (adjusted to be more permissive)
    if 0.1 <= density <= 0.7:
        # Sparse to moderate density suggests metadata
        score += 0.2
        pattern_details.append("sparse_density")
    elif density < 0.1:
        # Very sparse (1-2 cells) - could be single metadata value
        score += 0.1
        pattern_details.append("very_sparse")
    elif density > 0.85:
        # Very dense rows are likely table data (increased penalty)
        score -= 0.3
        pattern_details.append("dense_row")

    # Clamp score to 0.0-1.0 range
    score = max(0.0, min(1.0, score))

    logger.debug(
        "Row %d scored %.2f (patterns: %s, density: %.2f, cells: %d)",
        row_index,
        score,
        ", ".join(pattern_details) if pattern_details else "none",
        density,
        len(non_empty_cells),
    )

    return score


def find_header_candidate_rows(
    grid: list[list[Any]], min_score: float = 0.5
) -> list[tuple[int, float]]:
    """
    Scan entire grid and identify rows with high header scores.

    This function does NOT assume headers are at the top — it scans
    every row in the grid.

    Args:
        grid: 2D list of cell values (list of rows)
        min_score: Minimum score threshold (0.0-1.0). Default: 0.5

    Returns:
        List of (row_index, score) tuples for rows scoring above threshold.
        Row indices are 1-based (Excel convention).
        Returns empty list if no candidates found.

    Example:
        >>> grid = [["Invoice Number: 12345", None], [None, None], ["Date: 2024-01-01", None]]
        >>> find_header_candidate_rows(grid, min_score=0.5)
        [(1, 0.8), (3, 0.7)]
    """
    logger.debug(
        "Scanning grid (%d rows) for header candidates (min_score=%.2f)",
        len(grid),
        min_score,
    )

    candidate_rows = []

    for row_idx, row in enumerate(grid, start=1):
        score = score_row_as_header_candidate(row, row_idx)

        if score >= min_score:
            candidate_rows.append((row_idx, score))
            logger.debug("Row %d is a header candidate (score: %.2f)", row_idx, score)

    logger.info(
        "Found %d header candidate rows out of %d total rows",
        len(candidate_rows),
        len(grid),
    )

    return candidate_rows


def cluster_header_candidate_blocks(
    grid: list[list[Any]], scored_rows: list[tuple[int, float]], max_gap: int = 2
) -> list[HeaderCandidateBlock]:
    """
    Group nearby high-scoring rows into distinct header blocks.

    Rows are grouped into a block if they are within max_gap rows of each other.
    Each block's bounding box and content are extracted.

    Args:
        grid: 2D list of cell values
        scored_rows: List of (row_index, score) tuples (1-based indices)
        max_gap: Maximum row gap to consider rows as part of same block. Default: 2

    Returns:
        List of HeaderCandidateBlock instances, sorted by row_start.
        Returns empty list if no scored_rows provided.

    Example:
        >>> scored_rows = [(1, 0.8), (2, 0.7), (5, 0.6)]
        >>> blocks = cluster_header_candidate_blocks(grid, scored_rows, max_gap=2)
        >>> len(blocks)
        2  # First block: rows 1-2, second block: row 5
    """
    if not scored_rows:
        logger.info("No scored rows to cluster")
        return []

    logger.debug(
        "Clustering %d scored rows into blocks (max_gap=%d)",
        len(scored_rows),
        max_gap,
    )

    # Sort by row index
    sorted_rows = sorted(scored_rows, key=lambda x: x[0])

    blocks = []
    current_cluster = [sorted_rows[0]]

    # Cluster consecutive or nearby rows
    for row_idx, score in sorted_rows[1:]:
        last_row_idx = current_cluster[-1][0]

        # If within max_gap, add to current cluster
        if row_idx - last_row_idx <= max_gap + 1:
            current_cluster.append((row_idx, score))
        else:
            # Finalize current cluster and start new one
            blocks.append(_create_block_from_cluster(grid, current_cluster))
            current_cluster = [(row_idx, score)]

    # Finalize last cluster
    if current_cluster:
        blocks.append(_create_block_from_cluster(grid, current_cluster))

    logger.info("Clustered %d rows into %d header blocks", len(scored_rows), len(blocks))

    return blocks


def _create_block_from_cluster(
    grid: list[list[Any]], cluster: list[tuple[int, float]]
) -> HeaderCandidateBlock:
    """
    Create a HeaderCandidateBlock from a cluster of scored rows.

    Args:
        grid: 2D list of cell values
        cluster: List of (row_index, score) tuples (1-based)

    Returns:
        HeaderCandidateBlock instance
    """
    row_indices = [row_idx for row_idx, _ in cluster]
    scores = [score for _, score in cluster]

    row_start = min(row_indices)
    row_end = max(row_indices)

    # Calculate average score for the block
    avg_score = sum(scores) / len(scores)

    # Extract content and determine column range
    content = []
    col_indices = []

    for row_idx in range(row_start, row_end + 1):
        # Convert to 0-based index for grid access
        grid_row_idx = row_idx - 1

        if grid_row_idx < len(grid):
            row = grid[grid_row_idx]

            for col_idx, cell in enumerate(row, start=1):
                if cell not in (None, ""):
                    content.append((row_idx, col_idx, cell))
                    col_indices.append(col_idx)

    # Determine column range
    if col_indices:
        col_start = min(col_indices)
        col_end = max(col_indices)
    else:
        # Empty block (shouldn't happen, but handle gracefully)
        col_start = 1
        col_end = 1

    # Extract label/value pairs using enhanced pairing logic
    # Process each row in the block to detect multi-cell patterns
    label_value_pairs = []
    processed_rows = set()

    for row_idx in range(row_start, row_end + 1):
        if row_idx not in processed_rows:
            row_pairs = _extract_label_value_pairs(grid, row_idx)
            label_value_pairs.extend(row_pairs)
            processed_rows.add(row_idx)

    # Determine primary detection pattern
    # Check if any row had key-value patterns
    has_key_value = any(_contains_key_value_pattern(str(cell)) for _, _, cell in content)
    has_keywords = any(_contains_metadata_keyword(str(cell)) for _, _, cell in content)
    has_substantial_text = any(_is_substantial_text(str(cell)) for _, _, cell in content)

    if has_key_value and has_keywords:
        pattern = "key_value_and_keywords"
    elif has_key_value:
        pattern = "key_value_patterns"
    elif has_keywords:
        pattern = "metadata_keywords"
    elif has_substantial_text:
        pattern = "substantial_text"
    else:
        pattern = "structural_heuristics"

    return HeaderCandidateBlock(
        row_start=row_start,
        row_end=row_end,
        col_start=col_start,
        col_end=col_end,
        content=content,
        label_value_pairs=label_value_pairs,
        score=avg_score,
        detected_pattern=pattern,
    )


def _get_table_excluded_rows(
    grid: list[list[Any]], table_blocks: list[TableCandidateBlock]
) -> set[int]:
    """
    Identify which rows are NOT part of any table block.

    This is used for table exclusion approach: all non-table rows are
    potential header/metadata candidates.

    Args:
        grid: 2D list of cell values
        table_blocks: List of detected table blocks to exclude

    Returns:
        Set of 1-based row indices that are not part of any table block
        and are not empty rows.

    Example:
        >>> grid = [["Header"], [None], ["Item", 10], ["Widget", 20], [None], ["Footer"]]
        >>> table_blocks = [TableCandidateBlock(row_start=3, row_end=4, ...)]
        >>> _get_table_excluded_rows(grid, table_blocks)
        {1, 6}  # Rows 1 and 6 are not in table and not empty
    """
    # Start with all row indices
    all_rows = set(range(1, len(grid) + 1))

    # Remove rows that are part of table blocks
    table_rows = set()
    for block in table_blocks:
        for row_idx in range(block.row_start, block.row_end + 1):
            table_rows.add(row_idx)

    non_table_rows = all_rows - table_rows

    # Remove empty rows (all None or "")
    non_empty_non_table_rows = set()
    for row_idx in non_table_rows:
        # Convert to 0-based index for grid access
        grid_row_idx = row_idx - 1
        if grid_row_idx < len(grid):
            row = grid[grid_row_idx]
            # Check if row has any non-empty cells
            if any(cell not in (None, "") for cell in row):
                non_empty_non_table_rows.add(row_idx)

    logger.debug(
        "Table exclusion: %d total rows, %d table rows, %d non-table non-empty rows",
        len(grid),
        len(table_rows),
        len(non_empty_non_table_rows),
    )

    return non_empty_non_table_rows


def detect_header_candidate_blocks(
    grid: list[list[Any]],
    min_score: float = 0.3,
    max_gap: int = 2,
    table_blocks: list[TableCandidateBlock] | None = None,
) -> list[HeaderCandidateBlock]:
    """
    Main entry point for detecting invoice metadata blocks in a grid.

    This function orchestrates the entire header detection pipeline:
    1. If table_blocks provided: Use table exclusion approach (all non-table rows)
    2. Otherwise: Scan all rows for header-like patterns using scoring heuristics
    3. Cluster high-scoring rows into distinct blocks
    4. Return structured HeaderCandidateBlock instances

    Important: This function scans the ENTIRE grid, not just the top rows.
    It can detect multiple header blocks (e.g., shipper, consignee, billing info).

    Table Exclusion Approach (when table_blocks provided):
    - More comprehensive: Won't miss metadata that doesn't match scoring patterns
    - Field-agnostic: No need to predict what metadata looks like
    - Complete coverage: Captures ALL non-table content for AI processing
    - Use this when you've already detected tables using detect_table_candidate_blocks()

    Args:
        grid: 2D list of cell values (list of rows)
        min_score: Minimum score threshold for header candidates (0.0-1.0). Default: 0.3
                   Ignored when table_blocks is provided (all non-table rows are used).
        max_gap: Maximum row gap for clustering blocks. Default: 2
        table_blocks: Optional list of table blocks to exclude from header detection.
                      If provided, uses table exclusion approach instead of scoring.
                      Default: None (uses scoring heuristics).

    Returns:
        List of HeaderCandidateBlock instances, sorted by row_start (top to bottom).
        Returns empty list if no header candidates found or grid is empty.

    Raises:
        ValueError: If min_score is not in range 0.0-1.0

    Example (scoring approach - backward compatible):
        >>> from template_sense.extraction.sheet_extractor import extract_raw_grid
        >>> grid = extract_raw_grid(workbook, "Sheet1")
        >>> blocks = detect_header_candidate_blocks(grid)
        >>> print(f"Found {len(blocks)} header blocks")
        Found 2 header blocks

    Example (table exclusion approach - enhanced):
        >>> from template_sense.extraction.table_candidates import detect_table_candidate_blocks
        >>> grid = extract_raw_grid(workbook, "Sheet1")
        >>> table_blocks = detect_table_candidate_blocks(grid)
        >>> header_blocks = detect_header_candidate_blocks(grid, table_blocks=table_blocks)
        >>> print(f"Found {len(header_blocks)} header blocks")
        Found 3 header blocks
    """
    # Validate inputs
    if not 0.0 <= min_score <= 1.0:
        raise ValueError(f"min_score must be in range 0.0-1.0, got {min_score}")

    if not grid:
        logger.info("Grid is empty, returning no header blocks")
        return []

    # Determine which approach to use
    if table_blocks is not None:
        logger.info(
            "Detecting header candidate blocks using table exclusion approach "
            "(%d rows, %d table blocks, max_gap=%d)",
            len(grid),
            len(table_blocks),
            max_gap,
        )

        # Step 1: Get non-table rows
        non_table_rows = _get_table_excluded_rows(grid, table_blocks)

        if not non_table_rows:
            logger.info("No non-table rows found")
            return []

        # Step 2: Create scored rows with score=1.0 for all non-table rows
        # (we're not using scoring in table exclusion approach)
        scored_rows = [(row_idx, 1.0) for row_idx in sorted(non_table_rows)]

        logger.info(
            "Table exclusion: identified %d non-table rows as header candidates",
            len(scored_rows),
        )
    else:
        logger.info(
            "Detecting header candidate blocks using scoring heuristics "
            "(%d rows, min_score=%.2f, max_gap=%d)",
            len(grid),
            min_score,
            max_gap,
        )

        # Step 1: Find candidate rows using scoring
        scored_rows = find_header_candidate_rows(grid, min_score=min_score)

        if not scored_rows:
            logger.info("No header candidate rows found")
            return []

    # Step 2: Cluster into blocks
    blocks = cluster_header_candidate_blocks(grid, scored_rows, max_gap=max_gap)

    logger.info(
        "Header detection complete: found %d blocks from %d candidate rows",
        len(blocks),
        len(scored_rows),
    )

    return blocks


__all__ = [
    "HeaderCandidateBlock",
    "score_row_as_header_candidate",
    "find_header_candidate_rows",
    "cluster_header_candidate_blocks",
    "detect_header_candidate_blocks",
]
