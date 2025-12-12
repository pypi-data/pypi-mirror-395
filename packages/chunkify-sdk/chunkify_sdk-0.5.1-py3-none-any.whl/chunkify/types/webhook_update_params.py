# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, TypedDict

__all__ = ["WebhookUpdateParams"]


class WebhookUpdateParams(TypedDict, total=False):
    enabled: bool
    """Enabled indicates whether the webhook should be enabled or disabled."""

    events: List[
        Literal["job.completed", "job.failed", "job.cancelled", "upload.completed", "upload.failed", "upload.expired"]
    ]
    """Events specifies the types of events that will trigger the webhook."""
