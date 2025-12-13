"""Tests for HR Platform SDK exceptions."""

from __future__ import annotations

import pytest

from hr_platform.exceptions import (
    AuthenticationError,
    AuthorizationError,
    ConflictError,
    HRPlatformError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ServerError,
    TimeoutError,
    ValidationError,
    parse_api_error,
)


class TestHRPlatformError:
    """Tests for base HRPlatformError exception."""

    def test_init_with_message(self) -> None:
        """Test error with just a message."""
        error = HRPlatformError("Something went wrong")
        assert error.message == "Something went wrong"
        assert error.status is None
        assert error.code is None
        assert error.body is None

    def test_init_with_status(self) -> None:
        """Test error with status code."""
        error = HRPlatformError("Error", status=500)
        assert error.status == 500
        assert str(error) == "[500] Error"

    def test_init_with_body(self) -> None:
        """Test error with response body."""
        body = {"error": "details"}
        error = HRPlatformError("Error", body=body)
        assert error.body == body

    def test_repr(self) -> None:
        """Test error repr."""
        error = HRPlatformError("Error", status=500)
        assert repr(error) == "HRPlatformError(message='Error', status=500)"


class TestAuthenticationError:
    """Tests for AuthenticationError."""

    def test_default_message(self) -> None:
        """Test default authentication error message."""
        error = AuthenticationError()
        assert error.message == "Authentication required"
        assert error.status == 401
        assert error.code == "AUTHENTICATION_ERROR"

    def test_custom_message(self) -> None:
        """Test custom authentication error message."""
        error = AuthenticationError("Invalid API key")
        assert error.message == "Invalid API key"
        assert error.status == 401


class TestAuthorizationError:
    """Tests for AuthorizationError."""

    def test_default_message(self) -> None:
        """Test default authorization error message."""
        error = AuthorizationError()
        assert error.message == "Insufficient permissions"
        assert error.status == 403
        assert error.code == "AUTHORIZATION_ERROR"

    def test_custom_message(self) -> None:
        """Test custom authorization error message."""
        error = AuthorizationError("Admin role required")
        assert error.message == "Admin role required"


class TestNotFoundError:
    """Tests for NotFoundError."""

    def test_default_message(self) -> None:
        """Test default not found error message."""
        error = NotFoundError()
        assert error.message == "Resource not found"
        assert error.status == 404
        assert error.code == "NOT_FOUND"

    def test_with_resource_type(self) -> None:
        """Test not found error with resource type."""
        error = NotFoundError("Record not found", resource_type="record")
        assert error.resource_type == "record"

    def test_with_resource_id(self) -> None:
        """Test not found error with resource id."""
        error = NotFoundError("Record not found", resource_id="uuid-123")
        assert error.resource_id == "uuid-123"


class TestValidationError:
    """Tests for ValidationError."""

    def test_default_message(self) -> None:
        """Test default validation error message."""
        error = ValidationError()
        assert error.message == "Validation failed"
        assert error.status == 400
        assert error.code == "VALIDATION_ERROR"
        assert error.fields == []

    def test_with_fields(self) -> None:
        """Test validation error with field errors."""
        fields = [{"field": "email", "message": "Required"}]
        error = ValidationError("Validation failed", fields=fields)
        assert error.fields == fields

    def test_fields_default_empty(self) -> None:
        """Test fields default to empty list."""
        error = ValidationError()
        assert error.fields == []


class TestRateLimitError:
    """Tests for RateLimitError."""

    def test_default_message(self) -> None:
        """Test default rate limit error message."""
        error = RateLimitError()
        assert error.message == "Rate limit exceeded"
        assert error.status == 429
        assert error.code == "RATE_LIMIT_ERROR"

    def test_with_retry_after(self) -> None:
        """Test rate limit error with retry after."""
        error = RateLimitError(retry_after=60)
        assert error.retry_after == 60

    def test_retry_after_default_none(self) -> None:
        """Test retry_after defaults to None."""
        error = RateLimitError()
        assert error.retry_after is None


class TestConflictError:
    """Tests for ConflictError."""

    def test_default_message(self) -> None:
        """Test default conflict error message."""
        error = ConflictError()
        assert error.message == "Resource already exists"
        assert error.status == 409
        assert error.code == "CONFLICT_ERROR"

    def test_custom_message(self) -> None:
        """Test custom conflict error message."""
        error = ConflictError("Duplicate record")
        assert error.message == "Duplicate record"


class TestServerError:
    """Tests for ServerError."""

    def test_default_message(self) -> None:
        """Test default server error message."""
        error = ServerError()
        assert error.message == "Server error"
        assert error.status == 500
        assert error.code == "SERVER_ERROR"

    def test_with_custom_status_code(self) -> None:
        """Test server error with custom status code."""
        error = ServerError("Bad gateway", status=502)
        assert error.status == 502


class TestNetworkError:
    """Tests for NetworkError."""

    def test_default_message(self) -> None:
        """Test default network error message."""
        error = NetworkError()
        assert error.message == "Network error"
        assert error.code == "NETWORK_ERROR"
        assert error.status is None

    def test_with_original_error(self) -> None:
        """Test network error with original cause."""
        cause = ConnectionError("Connection refused")
        error = NetworkError("Connection failed", cause=cause)
        assert error.__cause__ is cause


class TestTimeoutError:
    """Tests for TimeoutError."""

    def test_timeout_message(self) -> None:
        """Test timeout error message includes seconds."""
        error = TimeoutError(30.0)
        assert "30" in error.message
        assert error.code == "TIMEOUT_ERROR"

    def test_with_timeout_seconds(self) -> None:
        """Test timeout error stores timeout value."""
        error = TimeoutError(45.5)
        assert error.timeout == 45.5


class TestExceptionHierarchy:
    """Tests for exception inheritance hierarchy."""

    def test_all_inherit_from_base(self) -> None:
        """Test all exceptions inherit from HRPlatformError."""
        exceptions = [
            AuthenticationError(),
            AuthorizationError(),
            NotFoundError(),
            ValidationError(),
            RateLimitError(),
            ConflictError(),
            ServerError(),
            NetworkError(),
            TimeoutError(30),
        ]
        for exc in exceptions:
            assert isinstance(exc, HRPlatformError)

    def test_can_catch_with_base_class(self) -> None:
        """Test catching specific exception with base class."""
        with pytest.raises(HRPlatformError):
            raise NotFoundError("Not found")

    def test_can_catch_specific_exception(self) -> None:
        """Test catching specific exception class."""
        with pytest.raises(NotFoundError):
            raise NotFoundError("Not found")

    def test_not_found_not_caught_as_auth_error(self) -> None:
        """Test NotFoundError is not caught by AuthenticationError."""
        with pytest.raises(NotFoundError):
            try:
                raise NotFoundError()
            except AuthenticationError:
                pytest.fail("NotFoundError should not be caught as AuthenticationError")


class TestParseApiError:
    """Tests for parse_api_error function."""

    def test_parse_400_validation_error(self) -> None:
        """Test parsing 400 status returns ValidationError."""
        body = {"error": "Invalid data", "details": [{"field": "email", "message": "Required"}]}
        error = parse_api_error(400, body)
        assert isinstance(error, ValidationError)
        assert error.fields == [{"field": "email", "message": "Required"}]

    def test_parse_401_authentication_error(self) -> None:
        """Test parsing 401 status returns AuthenticationError."""
        body = {"error": "Invalid token"}
        error = parse_api_error(401, body)
        assert isinstance(error, AuthenticationError)
        assert error.message == "Invalid token"

    def test_parse_403_authorization_error(self) -> None:
        """Test parsing 403 status returns AuthorizationError."""
        body = {"error": "Forbidden"}
        error = parse_api_error(403, body)
        assert isinstance(error, AuthorizationError)

    def test_parse_404_not_found_error(self) -> None:
        """Test parsing 404 status returns NotFoundError."""
        body = {"error": "Record not found"}
        error = parse_api_error(404, body)
        assert isinstance(error, NotFoundError)

    def test_parse_409_conflict_error(self) -> None:
        """Test parsing 409 status returns ConflictError."""
        body = {"error": "Duplicate record"}
        error = parse_api_error(409, body)
        assert isinstance(error, ConflictError)

    def test_parse_429_rate_limit_error(self) -> None:
        """Test parsing 429 status returns RateLimitError."""
        body = {"error": "Too many requests"}
        headers = {"Retry-After": "60", "X-RateLimit-Limit": "100"}
        error = parse_api_error(429, body, headers)
        assert isinstance(error, RateLimitError)
        assert error.retry_after == 60
        assert error.limit == 100

    def test_parse_500_server_error(self) -> None:
        """Test parsing 500 status returns ServerError."""
        body = {"error": "Internal server error"}
        error = parse_api_error(500, body)
        assert isinstance(error, ServerError)

    def test_parse_502_server_error(self) -> None:
        """Test parsing 502 status returns ServerError."""
        body = {"error": "Bad gateway"}
        error = parse_api_error(502, body)
        assert isinstance(error, ServerError)
        assert error.status == 502

    def test_parse_unknown_status(self) -> None:
        """Test parsing unknown status returns base HRPlatformError."""
        body = {"error": "Unknown error"}
        error = parse_api_error(418, body)
        assert isinstance(error, HRPlatformError)
        assert error.status == 418
