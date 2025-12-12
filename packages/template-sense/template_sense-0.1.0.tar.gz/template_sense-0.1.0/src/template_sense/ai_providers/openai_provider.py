"""
OpenAI provider implementation for Template Sense.

This module provides a concrete implementation of the AIProvider interface
for OpenAI's API (GPT models). It handles:
- Field classification using structured output
- Text translation
- Error handling and timeout management
"""

import logging

from openai import OpenAI

from template_sense.ai_providers.base_provider import BaseAIProvider
from template_sense.ai_providers.config import AIConfig
from template_sense.constants import (
    AI_CLASSIFICATION_TEMPERATURE,
    AI_TRANSLATION_TEMPERATURE,
    DEFAULT_AI_TIMEOUT_SECONDS,
    DEFAULT_OPENAI_MODEL,
)
from template_sense.errors import AIProviderError

logger = logging.getLogger(__name__)


class OpenAIProvider(BaseAIProvider):
    """
    OpenAI API provider implementation.

    Uses OpenAI's chat completion API with JSON mode for structured outputs.
    Supports GPT-4 and GPT-3.5 models.
    """

    def __init__(self, config: AIConfig):
        """
        Initialize OpenAI provider.

        Args:
            config: AIConfig with provider="openai", api_key, optional model

        Raises:
            AIProviderError: If API key is missing or client initialization fails
        """
        super().__init__(config)

        if not config.api_key:
            raise AIProviderError(
                provider_name="openai",
                error_details="API key is required",
                request_type="initialization",
            )

        try:
            self.client = OpenAI(
                api_key=config.api_key,
                timeout=config.timeout_seconds or DEFAULT_AI_TIMEOUT_SECONDS,
            )
            logger.debug("OpenAI client initialized successfully")
        except Exception as e:
            raise AIProviderError(
                provider_name="openai",
                error_details=f"Failed to initialize client: {str(e)}",
                request_type="initialization",
            ) from e

    @property
    def provider_name(self) -> str:
        """Returns 'openai'."""
        return "openai"

    @property
    def model(self) -> str:
        """Returns the configured model or default 'gpt-4'."""
        return self.config.model or DEFAULT_OPENAI_MODEL

    def _call_classify_api(self, system_message: str, user_message: str) -> str:
        """
        Execute OpenAI API call for classification.

        Args:
            system_message: System prompt for classification
            user_message: User prompt with payload data

        Returns:
            Raw response text from OpenAI API

        Raises:
            OpenAI API exceptions (will be wrapped by BaseAIProvider)
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            response_format={"type": "json_object"},
            temperature=AI_CLASSIFICATION_TEMPERATURE,
        )

        content = response.choices[0].message.content
        return content or ""

    def _call_translate_api(self, system_message: str, user_message: str) -> str:
        """
        Execute OpenAI API call for translation.

        Args:
            system_message: System prompt for translation
            user_message: Text to translate

        Returns:
            Translated text from OpenAI API

        Raises:
            OpenAI API exceptions (will be wrapped by BaseAIProvider)
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            temperature=AI_TRANSLATION_TEMPERATURE,
        )

        content = response.choices[0].message.content
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
        Execute OpenAI API call for text generation.

        Args:
            prompt: User prompt/question
            system_message: Optional system instruction
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0.0-1.0)
            json_mode: Whether to request JSON-formatted response

        Returns:
            Generated text from OpenAI API

        Raises:
            OpenAI API exceptions (will be wrapped by BaseAIProvider)
        """
        messages = []

        # Add system message if provided
        if system_message:
            messages.append({"role": "system", "content": system_message})

        messages.append({"role": "user", "content": prompt})

        # Build request parameters
        request_params = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        # Add JSON mode if requested
        if json_mode:
            request_params["response_format"] = {"type": "json_object"}

        response = self.client.chat.completions.create(**request_params)
        content = response.choices[0].message.content
        return content or ""


__all__ = ["OpenAIProvider"]
