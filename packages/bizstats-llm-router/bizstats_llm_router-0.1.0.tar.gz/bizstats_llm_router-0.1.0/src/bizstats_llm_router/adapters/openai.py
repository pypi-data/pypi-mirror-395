"""
OpenAI LLM Adapter.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.

Integrates OpenAI models (GPT-4, GPT-4o, GPT-3.5) with the LLM Router.
"""

import json
import logging
import time
from typing import Any, AsyncGenerator, List, Optional

import aiohttp

from ..base import LLMAdapter, LLMMessage, LLMResponse, StreamChunk
from ..config import LLMConfig

logger = logging.getLogger(__name__)


class OpenAIAdapter(LLMAdapter):
    """OpenAI LLM adapter using direct API calls."""

    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self._session: Optional[aiohttp.ClientSession] = None
        self._api_key = config.api_key
        self._base_url = config.api_base or "https://api.openai.com/v1"

    async def initialize(self) -> bool:
        """Initialize the OpenAI adapter."""
        try:
            if not self._api_key:
                logger.error("OpenAI API key is required")
                return False

            headers = {
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            }

            self._session = aiohttp.ClientSession(
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=self.config.timeout),
            )

            # Verify API connection
            async with self._session.get(f"{self._base_url}/models") as response:
                if response.status == 200:
                    self._is_initialized = True
                    self._is_available = True
                    logger.info(f"OpenAI adapter initialized for {self.config.model_name}")
                    return True
                else:
                    logger.error(f"OpenAI API returned {response.status}")
                    return False

        except Exception as e:
            logger.error(f"Failed to initialize OpenAI adapter: {e}")
            self._is_available = False
            return False

    async def cleanup(self) -> None:
        """Cleanup OpenAI connection."""
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
        """Send chat messages to OpenAI."""
        if not self._session or not self._is_available:
            raise RuntimeError("OpenAI adapter not initialized")

        start_time = time.time()

        try:
            # Convert messages to OpenAI format
            openai_messages = [
                {"role": msg.role, "content": msg.content}
                for msg in messages
            ]

            # Prepare request
            request_data = {
                "model": self.config.model_name,
                "messages": openai_messages,
                "temperature": self._get_temperature(temperature),
                "max_tokens": self._get_max_tokens(max_tokens),
                "stream": False,
            }

            # Add any extra parameters
            if kwargs:
                request_data.update(kwargs)

            # Send request
            async with self._session.post(
                f"{self._base_url}/chat/completions",
                json=request_data,
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    try:
                        error_data = json.loads(error_text)
                        error_msg = error_data.get("error", {}).get("message", error_text)
                    except json.JSONDecodeError:
                        error_msg = error_text
                    raise RuntimeError(f"OpenAI API error {response.status}: {error_msg}")

                data = await response.json()

                # Extract response
                choice = data.get("choices", [{}])[0]
                content = choice.get("message", {}).get("content", "")
                finish_reason = choice.get("finish_reason", "stop")

                usage = data.get("usage", {})
                prompt_tokens = usage.get("prompt_tokens", 0)
                completion_tokens = usage.get("completion_tokens", 0)

                response_time = time.time() - start_time

                return LLMResponse(
                    content=content,
                    model=data.get("model", self.config.model_name),
                    provider="openai",
                    tokens_used=prompt_tokens + completion_tokens,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    response_time=response_time,
                    finish_reason=finish_reason,
                    cost=self.calculate_cost(prompt_tokens, completion_tokens),
                    metadata={
                        "system_fingerprint": data.get("system_fingerprint"),
                        "created": data.get("created"),
                        "id": data.get("id"),
                    },
                )

        except Exception as e:
            logger.error(f"OpenAI chat error: {e}")
            raise

    async def stream_chat(
        self,
        messages: List[LLMMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> AsyncGenerator[StreamChunk, None]:
        """Stream chat response from OpenAI."""
        if not self._session or not self._is_available:
            raise RuntimeError("OpenAI adapter not initialized")

        try:
            # Convert messages to OpenAI format
            openai_messages = [
                {"role": msg.role, "content": msg.content}
                for msg in messages
            ]

            # Prepare request
            request_data = {
                "model": self.config.model_name,
                "messages": openai_messages,
                "temperature": self._get_temperature(temperature),
                "max_tokens": self._get_max_tokens(max_tokens),
                "stream": True,
            }

            if kwargs:
                request_data.update(kwargs)

            # Send streaming request
            async with self._session.post(
                f"{self._base_url}/chat/completions",
                json=request_data,
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise RuntimeError(f"OpenAI API error {response.status}: {error_text}")

                # Stream response
                async for line in response.content:
                    line_text = line.decode("utf-8").strip()
                    if line_text.startswith("data: "):
                        line_text = line_text[6:]  # Remove 'data: ' prefix

                        if line_text == "[DONE]":
                            yield StreamChunk(
                                content="",
                                model=self.config.model_name,
                                provider="openai",
                                is_final=True,
                                finish_reason="stop",
                            )
                            break

                        try:
                            data = json.loads(line_text)
                            choices = data.get("choices", [])
                            if choices:
                                delta = choices[0].get("delta", {})
                                content = delta.get("content")
                                finish_reason = choices[0].get("finish_reason")

                                if content:
                                    yield StreamChunk(
                                        content=content,
                                        model=data.get("model", self.config.model_name),
                                        provider="openai",
                                        is_final=finish_reason is not None,
                                        finish_reason=finish_reason,
                                    )

                        except json.JSONDecodeError:
                            continue

        except Exception as e:
            logger.error(f"OpenAI stream error: {e}")
            raise


def create_openai_adapter(
    model_name: str,
    api_key: str,
    **kwargs: Any,
) -> OpenAIAdapter:
    """Create an OpenAI adapter with common configurations.

    Args:
        model_name: OpenAI model name (gpt-4, gpt-4o, etc.)
        api_key: OpenAI API key.
        **kwargs: Additional configuration options.

    Returns:
        Configured OpenAIAdapter instance.
    """
    from ..config import CapabilityType, DEFAULT_MODEL_CONFIGS, LLMProvider, PrivacyLevel

    # Get default config for model
    model_defaults = DEFAULT_MODEL_CONFIGS.get("openai", {}).get(model_name, {})

    config = LLMConfig(
        provider=LLMProvider.OPENAI,
        model_name=model_name,
        api_key=api_key,
        context_length=model_defaults.get("context_length", 4096),
        capabilities=model_defaults.get("capabilities", [CapabilityType.TEXT]),
        cost_per_1k_input=model_defaults.get("cost_per_1k_input", 0.002),
        cost_per_1k_output=model_defaults.get("cost_per_1k_output", 0.002),
        specialization=model_defaults.get("specialization", "general"),
        privacy_level=PrivacyLevel.STANDARD,
        **kwargs,
    )

    return OpenAIAdapter(config)
