"""Tests for the asynchronous AsyncHittadeClient."""

import httpx
import pytest
import respx

from hittade_client import (
    AsyncHittadeClient,
    BasicAuth,
    HittadeAPIError,
    HittadeValidationError,
)


class TestAsyncHittadeClient:
    """Tests for AsyncHittadeClient."""

    @pytest.mark.asyncio
    async def test_init(self, base_url: str) -> None:
        """Test client initialization."""
        client = AsyncHittadeClient(base_url=base_url)
        assert client.base_url == base_url
        assert client.timeout == 30.0
        assert client.headers is None
        assert client.follow_redirects is True
        await client.close()

    @pytest.mark.asyncio
    async def test_init_with_custom_params(self, base_url: str) -> None:
        """Test client initialization with custom parameters."""
        headers = {"Authorization": "Bearer token"}
        client = AsyncHittadeClient(
            base_url=base_url,
            timeout=60.0,
            headers=headers,
            follow_redirects=False,
        )
        assert client.base_url == base_url
        assert client.timeout == 60.0
        assert client.headers == headers
        assert client.follow_redirects is False
        await client.close()

    @pytest.mark.asyncio
    async def test_init_with_basic_auth(self, base_url: str) -> None:
        """Test client initialization with BasicAuth."""
        client = AsyncHittadeClient(
            base_url=base_url,
            auth=BasicAuth(username="username", password="password"),
        )
        assert client.base_url == base_url
        assert client.auth is not None
        assert isinstance(client.auth, httpx.BasicAuth)
        await client.close()

    @pytest.mark.asyncio
    async def test_context_manager(self, base_url: str) -> None:
        """Test client as async context manager."""
        async with AsyncHittadeClient(base_url=base_url) as client:
            assert client.base_url == base_url

    @pytest.mark.asyncio
    async def test_context_manager_reuse(self, base_url: str) -> None:
        """Test that client can be reused after being closed."""
        client = AsyncHittadeClient(base_url=base_url)

        # First use
        async with client as c1:
            assert c1.base_url == base_url
            assert not c1._client.is_closed

        # Client should be closed after exiting context
        assert client._client.is_closed

        # Second use - should reinitialize
        async with client as c2:
            assert c2.base_url == base_url
            assert not c2._client.is_closed

        # Client should be closed again
        assert client._client.is_closed

    @respx.mock
    @pytest.mark.asyncio
    async def test_context_manager_reuse_with_requests(self, base_url: str, mock_paged_hosts_data: dict) -> None:
        """Test that client can make requests after being reused."""
        respx.get(f"{base_url}/api/hosts").mock(return_value=httpx.Response(200, json=mock_paged_hosts_data))

        client = AsyncHittadeClient(base_url=base_url)

        # First use
        async with client:
            result1 = await client.list_hosts()
            assert result1.count == 1

        # Second use - should work after being closed and reopened
        async with client:
            result2 = await client.list_hosts()
            assert result2.count == 1

    @respx.mock
    @pytest.mark.asyncio
    async def test_list_hosts_success(self, base_url: str, mock_paged_hosts_data: dict) -> None:
        """Test listing hosts successfully."""
        route = respx.get(f"{base_url}/api/hosts").mock(return_value=httpx.Response(200, json=mock_paged_hosts_data))

        async with AsyncHittadeClient(base_url=base_url) as client:
            result = await client.list_hosts()

            assert result.count == 1
            assert len(result.items) == 1
            assert result.items[0].id == "1"
            assert result.items[0].hostname == "test.example.com"

        assert route.called

    @respx.mock
    @pytest.mark.asyncio
    async def test_list_hosts_with_pagination(self, base_url: str, mock_paged_hosts_data: dict) -> None:
        """Test listing hosts with pagination parameters."""
        route = respx.get(f"{base_url}/api/hosts").mock(return_value=httpx.Response(200, json=mock_paged_hosts_data))

        async with AsyncHittadeClient(base_url=base_url) as client:
            result = await client.list_hosts(limit=100, offset=50)

            assert result.count == 1

        assert route.called
        # Verify query parameters
        request = route.calls.last.request
        assert "limit=100" in str(request.url)
        assert "offset=50" in str(request.url)

    @respx.mock
    @pytest.mark.asyncio
    async def test_list_hosts_http_error(self, base_url: str) -> None:
        """Test listing hosts with HTTP error."""
        respx.get(f"{base_url}/api/hosts").mock(return_value=httpx.Response(500, text="Internal Server Error"))

        async with AsyncHittadeClient(base_url=base_url) as client:
            with pytest.raises(HittadeAPIError) as exc_info:
                await client.list_hosts()

            assert "500" in str(exc_info.value)

    @respx.mock
    @pytest.mark.asyncio
    async def test_list_hosts_validation_error(self, base_url: str) -> None:
        """Test listing hosts with validation error."""
        invalid_data = {"invalid": "data"}
        respx.get(f"{base_url}/api/hosts").mock(return_value=httpx.Response(200, json=invalid_data))

        async with AsyncHittadeClient(base_url=base_url) as client:
            with pytest.raises(HittadeValidationError):
                await client.list_hosts()

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_host_config_success(self, base_url: str, mock_host_config_data: list[dict]) -> None:
        """Test getting host configuration successfully."""
        host_id = "test-host"
        route = respx.get(f"{base_url}/api/host/{host_id}/config").mock(
            return_value=httpx.Response(200, json=mock_host_config_data)
        )

        async with AsyncHittadeClient(base_url=base_url) as client:
            result = await client.get_host_config(host_id)

            assert len(result) == 2
            assert result[0].ctype == "network"
            assert result[0].name == "interface"
            assert result[0].value == "eth0"
            assert result[1].ctype == "system"

        assert route.called

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_host_config_http_error(self, base_url: str) -> None:
        """Test getting host configuration with HTTP error."""
        host_id = "test-host"
        respx.get(f"{base_url}/api/host/{host_id}/config").mock(return_value=httpx.Response(404, text="Not Found"))

        async with AsyncHittadeClient(base_url=base_url) as client:
            with pytest.raises(HittadeAPIError) as exc_info:
                await client.get_host_config(host_id)

            assert "404" in str(exc_info.value)

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_host_config_validation_error(self, base_url: str) -> None:
        """Test getting host configuration with validation error."""
        host_id = "test-host"
        invalid_data = [{"invalid": "data"}]
        respx.get(f"{base_url}/api/host/{host_id}/config").mock(return_value=httpx.Response(200, json=invalid_data))

        async with AsyncHittadeClient(base_url=base_url) as client:
            with pytest.raises(HittadeValidationError):
                await client.get_host_config(host_id)

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_host_details_success(self, base_url: str, mock_combined_host_data: dict) -> None:
        """Test getting host details successfully."""
        host_id = "test-host"
        route = respx.get(f"{base_url}/api/host/{host_id}").mock(
            return_value=httpx.Response(200, json=mock_combined_host_data)
        )

        async with AsyncHittadeClient(base_url=base_url) as client:
            result = await client.get_host_details(host_id)

            # Verify host info
            assert result.host.id == "1"
            assert result.host.hostname == "test.example.com"

            # Verify details
            assert result.details.osname == "Ubuntu"
            assert result.details.osrelease == "22.04"
            assert result.details.domain == "example.com"
            assert result.details.ipv4 == "192.168.1.100"
            assert result.details.ipv6 == "2001:db8::1"
            assert result.details.fail2ban is True

            # Verify packages
            assert len(result.packages) == 2
            assert result.packages[0].name == "nginx"
            assert result.packages[0].version == "1.18.0"

            # Verify containers
            assert len(result.containers) == 2
            assert result.containers[0].image == "nginx:latest"
            assert result.containers[0].imageid == "abc123"

            # Verify configs
            assert len(result.configs) == 2
            assert result.configs[0].ctype == "network"

        assert route.called

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_host_details_http_error(self, base_url: str) -> None:
        """Test getting host details with HTTP error."""
        host_id = "test-host"
        respx.get(f"{base_url}/api/host/{host_id}").mock(return_value=httpx.Response(403, text="Forbidden"))

        async with AsyncHittadeClient(base_url=base_url) as client:
            with pytest.raises(HittadeAPIError) as exc_info:
                await client.get_host_details(host_id)

            assert "403" in str(exc_info.value)

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_host_details_validation_error(self, base_url: str) -> None:
        """Test getting host details with validation error."""
        host_id = "test-host"
        invalid_data = {"invalid": "data"}
        respx.get(f"{base_url}/api/host/{host_id}").mock(return_value=httpx.Response(200, json=invalid_data))

        async with AsyncHittadeClient(base_url=base_url) as client:
            with pytest.raises(HittadeValidationError):
                await client.get_host_details(host_id)

    @respx.mock
    @pytest.mark.asyncio
    async def test_multiple_requests(
        self,
        base_url: str,
        mock_paged_hosts_data: dict,
        mock_host_config_data: list[dict],
    ) -> None:
        """Test making multiple requests with the same client."""
        respx.get(f"{base_url}/api/hosts").mock(return_value=httpx.Response(200, json=mock_paged_hosts_data))
        respx.get(f"{base_url}/api/host/test-host/config").mock(
            return_value=httpx.Response(200, json=mock_host_config_data)
        )

        async with AsyncHittadeClient(base_url=base_url) as client:
            # First request
            hosts = await client.list_hosts()
            assert hosts.count == 1

            # Second request
            config = await client.get_host_config("test-host")
            assert len(config) == 2

    @respx.mock
    @pytest.mark.asyncio
    async def test_basic_auth_header_sent(self, base_url: str, mock_paged_hosts_data: dict) -> None:
        """Test that BasicAuth is properly sent in requests."""
        route = respx.get(f"{base_url}/api/hosts").mock(return_value=httpx.Response(200, json=mock_paged_hosts_data))

        async with AsyncHittadeClient(
            base_url=base_url, auth=BasicAuth(username="testuser", password="testpass")
        ) as client:
            await client.list_hosts()

        assert route.called
        # Verify Authorization header was sent
        assert "authorization" in route.calls.last.request.headers
        # BasicAuth encodes as "Basic base64(username:password)"
        assert route.calls.last.request.headers["authorization"].startswith("Basic ")

    @pytest.mark.asyncio
    async def test_verify_ssl_default_true(self, base_url: str) -> None:
        """Test that SSL verification is enabled by default."""
        client = AsyncHittadeClient(base_url=base_url)
        assert client.verify is True
        assert client._client._transport._pool._ssl_context is not None
        await client.close()

    @pytest.mark.asyncio
    async def test_verify_ssl_can_be_disabled(self, base_url: str) -> None:
        """Test that SSL verification can be disabled."""
        client = AsyncHittadeClient(base_url=base_url, verify=False)
        assert client.verify is False
        ssl_ctx = client._client._transport._pool._ssl_context
        if ssl_ctx is not None:
            assert ssl_ctx.check_hostname is False
        await client.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_next_page_with_more_results(self, base_url: str, mock_host_data: dict) -> None:
        """Test next_page when there are more results."""
        # First page: offset=0, limit=2, count=5 (more results available)
        first_page_data = {"items": [mock_host_data], "count": 5}
        # Second page: offset=2, limit=2, count=5
        second_page_data = {"items": [mock_host_data], "count": 5}

        respx.get(f"{base_url}/api/hosts").mock(
            side_effect=[
                httpx.Response(200, json=first_page_data),
                httpx.Response(200, json=second_page_data),
            ]
        )

        async with AsyncHittadeClient(base_url=base_url) as client:
            # Get first page
            first_page = await client.list_hosts(limit=2, offset=0)
            assert first_page.count == 5
            assert first_page.limit == 2
            assert first_page.offset == 0

            # Get next page
            second_page = await client.next_page(first_page)
            assert second_page is not None
            assert second_page.count == 5
            assert second_page.limit == 2
            assert second_page.offset == 2

    @respx.mock
    @pytest.mark.asyncio
    async def test_next_page_no_more_results(self, base_url: str, mock_host_data: dict) -> None:
        """Test next_page when there are no more results."""
        # Last page: offset=4, limit=2, count=5 (offset + limit >= count)
        last_page_data = {"items": [mock_host_data], "count": 5}

        respx.get(f"{base_url}/api/hosts").mock(return_value=httpx.Response(200, json=last_page_data))

        async with AsyncHittadeClient(base_url=base_url) as client:
            # Get last page
            last_page = await client.list_hosts(limit=2, offset=4)
            assert last_page.count == 5
            assert last_page.limit == 2
            assert last_page.offset == 4

            # Try to get next page (should return None)
            next_page = await client.next_page(last_page)
            assert next_page is None

    @respx.mock
    @pytest.mark.asyncio
    async def test_next_page_exactly_at_end(self, base_url: str, mock_host_data: dict) -> None:
        """Test next_page when offset + limit equals count."""
        # Last page: offset=3, limit=2, count=5 (offset + limit == count)
        last_page_data = {"items": [mock_host_data, mock_host_data], "count": 5}

        respx.get(f"{base_url}/api/hosts").mock(return_value=httpx.Response(200, json=last_page_data))

        async with AsyncHittadeClient(base_url=base_url) as client:
            # Get last page
            last_page = await client.list_hosts(limit=2, offset=3)
            assert last_page.count == 5
            assert last_page.limit == 2
            assert last_page.offset == 3

            # Try to get next page (should return None)
            next_page = await client.next_page(last_page)
            assert next_page is None
