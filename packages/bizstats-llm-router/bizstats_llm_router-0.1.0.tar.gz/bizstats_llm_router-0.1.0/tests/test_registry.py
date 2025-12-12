"""
Tests for LLM Registry.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import pytest
from bizstats_llm_router import (
    LLMRegistry,
    LLMProvider,
    SelectionStrategy,
    get_registry,
    reset_registry,
)


class TestLLMRegistry:
    """Tests for LLMRegistry class."""

    @pytest.mark.asyncio
    async def test_register_adapter(self, registry, mock_adapter):
        """Test registering an adapter."""
        registry.register("test", mock_adapter)
        assert "test" in registry.list_all()
        assert registry.get("test") is mock_adapter

    @pytest.mark.asyncio
    async def test_unregister_adapter(self, registry, mock_adapter):
        """Test unregistering an adapter."""
        registry.register("test", mock_adapter)
        registry.unregister("test")
        assert "test" not in registry.list_all()
        assert registry.get("test") is None

    @pytest.mark.asyncio
    async def test_get_nonexistent_adapter(self, registry):
        """Test getting a non-existent adapter."""
        assert registry.get("nonexistent") is None

    @pytest.mark.asyncio
    async def test_list_all(self, registry, mock_adapter):
        """Test listing all adapters."""
        registry.register("adapter1", mock_adapter)
        registry.register("adapter2", mock_adapter)
        adapters = registry.list_all()
        assert len(adapters) == 2
        assert "adapter1" in adapters
        assert "adapter2" in adapters

    @pytest.mark.asyncio
    async def test_get_available(self, registry, mock_adapter):
        """Test getting available adapters."""
        await mock_adapter.initialize()
        registry.register("test", mock_adapter)
        available = await registry.get_available()
        assert "test" in available

    @pytest.mark.asyncio
    async def test_get_by_provider(self, registry, mock_adapter):
        """Test getting adapters by provider."""
        registry.register("test", mock_adapter)
        adapters = registry.get_by_provider(LLMProvider.OPENAI)
        assert len(adapters) == 1
        assert adapters[0] is mock_adapter

    @pytest.mark.asyncio
    async def test_select_llm_least_used(self, registry, mock_adapter):
        """Test LLM selection with least_used strategy."""
        await mock_adapter.initialize()
        registry.register("test", mock_adapter)
        selected = await registry.select_llm(strategy=SelectionStrategy.LEAST_USED)
        assert selected == "test"

    @pytest.mark.asyncio
    async def test_select_llm_with_requirements(self, registry, mock_adapter):
        """Test LLM selection with requirements."""
        await mock_adapter.initialize()
        registry.register("test", mock_adapter)
        selected = await registry.select_llm(
            requirements={"provider": "openai"}
        )
        assert selected == "test"

    @pytest.mark.asyncio
    async def test_select_llm_no_available(self, registry):
        """Test LLM selection when none available."""
        selected = await registry.select_llm()
        assert selected is None

    @pytest.mark.asyncio
    async def test_routing_rules(self, registry, mock_adapter):
        """Test setting and using routing rules."""
        await mock_adapter.initialize()
        registry.register("test", mock_adapter)
        registry.set_routing_rules({"code": ["test"]})
        selected = await registry.select_llm(request_type="code")
        assert selected == "test"

    @pytest.mark.asyncio
    async def test_log_request(self, registry, mock_adapter):
        """Test logging a request."""
        registry.register("test", mock_adapter)
        registry.log_request(
            "test",
            prompt_tokens=10,
            completion_tokens=20,
            response_time=0.5,
            cost=0.001,
            success=True,
        )
        metrics = registry.get_metrics("test")
        assert metrics["requests"] == 1
        assert metrics["successful_requests"] == 1
        assert metrics["prompt_tokens"] == 10
        assert metrics["completion_tokens"] == 20
        assert metrics["total_cost"] == 0.001

    @pytest.mark.asyncio
    async def test_log_failed_request(self, registry, mock_adapter):
        """Test logging a failed request."""
        registry.register("test", mock_adapter)
        registry.log_request(
            "test",
            prompt_tokens=0,
            completion_tokens=0,
            response_time=0,
            cost=0,
            success=False,
            error="Connection timeout",
        )
        metrics = registry.get_metrics("test")
        assert metrics["failed_requests"] == 1
        assert len(metrics["errors"]) == 1

    @pytest.mark.asyncio
    async def test_get_metrics(self, registry, mock_adapter):
        """Test getting metrics."""
        registry.register("test", mock_adapter)
        registry.log_request("test", 10, 20, 0.5, 0.001, True)

        # Get all metrics
        all_metrics = registry.get_metrics()
        assert "test" in all_metrics

        # Get specific metrics
        test_metrics = registry.get_metrics("test")
        assert test_metrics["requests"] == 1

    @pytest.mark.asyncio
    async def test_reset_metrics(self, registry, mock_adapter):
        """Test resetting metrics."""
        registry.register("test", mock_adapter)
        registry.log_request("test", 10, 20, 0.5, 0.001, True)
        registry.reset_metrics("test")
        metrics = registry.get_metrics("test")
        assert metrics["requests"] == 0

    @pytest.mark.asyncio
    async def test_get_status(self, registry, mock_adapter):
        """Test getting registry status."""
        await mock_adapter.initialize()
        registry.register("test", mock_adapter)
        status = await registry.get_status()
        assert status["total_registered"] == 1
        assert status["total_available"] == 1
        assert "test" in status["available_llms"]

    @pytest.mark.asyncio
    async def test_initialize_all(self, registry, mock_adapter):
        """Test initializing all adapters."""
        registry.register("test", mock_adapter)
        await registry.initialize()
        assert mock_adapter._is_initialized

    @pytest.mark.asyncio
    async def test_cleanup_all(self, registry, mock_adapter):
        """Test cleaning up all adapters."""
        await mock_adapter.initialize()
        registry.register("test", mock_adapter)
        await registry.cleanup()
        assert not mock_adapter._is_initialized


class TestGlobalRegistry:
    """Tests for global registry functions."""

    def test_get_registry(self):
        """Test getting global registry."""
        reset_registry()
        reg = get_registry()
        assert isinstance(reg, LLMRegistry)

    def test_get_registry_singleton(self):
        """Test registry is a singleton."""
        reset_registry()
        reg1 = get_registry()
        reg2 = get_registry()
        assert reg1 is reg2

    def test_reset_registry(self):
        """Test resetting global registry."""
        reg1 = get_registry()
        reset_registry()
        reg2 = get_registry()
        assert reg1 is not reg2
