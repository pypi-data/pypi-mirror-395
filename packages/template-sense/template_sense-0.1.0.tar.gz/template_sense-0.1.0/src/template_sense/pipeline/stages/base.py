"""
Base abstractions for pipeline stages.

This module defines the core abstractions that enable modular, testable pipeline
stages. Each stage implements the PipelineStage interface and receives/returns
a PipelineContext object that carries state through all pipeline stages.

The stage pattern enables:
- Independent testing of each stage in isolation
- Clear separation of concerns
- Easy addition/removal/reordering of stages
- Reduced cyclomatic complexity per function
"""

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from template_sense.adapters.excel_adapter import ExcelWorkbook
from template_sense.ai.header_classification import ClassifiedHeaderField
from template_sense.ai.line_item_extraction import ExtractedLineItem
from template_sense.ai.table_column_classification import ClassifiedTableColumn
from template_sense.ai.translation import TranslatedLabel
from template_sense.ai_providers.config import AIConfig
from template_sense.ai_providers.interface import AIProvider
from template_sense.output.canonical_aggregator import CanonicalTemplate
from template_sense.recovery.error_recovery import RecoveryEvent


@dataclass
class PipelineContext:
    """
    Carries state through all pipeline stages.

    This dataclass is progressively populated as each stage executes. Each stage
    reads from and writes to this context, enabling loose coupling between stages
    while maintaining type safety.

    Attributes:
        file_path: Path to the Excel file being processed
        field_dictionary: Structured canonical field dictionary with 'headers' and 'columns' sections
        header_field_dictionary: Internal header dict in dict[str, list[str]] format (set by ValidationStage)
        column_field_dictionary: Internal column dict in dict[str, list[str]] format (set by ValidationStage)
        ai_config: Optional AI provider configuration
        start_time: Pipeline start time for timing calculations
        workbook: Loaded Excel workbook (set by FileLoadingStage)
        sheet_name: Name of selected sheet (set by FileLoadingStage)
        grid: Raw grid data from sheet (set by GridExtractionStage)
        sheet_summary: Heuristic detection results (set by GridExtractionStage)
        ai_provider: Initialized AI provider (set by AIProviderSetupStage)
        ai_payload: Payload for AI classification (set by AIPayloadBuildingStage)
        classified_headers: Classified header fields (set by AIClassificationStage)
        classified_columns: Classified table columns (set by AIClassificationStage)
        extracted_line_items: Extracted line items (set by AIClassificationStage)
        translation_map: Map from original to translated labels (set by TranslationStage)
        header_match_results: Fuzzy match results for headers (set by FuzzyMatchingStage)
        column_match_results: Fuzzy match results for columns (set by FuzzyMatchingStage)
        canonical_template: Aggregated canonical template (set by CanonicalAggregationStage)
        normalized_output: Final normalized output dict (set by NormalizedOutputStage)
        metadata: Pipeline metadata (set by MetadataStage)
        recovery_events: Accumulated recovery events from all stages
    """

    # Input parameters
    file_path: Path
    field_dictionary: dict[str, dict[str, str]]
    ai_config: AIConfig | None = None

    # Internal transformed dictionaries (populated by ValidationStage)
    header_field_dictionary: dict[str, list[str]] = field(default_factory=dict)
    column_field_dictionary: dict[str, list[str]] = field(default_factory=dict)

    # Timing
    start_time: float = field(default_factory=time.perf_counter)

    # Stage outputs (populated progressively)
    workbook: ExcelWorkbook | None = None
    sheet_name: str | None = None
    grid: list[list[Any]] | None = None
    sheet_summary: dict[str, Any] | None = None
    ai_provider: AIProvider | None = None
    ai_payload: dict[str, Any] | None = None

    # AI classification results
    classified_headers: list[ClassifiedHeaderField] = field(default_factory=list)
    classified_columns: list[ClassifiedTableColumn] = field(default_factory=list)
    extracted_line_items: list[ExtractedLineItem] = field(default_factory=list)

    # Translation results
    translation_map: dict[str, TranslatedLabel] = field(default_factory=dict)

    # Mapping results
    header_match_results: list[Any] = field(default_factory=list)
    column_match_results: list[Any] = field(default_factory=list)

    # Final outputs
    canonical_template: CanonicalTemplate | None = None
    normalized_output: dict[str, Any] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    # Recovery tracking
    recovery_events: list[RecoveryEvent] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """
        Return final API response structure.

        Returns:
            Dictionary with normalized_output, recovery_events, and metadata
        """
        return {
            "normalized_output": self.normalized_output,
            "recovery_events": [event.to_dict() for event in self.recovery_events],
            "metadata": self.metadata,
        }


class PipelineStage(ABC):
    """
    Abstract base class for all pipeline stages.

    Each stage implements the execute() method which receives a PipelineContext,
    performs its specific logic, and returns an updated PipelineContext.

    Responsibilities of each stage:
    1. Log stage entry/exit
    2. Execute stage-specific logic
    3. Append any recovery events to context.recovery_events
    4. Return updated context

    Example:
        >>> class MyStage(PipelineStage):
        ...     def __init__(self):
        ...         self.logger = logging.getLogger(__name__)
        ...
        ...     def execute(self, context: PipelineContext) -> PipelineContext:
        ...         self.logger.info("MyStage: Starting...")
        ...         # ... stage logic ...
        ...         self.logger.info("MyStage: Complete")
        ...         return context
    """

    @abstractmethod
    def execute(self, context: PipelineContext) -> PipelineContext:
        """
        Execute this pipeline stage.

        Args:
            context: Current pipeline context with accumulated state

        Returns:
            Updated pipeline context

        Raises:
            May raise exceptions for fatal errors (e.g., FileValidationError,
            ExtractionError). Non-fatal errors should be captured as recovery
            events appended to context.recovery_events.
        """
        raise NotImplementedError


__all__ = ["PipelineContext", "PipelineStage"]
