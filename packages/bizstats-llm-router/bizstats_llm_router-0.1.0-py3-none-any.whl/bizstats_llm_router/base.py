"""
Base interfaces and data classes for LLM Router.

Provides abstract base classes for LLM adapters and standardized message/response formats.
"""

import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, AsyncGenerator, Dict, List, Optional

from .config import CapabilityType, LLMConfig

logger = logging.getLogger(__name__)


@dataclass
class LLMMessage:
    """Standardized message format for LLM interactions."""

    role: str  # "system", "user", "assistant", "tool"
    content: str
    name: Optional[str] = None  # For tool messages
    tool_call_id: Optional[str] = None  # For tool results
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        result = {"role": self.role, "content": self.content}
        if self.name:
            result["name"] = self.name
        if self.tool_call_id:
            result["tool_call_id"] = self.tool_call_id
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LLMMessage":
        """Create from dictionary."""
        return cls(
            role=data.get("role", "user"),
            content=data.get("content", ""),
            name=data.get("name"),
            tool_call_id=data.get("tool_call_id"),
            metadata=data.get("metadata", {}),
        )


@dataclass
class LLMResponse:
    """Standardized response from LLM."""

    content: str
    model: str
    provider: str = ""
    tokens_used: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    response_time: float = 0.0
    finish_reason: str = "stop"
    cost: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "content": self.content,
            "model": self.model,
            "provider": self.provider,
            "tokens_used": self.tokens_used,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "response_time": self.response_time,
            "finish_reason": self.finish_reason,
            "cost": self.cost,
            "metadata": self.metadata,
        }


@dataclass
class StreamChunk:
    """A chunk from a streaming response."""

    content: str
    model: str
    provider: str = ""
    finish_reason: Optional[str] = None
    is_final: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


class LLMAdapter(ABC):
    """Base interface for all LLM adapters."""

    def __init__(self, config: LLMConfig):
        self.config = config
        self._is_initialized = False
        self._is_available = False
        self._last_health_check = 0.0
        self._health_check_interval = 60.0  # seconds

    @property
    def provider_name(self) -> str:
        """Get the provider name."""
        return self.config.provider.value

    @property
    def model_name(self) -> str:
        """Get the model name."""
        return self.config.model_name

    @property
    def is_available(self) -> bool:
        """Check if adapter is available."""
        return self._is_available

    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the LLM adapter.

        Returns:
            True if initialization was successful, False otherwise.
        """
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup resources used by the adapter."""
        pass

    @abstractmethod
    async def chat(
        self,
        messages: List[LLMMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> LLMResponse:
        """Send chat messages and get response.

        Args:
            messages: List of messages in the conversation.
            temperature: Override default temperature.
            max_tokens: Override default max tokens.
            **kwargs: Additional provider-specific parameters.

        Returns:
            LLMResponse with the generated content.
        """
        pass

    @abstractmethod
    async def stream_chat(
        self,
        messages: List[LLMMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> AsyncGenerator[StreamChunk, None]:
        """Stream chat response.

        Args:
            messages: List of messages in the conversation.
            temperature: Override default temperature.
            max_tokens: Override default max tokens.
            **kwargs: Additional provider-specific parameters.

        Yields:
            StreamChunk objects with partial content.
        """
        pass

    async def health_check(self) -> bool:
        """Check if LLM is available and responding.

        Returns:
            True if the LLM is available, False otherwise.
        """
        now = time.time()

        # Use cached result if within interval
        if now - self._last_health_check < self._health_check_interval:
            return self._is_available

        try:
            # Simple health check - send minimal message
            test_message = [LLMMessage(role="user", content="Hi")]
            response = await self.chat(test_message, max_tokens=10)
            self._is_available = bool(response.content)
            self._last_health_check = now
            return self._is_available
        except Exception as e:
            logger.warning(f"Health check failed for {self.config.model_name}: {e}")
            self._is_available = False
            self._last_health_check = now
            return False

    def get_capabilities(self) -> Dict[str, Any]:
        """Get LLM capabilities information.

        Returns:
            Dictionary with capability information.
        """
        return {
            "provider": self.config.provider.value,
            "model": self.config.model_name,
            "capabilities": [cap.value for cap in self.config.capabilities],
            "context_length": self.config.context_length,
            "max_tokens": self.config.max_tokens,
            "cost_per_1k_input": self.config.cost_per_1k_input,
            "cost_per_1k_output": self.config.cost_per_1k_output,
            "privacy_level": self.config.privacy_level.value,
            "specialization": self.config.specialization,
            "available": self._is_available,
        }

    def calculate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        """Calculate the cost for a request.

        Args:
            prompt_tokens: Number of input tokens.
            completion_tokens: Number of output tokens.

        Returns:
            Total cost in USD.
        """
        input_cost = (prompt_tokens / 1000) * self.config.cost_per_1k_input
        output_cost = (completion_tokens / 1000) * self.config.cost_per_1k_output
        return input_cost + output_cost

    def _get_temperature(self, override: Optional[float]) -> float:
        """Get temperature value, using override or default."""
        if override is not None:
            return max(0.0, min(2.0, override))
        return self.config.temperature

    def _get_max_tokens(self, override: Optional[int]) -> int:
        """Get max tokens value, using override or default."""
        if override is not None:
            return max(1, min(self.config.context_length, override))
        return self.config.max_tokens


class AdapterFactory:
    """Factory for creating LLM adapters."""

    _adapters: Dict[str, type] = {}

    @classmethod
    def register(cls, provider: str, adapter_class: type) -> None:
        """Register an adapter class for a provider.

        Args:
            provider: Provider name.
            adapter_class: Adapter class to register.
        """
        cls._adapters[provider.lower()] = adapter_class

    @classmethod
    def create(cls, config: LLMConfig) -> LLMAdapter:
        """Create an adapter instance.

        Args:
            config: LLM configuration.

        Returns:
            Configured LLMAdapter instance.

        Raises:
            ValueError: If provider is not supported.
        """
        provider = config.provider.value.lower()
        if provider not in cls._adapters:
            raise ValueError(f"Unsupported provider: {provider}")
        return cls._adapters[provider](config)

    @classmethod
    def get_supported_providers(cls) -> List[str]:
        """Get list of supported provider names.

        Returns:
            List of provider names.
        """
        return list(cls._adapters.keys())


# Utility functions
def create_message(role: str, content: str, **metadata: Any) -> LLMMessage:
    """Helper to create LLM messages.

    Args:
        role: Message role (system, user, assistant).
        content: Message content.
        **metadata: Additional metadata.

    Returns:
        LLMMessage instance.
    """
    return LLMMessage(role=role, content=content, metadata=metadata)


def messages_from_dicts(messages: List[Dict[str, Any]]) -> List[LLMMessage]:
    """Convert list of dictionaries to LLMMessage list.

    Args:
        messages: List of message dictionaries.

    Returns:
        List of LLMMessage instances.
    """
    return [LLMMessage.from_dict(msg) for msg in messages]


def messages_to_dicts(messages: List[LLMMessage]) -> List[Dict[str, Any]]:
    """Convert list of LLMMessages to dictionaries.

    Args:
        messages: List of LLMMessage instances.

    Returns:
        List of message dictionaries.
    """
    return [msg.to_dict() for msg in messages]
