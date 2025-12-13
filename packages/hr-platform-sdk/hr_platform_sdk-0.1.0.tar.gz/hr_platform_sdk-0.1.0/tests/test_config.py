"""Tests for HR Platform SDK configuration."""

from __future__ import annotations

import pytest
from dataclasses import FrozenInstanceError

from hr_platform.core.config import (
    ApiKeyAuth,
    CookieAuth,
    HRPlatformConfig,
    RetryConfig,
)


class TestRetryConfig:
    """Tests for RetryConfig."""

    def test_default_values(self) -> None:
        """Test default retry configuration values."""
        config = RetryConfig()
        assert config.max_retries == 3
        assert config.initial_delay == 1.0
        assert config.max_delay == 30.0
        assert config.backoff_multiplier == 2.0
        assert config.retryable_statuses == (408, 429, 500, 502, 503, 504)
        assert config.respect_retry_after is True

    def test_custom_values(self) -> None:
        """Test custom retry configuration values."""
        config = RetryConfig(
            max_retries=5,
            initial_delay=0.5,
            max_delay=60.0,
            backoff_multiplier=3.0,
            retryable_statuses=(500, 503),
        )
        assert config.max_retries == 5
        assert config.initial_delay == 0.5
        assert config.max_delay == 60.0
        assert config.backoff_multiplier == 3.0
        assert config.retryable_statuses == (500, 503)

    def test_immutability(self) -> None:
        """Test that RetryConfig is frozen (immutable)."""
        config = RetryConfig()
        with pytest.raises(FrozenInstanceError):
            config.max_retries = 10  # type: ignore

    def test_retryable_statuses_is_tuple(self) -> None:
        """Test retryable_statuses is a tuple for immutability."""
        config = RetryConfig()
        assert isinstance(config.retryable_statuses, tuple)


class TestApiKeyAuth:
    """Tests for ApiKeyAuth."""

    def test_creation(self) -> None:
        """Test creating API key auth."""
        auth = ApiKeyAuth(api_key="hrp_test_abc123")
        assert auth.api_key == "hrp_test_abc123"
        assert auth.type == "api_key"

    def test_type_literal(self) -> None:
        """Test auth type is correct literal."""
        auth = ApiKeyAuth(api_key="hrp_test_abc123")
        assert auth.type == "api_key"

    def test_type_is_default(self) -> None:
        """Test type field has default value."""
        auth = ApiKeyAuth(api_key="hrp_test_abc123")
        # Type is automatically set to "api_key"
        assert auth.type == "api_key"


class TestCookieAuth:
    """Tests for CookieAuth."""

    def test_creation(self) -> None:
        """Test creating cookie auth."""
        auth = CookieAuth()
        assert auth.type == "cookie"

    def test_type_literal(self) -> None:
        """Test auth type is correct literal."""
        auth = CookieAuth()
        assert auth.type == "cookie"


class TestHRPlatformConfig:
    """Tests for HRPlatformConfig."""

    def test_default_values(self) -> None:
        """Test default config values."""
        config = HRPlatformConfig()
        assert config.base_url == "http://localhost:4000"
        assert config.api_version == "v1"
        assert config.timeout == 30.0
        assert isinstance(config.retry, RetryConfig)
        assert config.headers == {}
        # Default auth is CookieAuth
        assert isinstance(config.auth, CookieAuth)

    def test_with_api_key_auth(self) -> None:
        """Test config with API key auth."""
        config = HRPlatformConfig(
            base_url="https://api.example.com",
            auth=ApiKeyAuth(api_key="hrp_test_abc123"),
        )
        assert config.base_url == "https://api.example.com"
        assert isinstance(config.auth, ApiKeyAuth)
        assert config.auth.api_key == "hrp_test_abc123"

    def test_with_cookie_auth(self) -> None:
        """Test config with cookie auth."""
        config = HRPlatformConfig(
            base_url="https://api.example.com",
            auth=CookieAuth(),
        )
        assert config.base_url == "https://api.example.com"
        assert isinstance(config.auth, CookieAuth)

    def test_custom_values(self) -> None:
        """Test custom config values."""
        retry = RetryConfig(max_retries=5)
        config = HRPlatformConfig(
            base_url="https://custom.example.com",
            api_version="v2",
            auth=ApiKeyAuth(api_key="hrp_live_xyz"),
            timeout=60.0,
            retry=retry,
            headers={"X-Custom": "value"},
        )
        assert config.base_url == "https://custom.example.com"
        assert config.api_version == "v2"
        assert config.timeout == 60.0
        assert config.retry.max_retries == 5
        assert config.headers == {"X-Custom": "value"}

    def test_get_api_url_method(self) -> None:
        """Test get_api_url method combines base_url and version."""
        config = HRPlatformConfig(
            base_url="https://api.example.com",
            api_version="v1",
            auth=ApiKeyAuth(api_key="hrp_test_abc"),
        )
        assert config.get_api_url() == "https://api.example.com/api/v1"

    def test_get_api_url_v2(self) -> None:
        """Test get_api_url method with different version."""
        config = HRPlatformConfig(
            base_url="https://api.example.com",
            api_version="v2",
            auth=ApiKeyAuth(api_key="hrp_test_abc"),
        )
        assert config.get_api_url() == "https://api.example.com/api/v2"

    def test_get_api_url_strips_trailing_slash(self) -> None:
        """Test get_api_url strips trailing slash from base_url."""
        config = HRPlatformConfig(
            base_url="https://api.example.com/",
            api_version="v1",
            auth=ApiKeyAuth(api_key="hrp_test_abc"),
        )
        # The base_url itself is stored as-is, but get_api_url() strips it
        assert config.get_api_url() == "https://api.example.com/api/v1"

    def test_auth_type_api_key(self) -> None:
        """Test auth type with API key."""
        config = HRPlatformConfig(
            base_url="https://api.example.com",
            auth=ApiKeyAuth(api_key="hrp_test_abc"),
        )
        assert config.auth.type == "api_key"

    def test_auth_type_cookie(self) -> None:
        """Test auth type with cookie."""
        config = HRPlatformConfig(
            base_url="https://api.example.com",
            auth=CookieAuth(),
        )
        assert config.auth.type == "cookie"

    def test_default_retry_config(self) -> None:
        """Test default retry config is created."""
        config = HRPlatformConfig()
        assert config.retry.max_retries == 3
        assert config.retry.initial_delay == 1.0

    def test_headers_default_to_empty_dict(self) -> None:
        """Test headers default to empty dict."""
        config = HRPlatformConfig()
        assert config.headers == {}
        # Should be a new dict each time (not shared mutable default)
        config.headers["test"] = "value"
        new_config = HRPlatformConfig()
        assert new_config.headers == {}


class TestConfigDefaults:
    """Tests for module-level default configs."""

    def test_default_retry_config_exists(self) -> None:
        """Test DEFAULT_RETRY_CONFIG is available."""
        from hr_platform.core.config import DEFAULT_RETRY_CONFIG
        assert isinstance(DEFAULT_RETRY_CONFIG, RetryConfig)
        assert DEFAULT_RETRY_CONFIG.max_retries == 3

    def test_default_config_exists(self) -> None:
        """Test DEFAULT_CONFIG is available."""
        from hr_platform.core.config import DEFAULT_CONFIG
        assert isinstance(DEFAULT_CONFIG, HRPlatformConfig)
        assert DEFAULT_CONFIG.base_url == "http://localhost:4000"
