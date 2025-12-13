"""Admin resource.

API resource for administrative operations.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from hr_platform.models.admin import (
    AdminStatus,
    ApiKey,
    ApiKeysListResponse,
    ApiKeyScopesResponse,
    AuditLogsQueryParams,
    AuditLogsResponse,
    BlockUserResponse,
    ClearRateLimitResponse,
    CreateApiKeyRequest,
    CreateApiKeyResponse,
    InvalidateAllSessionsResponse,
    LogoutUserResponse,
    ResetPasswordResponse,
    RevokeApiKeyRequest,
    RevokeApiKeyResponse,
    RotateApiKeyResponse,
    SecurityDashboard,
    SessionsResponse,
    UnlockAccountResponse,
)
from hr_platform.resources.base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from hr_platform.core.async_http import AsyncHttpClient
    from hr_platform.core.http import HttpClient


class AdminResource(BaseResource):
    """Synchronous admin API resource.

    Provides methods for administrative operations. All methods require
    system_admin role.

    Example:
        >>> status = client.admin.get_status()
        >>> dashboard = client.admin.get_security_dashboard()
        >>> sessions = client.admin.list_sessions()
    """

    def __init__(self, client: "HttpClient") -> None:
        """Initialize admin resource.

        Args:
            client: HTTP client instance.
        """
        super().__init__(client)

    # System Status

    def get_status(self) -> AdminStatus:
        """Get system health and security status.

        Returns:
            System status with security feature indicators.

        Example:
            >>> status = client.admin.get_status()
            >>> print(f"Status: {status.status}")
            >>> print(f"Rate limiting: {status.security.rate_limiting}")
        """
        data = self._get("/admin/status")
        return AdminStatus.model_validate(data)

    def get_security_dashboard(self) -> SecurityDashboard:
        """Get security metrics for the last 24 hours.

        Returns:
            Security dashboard with failed logins, rate limits, etc.

        Example:
            >>> dashboard = client.admin.get_security_dashboard()
            >>> print(f"Failed logins (24h): {dashboard.failed_logins_24h}")
            >>> print(f"Locked accounts: {dashboard.locked_accounts}")
        """
        data = self._get("/admin/security/dashboard")
        return SecurityDashboard.model_validate(data)

    # User Management

    def block_user(self, user_id: str) -> BlockUserResponse:
        """Block a user account.

        Prevents login and terminates active sessions.

        Args:
            user_id: UUID of the user to block.

        Returns:
            Response confirming the block.

        Example:
            >>> response = client.admin.block_user("user-uuid")
            >>> print(response.message)
        """
        data = self._post(f"/admin/users/{user_id}/block")
        return BlockUserResponse.model_validate(data)

    def unblock_user(self, user_id: str) -> BlockUserResponse:
        """Unblock a previously blocked user account.

        Args:
            user_id: UUID of the user to unblock.

        Returns:
            Response confirming the unblock.

        Example:
            >>> response = client.admin.unblock_user("user-uuid")
            >>> print(response.message)
        """
        data = self._post(f"/admin/users/{user_id}/unblock")
        return BlockUserResponse.model_validate(data)

    def reset_password(self, user_id: str) -> ResetPasswordResponse:
        """Reset a user's password.

        Generates a temporary password. User will be required to
        change it on next login.

        Args:
            user_id: UUID of the user.

        Returns:
            Response with temporary password.

        Example:
            >>> response = client.admin.reset_password("user-uuid")
            >>> print(f"Temp password: {response.temp_password}")
        """
        data = self._post(f"/admin/users/{user_id}/reset-password")
        return ResetPasswordResponse.model_validate(data)

    def clear_rate_limit(self, email: str) -> ClearRateLimitResponse:
        """Clear rate limiting counters for a user.

        Args:
            email: Email address of the user.

        Returns:
            Response confirming the clear.

        Example:
            >>> response = client.admin.clear_rate_limit("user@vollers.de")
            >>> print(response.message)
        """
        data = self._post(f"/admin/users/{email}/reset-rate-limit")
        return ClearRateLimitResponse.model_validate(data)

    def unlock_account(self, email: str) -> UnlockAccountResponse:
        """Unlock a locked account.

        Unlocks accounts locked due to excessive failed login attempts.

        Args:
            email: Email address of the user.

        Returns:
            Response confirming the unlock.

        Example:
            >>> response = client.admin.unlock_account("user@vollers.de")
            >>> print(response.message)
        """
        data = self._post(f"/admin/unlock/{email}")
        return UnlockAccountResponse.model_validate(data)

    # Session Management

    def list_sessions(self) -> SessionsResponse:
        """List all active sessions.

        Returns:
            Response containing active sessions list.

        Example:
            >>> response = client.admin.list_sessions()
            >>> for session in response.sessions:
            ...     print(f"{session.user_email}: {session.ip_address}")
        """
        data = self._get("/admin/sessions")
        return SessionsResponse.model_validate(data)

    def force_logout(self, user_id: str) -> LogoutUserResponse:
        """Force logout a user by terminating all their sessions.

        Args:
            user_id: UUID of the user to logout.

        Returns:
            Response with number of sessions terminated.

        Example:
            >>> response = client.admin.force_logout("user-uuid")
            >>> print(f"Terminated {response.sessions_terminated} sessions")
        """
        data = self._post(f"/admin/sessions/{user_id}/logout")
        return LogoutUserResponse.model_validate(data)

    def invalidate_all_sessions(self) -> InvalidateAllSessionsResponse:
        """Invalidate all sessions system-wide.

        Emergency endpoint. Does not invalidate the admin's own session.

        Returns:
            Response with total sessions terminated.

        Example:
            >>> response = client.admin.invalidate_all_sessions()
            >>> print(f"Terminated {response.sessions_terminated} sessions")
        """
        data = self._post("/admin/sessions/invalidate-all")
        return InvalidateAllSessionsResponse.model_validate(data)

    # Audit Logs

    def get_audit_logs(
        self,
        *,
        page: int = 1,
        limit: int = 25,
        category: str | None = None,
        severity: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        user_email: str | None = None,
    ) -> AuditLogsResponse:
        """Query audit logs with pagination and filters.

        Args:
            page: Page number (default: 1).
            limit: Results per page (default: 25, max: 100).
            category: Filter by category (auth, data, workflow, admin).
            severity: Filter by severity (info, warning, error, critical).
            start_date: Filter from date (ISO 8601).
            end_date: Filter to date (ISO 8601).
            user_email: Filter by user email.

        Returns:
            Paginated audit logs response.

        Example:
            >>> logs = client.admin.get_audit_logs(
            ...     category="auth",
            ...     severity="warning",
            ...     limit=50
            ... )
            >>> for log in logs.logs:
            ...     print(f"{log.timestamp}: {log.action}")
        """
        params = AuditLogsQueryParams(
            page=page,
            limit=limit,
            category=category,
            severity=severity,
            start_date=start_date,
            end_date=end_date,
            user_email=user_email,
        )
        data = self._get("/admin/audit-logs", params=params.to_params())
        return AuditLogsResponse.model_validate(data)

    # API Key Management

    def list_api_keys(self) -> ApiKeysListResponse:
        """List all API keys (no secrets exposed).

        Returns:
            Response containing API keys list.

        Example:
            >>> response = client.admin.list_api_keys()
            >>> for key in response.keys:
            ...     print(f"{key.name}: {key.key_prefix}...")
        """
        data = self._get("/admin/api-keys")
        return ApiKeysListResponse.model_validate(data)

    def get_api_key(self, key_id: str) -> ApiKey:
        """Get a single API key's details.

        Args:
            key_id: UUID of the API key.

        Returns:
            API key metadata.

        Raises:
            NotFoundError: If key doesn't exist.

        Example:
            >>> key = client.admin.get_api_key("key-uuid")
            >>> print(f"Last used: {key.last_used_at}")
        """
        data = self._get(f"/admin/api-keys/{key_id}")
        return ApiKey.model_validate(data)

    def get_api_key_scopes(self) -> ApiKeyScopesResponse:
        """Get available API key scopes.

        Returns:
            Response containing available scopes.

        Example:
            >>> response = client.admin.get_api_key_scopes()
            >>> for scope in response.scopes:
            ...     print(f"{scope.scope}: {scope.description}")
        """
        data = self._get("/admin/api-keys/scopes")
        return ApiKeyScopesResponse.model_validate(data)

    def create_api_key(self, request: CreateApiKeyRequest) -> CreateApiKeyResponse:
        """Create a new API key.

        IMPORTANT: The plain text key is returned ONLY at creation time.
        Store it securely immediately.

        Args:
            request: API key creation request.

        Returns:
            Response with key metadata and plain text key.

        Example:
            >>> from hr_platform.models import CreateApiKeyRequest
            >>> response = client.admin.create_api_key(CreateApiKeyRequest(
            ...     name="D365 Integration",
            ...     user_id="user-uuid",
            ...     scopes=["records:read", "analytics:read"],
            ...     expires_in_days=365,
            ... ))
            >>> print(f"Key: {response.plain_text_key}")
            >>> print(response.warning)
        """
        data = self._post(
            "/admin/api-keys",
            data=request.model_dump(by_alias=True, exclude_none=True),
        )
        return CreateApiKeyResponse.model_validate(data)

    def revoke_api_key(
        self, key_id: str, reason: str | None = None
    ) -> RevokeApiKeyResponse:
        """Revoke an API key.

        Args:
            key_id: UUID of the API key.
            reason: Optional revocation reason.

        Returns:
            Response confirming revocation.

        Example:
            >>> response = client.admin.revoke_api_key(
            ...     "key-uuid",
            ...     reason="Key compromised"
            ... )
            >>> print(f"Revoked at: {response.revoked_at}")
        """
        request = RevokeApiKeyRequest(reason=reason) if reason else None
        data = self._delete(
            f"/admin/api-keys/{key_id}",
            params=request.model_dump(by_alias=True, exclude_none=True) if request else None,
        )
        return RevokeApiKeyResponse.model_validate(data)

    def rotate_api_key(self, key_id: str) -> RotateApiKeyResponse:
        """Rotate an API key (create new, revoke old).

        IMPORTANT: The new plain text key is returned ONLY at rotation time.
        Update your systems immediately.

        Args:
            key_id: UUID of the API key to rotate.

        Returns:
            Response with new key metadata and plain text key.

        Example:
            >>> response = client.admin.rotate_api_key("key-uuid")
            >>> print(f"Old key ID: {response.old_key_id}")
            >>> print(f"New key: {response.plain_text_key}")
        """
        data = self._post(f"/admin/api-keys/{key_id}/rotate")
        return RotateApiKeyResponse.model_validate(data)


class AsyncAdminResource(AsyncBaseResource):
    """Asynchronous admin API resource.

    Provides async methods for administrative operations. All methods
    require system_admin role.

    Example:
        >>> status = await client.admin.get_status()
        >>> dashboard = await client.admin.get_security_dashboard()
    """

    def __init__(self, client: "AsyncHttpClient") -> None:
        """Initialize async admin resource.

        Args:
            client: Async HTTP client instance.
        """
        super().__init__(client)

    # System Status

    async def get_status(self) -> AdminStatus:
        """Get system health and security status."""
        data = await self._get("/admin/status")
        return AdminStatus.model_validate(data)

    async def get_security_dashboard(self) -> SecurityDashboard:
        """Get security metrics for the last 24 hours."""
        data = await self._get("/admin/security/dashboard")
        return SecurityDashboard.model_validate(data)

    # User Management

    async def block_user(self, user_id: str) -> BlockUserResponse:
        """Block a user account."""
        data = await self._post(f"/admin/users/{user_id}/block")
        return BlockUserResponse.model_validate(data)

    async def unblock_user(self, user_id: str) -> BlockUserResponse:
        """Unblock a previously blocked user account."""
        data = await self._post(f"/admin/users/{user_id}/unblock")
        return BlockUserResponse.model_validate(data)

    async def reset_password(self, user_id: str) -> ResetPasswordResponse:
        """Reset a user's password."""
        data = await self._post(f"/admin/users/{user_id}/reset-password")
        return ResetPasswordResponse.model_validate(data)

    async def clear_rate_limit(self, email: str) -> ClearRateLimitResponse:
        """Clear rate limiting counters for a user."""
        data = await self._post(f"/admin/users/{email}/reset-rate-limit")
        return ClearRateLimitResponse.model_validate(data)

    async def unlock_account(self, email: str) -> UnlockAccountResponse:
        """Unlock a locked account."""
        data = await self._post(f"/admin/unlock/{email}")
        return UnlockAccountResponse.model_validate(data)

    # Session Management

    async def list_sessions(self) -> SessionsResponse:
        """List all active sessions."""
        data = await self._get("/admin/sessions")
        return SessionsResponse.model_validate(data)

    async def force_logout(self, user_id: str) -> LogoutUserResponse:
        """Force logout a user by terminating all their sessions."""
        data = await self._post(f"/admin/sessions/{user_id}/logout")
        return LogoutUserResponse.model_validate(data)

    async def invalidate_all_sessions(self) -> InvalidateAllSessionsResponse:
        """Invalidate all sessions system-wide."""
        data = await self._post("/admin/sessions/invalidate-all")
        return InvalidateAllSessionsResponse.model_validate(data)

    # Audit Logs

    async def get_audit_logs(
        self,
        *,
        page: int = 1,
        limit: int = 25,
        category: str | None = None,
        severity: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        user_email: str | None = None,
    ) -> AuditLogsResponse:
        """Query audit logs with pagination and filters."""
        params = AuditLogsQueryParams(
            page=page,
            limit=limit,
            category=category,
            severity=severity,
            start_date=start_date,
            end_date=end_date,
            user_email=user_email,
        )
        data = await self._get("/admin/audit-logs", params=params.to_params())
        return AuditLogsResponse.model_validate(data)

    # API Key Management

    async def list_api_keys(self) -> ApiKeysListResponse:
        """List all API keys (no secrets exposed)."""
        data = await self._get("/admin/api-keys")
        return ApiKeysListResponse.model_validate(data)

    async def get_api_key(self, key_id: str) -> ApiKey:
        """Get a single API key's details."""
        data = await self._get(f"/admin/api-keys/{key_id}")
        return ApiKey.model_validate(data)

    async def get_api_key_scopes(self) -> ApiKeyScopesResponse:
        """Get available API key scopes."""
        data = await self._get("/admin/api-keys/scopes")
        return ApiKeyScopesResponse.model_validate(data)

    async def create_api_key(
        self, request: CreateApiKeyRequest
    ) -> CreateApiKeyResponse:
        """Create a new API key."""
        data = await self._post(
            "/admin/api-keys",
            data=request.model_dump(by_alias=True, exclude_none=True),
        )
        return CreateApiKeyResponse.model_validate(data)

    async def revoke_api_key(
        self, key_id: str, reason: str | None = None
    ) -> RevokeApiKeyResponse:
        """Revoke an API key."""
        request = RevokeApiKeyRequest(reason=reason) if reason else None
        data = await self._delete(
            f"/admin/api-keys/{key_id}",
            params=request.model_dump(by_alias=True, exclude_none=True) if request else None,
        )
        return RevokeApiKeyResponse.model_validate(data)

    async def rotate_api_key(self, key_id: str) -> RotateApiKeyResponse:
        """Rotate an API key (create new, revoke old)."""
        data = await self._post(f"/admin/api-keys/{key_id}/rotate")
        return RotateApiKeyResponse.model_validate(data)
