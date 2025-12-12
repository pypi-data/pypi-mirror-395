"""
BizStats LLM Router - Multi-provider LLM routing with intelligent failover.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.

This package provides:
- Multi-provider LLM support (OpenAI, Anthropic, Google, Ollama, Azure, Bedrock)
- Intelligent request routing with automatic failover
- Response caching for cost optimization
- Rate limiting to prevent API abuse
- Cost tracking and budget management
- CrewAI integration support

Basic Usage:
    from bizstats_llm_router import LLMRouter, LLMMessage
    from bizstats_llm_router.adapters import create_openai_adapter

    # Create router
    router = LLMRouter()

    # Register adapters
    adapter = create_openai_adapter("gpt-4", api_key="your-key")
    router.register_adapter("gpt4", adapter)

    # Initialize
    await router.initialize()

    # Send request
    response = await router.chat([
        LLMMessage(role="user", content="Hello!")
    ])
"""

__version__ = "0.1.0"
__author__ = "Absolut-e Data Com Inc."
__license__ = "Proprietary"

# Core classes
from .base import (
    LLMAdapter,
    LLMMessage,
    LLMResponse,
    StreamChunk,
    AdapterFactory,
    create_message,
    messages_from_dicts,
    messages_to_dicts,
)

# Configuration
from .config import (
    LLMConfig,
    LLMProvider,
    LLMRouterSettings,
    CapabilityType,
    SelectionStrategy,
    PrivacyLevel,
    ProviderConfig,
    RoutingConfig,
    CacheConfig,
    RateLimitConfig,
    CostTrackingConfig,
    DEFAULT_MODEL_CONFIGS,
)

# Registry
from .registry import (
    LLMRegistry,
    get_registry,
    reset_registry,
)

# Router
from .router import (
    LLMRouter,
    create_router,
)

# Caching
from .caching import (
    ResponseCache,
    MemoryCache,
    get_cache,
    generate_cache_key,
)

# Rate limiting
from .rate_limiting import (
    RateLimiter,
    RateLimitExceeded,
    get_rate_limiter,
)

# Cost tracking
from .cost_tracking import (
    CostTracker,
    CostSummary,
    get_cost_tracker,
)

__all__ = [
    # Version
    "__version__",
    # Base
    "LLMAdapter",
    "LLMMessage",
    "LLMResponse",
    "StreamChunk",
    "AdapterFactory",
    "create_message",
    "messages_from_dicts",
    "messages_to_dicts",
    # Config
    "LLMConfig",
    "LLMProvider",
    "LLMRouterSettings",
    "CapabilityType",
    "SelectionStrategy",
    "PrivacyLevel",
    "ProviderConfig",
    "RoutingConfig",
    "CacheConfig",
    "RateLimitConfig",
    "CostTrackingConfig",
    "DEFAULT_MODEL_CONFIGS",
    # Registry
    "LLMRegistry",
    "get_registry",
    "reset_registry",
    # Router
    "LLMRouter",
    "create_router",
    # Caching
    "ResponseCache",
    "MemoryCache",
    "get_cache",
    "generate_cache_key",
    # Rate limiting
    "RateLimiter",
    "RateLimitExceeded",
    "get_rate_limiter",
    # Cost tracking
    "CostTracker",
    "CostSummary",
    "get_cost_tracker",
]
