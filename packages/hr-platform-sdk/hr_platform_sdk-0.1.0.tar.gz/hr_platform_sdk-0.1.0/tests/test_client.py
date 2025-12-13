"""Tests for HR Platform SDK clients."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from hr_platform import AsyncHRPlatformClient, HRPlatformClient
from hr_platform.core.config import ApiKeyAuth, CookieAuth, HRPlatformConfig, RetryConfig
from hr_platform.resources.admin import AdminResource, AsyncAdminResource
from hr_platform.resources.analytics import AnalyticsResource, AsyncAnalyticsResource
from hr_platform.resources.compliance import AsyncComplianceResource, ComplianceResource
from hr_platform.resources.records import AsyncRecordsResource, RecordsResource
from hr_platform.resources.users import AsyncUsersResource, UsersResource
from hr_platform.resources.webhooks import AsyncWebhooksResource, WebhooksResource


class TestHRPlatformClient:
    """Tests for synchronous HRPlatformClient."""

    def test_with_api_key_default_config(self) -> None:
        """Test creating client with API key and default config."""
        client = HRPlatformClient.with_api_key("hrp_test_abc123")
        try:
            assert client._config.base_url == "http://localhost:4000"
            assert client._config.api_version == "v1"
            assert client._config.timeout == 30.0
            assert isinstance(client._config.auth, ApiKeyAuth)
            assert client._config.auth.api_key == "hrp_test_abc123"
        finally:
            client.close()

    def test_with_api_key_custom_config(self) -> None:
        """Test creating client with API key and custom config."""
        client = HRPlatformClient.with_api_key(
            "hrp_live_xyz789",
            base_url="https://api.example.com",
            api_version="v2",
            timeout=60.0,
            headers={"X-Custom": "header"},
        )
        try:
            assert client._config.base_url == "https://api.example.com"
            assert client._config.api_version == "v2"
            assert client._config.timeout == 60.0
            assert client._config.headers == {"X-Custom": "header"}
        finally:
            client.close()

    def test_with_api_key_custom_retry(self) -> None:
        """Test creating client with custom retry config."""
        retry = RetryConfig(max_retries=5, initial_delay=0.5)
        client = HRPlatformClient.with_api_key(
            "hrp_test_abc123",
            retry=retry,
        )
        try:
            assert client._config.retry.max_retries == 5
            assert client._config.retry.initial_delay == 0.5
        finally:
            client.close()

    def test_with_cookie_auth(self) -> None:
        """Test creating client with cookie auth."""
        client = HRPlatformClient.with_cookie_auth(
            base_url="https://api.example.com",
        )
        try:
            assert isinstance(client._config.auth, CookieAuth)
            assert client._config.auth.type == "cookie"
        finally:
            client.close()

    def test_from_config(self) -> None:
        """Test creating client from existing config."""
        config = HRPlatformConfig(
            base_url="https://api.example.com",
            auth=ApiKeyAuth(api_key="hrp_test_abc"),
        )
        client = HRPlatformClient.from_config(config)
        try:
            assert client._config is config
        finally:
            client.close()

    def test_has_all_resources(self) -> None:
        """Test client has all resource attributes."""
        client = HRPlatformClient.with_api_key("hrp_test_abc123")
        try:
            assert isinstance(client.records, RecordsResource)
            assert isinstance(client.analytics, AnalyticsResource)
            assert isinstance(client.users, UsersResource)
            assert isinstance(client.admin, AdminResource)
            assert isinstance(client.compliance, ComplianceResource)
            assert isinstance(client.webhooks, WebhooksResource)
        finally:
            client.close()

    def test_config_property(self) -> None:
        """Test config property returns configuration."""
        client = HRPlatformClient.with_api_key("hrp_test_abc123")
        try:
            assert isinstance(client.config, HRPlatformConfig)
            assert client.config.base_url == "http://localhost:4000"
        finally:
            client.close()

    def test_context_manager(self) -> None:
        """Test client can be used as context manager."""
        with HRPlatformClient.with_api_key("hrp_test_abc123") as client:
            assert isinstance(client, HRPlatformClient)
            # Client should be usable inside context
            assert client._config is not None

    def test_repr(self) -> None:
        """Test client string representation."""
        client = HRPlatformClient.with_api_key("hrp_test_abc123")
        try:
            repr_str = repr(client)
            assert "HRPlatformClient" in repr_str
            assert "localhost:4000" in repr_str
            assert "api_key" in repr_str
        finally:
            client.close()


class TestAsyncHRPlatformClient:
    """Tests for asynchronous AsyncHRPlatformClient."""

    def test_with_api_key_default_config(self) -> None:
        """Test creating async client with API key and default config."""
        client = AsyncHRPlatformClient.with_api_key("hrp_test_abc123")
        assert client._config.base_url == "http://localhost:4000"
        assert client._config.api_version == "v1"
        assert isinstance(client._config.auth, ApiKeyAuth)

    def test_with_api_key_custom_config(self) -> None:
        """Test creating async client with API key and custom config."""
        client = AsyncHRPlatformClient.with_api_key(
            "hrp_live_xyz789",
            base_url="https://api.example.com",
            api_version="v2",
            timeout=60.0,
        )
        assert client._config.base_url == "https://api.example.com"
        assert client._config.api_version == "v2"
        assert client._config.timeout == 60.0

    def test_with_cookie_auth(self) -> None:
        """Test creating async client with cookie auth."""
        client = AsyncHRPlatformClient.with_cookie_auth(
            base_url="https://api.example.com",
        )
        assert isinstance(client._config.auth, CookieAuth)

    def test_from_config(self) -> None:
        """Test creating async client from existing config."""
        config = HRPlatformConfig(
            base_url="https://api.example.com",
            auth=ApiKeyAuth(api_key="hrp_test_abc"),
        )
        client = AsyncHRPlatformClient.from_config(config)
        assert client._config is config

    def test_has_all_async_resources(self) -> None:
        """Test async client has all async resource attributes."""
        client = AsyncHRPlatformClient.with_api_key("hrp_test_abc123")
        assert isinstance(client.records, AsyncRecordsResource)
        assert isinstance(client.analytics, AsyncAnalyticsResource)
        assert isinstance(client.users, AsyncUsersResource)
        assert isinstance(client.admin, AsyncAdminResource)
        assert isinstance(client.compliance, AsyncComplianceResource)
        assert isinstance(client.webhooks, AsyncWebhooksResource)

    def test_config_property(self) -> None:
        """Test config property returns configuration."""
        client = AsyncHRPlatformClient.with_api_key("hrp_test_abc123")
        assert isinstance(client.config, HRPlatformConfig)

    @pytest.mark.asyncio
    async def test_async_context_manager(self) -> None:
        """Test async client can be used as async context manager."""
        async with AsyncHRPlatformClient.with_api_key("hrp_test_abc123") as client:
            assert isinstance(client, AsyncHRPlatformClient)

    def test_repr(self) -> None:
        """Test async client string representation."""
        client = AsyncHRPlatformClient.with_api_key("hrp_test_abc123")
        repr_str = repr(client)
        assert "AsyncHRPlatformClient" in repr_str
        assert "api_key" in repr_str


class TestClientAuthenticationMethods:
    """Tests for client authentication method variations."""

    def test_api_key_auth_type(self) -> None:
        """Test API key authentication sets correct type."""
        client = HRPlatformClient.with_api_key("hrp_test_abc")
        try:
            assert client._config.auth.type == "api_key"
        finally:
            client.close()

    def test_cookie_auth_type(self) -> None:
        """Test cookie authentication sets correct type."""
        client = HRPlatformClient.with_cookie_auth()
        try:
            assert client._config.auth.type == "cookie"
        finally:
            client.close()

    def test_api_key_stored_correctly(self) -> None:
        """Test API key is stored in auth config."""
        client = HRPlatformClient.with_api_key("hrp_live_secret_key")
        try:
            assert isinstance(client._config.auth, ApiKeyAuth)
            assert client._config.auth.api_key == "hrp_live_secret_key"
        finally:
            client.close()


class TestClientConfiguration:
    """Tests for client configuration handling."""

    def test_default_retry_config(self) -> None:
        """Test default retry configuration is applied."""
        client = HRPlatformClient.with_api_key("hrp_test_abc")
        try:
            assert client._config.retry.max_retries == 3
            assert client._config.retry.initial_delay == 1.0
        finally:
            client.close()

    def test_custom_headers_applied(self) -> None:
        """Test custom headers are stored in config."""
        headers = {"X-Request-Id": "abc123", "X-Tenant": "test"}
        client = HRPlatformClient.with_api_key(
            "hrp_test_abc",
            headers=headers,
        )
        try:
            assert client._config.headers == headers
        finally:
            client.close()

    def test_base_url_variants(self) -> None:
        """Test various base URL formats."""
        # With trailing slash - stored as-is, get_api_url() handles it
        client1 = HRPlatformClient.with_api_key(
            "hrp_test_abc",
            base_url="https://api.example.com/",
        )
        try:
            # base_url stored as-is
            assert client1._config.base_url == "https://api.example.com/"
            # get_api_url() strips trailing slash when building full URL
            assert client1._config.get_api_url() == "https://api.example.com/api/v1"
        finally:
            client1.close()

        # Without trailing slash
        client2 = HRPlatformClient.with_api_key(
            "hrp_test_abc",
            base_url="https://api.example.com",
        )
        try:
            assert client2._config.base_url == "https://api.example.com"
            assert client2._config.get_api_url() == "https://api.example.com/api/v1"
        finally:
            client2.close()
