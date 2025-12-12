# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, TypedDict

from .._types import SequenceNotStr

__all__ = ["UploadListParams", "Created"]


class UploadListParams(TypedDict, total=False):
    id: str
    """Filter by upload ID"""

    created: Created

    limit: int
    """Pagination limit (max 100)"""

    metadata: Iterable[SequenceNotStr[str]]
    """Filter by metadata"""

    offset: int
    """Pagination offset"""

    source_id: str
    """Filter by source ID"""

    status: Literal["waiting", "completed", "failed", "expired"]
    """Filter by status (pending, completed, error)"""


class Created(TypedDict, total=False):
    gte: int
    """Filter by creation date greater than or equal (UNIX epoch time)"""

    lte: int
    """Filter by creation date less than or equal (UNIX epoch time)"""

    sort: Literal["asc", "desc"]
    """Sort by creation date (asc/desc)"""
