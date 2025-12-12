"""
Rate Limiting for LLM Router.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.

Provides rate limiting to prevent API abuse and manage costs.
"""

import asyncio
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from .config import RateLimitConfig

logger = logging.getLogger(__name__)


@dataclass
class RateLimitBucket:
    """Token bucket for rate limiting."""

    capacity: int
    tokens: float = field(default=0)
    last_update: float = field(default_factory=time.time)
    refill_rate: float = field(default=1.0)  # tokens per second

    def __post_init__(self):
        self.tokens = float(self.capacity)

    def consume(self, tokens: int = 1) -> bool:
        """Try to consume tokens from the bucket.

        Args:
            tokens: Number of tokens to consume.

        Returns:
            True if tokens were consumed, False if not enough tokens.
        """
        self._refill()

        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def _refill(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_update
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_update = now

    def time_until_available(self, tokens: int = 1) -> float:
        """Calculate time until tokens are available.

        Args:
            tokens: Number of tokens needed.

        Returns:
            Time in seconds until tokens are available.
        """
        self._refill()

        if self.tokens >= tokens:
            return 0

        needed = tokens - self.tokens
        return needed / self.refill_rate


class RateLimitExceeded(Exception):
    """Exception raised when rate limit is exceeded."""

    def __init__(self, message: str, retry_after: float = 0):
        super().__init__(message)
        self.retry_after = retry_after


class RateLimiter:
    """Rate limiter for LLM requests."""

    def __init__(self, config: RateLimitConfig):
        self.config = config
        self._request_bucket: Optional[RateLimitBucket] = None
        self._token_bucket: Optional[RateLimitBucket] = None
        self._provider_buckets: Dict[str, RateLimitBucket] = {}
        self._total_requests = 0
        self._rejected_requests = 0

        if config.enabled:
            self._initialize_buckets()

    def _initialize_buckets(self) -> None:
        """Initialize rate limit buckets."""
        # Request rate bucket
        self._request_bucket = RateLimitBucket(
            capacity=self.config.burst_size,
            refill_rate=self.config.requests_per_minute / 60.0,
        )

        # Token rate bucket
        self._token_bucket = RateLimitBucket(
            capacity=self.config.tokens_per_minute,
            refill_rate=self.config.tokens_per_minute / 60.0,
        )

        # Per-provider buckets
        for provider, limits in self.config.per_provider_limits.items():
            self._provider_buckets[provider] = RateLimitBucket(
                capacity=limits.get("burst_size", self.config.burst_size),
                refill_rate=limits.get("requests_per_minute", self.config.requests_per_minute) / 60.0,
            )

    async def check(self, provider: Optional[str] = None, tokens: int = 0) -> None:
        """Check if request is allowed under rate limits.

        Args:
            provider: Optional provider name for provider-specific limits.
            tokens: Estimated tokens for the request.

        Raises:
            RateLimitExceeded: If rate limit is exceeded.
        """
        if not self.config.enabled:
            return

        self._total_requests += 1

        # Check request rate
        if self._request_bucket and not self._request_bucket.consume(1):
            self._rejected_requests += 1
            retry_after = self._request_bucket.time_until_available(1)
            raise RateLimitExceeded(
                f"Request rate limit exceeded. Try again in {retry_after:.1f}s",
                retry_after=retry_after,
            )

        # Check token rate
        if tokens > 0 and self._token_bucket and not self._token_bucket.consume(tokens):
            self._rejected_requests += 1
            retry_after = self._token_bucket.time_until_available(tokens)
            raise RateLimitExceeded(
                f"Token rate limit exceeded. Try again in {retry_after:.1f}s",
                retry_after=retry_after,
            )

        # Check provider-specific rate
        if provider and provider in self._provider_buckets:
            bucket = self._provider_buckets[provider]
            if not bucket.consume(1):
                self._rejected_requests += 1
                retry_after = bucket.time_until_available(1)
                raise RateLimitExceeded(
                    f"Provider {provider} rate limit exceeded. Try again in {retry_after:.1f}s",
                    retry_after=retry_after,
                )

    async def wait_if_needed(self, provider: Optional[str] = None, tokens: int = 0) -> float:
        """Wait if rate limited, then proceed.

        Args:
            provider: Optional provider name.
            tokens: Estimated tokens.

        Returns:
            Time waited in seconds.
        """
        if not self.config.enabled:
            return 0

        max_wait = 0

        # Calculate wait times
        if self._request_bucket:
            wait = self._request_bucket.time_until_available(1)
            max_wait = max(max_wait, wait)

        if tokens > 0 and self._token_bucket:
            wait = self._token_bucket.time_until_available(tokens)
            max_wait = max(max_wait, wait)

        if provider and provider in self._provider_buckets:
            bucket = self._provider_buckets[provider]
            wait = bucket.time_until_available(1)
            max_wait = max(max_wait, wait)

        # Wait if needed
        if max_wait > 0:
            logger.info(f"Rate limited, waiting {max_wait:.1f}s")
            await asyncio.sleep(max_wait)

        # Now check (consume tokens)
        await self.check(provider, tokens)
        return max_wait

    def get_status(self) -> Dict[str, Any]:
        """Get rate limiter status.

        Returns:
            Status dictionary.
        """
        status = {
            "enabled": self.config.enabled,
            "total_requests": self._total_requests,
            "rejected_requests": self._rejected_requests,
            "rejection_rate": (
                round(self._rejected_requests / self._total_requests * 100, 2)
                if self._total_requests > 0
                else 0
            ),
        }

        if self._request_bucket:
            status["request_bucket"] = {
                "capacity": self._request_bucket.capacity,
                "available": round(self._request_bucket.tokens, 1),
                "refill_rate": round(self._request_bucket.refill_rate * 60, 1),  # per minute
            }

        if self._token_bucket:
            status["token_bucket"] = {
                "capacity": self._token_bucket.capacity,
                "available": round(self._token_bucket.tokens, 1),
                "refill_rate": round(self._token_bucket.refill_rate * 60, 1),
            }

        if self._provider_buckets:
            status["provider_buckets"] = {
                provider: {
                    "available": round(bucket.tokens, 1),
                    "capacity": bucket.capacity,
                }
                for provider, bucket in self._provider_buckets.items()
            }

        return status

    def reset(self) -> None:
        """Reset rate limiter state."""
        self._total_requests = 0
        self._rejected_requests = 0
        if self.config.enabled:
            self._initialize_buckets()


def get_rate_limiter(config: RateLimitConfig) -> RateLimiter:
    """Create a rate limiter instance.

    Args:
        config: Rate limit configuration.

    Returns:
        Configured RateLimiter instance.
    """
    return RateLimiter(config)
