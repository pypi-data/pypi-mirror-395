# SEE Python SDK

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](http://mypy-lang.org/)

A modern Python SDK for interacting with SEE services, featuring async support, full type safety, and Python 3.11+ capabilities.

## Features

- 🚀 **Modern Python**: Built with Python 3.11+ features (type hints, pattern matching, dataclasses)
- 🔄 **Async First**: Fully async API based on `asyncio` and `httpx`
- 📝 **Type Safe**: 100% type annotated with mypy strict mode support
- 🛡️ **Reliable**: Built-in retry mechanism, error handling, and rate limiting
- 🧪 **Well Tested**: Comprehensive test suite with pytest
- 📦 **Standard Compliant**: Follows PEP 517/518 with `pyproject.toml`

## Requirements

- Python 3.11+
- httpx >= 0.27.0

## Installation

```bash
pip install see-sdk
```

Install from source:

```bash
git clone https://github.com/yourusername/see-sdk.git
cd see-sdk
pip install -e .
```

## Quick Start

### Environment Setup

Set your API key as an environment variable:

```bash
export SEE_API_KEY="your-api-key-here"
```

### Basic Usage

```python
import asyncio
import os
from see import SeeClient
from see.models import CreateShortUrlRequest

async def main():
    api_key = os.getenv("SEE_API_KEY")
    
    async with SeeClient(api_key=api_key) as client:
        request = CreateShortUrlRequest(
            domain="s.ee",
            target_url="https://example.com/very/long/url",
            title="Example Short URL"
        )
        
        response = await client.create_short_url(request)
        print(f"Code: {response.code}")
        print(f"Message: {response.message}")
        print(f"Data: {response.data}")

asyncio.run(main())
```

### Custom Short URL

```python
import asyncio
import os
from datetime import datetime, timedelta
from see import SeeClient
from see.models import CreateShortUrlRequest

async def create_custom_url():
    api_key = os.getenv("SEE_API_KEY")
    
    async with SeeClient(api_key=api_key) as client:
        expire_time = int((datetime.now() + timedelta(days=30)).timestamp())
        
        request = CreateShortUrlRequest(
            domain="s.ee",
            target_url="https://example.com/product/123",
            custom_slug="product123",
            title="Product 123",
            expire_at=expire_time,
            tag_ids=[1, 2]
        )
        
        response = await client.create_short_url(request)
        print(f"Custom URL: {response.data}")

asyncio.run(create_custom_url())
```

### Managing URLs

```python
import asyncio
import os
from see import SeeClient
from see.models import UpdateShortUrlRequest, DeleteShortUrlRequest

async def manage_urls():
    api_key = os.getenv("SEE_API_KEY")
    
    async with SeeClient(api_key=api_key) as client:
        # Update
        update_request = UpdateShortUrlRequest(
            domain="s.ee",
            slug="abc123",
            target_url="https://example.com/new-destination",
            title="Updated Title"
        )
        updated = await client.update_short_url(update_request)
        
        # Delete
        delete_request = DeleteShortUrlRequest(
            domain="s.ee",
            slug="abc123"
        )
        deleted = await client.delete_short_url(delete_request)

asyncio.run(manage_urls())
```

### Domains and Tags

```python
import asyncio
import os
from see import SeeClient

async def get_metadata():
    api_key = os.getenv("SEE_API_KEY")
    
    async with SeeClient(api_key=api_key) as client:
        domains = await client.get_domains()
        print(f"Domains: {domains.data}")
        
        tags = await client.get_tags()
        print(f"Tags: {tags.data}")

asyncio.run(get_metadata())
```

## Advanced Usage

### Custom Configuration

```python
import os
from see import SeeClient

api_key = os.getenv("SEE_API_KEY")

# Create a client with custom configuration
async with SeeClient(
    api_key=api_key,
    base_url="https://s.ee/api",
    timeout=60.0,
    max_retries=5,
    proxy=None
) as client:
    # Use the client...
    pass
```

### Error Handling

```python
import asyncio
import os
from see import SeeClient
from see.models import CreateShortUrlRequest
from see.exceptions import (
    ValidationError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    APIError
)

async def safe_create_url():
    api_key = os.getenv("SEE_API_KEY")
    
    async with SeeClient(api_key=api_key) as client:
        try:
            request = CreateShortUrlRequest(
                domain="s.ee",
                target_url="https://example.com",
                title="Example"
            )
            response = await client.create_short_url(request)
        except ValidationError as e:
            print(f"Validation error: {e}")
        except AuthenticationError as e:
            print(f"Authentication failed: {e}")
        except RateLimitError as e:
            print(f"Rate limit: {e}")
        except NotFoundError as e:
            print(f"Not found: {e}")
        except APIError as e:
            print(f"API error: {e}")

asyncio.run(safe_create_url())
```

## Development

### Setup

```bash
git clone https://github.com/yourusername/see-sdk.git
cd see-sdk

python -m venv venv
source venv/bin/activate  # Linux/macOS

pip install -e ".[dev]"
pre-commit install
```

### Testing

```bash
pytest
pytest --cov=see --cov-report=html
pytest tests/test_client.py
```

### Code Quality

```bash
black src/ tests/
ruff check src/ tests/
mypy src/
```

## API Reference

### SeeClient

Main client class for API interactions.

#### Methods

- `create_short_url(request)` - Create short URL
- `update_short_url(request)` - Update short URL
- `delete_short_url(request)` - Delete short URL
- `get_domains()` - Get available domains
- `get_tags()` - Get available tags

### Models

#### CreateShortUrlRequest

```python
@dataclass
class CreateShortUrlRequest:
    domain: str
    target_url: str
    title: str
    custom_slug: str | None = None
    expire_at: int | None = None
    tag_ids: list[int] | None = None
```

### Exceptions

- `SeeError` - Base exception
- `APIError` - API error
- `AuthenticationError` - Authentication error
- `ValidationError` - Validation error
- `RateLimitError` - Rate limit error
- `NotFoundError` - Not found error

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT License - see [LICENSE](LICENSE) file.