"""
LLM Router - Main routing class with intelligent failover.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.

Provides unified interface for routing requests to multiple LLM providers
with automatic failover, retries, and cost tracking.
"""

import logging
import time
from typing import Any, AsyncGenerator, Dict, List, Optional

from tenacity import (
    AsyncRetrying,
    RetryError,
    stop_after_attempt,
    wait_exponential,
)

from .base import LLMAdapter, LLMMessage, LLMResponse, StreamChunk
from .config import (
    LLMConfig,
    LLMProvider,
    LLMRouterSettings,
    RoutingConfig,
    SelectionStrategy,
)
from .registry import LLMRegistry, get_registry

logger = logging.getLogger(__name__)


class LLMRouter:
    """
    Main LLM Router class for intelligent request routing.

    Features:
    - Multi-provider support with unified interface
    - Automatic failover when providers fail
    - Configurable retry policies
    - Cost tracking and optimization
    - Request/response caching
    - Rate limiting
    """

    def __init__(
        self,
        settings: Optional[LLMRouterSettings] = None,
        registry: Optional[LLMRegistry] = None,
    ):
        """Initialize the LLM Router.

        Args:
            settings: Router settings. Uses defaults if not provided.
            registry: LLM registry. Uses global instance if not provided.
        """
        self.settings = settings or LLMRouterSettings()
        self.registry = registry or get_registry()
        self._cache: Optional[Any] = None
        self._rate_limiter: Optional[Any] = None
        self._cost_tracker: Optional[Any] = None
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize the router and all registered adapters."""
        if self._initialized:
            return

        logger.info("Initializing LLM Router...")

        # Initialize registry
        await self.registry.initialize()

        # Set up caching if enabled
        if self.settings.cache.enabled:
            await self._setup_cache()

        # Set up rate limiting if enabled
        if self.settings.rate_limit.enabled:
            await self._setup_rate_limiter()

        # Set up cost tracking if enabled
        if self.settings.cost_tracking.enabled:
            await self._setup_cost_tracker()

        self._initialized = True
        logger.info("LLM Router initialized successfully")

    async def cleanup(self) -> None:
        """Cleanup router resources."""
        logger.info("Cleaning up LLM Router...")
        await self.registry.cleanup()
        self._initialized = False

    def register_adapter(self, llm_id: str, adapter: LLMAdapter) -> None:
        """Register an LLM adapter.

        Args:
            llm_id: Unique identifier for the adapter.
            adapter: LLMAdapter instance.
        """
        self.registry.register(llm_id, adapter)

    def unregister_adapter(self, llm_id: str) -> None:
        """Unregister an LLM adapter.

        Args:
            llm_id: Identifier of the adapter to remove.
        """
        self.registry.unregister(llm_id)

    async def chat(
        self,
        messages: List[LLMMessage],
        llm_id: Optional[str] = None,
        provider: Optional[LLMProvider] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        request_type: str = "general",
        requirements: Optional[Dict[str, Any]] = None,
        enable_failover: bool = True,
        **kwargs: Any,
    ) -> LLMResponse:
        """Send a chat request to an LLM.

        Args:
            messages: List of conversation messages.
            llm_id: Specific LLM ID to use. If None, uses routing.
            provider: Specific provider to use. If None, uses routing.
            temperature: Override default temperature.
            max_tokens: Override default max tokens.
            request_type: Type of request for routing.
            requirements: Requirements for LLM selection.
            enable_failover: Whether to enable failover on failure.
            **kwargs: Additional provider-specific parameters.

        Returns:
            LLMResponse from the selected LLM.

        Raises:
            RuntimeError: If no LLM is available or all attempts fail.
        """
        if not self._initialized:
            await self.initialize()

        # Check rate limit
        if self._rate_limiter:
            await self._check_rate_limit()

        # Check cache
        cache_key = None
        if self._cache and self.settings.cache.enabled:
            cache_key = self._generate_cache_key(messages, temperature, max_tokens)
            cached = await self._get_cached(cache_key)
            if cached:
                logger.debug("Cache hit for request")
                return cached

        # Select LLM
        selected_llm_id = await self._select_llm(
            llm_id, provider, request_type, requirements
        )

        if not selected_llm_id:
            raise RuntimeError("No LLM available for request")

        # Get fallback LLMs for failover
        fallback_llms = []
        if enable_failover and self.settings.routing.enable_failover:
            fallback_llms = await self._get_fallback_llms(
                selected_llm_id, request_type, requirements
            )

        # Execute with retries and failover
        response = await self._execute_with_failover(
            selected_llm_id,
            fallback_llms,
            messages,
            temperature,
            max_tokens,
            **kwargs,
        )

        # Cache response
        if cache_key and self._cache:
            await self._set_cached(cache_key, response)

        return response

    async def stream_chat(
        self,
        messages: List[LLMMessage],
        llm_id: Optional[str] = None,
        provider: Optional[LLMProvider] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        request_type: str = "general",
        requirements: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> AsyncGenerator[StreamChunk, None]:
        """Stream a chat response from an LLM.

        Args:
            messages: List of conversation messages.
            llm_id: Specific LLM ID to use.
            provider: Specific provider to use.
            temperature: Override default temperature.
            max_tokens: Override default max tokens.
            request_type: Type of request for routing.
            requirements: Requirements for LLM selection.
            **kwargs: Additional provider-specific parameters.

        Yields:
            StreamChunk objects with partial content.
        """
        if not self._initialized:
            await self.initialize()

        # Check rate limit
        if self._rate_limiter:
            await self._check_rate_limit()

        # Select LLM
        selected_llm_id = await self._select_llm(
            llm_id, provider, request_type, requirements
        )

        if not selected_llm_id:
            yield StreamChunk(
                content="Error: No LLM available",
                model="",
                is_final=True,
                finish_reason="error",
            )
            return

        adapter = self.registry.get(selected_llm_id)
        if not adapter:
            yield StreamChunk(
                content="Error: Adapter not found",
                model="",
                is_final=True,
                finish_reason="error",
            )
            return

        start_time = time.time()
        total_content = ""

        try:
            async for chunk in adapter.stream_chat(
                messages, temperature, max_tokens, **kwargs
            ):
                total_content += chunk.content
                yield chunk

            # Log successful request
            response_time = time.time() - start_time
            # Estimate tokens (rough)
            prompt_tokens = sum(len(m.content.split()) for m in messages)
            completion_tokens = len(total_content.split())
            cost = adapter.calculate_cost(prompt_tokens, completion_tokens)

            self.registry.log_request(
                selected_llm_id,
                prompt_tokens,
                completion_tokens,
                response_time,
                cost,
                success=True,
            )

        except Exception as e:
            logger.error(f"Stream error from {selected_llm_id}: {e}")
            self.registry.log_request(
                selected_llm_id, 0, 0, 0, 0, success=False, error=str(e)
            )
            yield StreamChunk(
                content=f"Error: {str(e)}",
                model=adapter.model_name,
                provider=adapter.provider_name,
                is_final=True,
                finish_reason="error",
            )

    async def _select_llm(
        self,
        llm_id: Optional[str],
        provider: Optional[LLMProvider],
        request_type: str,
        requirements: Optional[Dict[str, Any]],
    ) -> Optional[str]:
        """Select an LLM based on parameters.

        Args:
            llm_id: Specific LLM ID if provided.
            provider: Specific provider if provided.
            request_type: Request type for routing.
            requirements: Additional requirements.

        Returns:
            Selected LLM ID or None.
        """
        # Use specific LLM if provided
        if llm_id:
            adapter = self.registry.get(llm_id)
            if adapter and await adapter.health_check():
                return llm_id
            logger.warning(f"Requested LLM {llm_id} not available")

        # Use provider-specific LLM
        if provider:
            adapters = self.registry.get_by_provider(provider)
            for adapter in adapters:
                if await adapter.health_check():
                    # Find the ID for this adapter
                    for lid, a in self.registry._adapters.items():
                        if a is adapter:
                            return lid

        # Use routing to select
        requirements = requirements or {}
        return await self.registry.select_llm(
            request_type,
            requirements,
            self.settings.routing.selection_strategy,
        )

    async def _get_fallback_llms(
        self,
        primary_llm: str,
        request_type: str,
        requirements: Optional[Dict[str, Any]],
    ) -> List[str]:
        """Get list of fallback LLMs.

        Args:
            primary_llm: Primary LLM ID to exclude.
            request_type: Request type.
            requirements: Requirements for selection.

        Returns:
            List of fallback LLM IDs.
        """
        available = await self.registry.get_available()
        fallbacks = [llm_id for llm_id in available if llm_id != primary_llm]

        # Limit to configured max attempts
        max_fallbacks = self.settings.routing.max_failover_attempts - 1
        return fallbacks[:max_fallbacks]

    async def _execute_with_failover(
        self,
        primary_llm: str,
        fallback_llms: List[str],
        messages: List[LLMMessage],
        temperature: Optional[float],
        max_tokens: Optional[int],
        **kwargs: Any,
    ) -> LLMResponse:
        """Execute request with retries and failover.

        Args:
            primary_llm: Primary LLM ID.
            fallback_llms: List of fallback LLM IDs.
            messages: Chat messages.
            temperature: Temperature override.
            max_tokens: Max tokens override.
            **kwargs: Additional parameters.

        Returns:
            LLMResponse from successful execution.

        Raises:
            RuntimeError: If all attempts fail.
        """
        all_llms = [primary_llm] + fallback_llms
        last_error = None

        for llm_id in all_llms:
            adapter = self.registry.get(llm_id)
            if not adapter:
                continue

            try:
                # Try with retries
                response = await self._execute_with_retries(
                    adapter, messages, temperature, max_tokens, **kwargs
                )

                # Log success
                self.registry.log_request(
                    llm_id,
                    response.prompt_tokens,
                    response.completion_tokens,
                    response.response_time,
                    response.cost,
                    success=True,
                )

                # Track cost
                if self._cost_tracker:
                    await self._track_cost(response.cost)

                return response

            except Exception as e:
                last_error = e
                logger.warning(f"Failed with {llm_id}: {e}, trying next...")
                self.registry.log_request(
                    llm_id, 0, 0, 0, 0, success=False, error=str(e)
                )

        raise RuntimeError(f"All LLM attempts failed. Last error: {last_error}")

    async def _execute_with_retries(
        self,
        adapter: LLMAdapter,
        messages: List[LLMMessage],
        temperature: Optional[float],
        max_tokens: Optional[int],
        **kwargs: Any,
    ) -> LLMResponse:
        """Execute request with retry logic.

        Args:
            adapter: LLM adapter to use.
            messages: Chat messages.
            temperature: Temperature override.
            max_tokens: Max tokens override.
            **kwargs: Additional parameters.

        Returns:
            LLMResponse from successful execution.
        """
        start_time = time.time()

        try:
            async for attempt in AsyncRetrying(
                stop=stop_after_attempt(adapter.config.max_retries),
                wait=wait_exponential(
                    multiplier=adapter.config.retry_delay, min=1, max=10
                ),
                reraise=True,
            ):
                with attempt:
                    response = await adapter.chat(
                        messages, temperature, max_tokens, **kwargs
                    )
                    response.response_time = time.time() - start_time
                    response.provider = adapter.provider_name

                    # Calculate cost
                    response.cost = adapter.calculate_cost(
                        response.prompt_tokens, response.completion_tokens
                    )

                    return response

        except RetryError as e:
            raise e.last_attempt.exception()

        # This should not be reached, but just in case
        raise RuntimeError("Unexpected execution path")

    async def _setup_cache(self) -> None:
        """Set up response caching."""
        # Import cache implementation
        try:
            from .caching import get_cache

            self._cache = await get_cache(self.settings.cache)
            logger.info("Response caching enabled")
        except ImportError:
            logger.warning("Caching module not available")

    async def _setup_rate_limiter(self) -> None:
        """Set up rate limiting."""
        try:
            from .rate_limiting import get_rate_limiter

            self._rate_limiter = get_rate_limiter(self.settings.rate_limit)
            logger.info("Rate limiting enabled")
        except ImportError:
            logger.warning("Rate limiting module not available")

    async def _setup_cost_tracker(self) -> None:
        """Set up cost tracking."""
        try:
            from .cost_tracking import get_cost_tracker

            self._cost_tracker = get_cost_tracker(self.settings.cost_tracking)
            logger.info("Cost tracking enabled")
        except ImportError:
            logger.warning("Cost tracking module not available")

    def _generate_cache_key(
        self,
        messages: List[LLMMessage],
        temperature: Optional[float],
        max_tokens: Optional[int],
    ) -> str:
        """Generate cache key for request."""
        import hashlib
        import json

        data = {
            "messages": [m.to_dict() for m in messages],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        content = json.dumps(data, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()

    async def _get_cached(self, key: str) -> Optional[LLMResponse]:
        """Get cached response."""
        if not self._cache:
            return None
        return await self._cache.get(key)

    async def _set_cached(self, key: str, response: LLMResponse) -> None:
        """Cache a response."""
        if self._cache:
            await self._cache.set(key, response)

    async def _check_rate_limit(self) -> None:
        """Check and enforce rate limits."""
        if self._rate_limiter:
            await self._rate_limiter.check()

    async def _track_cost(self, cost: float) -> None:
        """Track request cost."""
        if self._cost_tracker:
            await self._cost_tracker.track(cost)

    def get_metrics(self) -> Dict[str, Any]:
        """Get router metrics.

        Returns:
            Dictionary with metrics from all components.
        """
        metrics = {
            "registry": self.registry.get_metrics(),
        }

        if self._cost_tracker:
            metrics["costs"] = self._cost_tracker.get_summary()

        if self._rate_limiter:
            metrics["rate_limits"] = self._rate_limiter.get_status()

        return metrics

    async def get_status(self) -> Dict[str, Any]:
        """Get router status.

        Returns:
            Dictionary with router status information.
        """
        return {
            "initialized": self._initialized,
            "cache_enabled": self._cache is not None,
            "rate_limit_enabled": self._rate_limiter is not None,
            "cost_tracking_enabled": self._cost_tracker is not None,
            "registry": await self.registry.get_status(),
        }


# Convenience function
def create_router(settings: Optional[LLMRouterSettings] = None) -> LLMRouter:
    """Create a new LLM Router instance.

    Args:
        settings: Optional router settings.

    Returns:
        Configured LLMRouter instance.
    """
    return LLMRouter(settings)
