"""Records resource.

API resource for HR record operations.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from hr_platform.models.records import (
    CreateRecordRequest,
    FullHRRecord,
    RecordCreatedResponse,
    RecordDeletedResponse,
    RecordUpdatedResponse,
    RejectRecordRequest,
    UpdateRecordRequest,
    WorkflowResponse,
)
from hr_platform.resources.base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from hr_platform.core.async_http import AsyncHttpClient
    from hr_platform.core.http import HttpClient


class RecordsResource(BaseResource):
    """Synchronous records API resource.

    Provides methods for HR record CRUD operations and workflow actions.

    Example:
        >>> records = client.records.list(entity="BVD", year="2025")
        >>> record = client.records.get("record-uuid")
        >>> new_record = client.records.create(CreateRecordRequest(...))
    """

    def __init__(self, client: "HttpClient") -> None:
        """Initialize records resource.

        Args:
            client: HTTP client instance.
        """
        super().__init__(client)

    def list(
        self,
        *,
        entity: str | None = None,
        year: str | None = None,
        month: str | None = None,
        status: str | None = None,
    ) -> list[FullHRRecord]:
        """List HR records with optional filters.

        Args:
            entity: Filter by entity code (BVD, VHH, VHO).
            year: Filter by year.
            month: Filter by month (1-12).
            status: Filter by status (DRAFT, SUBMITTED, APPROVED, REJECTED).

        Returns:
            List of HR records with full nested data.

        Example:
            >>> records = client.records.list(entity="BVD", year="2025")
            >>> for record in records:
            ...     print(f"{record.entity} {record.year}/{record.month}")
        """
        params: dict[str, str] = {}
        if entity is not None:
            params["entity"] = entity
        if year is not None:
            params["year"] = year
        if month is not None:
            params["month"] = month
        if status is not None:
            params["status"] = status

        data = self._get("/records", params=params if params else None)
        return [FullHRRecord.model_validate(item) for item in data]

    def get(self, record_id: str) -> FullHRRecord:
        """Get a single HR record by ID.

        Args:
            record_id: UUID of the record.

        Returns:
            Full HR record with nested data.

        Raises:
            NotFoundError: If record doesn't exist.

        Example:
            >>> record = client.records.get("550e8400-e29b-41d4-a716-446655440000")
            >>> print(record.status)
        """
        data = self._get(f"/records/{record_id}")
        return FullHRRecord.model_validate(data)

    def create(self, request: CreateRecordRequest) -> RecordCreatedResponse:
        """Create a new HR record.

        Args:
            request: Record creation request with all required data.

        Returns:
            Response containing the new record ID.

        Raises:
            ValidationError: If request data is invalid.
            ConflictError: If record for entity/year/month already exists.

        Example:
            >>> from hr_platform.models import CreateRecordRequest, Entity
            >>> response = client.records.create(CreateRecordRequest(
            ...     entity=Entity.BVD,
            ...     year=2025,
            ...     month=10,
            ...     working_days=21,
            ... ))
            >>> print(response.id)
        """
        data = self._post("/records", data=request.model_dump(by_alias=True))
        return RecordCreatedResponse.model_validate(data)

    def update(
        self, record_id: str, request: UpdateRecordRequest
    ) -> RecordUpdatedResponse:
        """Update an existing HR record.

        Args:
            record_id: UUID of the record to update.
            request: Update request with fields to change.

        Returns:
            Response confirming the update.

        Raises:
            NotFoundError: If record doesn't exist.
            ValidationError: If request data is invalid.
            HRPlatformError: If record is not in editable status.

        Example:
            >>> from hr_platform.models import UpdateRecordRequest
            >>> response = client.records.update(
            ...     "record-uuid",
            ...     UpdateRecordRequest(working_days=22)
            ... )
        """
        data = self._put(
            f"/records/{record_id}",
            data=request.model_dump(by_alias=True, exclude_none=True),
        )
        return RecordUpdatedResponse.model_validate(data)

    def delete(self, record_id: str) -> RecordDeletedResponse:
        """Delete an HR record.

        Args:
            record_id: UUID of the record to delete.

        Returns:
            Response confirming deletion.

        Raises:
            NotFoundError: If record doesn't exist.
            AuthorizationError: If user lacks delete permission.

        Example:
            >>> response = client.records.delete("record-uuid")
            >>> print(response.message)
        """
        data = self._delete(f"/records/{record_id}")
        return RecordDeletedResponse.model_validate(data)

    def submit(self, record_id: str) -> WorkflowResponse:
        """Submit a record for approval.

        Transitions record from DRAFT to SUBMITTED status.

        Args:
            record_id: UUID of the record to submit.

        Returns:
            Workflow response confirming submission.

        Raises:
            NotFoundError: If record doesn't exist.
            HRPlatformError: If record is not in submittable status.

        Example:
            >>> response = client.records.submit("record-uuid")
            >>> print(response.message)
        """
        data = self._post(f"/records/{record_id}/submit")
        return WorkflowResponse.model_validate(data)

    def approve(self, record_id: str) -> WorkflowResponse:
        """Approve a submitted record.

        Transitions record from SUBMITTED to APPROVED status.

        Args:
            record_id: UUID of the record to approve.

        Returns:
            Workflow response confirming approval.

        Raises:
            NotFoundError: If record doesn't exist.
            AuthorizationError: If user lacks approval permission.
            HRPlatformError: If record is not in approvable status.

        Example:
            >>> response = client.records.approve("record-uuid")
            >>> print(response.message)
        """
        data = self._post(f"/records/{record_id}/approve")
        return WorkflowResponse.model_validate(data)

    def reject(self, record_id: str, reason: str) -> WorkflowResponse:
        """Reject a submitted record.

        Transitions record from SUBMITTED to REJECTED status.

        Args:
            record_id: UUID of the record to reject.
            reason: Required reason for rejection.

        Returns:
            Workflow response confirming rejection.

        Raises:
            NotFoundError: If record doesn't exist.
            AuthorizationError: If user lacks rejection permission.
            ValidationError: If reason is empty.
            HRPlatformError: If record is not in rejectable status.

        Example:
            >>> response = client.records.reject(
            ...     "record-uuid",
            ...     reason="Sick days calculation incorrect"
            ... )
            >>> print(response.message)
        """
        request = RejectRecordRequest(reason=reason)
        data = self._post(
            f"/records/{record_id}/reject",
            data=request.model_dump(by_alias=True),
        )
        return WorkflowResponse.model_validate(data)


class AsyncRecordsResource(AsyncBaseResource):
    """Asynchronous records API resource.

    Provides async methods for HR record CRUD operations and workflow actions.

    Example:
        >>> records = await client.records.list(entity="BVD", year="2025")
        >>> record = await client.records.get("record-uuid")
    """

    def __init__(self, client: "AsyncHttpClient") -> None:
        """Initialize async records resource.

        Args:
            client: Async HTTP client instance.
        """
        super().__init__(client)

    async def list(
        self,
        *,
        entity: str | None = None,
        year: str | None = None,
        month: str | None = None,
        status: str | None = None,
    ) -> list[FullHRRecord]:
        """List HR records with optional filters.

        Args:
            entity: Filter by entity code (BVD, VHH, VHO).
            year: Filter by year.
            month: Filter by month (1-12).
            status: Filter by status (DRAFT, SUBMITTED, APPROVED, REJECTED).

        Returns:
            List of HR records with full nested data.
        """
        params: dict[str, str] = {}
        if entity is not None:
            params["entity"] = entity
        if year is not None:
            params["year"] = year
        if month is not None:
            params["month"] = month
        if status is not None:
            params["status"] = status

        data = await self._get("/records", params=params if params else None)
        return [FullHRRecord.model_validate(item) for item in data]

    async def get(self, record_id: str) -> FullHRRecord:
        """Get a single HR record by ID.

        Args:
            record_id: UUID of the record.

        Returns:
            Full HR record with nested data.

        Raises:
            NotFoundError: If record doesn't exist.
        """
        data = await self._get(f"/records/{record_id}")
        return FullHRRecord.model_validate(data)

    async def create(self, request: CreateRecordRequest) -> RecordCreatedResponse:
        """Create a new HR record.

        Args:
            request: Record creation request with all required data.

        Returns:
            Response containing the new record ID.

        Raises:
            ValidationError: If request data is invalid.
            ConflictError: If record for entity/year/month already exists.
        """
        data = await self._post("/records", data=request.model_dump(by_alias=True))
        return RecordCreatedResponse.model_validate(data)

    async def update(
        self, record_id: str, request: UpdateRecordRequest
    ) -> RecordUpdatedResponse:
        """Update an existing HR record.

        Args:
            record_id: UUID of the record to update.
            request: Update request with fields to change.

        Returns:
            Response confirming the update.

        Raises:
            NotFoundError: If record doesn't exist.
            ValidationError: If request data is invalid.
            HRPlatformError: If record is not in editable status.
        """
        data = await self._put(
            f"/records/{record_id}",
            data=request.model_dump(by_alias=True, exclude_none=True),
        )
        return RecordUpdatedResponse.model_validate(data)

    async def delete(self, record_id: str) -> RecordDeletedResponse:
        """Delete an HR record.

        Args:
            record_id: UUID of the record to delete.

        Returns:
            Response confirming deletion.

        Raises:
            NotFoundError: If record doesn't exist.
            AuthorizationError: If user lacks delete permission.
        """
        data = await self._delete(f"/records/{record_id}")
        return RecordDeletedResponse.model_validate(data)

    async def submit(self, record_id: str) -> WorkflowResponse:
        """Submit a record for approval.

        Transitions record from DRAFT to SUBMITTED status.

        Args:
            record_id: UUID of the record to submit.

        Returns:
            Workflow response confirming submission.

        Raises:
            NotFoundError: If record doesn't exist.
            HRPlatformError: If record is not in submittable status.
        """
        data = await self._post(f"/records/{record_id}/submit")
        return WorkflowResponse.model_validate(data)

    async def approve(self, record_id: str) -> WorkflowResponse:
        """Approve a submitted record.

        Transitions record from SUBMITTED to APPROVED status.

        Args:
            record_id: UUID of the record to approve.

        Returns:
            Workflow response confirming approval.

        Raises:
            NotFoundError: If record doesn't exist.
            AuthorizationError: If user lacks approval permission.
            HRPlatformError: If record is not in approvable status.
        """
        data = await self._post(f"/records/{record_id}/approve")
        return WorkflowResponse.model_validate(data)

    async def reject(self, record_id: str, reason: str) -> WorkflowResponse:
        """Reject a submitted record.

        Transitions record from SUBMITTED to REJECTED status.

        Args:
            record_id: UUID of the record to reject.
            reason: Required reason for rejection.

        Returns:
            Workflow response confirming rejection.

        Raises:
            NotFoundError: If record doesn't exist.
            AuthorizationError: If user lacks rejection permission.
            ValidationError: If reason is empty.
            HRPlatformError: If record is not in rejectable status.
        """
        request = RejectRecordRequest(reason=reason)
        data = await self._post(
            f"/records/{record_id}/reject",
            data=request.model_dump(by_alias=True),
        )
        return WorkflowResponse.model_validate(data)
