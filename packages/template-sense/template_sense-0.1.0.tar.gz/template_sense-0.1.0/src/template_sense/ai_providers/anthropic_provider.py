"""
Anthropic provider implementation for Template Sense.

This module provides a concrete implementation of the AIProvider interface
for Anthropic's API (Claude models). It handles:
- Field classification using structured output
- Text translation
- Error handling and timeout management
"""

import logging

from anthropic import Anthropic

from template_sense.ai_providers.base_provider import BaseAIProvider
from template_sense.ai_providers.config import AIConfig
from template_sense.constants import (
    AI_CLASSIFICATION_TEMPERATURE,
    AI_TRANSLATION_TEMPERATURE,
    ANTHROPIC_CLASSIFICATION_MAX_TOKENS,
    ANTHROPIC_TRANSLATION_MAX_TOKENS,
    DEFAULT_AI_TIMEOUT_SECONDS,
    DEFAULT_ANTHROPIC_MODEL,
)
from template_sense.errors import AIProviderError

logger = logging.getLogger(__name__)


class AnthropicProvider(BaseAIProvider):
    """
    Anthropic API provider implementation.

    Uses Anthropic's Messages API for Claude models.
    Instructs Claude to return JSON-formatted responses.
    """

    def __init__(self, config: AIConfig):
        """
        Initialize Anthropic provider.

        Args:
            config: AIConfig with provider="anthropic", api_key, optional model

        Raises:
            AIProviderError: If API key is missing or client initialization fails
        """
        super().__init__(config)

        if not config.api_key:
            raise AIProviderError(
                provider_name="anthropic",
                error_details="API key is required",
                request_type="initialization",
            )

        try:
            self.client = Anthropic(
                api_key=config.api_key,
                timeout=config.timeout_seconds or DEFAULT_AI_TIMEOUT_SECONDS,
            )
            logger.debug("Anthropic client initialized successfully")
        except Exception as e:
            raise AIProviderError(
                provider_name="anthropic",
                error_details=f"Failed to initialize client: {str(e)}",
                request_type="initialization",
            ) from e

    @property
    def provider_name(self) -> str:
        """Returns 'anthropic'."""
        return "anthropic"

    @property
    def model(self) -> str:
        """Returns the configured model or default 'claude-3-sonnet-20240229'."""
        return self.config.model or DEFAULT_ANTHROPIC_MODEL

    def _call_classify_api(self, system_message: str, user_message: str) -> str:
        """
        Execute Anthropic API call for classification.

        Args:
            system_message: System prompt for classification
            user_message: User prompt with payload data

        Returns:
            Raw response text from Anthropic API

        Raises:
            Anthropic API exceptions (will be wrapped by BaseAIProvider)
        """
        response = self.client.messages.create(
            model=self.model,
            max_tokens=ANTHROPIC_CLASSIFICATION_MAX_TOKENS,
            temperature=AI_CLASSIFICATION_TEMPERATURE,
            system=system_message,
            messages=[{"role": "user", "content": user_message}],
        )

        if not response.content:
            return ""

        content = response.content[0].text
        return content or ""

    def _call_translate_api(self, system_message: str, user_message: str) -> str:
        """
        Execute Anthropic API call for translation.

        Args:
            system_message: System prompt for translation
            user_message: Text to translate

        Returns:
            Translated text from Anthropic API

        Raises:
            Anthropic API exceptions (will be wrapped by BaseAIProvider)
        """
        response = self.client.messages.create(
            model=self.model,
            max_tokens=ANTHROPIC_TRANSLATION_MAX_TOKENS,
            temperature=AI_TRANSLATION_TEMPERATURE,
            system=system_message,
            messages=[{"role": "user", "content": user_message}],
        )

        if not response.content:
            return ""

        content = response.content[0].text
        return content or ""

    def _call_generate_api(
        self,
        prompt: str,
        system_message: str | None,
        max_tokens: int,
        temperature: float,
        json_mode: bool,
    ) -> str:
        """
        Execute Anthropic API call for text generation.

        Args:
            prompt: User prompt/question
            system_message: Optional system instruction
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0.0-1.0)
            json_mode: Whether to request JSON-formatted response

        Returns:
            Generated text from Anthropic API

        Raises:
            Anthropic API exceptions (will be wrapped by BaseAIProvider)
        """
        # Anthropic doesn't have native JSON mode - add to system message
        final_system_message = system_message or ""

        if json_mode and final_system_message:
            final_system_message += " Respond with valid JSON only."
        elif json_mode:
            final_system_message = "Respond with valid JSON only."

        # Build request parameters
        request_params = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}],
        }

        # Add system message if present
        if final_system_message:
            request_params["system"] = final_system_message

        response = self.client.messages.create(**request_params)

        if not response.content:
            return ""

        content = response.content[0].text
        return content or ""


__all__ = ["AnthropicProvider"]
