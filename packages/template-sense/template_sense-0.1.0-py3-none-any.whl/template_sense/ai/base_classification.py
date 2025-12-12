"""
Generic AI classification orchestrator and validation helpers.

This module provides reusable components for AI-based classification tasks,
eliminating duplication across header, column, and line item classification modules.
"""

import logging
from collections.abc import Callable
from typing import Any, Generic, TypeVar

from template_sense.ai_providers.interface import AIProvider
from template_sense.errors import AIProviderError

# Type variable for generic classification results
T = TypeVar("T")

# Type alias for parser functions
ParserFunc = Callable[[dict[str, Any], int], T]


def validate_confidence(
    value: Any,
    item_index: int,
    logger_instance: logging.Logger,
) -> float | None:
    """
    Validate and coerce a confidence score to [0.0, 1.0] range.

    This helper extracts the duplicated confidence validation logic from all
    three classification modules.

    Args:
        value: The raw confidence value from AI response (can be any type).
        item_index: Index of the item being parsed (for logging).
        logger_instance: Logger instance for warnings.

    Returns:
        Float in [0.0, 1.0] range, or None if invalid or out of range.
    """
    if value is None:
        return None

    try:
        confidence = float(value)
        # Validate confidence range
        if not 0.0 <= confidence <= 1.0:
            logger_instance.warning(
                "model_confidence out of range [0.0, 1.0]: %.2f. Setting to None.",
                confidence,
            )
            return None
        return confidence
    except (TypeError, ValueError):
        logger_instance.warning(
            "Invalid model_confidence value: %s. Setting to None.",
            value,
        )
        return None


def validate_metadata(
    value: Any,
    logger_instance: logging.Logger,
) -> dict[str, Any] | None:
    """
    Validate that metadata is a dict or None.

    This helper extracts the duplicated metadata validation logic from all
    three classification modules.

    Args:
        value: The raw metadata value from AI response (can be any type).
        logger_instance: Logger instance for warnings.

    Returns:
        The metadata dict if valid, or None if invalid type.
    """
    if value is None:
        return None

    if not isinstance(value, dict):
        logger_instance.warning(
            "metadata must be a dict, got %s. Setting to None.",
            type(value).__name__,
        )
        return None

    return value


class AIClassificationOrchestrator(Generic[T]):
    """
    Generic orchestrator for AI-based classification tasks.

    This class encapsulates the common pattern used across header, column, and
    line item classification:
    1. Call AI provider with error handling
    2. Validate response structure
    3. Parse items with partial success semantics
    4. Log summary statistics

    Type Parameters:
        T: The type of classified item (e.g., ClassifiedHeaderField,
           ClassifiedTableColumn, ExtractedLineItem)

    Attributes:
        context: Context string passed to AI provider ("headers", "columns", "line_items").
        response_key: Key in AI response dict containing the items list.
        parser_func: Function to parse a single item dict into type T.
        item_name: Human-readable item name for logging (e.g., "header field").
        logger: Logger instance for this classification task.
    """

    def __init__(
        self,
        context: str,
        response_key: str,
        parser_func: ParserFunc[T],
        item_name: str,
        logger: logging.Logger,
    ):
        """
        Initialize the classification orchestrator.

        Args:
            context: Context string for AI provider ("headers", "columns", "line_items").
            response_key: Key in AI response dict containing the items list.
            parser_func: Function that takes (item_dict, index) and returns parsed item.
            item_name: Human-readable name for logging (e.g., "header field").
            logger: Logger instance to use for all logging.
        """
        self.context = context
        self.response_key = response_key
        self.parser_func = parser_func
        self.item_name = item_name
        self.logger = logger

    def classify(
        self,
        ai_provider: AIProvider,
        payload: dict[str, Any],
    ) -> list[T]:
        """
        Execute classification with full error handling and logging.

        This method implements the common classification flow:
        1. Extract provider info and log debug message
        2. Call AI provider with error handling
        3. Validate response structure (dict, has key, key is list)
        4. Parse items with partial success (skip invalid items)
        5. Log summary statistics

        Args:
            ai_provider: An instance implementing the AIProvider interface.
            payload: AI payload dictionary to send to the provider.

        Returns:
            List of successfully parsed items of type T. Returns empty list
            if no items could be parsed.

        Raises:
            AIProviderError: If the API request fails or the response structure
                           is completely invalid (missing required keys, not a dict).
                           Individual item parsing errors are logged but don't raise.
        """
        provider_name = ai_provider.provider_name
        model_name = ai_provider.model

        # Calculate payload size for logging (approximate)
        payload_size = len(str(payload))

        self.logger.debug(
            "Calling AI provider for %s classification: provider=%s, model=%s, "
            "payload_size=%d bytes",
            self.item_name,
            provider_name,
            model_name,
            payload_size,
        )

        # Call the AI provider with context
        try:
            response = ai_provider.classify_fields(payload, context=self.context)
        except Exception as e:
            # AIProvider implementations should wrap errors in AIProviderError,
            # but catch any unexpected errors here as well
            error_msg = f"AI provider request failed: {str(e)}"
            self.logger.error(
                "%s classification failed for provider=%s, model=%s: %s",
                self.item_name.capitalize(),
                provider_name,
                model_name,
                error_msg,
            )
            if isinstance(e, AIProviderError):
                raise
            raise AIProviderError(
                provider_name=provider_name,
                error_details=str(e),
                request_type="classify_fields",
            ) from e

        # Validate response structure
        if not isinstance(response, dict):
            error_msg = f"Expected dict response, got {type(response).__name__}"
            self.logger.error(
                "Invalid response structure from provider=%s: %s",
                provider_name,
                error_msg,
            )
            raise AIProviderError(
                provider_name=provider_name,
                error_details=error_msg,
                request_type="classify_fields",
            )

        if self.response_key not in response:
            error_msg = f"Response missing required '{self.response_key}' key"
            self.logger.error(
                "Invalid response structure from provider=%s: %s",
                provider_name,
                error_msg,
            )
            raise AIProviderError(
                provider_name=provider_name,
                error_details=error_msg,
                request_type="classify_fields",
            )

        items_data = response[self.response_key]
        if not isinstance(items_data, list):
            error_msg = f"'{self.response_key}' must be a list, got {type(items_data).__name__}"
            self.logger.error(
                "Invalid response structure from provider=%s: %s",
                provider_name,
                error_msg,
            )
            raise AIProviderError(
                provider_name=provider_name,
                error_details=error_msg,
                request_type="classify_fields",
            )

        # Parse individual items
        # Prefer partial success: skip invalid items but continue processing
        classified_items: list[T] = []
        parse_errors = 0

        for idx, item_dict in enumerate(items_data):
            try:
                item = self.parser_func(item_dict, idx)
                classified_items.append(item)
            except (KeyError, TypeError, ValueError) as e:
                # Log the error but continue processing other items
                parse_errors += 1
                self.logger.warning(
                    "Failed to parse %s at index %d from provider=%s: %s. Skipping this item.",
                    self.item_name,
                    idx,
                    provider_name,
                    str(e),
                )
                continue

        # Log summary statistics
        total_items = len(items_data)
        success_count = len(classified_items)
        self.logger.info(
            "%s classification completed: provider=%s, model=%s, "
            "total_items=%d, successfully_parsed=%d, parse_errors=%d",
            self.item_name.capitalize(),
            provider_name,
            model_name,
            total_items,
            success_count,
            parse_errors,
        )

        # Calculate average confidence if available
        confidences = [
            getattr(item, "model_confidence", None)
            for item in classified_items
            if getattr(item, "model_confidence", None) is not None
        ]
        if confidences:
            avg_confidence = sum(confidences) / len(confidences)
            self.logger.debug(
                "Average model confidence: %.2f (based on %d items)",
                avg_confidence,
                len(confidences),
            )

        return classified_items
