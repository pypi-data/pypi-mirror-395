"""
Tests for response caching.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import pytest
from bizstats_llm_router import (
    LLMResponse,
    LLMMessage,
    CacheConfig,
    MemoryCache,
    ResponseCache,
    get_cache,
    generate_cache_key,
)


class TestMemoryCache:
    """Tests for MemoryCache."""

    @pytest.fixture
    def cache(self):
        return MemoryCache(max_size=10, default_ttl=3600)

    @pytest.fixture
    def sample_response(self):
        return LLMResponse(
            content="Test response",
            model="test-model",
            provider="test",
            tokens_used=10,
        )

    @pytest.mark.asyncio
    async def test_set_and_get(self, cache, sample_response):
        """Test setting and getting a cached response."""
        await cache.set("key1", sample_response)
        result = await cache.get("key1")
        assert result is not None
        assert result.content == "Test response"

    @pytest.mark.asyncio
    async def test_get_nonexistent(self, cache):
        """Test getting a non-existent key."""
        result = await cache.get("nonexistent")
        assert result is None

    @pytest.mark.asyncio
    async def test_delete(self, cache, sample_response):
        """Test deleting a cached entry."""
        await cache.set("key1", sample_response)
        await cache.delete("key1")
        result = await cache.get("key1")
        assert result is None

    @pytest.mark.asyncio
    async def test_clear(self, cache, sample_response):
        """Test clearing all entries."""
        await cache.set("key1", sample_response)
        await cache.set("key2", sample_response)
        await cache.clear()
        assert await cache.get("key1") is None
        assert await cache.get("key2") is None

    @pytest.mark.asyncio
    async def test_lru_eviction(self, sample_response):
        """Test LRU eviction when max size reached."""
        cache = MemoryCache(max_size=3, default_ttl=3600)

        await cache.set("key1", sample_response)
        await cache.set("key2", sample_response)
        await cache.set("key3", sample_response)
        await cache.set("key4", sample_response)  # Should evict key1

        assert await cache.get("key1") is None
        assert await cache.get("key4") is not None

    @pytest.mark.asyncio
    async def test_stats(self, cache, sample_response):
        """Test cache statistics."""
        await cache.set("key1", sample_response)
        await cache.get("key1")  # Hit
        await cache.get("nonexistent")  # Miss

        stats = cache.get_stats()
        assert stats["type"] == "memory"
        assert stats["size"] == 1
        assert stats["hits"] == 1
        assert stats["misses"] == 1
        assert stats["hit_rate"] == 50.0


class TestResponseCache:
    """Tests for ResponseCache high-level interface."""

    @pytest.mark.asyncio
    async def test_memory_backend(self):
        """Test memory backend initialization."""
        config = CacheConfig(enabled=True, backend="memory")
        cache = ResponseCache(config)
        await cache.initialize()

        response = LLMResponse(content="Test", model="test", provider="test")
        await cache.set("key1", response)
        result = await cache.get("key1")
        assert result.content == "Test"

    @pytest.mark.asyncio
    async def test_get_without_init(self):
        """Test get without initialization returns None."""
        config = CacheConfig(enabled=False)
        cache = ResponseCache(config)
        result = await cache.get("key1")
        assert result is None

    @pytest.mark.asyncio
    async def test_stats_without_backend(self):
        """Test stats without backend."""
        config = CacheConfig(enabled=False)
        cache = ResponseCache(config)
        stats = cache.get_stats()
        assert stats["enabled"] is False


class TestCacheKeyGeneration:
    """Tests for cache key generation."""

    def test_generate_key_basic(self):
        """Test basic key generation."""
        messages = [{"role": "user", "content": "Hello"}]
        key = generate_cache_key(messages)
        assert len(key) == 64  # SHA256 hex

    def test_generate_key_with_model(self):
        """Test key generation with model."""
        messages = [{"role": "user", "content": "Hello"}]
        key1 = generate_cache_key(messages, model="gpt-4")
        key2 = generate_cache_key(messages, model="gpt-3.5")
        assert key1 != key2

    def test_generate_key_with_temperature(self):
        """Test key generation with temperature."""
        messages = [{"role": "user", "content": "Hello"}]
        key1 = generate_cache_key(messages, temperature=0.5)
        key2 = generate_cache_key(messages, temperature=0.7)
        assert key1 != key2

    def test_generate_key_with_llm_messages(self):
        """Test key generation with LLMMessage objects."""
        messages = [
            LLMMessage(role="user", content="Hello"),
        ]
        key = generate_cache_key(messages)
        assert len(key) == 64

    def test_generate_key_deterministic(self):
        """Test that key generation is deterministic."""
        messages = [{"role": "user", "content": "Hello"}]
        key1 = generate_cache_key(messages, model="test", temperature=0.5)
        key2 = generate_cache_key(messages, model="test", temperature=0.5)
        assert key1 == key2


class TestResponseCacheOperations:
    """Extended tests for ResponseCache operations."""

    @pytest.mark.asyncio
    async def test_delete_with_backend(self):
        """Test delete operation with initialized backend."""
        config = CacheConfig(enabled=True, backend="memory")
        cache = ResponseCache(config)
        await cache.initialize()

        response = LLMResponse(content="Test", model="test", provider="test")
        await cache.set("key1", response)
        await cache.delete("key1")
        result = await cache.get("key1")
        assert result is None

    @pytest.mark.asyncio
    async def test_delete_without_backend(self):
        """Test delete operation without initialized backend."""
        config = CacheConfig(enabled=False)
        cache = ResponseCache(config)
        # Should not raise
        await cache.delete("key1")

    @pytest.mark.asyncio
    async def test_clear_with_backend(self):
        """Test clear operation with initialized backend."""
        config = CacheConfig(enabled=True, backend="memory")
        cache = ResponseCache(config)
        await cache.initialize()

        response = LLMResponse(content="Test", model="test", provider="test")
        await cache.set("key1", response)
        await cache.set("key2", response)
        await cache.clear()
        assert await cache.get("key1") is None
        assert await cache.get("key2") is None

    @pytest.mark.asyncio
    async def test_clear_without_backend(self):
        """Test clear operation without initialized backend."""
        config = CacheConfig(enabled=False)
        cache = ResponseCache(config)
        # Should not raise
        await cache.clear()

    @pytest.mark.asyncio
    async def test_set_without_backend(self):
        """Test set operation without initialized backend."""
        config = CacheConfig(enabled=False)
        cache = ResponseCache(config)
        response = LLMResponse(content="Test", model="test", provider="test")
        # Should not raise
        await cache.set("key1", response)

    @pytest.mark.asyncio
    async def test_stats_with_backend(self):
        """Test stats with initialized backend."""
        config = CacheConfig(enabled=True, backend="memory")
        cache = ResponseCache(config)
        await cache.initialize()
        stats = cache.get_stats()
        assert stats["type"] == "memory"


class TestMemoryCacheExpiration:
    """Tests for cache TTL expiration."""

    @pytest.mark.asyncio
    async def test_expired_entry_returns_none(self):
        """Test that expired entries return None."""
        import time

        cache = MemoryCache(max_size=10, default_ttl=1)
        response = LLMResponse(content="Test", model="test", provider="test")
        await cache.set("key1", response, ttl=0)  # 0 second TTL - immediately expired

        # Force expiration by manipulating the entry
        cache._cache["key1"]["expires_at"] = time.time() - 1

        result = await cache.get("key1")
        assert result is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent_key(self):
        """Test deleting a non-existent key doesn't raise."""
        cache = MemoryCache()
        # Should not raise
        await cache.delete("nonexistent")


class TestGetCache:
    """Tests for get_cache factory function."""

    @pytest.mark.asyncio
    async def test_get_memory_cache(self):
        """Test creating memory cache."""
        config = CacheConfig(enabled=True, backend="memory", max_size=100)
        cache = await get_cache(config)
        assert isinstance(cache, ResponseCache)
