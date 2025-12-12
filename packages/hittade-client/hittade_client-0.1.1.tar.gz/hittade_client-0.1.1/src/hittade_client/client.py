"""HTTP client for the Hittade API."""

from abc import ABC
from ssl import SSLContext
from typing import Any

import httpx
from pydantic import ValidationError

from .exceptions import HittadeAPIError, HittadeValidationError
from .models import BasicAuth, CombinedHostSchema, HostConfigurationSchema, PagedHostSchema


class BaseHittadeClient(ABC):
    """Base class for Hittade API clients."""

    def __init__(
        self,
        base_url: str,
        timeout: float = 30.0,
        headers: dict[str, str] | None = None,
        follow_redirects: bool = True,
        auth: BasicAuth | None = None,
        verify: SSLContext | str | bool = True,
    ) -> None:
        """Initialize the base Hittade client.

        Args:
            base_url: Base URL for the API
            timeout: Request timeout in seconds
            headers: Optional custom headers
            follow_redirects: Whether to follow redirects
            auth: Optional BasicAuth credentials
            verify: SSL verification. Can be:
                - True: verify SSL certificates (default)
                - False: disable SSL verification
                - str: path to CA bundle file
                - SSLContext: custom SSL context
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.headers = headers
        self.follow_redirects = follow_redirects
        self.auth = httpx.BasicAuth(auth.username, auth.password) if auth else None
        self.verify = verify

    @staticmethod
    def _handle_response(response: httpx.Response) -> dict[str, Any] | list[Any]:
        """Handle HTTP response and raise errors if needed.

        Args:
            response: HTTP response

        Returns:
            JSON response data

        Raises:
            HittadeAPIError: If the API returns an error
        """
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HittadeAPIError(f"API request failed with status {e.response.status_code}: {e.response.text}") from e

        return response.json()

    @staticmethod
    def _validate_paged_hosts(data: dict[str, Any], limit: int, offset: int) -> PagedHostSchema:
        """Validate and return paged hosts response.

        Args:
            data: Response data
            limit: Limit used in the request
            offset: Offset used in the request

        Returns:
            Validated paged host schema

        Raises:
            HittadeValidationError: If validation fails
        """
        try:
            data["limit"] = limit
            data["offset"] = offset
            return PagedHostSchema.model_validate(data)
        except ValidationError as e:
            raise HittadeValidationError(f"Failed to validate response: {e}") from e

    @staticmethod
    def _next_offset(paged_data: PagedHostSchema) -> int | None:
        """Calculate the next offset for pagination.

        Args:
            paged_data: Paged host schema
        Returns:
            Next offset or None if there are no more results
        """
        next_offset = paged_data.offset + paged_data.limit
        if next_offset >= paged_data.count:
            return None
        return next_offset

    @staticmethod
    def _validate_host_configs(data: list[Any]) -> list[HostConfigurationSchema]:
        """Validate and return host configurations.

        Args:
            data: Response data

        Returns:
            List of validated host configuration schemas

        Raises:
            HittadeValidationError: If validation fails
        """
        try:
            return [HostConfigurationSchema.model_validate(item) for item in data]
        except ValidationError as e:
            raise HittadeValidationError(f"Failed to validate response: {e}") from e

    @staticmethod
    def _validate_combined_host(data: dict[str, Any]) -> CombinedHostSchema:
        """Validate and return combined host details.

        Args:
            data: Response data

        Returns:
            Validated combined host schema

        Raises:
            HittadeValidationError: If validation fails
        """
        try:
            return CombinedHostSchema.model_validate(data)
        except ValidationError as e:
            raise HittadeValidationError(f"Failed to validate response: {e}") from e


class HittadeClient(BaseHittadeClient):
    """HTTP client for the Hittade API."""

    def __init__(
        self,
        base_url: str,
        timeout: float = 30.0,
        headers: dict[str, str] | None = None,
        follow_redirects: bool = True,
        auth: BasicAuth | None = None,
        verify: SSLContext | str | bool = True,
    ) -> None:
        """Initialize the Hittade client.

        Args:
            base_url: Base URL for the API
            timeout: Request timeout in seconds
            headers: Optional custom headers
            follow_redirects: Whether to follow redirects
            auth: Optional BasicAuth credentials
            verify: SSL verification. Can be:
                - True: verify SSL certificates (default)
                - False: disable SSL verification
                - str: path to CA bundle file
                - SSLContext: custom SSL context
        """
        super().__init__(base_url, timeout, headers, follow_redirects, auth, verify)
        self._client = self._init_client()

    def _init_client(self) -> httpx.Client:
        return httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
            headers=self.headers,
            follow_redirects=self.follow_redirects,
            auth=self.auth,
            verify=self.verify,
        )

    def __enter__(self) -> "HittadeClient":
        """Context manager entry."""
        if self._client.is_closed:
            self._client = self._init_client()
        return self

    def __exit__(self, *args: Any) -> None:
        """Context manager exit."""
        self.close()

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def list_hosts(
        self,
        limit: int = 500,
        offset: int = 0,
    ) -> PagedHostSchema:
        """List hosts.

        Args:
            limit: Maximum number of results (default: 500, minimum: 1)
            offset: Offset for pagination (default: 0, minimum: 0)

        Returns:
            Paged host schema with items and count

        Raises:
            HittadeAPIError: If the API request fails
            HittadeValidationError: If response validation fails
        """
        params = {"limit": limit, "offset": offset}
        response = self._client.get("/api/hosts", params=params)
        data = self._handle_response(response)
        assert isinstance(data, dict)
        return self._validate_paged_hosts(data, limit, offset)

    def next_page(self, paged_data: PagedHostSchema) -> PagedHostSchema | None:
        """Get the next page of hosts.

        Args:
            paged_data: Current paged host schema

        Returns:
            Next paged host schema or None if there are no more results

        Raises:
            HittadeAPIError: If the API request fails
            HittadeValidationError: If response validation fails
        """
        next_offset = self._next_offset(paged_data)
        if next_offset is None:
            return None
        return self.list_hosts(limit=paged_data.limit, offset=next_offset)

    def get_host_config(self, host_id: str) -> list[HostConfigurationSchema]:
        """Get host configuration.

        Returns only the host configuration entries.

        Args:
            host_id: Host ID

        Returns:
            List of host configuration schemas

        Raises:
            HittadeAPIError: If the API request fails
            HittadeValidationError: If response validation fails
        """
        response = self._client.get(f"/api/host/{host_id}/config")
        data = self._handle_response(response)
        assert isinstance(data, list)
        return self._validate_host_configs(data)

    def get_host_details(self, host_id: str) -> CombinedHostSchema:
        """Get host details.

        Args:
            host_id: Host ID

        Returns:
            Combined host schema with all details

        Raises:
            HittadeAPIError: If the API request fails
            HittadeValidationError: If response validation fails
        """
        response = self._client.get(f"/api/host/{host_id}")
        data = self._handle_response(response)
        assert isinstance(data, dict)
        return self._validate_combined_host(data)


class AsyncHittadeClient(BaseHittadeClient):
    """Async HTTP client for the Hittade API."""

    def __init__(
        self,
        base_url: str,
        timeout: float = 30.0,
        headers: dict[str, str] | None = None,
        follow_redirects: bool = True,
        auth: BasicAuth | None = None,
        verify: SSLContext | str | bool = True,
    ) -> None:
        """Initialize the async Hittade client.

        Args:
            base_url: Base URL for the API
            timeout: Request timeout in seconds
            headers: Optional custom headers
            follow_redirects: Whether to follow redirects
            auth: Optional BasicAuth credentials
            verify: SSL verification. Can be:
                - True: verify SSL certificates (default)
                - False: disable SSL verification
                - str: path to CA bundle file
                - SSLContext: custom SSL context
        """
        super().__init__(base_url, timeout, headers, follow_redirects, auth, verify)
        self._client = self._init_client()

    def _init_client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            headers=self.headers,
            follow_redirects=self.follow_redirects,
            auth=self.auth,
            verify=self.verify,
        )

    async def __aenter__(self) -> "AsyncHittadeClient":
        """Async context manager entry."""
        if self._client.is_closed:
            self._client = self._init_client()
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Async context manager exit."""
        await self.close()

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()

    async def list_hosts(
        self,
        limit: int = 500,
        offset: int = 0,
    ) -> PagedHostSchema:
        """List hosts.

        Args:
            limit: Maximum number of results (default: 500, minimum: 1)
            offset: Offset for pagination (default: 0, minimum: 0)

        Returns:
            Paged host schema with items and count

        Raises:
            HittadeAPIError: If the API request fails
            HittadeValidationError: If response validation fails
        """
        params = {"limit": limit, "offset": offset}
        response = await self._client.get("/api/hosts", params=params)
        data = self._handle_response(response)
        assert isinstance(data, dict)
        return self._validate_paged_hosts(data, limit, offset)

    async def next_page(self, paged_data: PagedHostSchema) -> PagedHostSchema | None:
        """Get the next page of hosts.

        Args:
            paged_data: Current paged host schema

        Returns:
            Next paged host schema or None if there are no more results

        Raises:
            HittadeAPIError: If the API request fails
            HittadeValidationError: If response validation fails
        """
        next_offset = self._next_offset(paged_data)
        if next_offset is None:
            return None
        return await self.list_hosts(limit=paged_data.limit, offset=next_offset)

    async def get_host_config(self, host_id: str) -> list[HostConfigurationSchema]:
        """Get host configuration.

        Returns only the host configuration entries.

        Args:
            host_id: Host ID

        Returns:
            List of host configuration schemas

        Raises:
            HittadeAPIError: If the API request fails
            HittadeValidationError: If response validation fails
        """
        response = await self._client.get(f"/api/host/{host_id}/config")
        data = self._handle_response(response)
        assert isinstance(data, list)
        return self._validate_host_configs(data)

    async def get_host_details(self, host_id: str) -> CombinedHostSchema:
        """Get host details.

        Args:
            host_id: Host ID

        Returns:
            Combined host schema with all details

        Raises:
            HittadeAPIError: If the API request fails
            HittadeValidationError: If response validation fails
        """
        response = await self._client.get(f"/api/host/{host_id}")
        data = self._handle_response(response)
        assert isinstance(data, dict)
        return self._validate_combined_host(data)
