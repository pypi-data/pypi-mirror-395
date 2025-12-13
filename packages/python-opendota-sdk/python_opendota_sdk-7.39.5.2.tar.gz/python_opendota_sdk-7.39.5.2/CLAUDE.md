# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Guidelines

This document contains critical information about working with this codebase. Follow these guidelines precisely.

## Core Development Rules

1. **Package Management**
   - ONLY use `uv`, NEVER `pip` or `python` directly
   - Installation: `uv add package` or `uv sync --dev`
   - Running Python: `uv run python script.py`
   - Running tools: `uv run pytest`, `uv run mypy`
   - FORBIDDEN: `pip install`, `python script.py`

2. **Code Quality**
   - Type hints required for all public functions
   - Pydantic models for all API responses
   - Async/await for all API calls
   - Line length: 120 characters maximum
   - Follow existing patterns in `src/python_opendota/client.py`

3. **Testing Requirements**
   - Framework: `uv run pytest`
   - Async testing: `pytest-asyncio` with `asyncio_mode = "auto"`
   - HTTP mocking: `pytest-httpx` for API tests
   - Coverage: `uv run pytest --cov=python_opendota`
   - Test structure mirrors source in `tests/`

## Architecture Patterns

### Client Design (`src/python_opendota/client.py`)
```python
# Dual usage pattern support
async with OpenDota() as client:  # Context manager (preferred)
    data = await client.get_match(match_id)

# OR manual management
client = OpenDota()
data = await client.get_match(match_id)
await client.close()
```

### Response Format Flexibility
```python
# Pydantic models (default)
client = OpenDota(format='pydantic')
match = await client.get_match(id)  # Returns Match model

# Raw JSON dicts
client = OpenDota(format='json')  
match = await client.get_match(id)  # Returns dict
```

### Type Aliases Pattern
```python
# Use TypeAlias for dual response types
MatchResponse: TypeAlias = Union[Match, dict]
PublicMatchesResponse: TypeAlias = Union[List[PublicMatch], List[dict]]
```

## API Integration

- Base URL: `https://api.opendota.com/api`
- Authentication: Bearer token or query parameter
- Rate limits: 60/min free, unlimited with API key
- Error handling: Custom exceptions for 404, 429, and general errors

### Key Endpoints
```python
# Matches
/matches/{match_id}          # Detailed match data
/publicMatches              # Recent public matches
/proMatches                 # Professional matches

# Players  
/players/{account_id}        # Player profile
/players/{account_id}/matches # Player match history

# Heroes
/heroes                     # Hero metadata
/heroStats                  # Hero statistics
```

## Code Formatting

1. **Ruff** (if configured)
   - Format: `uv run ruff format .`
   - Check: `uv run ruff check .`
   - Fix: `uv run ruff check . --fix`

2. **Type Checking**
   - Tool: `uv run mypy src/ --ignore-missing-imports`
   - Ensure all public APIs have type hints
   - Use Optional[] for nullable parameters
   - All type errors have been resolved

## Testing Commands

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_matches.py

# Run specific test
uv run pytest tests/test_matches.py::TestMatches::test_get_match

# Run with coverage
uv run pytest --cov=python_opendota

# Run with coverage and missing lines report
uv run pytest --cov=python_opendota --cov-report=term-missing

# Run with verbose output
uv run pytest -v
```

## Common Development Tasks

### Adding New Endpoint
1. Add method to `OpenDota` class in `client.py`
2. Create Pydantic model in `models/` if needed
3. Follow existing pattern with TypeAlias for response
4. Add `_format_response()` call for dual format support
5. Write tests in corresponding `test_*.py` file

### Updating Models
1. Models use Pydantic v2 with `BaseModel`
2. All fields should be Optional unless guaranteed by API
3. Use appropriate field types (int, str, List, etc.)
4. Add field validators if needed for normalization

### Error Handling
```python
# Use custom exceptions
from python_opendota.exceptions import (
    OpenDotaAPIError,
    OpenDotaRateLimitError, 
    OpenDotaNotFoundError
)

# Handle in _request method
if response.status_code == 404:
    raise OpenDotaNotFoundError("Resource not found", response.status_code)
elif response.status_code == 429:
    raise OpenDotaRateLimitError("Rate limit exceeded", response.status_code)
```

## Package Building

```bash
# Build distribution
uv run python -m build

# Upload to PyPI
uv run twine upload dist/*

# Install locally for testing
uv pip install -e .
```

## Important Notes

- Package name: `python-opendota` on PyPI
- Python versions: 3.9+ supported
- Dependencies: httpx, pydantic v2
- All methods are async, no sync wrapper provided
- Environment variable: `OPENDOTA_API_KEY` for authentication
- Context manager pattern preferred for automatic cleanup