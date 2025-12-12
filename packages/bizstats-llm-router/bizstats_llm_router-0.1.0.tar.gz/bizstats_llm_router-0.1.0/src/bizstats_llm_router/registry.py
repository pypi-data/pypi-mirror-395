"""
LLM Registry for managing multiple LLM adapters.

Provides centralized management, health monitoring, and metrics tracking
for all registered LLM adapters.
"""

import logging
import time
from typing import Any, Dict, List, Optional

from .base import LLMAdapter, LLMConfig
from .config import LLMProvider, SelectionStrategy

logger = logging.getLogger(__name__)


class LLMRegistry:
    """Registry for managing all available LLM adapters."""

    def __init__(self):
        self._adapters: Dict[str, LLMAdapter] = {}
        self._configs: Dict[str, LLMConfig] = {}
        self._routing_rules: Dict[str, List[str]] = {}
        self._metrics: Dict[str, Dict[str, Any]] = {}
        self._round_robin_index: Dict[str, int] = {}

    async def initialize(self) -> None:
        """Initialize all registered LLM adapters."""
        logger.info("Initializing LLM Registry...")

        for llm_id, adapter in self._adapters.items():
            try:
                success = await adapter.initialize()
                if success:
                    logger.info(f"LLM {llm_id} initialized successfully")
                else:
                    logger.warning(f"LLM {llm_id} initialization failed")
            except Exception as e:
                logger.error(f"LLM {llm_id} initialization error: {e}")

    async def cleanup(self) -> None:
        """Cleanup all registered LLM adapters."""
        logger.info("Cleaning up LLM Registry...")

        for llm_id, adapter in self._adapters.items():
            try:
                await adapter.cleanup()
                logger.info(f"LLM {llm_id} cleaned up")
            except Exception as e:
                logger.error(f"LLM {llm_id} cleanup error: {e}")

    def register(self, llm_id: str, adapter: LLMAdapter) -> None:
        """Register a new LLM adapter.

        Args:
            llm_id: Unique identifier for this LLM.
            adapter: LLMAdapter instance to register.
        """
        self._adapters[llm_id] = adapter
        self._configs[llm_id] = adapter.config
        self._metrics[llm_id] = {
            "requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_tokens": 0,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_cost": 0.0,
            "total_response_time": 0.0,
            "avg_response_time": 0.0,
            "last_used": 0,
            "errors": [],
        }
        logger.info(f"Registered LLM: {llm_id} ({adapter.config.model_name})")

    def unregister(self, llm_id: str) -> None:
        """Unregister an LLM adapter.

        Args:
            llm_id: Identifier of the LLM to unregister.
        """
        if llm_id in self._adapters:
            del self._adapters[llm_id]
            del self._configs[llm_id]
            del self._metrics[llm_id]
            logger.info(f"Unregistered LLM: {llm_id}")

    def get(self, llm_id: str) -> Optional[LLMAdapter]:
        """Get an LLM adapter by ID.

        Args:
            llm_id: Identifier of the LLM.

        Returns:
            LLMAdapter instance or None if not found.
        """
        return self._adapters.get(llm_id)

    def get_by_provider(self, provider: LLMProvider) -> List[LLMAdapter]:
        """Get all adapters for a specific provider.

        Args:
            provider: LLM provider.

        Returns:
            List of adapters for the provider.
        """
        return [
            adapter
            for adapter in self._adapters.values()
            if adapter.config.provider == provider
        ]

    def list_all(self) -> List[str]:
        """List all registered LLM IDs.

        Returns:
            List of LLM identifiers.
        """
        return list(self._adapters.keys())

    async def get_available(self) -> List[str]:
        """Get list of currently available LLM IDs.

        Returns:
            List of available LLM identifiers.
        """
        available = []
        for llm_id, adapter in self._adapters.items():
            if await adapter.health_check():
                available.append(llm_id)
        return available

    def set_routing_rules(self, rules: Dict[str, List[str]]) -> None:
        """Set routing rules for request types.

        Args:
            rules: Dictionary mapping request types to preferred LLM IDs.
        """
        self._routing_rules = rules
        logger.info(f"Set routing rules for: {list(rules.keys())}")

    async def select_llm(
        self,
        request_type: str = "general",
        requirements: Optional[Dict[str, Any]] = None,
        strategy: SelectionStrategy = SelectionStrategy.LEAST_USED,
    ) -> Optional[str]:
        """Select an LLM based on request type and requirements.

        Args:
            request_type: Type of request (e.g., "general", "code", "analysis").
            requirements: Optional requirements dictionary.
            strategy: Selection strategy to use.

        Returns:
            Selected LLM ID or None if no suitable LLM found.
        """
        requirements = requirements or {}

        # Get available LLMs
        available_llms = await self.get_available()
        if not available_llms:
            logger.warning("No LLMs available for selection")
            return None

        # Apply routing rules if defined
        if request_type in self._routing_rules:
            preferred = [
                llm_id
                for llm_id in self._routing_rules[request_type]
                if llm_id in available_llms
            ]
            if preferred:
                available_llms = preferred

        # Filter by requirements
        filtered_llms = self._filter_by_requirements(available_llms, requirements)

        if not filtered_llms:
            logger.warning(f"No LLMs match requirements: {requirements}")
            # Fall back to any available LLM
            filtered_llms = available_llms

        # Select based on strategy
        return self._select_by_strategy(filtered_llms, strategy, request_type)

    def _filter_by_requirements(
        self, llm_ids: List[str], requirements: Dict[str, Any]
    ) -> List[str]:
        """Filter LLMs by requirements.

        Args:
            llm_ids: List of LLM IDs to filter.
            requirements: Requirements dictionary.

        Returns:
            Filtered list of LLM IDs.
        """
        filtered = []

        for llm_id in llm_ids:
            config = self._configs.get(llm_id)
            if not config:
                continue

            # Check privacy level
            if requirements.get("privacy_level"):
                if config.privacy_level.value != requirements["privacy_level"]:
                    continue

            # Check capabilities
            if requirements.get("capabilities"):
                required_caps = set(requirements["capabilities"])
                available_caps = set(cap.value for cap in config.capabilities)
                if not required_caps.issubset(available_caps):
                    continue

            # Check max cost
            if requirements.get("max_cost_per_1k"):
                avg_cost = (config.cost_per_1k_input + config.cost_per_1k_output) / 2
                if avg_cost > requirements["max_cost_per_1k"]:
                    continue

            # Check min context length
            if requirements.get("min_context_length"):
                if config.context_length < requirements["min_context_length"]:
                    continue

            # Check provider
            if requirements.get("provider"):
                if config.provider.value != requirements["provider"]:
                    continue

            filtered.append(llm_id)

        return filtered

    def _select_by_strategy(
        self, llm_ids: List[str], strategy: SelectionStrategy, request_type: str
    ) -> Optional[str]:
        """Select an LLM using the specified strategy.

        Args:
            llm_ids: List of candidate LLM IDs.
            strategy: Selection strategy.
            request_type: Request type for round-robin tracking.

        Returns:
            Selected LLM ID.
        """
        if not llm_ids:
            return None

        if strategy == SelectionStrategy.LEAST_USED:
            return min(llm_ids, key=lambda x: self._metrics[x]["requests"])

        elif strategy == SelectionStrategy.FASTEST:
            return min(
                llm_ids,
                key=lambda x: self._metrics[x].get("avg_response_time", float("inf")),
            )

        elif strategy == SelectionStrategy.CHEAPEST:
            return min(
                llm_ids,
                key=lambda x: (
                    self._configs[x].cost_per_1k_input
                    + self._configs[x].cost_per_1k_output
                )
                / 2,
            )

        elif strategy == SelectionStrategy.ROUND_ROBIN:
            if request_type not in self._round_robin_index:
                self._round_robin_index[request_type] = 0
            index = self._round_robin_index[request_type] % len(llm_ids)
            self._round_robin_index[request_type] += 1
            return llm_ids[index]

        elif strategy == SelectionStrategy.PRIORITY:
            # Return first available (assumes list is priority-ordered)
            return llm_ids[0]

        elif strategy == SelectionStrategy.RANDOM:
            import random
            return random.choice(llm_ids)

        # Default: return first
        return llm_ids[0]

    def log_request(
        self,
        llm_id: str,
        prompt_tokens: int,
        completion_tokens: int,
        response_time: float,
        cost: float,
        success: bool = True,
        error: Optional[str] = None,
    ) -> None:
        """Log metrics for a request.

        Args:
            llm_id: LLM identifier.
            prompt_tokens: Number of prompt tokens.
            completion_tokens: Number of completion tokens.
            response_time: Response time in seconds.
            cost: Cost of the request.
            success: Whether the request was successful.
            error: Error message if failed.
        """
        if llm_id not in self._metrics:
            return

        metrics = self._metrics[llm_id]
        metrics["requests"] += 1
        metrics["last_used"] = time.time()

        if success:
            metrics["successful_requests"] += 1
            metrics["prompt_tokens"] += prompt_tokens
            metrics["completion_tokens"] += completion_tokens
            metrics["total_tokens"] += prompt_tokens + completion_tokens
            metrics["total_cost"] += cost
            metrics["total_response_time"] += response_time
            metrics["avg_response_time"] = (
                metrics["total_response_time"] / metrics["successful_requests"]
            )
        else:
            metrics["failed_requests"] += 1
            if error:
                metrics["errors"].append(
                    {"timestamp": time.time(), "error": error[:200]}
                )
                # Keep only last 10 errors
                metrics["errors"] = metrics["errors"][-10:]

    def get_metrics(self, llm_id: Optional[str] = None) -> Dict[str, Any]:
        """Get metrics for LLMs.

        Args:
            llm_id: Optional specific LLM ID. If None, returns all metrics.

        Returns:
            Metrics dictionary.
        """
        if llm_id:
            return self._metrics.get(llm_id, {}).copy()
        return {k: v.copy() for k, v in self._metrics.items()}

    def reset_metrics(self, llm_id: Optional[str] = None) -> None:
        """Reset metrics for LLMs.

        Args:
            llm_id: Optional specific LLM ID. If None, resets all metrics.
        """
        if llm_id:
            if llm_id in self._metrics:
                self._metrics[llm_id] = {
                    "requests": 0,
                    "successful_requests": 0,
                    "failed_requests": 0,
                    "total_tokens": 0,
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_cost": 0.0,
                    "total_response_time": 0.0,
                    "avg_response_time": 0.0,
                    "last_used": 0,
                    "errors": [],
                }
        else:
            for k in self._metrics:
                self.reset_metrics(k)

    async def get_status(self) -> Dict[str, Any]:
        """Get overall registry status.

        Returns:
            Status dictionary with registry information.
        """
        available_llms = await self.get_available()

        total_requests = sum(m["requests"] for m in self._metrics.values())
        total_cost = sum(m["total_cost"] for m in self._metrics.values())
        total_tokens = sum(m["total_tokens"] for m in self._metrics.values())

        return {
            "total_registered": len(self._adapters),
            "total_available": len(available_llms),
            "available_llms": available_llms,
            "total_requests": total_requests,
            "total_cost": round(total_cost, 6),
            "total_tokens": total_tokens,
            "routing_rules": list(self._routing_rules.keys()),
            "providers": {
                llm_id: adapter.get_capabilities()
                for llm_id, adapter in self._adapters.items()
            },
        }


# Global registry instance
_registry: Optional[LLMRegistry] = None


def get_registry() -> LLMRegistry:
    """Get the global LLM registry instance.

    Returns:
        LLMRegistry singleton instance.
    """
    global _registry
    if _registry is None:
        _registry = LLMRegistry()
    return _registry


def reset_registry() -> None:
    """Reset the global registry instance."""
    global _registry
    _registry = None
