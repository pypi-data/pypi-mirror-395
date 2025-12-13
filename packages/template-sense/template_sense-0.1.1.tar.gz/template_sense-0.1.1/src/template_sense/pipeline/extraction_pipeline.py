"""
End-to-end extraction pipeline for Template Sense.

This module provides the high-level orchestration that wires together all
extraction, AI classification, translation, mapping, and output building
components into a unified pipeline.

The pipeline executes the following stages:
1. File loading and workbook setup
2. Grid extraction from the selected sheet
3. Heuristic detection of header and table candidates
4. AI provider initialization
5. AI payload construction
6. AI-based classification (headers, columns, line items)
7. Translation of non-English labels
8. Fuzzy matching to canonical field dictionary
9. Confidence filtering and recovery event generation
10. Canonical template aggregation
11. Normalized output building
12. Metadata attachment and return

This module is provider-agnostic and designed to be the internal wrapper
that coordinates all pipeline steps. The public API (Task 38) will build
on top of this module.
"""

import logging
from pathlib import Path
from typing import Any

from template_sense.ai_providers.config import AIConfig

# Set up module logger
logger = logging.getLogger(__name__)


def run_extraction_pipeline(
    file_path: str | Path,
    field_dictionary: dict[str, dict[str, str]],
    ai_config: AIConfig | None = None,
) -> dict[str, Any]:
    """
    Execute end-to-end template extraction pipeline.

    This function orchestrates the complete extraction workflow using modular
    stages. Each stage implements the PipelineStage interface and operates on
    a shared PipelineContext object.

    Pipeline stages:
    1. ValidationStage - Validates inputs
    2. FileLoadingStage - Loads workbook and selects sheet
    3. GridExtractionStage - Extracts grid and builds sheet summary
    4. AIProviderSetupStage - Initializes AI provider
    5. AIPayloadBuildingStage - Builds AI payload
    6. AIClassificationStage - Classifies headers, columns, and line items
    7. TranslationStage - Translates labels to target language
    8. FuzzyMatchingStage - Matches fields to canonical dictionary
    9. ConfidenceFilteringStage - Filters by confidence thresholds
    10. CanonicalAggregationStage - Builds canonical template
    11. NormalizedOutputStage - Builds normalized JSON output
    12. MetadataStage - Builds metadata and closes workbook

    Args:
        file_path: Path to the Excel file (.xlsx or .xls)
        field_dictionary: Canonical field dictionary with multilingual variants.
                         Format: {"canonical_key": ["variant1", "variant2", ...]}
        ai_config: Optional AI provider configuration. If None, loads from environment.

    Returns:
        Dictionary with the following structure:
        {
            "normalized_output": {...},  # JSON-serializable normalized output
            "recovery_events": [...],     # List of recovery event dicts
            "metadata": {
                "sheet_name": str
            }
        }

    Raises:
        FileValidationError: If file is invalid, not found, or unsupported format
        InvalidFieldDictionaryError: If field dictionary is malformed
        ExtractionError: If workbook is empty or grid extraction fails fatally
        AIProviderError: If AI provider initialization fails (not for request failures)

    Example:
        >>> from pathlib import Path
        >>> from template_sense.pipeline.extraction_pipeline import run_extraction_pipeline
        >>>
        >>> field_dict = {
        ...     "invoice_number": ["Invoice Number", "Invoice No", "請求書番号"],
        ...     "due_date": ["Due Date", "Payment Due", "支払期日"],
        ... }
        >>>
        >>> result = run_extraction_pipeline(
        ...     file_path=Path("invoice.xlsx"),
        ...     field_dictionary=field_dict
        ... )
        >>>
        >>> print(result["normalized_output"]["headers"]["matched"])
        >>> print(result["recovery_events"])
        >>> print(result["metadata"]["sheet_name"])
    """
    from template_sense.pipeline.stages import (
        AIClassificationStage,
        AIPayloadBuildingStage,
        AIProviderSetupStage,
        CanonicalAggregationStage,
        ConfidenceFilteringStage,
        FileLoadingStage,
        FuzzyMatchingStage,
        GridExtractionStage,
        MetadataStage,
        NormalizedOutputStage,
        PipelineContext,
        TranslationStage,
        ValidationStage,
    )

    logger.info("=== Starting extraction pipeline ===")
    logger.info("File: %s", file_path)
    logger.info("Field dictionary keys: %d", len(field_dictionary))

    # Convert file_path to Path if string
    if isinstance(file_path, str):
        file_path = Path(file_path)

    # Initialize pipeline context
    context = PipelineContext(
        file_path=file_path,
        field_dictionary=field_dictionary,
        ai_config=ai_config,
    )

    # Define stage sequence
    stages = [
        ValidationStage(),
        FileLoadingStage(),
        GridExtractionStage(),
        AIProviderSetupStage(),
        AIPayloadBuildingStage(),
        AIClassificationStage(),
        TranslationStage(),
        FuzzyMatchingStage(),
        ConfidenceFilteringStage(),
        CanonicalAggregationStage(),
        NormalizedOutputStage(),
        MetadataStage(),
    ]

    # Execute stages sequentially
    for stage in stages:
        context = stage.execute(context)

    # Return final result
    return context.to_dict()


__all__ = ["run_extraction_pipeline"]
