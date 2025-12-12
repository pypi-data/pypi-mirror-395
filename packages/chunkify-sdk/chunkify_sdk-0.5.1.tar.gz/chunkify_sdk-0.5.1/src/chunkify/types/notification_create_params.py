# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["NotificationCreateParams"]


class NotificationCreateParams(TypedDict, total=False):
    event: Required[
        Literal["job.completed", "job.failed", "job.cancelled", "upload.completed", "upload.failed", "upload.expired"]
    ]
    """Event specifies the type of event that triggered the notification."""

    object_id: Required[str]
    """ObjectId specifies the object that triggered this notification."""

    webhook_id: Required[str]
    """WebhookId specifies the webhook endpoint that will receive the notification."""
