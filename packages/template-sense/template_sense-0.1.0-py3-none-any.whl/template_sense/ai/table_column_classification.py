"""
Table column classification via AI.

This module takes table candidate blocks detected by heuristics and uses
AI providers to classify table columns semantically, identifying their
meaning based on header labels and sample data.
"""

import logging
from dataclasses import dataclass
from typing import Any

from template_sense.ai.base_classification import (
    AIClassificationOrchestrator,
    validate_confidence,
    validate_metadata,
)
from template_sense.ai_providers.interface import AIProvider

# Set up module logger
logger = logging.getLogger(__name__)


@dataclass
class ClassifiedTableColumn:
    """
    Represents a single table column classified by AI.

    This dataclass stores the result of AI-based column classification,
    including the original column header, sample values, and position information.
    The canonical_key will be populated later by the mapping layer (fuzzy matching).

    Attributes:
        canonical_key: Semantic key after mapping (populated by mapping layer).
                      None until mapping is performed.
        raw_label: Original column header text from template (may be non-English).
                  Can be None if no clear header was detected.
        raw_position: Column position within the table (0-based).
        table_block_index: Index of the table candidate block this column came from.
        row_index: Row coordinate of the column header in the original grid
                  (1-based Excel convention).
        col_index: Column coordinate in the original grid (1-based Excel convention).
        sample_values: List of sample data values from this column for validation.
        model_confidence: AI confidence score (0.0-1.0), if provided by the model.
                         None if the provider doesn't return confidence scores.
        metadata: Optional provider-specific or additional classification metadata.
    """

    canonical_key: str | None
    raw_label: str | None
    raw_position: int
    table_block_index: int
    row_index: int
    col_index: int
    sample_values: list[Any]
    model_confidence: float | None = None
    metadata: dict[str, Any] | None = None


def classify_table_columns(
    ai_provider: AIProvider,
    payload: dict,
) -> list[ClassifiedTableColumn]:
    """
    Classify table columns using an AI provider.

    This function takes an AI payload (from build_ai_payload()) and uses the
    provided AI provider to classify table columns semantically. The AI model
    identifies column meanings based on header labels and sample data values.

    The function is provider-agnostic and works with any AIProvider implementation.
    It handles malformed responses gracefully and prefers partial success over
    complete failure.

    Args:
        ai_provider: An instance implementing the AIProvider interface.
        payload: AI payload dictionary from build_ai_payload(), containing:
                - sheet_name: str
                - header_candidates: list of header field dicts
                - table_candidates: list of table dicts
                - field_dictionary: canonical field mappings

    Returns:
        List of ClassifiedTableColumn instances. Returns empty list if no
        columns could be classified.

    Raises:
        AIProviderError: If the API request fails or the response structure
                        is completely invalid (missing required keys, not a dict).
                        Individual column parsing errors are logged but don't raise.

    Example:
        >>> from template_sense.ai_providers import get_ai_provider
        >>> from template_sense.ai_payload_schema import build_ai_payload
        >>>
        >>> provider = get_ai_provider()
        >>> payload = build_ai_payload(sheet_summary, field_dictionary)
        >>> classified = classify_table_columns(provider, payload)
        >>> for column in classified:
        ...     print(f"{column.raw_label}: {column.sample_values}")
    """
    # Delegate to generic orchestrator
    orchestrator = AIClassificationOrchestrator(
        context="columns",
        response_key="columns",
        parser_func=_parse_table_column,
        item_name="table column",
        logger=logger,
    )

    return orchestrator.classify(ai_provider, payload)


def _parse_table_column(
    column_dict: dict[str, Any],
    column_index: int,
) -> ClassifiedTableColumn:
    """
    Parse a single table column dictionary into a ClassifiedTableColumn.

    This helper function validates and extracts required fields from the
    AI response. It handles missing optional fields gracefully.

    Args:
        column_dict: Dictionary containing table column data from AI response.
        column_index: Index of this column in the response list (for error messages).

    Returns:
        ClassifiedTableColumn instance.

    Raises:
        KeyError: If required fields are missing.
        TypeError: If field types are invalid.
        ValueError: If field values are invalid (e.g., negative coordinates).
    """
    if not isinstance(column_dict, dict):
        raise TypeError(
            f"Table column at index {column_index} must be a dict, "
            f"got {type(column_dict).__name__}"
        )

    # Extract required fields
    # Note: raw_label can be None, but the key must be present
    raw_label = column_dict.get("raw_label")
    if raw_label is not None and not isinstance(raw_label, str):
        raise TypeError(f"'raw_label' must be a string or None, got {type(raw_label).__name__}")

    # Coordinates and position must be present and be integers
    try:
        raw_position = int(column_dict["raw_position"])
        table_block_index = int(column_dict["table_block_index"])
        row_index = int(column_dict["row_index"])
        col_index = int(column_dict["col_index"])
    except KeyError as e:
        raise KeyError(f"Missing required field: {e}") from e
    except (TypeError, ValueError) as e:
        raise TypeError(f"Position/coordinate fields must be integers: {e}") from e

    # Validate coordinate values (must be non-negative)
    if raw_position < 0 or table_block_index < 0 or row_index < 0 or col_index < 0:
        raise ValueError(
            f"Position/coordinates must be non-negative: raw_position={raw_position}, "
            f"table_block_index={table_block_index}, row_index={row_index}, col_index={col_index}"
        )

    # Extract sample_values (required field)
    sample_values = column_dict.get("sample_values")
    if sample_values is None:
        raise KeyError("Missing required field: 'sample_values'")
    if not isinstance(sample_values, list):
        raise TypeError(f"'sample_values' must be a list, got {type(sample_values).__name__}")
    # sample_values can be an empty list, which is valid

    # Extract optional fields using validation helpers
    model_confidence = validate_confidence(
        column_dict.get("model_confidence"),
        column_index,
        logger,
    )
    metadata = validate_metadata(column_dict.get("metadata"), logger)

    # canonical_key is not populated by AI (will be set by mapping layer)
    canonical_key = None

    return ClassifiedTableColumn(
        canonical_key=canonical_key,
        raw_label=raw_label,
        raw_position=raw_position,
        table_block_index=table_block_index,
        row_index=row_index,
        col_index=col_index,
        sample_values=sample_values,
        model_confidence=model_confidence,
        metadata=metadata,
    )
