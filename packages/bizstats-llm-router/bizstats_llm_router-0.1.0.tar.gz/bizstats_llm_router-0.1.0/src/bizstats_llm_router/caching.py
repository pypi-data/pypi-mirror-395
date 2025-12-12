"""
Response Caching for LLM Router.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.

Provides caching mechanisms for LLM responses to reduce costs and latency.
"""

import hashlib
import json
import logging
import time
from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import Any, Dict, Optional

from .base import LLMResponse
from .config import CacheConfig

logger = logging.getLogger(__name__)


class CacheBackend(ABC):
    """Abstract base class for cache backends."""

    @abstractmethod
    async def get(self, key: str) -> Optional[LLMResponse]:
        """Get a cached response."""
        pass

    @abstractmethod
    async def set(self, key: str, response: LLMResponse, ttl: Optional[int] = None) -> None:
        """Cache a response."""
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete a cached entry."""
        pass

    @abstractmethod
    async def clear(self) -> None:
        """Clear all cached entries."""
        pass

    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        pass


class MemoryCache(CacheBackend):
    """In-memory LRU cache implementation."""

    def __init__(self, max_size: int = 1000, default_ttl: int = 3600):
        self._cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
        self._max_size = max_size
        self._default_ttl = default_ttl
        self._hits = 0
        self._misses = 0

    async def get(self, key: str) -> Optional[LLMResponse]:
        """Get a cached response."""
        if key not in self._cache:
            self._misses += 1
            return None

        entry = self._cache[key]

        # Check if expired
        if entry["expires_at"] < time.time():
            del self._cache[key]
            self._misses += 1
            return None

        # Move to end (LRU)
        self._cache.move_to_end(key)
        self._hits += 1

        return self._deserialize_response(entry["data"])

    async def set(self, key: str, response: LLMResponse, ttl: Optional[int] = None) -> None:
        """Cache a response."""
        ttl = ttl or self._default_ttl

        # Evict oldest if at capacity
        while len(self._cache) >= self._max_size:
            self._cache.popitem(last=False)

        self._cache[key] = {
            "data": self._serialize_response(response),
            "expires_at": time.time() + ttl,
            "created_at": time.time(),
        }

    async def delete(self, key: str) -> None:
        """Delete a cached entry."""
        if key in self._cache:
            del self._cache[key]

    async def clear(self) -> None:
        """Clear all cached entries."""
        self._cache.clear()
        self._hits = 0
        self._misses = 0

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total = self._hits + self._misses
        hit_rate = (self._hits / total * 100) if total > 0 else 0

        return {
            "type": "memory",
            "size": len(self._cache),
            "max_size": self._max_size,
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": round(hit_rate, 2),
        }

    def _serialize_response(self, response: LLMResponse) -> Dict[str, Any]:
        """Serialize response for storage."""
        return response.to_dict()

    def _deserialize_response(self, data: Dict[str, Any]) -> LLMResponse:
        """Deserialize response from storage."""
        return LLMResponse(
            content=data["content"],
            model=data["model"],
            provider=data.get("provider", ""),
            tokens_used=data.get("tokens_used", 0),
            prompt_tokens=data.get("prompt_tokens", 0),
            completion_tokens=data.get("completion_tokens", 0),
            response_time=data.get("response_time", 0),
            finish_reason=data.get("finish_reason", "stop"),
            cost=data.get("cost", 0),
            metadata=data.get("metadata", {}),
        )


class RedisCache(CacheBackend):
    """Redis-based cache implementation."""

    def __init__(self, redis_url: str, prefix: str = "llm_router", default_ttl: int = 3600):
        self._redis_url = redis_url
        self._prefix = prefix
        self._default_ttl = default_ttl
        self._client = None
        self._hits = 0
        self._misses = 0

    async def _get_client(self):
        """Get or create Redis client."""
        if self._client is None:
            try:
                import redis.asyncio as redis
                self._client = redis.from_url(self._redis_url)
            except ImportError:
                raise ImportError("redis package required for Redis caching")
        return self._client

    def _make_key(self, key: str) -> str:
        """Create prefixed key."""
        return f"{self._prefix}:{key}"

    async def get(self, key: str) -> Optional[LLMResponse]:
        """Get a cached response."""
        try:
            client = await self._get_client()
            data = await client.get(self._make_key(key))

            if data is None:
                self._misses += 1
                return None

            self._hits += 1
            return self._deserialize_response(json.loads(data))

        except Exception as e:
            logger.warning(f"Redis get error: {e}")
            self._misses += 1
            return None

    async def set(self, key: str, response: LLMResponse, ttl: Optional[int] = None) -> None:
        """Cache a response."""
        try:
            client = await self._get_client()
            ttl = ttl or self._default_ttl
            data = json.dumps(self._serialize_response(response))
            await client.setex(self._make_key(key), ttl, data)

        except Exception as e:
            logger.warning(f"Redis set error: {e}")

    async def delete(self, key: str) -> None:
        """Delete a cached entry."""
        try:
            client = await self._get_client()
            await client.delete(self._make_key(key))
        except Exception as e:
            logger.warning(f"Redis delete error: {e}")

    async def clear(self) -> None:
        """Clear all cached entries."""
        try:
            client = await self._get_client()
            keys = await client.keys(f"{self._prefix}:*")
            if keys:
                await client.delete(*keys)
            self._hits = 0
            self._misses = 0
        except Exception as e:
            logger.warning(f"Redis clear error: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total = self._hits + self._misses
        hit_rate = (self._hits / total * 100) if total > 0 else 0

        return {
            "type": "redis",
            "url": self._redis_url.split("@")[-1] if "@" in self._redis_url else self._redis_url,
            "prefix": self._prefix,
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": round(hit_rate, 2),
        }

    def _serialize_response(self, response: LLMResponse) -> Dict[str, Any]:
        """Serialize response for storage."""
        return response.to_dict()

    def _deserialize_response(self, data: Dict[str, Any]) -> LLMResponse:
        """Deserialize response from storage."""
        return LLMResponse(
            content=data["content"],
            model=data["model"],
            provider=data.get("provider", ""),
            tokens_used=data.get("tokens_used", 0),
            prompt_tokens=data.get("prompt_tokens", 0),
            completion_tokens=data.get("completion_tokens", 0),
            response_time=data.get("response_time", 0),
            finish_reason=data.get("finish_reason", "stop"),
            cost=data.get("cost", 0),
            metadata=data.get("metadata", {}),
        )


class ResponseCache:
    """High-level cache interface for LLM responses."""

    def __init__(self, config: CacheConfig):
        self.config = config
        self._backend: Optional[CacheBackend] = None

    async def initialize(self) -> None:
        """Initialize the cache backend."""
        if self.config.backend == "redis" and self.config.redis_url:
            self._backend = RedisCache(
                redis_url=self.config.redis_url,
                prefix=self.config.cache_key_prefix,
                default_ttl=self.config.ttl_seconds,
            )
        else:
            self._backend = MemoryCache(
                max_size=self.config.max_size,
                default_ttl=self.config.ttl_seconds,
            )

        logger.info(f"Cache initialized with {self.config.backend} backend")

    async def get(self, key: str) -> Optional[LLMResponse]:
        """Get a cached response."""
        if not self._backend:
            return None
        return await self._backend.get(key)

    async def set(self, key: str, response: LLMResponse) -> None:
        """Cache a response."""
        if self._backend:
            await self._backend.set(key, response)

    async def delete(self, key: str) -> None:
        """Delete a cached entry."""
        if self._backend:
            await self._backend.delete(key)

    async def clear(self) -> None:
        """Clear all cached entries."""
        if self._backend:
            await self._backend.clear()

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        if self._backend:
            return self._backend.get_stats()
        return {"type": "none", "enabled": False}


# Factory function
async def get_cache(config: CacheConfig) -> ResponseCache:
    """Create and initialize a cache instance.

    Args:
        config: Cache configuration.

    Returns:
        Initialized ResponseCache instance.
    """
    cache = ResponseCache(config)
    await cache.initialize()
    return cache


def generate_cache_key(
    messages: list,
    model: str = "",
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
) -> str:
    """Generate a cache key for a request.

    Args:
        messages: List of messages (dicts or LLMMessage).
        model: Model name.
        temperature: Temperature setting.
        max_tokens: Max tokens setting.

    Returns:
        SHA256 hash as cache key.
    """
    # Normalize messages
    msg_data = []
    for msg in messages:
        if hasattr(msg, "to_dict"):
            msg_data.append(msg.to_dict())
        else:
            msg_data.append(msg)

    data = {
        "messages": msg_data,
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    content = json.dumps(data, sort_keys=True)
    return hashlib.sha256(content.encode()).hexdigest()
