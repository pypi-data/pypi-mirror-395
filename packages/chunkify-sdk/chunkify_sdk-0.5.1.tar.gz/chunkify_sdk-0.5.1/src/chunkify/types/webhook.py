# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["Webhook"]


class Webhook(BaseModel):
    id: str
    """Unique identifier of the webhook"""

    enabled: bool
    """Whether the webhook is currently enabled"""

    events: List[
        Literal["job.completed", "job.failed", "job.cancelled", "upload.completed", "upload.failed", "upload.expired"]
    ]
    """Array of event types this webhook subscribes to"""

    project_id: str
    """ID of the project this webhook belongs to"""

    url: str
    """URL where webhook events will be sent"""
