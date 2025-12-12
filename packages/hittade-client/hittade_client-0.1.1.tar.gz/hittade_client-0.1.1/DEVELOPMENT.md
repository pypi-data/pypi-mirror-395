# Development Context for python-hittade-client

> **For LLMs:** Read this entire document to understand the project state. All code is complete, tested, and follows project conventions. When making changes: (1) run `make reformat` after modifications, (2) run `make test` to verify tests pass, (3) run `make typecheck` to verify type safety, (4) maintain the existing architecture patterns (ABC base class, static validation methods, etc.).

## Project Overview
This is a Python HTTP client library for the Hittade API, built with httpx and pydantic. The library provides both synchronous and asynchronous clients with full type safety and comprehensive test coverage.

**Current Status:** ✅ Production-ready with comprehensive tests (42 tests, all passing)

## What Has Been Built

### 1. Core Implementation (src/hittade_client/)
- **models.py** - Pydantic models for all API schemas:
  - `BasicAuth` - BasicAuth credentials (username, password)
  - `HostSchema` - Basic host information
  - `PagedHostSchema` - Paginated list of hosts
  - `HostConfigurationSchema` - Host configuration entries
  - `HostDetailsSchema` - Detailed host information (OS, network, etc.)
  - `PackageSchema` - Installed package information
  - `ServerContainerSchema` - Docker container information
  - `CombinedHostSchema` - Complete host data with all nested models

- **client.py** - HTTP client implementation with ABC base class:
  - `BaseHittadeClient` - Abstract base class containing:
    - Common initialization logic (base_url, timeout, headers, follow_redirects, auth)
    - BasicAuth support using httpx.BasicAuth
    - Static response handling method (`_handle_response`)
    - Static validation methods for all response types
    - Static pagination helper method (`_next_offset`)
  - `HittadeClient` - Synchronous client using `httpx.Client`
    - Context manager support (`__enter__`/`__exit__`)
    - Four API methods: `list_hosts()`, `next_page()`, `get_host_config()`, `get_host_details()`
  - `AsyncHittadeClient` - Asynchronous client using `httpx.AsyncClient`
    - Async context manager support (`__aenter__`/`__aexit__`)
    - Same four API methods with async/await

- **exceptions.py** - Custom exception hierarchy:
  - `HittadeError` - Base exception
  - `HittadeAPIError` - HTTP/API errors
  - `HittadeValidationError` - Pydantic validation errors

- **__init__.py** - Clean public API exports with `__all__`
- **py.typed** - Type checking marker for mypy/pyright

### 2. API Endpoints Implemented
Based on openapi.json specification:
1. **GET /api/hosts** - List hosts with pagination (limit, offset)
   - Includes `next_page()` helper for easy pagination
2. **GET /api/host/{host_id}/config** - Get host configuration entries
3. **GET /api/host/{host_id}** - Get complete host details

### 3. Test Suite (tests/)
- **conftest.py** - Pytest fixtures with mock data for all API responses
- **test_client.py** - 19 tests for `HittadeClient` (synchronous)
- **test_async_client.py** - 19 tests for `AsyncHittadeClient` (asynchronous)

Test coverage includes:
- Client initialization and configuration
- BasicAuth initialization and header verification
- Context manager functionality
- All four API endpoints (list_hosts, next_page, get_host_config, get_host_details)
- Success cases with data validation
- HTTP error handling (404, 403, 500)
- Pydantic validation errors
- Query parameter handling
- Pagination with next_page method
- Multiple sequential requests

All 38 tests pass using respx for HTTP mocking.

## Dependencies
**Core:**
- httpx >= 0.28.1 - HTTP client
- pydantic >= 2.12.1 - Data validation

**Dev:**
- pytest >= 8.3.4 - Test framework
- pytest-asyncio >= 0.25.2 - Async test support
- respx >= 0.22.0 - HTTP mocking for tests

## Code Quality
- All code passes `ruff check` and `ruff format`
- Follows type hints throughout (Python 3.11+)
- No code duplication (shared logic in BaseHittadeClient ABC)
- Clean separation of sync/async implementations

## Project Structure
```
hittade-client/
├── src/hittade_client/
│   ├── __init__.py        # Public API exports
│   ├── client.py          # BaseHittadeClient, HittadeClient, AsyncHittadeClient
│   ├── models.py          # Pydantic schemas
│   ├── exceptions.py      # Custom exceptions
│   └── py.typed           # Type marker
├── tests/
│   ├── __init__.py
│   ├── conftest.py        # Pytest fixtures
│   ├── test_client.py     # Sync client tests (19 tests)
│   └── test_async_client.py  # Async client tests (19 tests)
├── openapi.json           # API specification (source of truth)
├── pyproject.toml         # Project config with BSD-2-Clause license
├── LICENSE                # BSD 2-Clause License
├── README.md              # User documentation
├── DEVELOPMENT.md         # This file - development documentation
├── Makefile               # Dev commands (test, reformat, typecheck, build, clean)
└── uv.lock                # Dependency lock file
```

## Common Commands
```bash
# Install in editable mode
uv pip install -e .

# Run tests
make test

# Format and lint
make reformat

# Type checking
make typecheck

# Build package
make build

# Clean build artifacts
make clean

# Sync dependencies
uv sync
```

## Design Decisions
1. **ABC Base Class** - Extracted all common logic (response handling, validation, auth) into `BaseHittadeClient` to eliminate duplication between sync and async clients
2. **Static Methods** - Validation and response handling are static since they don't need instance state
3. **Context Managers** - Both clients support context managers for automatic cleanup
4. **Separate Validation Methods** - Each response type has its own validation method for clarity and error handling
5. **Type Safety** - Full type hints with proper return types and pydantic validation
6. **BasicAuth Model** - Authentication credentials are represented as a Pydantic model for type safety and validation

## Architecture Patterns to Follow
When extending this codebase:
- **Add new endpoints:** Implement in both `HittadeClient` and `AsyncHittadeClient`, add validation method to `BaseHittadeClient` if needed
- **Add new models:** Create Pydantic models in `models.py`, export in `__init__.py`
- **Add new exceptions:** Inherit from `HittadeError` in `exceptions.py`
- **Write tests:** Mirror structure in `test_client.py` and `test_async_client.py` with respx mocking
- **Error handling:** Use `_handle_response()` for HTTP errors, wrap pydantic validation in try/except for `HittadeValidationError`

## Example Usage
```python
# Synchronous
from hittade_client import HittadeClient, BasicAuth

with HittadeClient(base_url="https://api.example.com") as client:
    hosts = client.list_hosts(limit=100)
    for host in hosts.items:
        print(f"{host.id}: {host.hostname}")
    
    # Pagination with next_page
    while True:
        hosts = client.list_hosts(limit=50)
        for host in hosts.items:
            print(f"{host.id}: {host.hostname}")
        
        hosts = client.next_page(hosts)
        if hosts is None:
            break  # No more results
    
    config = client.get_host_config("host-123")
    details = client.get_host_details("host-123")

# With BasicAuth
auth = BasicAuth(username="user", password="pass")
with HittadeClient(base_url="https://api.example.com", auth=auth) as client:
    hosts = client.list_hosts(limit=100)

# Asynchronous
from hittade_client import AsyncHittadeClient

async with AsyncHittadeClient(base_url="https://api.example.com") as client:
    hosts = await client.list_hosts(limit=100)
    
    # Pagination with next_page
    while hosts is not None:
        for host in hosts.items:
            print(f"{host.id}: {host.hostname}")
        hosts = await client.next_page(hosts)
    
    config = await client.get_host_config("host-123")
    details = await client.get_host_details("host-123")
```

## Next Steps / TODO
Potential improvements:
- ✅ ~~Add BasicAuth authentication support~~ (Completed)
- ✅ ~~Add pagination helpers for iterating through all hosts~~ (Completed - `next_page()` method)
- Add retry logic with exponential backoff
- Add rate limiting support
- Add request/response logging/debugging hooks
- Add iterator/generator for automatic pagination
- Add authentication support (API keys, OAuth, etc.)
- Add more comprehensive error messages
- Add response caching options
- Add request timeout customization per method
- Consider adding batch operations
- Add CLI interface for testing

## API Notes
- The API uses NinjaAPI framework
- All endpoints return JSON
- Host IDs are strings (not integers)
- Pagination uses limit/offset pattern (not cursor-based)
- BasicAuth authentication is supported via the `auth` parameter
- Date/time fields use ISO 8601 format

## Development Workflow
1. **Before making changes:** Run `make test` and `make typecheck` to ensure baseline is passing
2. **Make changes:** Follow existing patterns and conventions
3. **Format code:** Run `make reformat` (runs ruff check + format + extended checks)
4. **Run tests:** Run `make test` to verify changes
5. **Type check:** Run `make typecheck` to verify type safety
6. **Build package:** Run `make build` to create distribution packages (tests are excluded)
7. **Install package:** Run `uv pip install -e .` if you added new files/modules

**After any code changes, always run:** `make reformat && make test && make typecheck`

## Build Configuration
The package uses hatchling as the build backend:
- **pyproject.toml** - Configures hatchling to only package `src/hittade_client`
- Build output includes only source code, LICENSE, and README
- Use `make build` to create wheel and source distribution
- Use `make clean` to remove build artifacts

## Key Files to Review
- `src/hittade_client/client.py` - Main client implementation (read this first)
- `src/hittade_client/models.py` - All Pydantic schemas
- `openapi.json` - Source of truth for API specification
- `tests/conftest.py` - Mock data fixtures
- `tests/test_client.py` - Example test patterns
