"""Compliance resource.

API resource for GDPR compliance document flow.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from hr_platform.models.compliance import (
    AcknowledgeDocumentRequest,
    AcknowledgeDocumentResponse,
    AdminComplianceOverview,
    CompleteComplianceResponse,
    ComplianceDocument,
    ComplianceDocumentsResponse,
    ResetComplianceResponse,
    UserComplianceStatus,
)
from hr_platform.models.enums import ComplianceDocumentType
from hr_platform.resources.base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from hr_platform.core.async_http import AsyncHttpClient
    from hr_platform.core.http import HttpClient


class ComplianceResource(BaseResource):
    """Synchronous compliance API resource.

    Provides methods for GDPR compliance document acknowledgment flow.

    Example:
        >>> status = client.compliance.get_status()
        >>> documents = client.compliance.get_documents()
        >>> client.compliance.acknowledge(document_type, version, hash)
    """

    def __init__(self, client: "HttpClient") -> None:
        """Initialize compliance resource.

        Args:
            client: HTTP client instance.
        """
        super().__init__(client)

    def get_status(self) -> UserComplianceStatus:
        """Get the current user's compliance status.

        Returns:
            User's compliance status with acknowledged and pending documents.

        Example:
            >>> status = client.compliance.get_status()
            >>> if status.pending_documents:
            ...     print(f"{len(status.pending_documents)} documents pending")
            >>> if status.compliance_completed_at:
            ...     print(f"Completed: {status.compliance_completed_at}")
        """
        data = self._get("/compliance/status")
        return UserComplianceStatus.model_validate(data)

    def get_documents(self) -> ComplianceDocumentsResponse:
        """Get all compliance documents with content.

        Returns:
            Response containing all compliance documents.

        Example:
            >>> response = client.compliance.get_documents()
            >>> for doc in response.documents:
            ...     print(f"{doc.title} v{doc.version}")
        """
        data = self._get("/compliance/documents")
        return ComplianceDocumentsResponse.model_validate(data)

    def get_document(
        self, document_type: ComplianceDocumentType | str
    ) -> ComplianceDocument:
        """Get a specific compliance document.

        Args:
            document_type: Document type identifier.

        Returns:
            Compliance document with full content.

        Raises:
            NotFoundError: If document doesn't exist.

        Example:
            >>> doc = client.compliance.get_document("privacy_notice")
            >>> print(doc.full_content)
        """
        doc_type = (
            document_type.value
            if isinstance(document_type, ComplianceDocumentType)
            else document_type
        )
        data = self._get(f"/compliance/documents/{doc_type}")
        return ComplianceDocument.model_validate(data)

    def acknowledge(
        self,
        document_type: ComplianceDocumentType | str,
        document_version: str,
        document_content_hash: str,
    ) -> AcknowledgeDocumentResponse:
        """Acknowledge a compliance document.

        Args:
            document_type: Document type identifier.
            document_version: Document version (must match current).
            document_content_hash: Content hash (must match for verification).

        Returns:
            Response confirming acknowledgment.

        Raises:
            ValidationError: If content hash doesn't match.

        Example:
            >>> doc = client.compliance.get_document("privacy_notice")
            >>> response = client.compliance.acknowledge(
            ...     document_type=doc.type,
            ...     document_version=doc.version,
            ...     document_content_hash=doc.content_hash,
            ... )
            >>> print(f"Acknowledged at: {response.acknowledged_at}")
        """
        doc_type = (
            document_type
            if isinstance(document_type, ComplianceDocumentType)
            else ComplianceDocumentType(document_type)
        )
        request = AcknowledgeDocumentRequest(
            document_type=doc_type,
            document_version=document_version,
            document_content_hash=document_content_hash,
        )
        data = self._post(
            "/compliance/acknowledge",
            data=request.model_dump(by_alias=True),
        )
        return AcknowledgeDocumentResponse.model_validate(data)

    def complete(self) -> CompleteComplianceResponse:
        """Complete the compliance flow.

        Call after all documents have been acknowledged.

        Returns:
            Response confirming completion.

        Raises:
            HRPlatformError: If documents still pending.

        Example:
            >>> response = client.compliance.complete()
            >>> print(f"Completed at: {response.completed_at}")
        """
        data = self._post("/compliance/complete")
        return CompleteComplianceResponse.model_validate(data)

    # Admin endpoints

    def get_admin_overview(self) -> AdminComplianceOverview:
        """Get compliance status overview for all users.

        Requires system_admin role.

        Returns:
            Admin compliance overview with summary and user list.

        Example:
            >>> overview = client.compliance.get_admin_overview()
            >>> print(f"Completed: {overview.summary.completed_users}")
            >>> print(f"Pending: {overview.summary.pending_users}")
        """
        data = self._get("/admin/compliance/status")
        return AdminComplianceOverview.model_validate(data)

    def reset_user(self, user_id: str) -> ResetComplianceResponse:
        """Reset a user's compliance status.

        User will see compliance flow on next login.
        Requires system_admin role.

        Args:
            user_id: UUID of the user to reset.

        Returns:
            Response confirming reset.

        Example:
            >>> response = client.compliance.reset_user("user-uuid")
            >>> print(response.message)
        """
        data = self._post(f"/admin/compliance/reset/{user_id}")
        return ResetComplianceResponse.model_validate(data)


class AsyncComplianceResource(AsyncBaseResource):
    """Asynchronous compliance API resource.

    Provides async methods for GDPR compliance document acknowledgment flow.

    Example:
        >>> status = await client.compliance.get_status()
        >>> documents = await client.compliance.get_documents()
    """

    def __init__(self, client: "AsyncHttpClient") -> None:
        """Initialize async compliance resource.

        Args:
            client: Async HTTP client instance.
        """
        super().__init__(client)

    async def get_status(self) -> UserComplianceStatus:
        """Get the current user's compliance status."""
        data = await self._get("/compliance/status")
        return UserComplianceStatus.model_validate(data)

    async def get_documents(self) -> ComplianceDocumentsResponse:
        """Get all compliance documents with content."""
        data = await self._get("/compliance/documents")
        return ComplianceDocumentsResponse.model_validate(data)

    async def get_document(
        self, document_type: ComplianceDocumentType | str
    ) -> ComplianceDocument:
        """Get a specific compliance document."""
        doc_type = (
            document_type.value
            if isinstance(document_type, ComplianceDocumentType)
            else document_type
        )
        data = await self._get(f"/compliance/documents/{doc_type}")
        return ComplianceDocument.model_validate(data)

    async def acknowledge(
        self,
        document_type: ComplianceDocumentType | str,
        document_version: str,
        document_content_hash: str,
    ) -> AcknowledgeDocumentResponse:
        """Acknowledge a compliance document."""
        doc_type = (
            document_type
            if isinstance(document_type, ComplianceDocumentType)
            else ComplianceDocumentType(document_type)
        )
        request = AcknowledgeDocumentRequest(
            document_type=doc_type,
            document_version=document_version,
            document_content_hash=document_content_hash,
        )
        data = await self._post(
            "/compliance/acknowledge",
            data=request.model_dump(by_alias=True),
        )
        return AcknowledgeDocumentResponse.model_validate(data)

    async def complete(self) -> CompleteComplianceResponse:
        """Complete the compliance flow."""
        data = await self._post("/compliance/complete")
        return CompleteComplianceResponse.model_validate(data)

    # Admin endpoints

    async def get_admin_overview(self) -> AdminComplianceOverview:
        """Get compliance status overview for all users."""
        data = await self._get("/admin/compliance/status")
        return AdminComplianceOverview.model_validate(data)

    async def reset_user(self, user_id: str) -> ResetComplianceResponse:
        """Reset a user's compliance status."""
        data = await self._post(f"/admin/compliance/reset/{user_id}")
        return ResetComplianceResponse.model_validate(data)
