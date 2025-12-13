"""
Tests for base_classification module (generic AI classification orchestrator).
"""

import logging
from dataclasses import dataclass
from typing import Any
from unittest.mock import Mock

import pytest

from template_sense.ai.base_classification import (
    AIClassificationOrchestrator,
    validate_confidence,
    validate_metadata,
)
from template_sense.errors import AIProviderError


# Simple test dataclass for orchestrator tests
@dataclass
class TestItem:
    """Simple test item for orchestrator testing."""

    value: str
    index: int
    model_confidence: float | None = None


class TestValidateConfidence:
    """Tests for validate_confidence helper."""

    def test_validate_confidence_valid_float(self):
        """Test valid confidence value in range."""
        logger = Mock(spec=logging.Logger)
        result = validate_confidence(0.85, 0, logger)
        assert result == 0.85
        logger.warning.assert_not_called()

    def test_validate_confidence_valid_boundaries(self):
        """Test boundary values 0.0 and 1.0."""
        logger = Mock(spec=logging.Logger)
        assert validate_confidence(0.0, 0, logger) == 0.0
        assert validate_confidence(1.0, 0, logger) == 1.0
        logger.warning.assert_not_called()

    def test_validate_confidence_out_of_range_negative(self):
        """Test negative confidence value."""
        logger = Mock(spec=logging.Logger)
        result = validate_confidence(-0.1, 0, logger)
        assert result is None
        logger.warning.assert_called_once()
        assert "out of range" in str(logger.warning.call_args)

    def test_validate_confidence_out_of_range_high(self):
        """Test confidence value above 1.0."""
        logger = Mock(spec=logging.Logger)
        result = validate_confidence(1.5, 0, logger)
        assert result is None
        logger.warning.assert_called_once()
        assert "out of range" in str(logger.warning.call_args)

    def test_validate_confidence_invalid_type_string(self):
        """Test invalid type (string)."""
        logger = Mock(spec=logging.Logger)
        result = validate_confidence("not a number", 0, logger)
        assert result is None
        logger.warning.assert_called_once()
        assert "Invalid" in str(logger.warning.call_args)

    def test_validate_confidence_invalid_type_dict(self):
        """Test invalid type (dict)."""
        logger = Mock(spec=logging.Logger)
        result = validate_confidence({"confidence": 0.5}, 0, logger)
        assert result is None
        logger.warning.assert_called_once()

    def test_validate_confidence_none(self):
        """Test None value (should return None without warning)."""
        logger = Mock(spec=logging.Logger)
        result = validate_confidence(None, 0, logger)
        assert result is None
        logger.warning.assert_not_called()

    def test_validate_confidence_coerce_int(self):
        """Test coercion from int to float."""
        logger = Mock(spec=logging.Logger)
        result = validate_confidence(1, 0, logger)
        assert result == 1.0
        assert isinstance(result, float)
        logger.warning.assert_not_called()

    def test_validate_confidence_coerce_string_number(self):
        """Test coercion from string number."""
        logger = Mock(spec=logging.Logger)
        result = validate_confidence("0.75", 0, logger)
        assert result == 0.75
        logger.warning.assert_not_called()


class TestValidateMetadata:
    """Tests for validate_metadata helper."""

    def test_validate_metadata_valid_dict(self):
        """Test valid metadata dict."""
        logger = Mock(spec=logging.Logger)
        metadata = {"key": "value", "count": 42}
        result = validate_metadata(metadata, logger)
        assert result == metadata
        logger.warning.assert_not_called()

    def test_validate_metadata_empty_dict(self):
        """Test empty dict (valid)."""
        logger = Mock(spec=logging.Logger)
        result = validate_metadata({}, logger)
        assert result == {}
        logger.warning.assert_not_called()

    def test_validate_metadata_none(self):
        """Test None value (should return None without warning)."""
        logger = Mock(spec=logging.Logger)
        result = validate_metadata(None, logger)
        assert result is None
        logger.warning.assert_not_called()

    def test_validate_metadata_invalid_type_string(self):
        """Test invalid type (string)."""
        logger = Mock(spec=logging.Logger)
        result = validate_metadata("not a dict", logger)
        assert result is None
        logger.warning.assert_called_once()
        assert "must be a dict" in str(logger.warning.call_args)

    def test_validate_metadata_invalid_type_list(self):
        """Test invalid type (list)."""
        logger = Mock(spec=logging.Logger)
        result = validate_metadata([1, 2, 3], logger)
        assert result is None
        logger.warning.assert_called_once()

    def test_validate_metadata_invalid_type_int(self):
        """Test invalid type (int)."""
        logger = Mock(spec=logging.Logger)
        result = validate_metadata(42, logger)
        assert result is None
        logger.warning.assert_called_once()


class TestAIClassificationOrchestrator:
    """Tests for AIClassificationOrchestrator class."""

    def _create_mock_provider(self, response: Any) -> Mock:
        """Helper to create mock AIProvider."""
        provider = Mock()
        provider.provider_name = "test_provider"
        provider.model = "test_model"
        provider.classify_fields = Mock(return_value=response)
        return provider

    def _create_test_parser(self) -> Any:
        """Helper to create simple test parser function."""

        def parser(item_dict: dict[str, Any], index: int) -> TestItem:
            return TestItem(
                value=item_dict["value"],
                index=index,
                model_confidence=item_dict.get("model_confidence"),
            )

        return parser

    def test_orchestrator_classify_success(self):
        """Test successful classification with well-formed response."""
        response = {
            "test_items": [
                {"value": "item1", "model_confidence": 0.9},
                {"value": "item2", "model_confidence": 0.85},
            ]
        }
        provider = self._create_mock_provider(response)
        parser = self._create_test_parser()
        logger = Mock(spec=logging.Logger)

        orchestrator = AIClassificationOrchestrator(
            context="test_context",
            response_key="test_items",
            parser_func=parser,
            item_name="test item",
            logger=logger,
        )

        payload = {"data": "test"}
        result = orchestrator.classify(provider, payload)

        # Verify results
        assert len(result) == 2
        assert result[0].value == "item1"
        assert result[0].index == 0
        assert result[0].model_confidence == 0.9
        assert result[1].value == "item2"
        assert result[1].index == 1

        # Verify provider was called correctly
        provider.classify_fields.assert_called_once_with(payload, context="test_context")

        # Verify logging
        logger.debug.assert_called()
        logger.info.assert_called_once()
        logger.error.assert_not_called()

    def test_orchestrator_classify_empty_response(self):
        """Test classification with empty items list."""
        response = {"test_items": []}
        provider = self._create_mock_provider(response)
        parser = self._create_test_parser()
        logger = Mock(spec=logging.Logger)

        orchestrator = AIClassificationOrchestrator(
            context="test_context",
            response_key="test_items",
            parser_func=parser,
            item_name="test item",
            logger=logger,
        )

        result = orchestrator.classify(provider, {"data": "test"})

        assert result == []
        logger.info.assert_called_once()
        # Verify summary was logged (check args contain 0 for all counts)
        call_args = logger.info.call_args[0]
        assert 0 in call_args  # total_items=0
        assert "successfully_parsed" in call_args[0]  # format string

    def test_orchestrator_classify_partial_success(self):
        """Test classification with some invalid items (partial success)."""
        response = {
            "test_items": [
                {"value": "item1"},  # Valid
                {"wrong_key": "item2"},  # Invalid - missing 'value'
                {"value": "item3"},  # Valid
                {},  # Invalid - empty dict
            ]
        }
        provider = self._create_mock_provider(response)
        parser = self._create_test_parser()
        logger = Mock(spec=logging.Logger)

        orchestrator = AIClassificationOrchestrator(
            context="test_context",
            response_key="test_items",
            parser_func=parser,
            item_name="test item",
            logger=logger,
        )

        result = orchestrator.classify(provider, {"data": "test"})

        # Should successfully parse 2 items, skip 2 invalid ones
        assert len(result) == 2
        assert result[0].value == "item1"
        assert result[1].value == "item3"

        # Verify warnings were logged for failures
        assert logger.warning.call_count == 2
        # Check that warnings were logged (indices 1 and 3 should have failed)
        # The index is the second positional argument (args[2] after format string and item_name)
        warning_calls = logger.warning.call_args_list
        indices_logged = [call[0][2] for call in warning_calls]  # Third arg is idx
        assert 1 in indices_logged
        assert 3 in indices_logged

    def test_orchestrator_classify_provider_error(self):
        """Test classification when provider raises AIProviderError."""
        provider = Mock()
        provider.provider_name = "test_provider"
        provider.model = "test_model"
        provider.classify_fields = Mock(
            side_effect=AIProviderError(
                provider_name="test_provider",
                error_details="API error",
                request_type="classify_fields",
            )
        )

        parser = self._create_test_parser()
        logger = Mock(spec=logging.Logger)

        orchestrator = AIClassificationOrchestrator(
            context="test_context",
            response_key="test_items",
            parser_func=parser,
            item_name="test item",
            logger=logger,
        )

        with pytest.raises(AIProviderError) as exc_info:
            orchestrator.classify(provider, {"data": "test"})

        assert "test_provider" in str(exc_info.value)
        logger.error.assert_called_once()

    def test_orchestrator_classify_provider_unexpected_error(self):
        """Test classification when provider raises unexpected error."""
        provider = Mock()
        provider.provider_name = "test_provider"
        provider.model = "test_model"
        provider.classify_fields = Mock(side_effect=ValueError("Unexpected error"))

        parser = self._create_test_parser()
        logger = Mock(spec=logging.Logger)

        orchestrator = AIClassificationOrchestrator(
            context="test_context",
            response_key="test_items",
            parser_func=parser,
            item_name="test item",
            logger=logger,
        )

        with pytest.raises(AIProviderError) as exc_info:
            orchestrator.classify(provider, {"data": "test"})

        # Should wrap unexpected error in AIProviderError
        assert "Unexpected error" in str(exc_info.value)
        logger.error.assert_called_once()

    def test_orchestrator_classify_invalid_response_not_dict(self):
        """Test classification when response is not a dict."""
        provider = self._create_mock_provider("not a dict")
        parser = self._create_test_parser()
        logger = Mock(spec=logging.Logger)

        orchestrator = AIClassificationOrchestrator(
            context="test_context",
            response_key="test_items",
            parser_func=parser,
            item_name="test item",
            logger=logger,
        )

        with pytest.raises(AIProviderError) as exc_info:
            orchestrator.classify(provider, {"data": "test"})

        assert "Expected dict response" in str(exc_info.value)
        logger.error.assert_called()

    def test_orchestrator_classify_missing_response_key(self):
        """Test classification when response missing required key."""
        response = {"wrong_key": []}
        provider = self._create_mock_provider(response)
        parser = self._create_test_parser()
        logger = Mock(spec=logging.Logger)

        orchestrator = AIClassificationOrchestrator(
            context="test_context",
            response_key="test_items",
            parser_func=parser,
            item_name="test item",
            logger=logger,
        )

        with pytest.raises(AIProviderError) as exc_info:
            orchestrator.classify(provider, {"data": "test"})

        assert "missing required 'test_items' key" in str(exc_info.value)
        logger.error.assert_called()

    def test_orchestrator_classify_invalid_response_value_not_list(self):
        """Test classification when response key value is not a list."""
        response = {"test_items": "not a list"}
        provider = self._create_mock_provider(response)
        parser = self._create_test_parser()
        logger = Mock(spec=logging.Logger)

        orchestrator = AIClassificationOrchestrator(
            context="test_context",
            response_key="test_items",
            parser_func=parser,
            item_name="test item",
            logger=logger,
        )

        with pytest.raises(AIProviderError) as exc_info:
            orchestrator.classify(provider, {"data": "test"})

        assert "'test_items' must be a list" in str(exc_info.value)
        logger.error.assert_called()

    def test_orchestrator_classify_with_confidence_logging(self):
        """Test that average confidence is logged when present."""
        response = {
            "test_items": [
                {"value": "item1", "model_confidence": 0.9},
                {"value": "item2", "model_confidence": 0.8},
                {"value": "item3"},  # No confidence
            ]
        }
        provider = self._create_mock_provider(response)
        parser = self._create_test_parser()
        logger = Mock(spec=logging.Logger)

        orchestrator = AIClassificationOrchestrator(
            context="test_context",
            response_key="test_items",
            parser_func=parser,
            item_name="test item",
            logger=logger,
        )

        result = orchestrator.classify(provider, {"data": "test"})

        assert len(result) == 3
        # Check that debug log for average confidence was called
        debug_calls = [str(call) for call in logger.debug.call_args_list]
        confidence_log = [call for call in debug_calls if "Average model confidence" in call]
        assert len(confidence_log) == 1

    def test_orchestrator_classify_no_confidence_no_logging(self):
        """Test that no confidence logging when no items have confidence."""
        response = {
            "test_items": [
                {"value": "item1"},
                {"value": "item2"},
            ]
        }
        provider = self._create_mock_provider(response)
        parser = self._create_test_parser()
        logger = Mock(spec=logging.Logger)

        orchestrator = AIClassificationOrchestrator(
            context="test_context",
            response_key="test_items",
            parser_func=parser,
            item_name="test item",
            logger=logger,
        )

        result = orchestrator.classify(provider, {"data": "test"})

        assert len(result) == 2
        # Check that debug log for confidence was NOT called
        debug_calls = [str(call) for call in logger.debug.call_args_list]
        confidence_log = [call for call in debug_calls if "Average model confidence" in call]
        assert len(confidence_log) == 0
