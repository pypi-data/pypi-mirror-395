# Getting Started

??? info "🤖 AI Summary"

    Install: `pip install python-opendota-sdk` or `uv add python-opendota-sdk`. Use async context manager: `async with OpenDota() as client`. Optional API key via env var `OPENDOTA_API_KEY` or constructor param for unlimited calls. Two output formats: `format='pydantic'` (default, type-safe) or `format='json'` (raw dicts).

## Installation

### From PyPI (Recommended)

```bash
pip install python-opendota-sdk
```

Or with uv:

```bash
uv add python-opendota-sdk
```

### From Source

```bash
git clone https://github.com/DeepBlueCoding/python-opendota-sdk.git
cd python-opendota-sdk
uv sync
```

## Authentication

The OpenDota API supports optional API keys for higher rate limits.

### Rate Limits

| Tier | Daily Calls | Per Minute |
|------|-------------|------------|
| Free | 2,000 | 60 |
| With API Key | Unlimited | Higher |

### Setting API Key

```python
# Option 1: Environment variable
import os
os.environ["OPENDOTA_API_KEY"] = "your-api-key"

# Option 2: Direct initialization
from opendota import OpenDota
client = OpenDota(api_key="your-api-key")
```

## Basic Usage

### Context Manager (Recommended)

```python
from opendota import OpenDota

async with OpenDota() as client:
    matches = await client.get_public_matches()
    # Client automatically closed when exiting context
```

### Manual Management

```python
from opendota import OpenDota

client = OpenDota()
try:
    matches = await client.get_public_matches()
finally:
    await client.close()
```

## Output Formats

Choose between structured Pydantic models or raw JSON dictionaries:

```python
# Pydantic models (default) - Full type safety
client = OpenDota(format='pydantic')
matches = await client.get_public_matches()
print(matches[0].match_id)  # Type-safe access

# JSON dictionaries - Direct API response
client = OpenDota(format='json')
matches = await client.get_public_matches()
print(matches[0]['match_id'])  # Dict access
```

## Next Steps

- Check out the [Examples](examples.md) for common use cases
- See the [API Reference](api/client.md) for all available methods
