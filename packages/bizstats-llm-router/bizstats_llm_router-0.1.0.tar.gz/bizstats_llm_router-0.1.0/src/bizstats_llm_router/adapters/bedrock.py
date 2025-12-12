"""
AWS Bedrock LLM Adapter.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.

Integrates AWS Bedrock models with the LLM Router.
"""

import json
import logging
import os
import time
from typing import Any, AsyncGenerator, List, Optional

from ..base import LLMAdapter, LLMMessage, LLMResponse, StreamChunk
from ..config import LLMConfig

logger = logging.getLogger(__name__)


class BedrockAdapter(LLMAdapter):
    """AWS Bedrock LLM adapter."""

    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self._client = None
        self._runtime_client = None
        self._region = config.custom_params.get(
            "aws_region", os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        )

    async def initialize(self) -> bool:
        """Initialize the AWS Bedrock adapter."""
        try:
            import boto3

            # Create Bedrock runtime client
            self._runtime_client = boto3.client(
                "bedrock-runtime",
                region_name=self._region,
            )

            self._is_initialized = True
            self._is_available = True
            logger.info(f"AWS Bedrock adapter initialized for {self.config.model_name}")
            return True

        except ImportError:
            logger.error("boto3 package not installed")
            return False
        except Exception as e:
            logger.error(f"Failed to initialize AWS Bedrock adapter: {e}")
            self._is_available = False
            return False

    async def cleanup(self) -> None:
        """Cleanup AWS Bedrock connection."""
        self._runtime_client = None

    def _format_messages_for_claude(self, messages: List[LLMMessage]) -> dict:
        """Format messages for Claude models on Bedrock."""
        system_prompt = None
        formatted_messages = []

        for msg in messages:
            if msg.role == "system":
                system_prompt = msg.content
            else:
                formatted_messages.append({
                    "role": msg.role,
                    "content": [{"type": "text", "text": msg.content}],
                })

        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "messages": formatted_messages,
            "max_tokens": self.config.max_tokens,
        }

        if system_prompt:
            body["system"] = system_prompt

        return body

    def _format_messages_for_llama(self, messages: List[LLMMessage]) -> dict:
        """Format messages for Llama models on Bedrock."""
        prompt = ""
        for msg in messages:
            if msg.role == "system":
                prompt += f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n{msg.content}<|eot_id|>\n"
            elif msg.role == "user":
                prompt += f"<|start_header_id|>user<|end_header_id|>\n{msg.content}<|eot_id|>\n"
            elif msg.role == "assistant":
                prompt += f"<|start_header_id|>assistant<|end_header_id|>\n{msg.content}<|eot_id|>\n"

        prompt += "<|start_header_id|>assistant<|end_header_id|>\n"

        return {
            "prompt": prompt,
            "max_gen_len": self.config.max_tokens,
            "temperature": self.config.temperature,
        }

    async def chat(
        self,
        messages: List[LLMMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> LLMResponse:
        """Send chat messages to AWS Bedrock."""
        if not self._runtime_client or not self._is_available:
            raise RuntimeError("AWS Bedrock adapter not initialized")

        start_time = time.time()

        try:
            import asyncio

            # Determine model type and format request
            model_id = self.config.model_name

            if "anthropic" in model_id.lower():
                body = self._format_messages_for_claude(messages)
                if temperature is not None:
                    body["temperature"] = self._get_temperature(temperature)
                if max_tokens is not None:
                    body["max_tokens"] = self._get_max_tokens(max_tokens)
            elif "meta" in model_id.lower() or "llama" in model_id.lower():
                body = self._format_messages_for_llama(messages)
                if temperature is not None:
                    body["temperature"] = self._get_temperature(temperature)
                if max_tokens is not None:
                    body["max_gen_len"] = self._get_max_tokens(max_tokens)
            else:
                raise ValueError(f"Unsupported Bedrock model: {model_id}")

            # Invoke model (run in executor since boto3 is synchronous)
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self._runtime_client.invoke_model(
                    modelId=model_id,
                    body=json.dumps(body),
                    contentType="application/json",
                    accept="application/json",
                ),
            )

            # Parse response
            response_body = json.loads(response["body"].read())
            response_time = time.time() - start_time

            # Extract content based on model type
            if "anthropic" in model_id.lower():
                content_blocks = response_body.get("content", [])
                content = "".join(
                    block.get("text", "")
                    for block in content_blocks
                    if block.get("type") == "text"
                )
                prompt_tokens = response_body.get("usage", {}).get("input_tokens", 0)
                completion_tokens = response_body.get("usage", {}).get("output_tokens", 0)
                finish_reason = response_body.get("stop_reason", "end_turn")
            else:
                content = response_body.get("generation", "")
                # Llama doesn't return token counts in the same way
                prompt_tokens = len(" ".join(m.content for m in messages).split())
                completion_tokens = len(content.split())
                finish_reason = response_body.get("stop_reason", "stop")

            return LLMResponse(
                content=content,
                model=model_id,
                provider="bedrock",
                tokens_used=prompt_tokens + completion_tokens,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                response_time=response_time,
                finish_reason=finish_reason,
                cost=self.calculate_cost(prompt_tokens, completion_tokens),
                metadata={
                    "region": self._region,
                },
            )

        except Exception as e:
            logger.error(f"AWS Bedrock chat error: {e}")
            raise

    async def stream_chat(
        self,
        messages: List[LLMMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> AsyncGenerator[StreamChunk, None]:
        """Stream chat response from AWS Bedrock."""
        if not self._runtime_client or not self._is_available:
            raise RuntimeError("AWS Bedrock adapter not initialized")

        try:
            import asyncio

            model_id = self.config.model_name

            if "anthropic" in model_id.lower():
                body = self._format_messages_for_claude(messages)
                if temperature is not None:
                    body["temperature"] = self._get_temperature(temperature)
                if max_tokens is not None:
                    body["max_tokens"] = self._get_max_tokens(max_tokens)
            else:
                # Non-Claude models: fall back to non-streaming
                response = await self.chat(messages, temperature, max_tokens, **kwargs)
                yield StreamChunk(
                    content=response.content,
                    model=model_id,
                    provider="bedrock",
                    is_final=True,
                    finish_reason=response.finish_reason,
                )
                return

            # Use streaming for Claude models
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self._runtime_client.invoke_model_with_response_stream(
                    modelId=model_id,
                    body=json.dumps(body),
                    contentType="application/json",
                    accept="application/json",
                ),
            )

            # Process stream
            for event in response.get("body", []):
                chunk = json.loads(event.get("chunk", {}).get("bytes", b"{}"))

                if chunk.get("type") == "content_block_delta":
                    delta = chunk.get("delta", {})
                    if delta.get("type") == "text_delta":
                        text = delta.get("text", "")
                        if text:
                            yield StreamChunk(
                                content=text,
                                model=model_id,
                                provider="bedrock",
                            )

                elif chunk.get("type") == "message_stop":
                    yield StreamChunk(
                        content="",
                        model=model_id,
                        provider="bedrock",
                        is_final=True,
                        finish_reason="end_turn",
                    )
                    break

        except Exception as e:
            logger.error(f"AWS Bedrock stream error: {e}")
            raise


def create_bedrock_adapter(
    model_id: str,
    region: str = "us-east-1",
    **kwargs: Any,
) -> BedrockAdapter:
    """Create an AWS Bedrock adapter.

    Args:
        model_id: Bedrock model ID.
        region: AWS region.
        **kwargs: Additional configuration options.

    Returns:
        Configured BedrockAdapter instance.
    """
    from ..config import CapabilityType, LLMProvider, PrivacyLevel

    config = LLMConfig(
        provider=LLMProvider.BEDROCK,
        model_name=model_id,
        capabilities=[CapabilityType.TEXT, CapabilityType.REASONING],
        privacy_level=PrivacyLevel.STANDARD,
        custom_params={"aws_region": region},
        **kwargs,
    )

    return BedrockAdapter(config)
