"""Synchronous HTTP client with retry logic.

This module provides the core HTTP client wrapper used by all SDK resources.
It implements exponential backoff with jitter for transient failures.

Example:
    >>> from hr_platform.core.http import HttpClient
    >>> from hr_platform.core.config import HRPlatformConfig, ApiKeyAuth
    >>>
    >>> config = HRPlatformConfig(
    ...     base_url="https://hr-platform.vercel.app",
    ...     auth=ApiKeyAuth(api_key="hrp_live_xxx..."),
    ... )
    >>> client = HttpClient(config)
    >>> response = client.get("/records")
"""

from __future__ import annotations

import random
import time
from typing import Any, TypeVar

import httpx

from hr_platform.core.config import ApiKeyAuth, CookieAuth, HRPlatformConfig
from hr_platform.exceptions import (
    HRPlatformError,
    NetworkError,
    TimeoutError,
    parse_api_error,
)

T = TypeVar("T")


class HttpClient:
    """Synchronous HTTP client with automatic retry logic.

    This client wraps httpx to provide:
    - Automatic retries with exponential backoff
    - Jitter to prevent thundering herd
    - Respect for Retry-After headers
    - Proper error parsing into typed exceptions

    Attributes:
        config: SDK configuration including auth and retry settings.

    Example:
        >>> client = HttpClient(config)
        >>> records = client.get("/records")
        >>> new_record = client.post("/records", json={"entity": "BVD", ...})
    """

    def __init__(self, config: HRPlatformConfig) -> None:
        """Initialize the HTTP client.

        Args:
            config: SDK configuration with base URL, auth, and retry settings.
        """
        self.config = config
        self._client: httpx.Client | None = None

    def _get_client(self) -> httpx.Client:
        """Get or create the httpx client instance.

        Returns:
            Configured httpx.Client instance.
        """
        if self._client is None:
            headers = self._build_headers()
            self._client = httpx.Client(
                base_url=self.config.get_api_url(),
                headers=headers,
                timeout=httpx.Timeout(self.config.timeout),
                follow_redirects=True,
            )
        return self._client

    def _build_headers(self) -> dict[str, str]:
        """Build request headers including authentication.

        Returns:
            Dictionary of HTTP headers.
        """
        headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "hr-platform-sdk-python/0.1.0",
            **self.config.headers,
        }

        # Add authentication header
        if isinstance(self.config.auth, ApiKeyAuth):
            headers["X-API-Key"] = self.config.auth.api_key
        # CookieAuth doesn't need explicit headers - cookies handled by httpx

        return headers

    def _calculate_delay(self, attempt: int, retry_after: float | None = None) -> float:
        """Calculate delay before next retry attempt.

        Uses exponential backoff with jitter:
            delay = min(initial_delay * (multiplier ^ attempt) + jitter, max_delay)

        Args:
            attempt: Current retry attempt number (0-indexed).
            retry_after: Optional Retry-After header value from server.

        Returns:
            Delay in seconds before next retry.
        """
        retry_config = self.config.retry

        # Respect Retry-After header if configured and present
        if retry_config.respect_retry_after and retry_after is not None:
            return min(retry_after, retry_config.max_delay)

        # Calculate exponential backoff
        base_delay = retry_config.initial_delay * (
            retry_config.backoff_multiplier**attempt
        )

        # Add jitter (0-25% of base delay)
        jitter = random.uniform(0, base_delay * 0.25)
        delay = base_delay + jitter

        return min(delay, retry_config.max_delay)

    def _parse_retry_after(self, response: httpx.Response) -> float | None:
        """Parse Retry-After header from response.

        Args:
            response: HTTP response object.

        Returns:
            Retry-After value in seconds, or None if not present.
        """
        retry_after = response.headers.get("Retry-After")
        if retry_after is None:
            return None

        try:
            return float(retry_after)
        except ValueError:
            # Could be a date string - not supported for simplicity
            return None

    def _should_retry(self, status_code: int, attempt: int) -> bool:
        """Determine if request should be retried.

        Args:
            status_code: HTTP status code from response.
            attempt: Current retry attempt number.

        Returns:
            True if request should be retried.
        """
        retry_config = self.config.retry

        if attempt >= retry_config.max_retries:
            return False

        return status_code in retry_config.retryable_statuses

    def _request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> Any:
        """Make an HTTP request with retry logic.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE).
            path: API endpoint path (relative to base URL).
            **kwargs: Additional arguments passed to httpx.

        Returns:
            Parsed JSON response data.

        Raises:
            HRPlatformError: For API errors.
            NetworkError: For connection failures.
            TimeoutError: For request timeouts.
        """
        client = self._get_client()
        last_error: Exception | None = None

        for attempt in range(self.config.retry.max_retries + 1):
            try:
                response = client.request(method, path, **kwargs)

                # Success - return parsed JSON
                if response.is_success:
                    # Handle empty responses
                    if not response.content:
                        return None
                    return response.json()

                # Check if we should retry
                if self._should_retry(response.status_code, attempt):
                    retry_after = self._parse_retry_after(response)
                    delay = self._calculate_delay(attempt, retry_after)
                    time.sleep(delay)
                    continue

                # Parse error response
                try:
                    body = response.json()
                except Exception:
                    body = {"error": response.text}

                raise parse_api_error(
                    status=response.status_code,
                    body=body,
                    headers=dict(response.headers),
                )

            except httpx.TimeoutException as e:
                last_error = e
                if attempt < self.config.retry.max_retries:
                    delay = self._calculate_delay(attempt)
                    time.sleep(delay)
                    continue
                raise TimeoutError(self.config.timeout) from e

            except httpx.ConnectError as e:
                last_error = e
                if attempt < self.config.retry.max_retries:
                    delay = self._calculate_delay(attempt)
                    time.sleep(delay)
                    continue
                raise NetworkError(f"Connection failed: {e}", cause=e) from e

            except httpx.HTTPStatusError as e:
                # Should be handled by response.is_success check above
                last_error = e
                raise NetworkError(f"HTTP error: {e}", cause=e) from e

            except HRPlatformError:
                # Re-raise our own errors
                raise

            except Exception as e:
                last_error = e
                raise NetworkError(f"Request failed: {e}", cause=e) from e

        # Should not reach here, but handle gracefully
        if last_error:
            raise NetworkError(f"Request failed after retries: {last_error}")
        raise NetworkError("Request failed")

    def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        """Make a GET request.

        Args:
            path: API endpoint path.
            params: Optional query parameters.

        Returns:
            Parsed JSON response.

        Example:
            >>> records = client.get("/records", params={"entity": "BVD"})
        """
        return self._request("GET", path, params=params)

    def post(self, path: str, json: dict[str, Any] | None = None) -> Any:
        """Make a POST request.

        Args:
            path: API endpoint path.
            json: Request body as dictionary.

        Returns:
            Parsed JSON response.

        Example:
            >>> result = client.post("/records", json={"entity": "BVD", ...})
        """
        return self._request("POST", path, json=json)

    def put(self, path: str, json: dict[str, Any] | None = None) -> Any:
        """Make a PUT request.

        Args:
            path: API endpoint path.
            json: Request body as dictionary.

        Returns:
            Parsed JSON response.

        Example:
            >>> result = client.put("/records/123", json={"entity": "BVD", ...})
        """
        return self._request("PUT", path, json=json)

    def delete(self, path: str) -> Any:
        """Make a DELETE request.

        Args:
            path: API endpoint path.

        Returns:
            Parsed JSON response.

        Example:
            >>> result = client.delete("/records/123")
        """
        return self._request("DELETE", path)

    def close(self) -> None:
        """Close the HTTP client and release resources.

        Should be called when the client is no longer needed.
        """
        if self._client is not None:
            self._client.close()
            self._client = None

    def __enter__(self) -> "HttpClient":
        """Enter context manager."""
        return self

    def __exit__(self, *args: Any) -> None:
        """Exit context manager and close client."""
        self.close()
