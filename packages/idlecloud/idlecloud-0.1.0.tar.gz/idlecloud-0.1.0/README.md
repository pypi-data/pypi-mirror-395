# IdleCloud Python SDK

[![PyPI version](https://badge.fury.io/py/idlecloud.svg)](https://badge.fury.io/py/idlecloud)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Official Python SDK for [IdleCloud](https://idlecloud.ai) - Decentralized AI inference powered by idle GPU infrastructure.

> **Early Access:** IdleCloud is currently in private alpha. API access is by invitation only. Join our waitlist at [idlecloud.ai](https://idlecloud.ai).

## What is IdleCloud?

IdleCloud transforms idle mining rigs and GPUs into decentralized infrastructure for AI inference. By leveraging underutilized compute resources, we provide OpenAI-compatible LLM inference at a fraction of the cost.

## Features

- **Drop-in OpenAI compatibility** - Works with OpenAI's Python SDK
- **Easy to use** - Just set your API key and you're ready to go
- **Streaming support** - Real-time token streaming
- **Async/await** - Full async support for modern Python applications
- **Minimal dependencies** - Only depends on `openai` package
- **Type hints** - Full type annotations for better IDE support

## Installation

```bash
pip install idlecloud
```

## Quick Start

### 1. Get Your API Key

Request API access at [idlecloud.ai](https://idlecloud.ai). Once approved, you'll receive your API key.

### 2. Set Environment Variable

```bash
export IDLECLOUD_API_KEY="ic_..."
```

### 3. Use the SDK

```python
from idlecloud import IdleCloud

# Client reads API key from IDLECLOUD_API_KEY environment variable
client = IdleCloud()

# Create a completion
response = client.chat.completions.create(
    model="gpt-oss-20b",
    messages=[
        {"role": "user", "content": "What is the capital of France?"}
    ]
)

print(response.choices[0].message.content)
```

## Usage Examples

### Basic Completion

```python
from idlecloud import IdleCloud

client = IdleCloud(api_key="ic_...")

response = client.chat.completions.create(
    model="gpt-oss-20b",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing in simple terms."}
    ],
    temperature=0.7,
    max_tokens=150
)

print(response.choices[0].message.content)
print(f"Tokens used: {response.usage.total_tokens}")
```

### Streaming

```python
from idlecloud import IdleCloud

client = IdleCloud()

stream = client.chat.completions.create(
    model="gpt-oss-20b",
    messages=[{"role": "user", "content": "Write a short poem about AI"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)

print()  # Newline after streaming
```

### Async Usage

```python
import asyncio
from idlecloud import AsyncIdleCloud

async def main():
    client = AsyncIdleCloud()

    response = await client.chat.completions.create(
        model="gpt-oss-20b",
        messages=[{"role": "user", "content": "Hello!"}]
    )

    print(response.choices[0].message.content)

asyncio.run(main())
```

### Async Streaming

```python
import asyncio
from idlecloud import AsyncIdleCloud

async def main():
    client = AsyncIdleCloud()

    stream = await client.chat.completions.create(
        model="gpt-oss-20b",
        messages=[{"role": "user", "content": "Count to 5"}],
        stream=True
    )

    async for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)

    print()

asyncio.run(main())
```

### Error Handling

```python
from idlecloud import IdleCloud
from openai import APIError, RateLimitError, AuthenticationError

client = IdleCloud()

try:
    response = client.chat.completions.create(
        model="gpt-oss-20b",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print(response.choices[0].message.content)

except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
except APIError as e:
    print(f"API error: {e}")
```

### Advanced Configuration

```python
from idlecloud import IdleCloud

client = IdleCloud(
    api_key="ic_...",
    timeout=30.0,  # Request timeout in seconds
    max_retries=3,  # Number of retries on failure
    default_headers={
        "X-Custom-Header": "value"
    }
)

response = client.chat.completions.create(...)
```

## Migration from OpenAI

If you're already using OpenAI's Python SDK, migration is simple:

### Before (OpenAI)

```python
from openai import OpenAI

client = OpenAI(api_key="sk-...")

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### After (IdleCloud)

**Option 1: Use IdleCloud SDK (recommended)**

```python
from idlecloud import IdleCloud

client = IdleCloud(api_key="ic_...")  # Change 1: Import and API key

response = client.chat.completions.create(
    model="gpt-oss-20b",  # Change 2: Model name
    messages=[{"role": "user", "content": "Hello!"}]
)
```

**Option 2: Keep using OpenAI SDK**

```python
from openai import OpenAI

client = OpenAI(
    api_key="ic_...",  # Change 1: API key
    base_url="https://api.idlecloud.ai/v1"  # Change 2: Base URL
)

response = client.chat.completions.create(
    model="gpt-oss-20b",  # Change 3: Model name
    messages=[{"role": "user", "content": "Hello!"}]
)
```

Both options work identically! The IdleCloud SDK is just a convenience wrapper.

## Environment Variables

The SDK supports the following environment variables:

- `IDLECLOUD_API_KEY` - Your IdleCloud API key (required if not passed to constructor)
- `IDLECLOUD_BASE_URL` - Custom API base URL (optional, defaults to `https://api.idlecloud.ai/v1`)

## Available Models

Currently available models:

- `gpt-oss-20b` - General-purpose 20B parameter model optimized for cost and performance

More models coming soon! Check [idlecloud.ai/models](https://idlecloud.ai/models) for the latest list.

## API Reference

The IdleCloud SDK is a thin wrapper around OpenAI's Python SDK. All methods, parameters, and return types are identical to OpenAI's SDK.

For full API documentation, see:
- [OpenAI Python SDK Documentation](https://github.com/openai/openai-python)
- [IdleCloud API Documentation](https://docs.idlecloud.ai)

### Key Classes

- `IdleCloud` - Synchronous client (inherits from `openai.OpenAI`)
- `AsyncIdleCloud` - Asynchronous client (inherits from `openai.AsyncOpenAI`)

### Constructor Parameters

Both `IdleCloud` and `AsyncIdleCloud` accept:

- `api_key` (str, optional) - Your API key. Defaults to `IDLECLOUD_API_KEY` env var.
- `base_url` (str, optional) - API base URL. Defaults to `https://api.idlecloud.ai/v1`.
- `timeout` (float, optional) - Request timeout in seconds. Default: 600.
- `max_retries` (int, optional) - Maximum number of retries. Default: 2.
- `default_headers` (dict, optional) - Headers to include in all requests.
- `default_query` (dict, optional) - Query parameters to include in all requests.

All parameters from OpenAI's SDK are supported.

## Development

### Install from Source

```bash
pip install idlecloud
# For development, contact alex@idlecloud.ai for repository access
```

### Run Tests

```bash
# Set API key for integration tests
export IDLECLOUD_API_KEY="ic_..."

# Run all tests
pytest

# Run specific test file
pytest tests/test_basic.py

# Run with coverage
pytest --cov=idlecloud tests/
```

### Run Examples

```bash
cd examples
python basic_usage.py
python streaming.py
python async_usage.py
```

## FAQ

### Is this compatible with OpenAI's SDK?

Yes! IdleCloud's API is fully compatible with OpenAI's API. You can use either:
1. Our IdleCloud SDK (thin wrapper with IdleCloud defaults)
2. OpenAI's SDK directly with `base_url="https://api.idlecloud.ai/v1"`

Both work identically.

### What models are supported?

Currently we support `gpt-oss-20b`, a general-purpose 20B parameter model. More models coming soon.

### How is IdleCloud different from OpenAI?

IdleCloud provides OpenAI-compatible LLM inference at a significantly lower cost by leveraging distributed GPU resources. Same API, lower prices.

### Can I use this with LangChain, LlamaIndex, etc?

Yes! Any tool that works with OpenAI's SDK will work with IdleCloud. Just change the API key and base URL (or use our SDK).

### What about rate limits?

Rate limits depend on your plan. Free tier includes 10 requests/minute. See [idlecloud.ai/pricing](https://idlecloud.ai/pricing) for details.

## Support

- Email: [alex@idlecloud.ai](mailto:alex@idlecloud.ai)
- Website: [idlecloud.ai](https://idlecloud.ai)
- Documentation: [idlecloud.ai/docs](https://idlecloud.ai/docs)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Version History

### 0.1.0 (2025-12-05)
- Initial alpha release
- Chat completions support
- Streaming support
- Async/await support
- OpenAI SDK compatibility
- Early access program

---

**Built by the IdleCloud team**
