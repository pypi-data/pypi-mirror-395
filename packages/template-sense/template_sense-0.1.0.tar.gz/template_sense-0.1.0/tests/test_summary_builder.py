"""
Unit tests for summary_builder module.

Tests the sheet structure summary builder that aggregates header detection,
table detection, and table header row detection into AI-ready JSON summaries.
"""

from unittest.mock import Mock, patch

import pytest

from template_sense.adapters.excel_adapter import ExcelWorkbook
from template_sense.errors import ExtractionError
from template_sense.extraction.header_candidates import HeaderCandidateBlock
from template_sense.extraction.summary_builder import (
    _convert_value_to_primitive,
    _validate_block_coordinates,
    build_sheet_summary,
    normalize_header_blocks,
    normalize_table_blocks,
)
from template_sense.extraction.table_candidates import TableCandidateBlock
from template_sense.extraction.table_header_detection import TableHeaderInfo


class TestValidateBlockCoordinates:
    """Test _validate_block_coordinates helper function."""

    def test_valid_header_block_coordinates(self):
        """Test validation passes for valid header block coordinates."""
        block = HeaderCandidateBlock(
            row_start=1,
            row_end=3,
            col_start=1,
            col_end=5,
            content=[(1, 1, "test")],
            label_value_pairs=[],
            score=0.8,
            detected_pattern="test",
        )
        assert _validate_block_coordinates(block) is True

    def test_valid_table_block_coordinates(self):
        """Test validation passes for valid table block coordinates."""
        block = TableCandidateBlock(
            row_start=10,
            row_end=15,
            col_start=1,
            col_end=4,
            content=[(10, 1, "test")],
            score=0.8,
            detected_pattern="test",
        )
        assert _validate_block_coordinates(block) is True

    def test_invalid_row_order(self):
        """Test validation fails when row_start > row_end."""
        block = HeaderCandidateBlock(
            row_start=5,
            row_end=3,  # Invalid: start > end
            col_start=1,
            col_end=5,
            content=[(1, 1, "test")],
            label_value_pairs=[],
            score=0.8,
            detected_pattern="test",
        )
        assert _validate_block_coordinates(block) is False

    def test_invalid_col_order(self):
        """Test validation fails when col_start > col_end."""
        block = TableCandidateBlock(
            row_start=1,
            row_end=3,
            col_start=5,
            col_end=3,  # Invalid: start > end
            content=[(1, 1, "test")],
            score=0.8,
            detected_pattern="test",
        )
        assert _validate_block_coordinates(block) is False

    def test_invalid_negative_coordinates(self):
        """Test validation fails for coordinates < 1 (must be 1-based)."""
        block = HeaderCandidateBlock(
            row_start=0,  # Invalid: must be >= 1
            row_end=3,
            col_start=1,
            col_end=5,
            content=[(1, 1, "test")],
            label_value_pairs=[],
            score=0.8,
            detected_pattern="test",
        )
        assert _validate_block_coordinates(block) is False

    def test_empty_content(self):
        """Test validation fails for blocks with empty content."""
        block = HeaderCandidateBlock(
            row_start=1,
            row_end=3,
            col_start=1,
            col_end=5,
            content=[],  # Invalid: empty content
            label_value_pairs=[],
            score=0.8,
            detected_pattern="test",
        )
        assert _validate_block_coordinates(block) is False


class TestConvertValueToPrimitive:
    """Test _convert_value_to_primitive helper function."""

    def test_none_remains_none(self):
        """Test None values pass through unchanged."""
        assert _convert_value_to_primitive(None) is None

    def test_primitives_pass_through(self):
        """Test basic primitives (str, int, float, bool) pass through."""
        assert _convert_value_to_primitive("test") == "test"
        assert _convert_value_to_primitive(42) == 42
        assert _convert_value_to_primitive(3.14) == 3.14
        assert _convert_value_to_primitive(True) is True

    def test_datetime_converts_to_iso(self):
        """Test datetime objects convert to ISO format strings."""
        from datetime import datetime, timezone

        dt = datetime(2024, 1, 15, 10, 30, 0, tzinfo=timezone.utc)
        result = _convert_value_to_primitive(dt)
        assert result == "2024-01-15T10:30:00+00:00"

    def test_date_converts_to_iso(self):
        """Test date objects convert to ISO format strings."""
        from datetime import date

        d = date(2024, 1, 15)
        result = _convert_value_to_primitive(d)
        assert result == "2024-01-15"

    def test_list_recursively_converts(self):
        """Test lists are recursively converted."""
        from datetime import date

        input_list = ["test", 42, date(2024, 1, 15), None]
        result = _convert_value_to_primitive(input_list)
        assert result == ["test", 42, "2024-01-15", None]

    def test_dict_recursively_converts(self):
        """Test dicts are recursively converted."""
        from datetime import datetime, timezone

        input_dict = {
            "name": "test",
            "count": 42,
            "timestamp": datetime(2024, 1, 15, 10, 30, tzinfo=timezone.utc),
        }
        result = _convert_value_to_primitive(input_dict)
        assert result == {
            "name": "test",
            "count": 42,
            "timestamp": "2024-01-15T10:30:00+00:00",
        }

    def test_unknown_type_converts_to_string(self):
        """Test unknown types fall back to string conversion."""

        class CustomClass:
            def __str__(self):
                return "custom_value"

        obj = CustomClass()
        result = _convert_value_to_primitive(obj)
        assert result == "custom_value"


class TestNormalizeHeaderBlocks:
    """Test normalize_header_blocks function."""

    def test_empty_list_returns_empty(self):
        """Test empty block list returns empty list."""
        result = normalize_header_blocks([])
        assert result == []

    def test_single_valid_block(self):
        """Test single valid header block normalizes correctly."""
        block = HeaderCandidateBlock(
            row_start=1,
            row_end=2,
            col_start=1,
            col_end=3,
            content=[
                (1, 1, "Invoice Number: 12345"),
                (2, 1, "Date: 2024-01-01"),
            ],
            label_value_pairs=[
                ("Invoice Number", "12345", 1, 1),
                ("Date", "2024-01-01", 2, 1),
            ],
            score=0.85,
            detected_pattern="key_value_and_keywords",
        )

        result = normalize_header_blocks([block])

        assert len(result) == 1
        assert result[0]["row_start"] == 1
        assert result[0]["row_end"] == 2
        assert result[0]["col_start"] == 1
        assert result[0]["col_end"] == 3
        assert result[0]["score"] == 0.85
        assert result[0]["detected_pattern"] == "key_value_and_keywords"
        assert len(result[0]["content"]) == 2
        assert len(result[0]["label_value_pairs"]) == 2

    def test_filters_low_score_blocks(self):
        """Test blocks below min_score threshold are filtered out."""
        block1 = HeaderCandidateBlock(
            row_start=1,
            row_end=1,
            col_start=1,
            col_end=1,
            content=[(1, 1, "test")],
            label_value_pairs=[],
            score=0.9,  # Above threshold
            detected_pattern="test",
        )
        block2 = HeaderCandidateBlock(
            row_start=5,
            row_end=5,
            col_start=1,
            col_end=1,
            content=[(5, 1, "test")],
            label_value_pairs=[],
            score=0.3,  # Below threshold (0.7)
            detected_pattern="test",
        )

        result = normalize_header_blocks([block1, block2], min_score=0.7)

        assert len(result) == 1
        assert result[0]["score"] == 0.9

    def test_filters_invalid_coordinates(self):
        """Test blocks with invalid coordinates are filtered out."""
        block1 = HeaderCandidateBlock(
            row_start=1,
            row_end=2,
            col_start=1,
            col_end=3,
            content=[(1, 1, "valid")],
            label_value_pairs=[],
            score=0.8,
            detected_pattern="test",
        )
        block2 = HeaderCandidateBlock(
            row_start=5,
            row_end=3,  # Invalid: start > end
            col_start=1,
            col_end=3,
            content=[(5, 1, "invalid")],
            label_value_pairs=[],
            score=0.8,
            detected_pattern="test",
        )

        result = normalize_header_blocks([block1, block2])

        assert len(result) == 1
        assert result[0]["row_start"] == 1

    def test_sorts_by_row_start(self):
        """Test blocks are sorted by row_start for deterministic output."""
        block1 = HeaderCandidateBlock(
            row_start=10,
            row_end=12,
            col_start=1,
            col_end=3,
            content=[(10, 1, "second")],
            label_value_pairs=[],
            score=0.8,
            detected_pattern="test",
        )
        block2 = HeaderCandidateBlock(
            row_start=1,
            row_end=3,
            col_start=1,
            col_end=3,
            content=[(1, 1, "first")],
            label_value_pairs=[],
            score=0.8,
            detected_pattern="test",
        )

        result = normalize_header_blocks([block1, block2])

        assert len(result) == 2
        assert result[0]["row_start"] == 1  # First in sorted order
        assert result[1]["row_start"] == 10  # Second in sorted order

    def test_converts_values_to_primitives(self):
        """Test all values are converted to JSON-serializable primitives."""
        from datetime import date

        block = HeaderCandidateBlock(
            row_start=1,
            row_end=1,
            col_start=1,
            col_end=2,
            content=[
                (1, 1, "text"),
                (1, 2, date(2024, 1, 15)),
            ],
            label_value_pairs=[
                ("Date", date(2024, 1, 15), 1, 2),
            ],
            score=0.8,
            detected_pattern="test",
        )

        result = normalize_header_blocks([block])

        assert result[0]["content"][1][2] == "2024-01-15"  # Date converted to ISO string
        assert result[0]["label_value_pairs"][0]["value"] == "2024-01-15"


class TestNormalizeTableBlocks:
    """Test normalize_table_blocks function."""

    def test_empty_list_returns_empty(self):
        """Test empty block list returns empty list."""
        result = normalize_table_blocks([], {})
        assert result == []

    def test_single_valid_block_without_header(self):
        """Test single valid table block without header normalizes correctly."""
        block = TableCandidateBlock(
            row_start=10,
            row_end=15,
            col_start=1,
            col_end=4,
            content=[
                (10, 1, "Widget"),
                (10, 2, 10),
                (10, 3, 25.50),
                (10, 4, 255.00),
            ],
            score=0.78,
            detected_pattern="high_numeric_density",
        )

        result = normalize_table_blocks([block], {})

        assert len(result) == 1
        assert result[0]["row_start"] == 10
        assert result[0]["row_end"] == 15
        assert result[0]["col_start"] == 1
        assert result[0]["col_end"] == 4
        assert result[0]["score"] == 0.78
        assert result[0]["detected_pattern"] == "high_numeric_density"
        assert result[0]["header_row"] is None
        assert len(result[0]["content"]) == 4

    def test_single_valid_block_with_header(self):
        """Test single valid table block with header normalizes correctly."""
        block = TableCandidateBlock(
            row_start=10,
            row_end=15,
            col_start=1,
            col_end=4,
            content=[
                (10, 1, "Item"),
                (10, 2, "Qty"),
                (10, 3, "Price"),
                (10, 4, "Amount"),
            ],
            score=0.78,
            detected_pattern="high_numeric_density",
        )

        header_info = TableHeaderInfo(
            row_index=10,
            col_start=1,
            col_end=4,
            values=["Item", "Qty", "Price", "Amount"],
            score=0.92,
            detected_pattern="first_row_text_dense",
        )

        result = normalize_table_blocks([block], {10: header_info})

        assert len(result) == 1
        assert result[0]["header_row"] is not None
        assert result[0]["header_row"]["row_index"] == 10
        assert result[0]["header_row"]["values"] == ["Item", "Qty", "Price", "Amount"]
        assert result[0]["header_row"]["score"] == 0.92
        assert result[0]["header_row"]["detected_pattern"] == "first_row_text_dense"

    def test_filters_low_score_blocks(self):
        """Test blocks below min_score threshold are filtered out."""
        block1 = TableCandidateBlock(
            row_start=10,
            row_end=15,
            col_start=1,
            col_end=4,
            content=[(10, 1, "test")],
            score=0.9,  # Above threshold
            detected_pattern="test",
        )
        block2 = TableCandidateBlock(
            row_start=20,
            row_end=25,
            col_start=1,
            col_end=4,
            content=[(20, 1, "test")],
            score=0.3,  # Below threshold (0.7)
            detected_pattern="test",
        )

        result = normalize_table_blocks([block1, block2], {}, min_score=0.7)

        assert len(result) == 1
        assert result[0]["score"] == 0.9

    def test_sorts_by_row_start(self):
        """Test blocks are sorted by row_start for deterministic output."""
        block1 = TableCandidateBlock(
            row_start=20,
            row_end=25,
            col_start=1,
            col_end=4,
            content=[(20, 1, "second")],
            score=0.8,
            detected_pattern="test",
        )
        block2 = TableCandidateBlock(
            row_start=10,
            row_end=15,
            col_start=1,
            col_end=4,
            content=[(10, 1, "first")],
            score=0.8,
            detected_pattern="test",
        )

        result = normalize_table_blocks([block1, block2], {})

        assert len(result) == 2
        assert result[0]["row_start"] == 10  # First in sorted order
        assert result[1]["row_start"] == 20  # Second in sorted order


class TestBuildSheetSummary:
    """Test build_sheet_summary main entry point."""

    @patch("template_sense.extraction.summary_builder.extract_raw_grid")
    @patch("template_sense.extraction.summary_builder.detect_table_candidate_blocks")
    @patch("template_sense.extraction.summary_builder.detect_header_candidate_blocks")
    @patch("template_sense.extraction.summary_builder.detect_table_header_row")
    def test_empty_sheet_returns_empty_summary(
        self,
        mock_detect_table_header,
        mock_detect_headers,
        mock_detect_tables,
        mock_extract_grid,
    ):
        """Test empty sheet returns summary with empty blocks."""
        mock_workbook = Mock(spec=ExcelWorkbook)
        mock_workbook.get_sheet_names.return_value = ["Sheet1"]
        mock_extract_grid.return_value = []

        result = build_sheet_summary(mock_workbook, sheet_name="Sheet1")

        assert result["sheet_name"] == "Sheet1"
        assert result["header_blocks"] == []
        assert result["table_blocks"] == []

    @patch("template_sense.extraction.summary_builder.extract_raw_grid")
    @patch("template_sense.extraction.summary_builder.detect_table_candidate_blocks")
    @patch("template_sense.extraction.summary_builder.detect_header_candidate_blocks")
    @patch("template_sense.extraction.summary_builder.detect_table_header_row")
    def test_sheet_with_only_headers(
        self,
        mock_detect_table_header,
        mock_detect_headers,
        mock_detect_tables,
        mock_extract_grid,
    ):
        """Test sheet with only headers returns headers, no tables."""
        mock_workbook = Mock(spec=ExcelWorkbook)
        mock_workbook.get_sheet_names.return_value = ["Sheet1"]

        # Mock grid with header-like data
        mock_extract_grid.return_value = [
            ["Invoice Number: 12345"],
            ["Date: 2024-01-01"],
        ]

        # No tables detected
        mock_detect_tables.return_value = []

        # One header block detected
        header_block = HeaderCandidateBlock(
            row_start=1,
            row_end=2,
            col_start=1,
            col_end=1,
            content=[(1, 1, "Invoice Number: 12345"), (2, 1, "Date: 2024-01-01")],
            label_value_pairs=[],
            score=0.8,
            detected_pattern="key_value_patterns",
        )
        mock_detect_headers.return_value = [header_block]

        result = build_sheet_summary(mock_workbook, sheet_name="Sheet1")

        assert result["sheet_name"] == "Sheet1"
        assert len(result["header_blocks"]) == 1
        assert len(result["table_blocks"]) == 0

    @patch("template_sense.extraction.summary_builder.extract_raw_grid")
    @patch("template_sense.extraction.summary_builder.detect_table_candidate_blocks")
    @patch("template_sense.extraction.summary_builder.detect_header_candidate_blocks")
    @patch("template_sense.extraction.summary_builder.detect_table_header_row")
    def test_sheet_with_only_tables(
        self,
        mock_detect_table_header,
        mock_detect_headers,
        mock_detect_tables,
        mock_extract_grid,
    ):
        """Test sheet with only tables returns tables, no headers."""
        mock_workbook = Mock(spec=ExcelWorkbook)
        mock_workbook.get_sheet_names.return_value = ["Sheet1"]

        # Mock grid with table-like data
        mock_extract_grid.return_value = [
            ["Item", "Qty", "Price"],
            ["Widget", 10, 25.50],
            ["Gadget", 5, 15.00],
        ]

        # One table detected
        table_block = TableCandidateBlock(
            row_start=1,
            row_end=3,
            col_start=1,
            col_end=3,
            content=[
                (1, 1, "Item"),
                (1, 2, "Qty"),
                (1, 3, "Price"),
                (2, 1, "Widget"),
                (2, 2, 10),
                (2, 3, 25.50),
                (3, 1, "Gadget"),
                (3, 2, 5),
                (3, 3, 15.00),
            ],
            score=0.8,
            detected_pattern="high_numeric_density",
        )
        mock_detect_tables.return_value = [table_block]

        # No headers detected (table exclusion removes all rows)
        mock_detect_headers.return_value = []

        # Table header detected
        header_info = TableHeaderInfo(
            row_index=1,
            col_start=1,
            col_end=3,
            values=["Item", "Qty", "Price"],
            score=0.9,
            detected_pattern="first_row_text_dense",
        )
        mock_detect_table_header.return_value = header_info

        result = build_sheet_summary(mock_workbook, sheet_name="Sheet1")

        assert result["sheet_name"] == "Sheet1"
        assert len(result["header_blocks"]) == 0
        assert len(result["table_blocks"]) == 1
        assert result["table_blocks"][0]["header_row"] is not None

    @patch("template_sense.extraction.summary_builder.extract_raw_grid")
    @patch("template_sense.extraction.summary_builder.detect_table_candidate_blocks")
    @patch("template_sense.extraction.summary_builder.detect_header_candidate_blocks")
    @patch("template_sense.extraction.summary_builder.detect_table_header_row")
    def test_sheet_with_headers_and_tables(
        self,
        mock_detect_table_header,
        mock_detect_headers,
        mock_detect_tables,
        mock_extract_grid,
    ):
        """Test sheet with both headers and tables returns complete summary."""
        mock_workbook = Mock(spec=ExcelWorkbook)
        mock_workbook.get_sheet_names.return_value = ["Sheet1"]

        # Mock grid with headers and table
        mock_extract_grid.return_value = [
            ["Invoice Number: 12345"],
            ["Date: 2024-01-01"],
            [None],
            ["Item", "Qty", "Price"],
            ["Widget", 10, 25.50],
            ["Gadget", 5, 15.00],
        ]

        # One table detected
        table_block = TableCandidateBlock(
            row_start=4,
            row_end=6,
            col_start=1,
            col_end=3,
            content=[(4, 1, "Item"), (4, 2, "Qty"), (4, 3, "Price")],
            score=0.8,
            detected_pattern="high_numeric_density",
        )
        mock_detect_tables.return_value = [table_block]

        # One header block detected
        header_block = HeaderCandidateBlock(
            row_start=1,
            row_end=2,
            col_start=1,
            col_end=1,
            content=[(1, 1, "Invoice Number: 12345"), (2, 1, "Date: 2024-01-01")],
            label_value_pairs=[],
            score=0.8,
            detected_pattern="key_value_patterns",
        )
        mock_detect_headers.return_value = [header_block]

        # Table header detected
        header_info = TableHeaderInfo(
            row_index=4,
            col_start=1,
            col_end=3,
            values=["Item", "Qty", "Price"],
            score=0.9,
            detected_pattern="first_row_text_dense",
        )
        mock_detect_table_header.return_value = header_info

        result = build_sheet_summary(mock_workbook, sheet_name="Sheet1")

        assert result["sheet_name"] == "Sheet1"
        assert len(result["header_blocks"]) == 1
        assert len(result["table_blocks"]) == 1

    def test_invalid_min_score_raises_error(self):
        """Test invalid min_score raises ValueError."""
        mock_workbook = Mock(spec=ExcelWorkbook)

        with pytest.raises(ValueError, match="min_score must be in range 0.0-1.0"):
            build_sheet_summary(mock_workbook, min_score=1.5)

        with pytest.raises(ValueError, match="min_score must be in range 0.0-1.0"):
            build_sheet_summary(mock_workbook, min_score=-0.1)

    def test_no_sheet_name_uses_first_visible(self):
        """Test when sheet_name is None, uses first visible sheet."""
        mock_workbook = Mock(spec=ExcelWorkbook)
        mock_workbook.get_sheet_names.return_value = ["First", "Second", "Third"]

        with patch("template_sense.extraction.summary_builder.extract_raw_grid") as mock_extract:
            mock_extract.return_value = []

            result = build_sheet_summary(mock_workbook)

            assert result["sheet_name"] == "First"
            mock_extract.assert_called_once_with(mock_workbook, "First")

    def test_no_visible_sheets_raises_error(self):
        """Test ExtractionError raised when no visible sheets found."""
        mock_workbook = Mock(spec=ExcelWorkbook)
        mock_workbook.get_sheet_names.return_value = []

        with pytest.raises(ExtractionError, match="No visible sheets found"):
            build_sheet_summary(mock_workbook)

    @patch("template_sense.extraction.summary_builder.extract_raw_grid")
    @patch("template_sense.extraction.summary_builder.detect_table_candidate_blocks")
    @patch("template_sense.extraction.summary_builder.detect_header_candidate_blocks")
    @patch("template_sense.extraction.summary_builder.detect_table_header_row")
    def test_deterministic_output(
        self,
        mock_detect_table_header,
        mock_detect_headers,
        mock_detect_tables,
        mock_extract_grid,
    ):
        """Test repeated calls produce identical (deterministic) results."""
        mock_workbook = Mock(spec=ExcelWorkbook)
        mock_workbook.get_sheet_names.return_value = ["Sheet1"]

        # Mock consistent grid
        mock_extract_grid.return_value = [["test", "data"]]
        mock_detect_tables.return_value = []
        mock_detect_headers.return_value = []

        # Call twice
        result1 = build_sheet_summary(mock_workbook, sheet_name="Sheet1")
        result2 = build_sheet_summary(mock_workbook, sheet_name="Sheet1")

        # Results should be identical
        assert result1 == result2
