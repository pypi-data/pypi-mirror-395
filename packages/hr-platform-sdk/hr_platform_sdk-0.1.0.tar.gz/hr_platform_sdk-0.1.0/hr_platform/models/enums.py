"""Enums for HR Platform SDK.

This module defines enumeration types used throughout the SDK.
"""

from enum import Enum


class Entity(str, Enum):
    """Organizational entity codes.

    The platform supports three entities:
    - BVD: Bremen (Germany HQ)
    - VHH: Hamburg
    - VHO: Netherlands
    """

    BVD = "BVD"
    VHH = "VHH"
    VHO = "VHO"


class RecordStatus(str, Enum):
    """HR record workflow status.

    Status transitions:
    - DRAFT: Initial state, editable
    - SUBMITTED: Awaiting approval
    - APPROVED: Finalized (locked)
    - REJECTED: Returned for revision (editable)
    """

    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class UserRole(str, Enum):
    """User role codes.

    Role hierarchy:
    - system_admin: Platform administration, full access
    - group_head: HR manager, all entities, workflow approval
    - local_partner: Entity-scoped access
    """

    SYSTEM_ADMIN = "system_admin"
    GROUP_HEAD = "group_head"
    LOCAL_PARTNER = "local_partner"


class ComplianceDocumentType(str, Enum):
    """Compliance document types for GDPR flow.

    Users must acknowledge all documents on first login.
    """

    PRIVACY_NOTICE = "privacy_notice"
    LEGITIMATE_INTERESTS = "legitimate_interests"
    DATA_SUBJECT_RIGHTS = "data_subject_rights"
    INTERNAL_DATA_POLICY = "internal_data_policy"
    PASSWORD_SECURITY = "password_security"
