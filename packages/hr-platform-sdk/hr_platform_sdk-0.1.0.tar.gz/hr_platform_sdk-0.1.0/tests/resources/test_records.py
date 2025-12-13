"""Tests for HR Platform SDK records resource."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import httpx
import pytest

from hr_platform.core.config import ApiKeyAuth, HRPlatformConfig, RetryConfig
from hr_platform.core.http import HttpClient
from hr_platform.models.records import (
    CreateRecordRequest,
    FullHRRecord,
    RecordCreatedResponse,
    UpdateRecordRequest,
)
from hr_platform.resources.records import RecordsResource


@pytest.fixture
def http_client(config: HRPlatformConfig) -> MagicMock:
    """Create a mock HTTP client."""
    mock = MagicMock(spec=HttpClient)
    return mock


@pytest.fixture
def records_resource(http_client: MagicMock) -> RecordsResource:
    """Create records resource with mock HTTP client."""
    return RecordsResource(http_client)


class TestRecordsResourceList:
    """Tests for records.list() method."""

    def test_list_no_filters(
        self, records_resource: RecordsResource, http_client: MagicMock, mock_record: dict
    ) -> None:
        """Test listing records without filters."""
        http_client.get.return_value = [mock_record]

        result = records_resource.list()

        # When no filters, params is None (not {})
        http_client.get.assert_called_once_with("/records", params=None)
        assert len(result) == 1
        assert isinstance(result[0], FullHRRecord)
        assert result[0].entity == "BVD"

    def test_list_with_entity_filter(
        self, records_resource: RecordsResource, http_client: MagicMock, mock_record: dict
    ) -> None:
        """Test listing records with entity filter."""
        http_client.get.return_value = [mock_record]

        result = records_resource.list(entity="BVD")

        http_client.get.assert_called_once_with("/records", params={"entity": "BVD"})

    def test_list_with_year_filter(
        self, records_resource: RecordsResource, http_client: MagicMock, mock_record: dict
    ) -> None:
        """Test listing records with year filter."""
        http_client.get.return_value = [mock_record]

        result = records_resource.list(year="2025")

        http_client.get.assert_called_once_with("/records", params={"year": "2025"})

    def test_list_with_multiple_filters(
        self, records_resource: RecordsResource, http_client: MagicMock, mock_record: dict
    ) -> None:
        """Test listing records with multiple filters."""
        http_client.get.return_value = [mock_record]

        result = records_resource.list(entity="BVD", year="2025", month="12")

        http_client.get.assert_called_once_with(
            "/records", params={"entity": "BVD", "year": "2025", "month": "12"}
        )

    def test_list_empty_result(
        self, records_resource: RecordsResource, http_client: MagicMock
    ) -> None:
        """Test listing records returns empty list."""
        http_client.get.return_value = []

        result = records_resource.list()

        assert result == []


class TestRecordsResourceGet:
    """Tests for records.get() method."""

    def test_get_by_id(
        self, records_resource: RecordsResource, http_client: MagicMock, mock_record: dict
    ) -> None:
        """Test getting a record by ID."""
        http_client.get.return_value = mock_record

        result = records_resource.get("test-uuid-123")

        http_client.get.assert_called_once_with("/records/test-uuid-123", params=None)
        assert isinstance(result, FullHRRecord)
        assert result.id == "test-uuid-123"
        assert result.entity == "BVD"

    def test_get_returns_full_record(
        self, records_resource: RecordsResource, http_client: MagicMock, mock_record: dict
    ) -> None:
        """Test get returns full record with nested data."""
        http_client.get.return_value = mock_record

        result = records_resource.get("test-uuid-123")

        assert result.workforce is not None
        assert result.workforce.bc_male == 20
        assert result.capacity is not None
        assert result.capacity.fte_blue_collar == 20.2


class TestRecordsResourceCreate:
    """Tests for records.create() method."""

    def test_create_record(
        self, records_resource: RecordsResource, http_client: MagicMock
    ) -> None:
        """Test creating a record."""
        http_client.post.return_value = {
            "id": "new-uuid-456",
            "message": "Record created successfully",
        }

        request = CreateRecordRequest(
            entity="BVD",
            year=2025,
            month=12,
            working_days=21,
        )
        result = records_resource.create(request)

        http_client.post.assert_called_once()
        call_args = http_client.post.call_args
        assert call_args[0][0] == "/records"
        assert isinstance(result, RecordCreatedResponse)
        assert result.id == "new-uuid-456"

    def test_create_record_with_nested_data(
        self, records_resource: RecordsResource, http_client: MagicMock
    ) -> None:
        """Test creating a record with nested workforce data."""
        http_client.post.return_value = {
            "id": "new-uuid-789",
            "message": "Record created successfully",
        }

        request = CreateRecordRequest(
            entity="VHH",
            year=2025,
            month=11,
            working_days=20,
        )
        result = records_resource.create(request)

        assert result.id == "new-uuid-789"


class TestRecordsResourceUpdate:
    """Tests for records.update() method."""

    def test_update_record(
        self, records_resource: RecordsResource, http_client: MagicMock
    ) -> None:
        """Test updating a record."""
        http_client.put.return_value = {
            "id": "test-uuid-123",
            "message": "Record updated successfully",
        }

        request = UpdateRecordRequest(
            entity="BVD",
            year=2025,
            month=12,
            working_days=22,
        )
        result = records_resource.update("test-uuid-123", request)

        http_client.put.assert_called_once()
        call_args = http_client.put.call_args
        assert call_args[0][0] == "/records/test-uuid-123"


class TestRecordsResourceDelete:
    """Tests for records.delete() method."""

    def test_delete_record(
        self, records_resource: RecordsResource, http_client: MagicMock
    ) -> None:
        """Test deleting a record."""
        http_client.delete.return_value = {"message": "Record deleted successfully"}

        result = records_resource.delete("test-uuid-123")

        http_client.delete.assert_called_once_with("/records/test-uuid-123", params=None)


class TestRecordsResourceWorkflow:
    """Tests for workflow methods (submit, approve, reject)."""

    def test_submit_record(
        self, records_resource: RecordsResource, http_client: MagicMock
    ) -> None:
        """Test submitting a record for approval."""
        http_client.post.return_value = {"message": "Record submitted for approval"}

        result = records_resource.submit("test-uuid-123")

        http_client.post.assert_called_once_with(
            "/records/test-uuid-123/submit", data=None, params=None
        )

    def test_approve_record(
        self, records_resource: RecordsResource, http_client: MagicMock
    ) -> None:
        """Test approving a record."""
        http_client.post.return_value = {"message": "Record approved"}

        result = records_resource.approve("test-uuid-123")

        http_client.post.assert_called_once_with(
            "/records/test-uuid-123/approve", data=None, params=None
        )

    def test_reject_record(
        self, records_resource: RecordsResource, http_client: MagicMock
    ) -> None:
        """Test rejecting a record with reason."""
        http_client.post.return_value = {"message": "Record rejected"}

        result = records_resource.reject("test-uuid-123", reason="Data needs correction")

        http_client.post.assert_called_once_with(
            "/records/test-uuid-123/reject",
            data={"reason": "Data needs correction"},
            params=None,
        )
