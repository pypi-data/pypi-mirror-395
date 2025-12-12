# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["JpgParam"]


class JpgParam(TypedDict, total=False):
    id: Required[Literal["jpg"]]

    interval: Required[int]
    """
    Time interval in seconds at which frames are extracted from the video (e.g.,
    interval=10 extracts frames at 0s, 10s, 20s, etc.). Must be between 1 and 60
    seconds.
    """

    chunk_duration: int

    duration: int
    """
    Duration specifies the duration to process in seconds. Must be a positive value.
    """

    frames: int

    height: int

    seek: int
    """
    Seek specifies the timestamp to start processing from (in seconds). Must be a
    positive value.
    """

    sprite: bool

    width: int
