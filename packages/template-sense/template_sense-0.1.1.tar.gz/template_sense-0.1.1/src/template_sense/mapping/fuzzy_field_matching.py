"""
Fuzzy field matching layer for mapping translated labels to canonical field keys.

This module provides pure algorithmic fuzzy matching functionality that maps
translated field labels (e.g., "invoice number", "inv no") to Tako's canonical
field dictionary keys (e.g., "invoice_number").

The implementation is:
- Provider-agnostic (no AI calls)
- Deterministic (same inputs always produce same outputs)
- Configurable threshold-based matching
- Optimized for invoice template field names

Architecture Position: Translation → **Fuzzy Matching** → Output

Example Usage:
    >>> from template_sense.ai.translation import TranslatedLabel
    >>> from template_sense.mapping.fuzzy_field_matching import match_fields
    >>>
    >>> # Define Tako's canonical field dictionary
    >>> field_dict = {
    ...     "invoice_number": ["Invoice Number", "Invoice No", "Inv #", "請求書番号"],
    ...     "due_date": ["Due Date", "Payment Due", "支払期日"],
    ... }
    >>>
    >>> # Create translated labels from translation layer
    >>> translated_labels = [
    ...     TranslatedLabel(
    ...         original_text="請求書番号",
    ...         translated_text="Invoice Number",
    ...         detected_source_language="ja"
    ...     ),
    ...     TranslatedLabel(
    ...         original_text="payment due",
    ...         translated_text="payment due",
    ...         detected_source_language="en"
    ...     ),
    ... ]
    >>>
    >>> # Perform fuzzy matching
    >>> results = match_fields(translated_labels, field_dict, threshold=80.0)
    >>> for r in results:
    ...     print(f"{r.translated_text} → {r.canonical_key} (score: {r.match_score})")
    Invoice Number → invoice_number (score: 100.0)
    payment due → due_date (score: 95.2)
"""

import logging
import unicodedata
from dataclasses import dataclass

from rapidfuzz import fuzz

from template_sense.ai.translation import TranslatedLabel
from template_sense.ai_providers.interface import AIProvider
from template_sense.constants import (
    DEFAULT_AUTO_MAPPING_THRESHOLD,
    ENABLE_AI_SEMANTIC_MATCHING,
    SEMANTIC_MATCHING_CONFIDENCE_THRESHOLD,
    SEMANTIC_MATCHING_FUZZY_FLOOR,
)

# Set up module logger
logger = logging.getLogger(__name__)


@dataclass
class FieldMatchResult:
    """
    Result of fuzzy matching a translated label to canonical field keys.

    This dataclass represents the outcome of attempting to match a single
    translated label against Tako's canonical field dictionary. It includes
    the original text, translated text, best matching canonical key (if any),
    confidence score, and the specific dictionary variant that matched best.

    Attributes:
        original_text: Original non-English text from the template
                      (preserved from TranslatedLabel).
        translated_text: English text used for fuzzy matching
                        (from TranslatedLabel.translated_text).
        canonical_key: Best matched canonical field key (e.g., "invoice_number").
                      None if no match meets the threshold.
        match_score: Confidence score of the match (0-100 scale).
                    Higher scores indicate better matches.
        matched_variant: The specific dictionary variant that produced the best match
                        (e.g., "Invoice No" from the variants list).
                        None if no match meets threshold.

    Example:
        >>> result = FieldMatchResult(
        ...     original_text="請求書番号",
        ...     translated_text="invoice number",
        ...     canonical_key="invoice_number",
        ...     match_score=100.0,
        ...     matched_variant="Invoice Number"
        ... )
    """

    original_text: str
    translated_text: str
    canonical_key: str | None
    match_score: float
    matched_variant: str | None


def _normalize_text(text: str) -> str:
    """
    Normalize text for consistent fuzzy matching.

    This function performs several normalization steps to ensure consistent
    matching behavior:
    1. Unicode normalization (NFKC) to handle composed/decomposed characters
    2. Lowercase conversion for case-insensitive matching
    3. Whitespace stripping and collapsing (multiple spaces → single space)

    Args:
        text: Input text to normalize

    Returns:
        Normalized text ready for fuzzy matching

    Example:
        >>> _normalize_text("  Invoice  NUMBER  ")
        'invoice number'
        >>> _normalize_text("Café")  # Unicode normalization
        'café'
    """
    # Unicode normalization (handles diacritics, combining characters, etc.)
    normalized = unicodedata.normalize("NFKC", text)

    # Lowercase and whitespace handling
    normalized = normalized.lower().strip()

    # Collapse multiple whitespace to single space
    return " ".join(normalized.split())


def _calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculate similarity score between two text strings.

    Uses rapidfuzz's token_set_ratio algorithm, which is robust to:
    - Word order differences ("Invoice Number" vs "Number Invoice")
    - Partial matches
    - Extra/missing words

    Args:
        text1: First text string (already normalized)
        text2: Second text string (already normalized)

    Returns:
        Similarity score on 0-100 scale (100 = perfect match)

    Example:
        >>> _calculate_similarity("invoice number", "invoice number")
        100.0
        >>> _calculate_similarity("invoice number", "number invoice")
        100.0
        >>> _calculate_similarity("invoice no", "invoice number")
        76.92  # Approximate
    """
    return fuzz.token_set_ratio(text1, text2)


def _find_best_match(
    translated_text: str,
    field_dictionary: dict[str, list[str]],
    threshold: float,
) -> tuple[str | None, float, str | None]:
    """
    Find the best matching canonical key for a single translated label.

    This function compares the translated text against all canonical keys and
    their variants, tracking the highest scoring match. In case of ties, it
    uses lexicographic ordering of canonical keys for deterministic behavior.

    Args:
        translated_text: Normalized English text to match
        field_dictionary: Mapping of canonical_key -> list of variants
        threshold: Minimum match score (0-100) to accept a match

    Returns:
        Tuple of (canonical_key, match_score, matched_variant):
        - canonical_key: Best matching key, or None if below threshold
        - match_score: Highest score achieved (0-100), or 0.0 if no match
        - matched_variant: Specific variant that produced best score, or None

    Example:
        >>> field_dict = {
        ...     "invoice_number": ["Invoice Number", "Invoice No", "Inv #"],
        ...     "due_date": ["Due Date", "Payment Due"],
        ... }
        >>> _find_best_match("invoice no", field_dict, 80.0)
        ('invoice_number', 100.0, 'Invoice No')
        >>> _find_best_match("xyz", field_dict, 80.0)
        (None, 0.0, None)
    """
    # Normalize the input text once
    normalized_input = _normalize_text(translated_text)

    best_score = 0.0
    best_canonical_key: str | None = None
    best_variant: str | None = None

    # Track ties for deterministic tie-breaking
    tied_matches: list[tuple[str, str]] = []  # List of (canonical_key, variant)

    # Compare against all canonical keys and their variants
    for canonical_key, variants in field_dictionary.items():
        for variant in variants:
            normalized_variant = _normalize_text(variant)
            score = _calculate_similarity(normalized_input, normalized_variant)

            if score > best_score:
                # New best match found
                best_score = score
                best_canonical_key = canonical_key
                best_variant = variant
                tied_matches = [(canonical_key, variant)]

            elif score == best_score and score > 0:
                # Tie detected
                tied_matches.append((canonical_key, variant))

    # If we found a match above threshold
    if best_score >= threshold and best_canonical_key is not None:
        # Handle ties deterministically: lexicographic ordering of canonical_key
        if len(tied_matches) > 1:
            # Sort by canonical_key, then by variant
            tied_matches.sort(key=lambda x: (x[0], x[1]))
            best_canonical_key, best_variant = tied_matches[0]
            logger.debug(
                f"Tie detected (score={best_score}). Selected '{best_canonical_key}' "
                f"via lexicographic ordering from {len(tied_matches)} candidates."
            )

        logger.debug(
            f"Match found: '{translated_text}' → '{best_canonical_key}' "
            f"(score={best_score:.1f}, variant='{best_variant}')"
        )
        return best_canonical_key, best_score, best_variant

    # No match meets threshold
    logger.debug(
        f"No match found for '{translated_text}' above threshold {threshold:.1f} "
        f"(best score: {best_score:.1f})"
    )
    return None, best_score, None


def match_fields(
    translated_labels: list[TranslatedLabel],
    field_dictionary: dict[str, list[str]],
    threshold: float = DEFAULT_AUTO_MAPPING_THRESHOLD,
    ai_provider: AIProvider | None = None,
    enable_semantic_matching: bool = ENABLE_AI_SEMANTIC_MATCHING,
    semantic_confidence_threshold: float = SEMANTIC_MATCHING_CONFIDENCE_THRESHOLD,
) -> list[FieldMatchResult]:
    """
    Match translated labels to canonical field keys using fuzzy matching,
    with optional AI semantic matching fallback.

    This is the main public API for the fuzzy matching layer. It takes a list
    of translated labels (from the translation layer) and maps them to Tako's
    canonical field dictionary using deterministic fuzzy matching. Optionally,
    if fuzzy matching fails and AI semantic matching is enabled, it will use
    AI to determine semantic equivalence.

    Behavior:
    - For each label, compares against all canonical keys and variants (fuzzy matching)
    - Returns best match with score >= threshold
    - If fuzzy match fails (<threshold) and enable_semantic_matching=True and ai_provider provided:
      * Attempts AI semantic matching for scores >= SEMANTIC_MATCHING_FUZZY_FLOOR (30%)
      * Uses AI to determine semantic equivalence (e.g., "FROM" → "shipper")
      * Returns semantic match if AI confidence >= semantic_confidence_threshold
    - If no match meets threshold, returns FieldMatchResult with canonical_key=None
    - Deterministic fuzzy matching: same inputs always produce same outputs
    - Tie-breaking: lexicographic order of canonical_key

    Args:
        translated_labels: List of TranslatedLabel objects from translation layer.
                          These contain the English text to match against.
        field_dictionary: Tako's canonical field dictionary.
                         Format: {canonical_key: [variant1, variant2, ...]}
                         Example: {"invoice_number": ["Invoice No", "Inv #", "請求書番号"]}
        threshold: Minimum match score (0-100) to accept a fuzzy match.
                  Default: 80.0 (from DEFAULT_AUTO_MAPPING_THRESHOLD).
                  Recommended: 80-95 for good matches.
        ai_provider: Optional AI provider for semantic matching fallback.
                    If None or enable_semantic_matching=False, only fuzzy matching is used.
        enable_semantic_matching: Feature flag to enable AI semantic matching fallback.
                                 Default: False (from ENABLE_AI_SEMANTIC_MATCHING constant).
        semantic_confidence_threshold: Minimum AI confidence (0.0-1.0) to accept semantic match.
                                      Default: 0.7 (70%).

    Returns:
        List of FieldMatchResult objects (one per input label, same order).
        Each result contains original_text, translated_text, canonical_key,
        match_score, and matched_variant.

    Raises:
        ValueError: If threshold is not in range [0, 100]

    Example:
        >>> from template_sense.ai.translation import TranslatedLabel
        >>> from template_sense.ai_providers.factory import get_ai_provider
        >>> field_dict = {
        ...     "invoice_number": ["Invoice Number", "Invoice No"],
        ...     "shipper": ["Shipper", "Sender", "From"],
        ... }
        >>> labels = [
        ...     TranslatedLabel("請求書番号", "Invoice Number", "ja"),
        ...     TranslatedLabel("FROM", "FROM", "en"),
        ... ]
        >>> ai_provider = get_ai_provider()
        >>> results = match_fields(labels, field_dict, ai_provider=ai_provider, enable_semantic_matching=True)
        >>> for r in results:
        ...     print(f"{r.translated_text} → {r.canonical_key}")
        Invoice Number → invoice_number
        FROM → shipper  # Matched via AI semantic matching!
    """
    # Validate threshold
    if not (0.0 <= threshold <= 100.0):
        raise ValueError(f"Threshold must be in range [0, 100], got {threshold}")

    # Handle empty input
    if not translated_labels:
        logger.debug("Empty translated_labels list provided, returning empty results")
        return []

    if not field_dictionary:
        logger.warning("Empty field_dictionary provided. All labels will return canonical_key=None")

    logger.info(
        f"Starting fuzzy matching for {len(translated_labels)} labels against "
        f"{len(field_dictionary)} canonical keys (threshold={threshold:.1f})"
    )

    # Check if semantic matching is available
    semantic_matching_available = enable_semantic_matching and ai_provider is not None
    if semantic_matching_available:
        logger.info("AI semantic matching enabled as fallback for low-confidence matches")

    # Process each translated label
    results: list[FieldMatchResult] = []
    matched_count = 0
    unmatched_count = 0
    semantic_matched_count = 0

    for translated_label in translated_labels:
        # Extract translated text for matching
        translated_text = translated_label.translated_text

        # Step 1: Try fuzzy matching first
        canonical_key, match_score, matched_variant = _find_best_match(
            translated_text, field_dictionary, threshold
        )

        # Step 2: If fuzzy succeeded, use it
        if canonical_key is not None:
            result = FieldMatchResult(
                original_text=translated_label.original_text,
                translated_text=translated_text,
                canonical_key=canonical_key,
                match_score=match_score,
                matched_variant=matched_variant,
            )
            results.append(result)
            matched_count += 1
            continue

        # Step 3: If fuzzy failed and semantic matching available, try semantic matching
        if semantic_matching_available and match_score >= SEMANTIC_MATCHING_FUZZY_FLOOR:
            # Lazy import to avoid circular dependency
            from template_sense.mapping.semantic_field_matching import (
                semantic_match_field,
            )

            logger.debug(
                f"Fuzzy match failed for '{translated_text}' (score: {match_score:.1f}%), "
                f"attempting semantic matching"
            )

            try:
                semantic_result = semantic_match_field(
                    translated_label=translated_text,
                    field_dictionary=field_dictionary,
                    ai_provider=ai_provider,
                    best_fuzzy_score=match_score,
                    confidence_threshold=semantic_confidence_threshold,
                )

                # If semantic match succeeded, use it
                if (
                    semantic_result.canonical_key is not None
                    and semantic_result.semantic_confidence >= semantic_confidence_threshold
                ):
                    result = FieldMatchResult(
                        original_text=translated_label.original_text,
                        translated_text=translated_text,
                        canonical_key=semantic_result.canonical_key,
                        match_score=semantic_result.semantic_confidence
                        * 100,  # Convert to 0-100 scale
                        matched_variant=f"AI Semantic: {semantic_result.reasoning}",
                    )
                    results.append(result)
                    matched_count += 1
                    semantic_matched_count += 1
                    logger.info(
                        f"Semantic match found: '{translated_text}' → '{semantic_result.canonical_key}' "
                        f"(AI confidence: {semantic_result.semantic_confidence:.0%})"
                    )
                    continue

            except Exception as e:
                logger.warning(
                    f"Semantic matching failed for '{translated_text}': {str(e)}. "
                    f"Falling back to fuzzy result."
                )

        # Step 4: No match found (neither fuzzy nor semantic)
        result = FieldMatchResult(
            original_text=translated_label.original_text,
            translated_text=translated_text,
            canonical_key=None,
            match_score=match_score,
            matched_variant=None,
        )
        results.append(result)
        unmatched_count += 1

    # Log summary
    if semantic_matched_count > 0:
        logger.info(
            f"Fuzzy matching complete: {matched_count} matched "
            f"({semantic_matched_count} via AI semantic), {unmatched_count} unmatched "
            f"(total: {len(translated_labels)})"
        )
    else:
        logger.info(
            f"Fuzzy matching complete: {matched_count} matched, {unmatched_count} unmatched "
            f"(total: {len(translated_labels)})"
        )

    return results


__all__ = ["FieldMatchResult", "match_fields"]
