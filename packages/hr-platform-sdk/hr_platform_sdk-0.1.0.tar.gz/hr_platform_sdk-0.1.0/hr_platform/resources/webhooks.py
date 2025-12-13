"""Webhooks resource.

API resource for webhook subscription management.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from hr_platform.models.webhooks import (
    CreateWebhookRequest,
    CreateWebhookResponse,
    RetryDeliveryResponse,
    RevokeWebhookRequest,
    RevokeWebhookResponse,
    TestWebhookResponse,
    UpdateWebhookRequest,
    UpdateWebhookResponse,
    Webhook,
    WebhookDeliveriesResponse,
    WebhookEventTypesResponse,
    WebhooksListResponse,
)
from hr_platform.resources.base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from hr_platform.core.async_http import AsyncHttpClient
    from hr_platform.core.http import HttpClient


class WebhooksResource(BaseResource):
    """Synchronous webhooks API resource.

    Provides methods for webhook subscription management.

    Example:
        >>> webhooks = client.webhooks.list()
        >>> event_types = client.webhooks.get_event_types()
        >>> webhook = client.webhooks.create(CreateWebhookRequest(...))
    """

    def __init__(self, client: "HttpClient") -> None:
        """Initialize webhooks resource.

        Args:
            client: HTTP client instance.
        """
        super().__init__(client)

    def list(self) -> WebhooksListResponse:
        """List all webhook subscriptions.

        Returns:
            Response containing webhooks list.

        Example:
            >>> response = client.webhooks.list()
            >>> for webhook in response.webhooks:
            ...     print(f"{webhook.name}: {webhook.url}")
        """
        data = self._get("/webhooks")
        return WebhooksListResponse.model_validate(data)

    def get(self, webhook_id: str) -> Webhook:
        """Get a single webhook by ID.

        Args:
            webhook_id: UUID of the webhook.

        Returns:
            Webhook subscription details.

        Raises:
            NotFoundError: If webhook doesn't exist.

        Example:
            >>> webhook = client.webhooks.get("webhook-uuid")
            >>> print(f"Events: {webhook.events}")
        """
        data = self._get(f"/webhooks/{webhook_id}")
        return Webhook.model_validate(data)

    def create(self, request: CreateWebhookRequest) -> CreateWebhookResponse:
        """Create a new webhook subscription.

        IMPORTANT: The plain text secret is returned ONLY at creation time.
        Store it securely immediately for signature verification.

        Args:
            request: Webhook creation request.

        Returns:
            Response with webhook details and plain text secret.

        Example:
            >>> from hr_platform.models import CreateWebhookRequest
            >>> response = client.webhooks.create(CreateWebhookRequest(
            ...     name="D365 Integration",
            ...     url="https://your-endpoint.com/webhook",
            ...     events=["record.*", "workflow.*"],
            ...     api_key_id="key-uuid",  # Optional for entity scoping
            ... ))
            >>> print(f"Secret: {response.plain_text_secret}")
            >>> print(response.warning)
        """
        data = self._post(
            "/webhooks",
            data=request.model_dump(by_alias=True, exclude_none=True),
        )
        return CreateWebhookResponse.model_validate(data)

    def update(
        self, webhook_id: str, request: UpdateWebhookRequest
    ) -> UpdateWebhookResponse:
        """Update a webhook subscription.

        Args:
            webhook_id: UUID of the webhook to update.
            request: Update request with fields to change.

        Returns:
            Response with updated webhook.

        Raises:
            NotFoundError: If webhook doesn't exist.

        Example:
            >>> from hr_platform.models import UpdateWebhookRequest
            >>> response = client.webhooks.update(
            ...     "webhook-uuid",
            ...     UpdateWebhookRequest(enabled=False)
            ... )
        """
        data = self._put(
            f"/webhooks/{webhook_id}",
            data=request.model_dump(by_alias=True, exclude_none=True),
        )
        return UpdateWebhookResponse.model_validate(data)

    def delete(
        self, webhook_id: str, reason: str | None = None
    ) -> RevokeWebhookResponse:
        """Revoke a webhook subscription.

        Args:
            webhook_id: UUID of the webhook.
            reason: Optional revocation reason.

        Returns:
            Response confirming revocation.

        Example:
            >>> response = client.webhooks.delete(
            ...     "webhook-uuid",
            ...     reason="No longer needed"
            ... )
        """
        request = RevokeWebhookRequest(reason=reason) if reason else None
        data = self._delete(
            f"/webhooks/{webhook_id}",
            params=request.model_dump(by_alias=True, exclude_none=True) if request else None,
        )
        return RevokeWebhookResponse.model_validate(data)

    def test(self, webhook_id: str) -> TestWebhookResponse:
        """Send a test event to a webhook.

        Args:
            webhook_id: UUID of the webhook.

        Returns:
            Response with test result.

        Example:
            >>> response = client.webhooks.test("webhook-uuid")
            >>> if response.success:
            ...     print(f"Delivery ID: {response.delivery_id}")
        """
        data = self._post(f"/webhooks/{webhook_id}/test")
        return TestWebhookResponse.model_validate(data)

    def get_delivery_history(
        self,
        webhook_id: str,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> WebhookDeliveriesResponse:
        """Get delivery history for a webhook.

        Args:
            webhook_id: UUID of the webhook.
            limit: Maximum results to return (default: 50).
            offset: Number of results to skip.

        Returns:
            Response with delivery attempts.

        Example:
            >>> history = client.webhooks.get_delivery_history(
            ...     "webhook-uuid",
            ...     limit=100
            ... )
            >>> for delivery in history.deliveries:
            ...     print(f"{delivery.event_type}: {delivery.status}")
        """
        params = {"limit": str(limit), "offset": str(offset)}
        data = self._get(f"/webhooks/{webhook_id}/deliveries", params=params)
        return WebhookDeliveriesResponse.model_validate(data)

    def retry_delivery(
        self, webhook_id: str, delivery_id: str
    ) -> RetryDeliveryResponse:
        """Manually retry a failed delivery.

        Args:
            webhook_id: UUID of the webhook.
            delivery_id: UUID of the delivery to retry.

        Returns:
            Response confirming retry was queued.

        Example:
            >>> response = client.webhooks.retry_delivery(
            ...     "webhook-uuid",
            ...     "delivery-uuid"
            ... )
            >>> print(response.message)
        """
        data = self._post(f"/webhooks/{webhook_id}/deliveries/{delivery_id}/retry")
        return RetryDeliveryResponse.model_validate(data)

    def get_event_types(self) -> WebhookEventTypesResponse:
        """Get available webhook event types.

        Returns:
            Response with available event types and patterns.

        Example:
            >>> response = client.webhooks.get_event_types()
            >>> for event_type in response.event_types:
            ...     print(f"{event_type.event_type}: {event_type.description}")
        """
        data = self._get("/webhooks/events")
        return WebhookEventTypesResponse.model_validate(data)


class AsyncWebhooksResource(AsyncBaseResource):
    """Asynchronous webhooks API resource.

    Provides async methods for webhook subscription management.

    Example:
        >>> webhooks = await client.webhooks.list()
        >>> event_types = await client.webhooks.get_event_types()
    """

    def __init__(self, client: "AsyncHttpClient") -> None:
        """Initialize async webhooks resource.

        Args:
            client: Async HTTP client instance.
        """
        super().__init__(client)

    async def list(self) -> WebhooksListResponse:
        """List all webhook subscriptions."""
        data = await self._get("/webhooks")
        return WebhooksListResponse.model_validate(data)

    async def get(self, webhook_id: str) -> Webhook:
        """Get a single webhook by ID."""
        data = await self._get(f"/webhooks/{webhook_id}")
        return Webhook.model_validate(data)

    async def create(self, request: CreateWebhookRequest) -> CreateWebhookResponse:
        """Create a new webhook subscription."""
        data = await self._post(
            "/webhooks",
            data=request.model_dump(by_alias=True, exclude_none=True),
        )
        return CreateWebhookResponse.model_validate(data)

    async def update(
        self, webhook_id: str, request: UpdateWebhookRequest
    ) -> UpdateWebhookResponse:
        """Update a webhook subscription."""
        data = await self._put(
            f"/webhooks/{webhook_id}",
            data=request.model_dump(by_alias=True, exclude_none=True),
        )
        return UpdateWebhookResponse.model_validate(data)

    async def delete(
        self, webhook_id: str, reason: str | None = None
    ) -> RevokeWebhookResponse:
        """Revoke a webhook subscription."""
        request = RevokeWebhookRequest(reason=reason) if reason else None
        data = await self._delete(
            f"/webhooks/{webhook_id}",
            params=request.model_dump(by_alias=True, exclude_none=True) if request else None,
        )
        return RevokeWebhookResponse.model_validate(data)

    async def test(self, webhook_id: str) -> TestWebhookResponse:
        """Send a test event to a webhook."""
        data = await self._post(f"/webhooks/{webhook_id}/test")
        return TestWebhookResponse.model_validate(data)

    async def get_delivery_history(
        self,
        webhook_id: str,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> WebhookDeliveriesResponse:
        """Get delivery history for a webhook."""
        params = {"limit": str(limit), "offset": str(offset)}
        data = await self._get(f"/webhooks/{webhook_id}/deliveries", params=params)
        return WebhookDeliveriesResponse.model_validate(data)

    async def retry_delivery(
        self, webhook_id: str, delivery_id: str
    ) -> RetryDeliveryResponse:
        """Manually retry a failed delivery."""
        data = await self._post(f"/webhooks/{webhook_id}/deliveries/{delivery_id}/retry")
        return RetryDeliveryResponse.model_validate(data)

    async def get_event_types(self) -> WebhookEventTypesResponse:
        """Get available webhook event types."""
        data = await self._get("/webhooks/events")
        return WebhookEventTypesResponse.model_validate(data)
