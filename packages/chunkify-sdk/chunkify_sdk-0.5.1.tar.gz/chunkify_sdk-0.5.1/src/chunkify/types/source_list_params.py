# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, TypedDict

from .._types import SequenceNotStr

__all__ = ["SourceListParams", "Created", "Duration", "Height", "Size", "Width"]


class SourceListParams(TypedDict, total=False):
    id: str
    """Filter by source ID"""

    audio_codec: str
    """Filter by audio codec"""

    created: Created

    device: Literal["apple", "android", "unknown"]
    """Filter by device (apple/android)"""

    duration: Duration

    height: Height

    limit: int
    """Pagination limit (max 100)"""

    metadata: Iterable[SequenceNotStr[str]]
    """Filter by metadata"""

    offset: int
    """Pagination offset"""

    size: Size

    video_codec: str
    """Filter by video codec"""

    width: Width


class Created(TypedDict, total=False):
    gte: int
    """Filter by creation date greater than or equal (UNIX epoch time)"""

    lte: int
    """Filter by creation date less than or equal (UNIX epoch time)"""

    sort: Literal["asc", "desc"]
    """Sort by creation date (asc/desc)"""


class Duration(TypedDict, total=False):
    eq: float
    """Filter by exact duration"""

    gt: float
    """Filter by duration greater than"""

    gte: float
    """Filter by duration greater than or equal"""

    lt: float
    """Filter by duration less than"""

    lte: float
    """Filter by duration less than or equal"""


class Height(TypedDict, total=False):
    eq: int
    """Filter by exact height"""

    gt: int
    """Filter by height greater than"""

    gte: int
    """Filter by height greater than or equal"""

    lt: int
    """Filter by height less than"""

    lte: int
    """Filter by height less than or equal"""


class Size(TypedDict, total=False):
    eq: int
    """Filter by exact file size"""

    gt: int
    """Filter by file size greater than"""

    gte: int
    """Filter by file size greater than or equal"""

    lt: int
    """Filter by file size less than"""

    lte: int
    """Filter by file size less than or equal"""


class Width(TypedDict, total=False):
    eq: int
    """Filter by exact width"""

    gt: int
    """Filter by width greater than"""

    gte: int
    """Filter by width greater than or equal"""

    lt: int
    """Filter by width less than"""

    lte: int
    """Filter by width less than or equal"""
