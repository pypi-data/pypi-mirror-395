"""
LLM Provider Adapters.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.

This module provides adapters for various LLM providers including:
- OpenAI (GPT-4, GPT-4o, GPT-3.5)
- Anthropic (Claude 3)
- Google (Gemini)
- Ollama (Local models)
- Azure OpenAI
- AWS Bedrock
"""

from typing import TYPE_CHECKING

# Lazy imports to avoid dependency issues
if TYPE_CHECKING:
    from .openai import OpenAIAdapter
    from .anthropic import AnthropicAdapter
    from .google import GoogleAdapter
    from .ollama import OllamaAdapter
    from .azure import AzureOpenAIAdapter
    from .bedrock import BedrockAdapter

__all__ = [
    "OpenAIAdapter",
    "AnthropicAdapter",
    "GoogleAdapter",
    "OllamaAdapter",
    "AzureOpenAIAdapter",
    "BedrockAdapter",
    "get_adapter",
    "register_all_adapters",
]


def get_adapter(provider: str):
    """Get adapter class for a provider.

    Args:
        provider: Provider name.

    Returns:
        Adapter class.

    Raises:
        ValueError: If provider is not supported.
    """
    provider = provider.lower()

    if provider in ("openai",):
        from .openai import OpenAIAdapter
        return OpenAIAdapter

    elif provider in ("anthropic",):
        from .anthropic import AnthropicAdapter
        return AnthropicAdapter

    elif provider in ("google", "google_gemini", "gemini"):
        from .google import GoogleAdapter
        return GoogleAdapter

    elif provider in ("ollama", "ollama_local", "ollama_cloud"):
        from .ollama import OllamaAdapter
        return OllamaAdapter

    elif provider in ("azure_openai", "azure"):
        from .azure import AzureOpenAIAdapter
        return AzureOpenAIAdapter

    elif provider in ("bedrock", "aws_bedrock"):
        from .bedrock import BedrockAdapter
        return BedrockAdapter

    else:
        raise ValueError(f"Unsupported provider: {provider}")


def register_all_adapters():
    """Register all available adapters with the factory."""
    from ..base import AdapterFactory

    try:
        from .openai import OpenAIAdapter
        AdapterFactory.register("openai", OpenAIAdapter)
    except ImportError:
        pass

    try:
        from .anthropic import AnthropicAdapter
        AdapterFactory.register("anthropic", AnthropicAdapter)
    except ImportError:
        pass

    try:
        from .google import GoogleAdapter
        AdapterFactory.register("google", GoogleAdapter)
        AdapterFactory.register("google_gemini", GoogleAdapter)
        AdapterFactory.register("gemini", GoogleAdapter)
    except ImportError:
        pass

    try:
        from .ollama import OllamaAdapter
        AdapterFactory.register("ollama", OllamaAdapter)
        AdapterFactory.register("ollama_local", OllamaAdapter)
        AdapterFactory.register("ollama_cloud", OllamaAdapter)
    except ImportError:
        pass

    try:
        from .azure import AzureOpenAIAdapter
        AdapterFactory.register("azure_openai", AzureOpenAIAdapter)
        AdapterFactory.register("azure", AzureOpenAIAdapter)
    except ImportError:
        pass

    try:
        from .bedrock import BedrockAdapter
        AdapterFactory.register("bedrock", BedrockAdapter)
        AdapterFactory.register("aws_bedrock", BedrockAdapter)
    except ImportError:
        pass
