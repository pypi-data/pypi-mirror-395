"""
Google Gemini LLM Adapter.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.

Integrates Google Gemini models with the LLM Router.
"""

import asyncio
import logging
import time
from typing import Any, AsyncGenerator, List, Optional

from ..base import LLMAdapter, LLMMessage, LLMResponse, StreamChunk
from ..config import LLMConfig

logger = logging.getLogger(__name__)


class GoogleAdapter(LLMAdapter):
    """Google Gemini LLM adapter."""

    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self._client = None
        self._api_key = config.api_key

    async def initialize(self) -> bool:
        """Initialize the Google Gemini adapter."""
        try:
            import google.generativeai as genai

            if not self._api_key:
                logger.error("Google API key is required")
                return False

            # Configure the client
            genai.configure(api_key=self._api_key)

            # Initialize the model
            self._client = genai.GenerativeModel(self.config.model_name)

            self._is_initialized = True
            self._is_available = True
            logger.info(f"Google Gemini adapter initialized for {self.config.model_name}")
            return True

        except ImportError:
            logger.error("google-generativeai package not installed")
            return False
        except Exception as e:
            logger.error(f"Failed to initialize Google Gemini adapter: {e}")
            self._is_available = False
            return False

    async def cleanup(self) -> None:
        """Cleanup Google Gemini connection."""
        self._client = None

    def _convert_messages_to_content(self, messages: List[LLMMessage]) -> str:
        """Convert messages to Gemini content format."""
        parts = []

        for msg in messages:
            if msg.role == "system":
                parts.append(f"System: {msg.content}")
            elif msg.role == "user":
                parts.append(f"User: {msg.content}")
            elif msg.role == "assistant":
                parts.append(f"Assistant: {msg.content}")

        return "\n\n".join(parts)

    async def chat(
        self,
        messages: List[LLMMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> LLMResponse:
        """Send chat messages to Google Gemini."""
        if not self._client or not self._is_available:
            raise RuntimeError("Google Gemini adapter not initialized")

        start_time = time.time()

        try:
            # Convert messages to content
            content = self._convert_messages_to_content(messages)

            # Configure generation
            generation_config = {}
            if temperature is not None:
                generation_config["temperature"] = self._get_temperature(temperature)
            if max_tokens is not None:
                generation_config["max_output_tokens"] = self._get_max_tokens(max_tokens)

            # Generate response (synchronous call wrapped in async)
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self._client.generate_content(
                    content,
                    generation_config=generation_config if generation_config else None,
                ),
            )

            response_time = time.time() - start_time

            if response and response.text:
                # Estimate tokens (Gemini doesn't always return token counts)
                prompt_tokens = len(content.split())
                completion_tokens = len(response.text.split())

                return LLMResponse(
                    content=response.text.strip(),
                    model=self.config.model_name,
                    provider="google",
                    tokens_used=prompt_tokens + completion_tokens,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    response_time=response_time,
                    finish_reason="stop",
                    cost=self.calculate_cost(prompt_tokens, completion_tokens),
                )
            else:
                raise RuntimeError("No response from Google Gemini")

        except Exception as e:
            logger.error(f"Google Gemini chat error: {e}")
            raise

    async def stream_chat(
        self,
        messages: List[LLMMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> AsyncGenerator[StreamChunk, None]:
        """Stream chat response from Google Gemini."""
        if not self._client or not self._is_available:
            raise RuntimeError("Google Gemini adapter not initialized")

        try:
            # Convert messages
            content = self._convert_messages_to_content(messages)

            # Configure generation
            generation_config = {}
            if temperature is not None:
                generation_config["temperature"] = self._get_temperature(temperature)
            if max_tokens is not None:
                generation_config["max_output_tokens"] = self._get_max_tokens(max_tokens)

            # Generate streaming response
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self._client.generate_content(
                    content,
                    generation_config=generation_config if generation_config else None,
                    stream=True,
                ),
            )

            # Yield chunks
            for chunk in response:
                if chunk.text:
                    yield StreamChunk(
                        content=chunk.text,
                        model=self.config.model_name,
                        provider="google",
                    )
                    await asyncio.sleep(0)  # Allow other tasks to run

            yield StreamChunk(
                content="",
                model=self.config.model_name,
                provider="google",
                is_final=True,
                finish_reason="stop",
            )

        except Exception as e:
            logger.error(f"Google Gemini stream error: {e}")
            raise


def create_google_adapter(
    model_name: str,
    api_key: str,
    **kwargs: Any,
) -> GoogleAdapter:
    """Create a Google Gemini adapter with common configurations.

    Args:
        model_name: Gemini model name.
        api_key: Google API key.
        **kwargs: Additional configuration options.

    Returns:
        Configured GoogleAdapter instance.
    """
    from ..config import CapabilityType, DEFAULT_MODEL_CONFIGS, LLMProvider, PrivacyLevel

    model_defaults = DEFAULT_MODEL_CONFIGS.get("google", {}).get(model_name, {})

    config = LLMConfig(
        provider=LLMProvider.GOOGLE,
        model_name=model_name,
        api_key=api_key,
        context_length=model_defaults.get("context_length", 32768),
        capabilities=model_defaults.get("capabilities", [CapabilityType.TEXT]),
        cost_per_1k_input=model_defaults.get("cost_per_1k_input", 0.001),
        cost_per_1k_output=model_defaults.get("cost_per_1k_output", 0.002),
        specialization=model_defaults.get("specialization", "multimodal"),
        privacy_level=PrivacyLevel.STANDARD,
        **kwargs,
    )

    return GoogleAdapter(config)
