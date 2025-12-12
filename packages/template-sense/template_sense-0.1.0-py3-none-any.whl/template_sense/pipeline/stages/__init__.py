"""
Pipeline stages package.

This package contains modular pipeline stages that decompose the extraction
pipeline into independently testable components. Each stage implements the
PipelineStage interface and operates on a PipelineContext object.

The 12 stages are:
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
"""

from template_sense.pipeline.stages.ai_classification import AIClassificationStage
from template_sense.pipeline.stages.ai_payload_building import AIPayloadBuildingStage
from template_sense.pipeline.stages.ai_provider_setup import AIProviderSetupStage
from template_sense.pipeline.stages.base import PipelineContext, PipelineStage
from template_sense.pipeline.stages.canonical_aggregation import (
    CanonicalAggregationStage,
)
from template_sense.pipeline.stages.confidence_filtering import ConfidenceFilteringStage
from template_sense.pipeline.stages.file_loading import FileLoadingStage
from template_sense.pipeline.stages.fuzzy_matching import FuzzyMatchingStage
from template_sense.pipeline.stages.grid_extraction import GridExtractionStage
from template_sense.pipeline.stages.metadata import MetadataStage
from template_sense.pipeline.stages.normalized_output import NormalizedOutputStage
from template_sense.pipeline.stages.translation import TranslationStage
from template_sense.pipeline.stages.validation import ValidationStage

__all__ = [
    # Base abstractions
    "PipelineStage",
    "PipelineContext",
    # Stage implementations
    "ValidationStage",
    "FileLoadingStage",
    "GridExtractionStage",
    "AIProviderSetupStage",
    "AIPayloadBuildingStage",
    "AIClassificationStage",
    "TranslationStage",
    "FuzzyMatchingStage",
    "ConfidenceFilteringStage",
    "CanonicalAggregationStage",
    "NormalizedOutputStage",
    "MetadataStage",
]
