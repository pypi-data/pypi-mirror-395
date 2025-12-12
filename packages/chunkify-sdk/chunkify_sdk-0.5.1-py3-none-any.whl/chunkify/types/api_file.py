# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime

from .._models import BaseModel

__all__ = ["APIFile"]


class APIFile(BaseModel):
    id: str
    """Unique identifier of the file"""

    audio_bitrate: int
    """Audio bitrate in bits per second"""

    audio_codec: str
    """Audio codec used"""

    created_at: datetime
    """Timestamp when the file was created"""

    duration: int
    """Duration of the video in seconds"""

    height: int
    """Height of the video in pixels"""

    job_id: str
    """ID of the job that created this file"""

    mime_type: str
    """MIME type of the file"""

    path: str
    """Path to the file in storage"""

    size: int
    """Size of the file in bytes"""

    storage_id: str
    """StorageId identifier where the file is stored"""

    url: str
    """Pre-signed URL to directly access the file (only included when available)"""

    video_bitrate: int
    """Video bitrate in bits per second"""

    video_codec: str
    """Video codec used"""

    video_framerate: float
    """Video framerate in frames per second"""

    width: int
    """Width of the video in pixels"""
