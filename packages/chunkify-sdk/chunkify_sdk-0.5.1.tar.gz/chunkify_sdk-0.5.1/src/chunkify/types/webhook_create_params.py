# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, TypedDict

__all__ = ["WebhookCreateParams"]


class WebhookCreateParams(TypedDict, total=False):
    url: Required[str]
    """
    Url is the endpoint that will receive webhook notifications, which must be a
    valid HTTP URL.
    """

    enabled: bool
    """Enabled indicates whether the webhook is active."""

    events: List[
        Literal["job.completed", "job.failed", "job.cancelled", "upload.completed", "upload.failed", "upload.expired"]
    ]
    """Events specifies the types of events that will trigger the webhook."""
