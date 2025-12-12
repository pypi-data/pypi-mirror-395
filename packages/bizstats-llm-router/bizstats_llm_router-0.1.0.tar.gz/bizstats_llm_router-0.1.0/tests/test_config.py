"""
Tests for configuration classes.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import pytest
from bizstats_llm_router import (
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


class TestLLMProvider:
    """Tests for LLMProvider enum."""

    def test_provider_values(self):
        """Test provider enum values."""
        assert LLMProvider.OPENAI.value == "openai"
        assert LLMProvider.ANTHROPIC.value == "anthropic"
        assert LLMProvider.GOOGLE.value == "google"
        assert LLMProvider.OLLAMA.value == "ollama"
        assert LLMProvider.AZURE_OPENAI.value == "azure_openai"
        assert LLMProvider.BEDROCK.value == "bedrock"


class TestCapabilityType:
    """Tests for CapabilityType enum."""

    def test_capability_values(self):
        """Test capability enum values."""
        assert CapabilityType.TEXT.value == "text"
        assert CapabilityType.VISION.value == "vision"
        assert CapabilityType.TOOLS.value == "tools"
        assert CapabilityType.CODE.value == "code"
        assert CapabilityType.STREAMING.value == "streaming"


class TestLLMConfig:
    """Tests for LLMConfig dataclass."""

    def test_basic_config(self):
        """Test creating basic config."""
        config = LLMConfig(
            provider=LLMProvider.OPENAI,
            model_name="gpt-4",
        )
        assert config.provider == LLMProvider.OPENAI
        assert config.model_name == "gpt-4"
        assert config.temperature == 0.7
        assert config.max_tokens == 1000
        assert config.context_length == 4096

    def test_config_with_all_fields(self):
        """Test config with all fields."""
        config = LLMConfig(
            provider=LLMProvider.ANTHROPIC,
            model_name="claude-3-opus",
            api_key="test-key",
            api_base="https://api.anthropic.com",
            context_length=200000,
            temperature=0.5,
            max_tokens=4000,
            cost_per_1k_input=0.015,
            cost_per_1k_output=0.075,
            capabilities=[CapabilityType.TEXT, CapabilityType.VISION],
            privacy_level=PrivacyLevel.STANDARD,
            specialization="advanced_reasoning",
            timeout=120,
            max_retries=5,
        )
        assert config.api_key == "test-key"
        assert config.context_length == 200000
        assert config.cost_per_1k_output == 0.075
        assert CapabilityType.VISION in config.capabilities

    def test_config_to_dict(self):
        """Test converting config to dictionary."""
        config = LLMConfig(
            provider=LLMProvider.OPENAI,
            model_name="gpt-4",
            api_key="secret-key",
        )
        d = config.to_dict()
        assert d["provider"] == "openai"
        assert d["model_name"] == "gpt-4"
        assert d["api_key"] == "***"  # Should be masked


class TestProviderConfig:
    """Tests for ProviderConfig model."""

    def test_default_values(self):
        """Test default values."""
        config = ProviderConfig(provider=LLMProvider.OPENAI)
        assert config.enabled is True
        assert config.timeout == 60
        assert config.max_retries == 3
        assert config.models == []

    def test_with_models(self):
        """Test config with models list."""
        config = ProviderConfig(
            provider=LLMProvider.OPENAI,
            api_key="test-key",
            models=["gpt-4", "gpt-3.5-turbo"],
            default_model="gpt-4",
        )
        assert len(config.models) == 2
        assert config.default_model == "gpt-4"


class TestRoutingConfig:
    """Tests for RoutingConfig model."""

    def test_default_values(self):
        """Test default routing config."""
        config = RoutingConfig()
        assert config.default_provider == LLMProvider.OLLAMA
        assert config.enable_failover is True
        assert config.max_failover_attempts == 3
        assert config.selection_strategy == SelectionStrategy.LEAST_USED

    def test_custom_routing(self):
        """Test custom routing config."""
        config = RoutingConfig(
            default_provider=LLMProvider.OPENAI,
            fallback_providers=[LLMProvider.ANTHROPIC, LLMProvider.OLLAMA],
            selection_strategy=SelectionStrategy.CHEAPEST,
            routing_rules={"code": ["gpt-4", "claude-3"]},
        )
        assert len(config.fallback_providers) == 2
        assert config.selection_strategy == SelectionStrategy.CHEAPEST


class TestCacheConfig:
    """Tests for CacheConfig model."""

    def test_default_values(self):
        """Test default cache config."""
        config = CacheConfig()
        assert config.enabled is False
        assert config.backend == "memory"
        assert config.ttl_seconds == 3600
        assert config.max_size == 1000

    def test_redis_config(self):
        """Test Redis cache config."""
        config = CacheConfig(
            enabled=True,
            backend="redis",
            redis_url="redis://localhost:6379",
            ttl_seconds=7200,
        )
        assert config.backend == "redis"
        assert config.redis_url == "redis://localhost:6379"


class TestRateLimitConfig:
    """Tests for RateLimitConfig model."""

    def test_default_values(self):
        """Test default rate limit config."""
        config = RateLimitConfig()
        assert config.enabled is False
        assert config.requests_per_minute == 60
        assert config.tokens_per_minute == 100000
        assert config.burst_size == 10

    def test_custom_limits(self):
        """Test custom rate limits."""
        config = RateLimitConfig(
            enabled=True,
            requests_per_minute=30,
            per_provider_limits={
                "openai": {"requests_per_minute": 20},
            },
        )
        assert config.requests_per_minute == 30
        assert "openai" in config.per_provider_limits


class TestCostTrackingConfig:
    """Tests for CostTrackingConfig model."""

    def test_default_values(self):
        """Test default cost tracking config."""
        config = CostTrackingConfig()
        assert config.enabled is True
        assert config.budget_limit_daily is None
        assert config.budget_limit_monthly is None
        assert config.alert_threshold_percent == 80.0

    def test_with_budgets(self):
        """Test config with budgets."""
        config = CostTrackingConfig(
            budget_limit_daily=10.0,
            budget_limit_monthly=200.0,
            alert_threshold_percent=90.0,
            track_per_user=True,
        )
        assert config.budget_limit_daily == 10.0
        assert config.budget_limit_monthly == 200.0
        assert config.track_per_user is True


class TestLLMRouterSettings:
    """Tests for LLMRouterSettings model."""

    def test_default_settings(self):
        """Test default router settings."""
        settings = LLMRouterSettings()
        assert settings.default_temperature == 0.7
        assert settings.default_max_tokens == 2000
        assert settings.log_requests is True

    def test_custom_settings(self):
        """Test custom router settings."""
        settings = LLMRouterSettings(
            default_temperature=0.5,
            default_max_tokens=4000,
            log_responses=True,
            routing=RoutingConfig(enable_failover=False),
            cache=CacheConfig(enabled=True),
        )
        assert settings.default_temperature == 0.5
        assert settings.routing.enable_failover is False
        assert settings.cache.enabled is True


class TestDefaultModelConfigs:
    """Tests for default model configurations."""

    def test_openai_models(self):
        """Test OpenAI model configs exist."""
        assert "openai" in DEFAULT_MODEL_CONFIGS
        assert "gpt-4" in DEFAULT_MODEL_CONFIGS["openai"]
        assert "gpt-4o" in DEFAULT_MODEL_CONFIGS["openai"]

    def test_anthropic_models(self):
        """Test Anthropic model configs exist."""
        assert "anthropic" in DEFAULT_MODEL_CONFIGS
        assert "claude-3-opus-20240229" in DEFAULT_MODEL_CONFIGS["anthropic"]

    def test_google_models(self):
        """Test Google model configs exist."""
        assert "google" in DEFAULT_MODEL_CONFIGS
        assert "gemini-1.5-pro" in DEFAULT_MODEL_CONFIGS["google"]

    def test_ollama_models(self):
        """Test Ollama model configs exist."""
        assert "ollama" in DEFAULT_MODEL_CONFIGS
        assert "gemma2:9b" in DEFAULT_MODEL_CONFIGS["ollama"]

    def test_model_config_structure(self):
        """Test model config has expected fields."""
        gpt4_config = DEFAULT_MODEL_CONFIGS["openai"]["gpt-4"]
        assert "context_length" in gpt4_config
        assert "capabilities" in gpt4_config
        assert "cost_per_1k_input" in gpt4_config
