"""
Basic tests for IdleCloud SDK.

Tests client initialization, basic completions, and response parsing.
"""

import os
import pytest
from unittest.mock import Mock, patch

from idlecloud import IdleCloud, __version__


class TestClientInitialization:
    """Test client initialization and configuration."""

    def test_version_exists(self):
        """Test that version is defined."""
        assert __version__ == "1.0.0"

    def test_init_with_explicit_api_key(self):
        """Test initialization with explicit API key."""
        client = IdleCloud(api_key="ic_test_key")
        assert client.api_key == "ic_test_key"

    def test_init_with_env_var(self):
        """Test initialization with environment variable."""
        with patch.dict(os.environ, {"IDLECLOUD_API_KEY": "ic_env_key"}):
            client = IdleCloud()
            assert client.api_key == "ic_env_key"

    def test_init_without_api_key_raises_error(self):
        """Test that missing API key raises ValueError."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="No API key provided"):
                IdleCloud()

    def test_base_url_default(self):
        """Test that default base URL is set correctly."""
        client = IdleCloud(api_key="ic_test")
        assert client.base_url == "https://api.idlecloud.ai/v1"

    def test_base_url_explicit(self):
        """Test explicit base URL override."""
        client = IdleCloud(
            api_key="ic_test",
            base_url="https://custom.api.com/v1"
        )
        assert client.base_url == "https://custom.api.com/v1"

    def test_base_url_from_env(self):
        """Test base URL from environment variable."""
        with patch.dict(os.environ, {
            "IDLECLOUD_API_KEY": "ic_test",
            "IDLECLOUD_BASE_URL": "https://env.api.com/v1"
        }):
            client = IdleCloud()
            assert client.base_url == "https://env.api.com/v1"

    def test_custom_timeout(self):
        """Test custom timeout configuration."""
        client = IdleCloud(api_key="ic_test", timeout=30.0)
        assert client.timeout == 30.0

    def test_custom_max_retries(self):
        """Test custom max retries configuration."""
        client = IdleCloud(api_key="ic_test", max_retries=5)
        assert client.max_retries == 5


class TestBasicCompletion:
    """Test basic chat completions (requires real API or mocking)."""

    @pytest.fixture
    def client(self):
        """Create a test client."""
        return IdleCloud(api_key="ic_test_key")

    def test_client_has_chat_attribute(self, client):
        """Test that client has chat.completions interface."""
        assert hasattr(client, "chat")
        assert hasattr(client.chat, "completions")
        assert hasattr(client.chat.completions, "create")

    @pytest.mark.skipif(
        not os.environ.get("IDLECLOUD_API_KEY"),
        reason="Requires IDLECLOUD_API_KEY environment variable"
    )
    def test_real_completion(self):
        """
        Integration test with real API.
        Only runs if IDLECLOUD_API_KEY is set.
        """
        client = IdleCloud()  # Uses env var

        response = client.chat.completions.create(
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


class TestResponseParsing:
    """Test response object parsing and access."""

    @pytest.mark.skipif(
        not os.environ.get("IDLECLOUD_API_KEY"),
        reason="Requires IDLECLOUD_API_KEY environment variable"
    )
    def test_response_structure(self):
        """Test that response has expected structure."""
        client = IdleCloud()

        response = client.chat.completions.create(
            model="gpt-oss-20b",
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=5
        )

        # Test response attributes
        assert hasattr(response, "id")
        assert hasattr(response, "object")
        assert hasattr(response, "created")
        assert hasattr(response, "model")
        assert hasattr(response, "choices")
        assert hasattr(response, "usage")

        # Test choices structure
        choice = response.choices[0]
        assert hasattr(choice, "index")
        assert hasattr(choice, "message")
        assert hasattr(choice, "finish_reason")

        # Test message structure
        message = choice.message
        assert hasattr(message, "role")
        assert hasattr(message, "content")
        assert message.role == "assistant"

        # Test usage structure
        usage = response.usage
        assert hasattr(usage, "prompt_tokens")
        assert hasattr(usage, "completion_tokens")
        assert hasattr(usage, "total_tokens")
        assert usage.total_tokens > 0


class TestErrorHandling:
    """Test error handling and validation."""

    def test_invalid_api_key_format(self):
        """Test that invalid API key format is handled."""
        # Note: This may not raise immediately, only on first API call
        client = IdleCloud(api_key="invalid_key")
        assert client.api_key == "invalid_key"

    @pytest.mark.skipif(
        not os.environ.get("IDLECLOUD_API_KEY"),
        reason="Requires IDLECLOUD_API_KEY environment variable"
    )
    def test_invalid_model_name(self):
        """Test that invalid model name raises error."""
        from openai import APIError

        client = IdleCloud()

        with pytest.raises(Exception):  # Could be APIError or other
            client.chat.completions.create(
                model="invalid-model-xyz",
                messages=[{"role": "user", "content": "test"}]
            )
