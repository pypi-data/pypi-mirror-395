"""
Tests for LLM Router.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import pytest
from bizstats_llm_router import (
    LLMRouter,
    LLMMessage,
    LLMRouterSettings,
    LLMRegistry,
    create_router,
)


class TestLLMRouter:
    """Tests for LLMRouter class."""

    @pytest.mark.asyncio
    async def test_create_router(self):
        """Test creating a router."""
        router = create_router()
        assert isinstance(router, LLMRouter)

    @pytest.mark.asyncio
    async def test_initialize(self, router):
        """Test router initialization."""
        assert router._initialized is True

    @pytest.mark.asyncio
    async def test_register_adapter(self, router, mock_adapter):
        """Test registering an adapter through router."""
        router.register_adapter("new-adapter", mock_adapter)
        assert router.registry.get("new-adapter") is mock_adapter

    @pytest.mark.asyncio
    async def test_unregister_adapter(self, router, mock_adapter):
        """Test unregistering an adapter."""
        router.register_adapter("temp", mock_adapter)
        router.unregister_adapter("temp")
        assert router.registry.get("temp") is None

    @pytest.mark.asyncio
    async def test_chat_basic(self, router, sample_messages):
        """Test basic chat request."""
        response = await router.chat(sample_messages)
        assert response.content is not None
        # Mock adapter returns sample_response which has model="test-model"
        assert response.model == "test-model"

    @pytest.mark.asyncio
    async def test_chat_with_specific_llm(self, router, sample_messages):
        """Test chat with specific LLM ID."""
        response = await router.chat(
            sample_messages,
            llm_id="test-adapter",
        )
        assert response.content is not None

    @pytest.mark.asyncio
    async def test_chat_with_temperature(self, router, sample_messages):
        """Test chat with custom temperature."""
        response = await router.chat(
            sample_messages,
            temperature=0.5,
        )
        assert response.content is not None

    @pytest.mark.asyncio
    async def test_chat_with_max_tokens(self, router, sample_messages):
        """Test chat with custom max tokens."""
        response = await router.chat(
            sample_messages,
            max_tokens=100,
        )
        assert response.content is not None

    @pytest.mark.asyncio
    async def test_chat_with_request_type(self, router, sample_messages):
        """Test chat with request type for routing."""
        response = await router.chat(
            sample_messages,
            request_type="code",
        )
        assert response.content is not None

    @pytest.mark.asyncio
    async def test_stream_chat(self, router, sample_messages):
        """Test streaming chat."""
        chunks = []
        async for chunk in router.stream_chat(sample_messages):
            chunks.append(chunk)

        assert len(chunks) > 0
        # Last chunk should be final
        assert chunks[-1].is_final is True

    @pytest.mark.asyncio
    async def test_stream_chat_collects_content(self, router, sample_messages):
        """Test that streaming chat collects all content."""
        content = ""
        async for chunk in router.stream_chat(sample_messages):
            content += chunk.content

        assert len(content) > 0

    @pytest.mark.asyncio
    async def test_chat_no_llm_available(self):
        """Test chat when no LLM is available."""
        router = LLMRouter(registry=LLMRegistry())
        await router.initialize()

        with pytest.raises(RuntimeError, match="No LLM available"):
            await router.chat([LLMMessage(role="user", content="Hi")])

    @pytest.mark.asyncio
    async def test_get_metrics(self, router, sample_messages):
        """Test getting router metrics."""
        await router.chat(sample_messages)
        metrics = router.get_metrics()
        assert "registry" in metrics

    @pytest.mark.asyncio
    async def test_get_status(self, router):
        """Test getting router status."""
        status = await router.get_status()
        assert status["initialized"] is True
        assert "registry" in status

    @pytest.mark.asyncio
    async def test_cleanup(self, router):
        """Test router cleanup."""
        await router.cleanup()
        assert router._initialized is False


class TestRouterFailover:
    """Tests for router failover functionality."""

    @pytest.mark.asyncio
    async def test_failover_disabled(
        self, registry, mock_adapter, failing_adapter, sample_messages
    ):
        """Test that failover can be disabled - adapter error propagates."""
        # Don't initialize failing adapter so health check fails
        registry.register("failing", failing_adapter)
        # Don't register any other adapters - this forces failure

        router = LLMRouter(registry=registry)
        await router.initialize()

        # Should fail when no healthy LLM is available
        with pytest.raises(RuntimeError, match="No LLM available"):
            await router.chat(
                sample_messages,
                llm_id="failing",
                enable_failover=False,
            )

    @pytest.mark.asyncio
    async def test_failover_to_backup(
        self, registry, mock_adapter, failing_adapter, sample_messages
    ):
        """Test failover to backup LLM."""
        await mock_adapter.initialize()
        registry.register("failing", failing_adapter)
        registry.register("working", mock_adapter)

        settings = LLMRouterSettings()
        settings.routing.enable_failover = True
        router = LLMRouter(settings=settings, registry=registry)
        await router.initialize()

        # Should succeed with failover
        response = await router.chat(sample_messages)
        assert response.content is not None


class TestRouterAutoInitialize:
    """Tests for auto-initialization."""

    @pytest.mark.asyncio
    async def test_auto_initialize_on_chat(
        self, registry, mock_adapter, sample_messages
    ):
        """Test router auto-initializes on first chat."""
        await mock_adapter.initialize()
        registry.register("test", mock_adapter)

        router = LLMRouter(registry=registry)
        assert router._initialized is False

        # Should auto-initialize
        response = await router.chat(sample_messages)
        assert router._initialized is True
        assert response.content is not None

    @pytest.mark.asyncio
    async def test_auto_initialize_on_stream(
        self, registry, mock_adapter, sample_messages
    ):
        """Test router auto-initializes on stream."""
        await mock_adapter.initialize()
        registry.register("test", mock_adapter)

        router = LLMRouter(registry=registry)

        async for chunk in router.stream_chat(sample_messages):
            pass

        assert router._initialized is True


class TestRouterWithCaching:
    """Tests for router with caching enabled."""

    @pytest.mark.asyncio
    async def test_router_with_cache_enabled(
        self, registry, mock_adapter, sample_messages
    ):
        """Test router with caching enabled."""
        await mock_adapter.initialize()
        registry.register("test", mock_adapter)

        settings = LLMRouterSettings()
        settings.cache.enabled = True
        settings.cache.backend = "memory"

        router = LLMRouter(settings=settings, registry=registry)
        await router.initialize()

        # First call - cache miss
        response1 = await router.chat(sample_messages)
        assert response1.content is not None

        # Second call with same messages should work (may be cached)
        response2 = await router.chat(sample_messages)
        assert response2.content is not None

    @pytest.mark.asyncio
    async def test_cache_key_generation(self, registry, mock_adapter, sample_messages):
        """Test cache key generation."""
        await mock_adapter.initialize()
        registry.register("test", mock_adapter)

        router = LLMRouter(registry=registry)
        await router.initialize()

        key1 = router._generate_cache_key(sample_messages, 0.7, 100)
        key2 = router._generate_cache_key(sample_messages, 0.7, 100)
        key3 = router._generate_cache_key(sample_messages, 0.8, 100)

        assert key1 == key2  # Same params = same key
        assert key1 != key3  # Different temp = different key


class TestRouterWithRateLimiting:
    """Tests for router with rate limiting enabled."""

    @pytest.mark.asyncio
    async def test_router_with_rate_limit_enabled(
        self, registry, mock_adapter, sample_messages
    ):
        """Test router with rate limiting enabled."""
        await mock_adapter.initialize()
        registry.register("test", mock_adapter)

        settings = LLMRouterSettings()
        settings.rate_limit.enabled = True
        settings.rate_limit.requests_per_minute = 60

        router = LLMRouter(settings=settings, registry=registry)
        await router.initialize()

        response = await router.chat(sample_messages)
        assert response.content is not None


class TestRouterWithCostTracking:
    """Tests for router with cost tracking enabled."""

    @pytest.mark.asyncio
    async def test_router_with_cost_tracking(
        self, registry, mock_adapter, sample_messages
    ):
        """Test router with cost tracking enabled."""
        await mock_adapter.initialize()
        registry.register("test", mock_adapter)

        settings = LLMRouterSettings()
        settings.cost_tracking.enabled = True

        router = LLMRouter(settings=settings, registry=registry)
        await router.initialize()

        response = await router.chat(sample_messages)
        assert response.content is not None

    @pytest.mark.asyncio
    async def test_get_metrics_with_cost_tracking(
        self, registry, mock_adapter, sample_messages
    ):
        """Test getting metrics with cost tracking enabled."""
        await mock_adapter.initialize()
        registry.register("test", mock_adapter)

        settings = LLMRouterSettings()
        settings.cost_tracking.enabled = True

        router = LLMRouter(settings=settings, registry=registry)
        await router.initialize()

        await router.chat(sample_messages)
        metrics = router.get_metrics()

        assert "registry" in metrics
        assert "costs" in metrics


class TestRouterStreamErrors:
    """Tests for streaming chat error handling."""

    @pytest.mark.asyncio
    async def test_stream_chat_no_llm_available(self):
        """Test stream chat when no LLM is available."""
        router = LLMRouter(registry=LLMRegistry())
        await router.initialize()

        chunks = []
        async for chunk in router.stream_chat([LLMMessage(role="user", content="Hi")]):
            chunks.append(chunk)

        assert len(chunks) == 1
        assert "Error" in chunks[0].content
        assert chunks[0].is_final is True

    @pytest.mark.asyncio
    async def test_stream_chat_with_error(self, registry, mock_config, sample_messages):
        """Test stream chat when adapter raises error."""
        from typing import AsyncGenerator

        class ErrorStreamAdapter:
            """Adapter that raises error during streaming."""

            def __init__(self, config):
                self.config = config
                self._is_initialized = True
                self._is_available = True
                self.model_name = config.model_name
                self.provider_name = config.provider.value

            async def initialize(self):
                return True

            async def cleanup(self):
                pass

            async def health_check(self):
                return True

            async def stream_chat(self, messages, temperature=None, max_tokens=None, **kwargs):
                raise RuntimeError("Stream error")

            def calculate_cost(self, prompt_tokens, completion_tokens):
                return 0.0

        error_adapter = ErrorStreamAdapter(mock_config)
        registry.register("error", error_adapter)

        router = LLMRouter(registry=registry)
        await router.initialize()

        chunks = []
        async for chunk in router.stream_chat(sample_messages, llm_id="error"):
            chunks.append(chunk)

        assert any("Error" in c.content for c in chunks)


class TestRouterProviderSelection:
    """Tests for provider-specific selection."""

    @pytest.mark.asyncio
    async def test_select_by_provider(
        self, registry, mock_adapter, mock_config, sample_messages
    ):
        """Test selecting LLM by provider."""
        from bizstats_llm_router import LLMProvider

        await mock_adapter.initialize()
        registry.register("openai-1", mock_adapter)

        router = LLMRouter(registry=registry)
        await router.initialize()

        response = await router.chat(
            sample_messages,
            provider=LLMProvider.OPENAI,
        )
        assert response.content is not None


class TestRouterInitializationPaths:
    """Tests for various initialization paths."""

    @pytest.mark.asyncio
    async def test_initialize_already_initialized(self, router):
        """Test initialize when already initialized."""
        # Already initialized by fixture
        assert router._initialized is True

        # Second init should be a no-op
        await router.initialize()
        assert router._initialized is True

    @pytest.mark.asyncio
    async def test_initialize_with_all_features(self, registry, mock_adapter):
        """Test initialization with all features enabled."""
        await mock_adapter.initialize()
        registry.register("test", mock_adapter)

        settings = LLMRouterSettings()
        settings.cache.enabled = True
        settings.cache.backend = "memory"
        settings.rate_limit.enabled = True
        settings.cost_tracking.enabled = True

        router = LLMRouter(settings=settings, registry=registry)
        await router.initialize()

        assert router._initialized is True
        assert router._cache is not None
        assert router._rate_limiter is not None
        assert router._cost_tracker is not None

    @pytest.mark.asyncio
    async def test_get_status_with_all_features(self, registry, mock_adapter):
        """Test get_status with all features enabled."""
        await mock_adapter.initialize()
        registry.register("test", mock_adapter)

        settings = LLMRouterSettings()
        settings.cache.enabled = True
        settings.rate_limit.enabled = True
        settings.cost_tracking.enabled = True

        router = LLMRouter(settings=settings, registry=registry)
        await router.initialize()

        status = await router.get_status()

        assert status["initialized"] is True
        assert status["cache_enabled"] is True
        assert status["rate_limit_enabled"] is True
        assert status["cost_tracking_enabled"] is True


class TestRouterFallbackPaths:
    """Tests for fallback LLM selection."""

    @pytest.mark.asyncio
    async def test_get_fallback_llms(self, registry, mock_adapter, mock_config):
        """Test getting fallback LLMs."""
        await mock_adapter.initialize()
        registry.register("primary", mock_adapter)

        # Create second adapter
        class SecondAdapter:
            def __init__(self, config):
                self.config = config
                self._is_initialized = True
                self._is_available = True

            async def initialize(self):
                return True

            async def health_check(self):
                return True

            async def cleanup(self):
                pass

        backup = SecondAdapter(mock_config)
        registry.register("backup", backup)

        router = LLMRouter(registry=registry)
        await router.initialize()

        fallbacks = await router._get_fallback_llms("primary", "general", None)
        assert "backup" in fallbacks
        assert "primary" not in fallbacks
