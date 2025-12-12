"""
Error recovery and partial response handling for the Template Sense pipeline.

This module provides robust error handling for partial AI failures, low confidence scores,
and inconsistent outputs. It allows capturing usable structure from imperfect AI responses
without resorting to all-or-nothing failures.

Design Principles:
- Keep low-confidence fields (don't drop them)
- Flag fields with RecoveryEvent warnings
- Preserve downstream decision-making flexibility
- Deterministic, side-effect free (no AI calls)
- Provider-agnostic design

Usage:
    from template_sense.recovery import (
        RecoverySeverity,
        RecoveryEvent,
        filter_by_ai_confidence,
        filter_by_fuzzy_match_score,
        detect_high_failure_rate,
        aggregate_recovery_events,
    )
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from template_sense.constants import (
    MAX_FIELD_FAILURE_RATE,
    MIN_AI_CONFIDENCE_WARNING,
    MIN_FUZZY_MATCH_WARNING,
)


class RecoverySeverity(Enum):
    """Severity levels for recovery events."""

    INFO = "info"  # Informational events (e.g., missing confidence scores)
    WARNING = "warning"  # Low confidence or quality issues
    ERROR = "error"  # High failure rates or critical issues


@dataclass
class RecoveryEvent:
    """
    Represents a recovery event during the extraction pipeline.

    Attributes:
        severity: The severity level of the event
        stage: Pipeline stage where event occurred (e.g., "ai_classification", "fuzzy_matching")
        message: Human-readable description of the event
        field_identifier: Optional identifier for the field (e.g., field label or canonical key)
        confidence_score: Optional confidence/quality score associated with the event
        metadata: Additional context information as key-value pairs
    """

    severity: RecoverySeverity
    stage: str
    message: str
    field_identifier: str | None = None
    confidence_score: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert RecoveryEvent to a JSON-serializable dictionary.

        Returns:
            Dictionary representation of the event
        """
        return {
            "severity": self.severity.value,
            "stage": self.stage,
            "message": self.message,
            "field_identifier": self.field_identifier,
            "confidence_score": self.confidence_score,
            "metadata": self.metadata,
        }


def filter_by_ai_confidence(
    fields: list[Any],
    min_confidence: float = MIN_AI_CONFIDENCE_WARNING,
) -> tuple[list[Any], list[RecoveryEvent]]:
    """
    Flag fields with low AI confidence scores.

    This function does NOT drop fields - it keeps all fields and generates warning events
    for those below the confidence threshold or missing confidence scores.

    Args:
        fields: List of field objects (should have 'ai_confidence' attribute)
        min_confidence: Minimum acceptable AI confidence (0.0-1.0), defaults to constant

    Returns:
        Tuple of (all_fields, recovery_events)
        - all_fields: The original list unchanged
        - recovery_events: List of RecoveryEvent objects for flagged fields
    """
    events = []

    for field_obj in fields:
        # Get field identifier for reporting
        field_id = getattr(field_obj, "label", None) or getattr(
            field_obj, "canonical_key", str(field_obj)
        )

        # Check if confidence score exists (support both ai_confidence and model_confidence)
        ai_confidence = getattr(field_obj, "model_confidence", None) or getattr(
            field_obj, "ai_confidence", None
        )

        if ai_confidence is None:
            # Missing confidence score - INFO level
            events.append(
                RecoveryEvent(
                    severity=RecoverySeverity.INFO,
                    stage="ai_classification",
                    message=f"Field '{field_id}' has no AI confidence score",
                    field_identifier=field_id,
                    confidence_score=None,
                    metadata={"reason": "missing_confidence"},
                )
            )
        elif ai_confidence < min_confidence:
            # Low confidence - WARNING level
            events.append(
                RecoveryEvent(
                    severity=RecoverySeverity.WARNING,
                    stage="ai_classification",
                    message=f"Field '{field_id}' has low AI confidence: {ai_confidence:.2f} < {min_confidence:.2f}",
                    field_identifier=field_id,
                    confidence_score=ai_confidence,
                    metadata={"threshold": min_confidence, "reason": "low_confidence"},
                )
            )

    return fields, events


def filter_by_fuzzy_match_score(
    fields: list[Any],
    min_score: float = MIN_FUZZY_MATCH_WARNING,
) -> tuple[list[Any], list[RecoveryEvent]]:
    """
    Flag fields with low fuzzy match scores.

    This function does NOT drop fields - it keeps all fields and generates warning events
    for those below the fuzzy match threshold or missing scores.

    Args:
        fields: List of field objects (should have 'fuzzy_match_score' attribute)
        min_score: Minimum acceptable fuzzy match score (0.0-100.0), defaults to constant

    Returns:
        Tuple of (all_fields, recovery_events)
        - all_fields: The original list unchanged
        - recovery_events: List of RecoveryEvent objects for flagged fields
    """
    events = []

    for field_obj in fields:
        # Get field identifier for reporting
        field_id = getattr(field_obj, "label", None) or getattr(
            field_obj, "canonical_key", str(field_obj)
        )

        # Check if fuzzy match score exists
        fuzzy_score = getattr(field_obj, "fuzzy_match_score", None)

        if fuzzy_score is None:
            # Missing fuzzy match score - INFO level
            events.append(
                RecoveryEvent(
                    severity=RecoverySeverity.INFO,
                    stage="fuzzy_matching",
                    message=f"Field '{field_id}' has no fuzzy match score",
                    field_identifier=field_id,
                    confidence_score=None,
                    metadata={"reason": "missing_score"},
                )
            )
        elif fuzzy_score < min_score:
            # Low fuzzy match score - WARNING level
            events.append(
                RecoveryEvent(
                    severity=RecoverySeverity.WARNING,
                    stage="fuzzy_matching",
                    message=f"Field '{field_id}' has low fuzzy match score: {fuzzy_score:.2f} < {min_score:.2f}",
                    field_identifier=field_id,
                    confidence_score=fuzzy_score,
                    metadata={"threshold": min_score, "reason": "low_score"},
                )
            )

    return fields, events


def detect_high_failure_rate(
    total_fields: int,
    failed_fields: int,
    max_rate: float = MAX_FIELD_FAILURE_RATE,
    stage: str = "pipeline",
) -> list[RecoveryEvent]:
    """
    Detect if the field failure rate exceeds an acceptable threshold.

    Args:
        total_fields: Total number of fields processed
        failed_fields: Number of fields that failed processing
        max_rate: Maximum acceptable failure rate (0.0-1.0), defaults to constant
        stage: Pipeline stage identifier for the event

    Returns:
        List containing one ERROR RecoveryEvent if rate exceeded, empty list otherwise
    """
    # Handle edge case: no fields to process
    if total_fields == 0:
        return []

    # Calculate failure rate
    failure_rate = failed_fields / total_fields

    # Check if failure rate exceeds threshold
    if failure_rate > max_rate:
        return [
            RecoveryEvent(
                severity=RecoverySeverity.ERROR,
                stage=stage,
                message=f"High failure rate detected: {failure_rate:.1%} ({failed_fields}/{total_fields} fields) exceeds threshold {max_rate:.1%}",
                field_identifier=None,
                confidence_score=None,
                metadata={
                    "total_fields": total_fields,
                    "failed_fields": failed_fields,
                    "failure_rate": failure_rate,
                    "threshold": max_rate,
                },
            )
        ]

    return []


def aggregate_recovery_events(events: list[RecoveryEvent]) -> dict[str, Any]:
    """
    Aggregate and summarize recovery events.

    Creates a JSON-serializable summary of all recovery events, grouped by severity
    and stage.

    Args:
        events: List of RecoveryEvent objects to aggregate

    Returns:
        Dictionary with structure:
        {
            "total_events": int,
            "by_severity": {"info": int, "warning": int, "error": int},
            "by_stage": {"stage_name": int, ...},
            "events": [event.to_dict(), ...]
        }
    """
    # Initialize counters
    by_severity = {"info": 0, "warning": 0, "error": 0}
    by_stage: dict[str, int] = {}

    # Count events by severity and stage
    for event in events:
        # Count by severity
        severity_key = event.severity.value
        by_severity[severity_key] += 1

        # Count by stage
        stage_key = event.stage
        by_stage[stage_key] = by_stage.get(stage_key, 0) + 1

    # Build summary
    return {
        "total_events": len(events),
        "by_severity": by_severity,
        "by_stage": by_stage,
        "events": [event.to_dict() for event in events],
    }
