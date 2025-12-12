"""
Tests for rate limiting.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import pytest
from bizstats_llm_router import (
    RateLimitConfig,
    RateLimiter,
    RateLimitExceeded,
    get_rate_limiter,
)
from bizstats_llm_router.rate_limiting import RateLimitBucket


class TestRateLimitBucket:
    """Tests for RateLimitBucket."""

    def test_initial_tokens(self):
        """Test initial token count equals capacity."""
        bucket = RateLimitBucket(capacity=10)
        assert bucket.tokens == 10

    def test_consume_success(self):
        """Test successful token consumption."""
        bucket = RateLimitBucket(capacity=10)
        assert bucket.consume(5) is True
        assert bucket.tokens == 5

    def test_consume_fail(self):
        """Test failed token consumption."""
        bucket = RateLimitBucket(capacity=5)
        bucket.tokens = 3
        assert bucket.consume(5) is False
        # Tokens may have slightly increased due to refill, use approx
        assert bucket.tokens == pytest.approx(3, abs=0.1)  # Unchanged (within tolerance)

    def test_time_until_available(self):
        """Test time calculation until tokens available."""
        bucket = RateLimitBucket(capacity=10, refill_rate=1.0)
        bucket.tokens = 0
        bucket.last_update = bucket.last_update  # Reset time

        wait_time = bucket.time_until_available(5)
        assert wait_time > 0


class TestRateLimiter:
    """Tests for RateLimiter."""

    @pytest.fixture
    def enabled_config(self):
        return RateLimitConfig(
            enabled=True,
            requests_per_minute=60,
            tokens_per_minute=10000,
            burst_size=10,
        )

    @pytest.fixture
    def disabled_config(self):
        return RateLimitConfig(enabled=False)

    @pytest.mark.asyncio
    async def test_disabled_limiter(self, disabled_config):
        """Test disabled rate limiter allows everything."""
        limiter = RateLimiter(disabled_config)
        # Should not raise
        await limiter.check()

    @pytest.mark.asyncio
    async def test_check_within_limit(self, enabled_config):
        """Test check within rate limit."""
        limiter = RateLimiter(enabled_config)
        # Should not raise
        await limiter.check()
        await limiter.check()

    @pytest.mark.asyncio
    async def test_check_exceeds_limit(self):
        """Test check exceeding rate limit."""
        config = RateLimitConfig(
            enabled=True,
            requests_per_minute=60,
            burst_size=2,  # Only allow 2 burst
        )
        limiter = RateLimiter(config)

        # Use up burst
        await limiter.check()
        await limiter.check()

        # Third should fail
        with pytest.raises(RateLimitExceeded):
            await limiter.check()

    @pytest.mark.asyncio
    async def test_provider_specific_limits(self):
        """Test provider-specific rate limits."""
        config = RateLimitConfig(
            enabled=True,
            requests_per_minute=60,
            burst_size=10,
            per_provider_limits={
                "openai": {"requests_per_minute": 60, "burst_size": 1},
            },
        )
        limiter = RateLimiter(config)

        # First request to openai OK
        await limiter.check(provider="openai")

        # Second request to openai should fail
        with pytest.raises(RateLimitExceeded):
            await limiter.check(provider="openai")

        # But other providers still OK
        await limiter.check(provider="anthropic")

    @pytest.mark.asyncio
    async def test_get_status(self, enabled_config):
        """Test getting rate limiter status."""
        limiter = RateLimiter(enabled_config)
        await limiter.check()

        status = limiter.get_status()
        assert status["enabled"] is True
        assert status["total_requests"] == 1
        assert status["rejected_requests"] == 0
        assert "request_bucket" in status

    @pytest.mark.asyncio
    async def test_reset(self, enabled_config):
        """Test resetting rate limiter."""
        limiter = RateLimiter(enabled_config)
        await limiter.check()
        await limiter.check()

        limiter.reset()
        status = limiter.get_status()
        assert status["total_requests"] == 0


class TestRateLimitExceeded:
    """Tests for RateLimitExceeded exception."""

    def test_exception_message(self):
        """Test exception has message."""
        exc = RateLimitExceeded("Rate limit exceeded", retry_after=5.0)
        assert "Rate limit exceeded" in str(exc)
        assert exc.retry_after == 5.0

    def test_exception_default_retry(self):
        """Test exception default retry_after."""
        exc = RateLimitExceeded("Error")
        assert exc.retry_after == 0


class TestGetRateLimiter:
    """Tests for get_rate_limiter factory function."""

    def test_create_enabled_limiter(self):
        """Test creating enabled rate limiter."""
        config = RateLimitConfig(enabled=True)
        limiter = get_rate_limiter(config)
        assert isinstance(limiter, RateLimiter)
        assert limiter.config.enabled is True

    def test_create_disabled_limiter(self):
        """Test creating disabled rate limiter."""
        config = RateLimitConfig(enabled=False)
        limiter = get_rate_limiter(config)
        assert limiter.config.enabled is False
