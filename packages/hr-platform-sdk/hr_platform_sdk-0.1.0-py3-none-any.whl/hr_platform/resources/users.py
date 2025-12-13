"""Users resource.

API resource for user management operations.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from hr_platform.models.users import (
    ChangePasswordRequest,
    CreateUserRequest,
    PasswordPolicyResponse,
    Session,
    SessionInfo,
    UpdateUserRequest,
    User,
    UserDeletedResponse,
    UserProfile,
)
from hr_platform.resources.base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from hr_platform.core.async_http import AsyncHttpClient
    from hr_platform.core.http import HttpClient


class UsersResource(BaseResource):
    """Synchronous users API resource.

    Provides methods for user management and profile operations.

    Example:
        >>> users = client.users.list()
        >>> user = client.users.get("user-uuid")
        >>> profile = client.users.get_profile()
    """

    def __init__(self, client: "HttpClient") -> None:
        """Initialize users resource.

        Args:
            client: HTTP client instance.
        """
        super().__init__(client)

    def list(self) -> list[User]:
        """List all users.

        Requires system_admin role.

        Returns:
            List of user accounts.

        Raises:
            AuthorizationError: If user lacks admin permission.

        Example:
            >>> users = client.users.list()
            >>> for user in users:
            ...     print(f"{user.name} ({user.role})")
        """
        data = self._get("/users")
        return [User.model_validate(item) for item in data]

    def get(self, user_id: str) -> User:
        """Get a single user by ID.

        Requires system_admin role.

        Args:
            user_id: UUID of the user.

        Returns:
            User account details.

        Raises:
            NotFoundError: If user doesn't exist.
            AuthorizationError: If user lacks admin permission.

        Example:
            >>> user = client.users.get("550e8400-e29b-41d4-a716-446655440000")
            >>> print(f"{user.name}: {user.email}")
        """
        data = self._get(f"/users/{user_id}")
        return User.model_validate(data)

    def create(self, request: CreateUserRequest) -> User:
        """Create a new user.

        Requires system_admin role. Only system_admin can create
        other system_admin users.

        Args:
            request: User creation request.

        Returns:
            Created user account.

        Raises:
            ValidationError: If request data is invalid.
            AuthorizationError: If user lacks admin permission.

        Example:
            >>> from hr_platform.models import CreateUserRequest, UserRole, Entity
            >>> user = client.users.create(CreateUserRequest(
            ...     email="partner@vollers.de",
            ...     name="New Partner",
            ...     password="SecurePass123!",
            ...     role=UserRole.LOCAL_PARTNER,
            ...     entity=Entity.BVD,
            ... ))
        """
        data = self._post("/users", data=request.model_dump(by_alias=True))
        return User.model_validate(data)

    def update(self, user_id: str, request: UpdateUserRequest) -> User:
        """Update a user.

        Requires system_admin role. Cannot change own role.
        Only system_admin can promote users to system_admin.

        Args:
            user_id: UUID of the user to update.
            request: Update request with fields to change.

        Returns:
            Updated user account.

        Raises:
            NotFoundError: If user doesn't exist.
            ValidationError: If request data is invalid.
            AuthorizationError: If user lacks admin permission.

        Example:
            >>> from hr_platform.models import UpdateUserRequest, UserRole
            >>> user = client.users.update(
            ...     "user-uuid",
            ...     UpdateUserRequest(role=UserRole.GROUP_HEAD)
            ... )
        """
        data = self._put(
            f"/users/{user_id}",
            data=request.model_dump(by_alias=True, exclude_none=True),
        )
        return User.model_validate(data)

    def delete(self, user_id: str) -> UserDeletedResponse:
        """Delete a user.

        Requires system_admin role. Cannot delete own account.

        Args:
            user_id: UUID of the user to delete.

        Returns:
            Response confirming deletion.

        Raises:
            NotFoundError: If user doesn't exist.
            AuthorizationError: If user lacks admin permission.
            HRPlatformError: If attempting to delete own account.

        Example:
            >>> response = client.users.delete("user-uuid")
            >>> print(response.message)
        """
        data = self._delete(f"/users/{user_id}")
        return UserDeletedResponse.model_validate(data)

    def get_profile(self) -> UserProfile:
        """Get the current user's profile.

        Returns:
            Current user profile from session.

        Example:
            >>> profile = client.users.get_profile()
            >>> print(f"Logged in as: {profile.name}")
        """
        data = self._get("/users/me")
        return UserProfile.model_validate(data)

    def get_session(self) -> SessionInfo:
        """Get current session information.

        Returns:
            Session info with user profile and session details.

        Raises:
            AuthenticationError: If no valid session.

        Example:
            >>> session = client.users.get_session()
            >>> print(f"Session expires: {session.session.expires_at}")
        """
        data = self._get("/auth/get-session")
        return SessionInfo.model_validate(data)

    def change_password(
        self, current_password: str, new_password: str
    ) -> dict[str, str]:
        """Change the current user's password.

        Args:
            current_password: Current password for verification.
            new_password: New password (must meet policy requirements).

        Returns:
            Success message.

        Raises:
            ValidationError: If new password doesn't meet policy.
            AuthenticationError: If current password is incorrect.

        Example:
            >>> result = client.users.change_password(
            ...     current_password="OldPass123!",
            ...     new_password="NewSecure456@"
            ... )
        """
        request = ChangePasswordRequest(
            current_password=current_password,
            new_password=new_password,
        )
        return self._post(
            "/users/me/password",
            data=request.model_dump(by_alias=True),
        )

    def get_password_policy(self) -> PasswordPolicyResponse:
        """Get password policy requirements.

        Returns:
            Password policy with requirements.

        Example:
            >>> policy = client.users.get_password_policy()
            >>> print(f"Min length: {policy.policy.min_length}")
            >>> for req in policy.requirements:
            ...     print(f"- {req}")
        """
        data = self._get("/users/password-policy")
        return PasswordPolicyResponse.model_validate(data)


class AsyncUsersResource(AsyncBaseResource):
    """Asynchronous users API resource.

    Provides async methods for user management and profile operations.

    Example:
        >>> users = await client.users.list()
        >>> profile = await client.users.get_profile()
    """

    def __init__(self, client: "AsyncHttpClient") -> None:
        """Initialize async users resource.

        Args:
            client: Async HTTP client instance.
        """
        super().__init__(client)

    async def list(self) -> list[User]:
        """List all users.

        Requires system_admin role.

        Returns:
            List of user accounts.

        Raises:
            AuthorizationError: If user lacks admin permission.
        """
        data = await self._get("/users")
        return [User.model_validate(item) for item in data]

    async def get(self, user_id: str) -> User:
        """Get a single user by ID.

        Requires system_admin role.

        Args:
            user_id: UUID of the user.

        Returns:
            User account details.

        Raises:
            NotFoundError: If user doesn't exist.
            AuthorizationError: If user lacks admin permission.
        """
        data = await self._get(f"/users/{user_id}")
        return User.model_validate(data)

    async def create(self, request: CreateUserRequest) -> User:
        """Create a new user.

        Requires system_admin role. Only system_admin can create
        other system_admin users.

        Args:
            request: User creation request.

        Returns:
            Created user account.

        Raises:
            ValidationError: If request data is invalid.
            AuthorizationError: If user lacks admin permission.
        """
        data = await self._post("/users", data=request.model_dump(by_alias=True))
        return User.model_validate(data)

    async def update(self, user_id: str, request: UpdateUserRequest) -> User:
        """Update a user.

        Requires system_admin role. Cannot change own role.
        Only system_admin can promote users to system_admin.

        Args:
            user_id: UUID of the user to update.
            request: Update request with fields to change.

        Returns:
            Updated user account.

        Raises:
            NotFoundError: If user doesn't exist.
            ValidationError: If request data is invalid.
            AuthorizationError: If user lacks admin permission.
        """
        data = await self._put(
            f"/users/{user_id}",
            data=request.model_dump(by_alias=True, exclude_none=True),
        )
        return User.model_validate(data)

    async def delete(self, user_id: str) -> UserDeletedResponse:
        """Delete a user.

        Requires system_admin role. Cannot delete own account.

        Args:
            user_id: UUID of the user to delete.

        Returns:
            Response confirming deletion.

        Raises:
            NotFoundError: If user doesn't exist.
            AuthorizationError: If user lacks admin permission.
            HRPlatformError: If attempting to delete own account.
        """
        data = await self._delete(f"/users/{user_id}")
        return UserDeletedResponse.model_validate(data)

    async def get_profile(self) -> UserProfile:
        """Get the current user's profile.

        Returns:
            Current user profile from session.
        """
        data = await self._get("/users/me")
        return UserProfile.model_validate(data)

    async def get_session(self) -> SessionInfo:
        """Get current session information.

        Returns:
            Session info with user profile and session details.

        Raises:
            AuthenticationError: If no valid session.
        """
        data = await self._get("/auth/get-session")
        return SessionInfo.model_validate(data)

    async def change_password(
        self, current_password: str, new_password: str
    ) -> dict[str, str]:
        """Change the current user's password.

        Args:
            current_password: Current password for verification.
            new_password: New password (must meet policy requirements).

        Returns:
            Success message.

        Raises:
            ValidationError: If new password doesn't meet policy.
            AuthenticationError: If current password is incorrect.
        """
        request = ChangePasswordRequest(
            current_password=current_password,
            new_password=new_password,
        )
        return await self._post(
            "/users/me/password",
            data=request.model_dump(by_alias=True),
        )

    async def get_password_policy(self) -> PasswordPolicyResponse:
        """Get password policy requirements.

        Returns:
            Password policy with requirements.
        """
        data = await self._get("/users/password-policy")
        return PasswordPolicyResponse.model_validate(data)
