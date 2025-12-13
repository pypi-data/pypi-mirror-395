"""
Unit tests for table_header_detection module.

Tests the heuristic-based table header row detection including:
- Scoring individual rows for header likelihood
- Detecting header rows in various table patterns
- Handling edge cases (no header, multi-row headers, multilingual)
- Field-agnostic behavior verification
"""

import pytest

from template_sense.extraction.table_candidates import TableCandidateBlock
from template_sense.extraction.table_header_detection import (
    TableHeaderInfo,
    detect_table_header_row,
    score_row_as_header,
)

# ============================================================================
# Test: score_row_as_header
# ============================================================================


def test_score_text_dense_row_as_header():
    """Test that text-dense rows score high as headers."""
    # Typical table header row
    row = ["Item", "Quantity", "Price", "Amount"]
    score = score_row_as_header(row, row_index=1, is_first_row=True)

    # Should have high score (text-dense, first row)
    assert score >= 0.7
    assert score <= 1.0


def test_score_numeric_row_low():
    """Test that all-numeric rows score very low as headers."""
    # Data row with all numbers
    row = [100, 200, 300.50, 400.00]
    score = score_row_as_header(row, row_index=2, is_first_row=False)

    # Should have very low score (all numeric)
    assert score < 0.3


def test_score_mixed_text_numeric_row():
    """Test that mixed text/numeric rows score moderately."""
    # Row with product name and numbers (could be header or data)
    row = ["Product A", 10, 25.50, 255.00]
    score = score_row_as_header(row, row_index=2, is_first_row=False)

    # Should have moderate score (some text, but also numeric)
    assert 0.0 <= score <= 1.0


def test_score_all_caps_header():
    """Test that all-caps headers get special casing bonus."""
    # Header with all caps
    row = ["ITEM", "QTY", "PRICE", "TOTAL"]
    score = score_row_as_header(row, row_index=1, is_first_row=True)

    # Should have very high score (text + all caps + first row)
    assert score >= 0.8


def test_score_title_case_header():
    """Test that title case headers get special casing bonus."""
    # Header with title case
    row = ["Item Name", "Unit Price", "Total Amount"]
    score = score_row_as_header(row, row_index=1, is_first_row=True)

    # Should have high score (text + title case + first row)
    assert score >= 0.7


def test_score_empty_row_zero():
    """Test that empty rows score zero."""
    row = [None, None, None, None]
    score = score_row_as_header(row, row_index=1, is_first_row=False)

    assert score == 0.0


def test_score_sparse_row_low():
    """Test that sparse rows score low."""
    # Row with mostly empty cells
    row = ["Item", None, None, None, None]
    score = score_row_as_header(row, row_index=1, is_first_row=False)

    # Should have lower score due to low cell density
    assert score < 0.8


def test_score_first_row_bonus():
    """Test that first row gets bonus points."""
    row = ["Item", "Quantity", "Price"]

    score_first = score_row_as_header(row, row_index=1, is_first_row=True)
    score_not_first = score_row_as_header(row, row_index=3, is_first_row=False)

    # First row should score higher
    assert score_first > score_not_first


# ============================================================================
# Test: detect_table_header_row - Simple Cases
# ============================================================================


def test_detect_header_simple_table():
    """Test detecting header in a simple table with clear header row."""
    # Create a simple table block
    # Row 5: ["Item", "Quantity", "Price", "Amount"]  <- Header
    # Row 6: ["Widget A", 10, 25.50, 255.00]
    # Row 7: ["Widget B", 20, 30.00, 600.00]
    # Row 8: ["Widget C", 5, 15.75, 78.75]

    content = [
        # Row 5 (header)
        (5, 1, "Item"),
        (5, 2, "Quantity"),
        (5, 3, "Price"),
        (5, 4, "Amount"),
        # Row 6
        (6, 1, "Widget A"),
        (6, 2, 10),
        (6, 3, 25.50),
        (6, 4, 255.00),
        # Row 7
        (7, 1, "Widget B"),
        (7, 2, 20),
        (7, 3, 30.00),
        (7, 4, 600.00),
        # Row 8
        (8, 1, "Widget C"),
        (8, 2, 5),
        (8, 3, 15.75),
        (8, 4, 78.75),
    ]

    table_block = TableCandidateBlock(
        row_start=5,
        row_end=8,
        col_start=1,
        col_end=4,
        content=content,
        score=0.8,
        detected_pattern="high_numeric_density",
    )

    header_info = detect_table_header_row(table_block)

    assert header_info is not None
    assert header_info.row_index == 5  # First row
    assert header_info.col_start == 1
    assert header_info.col_end == 4
    assert header_info.values == ["Item", "Quantity", "Price", "Amount"]
    assert header_info.score >= 0.6


def test_detect_header_all_caps():
    """Test detecting all-caps header row."""
    # Table with all-caps header
    content = [
        # Row 10 (header - all caps)
        (10, 1, "ITEM"),
        (10, 2, "QTY"),
        (10, 3, "PRICE"),
        # Row 11
        (11, 1, "Product X"),
        (11, 2, 100),
        (11, 3, 50.00),
        # Row 12
        (12, 1, "Product Y"),
        (12, 2, 200),
        (12, 3, 75.00),
    ]

    table_block = TableCandidateBlock(
        row_start=10,
        row_end=12,
        col_start=1,
        col_end=3,
        content=content,
        score=0.75,
        detected_pattern="moderate_numeric_density",
    )

    header_info = detect_table_header_row(table_block)

    assert header_info is not None
    assert header_info.row_index == 10
    assert header_info.values == ["ITEM", "QTY", "PRICE"]
    assert header_info.score >= 0.7  # Should score very high (all caps + text + first)


def test_detect_header_in_middle():
    """Test detecting header row that is NOT the first row."""
    # Table where first row is a subtitle/category, second row is header
    content = [
        # Row 15 (category/subtitle - sparse)
        (15, 1, "Product Details"),
        (15, 2, None),
        (15, 3, None),
        # Row 16 (header)
        (16, 1, "Item"),
        (16, 2, "Quantity"),
        (16, 3, "Price"),
        # Row 17
        (17, 1, "Widget A"),
        (17, 2, 10),
        (17, 3, 25.50),
        # Row 18
        (18, 1, "Widget B"),
        (18, 2, 20),
        (18, 3, 30.00),
    ]

    table_block = TableCandidateBlock(
        row_start=15,
        row_end=18,
        col_start=1,
        col_end=3,
        content=content,
        score=0.7,
        detected_pattern="column_consistency",
    )

    header_info = detect_table_header_row(table_block)

    assert header_info is not None
    assert header_info.row_index == 16  # Second row (not first)
    assert header_info.values == ["Item", "Quantity", "Price"]


# ============================================================================
# Test: detect_table_header_row - Edge Cases
# ============================================================================


def test_detect_no_header_all_numeric():
    """Test that no header is detected when all rows are numeric."""
    # Table with no clear header (all numeric data)
    content = [
        # Row 20
        (20, 1, 100),
        (20, 2, 200),
        (20, 3, 300),
        # Row 21
        (21, 1, 110),
        (21, 2, 210),
        (21, 3, 310),
        # Row 22
        (22, 1, 120),
        (22, 2, 220),
        (22, 3, 320),
    ]

    table_block = TableCandidateBlock(
        row_start=20,
        row_end=22,
        col_start=1,
        col_end=3,
        content=content,
        score=0.9,
        detected_pattern="high_numeric_density",
    )

    header_info = detect_table_header_row(table_block)

    # Should return None (no text-based header found)
    assert header_info is None


def test_detect_header_multilingual_japanese():
    """Test detecting multilingual headers (Japanese)."""
    # Table with Japanese column headers
    content = [
        # Row 25 (Japanese header)
        (25, 1, "品目"),  # Item
        (25, 2, "数量"),  # Quantity
        (25, 3, "価格"),  # Price
        # Row 26
        (26, 1, "製品A"),
        (26, 2, 10),
        (26, 3, 2550),
        # Row 27
        (27, 1, "製品B"),
        (27, 2, 20),
        (27, 3, 3000),
    ]

    table_block = TableCandidateBlock(
        row_start=25,
        row_end=27,
        col_start=1,
        col_end=3,
        content=content,
        score=0.75,
        detected_pattern="moderate_numeric_density",
    )

    header_info = detect_table_header_row(table_block)

    assert header_info is not None
    assert header_info.row_index == 25
    assert header_info.values == ["品目", "数量", "価格"]
    assert header_info.score >= 0.6


def test_detect_header_multilingual_arabic():
    """Test detecting multilingual headers (Arabic)."""
    # Table with Arabic column headers
    content = [
        # Row 30 (Arabic header)
        (30, 1, "البند"),  # Item
        (30, 2, "الكمية"),  # Quantity
        (30, 3, "السعر"),  # Price
        # Row 31
        (31, 1, "منتج أ"),
        (31, 2, 10),
        (31, 3, 100.50),
        # Row 32
        (32, 1, "منتج ب"),
        (32, 2, 20),
        (32, 3, 200.00),
    ]

    table_block = TableCandidateBlock(
        row_start=30,
        row_end=32,
        col_start=1,
        col_end=3,
        content=content,
        score=0.75,
        detected_pattern="moderate_numeric_density",
    )

    header_info = detect_table_header_row(table_block)

    assert header_info is not None
    assert header_info.row_index == 30
    assert header_info.values == ["البند", "الكمية", "السعر"]


def test_detect_header_short_table_two_rows():
    """Test detecting header in very short table (2 rows)."""
    # Table with only 2 rows (header + 1 data row)
    content = [
        # Row 35 (header)
        (35, 1, "Item"),
        (35, 2, "Amount"),
        # Row 36 (single data row)
        (36, 1, "Widget"),
        (36, 2, 500.00),
    ]

    table_block = TableCandidateBlock(
        row_start=35,
        row_end=36,
        col_start=1,
        col_end=2,
        content=content,
        score=0.6,
        detected_pattern="column_consistency",
    )

    header_info = detect_table_header_row(table_block)

    assert header_info is not None
    assert header_info.row_index == 35
    assert header_info.values == ["Item", "Amount"]


def test_detect_header_with_numeric_in_header():
    """Test detecting header that contains some numeric values."""
    # Header with year or numbered columns
    content = [
        # Row 40 (header with numbers)
        (40, 1, "Product"),
        (40, 2, "2024"),  # Year in header
        (40, 3, "Q1 Sales"),
        # Row 41
        (41, 1, "Widget A"),
        (41, 2, 1000),
        (41, 3, 500),
        # Row 42
        (42, 1, "Widget B"),
        (42, 2, 2000),
        (42, 3, 750),
    ]

    table_block = TableCandidateBlock(
        row_start=40,
        row_end=42,
        col_start=1,
        col_end=3,
        content=content,
        score=0.7,
        detected_pattern="moderate_numeric_density",
    )

    header_info = detect_table_header_row(table_block)

    assert header_info is not None
    assert header_info.row_index == 40
    # "2024" is a string, not a number, so should be treated as text
    assert header_info.values == ["Product", "2024", "Q1 Sales"]


def test_detect_header_empty_table_block():
    """Test handling of empty table block gracefully."""
    # Empty table block
    table_block = TableCandidateBlock(
        row_start=50,
        row_end=52,
        col_start=1,
        col_end=3,
        content=[],  # No content
        score=0.5,
        detected_pattern="column_consistency",
    )

    header_info = detect_table_header_row(table_block)

    # Should return None gracefully
    assert header_info is None


def test_detect_header_below_threshold():
    """Test that header is not detected if score is below threshold."""
    # Table where no row clearly looks like a header
    content = [
        # Row 55 (ambiguous - mixed text/numeric)
        (55, 1, "A1"),
        (55, 2, 100),
        (55, 3, 200),
        # Row 56
        (56, 1, "B2"),
        (56, 2, 110),
        (56, 3, 210),
        # Row 57
        (57, 1, "C3"),
        (57, 2, 120),
        (57, 3, 220),
    ]

    table_block = TableCandidateBlock(
        row_start=55,
        row_end=57,
        col_start=1,
        col_end=3,
        content=content,
        score=0.8,
        detected_pattern="high_numeric_density",
    )

    # Use a very high threshold
    header_info = detect_table_header_row(table_block, min_score=0.9)

    # Should return None (no row scores high enough)
    assert header_info is None


# ============================================================================
# Test: Input Validation
# ============================================================================


def test_detect_header_invalid_min_score():
    """Test that invalid min_score raises ValueError."""
    content = [(5, 1, "Item"), (5, 2, "Quantity")]

    table_block = TableCandidateBlock(
        row_start=5,
        row_end=5,
        col_start=1,
        col_end=2,
        content=content,
        score=0.7,
        detected_pattern="column_consistency",
    )

    # Test min_score > 1.0
    with pytest.raises(ValueError, match="min_score must be in range 0.0-1.0"):
        detect_table_header_row(table_block, min_score=1.5)

    # Test min_score < 0.0
    with pytest.raises(ValueError, match="min_score must be in range 0.0-1.0"):
        detect_table_header_row(table_block, min_score=-0.1)


# ============================================================================
# Test: TableHeaderInfo Dataclass
# ============================================================================


def test_table_header_info_creation():
    """Test that TableHeaderInfo can be created correctly."""
    header_info = TableHeaderInfo(
        row_index=5,
        col_start=1,
        col_end=4,
        values=["Item", "Quantity", "Price", "Amount"],
        score=0.85,
        detected_pattern="first_row_text_dense",
    )

    assert header_info.row_index == 5
    assert header_info.col_start == 1
    assert header_info.col_end == 4
    assert header_info.values == ["Item", "Quantity", "Price", "Amount"]
    assert header_info.score == 0.85
    assert header_info.detected_pattern == "first_row_text_dense"
