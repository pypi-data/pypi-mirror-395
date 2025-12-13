"""
Output layer for Template Sense.

This module provides canonical data structures, aggregation functionality,
and normalized output transformation for the Template Sense pipeline.
"""

from template_sense.output.canonical_aggregator import (
    CanonicalHeaderField,
    CanonicalLineItem,
    CanonicalTable,
    CanonicalTableColumn,
    CanonicalTemplate,
    CanonicalTemplateInput,
    build_canonical_template,
)
from template_sense.output.normalized_output_builder import build_normalized_output

__all__ = [
    "CanonicalHeaderField",
    "CanonicalTableColumn",
    "CanonicalLineItem",
    "CanonicalTable",
    "CanonicalTemplate",
    "CanonicalTemplateInput",
    "build_canonical_template",
    "build_normalized_output",
]
