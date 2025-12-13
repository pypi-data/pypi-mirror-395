"""Core SDK components.

This module contains the core infrastructure for the SDK including
configuration, HTTP client, and retry logic.
"""

from hr_platform.core.config import (
    HRPlatformConfig,
    RetryConfig,
    ApiKeyAuth,
    CookieAuth,
    AuthConfig,
    DEFAULT_CONFIG,
    DEFAULT_RETRY_CONFIG,
)
from hr_platform.core.http import HttpClient
from hr_platform.core.async_http import AsyncHttpClient

__all__ = [
    # Configuration
    "HRPlatformConfig",
    "RetryConfig",
    "ApiKeyAuth",
    "CookieAuth",
    "AuthConfig",
    "DEFAULT_CONFIG",
    "DEFAULT_RETRY_CONFIG",
    # HTTP Clients
    "HttpClient",
    "AsyncHttpClient",
]
