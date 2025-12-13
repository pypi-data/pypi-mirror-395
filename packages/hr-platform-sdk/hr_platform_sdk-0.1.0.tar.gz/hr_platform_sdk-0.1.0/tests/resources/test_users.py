"""Tests for HR Platform SDK users resource."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from hr_platform.core.http import HttpClient
from hr_platform.models.users import (
    CreateUserRequest,
    PasswordPolicyResponse,
    UpdateUserRequest,
    User,
    UserDeletedResponse,
    UserProfile,
)
from hr_platform.resources.users import UsersResource


@pytest.fixture
def http_client() -> MagicMock:
    """Create a mock HTTP client."""
    mock = MagicMock(spec=HttpClient)
    return mock


@pytest.fixture
def users_resource(http_client: MagicMock) -> UsersResource:
    """Create users resource with mock HTTP client."""
    return UsersResource(http_client)


class TestUsersResourceList:
    """Tests for users.list() method."""

    def test_list_users(
        self, users_resource: UsersResource, http_client: MagicMock, mock_user: dict
    ) -> None:
        """Test listing users."""
        http_client.get.return_value = [mock_user]

        result = users_resource.list()

        http_client.get.assert_called_once_with("/users", params=None)
        assert len(result) == 1
        assert isinstance(result[0], User)
        assert result[0].email == "test@vollers.de"

    def test_list_users_empty(
        self, users_resource: UsersResource, http_client: MagicMock
    ) -> None:
        """Test listing users returns empty list."""
        http_client.get.return_value = []

        result = users_resource.list()

        assert result == []


class TestUsersResourceGet:
    """Tests for users.get() method."""

    def test_get_user(
        self, users_resource: UsersResource, http_client: MagicMock, mock_user: dict
    ) -> None:
        """Test getting a user by ID."""
        http_client.get.return_value = mock_user

        result = users_resource.get("user-uuid-123")

        http_client.get.assert_called_once_with("/users/user-uuid-123", params=None)
        assert isinstance(result, User)
        assert result.id == "user-uuid-123"


class TestUsersResourceCreate:
    """Tests for users.create() method."""

    def test_create_user(
        self, users_resource: UsersResource, http_client: MagicMock, mock_user: dict
    ) -> None:
        """Test creating a user."""
        http_client.post.return_value = mock_user

        request = CreateUserRequest(
            name="New User",
            email="newuser@vollers.de",
            password="SecurePassword123!",
            role="local_partner",
            entity="BVD",
        )
        result = users_resource.create(request)

        http_client.post.assert_called_once()
        call_args = http_client.post.call_args
        assert call_args[0][0] == "/users"
        # Verify data and params are passed
        assert "data" in call_args.kwargs or len(call_args[0]) > 1 or call_args[1].get("data")
        assert isinstance(result, User)


class TestUsersResourceUpdate:
    """Tests for users.update() method."""

    def test_update_user(
        self, users_resource: UsersResource, http_client: MagicMock, mock_user: dict
    ) -> None:
        """Test updating a user."""
        http_client.put.return_value = mock_user

        request = UpdateUserRequest(
            name="Updated Name",
            role="group_head",
        )
        result = users_resource.update("user-uuid-123", request)

        http_client.put.assert_called_once()
        call_args = http_client.put.call_args
        assert call_args[0][0] == "/users/user-uuid-123"


class TestUsersResourceDelete:
    """Tests for users.delete() method."""

    def test_delete_user(
        self, users_resource: UsersResource, http_client: MagicMock
    ) -> None:
        """Test deleting a user."""
        http_client.delete.return_value = {"message": "User deleted successfully"}

        result = users_resource.delete("user-uuid-123")

        http_client.delete.assert_called_once_with("/users/user-uuid-123", params=None)
        assert isinstance(result, UserDeletedResponse)


class TestUsersResourceProfile:
    """Tests for profile-related methods."""

    def test_get_profile(
        self, users_resource: UsersResource, http_client: MagicMock
    ) -> None:
        """Test getting current user profile."""
        profile_data = {
            "id": "user-uuid-123",
            "name": "Test User",
            "email": "test@vollers.de",
            "role": "group_head",
            "entity": None,
        }
        http_client.get.return_value = profile_data

        result = users_resource.get_profile()

        # Implementation uses /users/me
        http_client.get.assert_called_once_with("/users/me", params=None)
        assert isinstance(result, UserProfile)

    def test_change_password(
        self, users_resource: UsersResource, http_client: MagicMock
    ) -> None:
        """Test changing password."""
        http_client.post.return_value = {"success": True}

        # Implementation takes two strings, not a request object
        result = users_resource.change_password(
            current_password="OldPassword123!",
            new_password="NewPassword456!",
        )

        http_client.post.assert_called_once()
        call_args = http_client.post.call_args
        # Implementation uses /users/me/password
        assert call_args[0][0] == "/users/me/password"


class TestUsersResourcePasswordPolicy:
    """Tests for password policy method."""

    def test_get_password_policy(
        self, users_resource: UsersResource, http_client: MagicMock
    ) -> None:
        """Test getting password policy."""
        policy_data = {
            "policy": {
                "minLength": 12,
                "maxLength": 128,
                "requireUppercase": True,
                "requireLowercase": True,
                "requireNumbers": True,
                "requireSpecialChars": True,
            },
            "requirements": [
                "At least 12 characters",
                "At least one uppercase letter",
            ],
        }
        http_client.get.return_value = policy_data

        result = users_resource.get_password_policy()

        http_client.get.assert_called_once_with("/users/password-policy", params=None)
        assert isinstance(result, PasswordPolicyResponse)
        assert result.policy.min_length == 12
