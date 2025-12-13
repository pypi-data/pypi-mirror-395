"""User models.

Pydantic models for user management.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from hr_platform.models.enums import Entity, UserRole


class User(BaseModel):
    """User account information."""

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(description="User ID (UUID)")
    email: str = Field(description="Email address")
    name: str = Field(description="Display name")
    role: UserRole = Field(description="User role")
    entity: Entity | None = Field(
        default=None, description="Assigned entity (for local_partner)"
    )
    created_at: str = Field(description="Account creation timestamp")
    updated_at: str = Field(description="Last update timestamp")


class UserProfile(BaseModel):
    """Current user profile (from session)."""

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(description="User ID")
    email: str = Field(description="Email address")
    name: str = Field(description="Display name")
    role: UserRole = Field(description="User role")
    entity: Entity | None = Field(default=None, description="Assigned entity")


class Session(BaseModel):
    """Active session information."""

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(description="Session ID")
    expires_at: str = Field(alias="expiresAt", description="Session expiration time")


class SessionInfo(BaseModel):
    """Full session response from get-session endpoint."""

    model_config = ConfigDict(populate_by_name=True)

    user: UserProfile = Field(description="User profile")
    session: Session = Field(description="Session details")


class CreateUserRequest(BaseModel):
    """Request body for creating a new user."""

    model_config = ConfigDict(populate_by_name=True)

    email: str = Field(description="Email address")
    name: str = Field(description="Display name")
    password: str = Field(min_length=12, description="Password (12+ chars)")
    role: UserRole = Field(description="User role")
    entity: Entity | None = Field(
        default=None, description="Assigned entity (required for local_partner)"
    )


class UpdateUserRequest(BaseModel):
    """Request body for updating a user."""

    model_config = ConfigDict(populate_by_name=True)

    name: str | None = Field(default=None, description="Display name")
    role: UserRole | None = Field(default=None, description="User role")
    entity: Entity | None = Field(default=None, description="Assigned entity")


class ChangePasswordRequest(BaseModel):
    """Request body for changing password."""

    model_config = ConfigDict(populate_by_name=True)

    current_password: str = Field(
        alias="currentPassword", description="Current password"
    )
    new_password: str = Field(
        alias="newPassword", min_length=12, description="New password (12+ chars)"
    )


class PasswordPolicy(BaseModel):
    """Password policy requirements."""

    model_config = ConfigDict(populate_by_name=True)

    min_length: int = Field(alias="minLength", description="Minimum length")
    max_length: int = Field(alias="maxLength", description="Maximum length")
    require_uppercase: bool = Field(
        alias="requireUppercase", description="Requires uppercase"
    )
    require_lowercase: bool = Field(
        alias="requireLowercase", description="Requires lowercase"
    )
    require_numbers: bool = Field(alias="requireNumbers", description="Requires numbers")
    require_special_chars: bool = Field(
        alias="requireSpecialChars", description="Requires special characters"
    )


class PasswordPolicyResponse(BaseModel):
    """Response from password policy endpoint."""

    model_config = ConfigDict(populate_by_name=True)

    policy: PasswordPolicy = Field(description="Policy configuration")
    requirements: list[str] = Field(description="Human-readable requirements")


class UserDeletedResponse(BaseModel):
    """Response from deleting a user."""

    message: str = Field(default="User deleted successfully")
