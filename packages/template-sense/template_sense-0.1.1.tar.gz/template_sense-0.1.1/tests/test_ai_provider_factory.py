"""Tests for AI provider factory function."""

import pytest

from template_sense.ai_providers.config import AIConfig
from template_sense.ai_providers.factory import get_ai_provider
from template_sense.constants import (
    AI_PROVIDER_ENV_VAR,
    ANTHROPIC_API_KEY_ENV_VAR,
    OPENAI_API_KEY_ENV_VAR,
)
from template_sense.errors import AIProviderError


class TestGetAIProvider:
    """Tests for the get_ai_provider factory function."""

    def test_factory_with_explicit_openai_config(self):
        """Test factory with explicit OpenAI config."""
        from unittest.mock import patch

        config = AIConfig(provider="openai", api_key="sk-test-key", model="gpt-4")

        # Task 28 implemented providers, so factory should return OpenAIProvider
        with patch("template_sense.ai_providers.openai_provider.OpenAI"):
            provider = get_ai_provider(config)
            assert provider.provider_name == "openai"
            assert provider.config == config

    def test_factory_with_explicit_anthropic_config(self):
        """Test factory with explicit Anthropic config."""
        from unittest.mock import patch

        config = AIConfig(
            provider="anthropic",
            api_key="sk-ant-test-key",
            model="claude-3-sonnet-20240229",
        )

        # Task 28 implemented providers, so factory should return AnthropicProvider
        with patch("template_sense.ai_providers.anthropic_provider.Anthropic"):
            provider = get_ai_provider(config)
            assert provider.provider_name == "anthropic"
            assert provider.config == config

    def test_factory_loads_from_env_when_config_is_none(self, monkeypatch):
        """Test that factory loads config from env when config is None."""
        from unittest.mock import patch

        monkeypatch.setenv(AI_PROVIDER_ENV_VAR, "openai")
        monkeypatch.setenv(OPENAI_API_KEY_ENV_VAR, "sk-env-key")

        # Should load from env and successfully return provider
        with patch("template_sense.ai_providers.openai_provider.OpenAI"):
            provider = get_ai_provider(config=None)
            assert provider.provider_name == "openai"

    def test_factory_propagates_config_loading_errors(self, monkeypatch):
        """Test that factory propagates errors from load_ai_config."""
        # Don't set any environment variables
        monkeypatch.delenv(AI_PROVIDER_ENV_VAR, raising=False)
        monkeypatch.delenv(OPENAI_API_KEY_ENV_VAR, raising=False)
        monkeypatch.delenv(ANTHROPIC_API_KEY_ENV_VAR, raising=False)

        with pytest.raises(AIProviderError) as exc_info:
            get_ai_provider(config=None)

        error = exc_info.value
        assert "Missing required environment variable" in error.error_details

    def test_factory_with_unsupported_provider_config(self):
        """Test factory with unsupported provider in config."""
        # This should fail at AIConfig validation level
        with pytest.raises(AIProviderError) as exc_info:
            config = AIConfig(provider="gemini", api_key="sk-test")
            get_ai_provider(config)

        error = exc_info.value
        assert error.provider_name == "gemini"
        assert "Unsupported provider" in error.error_details

    def test_factory_error_message_is_clear(self):
        """Test that factory error message clearly indicates initialization errors."""
        from unittest.mock import patch

        config = AIConfig(provider="openai", api_key="sk-test")

        # Test that initialization errors are properly propagated
        with patch(
            "template_sense.ai_providers.openai_provider.OpenAI",
            side_effect=Exception("Client init failed"),
        ):
            with pytest.raises(AIProviderError) as exc_info:
                get_ai_provider(config)

            error = exc_info.value
            assert error.provider_name == "openai"
            assert "Failed to initialize client" in error.error_details

    def test_factory_preserves_config_settings(self, monkeypatch):
        """Test that factory preserves all config settings when loading from env."""
        from unittest.mock import patch

        monkeypatch.setenv(AI_PROVIDER_ENV_VAR, "anthropic")
        monkeypatch.setenv(ANTHROPIC_API_KEY_ENV_VAR, "sk-ant-key-xyz")

        # Factory should successfully create provider with env config
        with patch("template_sense.ai_providers.anthropic_provider.Anthropic"):
            provider = get_ai_provider()
            assert provider.provider_name == "anthropic"

    def test_factory_with_none_model_in_config(self):
        """Test factory with config that has model=None."""
        from unittest.mock import patch

        config = AIConfig(provider="openai", api_key="sk-test", model=None)

        # Should successfully create provider (provider will use default model)
        with patch("template_sense.ai_providers.openai_provider.OpenAI"):
            provider = get_ai_provider(config)
            assert provider.provider_name == "openai"
            assert provider.model == "gpt-4"  # Default model

    def test_factory_default_parameter_is_none(self):
        """Test that calling factory without args defaults to config=None."""
        import os
        from unittest.mock import patch

        # Setup valid env vars
        os.environ[AI_PROVIDER_ENV_VAR] = "openai"
        os.environ[OPENAI_API_KEY_ENV_VAR] = "sk-test"

        try:
            # Both should behave the same - successfully create provider
            with patch("template_sense.ai_providers.openai_provider.OpenAI"):
                provider1 = get_ai_provider()  # No args
                assert provider1.provider_name == "openai"

                provider2 = get_ai_provider(None)  # Explicit None
                assert provider2.provider_name == "openai"

        finally:
            # Cleanup
            os.environ.pop(AI_PROVIDER_ENV_VAR, None)
            os.environ.pop(OPENAI_API_KEY_ENV_VAR, None)
