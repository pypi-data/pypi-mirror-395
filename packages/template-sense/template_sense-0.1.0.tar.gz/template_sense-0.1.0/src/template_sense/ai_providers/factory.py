"""
AI provider factory for Template Sense.

This module provides a factory function to instantiate AI provider implementations.
It handles loading configuration from environment variables and returning the
appropriate provider instance.

Functions:
    get_ai_provider: Factory function to get AI provider instance

Usage Example:
    from template_sense.ai_providers.factory import get_ai_provider
    from template_sense.ai_providers.config import AIConfig

    # Load from environment variables
    provider = get_ai_provider()

    # Or with explicit config
    config = AIConfig(provider="openai", api_key="sk-...", model="gpt-4")
    provider = get_ai_provider(config)
"""

from template_sense.ai_providers.config import AIConfig, load_ai_config
from template_sense.ai_providers.interface import AIProvider
from template_sense.errors import AIProviderError


def get_ai_provider(config: AIConfig | None = None) -> AIProvider:
    """
    Factory function to get an AI provider instance.

    This function creates and returns an appropriate AI provider based on the
    configuration. If no config is provided, it loads configuration from
    environment variables.

    Supports OpenAI (GPT models) and Anthropic (Claude models).

    Args:
        config: Optional AI provider configuration. If None, loads from environment.

    Returns:
        AIProvider: Instance of OpenAIProvider or AnthropicProvider

    Raises:
        AIProviderError: If config loading fails, provider is unsupported, or
                        initialization fails

    Example:
        >>> from template_sense.ai_providers.factory import get_ai_provider
        >>> provider = get_ai_provider()  # Loads from env vars
        >>> result = provider.classify_fields(payload)
    """
    # Load config from environment if not provided
    if config is None:
        config = load_ai_config()

    # Validate provider is supported (already validated in AIConfig.__post_init__)
    provider_name = config.provider

    # Lazy import providers to avoid circular dependencies
    if provider_name == "openai":
        from template_sense.ai_providers.openai_provider import OpenAIProvider

        return OpenAIProvider(config)
    if provider_name == "anthropic":
        from template_sense.ai_providers.anthropic_provider import AnthropicProvider

        return AnthropicProvider(config)

    # Should never reach here due to validation in AIConfig.__post_init__
    raise AIProviderError(
        provider_name=provider_name,
        error_details=f"Provider implementation not found for '{provider_name}'.",
    )


__all__ = ["get_ai_provider"]
