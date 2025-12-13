"""Admin models.

Pydantic models for administrative functions.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    pass


class SecurityStatus(BaseModel):
    """Security features status."""

    model_config = ConfigDict(populate_by_name=True)

    rate_limiting: str = Field(alias="rateLimiting", description="Rate limiting status")
    session_timeout: str = Field(
        alias="sessionTimeout", description="Session timeout status"
    )
    audit_logging: str = Field(alias="auditLogging", description="Audit logging status")


class AuditStatus(BaseModel):
    """Audit log statistics."""

    model_config = ConfigDict(populate_by_name=True)

    total_records: int = Field(alias="totalRecords", description="Total audit records")
    oldest_record: Optional[str] = Field(
        alias="oldestRecord", default=None, description="Oldest record timestamp"
    )
    newest_record: Optional[str] = Field(
        alias="newestRecord", default=None, description="Newest record timestamp"
    )


class AdminStatus(BaseModel):
    """System status response."""

    model_config = ConfigDict(populate_by_name=True)

    status: str = Field(description="System status (healthy/unhealthy)")
    timestamp: str = Field(description="Current server time")
    security: SecurityStatus = Field(description="Security feature status")
    audit: Optional[AuditStatus] = Field(default=None, description="Audit log stats")


class SecurityDashboard(BaseModel):
    """Security dashboard metrics."""

    model_config = ConfigDict(populate_by_name=True)

    failed_logins_24h: int = Field(
        alias="failedLogins24h", description="Failed logins in last 24h"
    )
    rate_limit_events_24h: int = Field(
        alias="rateLimitEvents24h", description="Rate limit events in last 24h"
    )
    locked_accounts: int = Field(
        alias="lockedAccounts", description="Currently locked accounts"
    )
    active_sessions: int = Field(
        alias="activeSessions", description="Active sessions count"
    )
    timestamp: str = Field(description="Dashboard data timestamp")


class ActiveSession(BaseModel):
    """Active session info."""

    model_config = ConfigDict(populate_by_name=True)

    session_id: str = Field(alias="sessionId", description="Session ID")
    user_id: str = Field(alias="userId", description="User ID")
    user_email: str = Field(alias="userEmail", description="User email")
    user_name: str = Field(alias="userName", description="User name")
    ip_address: str | None = Field(
        alias="ipAddress", default=None, description="Client IP"
    )
    user_agent: str | None = Field(
        alias="userAgent", default=None, description="Client user agent"
    )
    created_at: str = Field(alias="createdAt", description="Session start time")
    last_activity_at: str | None = Field(
        alias="lastActivityAt", default=None, description="Last activity time"
    )


class SessionsResponse(BaseModel):
    """Response containing active sessions."""

    model_config = ConfigDict(populate_by_name=True)

    sessions: list[ActiveSession] = Field(description="Active sessions")


class AuditLog(BaseModel):
    """Single audit log entry."""

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(description="Log entry ID")
    timestamp: str = Field(description="Event timestamp")
    user_id: str | None = Field(alias="userId", default=None, description="User ID")
    user_email: str | None = Field(
        alias="userEmail", default=None, description="User email"
    )
    user_role: str | None = Field(alias="userRole", default=None, description="Role")
    ip_address: str | None = Field(
        alias="ipAddress", default=None, description="Client IP"
    )
    user_agent: str | None = Field(
        alias="userAgent", default=None, description="User agent"
    )
    event_type: str = Field(alias="eventType", description="Event type identifier")
    event_category: str = Field(
        alias="eventCategory", description="Category (auth, data, workflow, admin)"
    )
    severity: str = Field(description="Severity level")
    action: str = Field(description="Action description")
    resource_type: str | None = Field(
        alias="resourceType", default=None, description="Resource type"
    )
    resource_id: str | None = Field(
        alias="resourceId", default=None, description="Resource ID"
    )
    entity: str | None = Field(default=None, description="Entity code")
    details: dict | None = Field(default=None, description="Additional details")


class AuditLogPagination(BaseModel):
    """Pagination info for audit logs."""

    model_config = ConfigDict(populate_by_name=True)

    page: int = Field(description="Current page number")
    limit: int = Field(description="Results per page")
    total: int = Field(description="Total results")
    total_pages: int = Field(alias="totalPages", description="Total pages")


class AuditLogsResponse(BaseModel):
    """Paginated audit logs response."""

    model_config = ConfigDict(populate_by_name=True)

    logs: list[AuditLog] = Field(description="Audit log entries")
    pagination: AuditLogPagination = Field(description="Pagination info")


class AuditLogsQueryParams(BaseModel):
    """Query parameters for audit logs endpoint."""

    model_config = ConfigDict(populate_by_name=True)

    page: int = Field(default=1, ge=1, description="Page number")
    limit: int = Field(default=25, ge=1, le=100, description="Results per page")
    category: str | None = Field(
        default=None, description="Filter by category (auth, data, workflow, admin)"
    )
    severity: str | None = Field(
        default=None, description="Filter by severity (info, warning, error, critical)"
    )
    start_date: str | None = Field(
        alias="startDate", default=None, description="Filter from date (ISO 8601)"
    )
    end_date: str | None = Field(
        alias="endDate", default=None, description="Filter to date (ISO 8601)"
    )
    user_email: str | None = Field(
        alias="userEmail", default=None, description="Filter by user email"
    )

    def to_params(self) -> dict[str, str]:
        """Convert to query parameter dict."""
        params: dict[str, str] = {
            "page": str(self.page),
            "limit": str(self.limit),
        }
        if self.category:
            params["category"] = self.category
        if self.severity:
            params["severity"] = self.severity
        if self.start_date:
            params["startDate"] = self.start_date
        if self.end_date:
            params["endDate"] = self.end_date
        if self.user_email:
            params["userEmail"] = self.user_email
        return params


class BlockUserResponse(BaseModel):
    """Response from blocking/unblocking a user."""

    model_config = ConfigDict(populate_by_name=True)

    success: bool = Field(description="Success flag")
    user_id: str = Field(alias="userId", description="User ID")
    message: str = Field(description="Result message")


class ResetPasswordResponse(BaseModel):
    """Response from resetting a user's password."""

    model_config = ConfigDict(populate_by_name=True)

    success: bool = Field(description="Success flag")
    temp_password: str = Field(alias="tempPassword", description="Temporary password")
    user_id: str = Field(alias="userId", description="User ID")
    message: str = Field(description="Result message")


class LogoutUserResponse(BaseModel):
    """Response from forcing user logout."""

    model_config = ConfigDict(populate_by_name=True)

    success: bool = Field(description="Success flag")
    user_id: str = Field(alias="userId", description="User ID")
    sessions_terminated: int = Field(
        alias="sessionsTerminated", description="Number of sessions terminated"
    )
    message: str = Field(description="Result message")


class InvalidateAllSessionsResponse(BaseModel):
    """Response from invalidating all sessions."""

    model_config = ConfigDict(populate_by_name=True)

    success: bool = Field(description="Success flag")
    sessions_terminated: int = Field(
        alias="sessionsTerminated", description="Number of sessions terminated"
    )
    message: str = Field(description="Result message")


class ClearRateLimitResponse(BaseModel):
    """Response from clearing rate limits."""

    model_config = ConfigDict(populate_by_name=True)

    success: bool = Field(description="Success flag")
    email: str = Field(description="User email")
    message: str = Field(description="Result message")


class UnlockAccountResponse(BaseModel):
    """Response from unlocking an account."""

    model_config = ConfigDict(populate_by_name=True)

    success: bool = Field(description="Success flag")
    email: str = Field(description="User email")
    message: str = Field(description="Result message")


# API Key Management Models


class ApiKeyScope(BaseModel):
    """API key scope definition."""

    model_config = ConfigDict(populate_by_name=True)

    scope: str = Field(description="Scope identifier")
    name: str = Field(description="Human-readable name")
    description: str = Field(description="Scope description")


class ApiKey(BaseModel):
    """API key metadata (without secret)."""

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(description="Key ID")
    name: str = Field(description="Key name")
    key_prefix: str = Field(alias="keyPrefix", description="Key prefix (hrp_xxx_...)")
    user_id: str = Field(alias="userId", description="Associated user ID")
    user_email: str = Field(alias="userEmail", description="Associated user email")
    entity: str | None = Field(default=None, description="Entity scope")
    scopes: list[str] = Field(description="Granted scopes")
    rate_limit_override: int | None = Field(
        alias="rateLimitOverride", default=None, description="Custom rate limit"
    )
    expires_at: str | None = Field(
        alias="expiresAt", default=None, description="Expiration time"
    )
    last_used_at: str | None = Field(
        alias="lastUsedAt", default=None, description="Last usage time"
    )
    request_count: int = Field(alias="requestCount", description="Total requests made")
    created_at: str = Field(alias="createdAt", description="Creation time")
    revoked_at: str | None = Field(
        alias="revokedAt", default=None, description="Revocation time"
    )


class ApiKeysListResponse(BaseModel):
    """Response containing API keys list."""

    model_config = ConfigDict(populate_by_name=True)

    keys: list[ApiKey] = Field(description="API keys")
    total: int = Field(description="Total count")


class ApiKeyScopesResponse(BaseModel):
    """Response containing available scopes."""

    model_config = ConfigDict(populate_by_name=True)

    scopes: list[ApiKeyScope] = Field(description="Available scopes")


class CreateApiKeyRequest(BaseModel):
    """Request to create an API key."""

    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(min_length=1, max_length=100, description="Key name")
    user_id: str = Field(alias="userId", description="User ID to associate")
    entity: str | None = Field(default=None, description="Entity scope")
    scopes: list[str] = Field(min_length=1, description="Scopes to grant")
    rate_limit_override: int | None = Field(
        alias="rateLimitOverride", default=None, ge=1, le=10000
    )
    expires_in_days: int | None = Field(
        alias="expiresInDays", default=None, ge=1, le=365
    )


class CreateApiKeyResponse(BaseModel):
    """Response from creating an API key."""

    model_config = ConfigDict(populate_by_name=True)

    message: str = Field(description="Success message")
    key: ApiKey = Field(description="Key metadata")
    plain_text_key: str = Field(alias="plainTextKey", description="Plain text key")
    warning: str = Field(description="Warning about storing key")


class RevokeApiKeyRequest(BaseModel):
    """Request to revoke an API key."""

    model_config = ConfigDict(populate_by_name=True)

    reason: str | None = Field(default=None, description="Revocation reason")


class RevokeApiKeyResponse(BaseModel):
    """Response from revoking an API key."""

    model_config = ConfigDict(populate_by_name=True)

    success: bool = Field(description="Success flag")
    message: str = Field(description="Result message")
    key_id: str = Field(alias="keyId", description="Key ID")
    revoked_at: str = Field(alias="revokedAt", description="Revocation time")


class RotateApiKeyResponse(BaseModel):
    """Response from rotating an API key."""

    model_config = ConfigDict(populate_by_name=True)

    message: str = Field(description="Success message")
    old_key_id: str = Field(alias="oldKeyId", description="Old key ID")
    new_key: ApiKey = Field(alias="newKey", description="New key metadata")
    plain_text_key: str = Field(alias="plainTextKey", description="New plain text key")
    warning: str = Field(description="Warning about storing key")
