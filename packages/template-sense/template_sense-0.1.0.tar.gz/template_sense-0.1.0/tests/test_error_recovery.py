"""
Unit tests for the error recovery module.

Tests cover:
- RecoveryEvent serialization
- filter_by_ai_confidence
- filter_by_fuzzy_match_score
- detect_high_failure_rate
- aggregate_recovery_events
"""

from dataclasses import dataclass

import pytest

from template_sense.constants import (
    MAX_FIELD_FAILURE_RATE,
    MIN_AI_CONFIDENCE_WARNING,
    MIN_FUZZY_MATCH_WARNING,
)
from template_sense.recovery import (
    RecoveryEvent,
    RecoverySeverity,
    aggregate_recovery_events,
    detect_high_failure_rate,
    filter_by_ai_confidence,
    filter_by_fuzzy_match_score,
)

# ============================================================
# Test Fixtures
# ============================================================


@dataclass
class MockField:
    """Mock field object for testing."""

    label: str
    canonical_key: str | None = None
    ai_confidence: float | None = None
    fuzzy_match_score: float | None = None


@pytest.fixture
def sample_canonical_fields():
    """Mix of high/low/missing confidence scores and fuzzy match scores."""
    return [
        # High confidence, high fuzzy match
        MockField(
            label="Invoice Number",
            canonical_key="invoice_number",
            ai_confidence=0.95,
            fuzzy_match_score=95.0,
        ),
        # Low AI confidence, high fuzzy match
        MockField(
            label="Date",
            canonical_key="invoice_date",
            ai_confidence=0.4,
            fuzzy_match_score=88.0,
        ),
        # High AI confidence, low fuzzy match
        MockField(
            label="Total Amount",
            canonical_key="total_amount",
            ai_confidence=0.85,
            fuzzy_match_score=65.0,
        ),
        # Low both
        MockField(
            label="Unknown Field",
            canonical_key="unknown",
            ai_confidence=0.3,
            fuzzy_match_score=45.0,
        ),
        # Missing confidence scores
        MockField(
            label="Shipper Name",
            canonical_key="shipper_name",
            ai_confidence=None,
            fuzzy_match_score=None,
        ),
    ]


# ============================================================
# Test RecoveryEvent
# ============================================================


def test_recovery_event_to_dict_all_fields():
    """Test RecoveryEvent.to_dict() with all fields populated."""
    event = RecoveryEvent(
        severity=RecoverySeverity.WARNING,
        stage="ai_classification",
        message="Low confidence detected",
        field_identifier="invoice_number",
        confidence_score=0.45,
        metadata={"threshold": 0.5, "reason": "low_confidence"},
    )

    result = event.to_dict()

    assert result == {
        "severity": "warning",
        "stage": "ai_classification",
        "message": "Low confidence detected",
        "field_identifier": "invoice_number",
        "confidence_score": 0.45,
        "metadata": {"threshold": 0.5, "reason": "low_confidence"},
    }


def test_recovery_event_to_dict_optional_none():
    """Test RecoveryEvent.to_dict() with optional fields as None."""
    event = RecoveryEvent(
        severity=RecoverySeverity.ERROR,
        stage="pipeline",
        message="High failure rate",
    )

    result = event.to_dict()

    assert result == {
        "severity": "error",
        "stage": "pipeline",
        "message": "High failure rate",
        "field_identifier": None,
        "confidence_score": None,
        "metadata": {},
    }


def test_recovery_event_json_serializable():
    """Verify RecoveryEvent.to_dict() output is JSON-serializable."""
    import json

    event = RecoveryEvent(
        severity=RecoverySeverity.INFO,
        stage="fuzzy_matching",
        message="Missing score",
        field_identifier="test_field",
        confidence_score=None,
        metadata={"reason": "missing_score"},
    )

    # Should not raise
    json_str = json.dumps(event.to_dict())
    assert json_str is not None


# ============================================================
# Test filter_by_ai_confidence
# ============================================================


def test_filter_by_ai_confidence_all_above_threshold():
    """All fields above threshold should produce no events."""
    fields = [
        MockField(label="Field1", ai_confidence=0.8),
        MockField(label="Field2", ai_confidence=0.9),
        MockField(label="Field3", ai_confidence=0.75),
    ]

    result_fields, events = filter_by_ai_confidence(fields, min_confidence=0.5)

    assert result_fields == fields  # All fields returned
    assert len(events) == 0  # No warnings


def test_filter_by_ai_confidence_some_below_threshold():
    """Fields below threshold should generate WARNING events."""
    fields = [
        MockField(label="GoodField", ai_confidence=0.8),
        MockField(label="LowField1", ai_confidence=0.3),
        MockField(label="LowField2", ai_confidence=0.4),
    ]

    result_fields, events = filter_by_ai_confidence(fields, min_confidence=0.5)

    assert result_fields == fields  # All fields kept
    assert len(events) == 2  # Two warnings

    # Verify warning events
    for event in events:
        assert event.severity == RecoverySeverity.WARNING
        assert event.stage == "ai_classification"
        assert "low ai confidence" in event.message.lower()


def test_filter_by_ai_confidence_none_confidence():
    """Fields with None confidence should generate INFO events."""
    fields = [
        MockField(label="Field1", ai_confidence=0.8),
        MockField(label="Field2", ai_confidence=None),
        MockField(label="Field3", ai_confidence=None),
    ]

    result_fields, events = filter_by_ai_confidence(fields, min_confidence=0.5)

    assert result_fields == fields
    assert len(events) == 2  # Two INFO events

    # Verify INFO events
    for event in events:
        assert event.severity == RecoverySeverity.INFO
        assert event.stage == "ai_classification"
        assert "no AI confidence score" in event.message


def test_filter_by_ai_confidence_empty_input():
    """Empty input should return empty events."""
    result_fields, events = filter_by_ai_confidence([])

    assert result_fields == []
    assert events == []


def test_filter_by_ai_confidence_uses_default_threshold():
    """Should use MIN_AI_CONFIDENCE_WARNING constant by default."""
    fields = [
        MockField(label="Field1", ai_confidence=MIN_AI_CONFIDENCE_WARNING - 0.1),
    ]

    _, events = filter_by_ai_confidence(fields)

    assert len(events) == 1
    assert events[0].severity == RecoverySeverity.WARNING


# ============================================================
# Test filter_by_fuzzy_match_score
# ============================================================


def test_filter_by_fuzzy_match_score_all_above_threshold():
    """All fields above threshold should produce no events."""
    fields = [
        MockField(label="Field1", fuzzy_match_score=85.0),
        MockField(label="Field2", fuzzy_match_score=92.0),
        MockField(label="Field3", fuzzy_match_score=78.0),
    ]

    result_fields, events = filter_by_fuzzy_match_score(fields, min_score=70.0)

    assert result_fields == fields
    assert len(events) == 0


def test_filter_by_fuzzy_match_score_some_below_threshold():
    """Fields below threshold should generate WARNING events."""
    fields = [
        MockField(label="GoodField", fuzzy_match_score=85.0),
        MockField(label="LowField1", fuzzy_match_score=50.0),
        MockField(label="LowField2", fuzzy_match_score=65.0),
    ]

    result_fields, events = filter_by_fuzzy_match_score(fields, min_score=70.0)

    assert result_fields == fields  # All fields kept
    assert len(events) == 2  # Two warnings

    for event in events:
        assert event.severity == RecoverySeverity.WARNING
        assert event.stage == "fuzzy_matching"
        assert "low fuzzy match score" in event.message.lower()


def test_filter_by_fuzzy_match_score_none_score():
    """Fields with None fuzzy match score should generate INFO events."""
    fields = [
        MockField(label="Field1", fuzzy_match_score=85.0),
        MockField(label="Field2", fuzzy_match_score=None),
        MockField(label="Field3", fuzzy_match_score=None),
    ]

    result_fields, events = filter_by_fuzzy_match_score(fields, min_score=70.0)

    assert result_fields == fields
    assert len(events) == 2

    for event in events:
        assert event.severity == RecoverySeverity.INFO
        assert event.stage == "fuzzy_matching"
        assert "no fuzzy match score" in event.message


def test_filter_by_fuzzy_match_score_empty_input():
    """Empty input should return empty events."""
    result_fields, events = filter_by_fuzzy_match_score([])

    assert result_fields == []
    assert events == []


def test_filter_by_fuzzy_match_score_uses_default_threshold():
    """Should use MIN_FUZZY_MATCH_WARNING constant by default."""
    fields = [
        MockField(label="Field1", fuzzy_match_score=MIN_FUZZY_MATCH_WARNING - 5.0),
    ]

    _, events = filter_by_fuzzy_match_score(fields)

    assert len(events) == 1
    assert events[0].severity == RecoverySeverity.WARNING


def test_filter_by_fuzzy_match_score_validates_scale():
    """Validate fuzzy match score uses 0.0-100.0 scale."""
    fields = [
        MockField(label="Field1", fuzzy_match_score=69.0),  # Just below 70.0
        MockField(label="Field2", fuzzy_match_score=70.0),  # Exactly at threshold
        MockField(label="Field3", fuzzy_match_score=71.0),  # Just above
    ]

    _, events = filter_by_fuzzy_match_score(fields, min_score=70.0)

    # Only Field1 should trigger warning
    assert len(events) == 1
    assert events[0].field_identifier == "Field1"


# ============================================================
# Test detect_high_failure_rate
# ============================================================


def test_detect_high_failure_rate_below_threshold():
    """Failure rate below threshold should produce no events."""
    events = detect_high_failure_rate(total_fields=10, failed_fields=2, max_rate=0.3)  # 20% failure

    assert len(events) == 0


def test_detect_high_failure_rate_exactly_at_threshold():
    """Failure rate exactly at threshold should produce no events."""
    events = detect_high_failure_rate(total_fields=10, failed_fields=3, max_rate=0.3)  # Exactly 30%

    assert len(events) == 0


def test_detect_high_failure_rate_above_threshold():
    """Failure rate above threshold should produce ERROR event."""
    events = detect_high_failure_rate(
        total_fields=10, failed_fields=4, max_rate=0.3, stage="ai_classification"  # 40%
    )

    assert len(events) == 1
    event = events[0]
    assert event.severity == RecoverySeverity.ERROR
    assert event.stage == "ai_classification"
    assert "40.0%" in event.message or "40%" in event.message
    assert event.metadata["failure_rate"] == 0.4
    assert event.metadata["total_fields"] == 10
    assert event.metadata["failed_fields"] == 4


def test_detect_high_failure_rate_zero_total_fields():
    """Zero total fields should return no events (edge case)."""
    events = detect_high_failure_rate(total_fields=0, failed_fields=0, max_rate=0.3)

    assert len(events) == 0


def test_detect_high_failure_rate_100_percent_failure():
    """100% failure rate should produce ERROR event."""
    events = detect_high_failure_rate(total_fields=5, failed_fields=5, max_rate=0.3)  # 100%

    assert len(events) == 1
    assert events[0].severity == RecoverySeverity.ERROR
    assert events[0].metadata["failure_rate"] == 1.0


def test_detect_high_failure_rate_uses_default_threshold():
    """Should use MAX_FIELD_FAILURE_RATE constant by default."""
    # Create scenario slightly above default threshold
    total = 100
    failed = int(MAX_FIELD_FAILURE_RATE * total) + 1

    events = detect_high_failure_rate(total_fields=total, failed_fields=failed)

    assert len(events) == 1
    assert events[0].severity == RecoverySeverity.ERROR


# ============================================================
# Test aggregate_recovery_events
# ============================================================


def test_aggregate_recovery_events_empty_list():
    """Empty list should return zero counts."""
    result = aggregate_recovery_events([])

    assert result == {
        "total_events": 0,
        "by_severity": {"info": 0, "warning": 0, "error": 0},
        "by_stage": {},
        "events": [],
    }


def test_aggregate_recovery_events_mixed_severities():
    """Mixed severities should be counted correctly."""
    events = [
        RecoveryEvent(
            severity=RecoverySeverity.INFO,
            stage="ai_classification",
            message="Info message",
        ),
        RecoveryEvent(
            severity=RecoverySeverity.WARNING,
            stage="fuzzy_matching",
            message="Warning 1",
        ),
        RecoveryEvent(
            severity=RecoverySeverity.WARNING,
            stage="fuzzy_matching",
            message="Warning 2",
        ),
        RecoveryEvent(
            severity=RecoverySeverity.ERROR,
            stage="pipeline",
            message="Error message",
        ),
    ]

    result = aggregate_recovery_events(events)

    assert result["total_events"] == 4
    assert result["by_severity"] == {"info": 1, "warning": 2, "error": 1}
    assert len(result["events"]) == 4


def test_aggregate_recovery_events_multiple_stages():
    """Multiple stages should be counted correctly."""
    events = [
        RecoveryEvent(
            severity=RecoverySeverity.WARNING,
            stage="ai_classification",
            message="AI warning",
        ),
        RecoveryEvent(
            severity=RecoverySeverity.WARNING,
            stage="ai_classification",
            message="AI warning 2",
        ),
        RecoveryEvent(
            severity=RecoverySeverity.WARNING,
            stage="fuzzy_matching",
            message="Fuzzy warning",
        ),
        RecoveryEvent(severity=RecoverySeverity.ERROR, stage="pipeline", message="Pipeline error"),
    ]

    result = aggregate_recovery_events(events)

    assert result["by_stage"] == {
        "ai_classification": 2,
        "fuzzy_matching": 1,
        "pipeline": 1,
    }


def test_aggregate_recovery_events_serialization():
    """Verify events list is properly serialized."""
    events = [
        RecoveryEvent(
            severity=RecoverySeverity.WARNING,
            stage="ai_classification",
            message="Test",
            field_identifier="test_field",
            confidence_score=0.4,
            metadata={"key": "value"},
        ),
    ]

    result = aggregate_recovery_events(events)

    assert len(result["events"]) == 1
    event_dict = result["events"][0]
    assert event_dict["severity"] == "warning"
    assert event_dict["stage"] == "ai_classification"
    assert event_dict["message"] == "Test"
    assert event_dict["field_identifier"] == "test_field"
    assert event_dict["confidence_score"] == 0.4
    assert event_dict["metadata"] == {"key": "value"}


def test_aggregate_recovery_events_json_serializable():
    """Verify aggregate output is JSON-serializable."""
    import json

    events = [
        RecoveryEvent(
            severity=RecoverySeverity.INFO,
            stage="ai_classification",
            message="Info",
        ),
        RecoveryEvent(
            severity=RecoverySeverity.WARNING,
            stage="fuzzy_matching",
            message="Warning",
        ),
    ]

    result = aggregate_recovery_events(events)

    # Should not raise
    json_str = json.dumps(result)
    assert json_str is not None


# ============================================================
# Integration Tests
# ============================================================


def test_full_pipeline_with_sample_fields(sample_canonical_fields):
    """Test full recovery pipeline with realistic field data."""
    # Run AI confidence filter
    fields_after_ai, ai_events = filter_by_ai_confidence(sample_canonical_fields)

    # Run fuzzy match filter
    fields_after_fuzzy, fuzzy_events = filter_by_fuzzy_match_score(fields_after_ai)

    # Detect high failure rate
    total = len(sample_canonical_fields)
    failed = sum(
        1
        for f in sample_canonical_fields
        if (f.ai_confidence is not None and f.ai_confidence < 0.5)
        or (f.fuzzy_match_score is not None and f.fuzzy_match_score < 70.0)
    )
    failure_events = detect_high_failure_rate(total, failed, max_rate=0.3)

    # Aggregate all events
    all_events = ai_events + fuzzy_events + failure_events
    summary = aggregate_recovery_events(all_events)

    # Verify fields were not dropped
    assert len(fields_after_fuzzy) == len(sample_canonical_fields)

    # Verify we captured various event types
    assert summary["total_events"] > 0
    assert "ai_classification" in summary["by_stage"]
    assert "fuzzy_matching" in summary["by_stage"]


def test_field_identifier_fallback():
    """Test that field identifier falls back correctly when canonical_key is missing."""
    field_with_label_only = MockField(label="Test Field", canonical_key=None)

    _, events = filter_by_ai_confidence([field_with_label_only])

    # Should use label as identifier
    assert events[0].field_identifier == "Test Field"


def test_field_without_label_or_canonical():
    """Test field without label or canonical_key uses string representation."""

    @dataclass
    class MinimalField:
        ai_confidence: float | None = None

    field = MinimalField(ai_confidence=None)

    _, events = filter_by_ai_confidence([field])

    # Should not crash and should have some identifier
    assert len(events) == 1
    assert events[0].field_identifier is not None
