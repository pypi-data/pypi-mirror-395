"""
Unit tests for ai_payload_schema module.

Tests the AI payload schema builder and dataclasses, ensuring correct conversion
from sheet summary format to AI-ready payloads.
"""

import json

import pytest

from template_sense.ai_payload_schema import (
    AIHeaderCandidate,
    AIPayload,
    AITableCandidate,
    AITableHeaderCell,
    AITableHeaderInfo,
    _convert_header_candidates,
    _convert_table_header_info,
    _extract_sample_data_rows,
    build_ai_payload,
)

# ============================================================
# Fixtures
# ============================================================


@pytest.fixture
def tako_field_dictionary():
    """Tako's canonical field dictionary with multilingual aliases."""
    return {
        "invoice_number": ["Invoice number", "Invoice No", "請求書番号"],
        "due_date": ["Due date", "Payment due", "支払期日"],
        "shipper_name": ["Shipper", "Sender", "荷送人"],
        "box_name": ["Box name", "Container", "箱名"],
        "quantity": ["Quantity", "Qty", "数量"],
        "price": ["Price", "Unit price", "単価"],
        "amount": ["Amount", "Total", "金額"],
    }


@pytest.fixture
def header_blocks_sample():
    """Sample header blocks from sheet summary."""
    return [
        {
            "row_start": 1,
            "row_end": 3,
            "col_start": 1,
            "col_end": 5,
            "content": [
                [1, 1, "Invoice Number: INV-12345"],
                [2, 1, "Date: 2024-01-01"],
                [3, 1, "Shipper: Acme Corp"],
            ],
            "label_value_pairs": [
                {"label": "Invoice Number", "value": "INV-12345", "row": 1, "col": 1},
                {"label": "Date", "value": "2024-01-01", "row": 2, "col": 1},
                {"label": "Shipper", "value": "Acme Corp", "row": 3, "col": 1},
            ],
            "score": 0.85,
            "detected_pattern": "key_value_and_keywords",
        }
    ]


@pytest.fixture
def table_block_with_header():
    """Sample table block with header row and 10 data rows."""
    # Create table content: header + 10 data rows
    content = [
        # Header row (row 10)
        [10, 1, "Item"],
        [10, 2, "Quantity"],
        [10, 3, "Price"],
        [10, 4, "Amount"],
    ]

    # Add 10 data rows (rows 11-20)
    for i in range(1, 11):
        row = 10 + i
        content.extend(
            [
                [row, 1, f"Widget {chr(64 + i)}"],  # Widget A, Widget B, etc.
                [row, 2, i * 10],  # 10, 20, 30, ...
                [row, 3, 5.99 + i],  # 6.99, 7.99, 8.99, ...
                [row, 4, (i * 10) * (5.99 + i)],  # Calculated amount
            ]
        )

    return {
        "row_start": 10,
        "row_end": 20,
        "col_start": 1,
        "col_end": 4,
        "header_row": {
            "row_index": 10,
            "col_start": 1,
            "col_end": 4,
            "values": ["Item", "Quantity", "Price", "Amount"],
            "score": 0.92,
            "detected_pattern": "first_row_text_dense",
        },
        "content": content,
        "score": 0.78,
        "detected_pattern": "high_numeric_density",
    }


@pytest.fixture
def table_block_no_header():
    """Sample table block without header row (3 data rows only)."""
    content = [
        # 3 data rows (rows 15-17)
        [15, 1, "Item A"],
        [15, 2, 100],
        [16, 1, "Item B"],
        [16, 2, 200],
        [17, 1, "Item C"],
        [17, 2, 300],
    ]

    return {
        "row_start": 15,
        "row_end": 17,
        "col_start": 1,
        "col_end": 2,
        "header_row": None,  # No header detected
        "content": content,
        "score": 0.65,
        "detected_pattern": "moderate_numeric_density",
    }


# ============================================================
# Test Helper Functions
# ============================================================


def test_convert_header_candidates_normal(header_blocks_sample):
    """Test converting header blocks to header candidates."""
    candidates = _convert_header_candidates(header_blocks_sample)

    assert len(candidates) == 3
    assert all(isinstance(c, AIHeaderCandidate) for c in candidates)

    # Check first candidate
    assert candidates[0].row == 1
    assert candidates[0].col == 1
    assert candidates[0].label == "Invoice Number"
    assert candidates[0].value == "INV-12345"
    assert candidates[0].score == 0.85

    # Check second candidate
    assert candidates[1].label == "Date"
    assert candidates[1].value == "2024-01-01"

    # Check third candidate
    assert candidates[2].label == "Shipper"
    assert candidates[2].value == "Acme Corp"


def test_convert_header_candidates_empty():
    """Test converting empty header blocks."""
    candidates = _convert_header_candidates([])
    assert candidates == []


def test_convert_table_header_info_normal():
    """Test converting table header row dict to dataclass."""
    header_row_dict = {
        "row_index": 10,
        "col_start": 1,
        "col_end": 4,
        "values": ["Item", "Quantity", "Price", "Amount"],
        "score": 0.92,
        "detected_pattern": "first_row_text_dense",
    }

    header_info = _convert_table_header_info(header_row_dict)

    assert isinstance(header_info, AITableHeaderInfo)
    assert header_info.row_index == 10
    assert header_info.detected_pattern == "first_row_text_dense"
    assert len(header_info.cells) == 4

    # Check cells
    assert header_info.cells[0].col == 1
    assert header_info.cells[0].value == "Item"
    assert header_info.cells[0].score == 0.92

    assert header_info.cells[3].col == 4
    assert header_info.cells[3].value == "Amount"


def test_convert_table_header_info_none():
    """Test converting None header row."""
    header_info = _convert_table_header_info(None)
    assert header_info is None


def test_extract_sample_data_rows_with_header(table_block_with_header):
    """Test extracting sample rows from table with header."""
    content = table_block_with_header["content"]

    sample_rows, total_rows = _extract_sample_data_rows(
        table_content=content,
        header_row_index=10,  # Exclude header
        start_row=10,
        end_row=20,
        start_col=1,
        end_col=4,
        max_rows=5,
    )

    # Should have 5 sample rows (not 10, limited by max_rows)
    assert len(sample_rows) == 5
    assert total_rows == 10  # But total is 10

    # Check first row
    assert sample_rows[0] == ["Widget A", 10, 6.99, 69.9]

    # Check second row
    assert sample_rows[1][0] == "Widget B"
    assert sample_rows[1][1] == 20

    # Check last sample row (5th)
    assert sample_rows[4][0] == "Widget E"


def test_extract_sample_data_rows_without_header(table_block_no_header):
    """Test extracting sample rows from table without header."""
    content = table_block_no_header["content"]

    sample_rows, total_rows = _extract_sample_data_rows(
        table_content=content,
        header_row_index=None,  # No header
        start_row=15,
        end_row=17,
        start_col=1,
        end_col=2,
        max_rows=5,
    )

    # All 3 rows included (less than max_rows)
    assert len(sample_rows) == 3
    assert total_rows == 3

    assert sample_rows[0] == ["Item A", 100]
    assert sample_rows[1] == ["Item B", 200]
    assert sample_rows[2] == ["Item C", 300]


def test_extract_sample_data_rows_small_table():
    """Test extracting from very small table (only 2 rows)."""
    content = [
        [5, 1, "A"],
        [5, 2, 1],
        [6, 1, "B"],
        [6, 2, 2],
    ]

    sample_rows, total_rows = _extract_sample_data_rows(
        table_content=content,
        header_row_index=None,
        start_row=5,
        end_row=6,
        start_col=1,
        end_col=2,
        max_rows=5,
    )

    assert len(sample_rows) == 2
    assert total_rows == 2


# ============================================================
# Test build_ai_payload
# ============================================================


def test_build_ai_payload_normal_case(
    header_blocks_sample, table_block_with_header, tako_field_dictionary
):
    """Test building AI payload with headers and table."""
    sheet_summary = {
        "sheet_name": "Invoice",
        "header_blocks": header_blocks_sample,
        "table_blocks": [table_block_with_header],
    }

    payload = build_ai_payload(sheet_summary, tako_field_dictionary)

    # Check top-level structure
    assert payload["sheet_name"] == "Invoice"
    assert "header_candidates" in payload
    assert "table_candidates" in payload
    assert "field_dictionary" in payload

    # Check header candidates
    assert len(payload["header_candidates"]) == 3
    assert payload["header_candidates"][0]["label"] == "Invoice Number"

    # Check table candidates
    assert len(payload["table_candidates"]) == 1
    table = payload["table_candidates"][0]
    assert table["start_row"] == 10
    assert table["end_row"] == 20
    assert table["total_data_rows"] == 10
    assert len(table["sample_data_rows"]) == 5  # Default max_sample_rows

    # Check header row
    assert table["header_row"] is not None
    assert table["header_row"]["row_index"] == 10
    assert len(table["header_row"]["cells"]) == 4

    # Check field dictionary
    assert payload["field_dictionary"] == tako_field_dictionary


def test_build_ai_payload_headers_only(header_blocks_sample, tako_field_dictionary):
    """Test building AI payload with only headers (no tables)."""
    sheet_summary = {
        "sheet_name": "HeadersOnly",
        "header_blocks": header_blocks_sample,
        "table_blocks": [],
    }

    payload = build_ai_payload(sheet_summary, tako_field_dictionary)

    assert payload["sheet_name"] == "HeadersOnly"
    assert len(payload["header_candidates"]) == 3
    assert len(payload["table_candidates"]) == 0
    assert payload["field_dictionary"] == tako_field_dictionary


def test_build_ai_payload_table_only(table_block_with_header, tako_field_dictionary):
    """Test building AI payload with only table (no standalone headers)."""
    sheet_summary = {
        "sheet_name": "TableOnly",
        "header_blocks": [],
        "table_blocks": [table_block_with_header],
    }

    payload = build_ai_payload(sheet_summary, tako_field_dictionary)

    assert payload["sheet_name"] == "TableOnly"
    assert len(payload["header_candidates"]) == 0
    assert len(payload["table_candidates"]) == 1


def test_build_ai_payload_empty(tako_field_dictionary):
    """Test building AI payload with no candidates."""
    sheet_summary = {
        "sheet_name": "Empty",
        "header_blocks": [],
        "table_blocks": [],
    }

    payload = build_ai_payload(sheet_summary, tako_field_dictionary)

    assert payload["sheet_name"] == "Empty"
    assert len(payload["header_candidates"]) == 0
    assert len(payload["table_candidates"]) == 0
    assert payload["field_dictionary"] == tako_field_dictionary


def test_build_ai_payload_multiple_tables(
    table_block_with_header, table_block_no_header, tako_field_dictionary
):
    """Test building AI payload with multiple tables."""
    sheet_summary = {
        "sheet_name": "MultiTable",
        "header_blocks": [],
        "table_blocks": [table_block_with_header, table_block_no_header],
    }

    payload = build_ai_payload(sheet_summary, tako_field_dictionary)

    assert len(payload["table_candidates"]) == 2

    # First table (with header)
    assert payload["table_candidates"][0]["header_row"] is not None
    assert payload["table_candidates"][0]["total_data_rows"] == 10

    # Second table (no header)
    assert payload["table_candidates"][1]["header_row"] is None
    assert payload["table_candidates"][1]["total_data_rows"] == 3


def test_build_ai_payload_table_without_header(table_block_no_header, tako_field_dictionary):
    """Test building AI payload with table that has no detected header."""
    sheet_summary = {
        "sheet_name": "NoHeader",
        "header_blocks": [],
        "table_blocks": [table_block_no_header],
    }

    payload = build_ai_payload(sheet_summary, tako_field_dictionary)

    table = payload["table_candidates"][0]
    assert table["header_row"] is None
    assert len(table["sample_data_rows"]) == 3
    assert table["total_data_rows"] == 3


def test_build_ai_payload_small_table(tako_field_dictionary):
    """Test building AI payload with small table (only 3 rows)."""
    small_table = {
        "row_start": 5,
        "row_end": 7,
        "col_start": 1,
        "col_end": 2,
        "header_row": None,
        "content": [
            [5, 1, "A"],
            [5, 2, 1],
            [6, 1, "B"],
            [6, 2, 2],
            [7, 1, "C"],
            [7, 2, 3],
        ],
        "score": 0.7,
        "detected_pattern": "small_table",
    }

    sheet_summary = {
        "sheet_name": "SmallTable",
        "header_blocks": [],
        "table_blocks": [small_table],
    }

    payload = build_ai_payload(sheet_summary, tako_field_dictionary)

    table = payload["table_candidates"][0]
    # All 3 rows included (not truncated to 5)
    assert len(table["sample_data_rows"]) == 3
    assert table["total_data_rows"] == 3


def test_build_ai_payload_multilingual_field_dict(header_blocks_sample, table_block_with_header):
    """Test AI payload preserves multilingual field dictionary."""
    multilingual_dict = {
        "invoice_number": ["Invoice number", "請求書番号", "发票号码"],
        "box_name": ["Box name", "箱名", "箱子名称"],
        "quantity": ["Quantity", "数量", "數量"],
    }

    sheet_summary = {
        "sheet_name": "Multilingual",
        "header_blocks": header_blocks_sample,
        "table_blocks": [table_block_with_header],
    }

    payload = build_ai_payload(sheet_summary, multilingual_dict)

    # Field dictionary should be preserved exactly
    assert payload["field_dictionary"] == multilingual_dict
    assert "請求書番号" in payload["field_dictionary"]["invoice_number"]
    assert "发票号码" in payload["field_dictionary"]["invoice_number"]


def test_build_ai_payload_json_serializable(
    header_blocks_sample, table_block_with_header, tako_field_dictionary
):
    """Test that AI payload is fully JSON-serializable."""
    sheet_summary = {
        "sheet_name": "JSONTest",
        "header_blocks": header_blocks_sample,
        "table_blocks": [table_block_with_header],
    }

    payload = build_ai_payload(sheet_summary, tako_field_dictionary)

    # Should not raise exception
    json_str = json.dumps(payload)
    assert isinstance(json_str, str)

    # Should be deserializable
    deserialized = json.loads(json_str)
    assert deserialized["sheet_name"] == "JSONTest"


def test_build_ai_payload_custom_max_sample_rows(table_block_with_header, tako_field_dictionary):
    """Test building AI payload with custom max_sample_rows."""
    sheet_summary = {
        "sheet_name": "CustomMax",
        "header_blocks": [],
        "table_blocks": [table_block_with_header],
    }

    # Request only 3 sample rows
    payload = build_ai_payload(sheet_summary, tako_field_dictionary, max_sample_rows=3)

    table = payload["table_candidates"][0]
    assert len(table["sample_data_rows"]) == 3  # Limited to 3
    assert table["total_data_rows"] == 10  # But total is still 10


def test_build_ai_payload_invalid_max_sample_rows(header_blocks_sample, tako_field_dictionary):
    """Test that invalid max_sample_rows raises ValueError."""
    sheet_summary = {
        "sheet_name": "Invalid",
        "header_blocks": header_blocks_sample,
        "table_blocks": [],
    }

    with pytest.raises(ValueError, match="max_sample_rows must be >= 1"):
        build_ai_payload(sheet_summary, tako_field_dictionary, max_sample_rows=0)

    with pytest.raises(ValueError, match="max_sample_rows must be >= 1"):
        build_ai_payload(sheet_summary, tako_field_dictionary, max_sample_rows=-1)


# ============================================================
# Test Dataclass Structure
# ============================================================


def test_ai_header_candidate_dataclass():
    """Test AIHeaderCandidate dataclass creation."""
    candidate = AIHeaderCandidate(row=1, col=1, label="Invoice", value="12345", score=0.85)

    assert candidate.row == 1
    assert candidate.col == 1
    assert candidate.label == "Invoice"
    assert candidate.value == "12345"
    assert candidate.score == 0.85


def test_ai_table_header_cell_dataclass():
    """Test AITableHeaderCell dataclass creation."""
    cell = AITableHeaderCell(col=3, value="Quantity", score=0.92)

    assert cell.col == 3
    assert cell.value == "Quantity"
    assert cell.score == 0.92


def test_ai_table_header_info_dataclass():
    """Test AITableHeaderInfo dataclass creation."""
    cells = [
        AITableHeaderCell(col=1, value="Item", score=0.9),
        AITableHeaderCell(col=2, value="Qty", score=0.92),
    ]

    header_info = AITableHeaderInfo(
        row_index=10, cells=cells, detected_pattern="first_row_text_dense"
    )

    assert header_info.row_index == 10
    assert len(header_info.cells) == 2
    assert header_info.detected_pattern == "first_row_text_dense"


def test_ai_table_candidate_dataclass():
    """Test AITableCandidate dataclass creation."""
    header_info = AITableHeaderInfo(
        row_index=10,
        cells=[AITableHeaderCell(col=1, value="Item", score=0.9)],
        detected_pattern="first_row_text_dense",
    )

    table = AITableCandidate(
        start_row=10,
        end_row=20,
        start_col=1,
        end_col=4,
        header_row=header_info,
        sample_data_rows=[["A", 1, 2, 3], ["B", 4, 5, 6]],
        total_data_rows=10,
        score=0.78,
        detected_pattern="high_numeric_density",
    )

    assert table.start_row == 10
    assert table.header_row == header_info
    assert len(table.sample_data_rows) == 2
    assert table.total_data_rows == 10


def test_ai_payload_dataclass(tako_field_dictionary):
    """Test AIPayload dataclass creation."""
    payload = AIPayload(
        sheet_name="Test",
        header_candidates=[],
        table_candidates=[],
        field_dictionary=tako_field_dictionary,
    )

    assert payload.sheet_name == "Test"
    assert payload.header_candidates == []
    assert payload.table_candidates == []
    assert payload.field_dictionary == tako_field_dictionary
