"""HR Platform SDK Resources.

API resource classes for interacting with the HR Platform.

Example:
    >>> from hr_platform.resources import RecordsResource, AnalyticsResource
"""

from hr_platform.resources.admin import AdminResource, AsyncAdminResource
from hr_platform.resources.analytics import AnalyticsResource, AsyncAnalyticsResource
from hr_platform.resources.base import AsyncBaseResource, BaseResource
from hr_platform.resources.compliance import AsyncComplianceResource, ComplianceResource
from hr_platform.resources.records import AsyncRecordsResource, RecordsResource
from hr_platform.resources.users import AsyncUsersResource, UsersResource
from hr_platform.resources.webhooks import AsyncWebhooksResource, WebhooksResource

__all__ = [
    # Base
    "BaseResource",
    "AsyncBaseResource",
    # Records
    "RecordsResource",
    "AsyncRecordsResource",
    # Analytics
    "AnalyticsResource",
    "AsyncAnalyticsResource",
    # Users
    "UsersResource",
    "AsyncUsersResource",
    # Admin
    "AdminResource",
    "AsyncAdminResource",
    # Compliance
    "ComplianceResource",
    "AsyncComplianceResource",
    # Webhooks
    "WebhooksResource",
    "AsyncWebhooksResource",
]
