"""Webhook models.

Pydantic models for webhook subscriptions and deliveries.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class WebhookEventType(BaseModel):
    """Webhook event type definition."""

    model_config = ConfigDict(populate_by_name=True)

    event_type: str = Field(alias="eventType", description="Event type identifier")
    category: str = Field(description="Event category (record, workflow, user, compliance)")
    description: str = Field(description="Event description")


class WebhookEventTypesResponse(BaseModel):
    """Response containing available event types."""

    model_config = ConfigDict(populate_by_name=True)

    event_types: list[WebhookEventType] = Field(
        alias="eventTypes", description="Available event types"
    )


class Webhook(BaseModel):
    """Webhook subscription."""

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(description="Webhook ID (UUID)")
    name: str = Field(description="Webhook name")
    url: str = Field(description="Destination URL (HTTPS)")
    events: list[str] = Field(description="Subscribed event patterns")
    enabled: bool = Field(description="Whether webhook is active")
    api_key_id: str | None = Field(
        alias="apiKeyId", default=None, description="Associated API key ID"
    )
    created_at: str = Field(alias="createdAt", description="Creation timestamp")
    updated_at: str = Field(alias="updatedAt", description="Last update timestamp")


class WebhookDelivery(BaseModel):
    """Webhook delivery attempt."""

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(description="Delivery ID (UUID)")
    webhook_id: str = Field(alias="webhookId", description="Webhook ID")
    event_id: str = Field(alias="eventId", description="Event ID")
    event_type: str = Field(alias="eventType", description="Event type")
    status: str = Field(description="Delivery status (pending, success, failed)")
    http_status: int | None = Field(
        alias="httpStatus", default=None, description="HTTP response status"
    )
    error_message: str | None = Field(
        alias="errorMessage", default=None, description="Error message if failed"
    )
    attempt_count: int = Field(alias="attemptCount", description="Number of attempts")
    next_retry_at: str | None = Field(
        alias="nextRetryAt", default=None, description="Next retry timestamp"
    )
    delivered_at: str | None = Field(
        alias="deliveredAt", default=None, description="Successful delivery timestamp"
    )
    created_at: str = Field(alias="createdAt", description="Creation timestamp")


class WebhooksListResponse(BaseModel):
    """Response containing webhooks list."""

    model_config = ConfigDict(populate_by_name=True)

    webhooks: list[Webhook] = Field(description="Webhook subscriptions")
    total: int = Field(description="Total count")


class WebhookDeliveriesResponse(BaseModel):
    """Response containing delivery history."""

    model_config = ConfigDict(populate_by_name=True)

    deliveries: list[WebhookDelivery] = Field(description="Delivery attempts")
    total: int = Field(description="Total count")
    offset: int = Field(description="Current offset")
    limit: int = Field(description="Page size")


class CreateWebhookRequest(BaseModel):
    """Request to create a webhook subscription."""

    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(min_length=1, max_length=100, description="Webhook name")
    url: str = Field(description="Destination URL (HTTPS required)")
    events: list[str] = Field(min_length=1, description="Event patterns to subscribe")
    api_key_id: str | None = Field(
        alias="apiKeyId", default=None, description="API key ID for entity scoping"
    )


class CreateWebhookResponse(BaseModel):
    """Response from creating a webhook."""

    model_config = ConfigDict(populate_by_name=True)

    message: str = Field(description="Success message")
    webhook: Webhook = Field(description="Created webhook")
    plain_text_secret: str = Field(
        alias="plainTextSecret", description="Webhook secret (shown once)"
    )
    warning: str = Field(description="Warning about storing secret")


class UpdateWebhookRequest(BaseModel):
    """Request to update a webhook subscription."""

    model_config = ConfigDict(populate_by_name=True)

    name: str | None = Field(default=None, description="Webhook name")
    url: str | None = Field(default=None, description="Destination URL")
    events: list[str] | None = Field(default=None, description="Event patterns")
    enabled: bool | None = Field(default=None, description="Enable/disable webhook")


class UpdateWebhookResponse(BaseModel):
    """Response from updating a webhook."""

    model_config = ConfigDict(populate_by_name=True)

    message: str = Field(description="Success message")
    webhook: Webhook = Field(description="Updated webhook")


class RevokeWebhookRequest(BaseModel):
    """Request to revoke a webhook subscription."""

    model_config = ConfigDict(populate_by_name=True)

    reason: str | None = Field(default=None, description="Revocation reason")


class RevokeWebhookResponse(BaseModel):
    """Response from revoking a webhook."""

    model_config = ConfigDict(populate_by_name=True)

    success: bool = Field(description="Success flag")
    message: str = Field(description="Result message")
    webhook_id: str = Field(alias="webhookId", description="Webhook ID")


class TestWebhookResponse(BaseModel):
    """Response from sending a test event."""

    model_config = ConfigDict(populate_by_name=True)

    success: bool = Field(description="Whether test was sent")
    message: str = Field(description="Result message")
    delivery_id: str | None = Field(
        alias="deliveryId", default=None, description="Delivery ID for tracking"
    )


class RetryDeliveryResponse(BaseModel):
    """Response from retrying a delivery."""

    model_config = ConfigDict(populate_by_name=True)

    success: bool = Field(description="Whether retry was queued")
    message: str = Field(description="Result message")
    delivery_id: str = Field(alias="deliveryId", description="Delivery ID")
