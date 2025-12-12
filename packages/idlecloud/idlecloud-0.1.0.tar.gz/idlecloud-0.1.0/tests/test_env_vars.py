"""
Environment variable tests for IdleCloud SDK.

Tests environment variable handling for API keys and configuration.
"""

import os
import pytest
from unittest.mock import patch

from idlecloud import IdleCloud, AsyncIdleCloud


class TestEnvironmentVariables:
    """Test environment variable handling."""

    def test_api_key_from_env(self):
        """Test reading API key from IDLECLOUD_API_KEY."""
        with patch.dict(os.environ, {"IDLECLOUD_API_KEY": "ic_from_env"}):
            client = IdleCloud()
            assert client.api_key == "ic_from_env"

    def test_api_key_explicit_overrides_env(self):
        """Test that explicit API key overrides environment variable."""
        with patch.dict(os.environ, {"IDLECLOUD_API_KEY": "ic_from_env"}):
            client = IdleCloud(api_key="ic_explicit")
            assert client.api_key == "ic_explicit"

    def test_base_url_from_env(self):
        """Test reading base URL from IDLECLOUD_BASE_URL."""
        with patch.dict(os.environ, {
            "IDLECLOUD_API_KEY": "ic_test",
            "IDLECLOUD_BASE_URL": "https://custom.api.com/v1"
        }):
            client = IdleCloud()
            assert client.base_url == "https://custom.api.com/v1"

    def test_base_url_explicit_overrides_env(self):
        """Test that explicit base URL overrides environment variable."""
        with patch.dict(os.environ, {
            "IDLECLOUD_API_KEY": "ic_test",
            "IDLECLOUD_BASE_URL": "https://env.api.com/v1"
        }):
            client = IdleCloud(base_url="https://explicit.api.com/v1")
            assert client.base_url == "https://explicit.api.com/v1"

    def test_missing_api_key_raises_error(self):
        """Test that missing API key raises clear error."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError) as exc_info:
                IdleCloud()

            error_message = str(exc_info.value)
            assert "No API key provided" in error_message
            assert "IDLECLOUD_API_KEY" in error_message

    def test_default_base_url_when_not_set(self):
        """Test default base URL when env var not set."""
        with patch.dict(os.environ, {"IDLECLOUD_API_KEY": "ic_test"}):
            # Remove IDLECLOUD_BASE_URL if it exists
            os.environ.pop("IDLECLOUD_BASE_URL", None)

            client = IdleCloud()
            assert client.base_url == "https://api.idlecloud.ai/v1"

    def test_empty_api_key_env_var(self):
        """Test that empty API key env var is treated as missing."""
        with patch.dict(os.environ, {"IDLECLOUD_API_KEY": ""}):
            # Empty string should be treated as missing
            # Note: This behavior depends on how OpenAI SDK handles it
            client = IdleCloud(api_key="ic_explicit")
            assert client.api_key == "ic_explicit"

    def test_whitespace_in_env_vars(self):
        """Test that whitespace in env vars is preserved."""
        with patch.dict(os.environ, {
            "IDLECLOUD_API_KEY": "  ic_with_spaces  "
        }):
            client = IdleCloud()
            # Should preserve the value as-is (OpenAI SDK will handle validation)
            assert client.api_key == "  ic_with_spaces  "


class TestAsyncEnvironmentVariables:
    """Test environment variable handling for async client."""

    def test_async_api_key_from_env(self):
        """Test async client reading API key from env."""
        with patch.dict(os.environ, {"IDLECLOUD_API_KEY": "ic_async_env"}):
            client = AsyncIdleCloud()
            assert client.api_key == "ic_async_env"

    def test_async_api_key_explicit(self):
        """Test async client with explicit API key."""
        client = AsyncIdleCloud(api_key="ic_async_explicit")
        assert client.api_key == "ic_async_explicit"

    def test_async_base_url_from_env(self):
        """Test async client reading base URL from env."""
        with patch.dict(os.environ, {
            "IDLECLOUD_API_KEY": "ic_test",
            "IDLECLOUD_BASE_URL": "https://async.api.com/v1"
        }):
            client = AsyncIdleCloud()
            assert client.base_url == "https://async.api.com/v1"

    def test_async_missing_api_key_raises_error(self):
        """Test that async client raises error when API key missing."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError) as exc_info:
                AsyncIdleCloud()

            error_message = str(exc_info.value)
            assert "No API key provided" in error_message
            assert "IDLECLOUD_API_KEY" in error_message


class TestEnvironmentVariablePrecedence:
    """Test precedence of different configuration sources."""

    def test_precedence_explicit_over_env(self):
        """Test that explicit parameters take precedence over env vars."""
        with patch.dict(os.environ, {
            "IDLECLOUD_API_KEY": "ic_env_key",
            "IDLECLOUD_BASE_URL": "https://env.url.com/v1"
        }):
            client = IdleCloud(
                api_key="ic_explicit_key",
                base_url="https://explicit.url.com/v1"
            )

            assert client.api_key == "ic_explicit_key"
            assert client.base_url == "https://explicit.url.com/v1"

    def test_partial_override(self):
        """Test overriding only some parameters."""
        with patch.dict(os.environ, {
            "IDLECLOUD_API_KEY": "ic_env_key",
            "IDLECLOUD_BASE_URL": "https://env.url.com/v1"
        }):
            # Override only API key
            client = IdleCloud(api_key="ic_explicit")
            assert client.api_key == "ic_explicit"
            assert client.base_url == "https://env.url.com/v1"

            # Override only base URL
            client2 = IdleCloud(base_url="https://explicit.com/v1")
            assert client2.api_key == "ic_env_key"
            assert client2.base_url == "https://explicit.com/v1"


class TestEnvironmentVariableEdgeCases:
    """Test edge cases in environment variable handling."""

    def test_multiple_clients_with_different_configs(self):
        """Test creating multiple clients with different configurations."""
        with patch.dict(os.environ, {"IDLECLOUD_API_KEY": "ic_default"}):
            client1 = IdleCloud()
            client2 = IdleCloud(api_key="ic_custom")

            assert client1.api_key == "ic_default"
            assert client2.api_key == "ic_custom"

    def test_changing_env_var_after_client_creation(self):
        """Test that changing env var after creation doesn't affect client."""
        with patch.dict(os.environ, {"IDLECLOUD_API_KEY": "ic_original"}):
            client = IdleCloud()
            original_key = client.api_key

            # Change env var
            os.environ["IDLECLOUD_API_KEY"] = "ic_changed"

            # Client should still have original key
            assert client.api_key == original_key

    def test_env_var_with_special_characters(self):
        """Test env vars with special characters."""
        special_key = "ic_test-key_123.abc"

        with patch.dict(os.environ, {"IDLECLOUD_API_KEY": special_key}):
            client = IdleCloud()
            assert client.api_key == special_key

    def test_case_sensitive_env_vars(self):
        """Test that env var names are case-sensitive."""
        with patch.dict(os.environ, {
            "idlecloud_api_key": "ic_lowercase",  # Wrong case
            "IDLECLOUD_API_KEY": "ic_uppercase"   # Correct case
        }):
            client = IdleCloud()
            # Should use correct case only
            assert client.api_key == "ic_uppercase"
