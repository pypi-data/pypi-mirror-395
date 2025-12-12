"""
IdleCloud Python SDK

A thin wrapper around OpenAI's Python SDK that provides seamless access to
IdleCloud's OpenAI-compatible inference API.

Example:
    Basic usage with environment variable:
        >>> from idlecloud import IdleCloud
        >>> client = IdleCloud()  # Reads IDLECLOUD_API_KEY
        >>> response = client.chat.completions.create(
        ...     model="gpt-oss-20b",
        ...     messages=[{"role": "user", "content": "Hello!"}]
        ... )

    Explicit API key:
        >>> client = IdleCloud(api_key="ic_...")
        >>> response = client.chat.completions.create(...)

    Streaming:
        >>> stream = client.chat.completions.create(
        ...     model="gpt-oss-20b",
        ...     messages=[{"role": "user", "content": "Count to 5"}],
        ...     stream=True
        ... )
        >>> for chunk in stream:
        ...     print(chunk.choices[0].delta.content, end="")

    Async usage:
        >>> from idlecloud import AsyncIdleCloud
        >>> client = AsyncIdleCloud()
        >>> response = await client.chat.completions.create(...)
"""

import os
from typing import Optional

from openai import OpenAI as _OpenAI
from openai import AsyncOpenAI as _AsyncOpenAI

from ._version import __version__

__all__ = ["IdleCloud", "AsyncIdleCloud", "__version__"]


# Default configuration
DEFAULT_BASE_URL = "https://api.idlecloud.ai/v1"
ENV_VAR_API_KEY = "IDLECLOUD_API_KEY"
ENV_VAR_BASE_URL = "IDLECLOUD_BASE_URL"


class IdleCloud(_OpenAI):
    """
    Synchronous IdleCloud API client.

    This is a thin wrapper around OpenAI's client that automatically configures
    the base URL for IdleCloud's API and reads the API key from the
    IDLECLOUD_API_KEY environment variable by default.

    All methods and attributes from OpenAI's client are available. See:
    https://github.com/openai/openai-python for full documentation.

    Args:
        api_key: Your IdleCloud API key. If not provided, reads from
            IDLECLOUD_API_KEY environment variable.
        base_url: API base URL. Defaults to https://api.idlecloud.ai/v1.
            Can be overridden with IDLECLOUD_BASE_URL environment variable.
        **kwargs: Additional arguments passed to OpenAI client (timeout,
            max_retries, default_headers, etc.)

    Raises:
        ValueError: If no API key is provided and IDLECLOUD_API_KEY is not set.

    Example:
        >>> client = IdleCloud(api_key="ic_...")
        >>> response = client.chat.completions.create(
        ...     model="gpt-oss-20b",
        ...     messages=[{"role": "user", "content": "Hello!"}]
        ... )
        >>> print(response.choices[0].message.content)
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs,
    ) -> None:
        # Get API key from parameter or environment variable
        if api_key is None:
            api_key = os.environ.get(ENV_VAR_API_KEY)
            if api_key is None:
                raise ValueError(
                    f"No API key provided. Either pass api_key parameter or set "
                    f"{ENV_VAR_API_KEY} environment variable."
                )

        # Get base URL from parameter, environment variable, or use default
        if base_url is None:
            base_url = os.environ.get(ENV_VAR_BASE_URL, DEFAULT_BASE_URL)

        # Initialize parent OpenAI client with IdleCloud configuration
        super().__init__(api_key=api_key, base_url=base_url, **kwargs)


class AsyncIdleCloud(_AsyncOpenAI):
    """
    Asynchronous IdleCloud API client.

    This is a thin wrapper around OpenAI's async client that automatically
    configures the base URL for IdleCloud's API and reads the API key from
    the IDLECLOUD_API_KEY environment variable by default.

    All methods and attributes from OpenAI's async client are available. See:
    https://github.com/openai/openai-python for full documentation.

    Args:
        api_key: Your IdleCloud API key. If not provided, reads from
            IDLECLOUD_API_KEY environment variable.
        base_url: API base URL. Defaults to https://api.idlecloud.ai/v1.
            Can be overridden with IDLECLOUD_BASE_URL environment variable.
        **kwargs: Additional arguments passed to OpenAI client (timeout,
            max_retries, default_headers, etc.)

    Raises:
        ValueError: If no API key is provided and IDLECLOUD_API_KEY is not set.

    Example:
        >>> import asyncio
        >>> from idlecloud import AsyncIdleCloud
        >>>
        >>> async def main():
        ...     client = AsyncIdleCloud(api_key="ic_...")
        ...     response = await client.chat.completions.create(
        ...         model="gpt-oss-20b",
        ...         messages=[{"role": "user", "content": "Hello!"}]
        ...     )
        ...     print(response.choices[0].message.content)
        >>>
        >>> asyncio.run(main())
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs,
    ) -> None:
        # Get API key from parameter or environment variable
        if api_key is None:
            api_key = os.environ.get(ENV_VAR_API_KEY)
            if api_key is None:
                raise ValueError(
                    f"No API key provided. Either pass api_key parameter or set "
                    f"{ENV_VAR_API_KEY} environment variable."
                )

        # Get base URL from parameter, environment variable, or use default
        if base_url is None:
            base_url = os.environ.get(ENV_VAR_BASE_URL, DEFAULT_BASE_URL)

        # Initialize parent AsyncOpenAI client with IdleCloud configuration
        super().__init__(api_key=api_key, base_url=base_url, **kwargs)
