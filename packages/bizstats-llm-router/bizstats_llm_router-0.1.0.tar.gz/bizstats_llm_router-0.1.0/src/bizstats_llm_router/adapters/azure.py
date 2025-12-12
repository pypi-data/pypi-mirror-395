"""
Azure OpenAI LLM Adapter.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.

Integrates Azure OpenAI models with the LLM Router.
"""

import json
import logging
import time
from typing import Any, AsyncGenerator, List, Optional

import aiohttp

from ..base import LLMAdapter, LLMMessage, LLMResponse, StreamChunk
from ..config import LLMConfig

logger = logging.getLogger(__name__)


class AzureOpenAIAdapter(LLMAdapter):
    """Azure OpenAI LLM adapter."""

    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self._session: Optional[aiohttp.ClientSession] = None
        self._api_key = config.api_key
        self._endpoint = config.api_base
        self._api_version = config.custom_params.get("api_version", "2024-02-15-preview")
        self._deployment_name = config.custom_params.get("deployment_name", config.model_name)

    async def initialize(self) -> bool:
        """Initialize the Azure OpenAI adapter."""
        try:
            if not self._api_key:
                logger.error("Azure OpenAI API key is required")
                return False

            if not self._endpoint:
                logger.error("Azure OpenAI endpoint is required")
                return False

            headers = {
                "api-key": self._api_key,
                "Content-Type": "application/json",
            }

            self._session = aiohttp.ClientSession(
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=self.config.timeout),
            )

            self._is_initialized = True
            self._is_available = True
            logger.info(f"Azure OpenAI adapter initialized for {self._deployment_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize Azure OpenAI adapter: {e}")
            self._is_available = False
            return False

    async def cleanup(self) -> None:
        """Cleanup Azure OpenAI connection."""
        if self._session:
            await self._session.close()
            self._session = None

    def _get_api_url(self, endpoint_type: str = "chat/completions") -> str:
        """Get the full API URL for a request."""
        return (
            f"{self._endpoint}/openai/deployments/{self._deployment_name}/"
            f"{endpoint_type}?api-version={self._api_version}"
        )

    async def chat(
        self,
        messages: List[LLMMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> LLMResponse:
        """Send chat messages to Azure OpenAI."""
        if not self._session or not self._is_available:
            raise RuntimeError("Azure OpenAI adapter not initialized")

        start_time = time.time()

        try:
            # Convert messages
            azure_messages = [
                {"role": msg.role, "content": msg.content}
                for msg in messages
            ]

            # Prepare request
            request_data = {
                "messages": azure_messages,
                "temperature": self._get_temperature(temperature),
                "max_tokens": self._get_max_tokens(max_tokens),
            }

            if kwargs:
                request_data.update(kwargs)

            # Send request
            async with self._session.post(
                self._get_api_url(),
                json=request_data,
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise RuntimeError(f"Azure OpenAI error {response.status}: {error_text}")

                data = await response.json()

                choice = data.get("choices", [{}])[0]
                content = choice.get("message", {}).get("content", "")
                finish_reason = choice.get("finish_reason", "stop")

                usage = data.get("usage", {})
                prompt_tokens = usage.get("prompt_tokens", 0)
                completion_tokens = usage.get("completion_tokens", 0)

                response_time = time.time() - start_time

                return LLMResponse(
                    content=content,
                    model=self._deployment_name,
                    provider="azure_openai",
                    tokens_used=prompt_tokens + completion_tokens,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    response_time=response_time,
                    finish_reason=finish_reason,
                    cost=self.calculate_cost(prompt_tokens, completion_tokens),
                    metadata={
                        "deployment": self._deployment_name,
                        "id": data.get("id"),
                    },
                )

        except Exception as e:
            logger.error(f"Azure OpenAI chat error: {e}")
            raise

    async def stream_chat(
        self,
        messages: List[LLMMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> AsyncGenerator[StreamChunk, None]:
        """Stream chat response from Azure OpenAI."""
        if not self._session or not self._is_available:
            raise RuntimeError("Azure OpenAI adapter not initialized")

        try:
            # Convert messages
            azure_messages = [
                {"role": msg.role, "content": msg.content}
                for msg in messages
            ]

            # Prepare request
            request_data = {
                "messages": azure_messages,
                "temperature": self._get_temperature(temperature),
                "max_tokens": self._get_max_tokens(max_tokens),
                "stream": True,
            }

            if kwargs:
                request_data.update(kwargs)

            # Send streaming request
            async with self._session.post(
                self._get_api_url(),
                json=request_data,
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise RuntimeError(f"Azure OpenAI error {response.status}: {error_text}")

                async for line in response.content:
                    line_text = line.decode("utf-8").strip()

                    if line_text.startswith("data: "):
                        line_text = line_text[6:]

                        if line_text == "[DONE]":
                            yield StreamChunk(
                                content="",
                                model=self._deployment_name,
                                provider="azure_openai",
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
                                        model=self._deployment_name,
                                        provider="azure_openai",
                                        is_final=finish_reason is not None,
                                        finish_reason=finish_reason,
                                    )

                        except json.JSONDecodeError:
                            continue

        except Exception as e:
            logger.error(f"Azure OpenAI stream error: {e}")
            raise


def create_azure_adapter(
    deployment_name: str,
    endpoint: str,
    api_key: str,
    api_version: str = "2024-02-15-preview",
    **kwargs: Any,
) -> AzureOpenAIAdapter:
    """Create an Azure OpenAI adapter.

    Args:
        deployment_name: Azure deployment name.
        endpoint: Azure OpenAI endpoint URL.
        api_key: Azure API key.
        api_version: API version.
        **kwargs: Additional configuration options.

    Returns:
        Configured AzureOpenAIAdapter instance.
    """
    from ..config import CapabilityType, LLMProvider, PrivacyLevel

    config = LLMConfig(
        provider=LLMProvider.AZURE_OPENAI,
        model_name=deployment_name,
        api_key=api_key,
        api_base=endpoint,
        capabilities=[CapabilityType.TEXT, CapabilityType.TOOLS],
        privacy_level=PrivacyLevel.STANDARD,
        custom_params={
            "api_version": api_version,
            "deployment_name": deployment_name,
        },
        **kwargs,
    )

    return AzureOpenAIAdapter(config)
