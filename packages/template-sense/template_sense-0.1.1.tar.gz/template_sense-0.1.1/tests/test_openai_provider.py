"""
Tests for OpenAI provider implementation.

This module tests the OpenAIProvider class, including:
- Successful API calls (classification and translation)
- Error handling (authentication, timeout, API errors)
- JSON parsing and response validation
- Configuration handling
"""

import json
from unittest.mock import Mock, patch

import pytest

from template_sense.ai_providers.config import AIConfig
from template_sense.ai_providers.openai_provider import OpenAIProvider
from template_sense.errors import AIProviderError


class TestOpenAIProviderInitialization:
    """Test OpenAIProvider initialization and configuration."""

    def test_init_with_valid_config(self):
        """Test successful initialization with valid config."""
        config = AIConfig(provider="openai", api_key="sk-test-key")

        with patch("template_sense.ai_providers.openai_provider.OpenAI"):
            provider = OpenAIProvider(config)

            assert provider.provider_name == "openai"
            assert provider.config == config

    def test_init_without_api_key_raises_error(self):
        """Test initialization without API key raises AIProviderError."""
        config = AIConfig(provider="openai", api_key="")

        with pytest.raises(AIProviderError) as exc_info:
            OpenAIProvider(config)

        error = exc_info.value
        assert error.provider_name == "openai"
        assert "API key is required" in error.error_details
        assert error.request_type == "initialization"

    def test_init_client_failure_raises_error(self):
        """Test client initialization failure raises AIProviderError."""
        config = AIConfig(provider="openai", api_key="sk-test-key")

        with patch(
            "template_sense.ai_providers.openai_provider.OpenAI",
            side_effect=Exception("Client init failed"),
        ):
            with pytest.raises(AIProviderError) as exc_info:
                OpenAIProvider(config)

            error = exc_info.value
            assert error.provider_name == "openai"
            assert "Failed to initialize client" in error.error_details

    def test_model_property_uses_config_model(self):
        """Test model property returns configured model."""
        config = AIConfig(provider="openai", api_key="sk-test-key", model="gpt-3.5-turbo")

        with patch("template_sense.ai_providers.openai_provider.OpenAI"):
            provider = OpenAIProvider(config)
            assert provider.model == "gpt-3.5-turbo"

    def test_model_property_defaults_to_gpt4(self):
        """Test model property defaults to gpt-4 when not configured."""
        config = AIConfig(provider="openai", api_key="sk-test-key")

        with patch("template_sense.ai_providers.openai_provider.OpenAI"):
            provider = OpenAIProvider(config)
            assert provider.model == "gpt-4"


class TestOpenAIProviderClassifyFields:
    """Test OpenAIProvider classify_fields method."""

    @pytest.fixture
    def provider(self):
        """Create OpenAIProvider instance with mocked client."""
        config = AIConfig(provider="openai", api_key="sk-test-key")
        with patch("template_sense.ai_providers.openai_provider.OpenAI"):
            return OpenAIProvider(config)

    @pytest.fixture
    def sample_payload(self):
        """Sample AI payload for testing."""
        return {
            "sheet_name": "Sheet1",
            "header_candidates": [
                {"row": 1, "col": 1, "label": "Invoice", "value": "12345", "score": 0.9}
            ],
            "table_candidates": [],
            "field_dictionary": {"invoice_number": ["Invoice", "Invoice No"]},
        }

    def test_classify_fields_success(self, provider, sample_payload):
        """Test successful field classification."""
        # Mock successful API response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps(
            {
                "headers": [
                    {
                        "raw_label": "Invoice",
                        "raw_value": "12345",
                        "row_index": 1,
                        "col_index": 1,
                        "block_index": 0,
                    }
                ]
            }
        )

        provider.client.chat.completions.create = Mock(return_value=mock_response)

        result = provider.classify_fields(sample_payload)

        assert "headers" in result
        assert result["headers"][0]["raw_label"] == "Invoice"
        provider.client.chat.completions.create.assert_called_once()

    def test_classify_fields_with_headers_context(self, provider, sample_payload):
        """Test field classification with explicit headers context."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps(
            {
                "headers": [
                    {
                        "raw_label": "Invoice",
                        "raw_value": "12345",
                        "row_index": 1,
                        "col_index": 1,
                        "block_index": 0,
                    }
                ]
            }
        )

        provider.client.chat.completions.create = Mock(return_value=mock_response)

        result = provider.classify_fields(sample_payload, context="headers")

        assert "headers" in result
        provider.client.chat.completions.create.assert_called_once()

    def test_classify_fields_with_columns_context(self, provider, sample_payload):
        """Test field classification with columns context."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps(
            {
                "columns": [
                    {
                        "raw_label": "Item",
                        "raw_position": 0,
                        "table_block_index": 0,
                        "row_index": 5,
                        "col_index": 1,
                        "sample_values": ["A", "B"],
                    }
                ]
            }
        )

        provider.client.chat.completions.create = Mock(return_value=mock_response)

        result = provider.classify_fields(sample_payload, context="columns")

        assert "columns" in result
        assert result["columns"][0]["raw_label"] == "Item"
        provider.client.chat.completions.create.assert_called_once()

    def test_classify_fields_with_line_items_context(self, provider, sample_payload):
        """Test field classification with line_items context."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps(
            {
                "line_items": [
                    {
                        "table_index": 0,
                        "row_index": 6,
                        "columns": {"item": "Product A"},
                        "is_subtotal": False,
                    }
                ]
            }
        )

        provider.client.chat.completions.create = Mock(return_value=mock_response)

        result = provider.classify_fields(sample_payload, context="line_items")

        assert "line_items" in result
        provider.client.chat.completions.create.assert_called_once()

    def test_classify_fields_invalid_context(self, provider, sample_payload):
        """Test field classification with invalid context raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            provider.classify_fields(sample_payload, context="invalid_context")

        assert "Invalid context" in str(exc_info.value)

    def test_classify_fields_missing_expected_key(self, provider, sample_payload):
        """Test classification with response missing expected key for context."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        # Response has "columns" key but we're using headers context
        mock_response.choices[0].message.content = json.dumps({"columns": [{"raw_label": "Item"}]})

        provider.client.chat.completions.create = Mock(return_value=mock_response)

        with pytest.raises(AIProviderError) as exc_info:
            provider.classify_fields(sample_payload, context="headers")

        error = exc_info.value
        assert "Response missing 'headers' key" in error.error_details

    def test_classify_fields_authentication_error(self, provider, sample_payload):
        """Test classification with authentication error."""
        from openai import AuthenticationError

        # Create a mock response and body for the error
        mock_response = Mock()
        mock_response.status_code = 401

        provider.client.chat.completions.create = Mock(
            side_effect=AuthenticationError("Invalid API key", response=mock_response, body={})
        )

        with pytest.raises(AIProviderError) as exc_info:
            provider.classify_fields(sample_payload)

        error = exc_info.value
        assert error.provider_name == "openai"
        assert "Authentication failed" in error.error_details
        assert error.request_type == "classify_fields"

    def test_classify_fields_timeout_error(self, provider, sample_payload):
        """Test classification with timeout error."""
        from openai import APITimeoutError

        provider.client.chat.completions.create = Mock(
            side_effect=APITimeoutError("Request timed out")
        )

        with pytest.raises(AIProviderError) as exc_info:
            provider.classify_fields(sample_payload)

        error = exc_info.value
        assert error.provider_name == "openai"
        assert "Request timed out" in error.error_details
        assert error.request_type == "classify_fields"

    def test_classify_fields_api_error(self, provider, sample_payload):
        """Test classification with API error."""
        from openai import APIError

        # Create a mock request for the error
        mock_request = Mock()

        provider.client.chat.completions.create = Mock(
            side_effect=APIError("Rate limit exceeded", request=mock_request, body={})
        )

        with pytest.raises(AIProviderError) as exc_info:
            provider.classify_fields(sample_payload)

        error = exc_info.value
        assert error.provider_name == "openai"
        assert "API error" in error.error_details

    def test_classify_fields_empty_response(self, provider, sample_payload):
        """Test classification with empty response."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = None

        provider.client.chat.completions.create = Mock(return_value=mock_response)

        with pytest.raises(AIProviderError) as exc_info:
            provider.classify_fields(sample_payload)

        error = exc_info.value
        assert "Empty response" in error.error_details

    def test_classify_fields_invalid_json(self, provider, sample_payload):
        """Test classification with invalid JSON response."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Not valid JSON"

        provider.client.chat.completions.create = Mock(return_value=mock_response)

        with pytest.raises(AIProviderError) as exc_info:
            provider.classify_fields(sample_payload)

        error = exc_info.value
        assert "Invalid JSON" in error.error_details

    def test_classify_fields_unexpected_error(self, provider, sample_payload):
        """Test classification with unexpected error."""
        provider.client.chat.completions.create = Mock(side_effect=RuntimeError("Unexpected error"))

        with pytest.raises(AIProviderError) as exc_info:
            provider.classify_fields(sample_payload)

        error = exc_info.value
        assert "Unexpected error" in error.error_details


class TestOpenAIProviderTranslateText:
    """Test OpenAIProvider translate_text method."""

    @pytest.fixture
    def provider(self):
        """Create OpenAIProvider instance with mocked client."""
        config = AIConfig(provider="openai", api_key="sk-test-key")
        with patch("template_sense.ai_providers.openai_provider.OpenAI"):
            return OpenAIProvider(config)

    def test_translate_text_success(self, provider):
        """Test successful text translation."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Invoice Number"

        provider.client.chat.completions.create = Mock(return_value=mock_response)

        result = provider.translate_text("請求書番号", source_lang="ja", target_lang="en")

        assert result == "Invoice Number"
        provider.client.chat.completions.create.assert_called_once()

    def test_translate_text_authentication_error(self, provider):
        """Test translation with authentication error."""
        from openai import AuthenticationError

        # Create a mock response and body for the error
        mock_response = Mock()
        mock_response.status_code = 401

        provider.client.chat.completions.create = Mock(
            side_effect=AuthenticationError("Invalid API key", response=mock_response, body={})
        )

        with pytest.raises(AIProviderError) as exc_info:
            provider.translate_text("test", source_lang="ja")

        error = exc_info.value
        assert error.provider_name == "openai"
        assert "Authentication failed" in error.error_details
        assert error.request_type == "translate_text"

    def test_translate_text_timeout_error(self, provider):
        """Test translation with timeout error."""
        from openai import APITimeoutError

        provider.client.chat.completions.create = Mock(
            side_effect=APITimeoutError("Request timed out")
        )

        with pytest.raises(AIProviderError) as exc_info:
            provider.translate_text("test", source_lang="ja")

        error = exc_info.value
        assert "Request timed out" in error.error_details

    def test_translate_text_api_error(self, provider):
        """Test translation with API error."""
        from openai import APIError

        # Create a mock request for the error
        mock_request = Mock()

        provider.client.chat.completions.create = Mock(
            side_effect=APIError("Service unavailable", request=mock_request, body={})
        )

        with pytest.raises(AIProviderError) as exc_info:
            provider.translate_text("test", source_lang="ja")

        error = exc_info.value
        assert "API error" in error.error_details

    def test_translate_text_empty_response(self, provider):
        """Test translation with empty response."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = None

        provider.client.chat.completions.create = Mock(return_value=mock_response)

        with pytest.raises(AIProviderError) as exc_info:
            provider.translate_text("test", source_lang="ja")

        error = exc_info.value
        assert "Empty translation response" in error.error_details

    def test_translate_text_strips_whitespace(self, provider):
        """Test translation strips leading/trailing whitespace."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "  Invoice Number  \n"

        provider.client.chat.completions.create = Mock(return_value=mock_response)

        result = provider.translate_text("請求書番号", source_lang="ja")

        assert result == "Invoice Number"  # Whitespace stripped

    def test_translate_text_unexpected_error(self, provider):
        """Test translation with unexpected error."""
        provider.client.chat.completions.create = Mock(side_effect=RuntimeError("Unexpected error"))

        with pytest.raises(AIProviderError) as exc_info:
            provider.translate_text("test", source_lang="ja")

        error = exc_info.value
        assert "Unexpected error" in error.error_details
