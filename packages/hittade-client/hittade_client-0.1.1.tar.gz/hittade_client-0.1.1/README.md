# Hittade Client

A Python HTTP client library for the [Hittade API](https://github.com/SUNET/hittade-server/), providing both synchronous and asynchronous interfaces with full type safety.

## Features

- 🔄 Both synchronous and asynchronous clients
- 🔒 Full type safety with Pydantic models
- ✅ Comprehensive test coverage (42 tests, 100% passing)
- 🔐 BasicAuth authentication support
- 📄 Built-in pagination helpers
- 🎯 Clean, minimal API
- 📦 Context manager support for automatic cleanup

## Installation

```bash
pip install hittade-client
```

Or with uv:

```bash
uv pip install hittade-client
```

## Quick Start

### Synchronous Client

```python
from hittade_client import HittadeClient

# Basic usage
with HittadeClient(base_url="https://api.example.com") as client:
    # List all hosts
    hosts = client.list_hosts(limit=100)
    for host in hosts.items:
        print(f"{host.id}: {host.hostname}")
    
    # Paginate through all hosts
    page = client.list_hosts(limit=50)
    while page is not None:
        for host in page.items:
            print(f"{host.id}: {host.hostname}")
        page = client.next_page(page)
    
    # Get host configuration
    config = client.get_host_config("host-123")
    for entry in config:
        print(f"{entry.ctype}: {entry.name} = {entry.value}")
    
    # Get detailed host information
    details = client.get_host_details("host-123")
    print(f"OS: {details.details.osname} {details.details.osrelease}")
    print(f"IP: {details.details.ipv4}")
    print(f"Packages: {len(details.packages)}")
    print(f"Containers: {len(details.containers)}")
```

### Asynchronous Client

```python
from hittade_client import AsyncHittadeClient

async def main():
    async with AsyncHittadeClient(base_url="https://api.example.com") as client:
        # List hosts
        hosts = await client.list_hosts(limit=100)
        
        # Paginate through all hosts
        page = await client.list_hosts(limit=50)
        while page is not None:
            for host in page.items:
                print(f"{host.id}: {host.hostname}")
            page = await client.next_page(page)
        
        # Get host configuration
        config = await client.get_host_config("host-123")
        
        # Get detailed host information
        details = await client.get_host_details("host-123")
```

### Authentication

```python
from hittade_client import HittadeClient, BasicAuth

# With BasicAuth
auth = BasicAuth(username="your-username", password="your-password")

with HittadeClient(base_url="https://api.example.com", auth=auth) as client:
    hosts = client.list_hosts()
```

### Custom Configuration

```python
from hittade_client import HittadeClient, BasicAuth

client = HittadeClient(
    base_url="https://api.example.com",
    timeout=60.0,  # Request timeout in seconds
    headers={"X-Custom-Header": "value"},  # Custom headers
    follow_redirects=True,  # Follow HTTP redirects
    auth=BasicAuth(username="user", password="pass"),  # BasicAuth
)

# Use the client
hosts = client.list_hosts(limit=50, offset=100)

# Don't forget to close when not using context manager
client.close()
```

## API Reference

### Client Methods

#### `list_hosts(limit=500, offset=0)`

List hosts with pagination.

**Parameters:**
- `limit` (int): Maximum number of results (default: 500, minimum: 1)
- `offset` (int): Offset for pagination (default: 0, minimum: 0)

**Returns:** `PagedHostSchema` with `items` (list of hosts), `count` (total count), `limit`, and `offset`

#### `next_page(paged_data)`

Get the next page of hosts based on current page data.

**Parameters:**
- `paged_data` (PagedHostSchema): Current page data from `list_hosts()`

**Returns:** `PagedHostSchema` for the next page, or `None` if no more results

**Example:**
```python
page = client.list_hosts(limit=50)
while page is not None:
    # Process page.items
    page = client.next_page(page)
```

#### `get_host_config(host_id)`

Get host configuration entries.

**Parameters:**
- `host_id` (str): The host identifier

**Returns:** List of `HostConfigurationSchema` objects

#### `get_host_details(host_id)`

Get complete host details including OS information, network configuration, packages, and containers.

**Parameters:**
- `host_id` (str): The host identifier

**Returns:** `CombinedHostSchema` with all host details

### Models

#### `BasicAuth`
- `username` (str): Username for authentication
- `password` (str): Password for authentication

#### `HostSchema`
- `id` (str): Host identifier
- `hostname` (str): Host hostname

#### `PagedHostSchema`
- `items` (list[HostSchema]): List of hosts
- `count` (int): Total count of hosts
- `limit` (int): Limit used in request
- `offset` (int): Offset used in request

#### `HostConfigurationSchema`
- `ctype` (str): Configuration type
- `name` (str): Configuration name
- `value` (str): Configuration value

#### `HostDetailsSchema`
- `time` (datetime): Timestamp
- `domain` (str | None): Domain name
- `osname` (str): Operating system name
- `osrelease` (str): Operating system release
- `rkr` (str): RKR value
- `cosmosrepourl` (str): Cosmos repository URL
- `ipv4` (str | None): IPv4 address
- `ipv6` (str | None): IPv6 address
- `fail2ban` (bool): Fail2ban status

#### `PackageSchema`
- `id` (int): Package identifier
- `name` (str): Package name
- `version` (str): Package version

#### `ServerContainerSchema`
- `image` (str): Container image name
- `imageid` (str): Container image ID

#### `CombinedHostSchema`
- `host` (HostSchema): Basic host information
- `details` (HostDetailsSchema): Detailed host information
- `packages` (list[PackageSchema]): Installed packages
- `containers` (list[ServerContainerSchema]): Running containers
- `configs` (list[HostConfigurationSchema]): Configuration entries

### Exceptions

#### `HittadeError`
Base exception for all Hittade client errors.

#### `HittadeAPIError`
Raised when the API returns an HTTP error (4xx, 5xx status codes).

#### `HittadeValidationError`
Raised when response validation fails (invalid response data from API).

## Development

### Setup

```bash
# Install dependencies
uv sync

# Install in editable mode
uv pip install -e .
```

### Running Tests

```bash
# Run all tests
make test

# Run with pytest directly
uv run pytest tests/ -v
```

### Code Formatting

```bash
# Format and lint code
make reformat
```

### Type Checking

```bash
# Run mypy type checker
make typecheck
```

### Building Package

```bash
# Build distribution packages (wheel and source)
make build

# Clean build artifacts
make clean
```

## Requirements

- Python 3.11 or higher
- httpx >= 0.28.1
- pydantic >= 2.12.1

## License

This project is licensed under the BSD 2-Clause License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Links

- [Documentation](./DEVELOPMENT.md)
- [Source Code](https://github.com/yourusername/python-hittade-client)
- [Issue Tracker](https://github.com/yourusername/python-hittade-client/issues)
