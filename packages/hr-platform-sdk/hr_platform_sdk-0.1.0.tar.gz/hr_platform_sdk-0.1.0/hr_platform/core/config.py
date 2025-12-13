"""HR Platform SDK Configuration.

This module defines all configuration types used by the SDK including
authentication, retry logic, and general client settings.

Example:
    >>> from hr_platform.core.config import HRPlatformConfig, ApiKeyAuth, RetryConfig
    >>>
    >>> config = HRPlatformConfig(
    ...     base_url="https://hr-platform.vercel.app",
    ...     auth=ApiKeyAuth(api_key="hrp_live_xxx..."),
    ...     retry=RetryConfig(max_retries=5),
    ... )
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Union


@dataclass(frozen=True)
class RetryConfig:
    """Configuration for request retries with exponential backoff.

    The SDK uses exponential backoff with jitter to retry failed requests.
    The delay between retries is calculated as:
        delay = initial_delay * (backoff_multiplier ^ attempt) + jitter

    Attributes:
        max_retries: Maximum number of retry attempts (default: 3).
        initial_delay: Initial delay in seconds before first retry (default: 1.0).
        max_delay: Maximum delay in seconds between retries (default: 30.0).
        backoff_multiplier: Multiplier for exponential backoff (default: 2.0).
        retryable_statuses: HTTP status codes that trigger retries.
        respect_retry_after: Whether to respect Retry-After header from server.

    Example:
        >>> retry_config = RetryConfig(
        ...     max_retries=5,
        ...     initial_delay=0.5,
        ...     backoff_multiplier=2.5,
        ... )
    """

    max_retries: int = 3
    initial_delay: float = 1.0
    max_delay: float = 30.0
    backoff_multiplier: float = 2.0
    retryable_statuses: tuple[int, ...] = (408, 429, 500, 502, 503, 504)
    respect_retry_after: bool = True


@dataclass
class ApiKeyAuth:
    """API key authentication configuration.

    API keys are the recommended authentication method for service-to-service
    integrations. Keys follow the format: hrp_{env}_{random}

    Attributes:
        type: Authentication type identifier (always "api_key").
        api_key: The API key string.

    Example:
        >>> auth = ApiKeyAuth(api_key="hrp_live_aBcDeFgH...")
    """

    api_key: str
    type: Literal["api_key"] = "api_key"


@dataclass
class CookieAuth:
    """Cookie-based session authentication configuration.

    Cookie authentication is used for browser-based applications that
    maintain session state via HTTP cookies. The SDK will include
    cookies in requests automatically.

    Attributes:
        type: Authentication type identifier (always "cookie").

    Example:
        >>> auth = CookieAuth()  # Uses existing browser cookies
    """

    type: Literal["cookie"] = "cookie"


# Union type for authentication configuration
AuthConfig = Union[ApiKeyAuth, CookieAuth]


@dataclass
class HRPlatformConfig:
    """Main SDK configuration.

    This configuration object controls all aspects of the SDK's behavior
    including the API endpoint, authentication, timeouts, and retry logic.

    Attributes:
        base_url: Base URL for the API (default: http://localhost:4000).
        api_version: API version to use (default: "v1").
        auth: Authentication configuration (ApiKeyAuth or CookieAuth).
        timeout: Request timeout in seconds (default: 30.0).
        retry: Retry configuration for failed requests.
        headers: Additional headers to include in all requests.

    Example:
        >>> from hr_platform.core.config import HRPlatformConfig, ApiKeyAuth
        >>>
        >>> config = HRPlatformConfig(
        ...     base_url="https://hr-platform.vercel.app",
        ...     api_version="v1",
        ...     auth=ApiKeyAuth(api_key="hrp_live_xxx..."),
        ...     timeout=60.0,
        ... )
    """

    base_url: str = "http://localhost:4000"
    api_version: str = "v1"
    auth: AuthConfig = field(default_factory=CookieAuth)
    timeout: float = 30.0
    retry: RetryConfig = field(default_factory=RetryConfig)
    headers: dict[str, str] = field(default_factory=dict)

    def get_api_url(self) -> str:
        """Get the full API URL including version.

        Returns:
            Full API URL (e.g., "https://hr-platform.vercel.app/api/v1").
        """
        base = self.base_url.rstrip("/")
        return f"{base}/api/{self.api_version}"


# Default configurations for convenience
DEFAULT_RETRY_CONFIG = RetryConfig()
DEFAULT_CONFIG = HRPlatformConfig()
