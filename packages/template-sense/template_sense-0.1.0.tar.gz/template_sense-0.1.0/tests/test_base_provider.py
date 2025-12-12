"""
Tests for BaseAIProvider shared functionality.

This module tests the common logic in BaseAIProvider using a mock
provider implementation. It verifies:
- Prompt building
- Context validation
- Response parsing and validation
- Error handling and exception mapping
"""

import json
from unittest.mock import Mock

import pytest

from template_sense.ai_providers.base_provider import BaseAIProvider
from template_sense.ai_providers.config import AIConfig
from template_sense.errors import AIProviderError


class MockProvider(BaseAIProvider):
    """Test implementation of BaseAIProvider for testing shared logic."""

    def __init__(self, config: AIConfig):
        super().__init__(config)
        self.classify_response = '{"headers": []}'
        self.translate_response = "translated text"
        self.generate_response = "generated text"

    @property
    def provider_name(self) -> str:
        return "mock"

    @property
    def model(self) -> str:
        return "mock-model"

    def _call_classify_api(self, system_message: str, user_message: str) -> str:
        return self.classify_response

    def _call_translate_api(self, system_message: str, user_message: str) -> str:
        return self.translate_response

    def _call_generate_api(
        self,
        prompt: str,
        system_message: str | None,
        max_tokens: int,
        temperature: float,
        json_mode: bool,
    ) -> str:
        return self.generate_response


@pytest.fixture
def mock_provider():
    """Create a mock provider for testing."""
    # Create config without validation (for testing purposes only)
    from dataclasses import dataclass

    @dataclass
    class TestConfig:
        provider: str = "mock"
        api_key: str = "test-key"
        model: str | None = None
        timeout_seconds: int | None = None

    config = TestConfig()
    return MockProvider(config)


class TestContextValidation:
    """Tests for context validation."""

    def test_validate_context_valid_headers(self, mock_provider):
        """Test that 'headers' context is valid."""
        mock_provider._validate_context("headers")  # Should not raise

    def test_validate_context_valid_columns(self, mock_provider):
        """Test that 'columns' context is valid."""
        mock_provider._validate_context("columns")  # Should not raise

    def test_validate_context_valid_line_items(self, mock_provider):
        """Test that 'line_items' context is valid."""
        mock_provider._validate_context("line_items")  # Should not raise

    def test_validate_context_invalid(self, mock_provider):
        """Test that invalid context raises ValueError."""
        with pytest.raises(ValueError, match="Invalid context: invalid"):
            mock_provider._validate_context("invalid")


class TestPromptBuilding:
    """Tests for prompt building methods."""

    def test_build_system_prompt_headers(self, mock_provider):
        """Test system prompt for headers context."""
        prompt = mock_provider._build_system_prompt("headers")
        assert "field classification assistant for invoice templates" in prompt
        assert "headers" in prompt
        assert "PATTERN DETECTION" in prompt
        assert "raw_label" in prompt
        assert "raw_value" in prompt

    def test_build_system_prompt_columns(self, mock_provider):
        """Test system prompt for columns context."""
        prompt = mock_provider._build_system_prompt("columns")
        assert "table column classification assistant" in prompt
        assert "columns" in prompt
        assert "raw_position" in prompt
        assert "sample_values" in prompt

    def test_build_system_prompt_line_items(self, mock_provider):
        """Test system prompt for line_items context."""
        prompt = mock_provider._build_system_prompt("line_items")
        assert "line item extraction assistant" in prompt
        assert "line_items" in prompt
        assert "table_index" in prompt
        assert "is_subtotal" in prompt

    def test_build_user_prompt_headers(self, mock_provider):
        """Test user prompt for headers context."""
        payload = {"header_fields": [{"label": "Invoice No"}]}
        prompt = mock_provider._build_user_prompt(payload, "headers")
        assert "invoice template header fields" in prompt
        assert json.dumps(payload, indent=2) in prompt
        assert "JSON object" in prompt

    def test_build_user_prompt_columns(self, mock_provider):
        """Test user prompt for columns context."""
        payload = {"table_columns": [{"label": "Item"}]}
        prompt = mock_provider._build_user_prompt(payload, "columns")
        assert "invoice table columns" in prompt
        assert json.dumps(payload, indent=2) in prompt

    def test_build_user_prompt_line_items(self, mock_provider):
        """Test user prompt for line_items context."""
        payload = {"line_items": [{"row": 1}]}
        prompt = mock_provider._build_user_prompt(payload, "line_items")
        assert "invoice table line items" in prompt
        assert json.dumps(payload, indent=2) in prompt


class TestExpectedResponseKey:
    """Tests for expected response key mapping."""

    def test_get_expected_response_key_headers(self, mock_provider):
        """Test expected key for headers context."""
        key = mock_provider._get_expected_response_key("headers")
        assert key == "headers"

    def test_get_expected_response_key_columns(self, mock_provider):
        """Test expected key for columns context."""
        key = mock_provider._get_expected_response_key("columns")
        assert key == "columns"

    def test_get_expected_response_key_line_items(self, mock_provider):
        """Test expected key for line_items context."""
        key = mock_provider._get_expected_response_key("line_items")
        assert key == "line_items"


class TestResponseParsing:
    """Tests for response parsing and validation."""

    def test_parse_and_validate_response_valid(self, mock_provider):
        """Test parsing valid JSON response."""
        content = '{"headers": [{"raw_label": "Invoice"}]}'
        result = mock_provider._parse_and_validate_response(content, "headers", "classify_fields")
        assert result == {"headers": [{"raw_label": "Invoice"}]}

    def test_parse_and_validate_response_empty(self, mock_provider):
        """Test parsing empty response raises error."""
        with pytest.raises(AIProviderError, match="Empty response from API"):
            mock_provider._parse_and_validate_response("", "headers", "classify_fields")

    def test_parse_and_validate_response_invalid_json(self, mock_provider):
        """Test parsing invalid JSON raises error."""
        with pytest.raises(AIProviderError, match="Invalid JSON in response"):
            mock_provider._parse_and_validate_response("{invalid", "headers", "classify_fields")

    def test_parse_and_validate_response_missing_key(self, mock_provider):
        """Test parsing response with missing expected key raises error."""
        content = '{"wrong_key": []}'
        with pytest.raises(AIProviderError, match="Response missing 'headers' key"):
            mock_provider._parse_and_validate_response(content, "headers", "classify_fields")


class TestClassifyFields:
    """Tests for classify_fields method."""

    def test_classify_fields_success_headers(self, mock_provider):
        """Test successful classification for headers context."""
        mock_provider.classify_response = '{"headers": [{"raw_label": "Invoice"}]}'
        payload = {"header_fields": []}
        result = mock_provider.classify_fields(payload, "headers")
        assert "headers" in result
        assert result["headers"][0]["raw_label"] == "Invoice"

    def test_classify_fields_success_columns(self, mock_provider):
        """Test successful classification for columns context."""
        mock_provider.classify_response = '{"columns": [{"raw_label": "Item"}]}'
        payload = {"table_columns": []}
        result = mock_provider.classify_fields(payload, "columns")
        assert "columns" in result
        assert result["columns"][0]["raw_label"] == "Item"

    def test_classify_fields_invalid_context(self, mock_provider):
        """Test classification with invalid context raises ValueError."""
        with pytest.raises(ValueError, match="Invalid context"):
            mock_provider.classify_fields({}, "invalid")

    def test_classify_fields_empty_response(self, mock_provider):
        """Test classification with empty response raises error."""
        mock_provider.classify_response = ""
        with pytest.raises(AIProviderError, match="Empty response"):
            mock_provider.classify_fields({}, "headers")

    def test_classify_fields_api_error(self, mock_provider):
        """Test classification with API error is wrapped."""

        def raise_error(system, user):
            raise Exception("API failure")

        mock_provider._call_classify_api = raise_error
        with pytest.raises(AIProviderError, match="Unexpected error"):
            mock_provider.classify_fields({}, "headers")


class TestTranslateText:
    """Tests for translate_text method."""

    def test_translate_text_success(self, mock_provider):
        """Test successful translation."""
        mock_provider.translate_response = "Invoice Number"
        result = mock_provider.translate_text("請求書番号", "ja", "en")
        assert result == "Invoice Number"

    def test_translate_text_empty_response(self, mock_provider):
        """Test translation with empty response raises error."""
        mock_provider.translate_response = ""
        with pytest.raises(AIProviderError, match="Empty translation response"):
            mock_provider.translate_text("text", "ja", "en")

    def test_translate_text_strips_whitespace(self, mock_provider):
        """Test translation strips whitespace from response."""
        mock_provider.translate_response = "  Invoice Number  "
        result = mock_provider.translate_text("請求書番号", "ja", "en")
        assert result == "Invoice Number"

    def test_translate_text_api_error(self, mock_provider):
        """Test translation with API error is wrapped."""

        def raise_error(system, user):
            raise Exception("API failure")

        mock_provider._call_translate_api = raise_error
        with pytest.raises(AIProviderError, match="Unexpected error"):
            mock_provider.translate_text("text", "ja", "en")


class TestErrorWrapping:
    """Tests for error wrapping and exception mapping."""

    def test_wrap_api_error_openai_auth(self, mock_provider):
        """Test wrapping OpenAI AuthenticationError."""
        try:
            from openai import AuthenticationError

            error = AuthenticationError("Invalid API key", response=Mock(), body=None)
            wrapped = mock_provider._wrap_api_error(error, "classify_fields")
            assert isinstance(wrapped, AIProviderError)
            assert "Authentication failed" in wrapped.error_details
            assert wrapped.provider_name == "mock"
            assert wrapped.request_type == "classify_fields"
        except ImportError:
            pytest.skip("OpenAI SDK not installed")

    def test_wrap_api_error_openai_timeout(self, mock_provider):
        """Test wrapping OpenAI APITimeoutError."""
        try:
            from openai import APITimeoutError

            error = APITimeoutError(request=Mock())
            wrapped = mock_provider._wrap_api_error(error, "classify_fields")
            assert isinstance(wrapped, AIProviderError)
            assert "Request timed out" in wrapped.error_details
        except ImportError:
            pytest.skip("OpenAI SDK not installed")

    def test_wrap_api_error_openai_api_error(self, mock_provider):
        """Test wrapping OpenAI APIError."""
        try:
            from openai import APIError

            error = APIError("API error", request=Mock(), body=None)
            wrapped = mock_provider._wrap_api_error(error, "classify_fields")
            assert isinstance(wrapped, AIProviderError)
            assert "API error" in wrapped.error_details
        except ImportError:
            pytest.skip("OpenAI SDK not installed")

    def test_wrap_api_error_anthropic_auth(self, mock_provider):
        """Test wrapping Anthropic AuthenticationError."""
        try:
            from anthropic import AuthenticationError

            error = AuthenticationError("Invalid API key", response=Mock(), body=None)
            wrapped = mock_provider._wrap_api_error(error, "translate_text")
            assert isinstance(wrapped, AIProviderError)
            assert "Authentication failed" in wrapped.error_details
            assert wrapped.request_type == "translate_text"
        except ImportError:
            pytest.skip("Anthropic SDK not installed")

    def test_wrap_api_error_anthropic_timeout(self, mock_provider):
        """Test wrapping Anthropic APITimeoutError."""
        try:
            from anthropic import APITimeoutError

            error = APITimeoutError(request=Mock())
            wrapped = mock_provider._wrap_api_error(error, "translate_text")
            assert isinstance(wrapped, AIProviderError)
            assert "Request timed out" in wrapped.error_details
        except ImportError:
            pytest.skip("Anthropic SDK not installed")

    def test_wrap_api_error_anthropic_api_error(self, mock_provider):
        """Test wrapping Anthropic APIError."""
        try:
            from anthropic import APIError

            error = APIError("API error", request=Mock(), body=None)
            wrapped = mock_provider._wrap_api_error(error, "translate_text")
            assert isinstance(wrapped, AIProviderError)
            assert "API error" in wrapped.error_details
        except ImportError:
            pytest.skip("Anthropic SDK not installed")

    def test_wrap_api_error_unexpected(self, mock_provider):
        """Test wrapping unexpected exception."""
        error = ValueError("Unexpected error")
        wrapped = mock_provider._wrap_api_error(error, "classify_fields")
        assert isinstance(wrapped, AIProviderError)
        assert "Unexpected error" in wrapped.error_details
        assert wrapped.provider_name == "mock"


class TestInheritance:
    """Tests for BaseAIProvider inheritance."""

    def test_mock_provider_is_base_provider(self, mock_provider):
        """Test that MockProvider is an instance of BaseAIProvider."""
        assert isinstance(mock_provider, BaseAIProvider)

    def test_provider_name_property(self, mock_provider):
        """Test provider_name property."""
        assert mock_provider.provider_name == "mock"

    def test_model_property(self, mock_provider):
        """Test model property."""
        assert mock_provider.model == "mock-model"


class TestGenerateText:
    """Tests for generate_text template method."""

    def test_generate_text_success(self, mock_provider):
        """Test successful text generation."""
        mock_provider.generate_response = "Generated response text"

        result = mock_provider.generate_text(
            prompt="Test prompt",
            system_message="Test system message",
            max_tokens=150,
            temperature=0.0,
            json_mode=True,
        )

        assert result == "Generated response text"

    def test_generate_text_with_defaults(self, mock_provider):
        """Test text generation with default parameters."""
        mock_provider.generate_response = "Default response"

        result = mock_provider.generate_text(prompt="Test prompt")

        assert result == "Default response"

    def test_generate_text_empty_prompt(self, mock_provider):
        """Test that empty prompt raises ValueError."""
        with pytest.raises(ValueError, match="Prompt cannot be empty"):
            mock_provider.generate_text(prompt="")

    def test_generate_text_whitespace_prompt(self, mock_provider):
        """Test that whitespace-only prompt raises ValueError."""
        with pytest.raises(ValueError, match="Prompt cannot be empty"):
            mock_provider.generate_text(prompt="   ")

    def test_generate_text_empty_response(self, mock_provider):
        """Test that empty response raises AIProviderError."""
        mock_provider.generate_response = ""

        with pytest.raises(AIProviderError, match="Empty response from API"):
            mock_provider.generate_text(prompt="Test prompt")

    def test_generate_text_api_error(self, mock_provider):
        """Test that API errors are wrapped in AIProviderError."""

        # Override _call_generate_api to raise an exception
        def raise_error(*args, **kwargs):
            raise Exception("API error occurred")

        mock_provider._call_generate_api = raise_error

        with pytest.raises(AIProviderError, match="Unexpected error"):
            mock_provider.generate_text(prompt="Test prompt")
