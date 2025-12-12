"""
Test configuration and fixtures for LLM Router tests.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import pytest
from typing import AsyncGenerator, List
from unittest.mock import AsyncMock, MagicMock

from bizstats_llm_router import (
    LLMAdapter,
    LLMConfig,
    LLMMessage,
    LLMResponse,
    LLMProvider,
    LLMRegistry,
    LLMRouter,
    LLMRouterSettings,
    StreamChunk,
    CapabilityType,
    PrivacyLevel,
)


@pytest.fixture
def sample_messages() -> List[LLMMessage]:
    """Create sample messages for testing."""
    return [
        LLMMessage(role="system", content="You are a helpful assistant."),
        LLMMessage(role="user", content="Hello!"),
    ]


@pytest.fixture
def sample_response() -> LLMResponse:
    """Create a sample response for testing."""
    return LLMResponse(
        content="Hello! How can I help you today?",
        model="test-model",
        provider="test",
        tokens_used=25,
        prompt_tokens=10,
        completion_tokens=15,
        response_time=0.5,
        finish_reason="stop",
        cost=0.0001,
    )


@pytest.fixture
def mock_config() -> LLMConfig:
    """Create a mock LLM configuration."""
    return LLMConfig(
        provider=LLMProvider.OPENAI,
        model_name="gpt-4",
        api_key="test-api-key",
        context_length=8192,
        temperature=0.7,
        max_tokens=1000,
        cost_per_1k_input=0.03,
        cost_per_1k_output=0.06,
        capabilities=[CapabilityType.TEXT, CapabilityType.TOOLS],
        privacy_level=PrivacyLevel.STANDARD,
        timeout=60,
        max_retries=3,
    )


class MockAdapter(LLMAdapter):
    """Mock adapter for testing."""

    def __init__(self, config: LLMConfig, response: LLMResponse = None):
        super().__init__(config)
        self._mock_response = response or LLMResponse(
            content="Mock response",
            model=config.model_name,
            provider=config.provider.value,
        )
        self._chat_called = False
        self._stream_called = False

    async def initialize(self) -> bool:
        self._is_initialized = True
        self._is_available = True
        return True

    async def cleanup(self) -> None:
        self._is_initialized = False
        self._is_available = False

    async def chat(
        self,
        messages: List[LLMMessage],
        temperature=None,
        max_tokens=None,
        **kwargs,
    ) -> LLMResponse:
        self._chat_called = True
        return self._mock_response

    async def stream_chat(
        self,
        messages: List[LLMMessage],
        temperature=None,
        max_tokens=None,
        **kwargs,
    ) -> AsyncGenerator[StreamChunk, None]:
        self._stream_called = True
        words = self._mock_response.content.split()
        for word in words:
            yield StreamChunk(
                content=word + " ",
                model=self.config.model_name,
                provider=self.config.provider.value,
            )
        yield StreamChunk(
            content="",
            model=self.config.model_name,
            provider=self.config.provider.value,
            is_final=True,
            finish_reason="stop",
        )


@pytest.fixture
def mock_adapter(mock_config: LLMConfig, sample_response: LLMResponse) -> MockAdapter:
    """Create a mock adapter for testing."""
    return MockAdapter(mock_config, sample_response)


@pytest.fixture
def registry() -> LLMRegistry:
    """Create a fresh registry for testing."""
    return LLMRegistry()


@pytest.fixture
def router_settings() -> LLMRouterSettings:
    """Create router settings for testing."""
    return LLMRouterSettings(
        default_temperature=0.7,
        default_max_tokens=2000,
        default_timeout=60,
    )


@pytest.fixture
async def router(
    registry: LLMRegistry,
    router_settings: LLMRouterSettings,
    mock_adapter: MockAdapter,
) -> LLMRouter:
    """Create a configured router for testing."""
    router = LLMRouter(settings=router_settings, registry=registry)
    registry.register("test-adapter", mock_adapter)
    await router.initialize()
    return router


@pytest.fixture
def failing_adapter(mock_config: LLMConfig) -> MockAdapter:
    """Create an adapter that fails on chat."""
    class FailingAdapter(MockAdapter):
        async def chat(self, messages, temperature=None, max_tokens=None, **kwargs):
            raise RuntimeError("Simulated failure")

        async def health_check(self) -> bool:
            return False

    return FailingAdapter(mock_config)
