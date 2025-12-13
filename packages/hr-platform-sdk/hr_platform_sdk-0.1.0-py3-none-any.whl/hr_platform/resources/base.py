"""Base resource class.

Provides common functionality for all API resources.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from hr_platform.core.http import HttpClient
    from hr_platform.core.async_http import AsyncHttpClient


class BaseResource:
    """Base class for synchronous API resources."""

    def __init__(self, client: "HttpClient") -> None:
        """Initialize resource with HTTP client.

        Args:
            client: HTTP client instance for making requests.
        """
        self._client = client

    def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        """Make GET request.

        Args:
            path: API endpoint path.
            params: Optional query parameters.

        Returns:
            Response data.
        """
        return self._client.get(path, params=params)

    def _post(
        self,
        path: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Make POST request.

        Args:
            path: API endpoint path.
            data: Request body data.
            params: Optional query parameters.

        Returns:
            Response data.
        """
        return self._client.post(path, data=data, params=params)

    def _put(
        self,
        path: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Make PUT request.

        Args:
            path: API endpoint path.
            data: Request body data.
            params: Optional query parameters.

        Returns:
            Response data.
        """
        return self._client.put(path, data=data, params=params)

    def _delete(self, path: str, params: dict[str, Any] | None = None) -> Any:
        """Make DELETE request.

        Args:
            path: API endpoint path.
            params: Optional query parameters.

        Returns:
            Response data.
        """
        return self._client.delete(path, params=params)


class AsyncBaseResource:
    """Base class for asynchronous API resources."""

    def __init__(self, client: "AsyncHttpClient") -> None:
        """Initialize resource with async HTTP client.

        Args:
            client: Async HTTP client instance for making requests.
        """
        self._client = client

    async def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        """Make async GET request.

        Args:
            path: API endpoint path.
            params: Optional query parameters.

        Returns:
            Response data.
        """
        return await self._client.get(path, params=params)

    async def _post(
        self,
        path: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Make async POST request.

        Args:
            path: API endpoint path.
            data: Request body data.
            params: Optional query parameters.

        Returns:
            Response data.
        """
        return await self._client.post(path, data=data, params=params)

    async def _put(
        self,
        path: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Make async PUT request.

        Args:
            path: API endpoint path.
            data: Request body data.
            params: Optional query parameters.

        Returns:
            Response data.
        """
        return await self._client.put(path, data=data, params=params)

    async def _delete(self, path: str, params: dict[str, Any] | None = None) -> Any:
        """Make async DELETE request.

        Args:
            path: API endpoint path.
            params: Optional query parameters.

        Returns:
            Response data.
        """
        return await self._client.delete(path, params=params)
