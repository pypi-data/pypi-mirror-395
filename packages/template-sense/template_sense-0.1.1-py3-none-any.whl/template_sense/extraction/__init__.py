"""
Extraction utilities for Template Sense.

This package contains modules for extracting structured data from Excel templates,
including sheet-level extraction utilities, heuristic-based header detection,
and heuristic-based table detection.
"""

from template_sense.extraction.header_candidates import (
    HeaderCandidateBlock,
    cluster_header_candidate_blocks,
    detect_header_candidate_blocks,
    find_header_candidate_rows,
    score_row_as_header_candidate,
)
from template_sense.extraction.sheet_extractor import (
    extract_non_empty_columns,
    extract_non_empty_rows,
    extract_raw_grid,
    get_used_range,
)
from template_sense.extraction.table_candidates import (
    TableCandidateBlock,
    cluster_table_blocks,
    detect_table_candidate_blocks,
    find_table_candidate_rows,
    score_row_as_table_candidate,
)

__all__ = [
    # Sheet extraction utilities
    "extract_raw_grid",
    "extract_non_empty_rows",
    "extract_non_empty_columns",
    "get_used_range",
    # Header candidate detection
    "HeaderCandidateBlock",
    "score_row_as_header_candidate",
    "find_header_candidate_rows",
    "cluster_header_candidate_blocks",
    "detect_header_candidate_blocks",
    # Table candidate detection
    "TableCandidateBlock",
    "score_row_as_table_candidate",
    "find_table_candidate_rows",
    "cluster_table_blocks",
    "detect_table_candidate_blocks",
]
