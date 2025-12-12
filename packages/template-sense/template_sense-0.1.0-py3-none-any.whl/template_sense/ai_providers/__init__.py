"""
AI provider abstraction layer for Template Sense.

This package provides a provider-agnostic interface for AI operations,
allowing Tako to use different AI providers (OpenAI, Anthropic) without
changing core application logic.

Public API:
    AIProvider: Abstract base class for all provider implementations
    AIConfig: Configuration dataclass for provider settings
    load_ai_config: Load configuration from environment variables
    get_ai_provider: Factory function to get provider instance
    OpenAIProvider: OpenAI (GPT) provider implementation
    AnthropicProvider: Anthropic (Claude) provider implementation

Usage Example:
    from template_sense.ai_providers import get_ai_provider

    # Load provider from environment variables
    provider = get_ai_provider()

    # Or with explicit config
    from template_sense.ai_providers import AIConfig

    config = AIConfig(provider="openai", api_key="sk-...", model="gpt-4")
    provider = get_ai_provider(config)

    # Use provider for classification
    result = provider.classify_fields(payload)
"""

from template_sense.ai_providers.anthropic_provider import AnthropicProvider
from template_sense.ai_providers.config import AIConfig, load_ai_config
from template_sense.ai_providers.factory import get_ai_provider
from template_sense.ai_providers.interface import AIProvider
from template_sense.ai_providers.openai_provider import OpenAIProvider

__all__ = [
    "AIProvider",
    "AIConfig",
    "load_ai_config",
    "get_ai_provider",
    "OpenAIProvider",
    "AnthropicProvider",
]
