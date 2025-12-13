"""
Header field classification via AI.

This module takes header candidate blocks detected by heuristics and uses
AI providers to classify them semantically, identifying label/value pairs
and their meaning.
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
class ClassifiedHeaderField:
    """
    Represents a header field classified by AI with semantic meaning.

    This dataclass stores the result of AI-based field classification,
    including the original label/value and coordinates. The canonical_key
    will be populated later by the mapping layer (fuzzy matching).

    Attributes:
        canonical_key: Semantic key after mapping (populated by mapping layer).
                      None until mapping is performed.
        raw_label: Original label text from template (may be non-English).
                  Can be None if no clear label was detected.
        raw_value: Associated value from the template.
        block_index: Index of the HeaderCandidateBlock this field came from.
        row_index: Row coordinate in the original grid (1-based Excel convention).
        col_index: Column coordinate in the original grid (1-based Excel convention).
        label_col_offset: Offset from main cell to label cell (0 = same cell, positive = cells to right).
        value_col_offset: Offset from main cell to value cell (0 = same cell, positive = cells to right).
        pattern_type: Type of label-value pattern detected ("multi_cell", "same_cell", or None).
        model_confidence: AI confidence score (0.0-1.0), if provided by the model.
                         None if the provider doesn't return confidence scores.
        metadata: Optional provider-specific or additional classification metadata.
    """

    canonical_key: str | None
    raw_label: str | None
    raw_value: Any
    block_index: int
    row_index: int
    col_index: int
    label_col_offset: int = 0
    value_col_offset: int = 0
    pattern_type: str | None = None
    model_confidence: float | None = None
    metadata: dict[str, Any] | None = None


def classify_header_fields(
    ai_provider: AIProvider,
    payload: dict,
) -> list[ClassifiedHeaderField]:
    """
    Classify header fields using an AI provider.

    This function takes an AI payload (from build_ai_payload()) and uses the
    provided AI provider to classify header fields semantically. The AI model
    identifies label/value pairs and provides confidence scores.

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
        List of ClassifiedHeaderField instances. Returns empty list if no
        headers could be classified.

    Raises:
        AIProviderError: If the API request fails or the response structure
                        is completely invalid (missing required keys, not a dict).
                        Individual field parsing errors are logged but don't raise.

    Example:
        >>> from template_sense.ai_providers import get_ai_provider
        >>> from template_sense.ai_payload_schema import build_ai_payload
        >>>
        >>> provider = get_ai_provider()
        >>> payload = build_ai_payload(sheet_summary, field_dictionary)
        >>> classified = classify_header_fields(provider, payload)
        >>> for field in classified:
        ...     print(f"{field.raw_label}: {field.raw_value}")
    """
    # Delegate to generic orchestrator
    orchestrator = AIClassificationOrchestrator(
        context="headers",
        response_key="headers",
        parser_func=_parse_header_field,
        item_name="header field",
        logger=logger,
    )

    return orchestrator.classify(ai_provider, payload)


def _parse_header_field(
    header_dict: dict[str, Any],
    field_index: int,
) -> ClassifiedHeaderField:
    """
    Parse a single header field dictionary into a ClassifiedHeaderField.

    This helper function validates and extracts required fields from the
    AI response. It handles missing optional fields gracefully.

    Args:
        header_dict: Dictionary containing header field data from AI response.
        field_index: Index of this field in the response list (for error messages).

    Returns:
        ClassifiedHeaderField instance.

    Raises:
        KeyError: If required fields are missing.
        TypeError: If field types are invalid.
        ValueError: If field values are invalid (e.g., negative coordinates).
    """
    if not isinstance(header_dict, dict):
        raise TypeError(
            f"Header field at index {field_index} must be a dict, "
            f"got {type(header_dict).__name__}"
        )

    # Extract required fields
    # Note: raw_label can be None, but the key must be present
    raw_label = header_dict.get("raw_label")
    if raw_label is not None and not isinstance(raw_label, str):
        raise TypeError(f"'raw_label' must be a string or None, got {type(raw_label).__name__}")

    raw_value = header_dict.get("raw_value")
    # raw_value can be any type (including None)

    # Coordinates must be present and be integers
    try:
        block_index = int(header_dict["block_index"])
        row_index = int(header_dict["row_index"])
        col_index = int(header_dict["col_index"])
    except KeyError as e:
        raise KeyError(f"Missing required coordinate field: {e}") from e
    except (TypeError, ValueError) as e:
        raise TypeError(f"Coordinate fields must be integers: {e}") from e

    # Validate coordinate values (must be non-negative)
    if block_index < 0 or row_index < 0 or col_index < 0:
        raise ValueError(
            f"Coordinates must be non-negative: block_index={block_index}, "
            f"row_index={row_index}, col_index={col_index}"
        )

    # Extract optional fields using validation helpers
    model_confidence = validate_confidence(
        header_dict.get("model_confidence"),
        field_index,
        logger,
    )
    metadata = validate_metadata(header_dict.get("metadata"), logger)

    # Extract label/value pattern fields (optional, new in BAT-53)
    label_col_offset = header_dict.get("label_col_offset", 0)
    value_col_offset = header_dict.get("value_col_offset", 0)
    pattern_type = header_dict.get("pattern_type")

    # Validate pattern fields
    try:
        label_col_offset = int(label_col_offset)
        value_col_offset = int(value_col_offset)
    except (TypeError, ValueError):
        logger.warning("Invalid label/value_col_offset values. Using defaults (0, 0).")
        label_col_offset = 0
        value_col_offset = 0

    if pattern_type is not None and pattern_type not in ["multi_cell", "same_cell"]:
        logger.warning(
            "Invalid pattern_type value: %s. Must be 'multi_cell', 'same_cell', or None. Setting to None.",
            pattern_type,
        )
        pattern_type = None

    # canonical_key is not populated by AI (will be set by mapping layer)
    canonical_key = None

    return ClassifiedHeaderField(
        canonical_key=canonical_key,
        raw_label=raw_label,
        raw_value=raw_value,
        block_index=block_index,
        row_index=row_index,
        col_index=col_index,
        label_col_offset=label_col_offset,
        value_col_offset=value_col_offset,
        pattern_type=pattern_type,
        model_confidence=model_confidence,
        metadata=metadata,
    )
