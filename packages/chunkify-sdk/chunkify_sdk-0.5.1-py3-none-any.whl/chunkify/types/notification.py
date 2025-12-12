# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from .webhook import Webhook
from .._models import BaseModel

__all__ = ["Notification"]


class Notification(BaseModel):
    id: str
    """Unique identifier of the notification"""

    created_at: datetime
    """Timestamp when the notification was created"""

    event: Literal[
        "job.completed", "job.failed", "job.cancelled", "upload.completed", "upload.failed", "upload.expired"
    ]
    """Type of event that triggered this notification"""

    object_id: str
    """ID of the object that triggered this notification"""

    payload: str
    """JSON payload that was sent to the webhook endpoint"""

    webhook: Webhook
    """Webhook endpoint configuration that received this notification"""

    response_status_code: Optional[int] = None
    """HTTP status code received from the webhook endpoint"""
