"""
AI-powered semantic field matching for fields that fail fuzzy matching.

This module provides an optional AI-based fallback layer that uses semantic
understanding to match fields when literal string similarity is insufficient.

Architecture Position: Translation → Fuzzy Matching → **Semantic Matching** → Output

Example Usage:
    >>> from template_sense.ai_providers.factory import get_ai_provider
    >>> from template_sense.mapping.semantic_field_matching import semantic_match_field
    >>>
    >>> # Define Tako's canonical field dictionary
    >>> field_dict = {
    ...     "shipper": ["Shipper", "Sender", "From", "Consignor"],
    ...     "consignee": ["Consignee", "Receiver", "To", "Recipient"],
    ... }
    >>>
    >>> ai_provider = get_ai_provider()
    >>> result = semantic_match_field(
    ...     translated_label="FROM",
    ...     field_dictionary=field_dict,
    ...     ai_provider=ai_provider,
    ...     best_fuzzy_score=33.3,
    ... )
    >>> print(f"{result.translated_text} → {result.canonical_key} ({result.semantic_confidence:.0%})")
    FROM → shipper (95%)
"""

import json
import logging
from dataclasses import dataclass

from template_sense.ai_providers.interface import AIProvider
from template_sense.constants import (
    SEMANTIC_MATCHING_CONFIDENCE_THRESHOLD,
    SEMANTIC_MATCHING_MAX_TOKENS,
    SEMANTIC_MATCHING_TEMPERATURE,
    SEMANTIC_MATCHING_TIMEOUT_SECONDS,
)
from template_sense.errors import AIProviderError

# Set up module logger
logger = logging.getLogger(__name__)


@dataclass
class SemanticMatchResult:
    """
    Result of AI semantic matching.

    This dataclass represents the outcome of using AI to semantically match
    a field label against Tako's canonical field dictionary. It includes the
    AI's confidence score and reasoning for the match.

    Attributes:
        original_text: Original field label from template (may be non-English).
        translated_text: English text used for semantic matching.
        canonical_key: Best matched canonical field key (e.g., "shipper").
                      None if no semantic match meets the confidence threshold.
        semantic_confidence: AI's confidence in the match (0.0-1.0 scale).
                            Higher scores indicate stronger semantic equivalence.
        reasoning: Brief explanation from AI justifying the match (optional).
                  Useful for debugging and auditing semantic matches.
        fuzzy_fallback_score: Original fuzzy match score (0.0-100.0 scale)
                             for comparison and audit purposes.

    Example:
        >>> result = SemanticMatchResult(
        ...     original_text="FROM",
        ...     translated_text="FROM",
        ...     canonical_key="shipper",
        ...     semantic_confidence=0.95,
        ...     reasoning="'FROM' indicates sender/shipper in logistics context",
        ...     fuzzy_fallback_score=33.3
        ... )
    """

    original_text: str
    translated_text: str
    canonical_key: str | None
    semantic_confidence: float
    reasoning: str | None
    fuzzy_fallback_score: float


def _build_semantic_matching_prompt(
    translated_label: str,
    field_dictionary: dict[str, list[str]],
    best_fuzzy_score: float,
) -> str:
    """
    Build AI prompt for semantic field matching.

    Args:
        translated_label: The translated field label to match
        field_dictionary: Tako's canonical field dictionary
        best_fuzzy_score: The best fuzzy match score for context

    Returns:
        Formatted prompt string for AI provider
    """
    # Format field dictionary for prompt
    dict_lines = []
    for canonical_key, variants in sorted(field_dictionary.items()):
        variants_str = ", ".join(f'"{v}"' for v in variants[:5])  # Limit to 5 variants
        dict_lines.append(f'  - "{canonical_key}": {variants_str}')
    field_dict_formatted = "\n".join(dict_lines)

    return f"""You are a field mapping expert for invoice processing. Determine if the field label is semantically equivalent to any canonical field in Tako's dictionary.

**Field to Match:**
- Label: "{translated_label}"
- Best Fuzzy Match Score: {best_fuzzy_score:.1f}%

**Tako's Canonical Fields:**
{field_dict_formatted}

**Instructions:**
1. Determine if the label is semantically equivalent to ANY canonical field
2. Consider:
   - Business domain context (invoices, shipping, logistics)
   - Common synonyms and abbreviations
   - Language conventions (e.g., "FROM" = shipper in logistics)
   - Intent and purpose of the field
3. If there's a semantic match, return the canonical key and your confidence (0.0-1.0)
4. If no semantic match exists, return null

**Examples:**
- "FROM" → "shipper" (logistics sender)
- "TO" → "consignee" (logistics receiver)
- "SHIPMENT DAY" → "etd" (estimated time of departure)
- "INV NO" → "invoice_number" (invoice identifier)

**Response Format (JSON only, no markdown):**
{{
  "canonical_key": "shipper",
  "confidence": 0.95,
  "reasoning": "'FROM' indicates sender/shipper in logistics context"
}}

**Important:**
- Only match if you're confident (≥0.7)
- When in doubt, return {{"canonical_key": null, "confidence": 0.0, "reasoning": "No semantic equivalence"}}
- Consider the invoice/logistics domain context"""


def semantic_match_field(
    translated_label: str,
    field_dictionary: dict[str, list[str]],
    ai_provider: AIProvider,
    best_fuzzy_score: float,
    confidence_threshold: float = SEMANTIC_MATCHING_CONFIDENCE_THRESHOLD,
    timeout_seconds: int = SEMANTIC_MATCHING_TIMEOUT_SECONDS,
) -> SemanticMatchResult:
    """
    Use AI to semantically match a field label to canonical dictionary.

    This function is called when fuzzy matching fails to meet the threshold.
    It asks the AI to determine if the translated label is semantically
    equivalent to any canonical field in Tako's dictionary.

    Args:
        translated_label: The translated field label to match
        field_dictionary: Tako's canonical field dictionary
        ai_provider: AI provider instance for semantic matching
        best_fuzzy_score: The best fuzzy match score (for context)
        confidence_threshold: Minimum AI confidence to accept match (default: 0.7)
        timeout_seconds: Timeout for AI request (default: 10s)

    Returns:
        SemanticMatchResult with the AI's best match or None if no match

    Raises:
        AIProviderError: If AI request fails (caught and logged, returns no match)

    Example:
        >>> result = semantic_match_field(
        ...     translated_label="FROM",
        ...     field_dictionary={"shipper": ["Shipper", "From"]},
        ...     ai_provider=ai_provider,
        ...     best_fuzzy_score=33.3,
        ... )
        >>> if result.canonical_key:
        ...     print(f"Match: {result.canonical_key} ({result.semantic_confidence:.0%})")
    """
    logger.debug(
        "Attempting semantic match for '%s' (fuzzy score: %.1f%%)",
        translated_label,
        best_fuzzy_score,
    )

    try:
        # Build prompt
        prompt = _build_semantic_matching_prompt(
            translated_label=translated_label,
            field_dictionary=field_dictionary,
            best_fuzzy_score=best_fuzzy_score,
        )

        # Call AI provider using the provider-agnostic interface
        system_msg = "You are a field mapping expert. Return only valid JSON."

        try:
            response_text = ai_provider.generate_text(
                prompt=prompt,
                system_message=system_msg,
                max_tokens=SEMANTIC_MATCHING_MAX_TOKENS,
                temperature=SEMANTIC_MATCHING_TEMPERATURE,
                json_mode=True,
            )
        except AIProviderError as api_error:
            logger.error(
                "Failed to call AI provider for semantic matching: %s",
                str(api_error),
            )
            return SemanticMatchResult(
                original_text=translated_label,
                translated_text=translated_label,
                canonical_key=None,
                semantic_confidence=0.0,
                reasoning=f"API call failed: {str(api_error)}",
                fuzzy_fallback_score=best_fuzzy_score,
            )

        # Parse AI response (expected to be JSON)
        try:
            # Extract JSON from response (handle markdown code blocks if present)
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif response_text.startswith("```"):
                response_text = response_text.split("```")[1].split("```")[0].strip()

            response_data = json.loads(response_text)
            canonical_key = response_data.get("canonical_key")
            confidence = float(response_data.get("confidence", 0.0))
            reasoning = response_data.get("reasoning", "No reasoning provided")

        except (json.JSONDecodeError, ValueError, KeyError) as parse_error:
            logger.warning(
                "Failed to parse AI response for semantic matching: %s. Response: %s",
                str(parse_error),
                response_text[:200],
            )
            return SemanticMatchResult(
                original_text=translated_label,
                translated_text=translated_label,
                canonical_key=None,
                semantic_confidence=0.0,
                reasoning=f"Failed to parse AI response: {str(parse_error)}",
                fuzzy_fallback_score=best_fuzzy_score,
            )

        # Check confidence threshold
        if canonical_key and confidence >= confidence_threshold:
            logger.info(
                "Semantic match found: '%s' → '%s' (confidence: %.0%%, reasoning: %s)",
                translated_label,
                canonical_key,
                confidence,
                reasoning,
            )
            return SemanticMatchResult(
                original_text=translated_label,
                translated_text=translated_label,
                canonical_key=canonical_key,
                semantic_confidence=confidence,
                reasoning=reasoning,
                fuzzy_fallback_score=best_fuzzy_score,
            )

        logger.debug(
            "Semantic match below threshold: '%s' (confidence: %.0%% < %.0%%)",
            translated_label,
            confidence,
            confidence_threshold,
        )
        return SemanticMatchResult(
            original_text=translated_label,
            translated_text=translated_label,
            canonical_key=None,
            semantic_confidence=confidence,
            reasoning=reasoning,
            fuzzy_fallback_score=best_fuzzy_score,
        )

    except AIProviderError as ai_error:
        logger.error(
            "AI provider error during semantic matching for '%s': %s",
            translated_label,
            str(ai_error),
        )
        return SemanticMatchResult(
            original_text=translated_label,
            translated_text=translated_label,
            canonical_key=None,
            semantic_confidence=0.0,
            reasoning=f"AI provider error: {str(ai_error)}",
            fuzzy_fallback_score=best_fuzzy_score,
        )

    except Exception as error:
        logger.error(
            "Unexpected error during semantic matching for '%s': %s",
            translated_label,
            str(error),
            exc_info=True,
        )
        return SemanticMatchResult(
            original_text=translated_label,
            translated_text=translated_label,
            canonical_key=None,
            semantic_confidence=0.0,
            reasoning=f"Unexpected error: {str(error)}",
            fuzzy_fallback_score=best_fuzzy_score,
        )


def semantic_match_fields_batch(
    unmatched_labels: list[tuple[str, float]],
    field_dictionary: dict[str, list[str]],
    ai_provider: AIProvider,
    confidence_threshold: float = SEMANTIC_MATCHING_CONFIDENCE_THRESHOLD,
    timeout_seconds: int = SEMANTIC_MATCHING_TIMEOUT_SECONDS,
) -> list[SemanticMatchResult]:
    """
    Batch process multiple unmatched fields through semantic matching.

    This function is more efficient than calling semantic_match_field() individually
    when multiple fields need semantic matching. However, the current implementation
    calls the AI for each field individually. Future optimization: batch all fields
    in a single AI call.

    Args:
        unmatched_labels: List of (translated_label, fuzzy_score) tuples
        field_dictionary: Tako's canonical field dictionary
        ai_provider: AI provider instance
        confidence_threshold: Minimum AI confidence to accept match
        timeout_seconds: Timeout for each AI request

    Returns:
        List of SemanticMatchResult for each input label

    Example:
        >>> unmatched = [("FROM", 33.3), ("TO", 40.0)]
        >>> results = semantic_match_fields_batch(
        ...     unmatched_labels=unmatched,
        ...     field_dictionary=field_dict,
        ...     ai_provider=ai_provider,
        ... )
    """
    logger.info("Batch semantic matching for %d unmatched fields", len(unmatched_labels))

    results = []
    for translated_label, fuzzy_score in unmatched_labels:
        result = semantic_match_field(
            translated_label=translated_label,
            field_dictionary=field_dictionary,
            ai_provider=ai_provider,
            best_fuzzy_score=fuzzy_score,
            confidence_threshold=confidence_threshold,
            timeout_seconds=timeout_seconds,
        )
        results.append(result)

    # Log summary
    matched_count = sum(1 for r in results if r.canonical_key is not None)
    logger.info(
        "Batch semantic matching complete: %d/%d matched (%.1f%%)",
        matched_count,
        len(results),
        (matched_count / len(results) * 100) if results else 0,
    )

    return results
