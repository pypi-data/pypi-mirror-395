"""
Configuration classes for LLM Router.

Provides Pydantic-based configuration for LLM providers, routing, and caching.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class LLMProvider(str, Enum):
    """Supported LLM providers."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    GOOGLE_GEMINI = "google_gemini"
    OLLAMA = "ollama"
    OLLAMA_LOCAL = "ollama_local"
    OLLAMA_CLOUD = "ollama_cloud"
    AZURE_OPENAI = "azure_openai"
    VERTEX_AI = "vertex_ai"
    BEDROCK = "bedrock"
    OPENROUTER = "openrouter"
    HUGGINGFACE = "huggingface"
    CUSTOM = "custom"


class CapabilityType(str, Enum):
    """LLM capability types."""

    TEXT = "text"
    VISION = "vision"
    TOOLS = "tools"
    CODE = "code"
    ANALYSIS = "analysis"
    MULTILINGUAL = "multilingual"
    REASONING = "reasoning"
    EMBEDDING = "embedding"
    STREAMING = "streaming"


class SelectionStrategy(str, Enum):
    """LLM selection strategies for routing."""

    LEAST_USED = "least_used"
    FASTEST = "fastest"
    CHEAPEST = "cheapest"
    ROUND_ROBIN = "round_robin"
    PRIORITY = "priority"
    RANDOM = "random"


class PrivacyLevel(str, Enum):
    """Privacy levels for LLM providers."""

    LOW = "low"  # Cloud providers with minimal privacy
    STANDARD = "standard"  # Standard cloud providers
    HIGH = "high"  # Local models, high privacy


@dataclass
class LLMConfig:
    """Configuration for a single LLM instance."""

    provider: LLMProvider
    model_name: str
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    local_path: Optional[str] = None
    context_length: int = 4096
    temperature: float = 0.7
    max_tokens: int = 1000
    cost_per_1k_input: float = 0.0
    cost_per_1k_output: float = 0.0
    capabilities: List[CapabilityType] = field(default_factory=list)
    privacy_level: PrivacyLevel = PrivacyLevel.STANDARD
    specialization: Optional[str] = None
    custom_params: Dict[str, Any] = field(default_factory=dict)

    # Model metadata
    family: Optional[str] = None
    parameter_size: Optional[str] = None
    quantization: Optional[str] = None

    # Performance settings
    timeout: int = 60
    max_retries: int = 3
    retry_delay: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "provider": self.provider.value,
            "model_name": self.model_name,
            "api_key": "***" if self.api_key else None,
            "api_base": self.api_base,
            "context_length": self.context_length,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "cost_per_1k_input": self.cost_per_1k_input,
            "cost_per_1k_output": self.cost_per_1k_output,
            "capabilities": [c.value for c in self.capabilities],
            "privacy_level": self.privacy_level.value,
            "specialization": self.specialization,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
        }


class ProviderConfig(BaseModel):
    """Configuration for a provider in settings."""

    provider: LLMProvider
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    enabled: bool = True
    default_model: Optional[str] = None
    models: List[str] = Field(default_factory=list)
    timeout: int = 60
    max_retries: int = 3
    extra_config: Dict[str, Any] = Field(default_factory=dict)


class RoutingConfig(BaseModel):
    """Configuration for request routing."""

    default_provider: LLMProvider = LLMProvider.OLLAMA
    fallback_providers: List[LLMProvider] = Field(default_factory=list)
    selection_strategy: SelectionStrategy = SelectionStrategy.LEAST_USED
    enable_failover: bool = True
    max_failover_attempts: int = 3
    routing_rules: Dict[str, List[str]] = Field(default_factory=dict)


class CacheConfig(BaseModel):
    """Configuration for response caching."""

    enabled: bool = False
    backend: str = "memory"  # memory, redis
    redis_url: Optional[str] = None
    ttl_seconds: int = 3600
    max_size: int = 1000
    cache_key_prefix: str = "llm_router"


class RateLimitConfig(BaseModel):
    """Configuration for rate limiting."""

    enabled: bool = False
    requests_per_minute: int = 60
    tokens_per_minute: int = 100000
    burst_size: int = 10
    per_provider_limits: Dict[str, Dict[str, int]] = Field(default_factory=dict)


class CostTrackingConfig(BaseModel):
    """Configuration for cost tracking."""

    enabled: bool = True
    budget_limit_daily: Optional[float] = None
    budget_limit_monthly: Optional[float] = None
    alert_threshold_percent: float = 80.0
    track_per_user: bool = False


class LLMRouterSettings(BaseSettings):
    """Main settings for LLM Router."""

    # Provider configurations
    providers: Dict[str, ProviderConfig] = Field(default_factory=dict)

    # Routing configuration
    routing: RoutingConfig = Field(default_factory=RoutingConfig)

    # Caching configuration
    cache: CacheConfig = Field(default_factory=CacheConfig)

    # Rate limiting configuration
    rate_limit: RateLimitConfig = Field(default_factory=RateLimitConfig)

    # Cost tracking configuration
    cost_tracking: CostTrackingConfig = Field(default_factory=CostTrackingConfig)

    # Default settings
    default_temperature: float = 0.7
    default_max_tokens: int = 2000
    default_timeout: int = 60

    # Logging
    log_requests: bool = True
    log_responses: bool = False
    log_costs: bool = True

    class Config:
        env_prefix = "LLM_ROUTER_"
        env_nested_delimiter = "__"


# Default model configurations for known providers
DEFAULT_MODEL_CONFIGS: Dict[str, Dict[str, Any]] = {
    "openai": {
        "gpt-4": {
            "context_length": 8192,
            "capabilities": [CapabilityType.TEXT, CapabilityType.TOOLS, CapabilityType.REASONING],
            "cost_per_1k_input": 0.03,
            "cost_per_1k_output": 0.06,
            "specialization": "advanced_reasoning",
        },
        "gpt-4-turbo": {
            "context_length": 128000,
            "capabilities": [
                CapabilityType.TEXT,
                CapabilityType.TOOLS,
                CapabilityType.REASONING,
                CapabilityType.VISION,
            ],
            "cost_per_1k_input": 0.01,
            "cost_per_1k_output": 0.03,
            "specialization": "advanced_reasoning",
        },
        "gpt-4o": {
            "context_length": 128000,
            "capabilities": [
                CapabilityType.TEXT,
                CapabilityType.TOOLS,
                CapabilityType.REASONING,
                CapabilityType.VISION,
            ],
            "cost_per_1k_input": 0.005,
            "cost_per_1k_output": 0.015,
            "specialization": "multimodal",
        },
        "gpt-3.5-turbo": {
            "context_length": 16384,
            "capabilities": [CapabilityType.TEXT, CapabilityType.TOOLS],
            "cost_per_1k_input": 0.0005,
            "cost_per_1k_output": 0.0015,
            "specialization": "general",
        },
    },
    "anthropic": {
        "claude-3-opus-20240229": {
            "context_length": 200000,
            "capabilities": [
                CapabilityType.TEXT,
                CapabilityType.TOOLS,
                CapabilityType.REASONING,
                CapabilityType.VISION,
                CapabilityType.ANALYSIS,
            ],
            "cost_per_1k_input": 0.015,
            "cost_per_1k_output": 0.075,
            "specialization": "advanced_reasoning",
        },
        "claude-3-sonnet-20240229": {
            "context_length": 200000,
            "capabilities": [
                CapabilityType.TEXT,
                CapabilityType.TOOLS,
                CapabilityType.REASONING,
                CapabilityType.VISION,
            ],
            "cost_per_1k_input": 0.003,
            "cost_per_1k_output": 0.015,
            "specialization": "balanced",
        },
        "claude-3-haiku-20240307": {
            "context_length": 200000,
            "capabilities": [CapabilityType.TEXT, CapabilityType.TOOLS, CapabilityType.VISION],
            "cost_per_1k_input": 0.00025,
            "cost_per_1k_output": 0.00125,
            "specialization": "fast",
        },
    },
    "google": {
        "gemini-1.5-pro": {
            "context_length": 1000000,
            "capabilities": [
                CapabilityType.TEXT,
                CapabilityType.TOOLS,
                CapabilityType.REASONING,
                CapabilityType.VISION,
                CapabilityType.MULTILINGUAL,
            ],
            "cost_per_1k_input": 0.00125,
            "cost_per_1k_output": 0.005,
            "specialization": "multimodal",
        },
        "gemini-1.5-flash": {
            "context_length": 1000000,
            "capabilities": [
                CapabilityType.TEXT,
                CapabilityType.TOOLS,
                CapabilityType.VISION,
                CapabilityType.MULTILINGUAL,
            ],
            "cost_per_1k_input": 0.000075,
            "cost_per_1k_output": 0.0003,
            "specialization": "fast",
        },
        "gemini-2.0-flash-exp": {
            "context_length": 1000000,
            "capabilities": [
                CapabilityType.TEXT,
                CapabilityType.TOOLS,
                CapabilityType.REASONING,
                CapabilityType.VISION,
            ],
            "cost_per_1k_input": 0.0,
            "cost_per_1k_output": 0.0,
            "specialization": "experimental",
        },
    },
    "ollama": {
        "gemma2:9b": {
            "context_length": 8192,
            "capabilities": [CapabilityType.TEXT, CapabilityType.TOOLS, CapabilityType.REASONING],
            "cost_per_1k_input": 0.0,
            "cost_per_1k_output": 0.0,
            "specialization": "general_advanced",
            "privacy_level": PrivacyLevel.HIGH,
        },
        "llama3.1:8b": {
            "context_length": 8192,
            "capabilities": [CapabilityType.TEXT, CapabilityType.TOOLS, CapabilityType.REASONING],
            "cost_per_1k_input": 0.0,
            "cost_per_1k_output": 0.0,
            "specialization": "general",
            "privacy_level": PrivacyLevel.HIGH,
        },
        "llama3.1:70b": {
            "context_length": 8192,
            "capabilities": [
                CapabilityType.TEXT,
                CapabilityType.TOOLS,
                CapabilityType.REASONING,
                CapabilityType.ANALYSIS,
            ],
            "cost_per_1k_input": 0.0,
            "cost_per_1k_output": 0.0,
            "specialization": "advanced_reasoning",
            "privacy_level": PrivacyLevel.HIGH,
        },
    },
}
