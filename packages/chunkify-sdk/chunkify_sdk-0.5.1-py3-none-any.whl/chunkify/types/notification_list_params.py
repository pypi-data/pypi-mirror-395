# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, TypedDict

__all__ = ["NotificationListParams", "Created", "ResponseStatusCode"]


class NotificationListParams(TypedDict, total=False):
    created: Created

    events: List[
        Literal["job.completed", "job.failed", "job.cancelled", "upload.completed", "upload.failed", "upload.expired"]
    ]
    """Filter by events"""

    limit: int
    """Pagination limit (max 100)"""

    object_id: str
    """Filter by object ID"""

    offset: int
    """Pagination offset"""

    response_status_code: ResponseStatusCode

    webhook_id: str
    """Filter by webhook ID"""


class Created(TypedDict, total=False):
    gte: int
    """Filter by creation date greater than or equal (UNIX epoch time)"""

    lte: int
    """Filter by creation date less than or equal (UNIX epoch time)"""

    sort: Literal["asc", "desc"]
    """Sort by creation date (asc/desc)"""


class ResponseStatusCode(TypedDict, total=False):
    eq: int
    """Filter by exact response status code"""

    gte: int
    """Filter by response status code greater than or equal"""

    lte: int
    """Filter by response status code less than or equal"""
