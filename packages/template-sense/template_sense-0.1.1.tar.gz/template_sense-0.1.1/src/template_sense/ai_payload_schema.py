"""
AI payload schema for Template Sense.

This module defines the schema for AI payloads sent to AI providers (OpenAI, Anthropic)
for template analysis. The schema is provider-agnostic and includes all necessary context
for semantic field classification and column header mapping.

The AI payload includes:
- Sheet metadata (name)
- Header candidates (detected key-value pairs from heuristics)
- Table candidates (detected tables with headers and sample data rows)
- Field dictionary (Tako's canonical field mappings with multilingual aliases)

This module does NOT:
- Call any AI services (that happens in ai_providers/)
- Perform translation (that happens in translation/)
- Perform fuzzy matching (that happens in mapping/)
- Modify or interpret field values

This module DOES:
- Define clear, typed schema for AI payloads
- Convert sheet summary output to AI-ready format
- Extract sample data rows from tables
- Ensure all data is JSON-serializable

Functions:
    build_ai_payload: Main entry point for building AI payload from sheet summary

Usage Example:
    from pathlib import Path
    from template_sense.file_loader import load_excel_file
    from template_sense.adapters.excel_adapter import ExcelWorkbook
    from template_sense.extraction.summary_builder import build_sheet_summary
    from template_sense.ai_payload_schema import build_ai_payload

    # Load workbook and build summary
    raw_workbook = load_excel_file(Path("invoice.xlsx"))
    workbook = ExcelWorkbook(raw_workbook)
    summary = build_sheet_summary(workbook, sheet_name="Sheet1")

    # Tako's field dictionary (multilingual)
    field_dict = {
        "invoice_number": ["Invoice number", "Invoice No", "請求書番号"],
        "due_date": ["Due date", "Payment due", "支払期日"],
        "box_name": ["Box name", "Container", "箱名"],
    }

    # Build AI payload
    payload = build_ai_payload(summary, field_dict)
    print(payload)
    # {
    #     "sheet_name": "Sheet1",
    #     "header_candidates": [...],
    #     "table_candidates": [...],
    #     "field_dictionary": {...}
    # }
"""

import logging
from dataclasses import asdict, dataclass
from typing import Any

from template_sense.constants import DEFAULT_ADJACENT_CELL_RADIUS, DEFAULT_AI_SAMPLE_ROWS

# Set up module logger
logger = logging.getLogger(__name__)


@dataclass
class AIHeaderCandidate:
    """
    Represents a single header field candidate detected by heuristics.

    Header candidates are typically key-value pairs found in the upper section
    of invoice templates (e.g., "Invoice Number: 12345", "Due Date: 2024-01-01").

    Attributes:
        row: 1-based row index where this header was found
        col: 1-based column index where this header was found
        label: The label/key text (e.g., "Invoice Number", "請求書番号")
        value: The associated value (e.g., "12345", "2024-01-01")
        score: Confidence score from heuristic detection (0.0-1.0)
        adjacent_cells: Optional dict containing values from nearby cells for context.
                       Keys are directional offsets (e.g., "left_1", "right_2", "above_1").
                       Values are cell contents (any type, or None for empty/out-of-bounds).

    Example:
        >>> header = AIHeaderCandidate(
        ...     row=1,
        ...     col=1,
        ...     label="Invoice Number",
        ...     value="INV-12345",
        ...     score=0.85,
        ...     adjacent_cells={"right_1": "2024-01-01", "below_1": "Paid"}
        ... )
    """

    row: int
    col: int
    label: str
    value: Any
    score: float
    adjacent_cells: dict[str, Any] | None = None


@dataclass
class AITableHeaderCell:
    """
    Represents a single cell in a table header row.

    Each header cell corresponds to a column in the table and contains
    the column label (e.g., "Item", "Quantity", "Price").

    Attributes:
        col: 1-based column index (absolute sheet position)
        value: Header cell value (column label, any language)
        score: Confidence score for this specific header cell (0.0-1.0)

    Example:
        >>> cell = AITableHeaderCell(
        ...     col=3,
        ...     value="Quantity",
        ...     score=0.92
        ... )
    """

    col: int
    value: Any
    score: float


@dataclass
class AITableHeaderInfo:
    """
    Represents a detected table header row.

    Contains the row index, individual header cells, and metadata about
    how the header was detected.

    Attributes:
        row_index: 1-based row index of the header row
        cells: List of header cells with column positions and values
        detected_pattern: Pattern used to detect this header (e.g., "first_row_text_dense")

    Example:
        >>> header_info = AITableHeaderInfo(
        ...     row_index=10,
        ...     cells=[
        ...         AITableHeaderCell(col=1, value="Item", score=0.9),
        ...         AITableHeaderCell(col=2, value="Quantity", score=0.92),
        ...     ],
        ...     detected_pattern="first_row_text_dense"
        ... )
    """

    row_index: int
    cells: list[AITableHeaderCell]
    detected_pattern: str


@dataclass
class AITableCandidate:
    """
    Represents a detected table with header and sample data rows.

    Tables are rectangular data regions detected by heuristics. This schema includes
    the table boundaries, detected header row (if any), and sample data rows to help
    AI understand column semantics.

    Attributes:
        start_row: 1-based start row (inclusive)
        end_row: 1-based end row (inclusive)
        start_col: 1-based start column (inclusive)
        end_col: 1-based end column (inclusive)
        header_row: Detected header row info (None if no header detected)
        sample_data_rows: First N rows of data (excluding header), as dense 2D array
        total_data_rows: Total number of data rows in the table (for context)
        score: Confidence score from table detection heuristics (0.0-1.0)
        detected_pattern: Pattern used to detect this table (e.g., "high_numeric_density")

    Example:
        >>> table = AITableCandidate(
        ...     start_row=10,
        ...     end_row=25,
        ...     start_col=1,
        ...     end_col=4,
        ...     header_row=AITableHeaderInfo(...),
        ...     sample_data_rows=[
        ...         ["Widget A", 10, 5.99, 59.90],
        ...         ["Widget B", 5, 12.50, 62.50],
        ...     ],
        ...     total_data_rows=15,
        ...     score=0.78,
        ...     detected_pattern="high_numeric_density"
        ... )
    """

    start_row: int
    end_row: int
    start_col: int
    end_col: int
    header_row: AITableHeaderInfo | None
    sample_data_rows: list[list[Any]]
    total_data_rows: int
    score: float
    detected_pattern: str


@dataclass
class AIPayload:
    """
    Complete AI payload for template analysis.

    This is the top-level schema sent to AI providers for semantic classification
    of headers and table columns. The payload is provider-agnostic and includes
    all necessary context for accurate field mapping.

    Attributes:
        sheet_name: Name of the Excel sheet being analyzed
        header_candidates: List of detected header fields (key-value pairs)
        table_candidates: List of detected tables with headers and sample data
        field_dictionary: Structured canonical field mapping with 'headers' and 'columns' sections

    Example:
        >>> payload = AIPayload(
        ...     sheet_name="Sheet1",
        ...     header_candidates=[...],
        ...     table_candidates=[...],
        ...     field_dictionary={
        ...         "headers": {
        ...             "invoice_number": ["Invoice number", "請求書番号"],
        ...         },
        ...         "columns": {
        ...             "box_name": ["Box name", "箱名"],
        ...         }
        ...     }
        ... )
    """

    sheet_name: str
    header_candidates: list[AIHeaderCandidate]
    table_candidates: list[AITableCandidate]
    field_dictionary: dict[str, dict[str, list[str]]]


def _extract_adjacent_cells(
    grid: list[list[Any]],
    row: int,
    col: int,
    radius: int = DEFAULT_ADJACENT_CELL_RADIUS,
) -> dict[str, Any]:
    """
    Extract adjacent cell values from grid for context.

    Extracts cells in all four directions (left, right, above, below) up to
    the specified radius. Keys are formatted as "{direction}_{offset}" where
    offset is 1-based distance from the source cell.

    Args:
        grid: 2D grid of cell values (0-indexed: grid[row][col])
        row: 1-based row index of source cell
        col: 1-based column index of source cell
        radius: Maximum number of cells to extract in each direction (default: 3)

    Returns:
        Dict mapping direction keys to cell values. Example:
        {
            "left_1": "Invoice:",
            "left_2": None,
            "right_1": "12345",
            "right_2": None,
            "above_1": "Header",
            "below_1": "Footer"
        }

    Example:
        >>> grid = [
        ...     ["A", "B", "C", "D"],
        ...     ["E", "F", "G", "H"],
        ...     ["I", "J", "K", "L"],
        ... ]
        >>> adjacent = _extract_adjacent_cells(grid, row=2, col=2, radius=2)
        >>> adjacent["left_1"]
        'E'
        >>> adjacent["right_1"]
        'G'
    """
    adjacent = {}

    # Convert to 0-based for grid access
    row_0 = row - 1
    col_0 = col - 1

    grid_rows = len(grid)
    grid_cols = len(grid[0]) if grid_rows > 0 else 0

    # Extract left cells
    for offset in range(1, radius + 1):
        target_col = col_0 - offset
        if target_col >= 0:
            adjacent[f"left_{offset}"] = grid[row_0][target_col]
        else:
            adjacent[f"left_{offset}"] = None

    # Extract right cells
    for offset in range(1, radius + 1):
        target_col = col_0 + offset
        if target_col < grid_cols:
            adjacent[f"right_{offset}"] = grid[row_0][target_col]
        else:
            adjacent[f"right_{offset}"] = None

    # Extract above cells
    for offset in range(1, radius + 1):
        target_row = row_0 - offset
        if target_row >= 0:
            adjacent[f"above_{offset}"] = grid[target_row][col_0]
        else:
            adjacent[f"above_{offset}"] = None

    # Extract below cells
    for offset in range(1, radius + 1):
        target_row = row_0 + offset
        if target_row < grid_rows:
            adjacent[f"below_{offset}"] = grid[target_row][col_0]
        else:
            adjacent[f"below_{offset}"] = None

    return adjacent


def _convert_header_candidates(
    header_blocks: list[dict[str, Any]],
    grid: list[list[Any]] | None = None,
    adjacent_cell_radius: int = DEFAULT_ADJACENT_CELL_RADIUS,
) -> list[AIHeaderCandidate]:
    """
    Convert header blocks from sheet summary to AIHeaderCandidate list.

    Extracts label_value_pairs from each header block and flattens them into
    individual AIHeaderCandidate objects. If grid is provided, also extracts
    adjacent cell context for AI pattern detection.

    Args:
        header_blocks: List of header block dicts from build_sheet_summary()
        grid: Optional 2D grid of cell values for adjacent cell extraction
        adjacent_cell_radius: Number of adjacent cells to extract in each direction

    Returns:
        List of AIHeaderCandidate objects

    Example:
        >>> header_blocks = [
        ...     {
        ...         "label_value_pairs": [
        ...             {"label": "Invoice", "value": "12345", "row": 1, "col": 1},
        ...             {"label": "Date", "value": "2024-01-01", "row": 2, "col": 1},
        ...         ],
        ...         "score": 0.85,
        ...     }
        ... ]
        >>> candidates = _convert_header_candidates(header_blocks)
        >>> len(candidates)
        2
    """
    candidates = []

    for block in header_blocks:
        block_score = block.get("score", 0.0)

        for pair in block.get("label_value_pairs", []):
            # Extract adjacent cells if grid is provided
            adjacent_cells = None
            if grid is not None:
                adjacent_cells = _extract_adjacent_cells(
                    grid=grid,
                    row=pair["row"],
                    col=pair["col"],
                    radius=adjacent_cell_radius,
                )

            candidate = AIHeaderCandidate(
                row=pair["row"],
                col=pair["col"],
                label=pair["label"],
                value=pair["value"],
                score=block_score,
                adjacent_cells=adjacent_cells,
            )
            candidates.append(candidate)

    logger.debug(
        "Converted %d header blocks to %d header candidates (grid_provided=%s)",
        len(header_blocks),
        len(candidates),
        grid is not None,
    )

    return candidates


def _convert_table_header_info(header_row: dict[str, Any] | None) -> AITableHeaderInfo | None:
    """
    Convert table header row dict to AITableHeaderInfo dataclass.

    Args:
        header_row: Header row dict from sheet summary (or None)

    Returns:
        AITableHeaderInfo object (or None if input is None)

    Example:
        >>> header_row = {
        ...     "row_index": 10,
        ...     "col_start": 1,
        ...     "col_end": 4,
        ...     "values": ["Item", "Quantity", "Price", "Amount"],
        ...     "score": 0.92,
        ...     "detected_pattern": "first_row_text_dense"
        ... }
        >>> header_info = _convert_table_header_info(header_row)
        >>> len(header_info.cells)
        4
    """
    if header_row is None:
        return None

    row_index = header_row["row_index"]
    col_start = header_row["col_start"]
    values = header_row["values"]
    score = header_row["score"]
    detected_pattern = header_row["detected_pattern"]

    # Create a cell for each header value
    cells = [
        AITableHeaderCell(col=col_start + i, value=value, score=score)
        for i, value in enumerate(values)
    ]

    return AITableHeaderInfo(
        row_index=row_index,
        cells=cells,
        detected_pattern=detected_pattern,
    )


def _extract_sample_data_rows(
    table_content: list[list[Any]],
    header_row_index: int | None,
    start_row: int,
    end_row: int,
    start_col: int,
    end_col: int,
    max_rows: int,
) -> tuple[list[list[Any]], int]:
    """
    Extract sample data rows from table content.

    Converts sparse [row, col, value] format to dense 2D array and extracts
    the first N data rows (excluding header row).

    Args:
        table_content: List of [row, col, value] tuples from sheet summary
        header_row_index: Row index of header (to exclude), or None
        start_row: Table start row (1-based, inclusive)
        end_row: Table end row (1-based, inclusive)
        start_col: Table start column (1-based, inclusive)
        end_col: Table end column (1-based, inclusive)
        max_rows: Maximum number of sample rows to extract

    Returns:
        Tuple of (sample_data_rows, total_data_rows):
        - sample_data_rows: List of dense row arrays (first N rows)
        - total_data_rows: Total count of data rows in table

    Example:
        >>> content = [
        ...     [10, 1, "Item"], [10, 2, "Quantity"],  # Header row
        ...     [11, 1, "Widget A"], [11, 2, 10],      # Data row 1
        ...     [12, 1, "Widget B"], [12, 2, 5],       # Data row 2
        ... ]
        >>> sample, total = _extract_sample_data_rows(
        ...     content, header_row_index=10,
        ...     start_row=10, end_row=12, start_col=1, end_col=2,
        ...     max_rows=5
        ... )
        >>> len(sample)
        2
        >>> total
        2
    """
    # Build a sparse dict: (row, col) -> value
    sparse_grid: dict[tuple[int, int], Any] = {}
    for row, col, value in table_content:
        sparse_grid[(row, col)] = value

    # Determine which rows are data rows (exclude header if present)
    data_row_indices = []
    for row in range(start_row, end_row + 1):
        if header_row_index is not None and row == header_row_index:
            continue  # Skip header row
        data_row_indices.append(row)

    total_data_rows = len(data_row_indices)

    # Extract first N data rows
    sample_row_indices = data_row_indices[:max_rows]

    # Convert to dense 2D array
    sample_data_rows = []
    for row in sample_row_indices:
        dense_row = []
        for col in range(start_col, end_col + 1):
            value = sparse_grid.get((row, col), None)
            dense_row.append(value)
        sample_data_rows.append(dense_row)

    logger.debug(
        "Extracted %d sample rows from table R%d:R%d (total data rows: %d)",
        len(sample_data_rows),
        start_row,
        end_row,
        total_data_rows,
    )

    return sample_data_rows, total_data_rows


def build_ai_payload(
    sheet_summary: dict[str, Any],
    field_dictionary: dict[str, dict[str, list[str]]],
    grid: list[list[Any]] | None = None,
    max_sample_rows: int = DEFAULT_AI_SAMPLE_ROWS,
    adjacent_cell_radius: int = DEFAULT_ADJACENT_CELL_RADIUS,
) -> dict[str, Any]:
    """
    Build AI payload from sheet summary and field dictionary.

    This is the main entry point for converting sheet structure summary (from BAT-28)
    into an AI-ready payload for semantic classification. The payload includes all
    necessary context for AI to match fields and columns to Tako's canonical dictionary.

    Args:
        sheet_summary: Output from build_sheet_summary() containing header and table blocks
        field_dictionary: Structured canonical field mapping with 'headers' and 'columns' sections
        grid: Optional 2D grid of cell values for adjacent cell context extraction
        max_sample_rows: Maximum number of sample data rows to include per table (default: 5)
        adjacent_cell_radius: Number of adjacent cells to extract in each direction (default: 3)

    Returns:
        JSON-serializable dict with AI payload structure matching AIPayload schema

    Raises:
        ValueError: If max_sample_rows is not positive

    Example:
        >>> from template_sense.extraction.summary_builder import build_sheet_summary
        >>> summary = build_sheet_summary(workbook, sheet_name="Sheet1")
        >>> field_dict = {
        ...     "headers": {
        ...         "invoice_number": ["Invoice number", "請求書番号"],
        ...     },
        ...     "columns": {
        ...         "box_name": ["Box name", "箱名"],
        ...     }
        ... }
        >>> payload = build_ai_payload(summary, field_dict)
        >>> payload["sheet_name"]
        'Sheet1'
        >>> len(payload["header_candidates"])
        5
    """
    # Validate max_sample_rows
    if max_sample_rows < 1:
        raise ValueError(f"max_sample_rows must be >= 1, got {max_sample_rows}")

    logger.info(
        "Building AI payload for sheet '%s' (max_sample_rows=%d, grid_provided=%s)",
        sheet_summary.get("sheet_name", "Unknown"),
        max_sample_rows,
        grid is not None,
    )

    # Extract sheet name
    sheet_name = sheet_summary.get("sheet_name", "")

    # Convert header blocks to header candidates
    header_blocks = sheet_summary.get("header_blocks", [])
    header_candidates = _convert_header_candidates(
        header_blocks=header_blocks,
        grid=grid,
        adjacent_cell_radius=adjacent_cell_radius,
    )

    # Convert table blocks to table candidates
    table_blocks = sheet_summary.get("table_blocks", [])
    table_candidates = []

    for table_block in table_blocks:
        # Convert header row (if present)
        header_row_dict = table_block.get("header_row")
        header_row = _convert_table_header_info(header_row_dict)

        # Extract sample data rows
        header_row_index = header_row.row_index if header_row else None
        sample_data_rows, total_data_rows = _extract_sample_data_rows(
            table_content=table_block["content"],
            header_row_index=header_row_index,
            start_row=table_block["row_start"],
            end_row=table_block["row_end"],
            start_col=table_block["col_start"],
            end_col=table_block["col_end"],
            max_rows=max_sample_rows,
        )

        # Build AITableCandidate
        table_candidate = AITableCandidate(
            start_row=table_block["row_start"],
            end_row=table_block["row_end"],
            start_col=table_block["col_start"],
            end_col=table_block["col_end"],
            header_row=header_row,
            sample_data_rows=sample_data_rows,
            total_data_rows=total_data_rows,
            score=table_block["score"],
            detected_pattern=table_block["detected_pattern"],
        )
        table_candidates.append(table_candidate)

    # Build AIPayload
    payload = AIPayload(
        sheet_name=sheet_name,
        header_candidates=header_candidates,
        table_candidates=table_candidates,
        field_dictionary=field_dictionary,
    )

    logger.info(
        "AI payload built: %d header candidates, %d table candidates",
        len(header_candidates),
        len(table_candidates),
    )

    # Convert to JSON-serializable dict
    return asdict(payload)


__all__ = [
    "AIHeaderCandidate",
    "AITableHeaderCell",
    "AITableHeaderInfo",
    "AITableCandidate",
    "AIPayload",
    "build_ai_payload",
]
