# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["Jpg"]


class Jpg(BaseModel):
    id: Literal["jpg"]

    interval: int
    """
    Time interval in seconds at which frames are extracted from the video (e.g.,
    interval=10 extracts frames at 0s, 10s, 20s, etc.). Must be between 1 and 60
    seconds.
    """

    chunk_duration: Optional[int] = None

    duration: Optional[int] = None
    """
    Duration specifies the duration to process in seconds. Must be a positive value.
    """

    frames: Optional[int] = None

    height: Optional[int] = None

    seek: Optional[int] = None
    """
    Seek specifies the timestamp to start processing from (in seconds). Must be a
    positive value.
    """

    sprite: Optional[bool] = None

    width: Optional[int] = None
