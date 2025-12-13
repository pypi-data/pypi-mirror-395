"""HR Platform SDK Exception Classes.

Structured exception classes matching HTTP status codes and API error responses.
All exceptions inherit from HRPlatformError for easy catching.

Example:
    >>> from hr_platform import HRPlatformClient
    >>> from hr_platform.exceptions import NotFoundError, RateLimitError
    >>>
    >>> try:
    ...     record = client.records.get("invalid-id")
    ... except NotFoundError:
    ...     print("Record not found")
    ... except RateLimitError as e:
    ...     print(f"Rate limited. Retry after {e.retry_after} seconds")
"""

from __future__ import annotations

from typing import Any


class HRPlatformError(Exception):
    """Base exception for all SDK errors.

    All SDK exceptions inherit from this class, making it easy to catch
    any SDK-related error with a single except clause.

    Attributes:
        message: Human-readable error message.
        status: HTTP status code (if applicable).
        code: Machine-readable error code.
        body: Original response body (if available).
    """

    def __init__(
        self,
        message: str,
        *,
        status: int | None = None,
        code: str | None = None,
        body: Any = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status = status
        self.code = code
        self.body = body

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message={self.message!r}, status={self.status})"

    def __str__(self) -> str:
        if self.status:
            return f"[{self.status}] {self.message}"
        return self.message


class AuthenticationError(HRPlatformError):
    """Authentication error (HTTP 401).

    Raised when API key or session is invalid, expired, or missing.

    Example:
        >>> try:
        ...     client.records.list()
        ... except AuthenticationError:
        ...     print("Please check your API key")
    """

    def __init__(
        self,
        message: str = "Authentication required",
        body: Any = None,
    ) -> None:
        super().__init__(
            message,
            status=401,
            code="AUTHENTICATION_ERROR",
            body=body,
        )


class AuthorizationError(HRPlatformError):
    """Authorization error (HTTP 403).

    Raised when user lacks permission for the requested operation.
    This can occur when:
    - Accessing resources outside your entity scope
    - Attempting admin operations without admin role
    - Accessing workflow actions without proper permissions

    Example:
        >>> try:
        ...     client.admin.list_users()
        ... except AuthorizationError:
        ...     print("Admin access required")
    """

    def __init__(
        self,
        message: str = "Insufficient permissions",
        body: Any = None,
    ) -> None:
        super().__init__(
            message,
            status=403,
            code="AUTHORIZATION_ERROR",
            body=body,
        )


class NotFoundError(HRPlatformError):
    """Not found error (HTTP 404).

    Raised when the requested resource does not exist.

    Attributes:
        resource_type: Type of resource that was not found (e.g., "record", "user").
        resource_id: ID of the resource that was not found.

    Example:
        >>> try:
        ...     record = client.records.get("non-existent-id")
        ... except NotFoundError as e:
        ...     print(f"Resource {e.resource_id} not found")
    """

    def __init__(
        self,
        message: str = "Resource not found",
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        body: Any = None,
    ) -> None:
        super().__init__(
            message,
            status=404,
            code="NOT_FOUND",
            body=body,
        )
        self.resource_type = resource_type
        self.resource_id = resource_id


class ValidationError(HRPlatformError):
    """Validation error (HTTP 400).

    Raised when request data fails validation. Contains field-level
    error details when available.

    Attributes:
        fields: List of field-level errors with 'field' and 'message' keys.

    Example:
        >>> try:
        ...     client.records.create(invalid_data)
        ... except ValidationError as e:
        ...     for field_error in e.fields:
        ...         print(f"{field_error['field']}: {field_error['message']}")
    """

    def __init__(
        self,
        message: str = "Validation failed",
        fields: list[dict[str, str]] | None = None,
        body: Any = None,
    ) -> None:
        super().__init__(
            message,
            status=400,
            code="VALIDATION_ERROR",
            body=body,
        )
        self.fields = fields or []


class RateLimitError(HRPlatformError):
    """Rate limit error (HTTP 429).

    Raised when request rate limit is exceeded. Contains information
    about when to retry.

    Attributes:
        retry_after: Number of seconds to wait before retrying.
        limit: The rate limit that was exceeded.
        remaining: Number of requests remaining in the window.

    Example:
        >>> try:
        ...     client.records.list()
        ... except RateLimitError as e:
        ...     if e.retry_after:
        ...         time.sleep(e.retry_after)
        ...         # Retry the request
    """

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        *,
        retry_after: int | None = None,
        limit: int | None = None,
        remaining: int | None = None,
        body: Any = None,
    ) -> None:
        super().__init__(
            message,
            status=429,
            code="RATE_LIMIT_ERROR",
            body=body,
        )
        self.retry_after = retry_after
        self.limit = limit
        self.remaining = remaining


class ConflictError(HRPlatformError):
    """Conflict error (HTTP 409).

    Raised when a resource already exists or there's a conflict
    with the current state (e.g., duplicate record for entity/year/month).

    Example:
        >>> try:
        ...     client.records.create(duplicate_record)
        ... except ConflictError:
        ...     print("Record already exists for this period")
    """

    def __init__(
        self,
        message: str = "Resource already exists",
        body: Any = None,
    ) -> None:
        super().__init__(
            message,
            status=409,
            code="CONFLICT_ERROR",
            body=body,
        )


class ServerError(HRPlatformError):
    """Server error (HTTP 5xx).

    Raised for server-side errors. These are typically transient
    and the request may succeed on retry.

    Example:
        >>> try:
        ...     client.records.list()
        ... except ServerError as e:
        ...     print(f"Server error ({e.status}): {e.message}")
    """

    def __init__(
        self,
        message: str = "Server error",
        status: int = 500,
        body: Any = None,
    ) -> None:
        super().__init__(
            message,
            status=status,
            code="SERVER_ERROR",
            body=body,
        )


class NetworkError(HRPlatformError):
    """Network error.

    Raised when the request fails due to network issues such as
    DNS resolution failures, connection refused, or connection reset.

    Example:
        >>> try:
        ...     client.records.list()
        ... except NetworkError as e:
        ...     print(f"Network error: {e.message}")
        ...     if e.__cause__:
        ...         print(f"Caused by: {e.__cause__}")
    """

    def __init__(
        self,
        message: str = "Network error",
        cause: BaseException | None = None,
    ) -> None:
        super().__init__(message, code="NETWORK_ERROR")
        self.__cause__ = cause


class TimeoutError(HRPlatformError):
    """Timeout error.

    Raised when the request exceeds the configured timeout.

    Attributes:
        timeout: The timeout value in seconds that was exceeded.

    Example:
        >>> try:
        ...     client.records.list()
        ... except TimeoutError as e:
        ...     print(f"Request timed out after {e.timeout}s")
    """

    def __init__(self, timeout: float) -> None:
        super().__init__(
            f"Request timed out after {timeout}s",
            code="TIMEOUT_ERROR",
        )
        self.timeout = timeout


def parse_api_error(
    status: int,
    body: Any,
    headers: dict[str, str] | None = None,
) -> HRPlatformError:
    """Parse an API error response into the appropriate exception class.

    This function inspects the HTTP status code and response body to
    create the most appropriate exception class.

    Args:
        status: HTTP status code.
        body: Response body (typically a dict with 'error' key).
        headers: Response headers (used for rate limit info).

    Returns:
        An appropriate HRPlatformError subclass instance.
    """
    headers = headers or {}

    # Extract message from body
    message: str | None = None
    if isinstance(body, dict):
        message = body.get("error") or body.get("message")

    if status == 400:
        details = body.get("details", []) if isinstance(body, dict) else []
        return ValidationError(
            message or "Validation failed",
            fields=details,
            body=body,
        )

    if status == 401:
        return AuthenticationError(
            message or "Authentication required",
            body=body,
        )

    if status == 403:
        return AuthorizationError(
            message or "Insufficient permissions",
            body=body,
        )

    if status == 404:
        return NotFoundError(
            message or "Resource not found",
            body=body,
        )

    if status == 409:
        return ConflictError(
            message or "Resource already exists",
            body=body,
        )

    if status == 429:
        # Parse rate limit headers
        retry_after_str = headers.get("retry-after") or headers.get("Retry-After")
        limit_str = headers.get("x-ratelimit-limit") or headers.get("X-RateLimit-Limit")
        remaining_str = headers.get("x-ratelimit-remaining") or headers.get("X-RateLimit-Remaining")

        return RateLimitError(
            message or "Rate limit exceeded",
            retry_after=int(retry_after_str) if retry_after_str else None,
            limit=int(limit_str) if limit_str else None,
            remaining=int(remaining_str) if remaining_str else None,
            body=body,
        )

    if status >= 500:
        return ServerError(
            message or "Server error",
            status=status,
            body=body,
        )

    # Default for other status codes
    return HRPlatformError(
        message or f"HTTP {status} error",
        status=status,
        body=body,
    )
