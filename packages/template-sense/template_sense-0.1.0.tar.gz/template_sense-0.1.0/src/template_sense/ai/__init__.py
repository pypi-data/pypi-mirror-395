"""
AI-assisted classification and analysis modules.

This package contains modules for AI-based template analysis, including
header field classification, table column classification, line item extraction,
and translation.
"""

from template_sense.ai.header_classification import (
    ClassifiedHeaderField,
    classify_header_fields,
)
from template_sense.ai.line_item_extraction import (
    ExtractedLineItem,
    extract_line_items,
)
from template_sense.ai.table_column_classification import (
    ClassifiedTableColumn,
    classify_table_columns,
)
from template_sense.ai.translation import (
    TranslatedLabel,
    translate_labels,
)

__all__ = [
    "ClassifiedHeaderField",
    "classify_header_fields",
    "ClassifiedTableColumn",
    "classify_table_columns",
    "ExtractedLineItem",
    "extract_line_items",
    "TranslatedLabel",
    "translate_labels",
]
