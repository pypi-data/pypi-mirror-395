"""
Row-level line item extraction via AI.

This module takes table candidate blocks and their column classifications,
and uses AI providers to extract structured line items (rows) from the table data.
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
class ExtractedLineItem:
    """
    Represents a single line item (row) extracted from a table via AI.

    This dataclass stores the result of AI-based line item extraction,
    including the row data mapped to column classifications. Line items
    may represent actual invoice items or special rows (subtotals, headers).

    Attributes:
        table_index: Index of the table this row belongs to.
        row_index: Row coordinate in original grid (1-based Excel convention).
        line_number: Sequential line item number if present in the data.
                    None if no explicit line number column exists.
        columns: Dict mapping column names to extracted values.
                Keys are canonical_key from column classification (e.g., "product_name").
                Values can be any type (str, int, float, None).
        is_subtotal: Flag indicating if this row is a subtotal/summary row.
                    True for non-item rows (section totals, headers within table).
        model_confidence: AI confidence score (0.0-1.0), if provided.
        metadata: Optional provider-specific data.
    """

    table_index: int
    row_index: int
    line_number: int | None
    columns: dict[str, Any]
    is_subtotal: bool = False
    model_confidence: float | None = None
    metadata: dict[str, Any] | None = None


def extract_line_items(
    ai_provider: AIProvider,
    payload: dict,
) -> list[ExtractedLineItem]:
    """
    Extract line items from table data using an AI provider.

    This function takes an AI payload (containing table candidates and column
    classifications) and uses the provided AI provider to extract structured
    line items row by row. The AI model identifies actual line items vs. subtotal
    rows and maps cell values to the appropriate columns.

    The function is provider-agnostic and works with any AIProvider implementation.
    It handles malformed responses gracefully and prefers partial success over
    complete failure.

    Args:
        ai_provider: An instance implementing the AIProvider interface.
        payload: AI payload dictionary containing:
                - table_candidates: list of table dicts with column classifications
                - field_dictionary: canonical field mappings
                - (optional) other context fields

    Returns:
        List of ExtractedLineItem instances. Returns empty list if no
        line items could be extracted.

    Raises:
        AIProviderError: If the API request fails or the response structure
                        is completely invalid (missing required keys, not a dict).
                        Individual item parsing errors are logged but don't raise.

    Example:
        >>> from template_sense.ai_providers import get_ai_provider
        >>> from template_sense.ai_payload_schema import build_ai_payload
        >>>
        >>> provider = get_ai_provider()
        >>> payload = build_ai_payload(sheet_summary, field_dictionary)
        >>> line_items = extract_line_items(provider, payload)
        >>> for item in line_items:
        ...     print(f"Row {item.row_index}: {item.columns}")
    """
    # Delegate to generic orchestrator
    orchestrator = AIClassificationOrchestrator(
        context="line_items",
        response_key="line_items",
        parser_func=_parse_line_item,
        item_name="line item",
        logger=logger,
    )

    return orchestrator.classify(ai_provider, payload)


def _parse_line_item(
    item_dict: dict[str, Any],
    item_index: int,
) -> ExtractedLineItem:
    """
    Parse a single line item dictionary into an ExtractedLineItem.

    This helper function validates and extracts required fields from the
    AI response. It handles missing optional fields gracefully.

    Args:
        item_dict: Dictionary containing line item data from AI response.
        item_index: Index of this item in the response list (for error messages).

    Returns:
        ExtractedLineItem instance.

    Raises:
        KeyError: If required fields are missing.
        TypeError: If field types are invalid.
        ValueError: If field values are invalid (e.g., negative indices).
    """
    if not isinstance(item_dict, dict):
        raise TypeError(
            f"Line item at index {item_index} must be a dict, got {type(item_dict).__name__}"
        )

    # Extract required fields
    try:
        table_index = int(item_dict["table_index"])
        row_index = int(item_dict["row_index"])
    except KeyError as e:
        raise KeyError(f"Missing required field: {e}") from e
    except (TypeError, ValueError) as e:
        raise TypeError(f"Index fields must be integers: {e}") from e

    # Validate index values (must be non-negative)
    if table_index < 0 or row_index < 0:
        raise ValueError(
            f"Indices must be non-negative: table_index={table_index}, row_index={row_index}"
        )

    # Extract line_number (optional, can be None)
    line_number = item_dict.get("line_number")
    if line_number is not None:
        try:
            line_number = int(line_number)
        except (TypeError, ValueError) as e:
            raise TypeError(f"'line_number' must be an integer or None: {e}") from e

    # Extract columns (required, must be dict, can be empty)
    columns = item_dict.get("columns")
    if columns is None:
        raise KeyError("Missing required field: 'columns'")
    if not isinstance(columns, dict):
        raise TypeError(f"'columns' must be a dict, got {type(columns).__name__}")

    # Extract is_subtotal (optional, defaults to False)
    is_subtotal = item_dict.get("is_subtotal", False)
    if not isinstance(is_subtotal, bool):
        raise TypeError(f"'is_subtotal' must be a bool, got {type(is_subtotal).__name__}")

    # Extract optional fields using validation helpers
    model_confidence = validate_confidence(
        item_dict.get("model_confidence"),
        item_index,
        logger,
    )
    metadata = validate_metadata(item_dict.get("metadata"), logger)

    return ExtractedLineItem(
        table_index=table_index,
        row_index=row_index,
        line_number=line_number,
        columns=columns,
        is_subtotal=is_subtotal,
        model_confidence=model_confidence,
        metadata=metadata,
    )
