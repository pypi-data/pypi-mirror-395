"""Tests for AI provider configuration management."""

import pytest

from template_sense.ai_providers.config import AIConfig, load_ai_config
from template_sense.constants import (
    AI_MODEL_ENV_VAR,
    AI_PROVIDER_ENV_VAR,
    ANTHROPIC_API_KEY_ENV_VAR,
    DEFAULT_AI_TIMEOUT_SECONDS,
    OPENAI_API_KEY_ENV_VAR,
)
from template_sense.errors import AIProviderError


class TestAIConfig:
    """Tests for the AIConfig dataclass."""

    def test_config_with_valid_openai_provider(self):
        """Test creating config with valid OpenAI provider."""
        config = AIConfig(
            provider="openai",
            api_key="sk-test-key-123",
            model="gpt-4",
            timeout_seconds=30,
        )

        assert config.provider == "openai"
        assert config.api_key == "sk-test-key-123"
        assert config.model == "gpt-4"
        assert config.timeout_seconds == 30

    def test_config_with_valid_anthropic_provider(self):
        """Test creating config with valid Anthropic provider."""
        config = AIConfig(
            provider="anthropic",
            api_key="sk-ant-test-key-456",
            model="claude-3-sonnet-20240229",
        )

        assert config.provider == "anthropic"
        assert config.api_key == "sk-ant-test-key-456"
        assert config.model == "claude-3-sonnet-20240229"
        assert config.timeout_seconds == DEFAULT_AI_TIMEOUT_SECONDS  # Default

    def test_config_with_none_model(self):
        """Test creating config with None model (valid)."""
        config = AIConfig(provider="openai", api_key="sk-test", model=None)

        assert config.provider == "openai"
        assert config.model is None

    def test_config_uses_default_timeout(self):
        """Test that config uses default timeout from constants."""
        config = AIConfig(provider="openai", api_key="sk-test")

        assert config.timeout_seconds == DEFAULT_AI_TIMEOUT_SECONDS

    def test_config_rejects_unsupported_provider(self):
        """Test that AIConfig raises error for unsupported provider."""
        with pytest.raises(AIProviderError) as exc_info:
            AIConfig(provider="unsupported", api_key="sk-test")

        error = exc_info.value
        assert error.provider_name == "unsupported"
        assert "Unsupported provider" in error.error_details
        assert "openai" in error.error_details
        assert "anthropic" in error.error_details

    def test_config_rejects_empty_provider(self):
        """Test that AIConfig raises error for empty provider."""
        with pytest.raises(AIProviderError) as exc_info:
            AIConfig(provider="", api_key="sk-test")

        error = exc_info.value
        assert error.provider_name == ""
        assert "Unsupported provider" in error.error_details


class TestLoadAIConfig:
    """Tests for the load_ai_config function."""

    def test_load_config_with_valid_openai_env_vars(self, monkeypatch):
        """Test loading config from environment with OpenAI provider."""
        monkeypatch.setenv(AI_PROVIDER_ENV_VAR, "openai")
        monkeypatch.setenv(OPENAI_API_KEY_ENV_VAR, "sk-test-openai-key")
        monkeypatch.setenv(AI_MODEL_ENV_VAR, "gpt-4-turbo")

        config = load_ai_config()

        assert config.provider == "openai"
        assert config.api_key == "sk-test-openai-key"
        assert config.model == "gpt-4-turbo"
        assert config.timeout_seconds == DEFAULT_AI_TIMEOUT_SECONDS

    def test_load_config_with_valid_anthropic_env_vars(self, monkeypatch):
        """Test loading config from environment with Anthropic provider."""
        monkeypatch.setenv(AI_PROVIDER_ENV_VAR, "anthropic")
        monkeypatch.setenv(ANTHROPIC_API_KEY_ENV_VAR, "sk-ant-test-key")
        monkeypatch.setenv(AI_MODEL_ENV_VAR, "claude-3-opus-20240229")

        config = load_ai_config()

        assert config.provider == "anthropic"
        assert config.api_key == "sk-ant-test-key"
        assert config.model == "claude-3-opus-20240229"

    def test_load_config_without_model_env_var(self, monkeypatch):
        """Test loading config when model env var is not set (optional)."""
        monkeypatch.setenv(AI_PROVIDER_ENV_VAR, "openai")
        monkeypatch.setenv(OPENAI_API_KEY_ENV_VAR, "sk-test-key")
        # AI_MODEL_ENV_VAR not set
        monkeypatch.delenv(AI_MODEL_ENV_VAR, raising=False)

        config = load_ai_config()

        assert config.provider == "openai"
        assert config.api_key == "sk-test-key"
        assert config.model is None  # Model is optional

    def test_load_config_provider_case_insensitive(self, monkeypatch):
        """Test that provider name is normalized to lowercase."""
        monkeypatch.setenv(AI_PROVIDER_ENV_VAR, "OpenAI")  # Mixed case
        monkeypatch.setenv(OPENAI_API_KEY_ENV_VAR, "sk-test-key")

        config = load_ai_config()

        assert config.provider == "openai"  # Normalized to lowercase

    def test_load_config_missing_provider_env_var(self, monkeypatch):
        """Test that missing provider env var raises error."""
        # Clear all AI-related env vars to ensure clean test
        monkeypatch.delenv(AI_PROVIDER_ENV_VAR, raising=False)
        monkeypatch.delenv(AI_MODEL_ENV_VAR, raising=False)
        monkeypatch.setenv(OPENAI_API_KEY_ENV_VAR, "sk-test-key")

        with pytest.raises(AIProviderError) as exc_info:
            load_ai_config()

        error = exc_info.value
        assert error.provider_name == "unknown"
        assert AI_PROVIDER_ENV_VAR in error.error_details
        assert "Missing required environment variable" in error.error_details

    def test_load_config_unsupported_provider(self, monkeypatch):
        """Test that unsupported provider raises error."""
        monkeypatch.setenv(AI_PROVIDER_ENV_VAR, "gemini")  # Not supported
        monkeypatch.setenv(OPENAI_API_KEY_ENV_VAR, "sk-test-key")

        with pytest.raises(AIProviderError) as exc_info:
            load_ai_config()

        error = exc_info.value
        assert error.provider_name == "gemini"
        assert "Unsupported provider" in error.error_details
        assert "openai" in error.error_details
        assert "anthropic" in error.error_details

    def test_load_config_missing_openai_api_key(self, monkeypatch):
        """Test that missing OpenAI API key raises error."""
        monkeypatch.setenv(AI_PROVIDER_ENV_VAR, "openai")
        # Clear API keys to ensure clean test
        monkeypatch.delenv(OPENAI_API_KEY_ENV_VAR, raising=False)
        monkeypatch.delenv(ANTHROPIC_API_KEY_ENV_VAR, raising=False)

        with pytest.raises(AIProviderError) as exc_info:
            load_ai_config()

        error = exc_info.value
        assert error.provider_name == "openai"
        assert OPENAI_API_KEY_ENV_VAR in error.error_details
        assert "Missing required environment variable" in error.error_details

    def test_load_config_missing_anthropic_api_key(self, monkeypatch):
        """Test that missing Anthropic API key raises error."""
        monkeypatch.setenv(AI_PROVIDER_ENV_VAR, "anthropic")
        # Clear API keys to ensure clean test
        monkeypatch.delenv(OPENAI_API_KEY_ENV_VAR, raising=False)
        monkeypatch.delenv(ANTHROPIC_API_KEY_ENV_VAR, raising=False)

        with pytest.raises(AIProviderError) as exc_info:
            load_ai_config()

        error = exc_info.value
        assert error.provider_name == "anthropic"
        assert ANTHROPIC_API_KEY_ENV_VAR in error.error_details
        assert "Missing required environment variable" in error.error_details

    def test_load_config_wrong_api_key_for_provider(self, monkeypatch):
        """Test that setting wrong API key env var for provider raises error."""
        monkeypatch.setenv(AI_PROVIDER_ENV_VAR, "openai")
        # Clear OpenAI key and set only Anthropic key
        monkeypatch.delenv(OPENAI_API_KEY_ENV_VAR, raising=False)
        monkeypatch.setenv(ANTHROPIC_API_KEY_ENV_VAR, "sk-ant-test")

        with pytest.raises(AIProviderError) as exc_info:
            load_ai_config()

        error = exc_info.value
        assert error.provider_name == "openai"
        assert OPENAI_API_KEY_ENV_VAR in error.error_details
