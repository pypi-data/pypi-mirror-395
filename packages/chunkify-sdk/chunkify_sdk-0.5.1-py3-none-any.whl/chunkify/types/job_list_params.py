# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, TypedDict

from .._types import SequenceNotStr

__all__ = ["JobListParams", "Created"]


class JobListParams(TypedDict, total=False):
    id: str
    """Filter by job ID"""

    created: Created

    format_id: Literal["mp4_h264", "mp4_h265", "mp4_av1", "webm_vp9", "hls_h264", "hls_h265", "hls_av1", "jpg"]
    """Filter by format id"""

    hls_manifest_id: str
    """Filter by hls manifest ID"""

    limit: int
    """Pagination limit"""

    metadata: Iterable[SequenceNotStr[str]]
    """Filter by metadata"""

    offset: int
    """Pagination offset"""

    source_id: str
    """Filter by source ID"""

    status: Literal["completed", "processing", "failed", "cancelled", "queued"]
    """Filter by job status"""


class Created(TypedDict, total=False):
    gte: int
    """Filter by creation date greater than or equal"""

    lte: int
    """Filter by creation date less than or equal"""

    sort: Literal["asc", "desc"]
    """Sort by creation date (asc/desc)"""
