"""HR Platform SDK Client.

Synchronous client for interacting with the HR Platform API.

Example:
    >>> from hr_platform import HRPlatformClient
    >>>
    >>> # API key authentication (recommended for services)
    >>> client = HRPlatformClient.with_api_key(
    ...     "hrp_live_xxx...",
    ...     base_url="https://hr-platform.vercel.app",
    ... )
    >>>
    >>> # Cookie authentication (for browser apps)
    >>> client = HRPlatformClient.with_cookie_auth()
    >>>
    >>> # Use the client
    >>> records = client.records.list(entity="BVD")
    >>> summary = client.analytics.get_summary()
"""

from __future__ import annotations

from typing import Any

from hr_platform.core.config import (
    ApiKeyAuth,
    CookieAuth,
    HRPlatformConfig,
    RetryConfig,
)
from hr_platform.core.http import HttpClient
from hr_platform.resources.admin import AdminResource
from hr_platform.resources.analytics import AnalyticsResource
from hr_platform.resources.compliance import ComplianceResource
from hr_platform.resources.records import RecordsResource
from hr_platform.resources.users import UsersResource
from hr_platform.resources.webhooks import WebhooksResource


class HRPlatformClient:
    """Synchronous HR Platform API client.

    The main entry point for interacting with the HR Platform API.
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
        >>> client = HRPlatformClient.with_api_key("hrp_live_xxx...")
        >>>
        >>> # List records
        >>> records = client.records.list()
        >>>
        >>> # Get analytics
        >>> summary = client.analytics.get_summary()
        >>>
        >>> # Create a record
        >>> from hr_platform.models import CreateRecordRequest
        >>> response = client.records.create(CreateRecordRequest(
        ...     entity="BVD",
        ...     year=2025,
        ...     month=12,
        ... ))
        >>>
        >>> # Clean up when done
        >>> client.close()
    """

    def __init__(self, config: HRPlatformConfig) -> None:
        """Initialize the client with configuration.

        Prefer using factory methods instead of direct instantiation:
        - `HRPlatformClient.with_api_key()` for service integrations
        - `HRPlatformClient.with_cookie_auth()` for browser apps

        Args:
            config: SDK configuration with auth, base URL, and retry settings.
        """
        self._config = config
        self._http_client = HttpClient(config)

        # Initialize resources
        self.records = RecordsResource(self._http_client)
        self.analytics = AnalyticsResource(self._http_client)
        self.users = UsersResource(self._http_client)
        self.admin = AdminResource(self._http_client)
        self.compliance = ComplianceResource(self._http_client)
        self.webhooks = WebhooksResource(self._http_client)

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
    ) -> "HRPlatformClient":
        """Create a client with API key authentication.

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
            Configured HRPlatformClient instance.

        Example:
            >>> client = HRPlatformClient.with_api_key(
            ...     "hrp_live_aBcDeFgH...",
            ...     base_url="https://hr-platform.vercel.app",
            ...     timeout=60.0,
            ... )
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
    ) -> "HRPlatformClient":
        """Create a client with cookie-based session authentication.

        This method is intended for browser-based applications that use
        HTTP cookies for session management.

        Args:
            base_url: Base URL for the API server.
            api_version: API version (default: "v1").
            timeout: Request timeout in seconds (default: 30.0).
            retry: Custom retry configuration.
            headers: Additional headers to include in requests.

        Returns:
            Configured HRPlatformClient instance.

        Example:
            >>> client = HRPlatformClient.with_cookie_auth(
            ...     base_url="https://hr-platform.vercel.app",
            ... )
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
    def from_config(cls, config: HRPlatformConfig) -> "HRPlatformClient":
        """Create a client from an existing configuration.

        Args:
            config: Pre-configured HRPlatformConfig instance.

        Returns:
            Configured HRPlatformClient instance.

        Example:
            >>> from hr_platform.core.config import HRPlatformConfig, ApiKeyAuth
            >>> config = HRPlatformConfig(
            ...     base_url="https://hr-platform.vercel.app",
            ...     auth=ApiKeyAuth(api_key="hrp_live_xxx..."),
            ... )
            >>> client = HRPlatformClient.from_config(config)
        """
        return cls(config)

    @property
    def config(self) -> HRPlatformConfig:
        """Get the current configuration.

        Returns:
            The SDK configuration.
        """
        return self._config

    def close(self) -> None:
        """Close the client and release resources.

        Should be called when the client is no longer needed,
        or use the client as a context manager.

        Example:
            >>> client = HRPlatformClient.with_api_key("hrp_live_xxx...")
            >>> try:
            ...     records = client.records.list()
            ... finally:
            ...     client.close()
        """
        self._http_client.close()

    def __enter__(self) -> "HRPlatformClient":
        """Enter context manager.

        Example:
            >>> with HRPlatformClient.with_api_key("hrp_live_xxx...") as client:
            ...     records = client.records.list()
        """
        return self

    def __exit__(self, *args: Any) -> None:
        """Exit context manager and close client."""
        self.close()

    def __repr__(self) -> str:
        """Return string representation of the client."""
        auth_type = self._config.auth.type
        return f"HRPlatformClient(base_url={self._config.base_url!r}, auth={auth_type})"
