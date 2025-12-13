"""
Mapping layer for fuzzy matching translated labels to canonical field keys.

This package provides functionality for mapping translated field labels to
Tako's canonical field dictionary using fuzzy matching algorithms.
"""

from template_sense.mapping.fuzzy_field_matching import FieldMatchResult, match_fields

__all__ = ["FieldMatchResult", "match_fields"]
