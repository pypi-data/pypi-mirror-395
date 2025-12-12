"""
Ollama LLM Adapter.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.

Integrates local Ollama models with the LLM Router.
Supports both local and cloud-hosted Ollama instances.
"""

import logging
import os
import time
from typing import Any, AsyncGenerator, List, Optional

import httpx

from ..base import LLMAdapter, LLMMessage, LLMResponse, StreamChunk
from ..config import LLMConfig

logger = logging.getLogger(__name__)

# Try to import ollama package
try:
    import ollama
    HAS_OLLAMA = True
except ImportError:
    HAS_OLLAMA = False


class OllamaAdapter(LLMAdapter):
    """Ollama LLM adapter for local/cloud models."""

    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self._client = None
        self._base_url = config.api_base or os.getenv(
            "OLLAMA_BASE_URL", "http://localhost:11434"
        )
        self._api_key = config.api_key or os.getenv("OLLAMA_API_KEY")
        self._available_models: List[str] = []

    async def initialize(self) -> bool:
        """Initialize the Ollama adapter."""
        try:
            if HAS_OLLAMA:
                # Use official ollama package
                client_kwargs = {"host": self._base_url}
                if self._api_key:
                    client_kwargs["headers"] = {"Authorization": f"Bearer {self._api_key}"}
                    logger.info("Using API key for Ollama authentication")

                self._client = ollama.AsyncClient(**client_kwargs)
                self._available_models = await self._load_available_models()
            else:
                # Fall back to HTTP client
                logger.info("Using HTTP client for Ollama (ollama package not installed)")
                self._client = httpx.AsyncClient(
                    base_url=self._base_url,
                    timeout=self.config.timeout,
                    headers={"Authorization": f"Bearer {self._api_key}"} if self._api_key else {},
                )
                self._available_models = await self._load_models_http()

            self._is_initialized = True
            self._is_available = True
            logger.info(f"Ollama adapter initialized for {self.config.model_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize Ollama adapter: {e}")
            self._is_available = False
            return False

    async def _load_available_models(self) -> List[str]:
        """Load available models using ollama package."""
        try:
            result = await self._client.list()
            models = [model["name"] for model in result.get("models", [])]
            logger.info(f"Loaded {len(models)} models from Ollama")
            return models
        except Exception as e:
            logger.warning(f"Could not fetch models: {e}")
            return []

    async def _load_models_http(self) -> List[str]:
        """Load available models using HTTP client."""
        try:
            response = await self._client.get("/api/tags")
            if response.status_code == 200:
                data = response.json()
                models = [model["name"] for model in data.get("models", [])]
                return models
        except Exception as e:
            logger.warning(f"Could not fetch models via HTTP: {e}")
        return []

    async def cleanup(self) -> None:
        """Cleanup Ollama connection."""
        if self._client and isinstance(self._client, httpx.AsyncClient):
            await self._client.aclose()
        self._client = None

    async def chat(
        self,
        messages: List[LLMMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> LLMResponse:
        """Send chat messages to Ollama."""
        if not self._client or not self._is_available:
            raise RuntimeError("Ollama adapter not initialized")

        start_time = time.time()

        try:
            # Convert messages
            ollama_messages = [
                {"role": msg.role, "content": msg.content}
                for msg in messages
            ]

            options = {
                "temperature": self._get_temperature(temperature),
                "num_predict": self._get_max_tokens(max_tokens),
            }

            if HAS_OLLAMA:
                # Use ollama package
                response = await self._client.chat(
                    model=self.config.model_name,
                    messages=ollama_messages,
                    options=options,
                    stream=False,
                )

                content = response.get("message", {}).get("content", "")
                prompt_tokens = response.get("prompt_eval_count", 0)
                completion_tokens = response.get("eval_count", 0)
                finish_reason = response.get("done_reason", "stop")

            else:
                # Use HTTP client
                response = await self._client.post(
                    "/api/chat",
                    json={
                        "model": self.config.model_name,
                        "messages": ollama_messages,
                        "options": options,
                        "stream": False,
                    },
                )

                if response.status_code != 200:
                    raise RuntimeError(f"Ollama API error: {response.text}")

                data = response.json()
                content = data.get("message", {}).get("content", "")
                prompt_tokens = data.get("prompt_eval_count", 0)
                completion_tokens = data.get("eval_count", 0)
                finish_reason = data.get("done_reason", "stop")

            response_time = time.time() - start_time

            return LLMResponse(
                content=content,
                model=self.config.model_name,
                provider="ollama",
                tokens_used=prompt_tokens + completion_tokens,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                response_time=response_time,
                finish_reason=finish_reason,
                cost=0.0,  # Ollama is free
                metadata={
                    "base_url": self._base_url,
                },
            )

        except Exception as e:
            logger.error(f"Ollama chat error: {e}")
            raise

    async def stream_chat(
        self,
        messages: List[LLMMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> AsyncGenerator[StreamChunk, None]:
        """Stream chat response from Ollama."""
        if not self._client or not self._is_available:
            raise RuntimeError("Ollama adapter not initialized")

        try:
            # Convert messages
            ollama_messages = [
                {"role": msg.role, "content": msg.content}
                for msg in messages
            ]

            options = {
                "temperature": self._get_temperature(temperature),
                "num_predict": self._get_max_tokens(max_tokens),
            }

            if HAS_OLLAMA:
                # Use ollama package streaming
                async for part in await self._client.chat(
                    model=self.config.model_name,
                    messages=ollama_messages,
                    options=options,
                    stream=True,
                ):
                    content = part.get("message", {}).get("content", "")
                    if content:
                        yield StreamChunk(
                            content=content,
                            model=self.config.model_name,
                            provider="ollama",
                        )

                    if part.get("done", False):
                        yield StreamChunk(
                            content="",
                            model=self.config.model_name,
                            provider="ollama",
                            is_final=True,
                            finish_reason=part.get("done_reason", "stop"),
                        )
                        break

            else:
                # Use HTTP client streaming
                async with self._client.stream(
                    "POST",
                    "/api/chat",
                    json={
                        "model": self.config.model_name,
                        "messages": ollama_messages,
                        "options": options,
                        "stream": True,
                    },
                ) as response:
                    async for line in response.aiter_lines():
                        if line:
                            import json
                            data = json.loads(line)
                            content = data.get("message", {}).get("content", "")

                            if content:
                                yield StreamChunk(
                                    content=content,
                                    model=self.config.model_name,
                                    provider="ollama",
                                )

                            if data.get("done", False):
                                yield StreamChunk(
                                    content="",
                                    model=self.config.model_name,
                                    provider="ollama",
                                    is_final=True,
                                    finish_reason=data.get("done_reason", "stop"),
                                )
                                break

        except Exception as e:
            logger.error(f"Ollama stream error: {e}")
            raise

    def get_available_models(self) -> List[str]:
        """Get list of available models.

        Returns:
            List of model names available on this Ollama instance.
        """
        return self._available_models.copy()


def create_ollama_adapter(
    model_name: str,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    **kwargs: Any,
) -> OllamaAdapter:
    """Create an Ollama adapter with common configurations.

    Args:
        model_name: Ollama model name.
        base_url: Ollama server URL.
        api_key: Optional API key for authenticated instances.
        **kwargs: Additional configuration options.

    Returns:
        Configured OllamaAdapter instance.
    """
    from ..config import CapabilityType, DEFAULT_MODEL_CONFIGS, LLMProvider, PrivacyLevel

    model_defaults = DEFAULT_MODEL_CONFIGS.get("ollama", {}).get(model_name, {})

    config = LLMConfig(
        provider=LLMProvider.OLLAMA,
        model_name=model_name,
        api_key=api_key,
        api_base=base_url,
        context_length=model_defaults.get("context_length", 4096),
        capabilities=model_defaults.get("capabilities", [CapabilityType.TEXT]),
        cost_per_1k_input=0.0,
        cost_per_1k_output=0.0,
        specialization=model_defaults.get("specialization", "general"),
        privacy_level=PrivacyLevel.HIGH,
        timeout=kwargs.get("timeout", 120),  # Longer timeout for local models
        **kwargs,
    )

    return OllamaAdapter(config)
