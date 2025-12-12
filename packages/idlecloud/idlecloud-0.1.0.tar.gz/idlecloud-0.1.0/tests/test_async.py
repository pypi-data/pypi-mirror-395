"""
Async tests for IdleCloud SDK.

Tests asynchronous chat completions and streaming.
"""

import os
import pytest

from idlecloud import AsyncIdleCloud


class TestAsyncClientInitialization:
    """Test async client initialization."""

    def test_init_with_explicit_api_key(self):
        """Test async client initialization with explicit API key."""
        client = AsyncIdleCloud(api_key="ic_test_key")
        assert client.api_key == "ic_test_key"

    def test_init_with_env_var(self):
        """Test async client initialization with environment variable."""
        with pytest.mock.patch.dict(os.environ, {"IDLECLOUD_API_KEY": "ic_env_key"}):
            client = AsyncIdleCloud()
            assert client.api_key == "ic_env_key"

    def test_init_without_api_key_raises_error(self):
        """Test that missing API key raises ValueError."""
        with pytest.mock.patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="No API key provided"):
                AsyncIdleCloud()

    def test_base_url_default(self):
        """Test that default base URL is set correctly."""
        client = AsyncIdleCloud(api_key="ic_test")
        assert client.base_url == "https://api.idlecloud.ai/v1"


@pytest.mark.asyncio
class TestAsyncCompletion:
    """Test async chat completions."""

    @pytest.fixture
    def client(self):
        """Create an async test client."""
        if not os.environ.get("IDLECLOUD_API_KEY"):
            pytest.skip("Requires IDLECLOUD_API_KEY environment variable")
        return AsyncIdleCloud()

    async def test_client_has_chat_attribute(self, client):
        """Test that async client has chat.completions interface."""
        assert hasattr(client, "chat")
        assert hasattr(client.chat, "completions")
        assert hasattr(client.chat.completions, "create")

    async def test_basic_async_completion(self, client):
        """Test basic async completion."""
        response = await client.chat.completions.create(
            model="gpt-oss-20b",
            messages=[
                {"role": "user", "content": "Say 'test successful'"}
            ],
            max_tokens=10
        )

        # Verify response structure
        assert response.id is not None
        assert response.object == "chat.completion"
        assert len(response.choices) > 0
        assert response.choices[0].message.content is not None
        assert response.usage.total_tokens > 0

    async def test_async_response_structure(self, client):
        """Test async response structure."""
        response = await client.chat.completions.create(
            model="gpt-oss-20b",
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=5
        )

        # Test response attributes
        assert hasattr(response, "id")
        assert hasattr(response, "choices")
        assert hasattr(response, "usage")

        # Test message structure
        message = response.choices[0].message
        assert message.role == "assistant"
        assert message.content is not None

    async def test_async_with_system_message(self, client):
        """Test async completion with system message."""
        response = await client.chat.completions.create(
            model="gpt-oss-20b",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is 2+2?"}
            ],
            max_tokens=20
        )

        assert response.choices[0].message.content is not None

    async def test_async_with_temperature(self, client):
        """Test async completion with temperature parameter."""
        response = await client.chat.completions.create(
            model="gpt-oss-20b",
            messages=[{"role": "user", "content": "Hi"}],
            temperature=0.5,
            max_tokens=10
        )

        assert response.choices[0].message.content is not None


@pytest.mark.asyncio
class TestAsyncStreaming:
    """Test async streaming completions."""

    @pytest.fixture
    def client(self):
        """Create an async test client."""
        if not os.environ.get("IDLECLOUD_API_KEY"):
            pytest.skip("Requires IDLECLOUD_API_KEY environment variable")
        return AsyncIdleCloud()

    async def test_async_streaming_returns_async_generator(self, client):
        """Test that async streaming returns an async generator."""
        stream = await client.chat.completions.create(
            model="gpt-oss-20b",
            messages=[{"role": "user", "content": "Hi"}],
            stream=True,
            max_tokens=5
        )

        # Should have async iteration protocol
        assert hasattr(stream, "__aiter__")

    async def test_async_streaming_chunks(self, client):
        """Test async streaming chunk structure."""
        stream = await client.chat.completions.create(
            model="gpt-oss-20b",
            messages=[{"role": "user", "content": "Count to 3"}],
            stream=True,
            max_tokens=20
        )

        chunks = []
        async for chunk in stream:
            chunks.append(chunk)

        assert len(chunks) > 0

        # Check chunk structure
        first_chunk = chunks[0]
        assert hasattr(first_chunk, "id")
        assert first_chunk.object == "chat.completion.chunk"
        assert hasattr(first_chunk, "choices")

    async def test_async_streaming_accumulation(self, client):
        """Test async streaming token accumulation."""
        stream = await client.chat.completions.create(
            model="gpt-oss-20b",
            messages=[{"role": "user", "content": "Say 'hello'"}],
            stream=True,
            max_tokens=10
        )

        accumulated = ""
        async for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                accumulated += delta.content

        assert len(accumulated) > 0

    async def test_async_streaming_multiple_chunks(self, client):
        """Test that async streaming produces multiple chunks."""
        stream = await client.chat.completions.create(
            model="gpt-oss-20b",
            messages=[{"role": "user", "content": "Count from 1 to 10"}],
            stream=True,
            max_tokens=50
        )

        chunk_count = 0
        async for chunk in stream:
            chunk_count += 1
            assert hasattr(chunk, "choices")

        assert chunk_count > 1


@pytest.mark.asyncio
class TestAsyncConcurrency:
    """Test concurrent async requests."""

    @pytest.fixture
    def client(self):
        """Create an async test client."""
        if not os.environ.get("IDLECLOUD_API_KEY"):
            pytest.skip("Requires IDLECLOUD_API_KEY environment variable")
        return AsyncIdleCloud()

    async def test_concurrent_requests(self, client):
        """Test multiple concurrent async requests."""
        import asyncio

        # Create multiple tasks
        tasks = [
            client.chat.completions.create(
                model="gpt-oss-20b",
                messages=[{"role": "user", "content": f"Say number {i}"}],
                max_tokens=5
            )
            for i in range(3)
        ]

        # Wait for all to complete
        responses = await asyncio.gather(*tasks)

        # All should succeed
        assert len(responses) == 3
        for response in responses:
            assert response.choices[0].message.content is not None

    async def test_concurrent_streaming(self, client):
        """Test multiple concurrent async streams."""
        import asyncio

        async def consume_stream(stream):
            """Consume a stream and return accumulated content."""
            accumulated = ""
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    accumulated += chunk.choices[0].delta.content
            return accumulated

        # Create multiple streams
        streams = [
            await client.chat.completions.create(
                model="gpt-oss-20b",
                messages=[{"role": "user", "content": f"Number {i}"}],
                stream=True,
                max_tokens=10
            )
            for i in range(2)
        ]

        # Consume all streams concurrently
        results = await asyncio.gather(*[consume_stream(s) for s in streams])

        # All should have content
        assert len(results) == 2
        for result in results:
            assert len(result) > 0


@pytest.mark.asyncio
class TestAsyncErrorHandling:
    """Test async error handling."""

    async def test_async_invalid_model(self):
        """Test async request with invalid model."""
        if not os.environ.get("IDLECLOUD_API_KEY"):
            pytest.skip("Requires IDLECLOUD_API_KEY environment variable")

        client = AsyncIdleCloud()

        with pytest.raises(Exception):
            await client.chat.completions.create(
                model="invalid-model",
                messages=[{"role": "user", "content": "Hi"}]
            )
