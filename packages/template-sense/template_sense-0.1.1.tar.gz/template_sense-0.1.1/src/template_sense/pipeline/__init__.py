"""
End-to-end extraction pipeline orchestration.

This module provides the high-level coordination layer that wires together
all extraction, AI classification, translation, mapping, and output building
components into a unified pipeline.
"""

from template_sense.pipeline.extraction_pipeline import run_extraction_pipeline

__all__ = ["run_extraction_pipeline"]
