"""Pytest configuration and fixtures."""

import pytest


@pytest.fixture
def base_url() -> str:
    """Return the base URL for testing."""
    return "https://api.example.com"


@pytest.fixture
def mock_host_data() -> dict:
    """Return mock host data."""
    return {"id": 1, "hostname": "test.example.com"}


@pytest.fixture
def mock_paged_hosts_data(mock_host_data: dict) -> dict:
    """Return mock paged hosts data."""
    return {"items": [mock_host_data], "count": 1}


@pytest.fixture
def mock_host_config_data() -> list[dict]:
    """Return mock host configuration data."""
    return [
        {"ctype": "network", "name": "interface", "value": "eth0"},
        {"ctype": "system", "name": "hostname", "value": "test.example.com"},
    ]


@pytest.fixture
def mock_host_details_data() -> dict:
    """Return mock host details data."""
    return {
        "time": "2024-01-01T12:00:00Z",
        "domain": "example.com",
        "osname": "Ubuntu",
        "osrelease": "22.04",
        "rkr": "5.15.0-generic",
        "cosmosrepourl": "https://cosmos.example.com",
        "ipv4": "192.168.1.100",
        "ipv6": "2001:db8::1",
        "fail2ban": True,
    }


@pytest.fixture
def mock_package_data() -> list[dict]:
    """Return mock package data."""
    return [
        {"id": 1, "name": "nginx", "version": "1.18.0"},
        {"id": 2, "name": "python3", "version": "3.10.12"},
    ]


@pytest.fixture
def mock_container_data() -> list[dict]:
    """Return mock container data."""
    return [
        {"image": "nginx:latest", "imageid": "abc123"},
        {"image": "postgres:15", "imageid": "def456"},
    ]


@pytest.fixture
def mock_combined_host_data(
    mock_host_data: dict,
    mock_host_details_data: dict,
    mock_package_data: list[dict],
    mock_container_data: list[dict],
    mock_host_config_data: list[dict],
) -> dict:
    """Return mock combined host data."""
    return {
        "host": mock_host_data,
        "details": mock_host_details_data,
        "packages": mock_package_data,
        "containers": mock_container_data,
        "configs": mock_host_config_data,
    }
