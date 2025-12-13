"""HR Platform SDK Async Client.

Asynchronous client for interacting with the HR Platform API.

Example:
    >>> from hr_platform import AsyncHRPlatformClient
    >>>
    >>> # API key authentication (recommended for services)
    >>> async with AsyncHRPlatformClient.with_api_key(
    ...     "hrp_live_xxx...",
    ...     base_url="https://hr-platform.vercel.app",
    ... ) as client:
    ...     records = await client.records.list(entity="BVD")
    ...     summary = await client.analytics.get_summary()
"""

from __future__ import annotations

from typing import Any

from hr_platform.core.async_http import AsyncHttpClient
from hr_platform.core.config import (
    ApiKeyAuth,
    CookieAuth,
    HRPlatformConfig,
    RetryConfig,
)
from hr_platform.resources.admin import AsyncAdminResource
from hr_platform.resources.analytics import AsyncAnalyticsResource
from hr_platform.resources.compliance import AsyncComplianceResource
from hr_platform.resources.records import AsyncRecordsResource
from hr_platform.resources.users import AsyncUsersResource
from hr_platform.resources.webhooks import AsyncWebhooksResource


class AsyncHRPlatformClient:
    """Asynchronous HR Platform API client.

    The main entry point for async interaction with the HR Platform API.
    Use the factory methods `with_api_key()` or `with_cookie_auth()`
    to create properly configured instances.

    Attributes:
        records: HR records resource for CRUD and workflow operations.
        analytics: Analytics resource for metrics and trends.
        users: User management resource.
        admin: Admin resource for system administration.
        compliance: Compliance resource for GDPR document flow.
        webhooks: Webhooks resource for subscription management.

    Example:
        >>> async with AsyncHRPlatformClient.with_api_key("hrp_live_xxx...") as client:
        ...     # List records
        ...     records = await client.records.list()
        ...
        ...     # Get analytics
        ...     summary = await client.analytics.get_summary()
        ...
        ...     # Create a record
        ...     from hr_platform.models import CreateRecordRequest
        ...     response = await client.records.create(CreateRecordRequest(
        ...         entity="BVD",
        ...         year=2025,
        ...         month=12,
        ...     ))
    """

    def __init__(self, config: HRPlatformConfig) -> None:
        """Initialize the async client with configuration.

        Prefer using factory methods instead of direct instantiation:
        - `AsyncHRPlatformClient.with_api_key()` for service integrations
        - `AsyncHRPlatformClient.with_cookie_auth()` for browser apps

        Args:
            config: SDK configuration with auth, base URL, and retry settings.
        """
        self._config = config
        self._http_client = AsyncHttpClient(config)

        # Initialize resources
        self.records = AsyncRecordsResource(self._http_client)
        self.analytics = AsyncAnalyticsResource(self._http_client)
        self.users = AsyncUsersResource(self._http_client)
        self.admin = AsyncAdminResource(self._http_client)
        self.compliance = AsyncComplianceResource(self._http_client)
        self.webhooks = AsyncWebhooksResource(self._http_client)

    @classmethod
    def with_api_key(
        cls,
        api_key: str,
        *,
        base_url: str = "http://localhost:4000",
        api_version: str = "v1",
        timeout: float = 30.0,
        retry: RetryConfig | None = None,
        headers: dict[str, str] | None = None,
    ) -> "AsyncHRPlatformClient":
        """Create an async client with API key authentication.

        This is the recommended method for service-to-service integrations.
        API keys provide scoped access without requiring interactive login.

        Args:
            api_key: API key (format: hrp_{env}_{random}).
            base_url: Base URL for the API server.
            api_version: API version (default: "v1").
            timeout: Request timeout in seconds (default: 30.0).
            retry: Custom retry configuration.
            headers: Additional headers to include in requests.

        Returns:
            Configured AsyncHRPlatformClient instance.

        Example:
            >>> async with AsyncHRPlatformClient.with_api_key(
            ...     "hrp_live_aBcDeFgH...",
            ...     base_url="https://hr-platform.vercel.app",
            ...     timeout=60.0,
            ... ) as client:
            ...     records = await client.records.list()
        """
        config = HRPlatformConfig(
            base_url=base_url,
            api_version=api_version,
            auth=ApiKeyAuth(api_key=api_key),
            timeout=timeout,
            retry=retry or RetryConfig(),
            headers=headers or {},
        )
        return cls(config)

    @classmethod
    def with_cookie_auth(
        cls,
        *,
        base_url: str = "http://localhost:4000",
        api_version: str = "v1",
        timeout: float = 30.0,
        retry: RetryConfig | None = None,
        headers: dict[str, str] | None = None,
    ) -> "AsyncHRPlatformClient":
        """Create an async client with cookie-based session authentication.

        This method is intended for browser-based applications that use
        HTTP cookies for session management.

        Args:
            base_url: Base URL for the API server.
            api_version: API version (default: "v1").
            timeout: Request timeout in seconds (default: 30.0).
            retry: Custom retry configuration.
            headers: Additional headers to include in requests.

        Returns:
            Configured AsyncHRPlatformClient instance.

        Example:
            >>> async with AsyncHRPlatformClient.with_cookie_auth(
            ...     base_url="https://hr-platform.vercel.app",
            ... ) as client:
            ...     records = await client.records.list()
        """
        config = HRPlatformConfig(
            base_url=base_url,
            api_version=api_version,
            auth=CookieAuth(),
            timeout=timeout,
            retry=retry or RetryConfig(),
            headers=headers or {},
        )
        return cls(config)

    @classmethod
    def from_config(cls, config: HRPlatformConfig) -> "AsyncHRPlatformClient":
        """Create an async client from an existing configuration.

        Args:
            config: Pre-configured HRPlatformConfig instance.

        Returns:
            Configured AsyncHRPlatformClient instance.

        Example:
            >>> from hr_platform.core.config import HRPlatformConfig, ApiKeyAuth
            >>> config = HRPlatformConfig(
            ...     base_url="https://hr-platform.vercel.app",
            ...     auth=ApiKeyAuth(api_key="hrp_live_xxx..."),
            ... )
            >>> client = AsyncHRPlatformClient.from_config(config)
        """
        return cls(config)

    @property
    def config(self) -> HRPlatformConfig:
        """Get the current configuration.

        Returns:
            The SDK configuration.
        """
        return self._config

    async def close(self) -> None:
        """Close the client and release resources.

        Should be called when the client is no longer needed,
        or use the client as an async context manager.

        Example:
            >>> client = AsyncHRPlatformClient.with_api_key("hrp_live_xxx...")
            >>> try:
            ...     records = await client.records.list()
            ... finally:
            ...     await client.close()
        """
        await self._http_client.close()

    async def __aenter__(self) -> "AsyncHRPlatformClient":
        """Enter async context manager.

        Example:
            >>> async with AsyncHRPlatformClient.with_api_key("hrp_live_xxx...") as client:
            ...     records = await client.records.list()
        """
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Exit async context manager and close client."""
        await self.close()

    def __repr__(self) -> str:
        """Return string representation of the client."""
        auth_type = self._config.auth.type
        return f"AsyncHRPlatformClient(base_url={self._config.base_url!r}, auth={auth_type})"
