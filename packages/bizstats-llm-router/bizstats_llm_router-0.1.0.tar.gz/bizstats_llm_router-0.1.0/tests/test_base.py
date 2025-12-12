"""
Tests for base classes and interfaces.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import pytest
from bizstats_llm_router import (
    LLMMessage,
    LLMResponse,
    StreamChunk,
    create_message,
    messages_from_dicts,
    messages_to_dicts,
)


class TestLLMMessage:
    """Tests for LLMMessage class."""

    def test_create_message(self):
        """Test creating a basic message."""
        msg = LLMMessage(role="user", content="Hello")
        assert msg.role == "user"
        assert msg.content == "Hello"
        assert msg.name is None
        assert msg.tool_call_id is None
        assert msg.metadata == {}

    def test_message_with_metadata(self):
        """Test creating a message with metadata."""
        msg = LLMMessage(
            role="assistant",
            content="Hi there!",
            metadata={"confidence": 0.95},
        )
        assert msg.metadata["confidence"] == 0.95

    def test_message_to_dict(self):
        """Test converting message to dictionary."""
        msg = LLMMessage(role="user", content="Hello")
        d = msg.to_dict()
        assert d == {"role": "user", "content": "Hello"}

    def test_message_to_dict_with_optional_fields(self):
        """Test converting message with optional fields to dictionary."""
        msg = LLMMessage(
            role="tool",
            content="Result: 42",
            name="calculator",
            tool_call_id="call_123",
        )
        d = msg.to_dict()
        assert d["name"] == "calculator"
        assert d["tool_call_id"] == "call_123"

    def test_message_from_dict(self):
        """Test creating message from dictionary."""
        d = {"role": "user", "content": "Hello"}
        msg = LLMMessage.from_dict(d)
        assert msg.role == "user"
        assert msg.content == "Hello"

    def test_message_from_dict_with_defaults(self):
        """Test creating message from incomplete dictionary."""
        d = {}
        msg = LLMMessage.from_dict(d)
        assert msg.role == "user"
        assert msg.content == ""


class TestLLMResponse:
    """Tests for LLMResponse class."""

    def test_create_response(self):
        """Test creating a basic response."""
        resp = LLMResponse(
            content="Hello!",
            model="gpt-4",
            provider="openai",
        )
        assert resp.content == "Hello!"
        assert resp.model == "gpt-4"
        assert resp.provider == "openai"
        assert resp.tokens_used == 0
        assert resp.cost == 0.0

    def test_response_with_full_data(self):
        """Test creating response with all fields."""
        resp = LLMResponse(
            content="Hello!",
            model="gpt-4",
            provider="openai",
            tokens_used=25,
            prompt_tokens=10,
            completion_tokens=15,
            response_time=0.5,
            finish_reason="stop",
            cost=0.001,
            metadata={"id": "resp_123"},
        )
        assert resp.tokens_used == 25
        assert resp.prompt_tokens == 10
        assert resp.completion_tokens == 15
        assert resp.response_time == 0.5
        assert resp.finish_reason == "stop"
        assert resp.cost == 0.001
        assert resp.metadata["id"] == "resp_123"

    def test_response_to_dict(self):
        """Test converting response to dictionary."""
        resp = LLMResponse(
            content="Hi",
            model="test",
            provider="test",
            tokens_used=10,
        )
        d = resp.to_dict()
        assert d["content"] == "Hi"
        assert d["model"] == "test"
        assert d["tokens_used"] == 10


class TestStreamChunk:
    """Tests for StreamChunk class."""

    def test_create_chunk(self):
        """Test creating a stream chunk."""
        chunk = StreamChunk(
            content="Hello",
            model="gpt-4",
            provider="openai",
        )
        assert chunk.content == "Hello"
        assert chunk.is_final is False
        assert chunk.finish_reason is None

    def test_final_chunk(self):
        """Test creating a final stream chunk."""
        chunk = StreamChunk(
            content="",
            model="gpt-4",
            provider="openai",
            is_final=True,
            finish_reason="stop",
        )
        assert chunk.is_final is True
        assert chunk.finish_reason == "stop"


class TestUtilityFunctions:
    """Tests for utility functions."""

    def test_create_message(self):
        """Test create_message helper."""
        msg = create_message("user", "Hello", importance="high")
        assert msg.role == "user"
        assert msg.content == "Hello"
        assert msg.metadata["importance"] == "high"

    def test_messages_from_dicts(self):
        """Test converting list of dicts to messages."""
        dicts = [
            {"role": "system", "content": "You are helpful."},
            {"role": "user", "content": "Hello"},
        ]
        messages = messages_from_dicts(dicts)
        assert len(messages) == 2
        assert messages[0].role == "system"
        assert messages[1].content == "Hello"

    def test_messages_to_dicts(self):
        """Test converting list of messages to dicts."""
        messages = [
            LLMMessage(role="user", content="Hi"),
            LLMMessage(role="assistant", content="Hello!"),
        ]
        dicts = messages_to_dicts(messages)
        assert len(dicts) == 2
        assert dicts[0]["role"] == "user"
        assert dicts[1]["content"] == "Hello!"


class TestLLMMessageEdgeCases:
    """Edge case tests for LLMMessage."""

    def test_message_with_name(self):
        """Test message with function name."""
        msg = LLMMessage(role="function", content="result", name="get_weather")
        assert msg.name == "get_weather"
        d = msg.to_dict()
        assert d["name"] == "get_weather"

    def test_message_with_tool_call(self):
        """Test message with tool call ID."""
        msg = LLMMessage(role="tool", content="42", tool_call_id="call_abc123")
        assert msg.tool_call_id == "call_abc123"
        d = msg.to_dict()
        assert d["tool_call_id"] == "call_abc123"

    def test_message_from_dict_all_fields(self):
        """Test from_dict with all optional fields."""
        d = {
            "role": "tool",
            "content": "result",
            "name": "calculator",
            "tool_call_id": "call_xyz",
            "metadata": {"extra": "data"},
        }
        msg = LLMMessage.from_dict(d)
        assert msg.name == "calculator"
        assert msg.tool_call_id == "call_xyz"
        assert msg.metadata["extra"] == "data"


class TestLLMResponseEdgeCases:
    """Edge case tests for LLMResponse."""

    def test_response_with_empty_content(self):
        """Test response with empty content."""
        resp = LLMResponse(content="", model="test", provider="test")
        assert resp.content == ""

    def test_response_defaults(self):
        """Test response default values."""
        resp = LLMResponse(content="test", model="model")
        assert resp.provider == ""
        assert resp.tokens_used == 0
        assert resp.prompt_tokens == 0
        assert resp.completion_tokens == 0
        assert resp.response_time == 0.0
        assert resp.finish_reason == "stop"
        assert resp.cost == 0.0
        assert resp.metadata == {}


class TestStreamChunkEdgeCases:
    """Edge case tests for StreamChunk."""

    def test_chunk_with_metadata(self):
        """Test chunk with metadata information."""
        chunk = StreamChunk(
            content="Hello",
            model="gpt-4",
            provider="openai",
            metadata={"usage": 5},
        )
        assert chunk.metadata["usage"] == 5

    def test_chunk_defaults(self):
        """Test chunk default values."""
        chunk = StreamChunk(content="test", model="test")
        assert chunk.provider == ""
        assert chunk.is_final is False
        assert chunk.finish_reason is None
        assert chunk.metadata == {}
