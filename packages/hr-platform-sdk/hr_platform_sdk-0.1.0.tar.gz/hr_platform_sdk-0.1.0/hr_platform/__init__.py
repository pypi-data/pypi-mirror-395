"""HR Platform Python SDK.

Type-safe Python SDK for the HR Platform API with async support and pandas integration.

Example:
    >>> from hr_platform import HRPlatformClient
    >>>
    >>> # API Key authentication (service-to-service)
    >>> client = HRPlatformClient.with_api_key(
    ...     "hrp_live_xxx...",
    ...     base_url="https://hr-platform.vercel.app"
    ... )
    >>> records = client.records.list()
    >>>
    >>> # Async usage
    >>> from hr_platform import AsyncHRPlatformClient
    >>> async with AsyncHRPlatformClient.with_api_key("hrp_live_xxx...") as client:
    ...     records = await client.records.list()
"""

from hr_platform.client import HRPlatformClient
from hr_platform.async_client import AsyncHRPlatformClient
from hr_platform.core.config import (
    HRPlatformConfig,
    RetryConfig,
    ApiKeyAuth,
    CookieAuth,
)
from hr_platform.exceptions import (
    HRPlatformError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    ConflictError,
    ServerError,
    NetworkError,
    TimeoutError,
)

__version__ = "0.1.0"

__all__ = [
    # Clients
    "HRPlatformClient",
    "AsyncHRPlatformClient",
    # Configuration
    "HRPlatformConfig",
    "RetryConfig",
    "ApiKeyAuth",
    "CookieAuth",
    # Exceptions
    "HRPlatformError",
    "AuthenticationError",
    "AuthorizationError",
    "NotFoundError",
    "ValidationError",
    "RateLimitError",
    "ConflictError",
    "ServerError",
    "NetworkError",
    "TimeoutError",
    # Version
    "__version__",
]
