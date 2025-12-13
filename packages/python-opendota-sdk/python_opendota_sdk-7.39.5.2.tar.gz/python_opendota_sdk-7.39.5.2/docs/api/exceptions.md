# Exceptions

??? info "🤖 AI Summary"

    Exception hierarchy: `OpenDotaError` (base) → `OpenDotaAPIError` (has `status_code`) → `OpenDotaRateLimitError` (429), `OpenDotaNotFoundError` (404). Catch specific exceptions first, fallback to `OpenDotaAPIError`. For rate limits, implement exponential backoff retry (2^attempt seconds).

Custom exceptions for handling API errors.

## Exception Hierarchy

```
OpenDotaError (base)
└── OpenDotaAPIError
    ├── OpenDotaRateLimitError
    └── OpenDotaNotFoundError
```

## OpenDotaError

Base exception for all OpenDota SDK errors.

```python
class OpenDotaError(Exception):
    """Base exception for OpenDota API errors."""
    pass
```

## OpenDotaAPIError

General API error with status code.

```python
class OpenDotaAPIError(OpenDotaError):
    def __init__(self, message: str, status_code: int):
        self.status_code = status_code
        super().__init__(message)
```

**Attributes:**

- `status_code` (int): HTTP status code from the API

## OpenDotaRateLimitError

Raised when API rate limit is exceeded (HTTP 429).

```python
class OpenDotaRateLimitError(OpenDotaAPIError):
    """Rate limit exceeded error."""
    pass
```

## OpenDotaNotFoundError

Raised when a resource is not found (HTTP 404).

```python
class OpenDotaNotFoundError(OpenDotaAPIError):
    """Resource not found error."""
    pass
```

## Error Handling Example

```python
from opendota import OpenDota
from opendota.exceptions import (
    OpenDotaAPIError,
    OpenDotaNotFoundError,
    OpenDotaRateLimitError
)

async with OpenDota() as client:
    try:
        match = await client.get_match(invalid_match_id)
    except OpenDotaNotFoundError:
        print("Match not found")
    except OpenDotaRateLimitError:
        print("Rate limit exceeded - wait before retrying")
    except OpenDotaAPIError as e:
        print(f"API error (status {e.status_code}): {e}")
```

## Retry Strategy

For rate limit errors, implement exponential backoff:

```python
import asyncio
from opendota.exceptions import OpenDotaRateLimitError

async def get_match_with_retry(client, match_id, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await client.get_match(match_id)
        except OpenDotaRateLimitError:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 1, 2, 4 seconds
                await asyncio.sleep(wait_time)
            else:
                raise
```
