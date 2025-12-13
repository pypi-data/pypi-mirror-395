"""Compliance models.

Pydantic models for GDPR compliance document flow.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from hr_platform.models.enums import ComplianceDocumentType


class ComplianceDocument(BaseModel):
    """Compliance document content.

    Legal documents users must acknowledge on first login.
    """

    model_config = ConfigDict(populate_by_name=True)

    type: ComplianceDocumentType = Field(description="Document type identifier")
    version: str = Field(description="Document version (semver)")
    title: str = Field(description="Document title")
    summary: str = Field(description="Brief summary of document")
    full_content: str = Field(alias="fullContent", description="Full document text")
    content_hash: str = Field(alias="contentHash", description="SHA-256 hash of content")


class DocumentAcknowledgment(BaseModel):
    """Record of a document acknowledgment."""

    model_config = ConfigDict(populate_by_name=True)

    document_type: ComplianceDocumentType = Field(
        alias="documentType", description="Document type"
    )
    document_version: str = Field(alias="documentVersion", description="Version")
    acknowledged_at: str = Field(alias="acknowledgedAt", description="Timestamp")


class UserComplianceStatus(BaseModel):
    """User's compliance status.

    Tracks which documents have been acknowledged.
    """

    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias="userId", description="User ID")
    is_first_login: bool = Field(alias="isFirstLogin", description="First login flag")
    compliance_completed_at: str | None = Field(
        alias="complianceCompletedAt", default=None, description="Completion timestamp"
    )
    compliance_version: str | None = Field(
        alias="complianceVersion", default=None, description="Version acknowledged"
    )
    acknowledged_documents: list[DocumentAcknowledgment] = Field(
        alias="acknowledgedDocuments", default_factory=list
    )
    pending_documents: list[ComplianceDocumentType] = Field(
        alias="pendingDocuments", default_factory=list
    )


class ComplianceDocumentsResponse(BaseModel):
    """Response containing all compliance documents."""

    model_config = ConfigDict(populate_by_name=True)

    documents: list[ComplianceDocument] = Field(description="All documents")


class AcknowledgeDocumentRequest(BaseModel):
    """Request to acknowledge a compliance document."""

    model_config = ConfigDict(populate_by_name=True)

    document_type: ComplianceDocumentType = Field(
        alias="documentType", description="Document type to acknowledge"
    )
    document_version: str = Field(alias="documentVersion", description="Version")
    document_content_hash: str = Field(
        alias="documentContentHash", description="Content hash for verification"
    )


class AcknowledgeDocumentResponse(BaseModel):
    """Response from acknowledging a document."""

    model_config = ConfigDict(populate_by_name=True)

    success: bool = Field(description="Success flag")
    document_type: ComplianceDocumentType = Field(
        alias="documentType", description="Document acknowledged"
    )
    acknowledged_at: str = Field(alias="acknowledgedAt", description="Timestamp")


class CompleteComplianceResponse(BaseModel):
    """Response from completing the compliance flow."""

    model_config = ConfigDict(populate_by_name=True)

    success: bool = Field(description="Success flag")
    completed_at: str = Field(alias="completedAt", description="Completion timestamp")


class AdminUserComplianceRecord(BaseModel):
    """Admin view of user's compliance status."""

    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias="userId", description="User ID")
    user_email: str = Field(alias="userEmail", description="User email")
    user_name: str = Field(alias="userName", description="User name")
    role: str = Field(description="User role")
    is_first_login: bool = Field(alias="isFirstLogin", description="First login flag")
    compliance_completed_at: str | None = Field(
        alias="complianceCompletedAt", default=None
    )
    compliance_version: str | None = Field(alias="complianceVersion", default=None)
    pending_documents: int = Field(
        alias="pendingDocuments", description="Count of pending documents"
    )


class AdminComplianceOverview(BaseModel):
    """Admin compliance dashboard data."""

    model_config = ConfigDict(populate_by_name=True)

    summary: "ComplianceSummary" = Field(description="Summary statistics")
    users: list[AdminUserComplianceRecord] = Field(description="User list")


class ComplianceSummary(BaseModel):
    """Summary statistics for compliance."""

    model_config = ConfigDict(populate_by_name=True)

    total_users: int = Field(alias="totalUsers", description="Total user count")
    completed_users: int = Field(
        alias="completedUsers", description="Users who completed compliance"
    )
    pending_users: int = Field(
        alias="pendingUsers", description="Users pending compliance"
    )


class ResetComplianceResponse(BaseModel):
    """Response from resetting user compliance."""

    model_config = ConfigDict(populate_by_name=True)

    success: bool = Field(description="Success flag")
    user_id: str = Field(alias="userId", description="User ID reset")
    message: str = Field(description="Result message")
