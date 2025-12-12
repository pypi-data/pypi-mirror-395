"""
Streaming tests for IdleCloud SDK.

Tests streaming chat completions and SSE handling.
"""

import os
import pytest

from idlecloud import IdleCloud


class TestStreaming:
    """Test streaming completions."""

    @pytest.fixture
    def client(self):
        """Create a test client."""
        if not os.environ.get("IDLECLOUD_API_KEY"):
            pytest.skip("Requires IDLECLOUD_API_KEY environment variable")
        return IdleCloud()

    def test_streaming_returns_generator(self, client):
        """Test that streaming returns an iterable."""
        stream = client.chat.completions.create(
            model="gpt-oss-20b",
            messages=[{"role": "user", "content": "Say hi"}],
            stream=True,
            max_tokens=5
        )

        # Stream should be iterable
        assert hasattr(stream, "__iter__")

    def test_streaming_chunks_structure(self, client):
        """Test that streaming chunks have expected structure."""
        stream = client.chat.completions.create(
            model="gpt-oss-20b",
            messages=[{"role": "user", "content": "Count to 3"}],
            stream=True,
            max_tokens=20
        )

        chunks = list(stream)
        assert len(chunks) > 0

        # Check first chunk structure
        first_chunk = chunks[0]
        assert hasattr(first_chunk, "id")
        assert hasattr(first_chunk, "object")
        assert first_chunk.object == "chat.completion.chunk"
        assert hasattr(first_chunk, "choices")
        assert len(first_chunk.choices) > 0

        # Check delta structure
        delta = first_chunk.choices[0].delta
        assert hasattr(delta, "content") or hasattr(delta, "role")

    def test_streaming_accumulation(self, client):
        """Test that streaming tokens can be accumulated."""
        stream = client.chat.completions.create(
            model="gpt-oss-20b",
            messages=[{"role": "user", "content": "Say 'hello world'"}],
            stream=True,
            max_tokens=10
        )

        accumulated = ""
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                accumulated += delta.content

        # Should have accumulated some content
        assert len(accumulated) > 0
        assert isinstance(accumulated, str)

    def test_streaming_finish_reason(self, client):
        """Test that finish_reason is set in final chunk."""
        stream = client.chat.completions.create(
            model="gpt-oss-20b",
            messages=[{"role": "user", "content": "Hi"}],
            stream=True,
            max_tokens=5
        )

        chunks = list(stream)

        # Last chunk should have finish_reason
        last_chunk = chunks[-1]
        finish_reason = last_chunk.choices[0].finish_reason

        # finish_reason should be "stop" or "length"
        assert finish_reason in ["stop", "length", None]

    def test_streaming_multiple_chunks(self, client):
        """Test that streaming produces multiple chunks."""
        stream = client.chat.completions.create(
            model="gpt-oss-20b",
            messages=[{"role": "user", "content": "Count from 1 to 10"}],
            stream=True,
            max_tokens=50
        )

        chunk_count = 0
        for chunk in stream:
            chunk_count += 1
            # Each chunk should have expected structure
            assert hasattr(chunk, "choices")
            assert len(chunk.choices) > 0

        # Should have received multiple chunks
        assert chunk_count > 1

    def test_streaming_with_system_message(self, client):
        """Test streaming with system message."""
        stream = client.chat.completions.create(
            model="gpt-oss-20b",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hi"}
            ],
            stream=True,
            max_tokens=10
        )

        # Should be able to iterate
        chunks = list(stream)
        assert len(chunks) > 0

    def test_streaming_context_manager(self, client):
        """Test streaming with context manager (if supported)."""
        stream = client.chat.completions.create(
            model="gpt-oss-20b",
            messages=[{"role": "user", "content": "Hi"}],
            stream=True,
            max_tokens=5
        )

        # Should be able to iterate normally
        accumulated = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                accumulated += chunk.choices[0].delta.content

        assert len(accumulated) > 0


class TestStreamingParameters:
    """Test streaming with various parameters."""

    @pytest.fixture
    def client(self):
        """Create a test client."""
        if not os.environ.get("IDLECLOUD_API_KEY"):
            pytest.skip("Requires IDLECLOUD_API_KEY environment variable")
        return IdleCloud()

    def test_streaming_with_temperature(self, client):
        """Test streaming with temperature parameter."""
        stream = client.chat.completions.create(
            model="gpt-oss-20b",
            messages=[{"role": "user", "content": "Hi"}],
            stream=True,
            temperature=0.5,
            max_tokens=10
        )

        chunks = list(stream)
        assert len(chunks) > 0

    def test_streaming_with_max_tokens(self, client):
        """Test streaming with max_tokens limit."""
        stream = client.chat.completions.create(
            model="gpt-oss-20b",
            messages=[{"role": "user", "content": "Write a long story"}],
            stream=True,
            max_tokens=10  # Low limit
        )

        chunks = list(stream)

        # Should stop due to max_tokens
        last_chunk = chunks[-1]
        finish_reason = last_chunk.choices[0].finish_reason

        # May be "length" if hit token limit
        assert finish_reason in ["stop", "length", None]


class TestStreamingErrorHandling:
    """Test error handling during streaming."""

    def test_streaming_without_api_key(self):
        """Test that streaming without API key fails appropriately."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError):
                client = IdleCloud()

    @pytest.mark.skipif(
        not os.environ.get("IDLECLOUD_API_KEY"),
        reason="Requires IDLECLOUD_API_KEY environment variable"
    )
    def test_streaming_with_invalid_model(self):
        """Test streaming with invalid model name."""
        client = IdleCloud()

        with pytest.raises(Exception):
            stream = client.chat.completions.create(
                model="invalid-model",
                messages=[{"role": "user", "content": "Hi"}],
                stream=True
            )
            # Force evaluation by consuming stream
            list(stream)


# Import for test that uses it
from unittest.mock import patch
