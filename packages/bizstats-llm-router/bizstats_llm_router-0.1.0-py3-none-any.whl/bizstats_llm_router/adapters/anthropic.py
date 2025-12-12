"""
Anthropic Claude LLM Adapter.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.

Integrates Anthropic Claude models with the LLM Router.
"""

import json
import logging
import time
from typing import Any, AsyncGenerator, List, Optional

import aiohttp

from ..base import LLMAdapter, LLMMessage, LLMResponse, StreamChunk
from ..config import LLMConfig

logger = logging.getLogger(__name__)


class AnthropicAdapter(LLMAdapter):
    """Anthropic Claude LLM adapter."""

    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self._session: Optional[aiohttp.ClientSession] = None
        self._api_key = config.api_key
        self._base_url = config.api_base or "https://api.anthropic.com"
        self._api_version = "2023-06-01"

    async def initialize(self) -> bool:
        """Initialize the Anthropic adapter."""
        try:
            if not self._api_key:
                logger.error("Anthropic API key is required")
                return False

            headers = {
                "x-api-key": self._api_key,
                "anthropic-version": self._api_version,
                "Content-Type": "application/json",
            }

            self._session = aiohttp.ClientSession(
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=self.config.timeout),
            )

            self._is_initialized = True
            self._is_available = True
            logger.info(f"Anthropic adapter initialized for {self.config.model_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize Anthropic adapter: {e}")
            self._is_available = False
            return False

    async def cleanup(self) -> None:
        """Cleanup Anthropic connection."""
        if self._session:
            await self._session.close()
            self._session = None

    async def chat(
        self,
        messages: List[LLMMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> LLMResponse:
        """Send chat messages to Anthropic."""
        if not self._session or not self._is_available:
            raise RuntimeError("Anthropic adapter not initialized")

        start_time = time.time()

        try:
            # Extract system message and convert others
            system_message = None
            anthropic_messages = []

            for msg in messages:
                if msg.role == "system":
                    system_message = msg.content
                else:
                    anthropic_messages.append({
                        "role": msg.role,
                        "content": msg.content,
                    })

            # Prepare request
            request_data = {
                "model": self.config.model_name,
                "messages": anthropic_messages,
                "max_tokens": self._get_max_tokens(max_tokens),
            }

            if system_message:
                request_data["system"] = system_message

            # Temperature is optional for Anthropic
            temp = self._get_temperature(temperature)
            if temp != 1.0:  # Only include if not default
                request_data["temperature"] = temp

            if kwargs:
                request_data.update(kwargs)

            # Send request
            async with self._session.post(
                f"{self._base_url}/v1/messages",
                json=request_data,
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise RuntimeError(f"Anthropic API error {response.status}: {error_text}")

                data = await response.json()

                # Extract response
                content_blocks = data.get("content", [])
                content = "".join(
                    block.get("text", "")
                    for block in content_blocks
                    if block.get("type") == "text"
                )

                usage = data.get("usage", {})
                prompt_tokens = usage.get("input_tokens", 0)
                completion_tokens = usage.get("output_tokens", 0)

                response_time = time.time() - start_time

                return LLMResponse(
                    content=content,
                    model=data.get("model", self.config.model_name),
                    provider="anthropic",
                    tokens_used=prompt_tokens + completion_tokens,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    response_time=response_time,
                    finish_reason=data.get("stop_reason", "end_turn"),
                    cost=self.calculate_cost(prompt_tokens, completion_tokens),
                    metadata={
                        "id": data.get("id"),
                        "type": data.get("type"),
                    },
                )

        except Exception as e:
            logger.error(f"Anthropic chat error: {e}")
            raise

    async def stream_chat(
        self,
        messages: List[LLMMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> AsyncGenerator[StreamChunk, None]:
        """Stream chat response from Anthropic."""
        if not self._session or not self._is_available:
            raise RuntimeError("Anthropic adapter not initialized")

        try:
            # Extract system message and convert others
            system_message = None
            anthropic_messages = []

            for msg in messages:
                if msg.role == "system":
                    system_message = msg.content
                else:
                    anthropic_messages.append({
                        "role": msg.role,
                        "content": msg.content,
                    })

            # Prepare request
            request_data = {
                "model": self.config.model_name,
                "messages": anthropic_messages,
                "max_tokens": self._get_max_tokens(max_tokens),
                "stream": True,
            }

            if system_message:
                request_data["system"] = system_message

            temp = self._get_temperature(temperature)
            if temp != 1.0:
                request_data["temperature"] = temp

            if kwargs:
                request_data.update(kwargs)

            # Send streaming request
            async with self._session.post(
                f"{self._base_url}/v1/messages",
                json=request_data,
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise RuntimeError(f"Anthropic API error {response.status}: {error_text}")

                # Stream response
                async for line in response.content:
                    line_text = line.decode("utf-8").strip()

                    if line_text.startswith("data: "):
                        line_text = line_text[6:]

                        try:
                            data = json.loads(line_text)
                            event_type = data.get("type")

                            if event_type == "content_block_delta":
                                delta = data.get("delta", {})
                                if delta.get("type") == "text_delta":
                                    text = delta.get("text", "")
                                    if text:
                                        yield StreamChunk(
                                            content=text,
                                            model=self.config.model_name,
                                            provider="anthropic",
                                        )

                            elif event_type == "message_stop":
                                yield StreamChunk(
                                    content="",
                                    model=self.config.model_name,
                                    provider="anthropic",
                                    is_final=True,
                                    finish_reason="end_turn",
                                )
                                break

                        except json.JSONDecodeError:
                            continue

        except Exception as e:
            logger.error(f"Anthropic stream error: {e}")
            raise


def create_anthropic_adapter(
    model_name: str,
    api_key: str,
    **kwargs: Any,
) -> AnthropicAdapter:
    """Create an Anthropic adapter with common configurations.

    Args:
        model_name: Claude model name.
        api_key: Anthropic API key.
        **kwargs: Additional configuration options.

    Returns:
        Configured AnthropicAdapter instance.
    """
    from ..config import CapabilityType, DEFAULT_MODEL_CONFIGS, LLMProvider, PrivacyLevel

    model_defaults = DEFAULT_MODEL_CONFIGS.get("anthropic", {}).get(model_name, {})

    config = LLMConfig(
        provider=LLMProvider.ANTHROPIC,
        model_name=model_name,
        api_key=api_key,
        context_length=model_defaults.get("context_length", 200000),
        capabilities=model_defaults.get("capabilities", [CapabilityType.TEXT]),
        cost_per_1k_input=model_defaults.get("cost_per_1k_input", 0.003),
        cost_per_1k_output=model_defaults.get("cost_per_1k_output", 0.015),
        specialization=model_defaults.get("specialization", "balanced"),
        privacy_level=PrivacyLevel.STANDARD,
        **kwargs,
    )

    return AnthropicAdapter(config)
