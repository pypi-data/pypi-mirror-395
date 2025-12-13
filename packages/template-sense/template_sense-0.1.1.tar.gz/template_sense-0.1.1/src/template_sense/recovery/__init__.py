"""
Recovery module for error handling and partial response recovery.

This module provides tools for handling partial AI failures, low confidence scores,
and inconsistent outputs across the extraction pipeline.
"""

from template_sense.recovery.error_recovery import (
    RecoveryEvent,
    RecoverySeverity,
    aggregate_recovery_events,
    detect_high_failure_rate,
    filter_by_ai_confidence,
    filter_by_fuzzy_match_score,
)

__all__ = [
    "RecoverySeverity",
    "RecoveryEvent",
    "filter_by_ai_confidence",
    "filter_by_fuzzy_match_score",
    "detect_high_failure_rate",
    "aggregate_recovery_events",
]
