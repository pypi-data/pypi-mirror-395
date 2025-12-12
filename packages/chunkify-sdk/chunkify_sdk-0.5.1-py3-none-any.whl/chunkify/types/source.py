# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict
from datetime import datetime

from .._models import BaseModel

__all__ = ["Source"]


class Source(BaseModel):
    id: str
    """Unique identifier of the source"""

    audio_bitrate: int
    """Audio bitrate in bits per second"""

    audio_codec: str
    """Audio codec used"""

    created_at: datetime
    """Timestamp when the source was created"""

    device: str
    """Device used to record the video"""

    duration: int
    """Duration of the video in seconds"""

    height: int
    """Height of the video in pixels"""

    metadata: Dict[str, str]
    """Additional metadata for the source"""

    size: int
    """Size of the source file in bytes"""

    url: str
    """URL where the source video can be accessed"""

    video_bitrate: int
    """Video bitrate in bits per second"""

    video_codec: str
    """Video codec used"""

    video_framerate: float
    """Video framerate in frames per second"""

    width: int
    """Width of the video in pixels"""
