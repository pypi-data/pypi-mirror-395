"""Tests for AI provider abstract interface."""

from typing import Any

import pytest

from template_sense.ai_providers.config import AIConfig
from template_sense.ai_providers.interface import AIProvider


class TestAIProviderInterface:
    """Tests for the AIProvider abstract base class."""

    def test_cannot_instantiate_abstract_class(self):
        """Test that AIProvider cannot be instantiated directly."""
        config = AIConfig(provider="openai", api_key="sk-test")

        with pytest.raises(TypeError) as exc_info:
            AIProvider(config)  # type: ignore

        assert "Can't instantiate abstract class" in str(exc_info.value)

    def test_subclass_must_implement_provider_name(self):
        """Test that subclass must implement provider_name property."""

        class IncompleteProvider(AIProvider):
            @property
            def model(self) -> str:
                return "test-model"

            def classify_fields(self, payload: dict[str, Any]) -> dict[str, Any]:
                return {}

            def translate_text(self, text: str, source_lang: str, target_lang: str = "en") -> str:
                return text

            def generate_text(
                self,
                prompt: str,
                system_message: str | None = None,
                max_tokens: int = 150,
                temperature: float = 0.0,
                json_mode: bool = True,
            ) -> str:
                return "generated"

        config = AIConfig(provider="openai", api_key="sk-test")

        with pytest.raises(TypeError) as exc_info:
            IncompleteProvider(config)  # type: ignore

        assert "Can't instantiate abstract class" in str(exc_info.value)

    def test_subclass_must_implement_model(self):
        """Test that subclass must implement model property."""

        class IncompleteProvider(AIProvider):
            @property
            def provider_name(self) -> str:
                return "test"

            def classify_fields(self, payload: dict[str, Any]) -> dict[str, Any]:
                return {}

            def translate_text(self, text: str, source_lang: str, target_lang: str = "en") -> str:
                return text

            def generate_text(
                self,
                prompt: str,
                system_message: str | None = None,
                max_tokens: int = 150,
                temperature: float = 0.0,
                json_mode: bool = True,
            ) -> str:
                return "generated"

        config = AIConfig(provider="openai", api_key="sk-test")

        with pytest.raises(TypeError) as exc_info:
            IncompleteProvider(config)  # type: ignore

        assert "Can't instantiate abstract class" in str(exc_info.value)

    def test_subclass_must_implement_classify_fields(self):
        """Test that subclass must implement classify_fields method."""

        class IncompleteProvider(AIProvider):
            @property
            def provider_name(self) -> str:
                return "test"

            @property
            def model(self) -> str:
                return "test-model"

            def translate_text(self, text: str, source_lang: str, target_lang: str = "en") -> str:
                return text

            def generate_text(
                self,
                prompt: str,
                system_message: str | None = None,
                max_tokens: int = 150,
                temperature: float = 0.0,
                json_mode: bool = True,
            ) -> str:
                return "generated"

        config = AIConfig(provider="openai", api_key="sk-test")

        with pytest.raises(TypeError) as exc_info:
            IncompleteProvider(config)  # type: ignore

        assert "Can't instantiate abstract class" in str(exc_info.value)

    def test_subclass_must_implement_translate_text(self):
        """Test that subclass must implement translate_text method."""

        class IncompleteProvider(AIProvider):
            @property
            def provider_name(self) -> str:
                return "test"

            @property
            def model(self) -> str:
                return "test-model"

            def classify_fields(self, payload: dict[str, Any]) -> dict[str, Any]:
                return {}

        config = AIConfig(provider="openai", api_key="sk-test")

        with pytest.raises(TypeError) as exc_info:
            IncompleteProvider(config)  # type: ignore

        assert "Can't instantiate abstract class" in str(exc_info.value)

    def test_complete_subclass_can_be_instantiated(self):
        """Test that a complete implementation can be instantiated."""

        class CompleteProvider(AIProvider):
            @property
            def provider_name(self) -> str:
                return "test"

            @property
            def model(self) -> str:
                return self.config.model or "default-model"

            def classify_fields(self, payload: dict[str, Any]) -> dict[str, Any]:
                return {"result": "classified"}

            def translate_text(self, text: str, source_lang: str, target_lang: str = "en") -> str:
                return f"translated:{text}"

            def generate_text(
                self,
                prompt: str,
                system_message: str | None = None,
                max_tokens: int = 150,
                temperature: float = 0.0,
                json_mode: bool = True,
            ) -> str:
                return "generated text"

        config = AIConfig(provider="openai", api_key="sk-test", model="gpt-4")
        provider = CompleteProvider(config)

        assert provider.config == config
        assert provider.provider_name == "test"
        assert provider.model == "gpt-4"

    def test_complete_subclass_classify_fields_works(self):
        """Test that classify_fields works in complete implementation."""

        class MockProvider(AIProvider):
            @property
            def provider_name(self) -> str:
                return "mock"

            @property
            def model(self) -> str:
                return "mock-model"

            def classify_fields(self, payload: dict[str, Any]) -> dict[str, Any]:
                return {
                    "classifications": [{"field": "Invoice No", "canonical_key": "invoice_number"}]
                }

            def translate_text(self, text: str, source_lang: str, target_lang: str = "en") -> str:
                return text

            def generate_text(
                self,
                prompt: str,
                system_message: str | None = None,
                max_tokens: int = 150,
                temperature: float = 0.0,
                json_mode: bool = True,
            ) -> str:
                return "generated"

        config = AIConfig(provider="openai", api_key="sk-test")
        provider = MockProvider(config)

        result = provider.classify_fields({"header_fields": []})

        assert "classifications" in result
        assert result["classifications"][0]["canonical_key"] == "invoice_number"

    def test_complete_subclass_translate_text_works(self):
        """Test that translate_text works in complete implementation."""

        class MockProvider(AIProvider):
            @property
            def provider_name(self) -> str:
                return "mock"

            @property
            def model(self) -> str:
                return "mock-model"

            def classify_fields(self, payload: dict[str, Any]) -> dict[str, Any]:
                return {}

            def translate_text(self, text: str, source_lang: str, target_lang: str = "en") -> str:
                if source_lang == "ja" and target_lang == "en":
                    return "Invoice Number"
                return text

            def generate_text(
                self,
                prompt: str,
                system_message: str | None = None,
                max_tokens: int = 150,
                temperature: float = 0.0,
                json_mode: bool = True,
            ) -> str:
                return "generated"

        config = AIConfig(provider="openai", api_key="sk-test")
        provider = MockProvider(config)

        result = provider.translate_text("請求書番号", source_lang="ja")

        assert result == "Invoice Number"

    def test_config_stored_in_provider(self):
        """Test that config is properly stored in provider instance."""

        class MockProvider(AIProvider):
            @property
            def provider_name(self) -> str:
                return "mock"

            @property
            def model(self) -> str:
                return "mock-model"

            def classify_fields(self, payload: dict[str, Any]) -> dict[str, Any]:
                return {}

            def translate_text(self, text: str, source_lang: str, target_lang: str = "en") -> str:
                return text

            def generate_text(
                self,
                prompt: str,
                system_message: str | None = None,
                max_tokens: int = 150,
                temperature: float = 0.0,
                json_mode: bool = True,
            ) -> str:
                return "generated"

        config = AIConfig(
            provider="openai", api_key="sk-secret-123", model="gpt-4", timeout_seconds=60
        )
        provider = MockProvider(config)

        assert provider.config.provider == "openai"
        assert provider.config.api_key == "sk-secret-123"
        assert provider.config.model == "gpt-4"
        assert provider.config.timeout_seconds == 60
