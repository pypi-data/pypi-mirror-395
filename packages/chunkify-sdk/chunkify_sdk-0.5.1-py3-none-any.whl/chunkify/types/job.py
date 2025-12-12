# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Union, Optional
from datetime import datetime
from typing_extensions import Literal

from .jpg import Jpg
from .hls_av1 import HlsAv1
from .mp4_av1 import MP4Av1
from .._models import BaseModel
from .hls_h264 import HlsH264
from .hls_h265 import HlsH265
from .mp4_h264 import MP4H264
from .mp4_h265 import MP4H265
from .webm_vp9 import WebmVp9
from .shared.chunkify_error import ChunkifyError

__all__ = [
    "Job",
    "FormatMP4Av1",
    "FormatMP4H264",
    "FormatMP4H265",
    "FormatWebmVp9",
    "FormatHlsAv1",
    "FormatHlsH264",
    "FormatHlsH265",
    "FormatJpg",
    "Storage",
    "Transcoder",
]


class FormatMP4Av1(MP4Av1):
    id: Literal["mp4_h264", "mp4_h265", "mp4_av1", "webm_vp9", "hls_h264", "hls_h265", "hls_av1", "jpg"]  # type: ignore
    """The format ID"""


class FormatMP4H264(MP4H264):
    id: Literal["mp4_h264", "mp4_h265", "mp4_av1", "webm_vp9", "hls_h264", "hls_h265", "hls_av1", "jpg"]  # type: ignore
    """The format ID"""


class FormatMP4H265(MP4H265):
    id: Literal["mp4_h264", "mp4_h265", "mp4_av1", "webm_vp9", "hls_h264", "hls_h265", "hls_av1", "jpg"]  # type: ignore
    """The format ID"""


class FormatWebmVp9(WebmVp9):
    id: Literal["mp4_h264", "mp4_h265", "mp4_av1", "webm_vp9", "hls_h264", "hls_h265", "hls_av1", "jpg"]  # type: ignore
    """The format ID"""


class FormatHlsAv1(HlsAv1):
    id: Literal["mp4_h264", "mp4_h265", "mp4_av1", "webm_vp9", "hls_h264", "hls_h265", "hls_av1", "jpg"]  # type: ignore
    """The format ID"""


class FormatHlsH264(HlsH264):
    id: Literal["mp4_h264", "mp4_h265", "mp4_av1", "webm_vp9", "hls_h264", "hls_h265", "hls_av1", "jpg"]  # type: ignore
    """The format ID"""


class FormatHlsH265(HlsH265):
    id: Literal["mp4_h264", "mp4_h265", "mp4_av1", "webm_vp9", "hls_h264", "hls_h265", "hls_av1", "jpg"]  # type: ignore
    """The format ID"""


class FormatJpg(Jpg):
    id: Literal["mp4_h264", "mp4_h265", "mp4_av1", "webm_vp9", "hls_h264", "hls_h265", "hls_av1", "jpg"]  # type: ignore
    """The format ID"""


class Storage(BaseModel):
    id: str
    """ID of the storage"""

    path: str
    """Path where the output will be stored"""


class Transcoder(BaseModel):
    auto: bool
    """Whether the transcoder configuration is automatically set by Chunkify"""

    quantity: int
    """Number of instances allocated"""

    type: Literal["4vCPU", "8vCPU", "16vCPU"]
    """Type of transcoder instance"""


class Job(BaseModel):
    id: str
    """Unique identifier for the job"""

    billable_time: int
    """Billable time in seconds"""

    created_at: datetime
    """Creation timestamp"""

    format: Union[
        FormatMP4Av1, FormatMP4H264, FormatMP4H265, FormatWebmVp9, FormatHlsAv1, FormatHlsH264, FormatHlsH265, FormatJpg
    ]
    """A template defines the transcoding parameters and settings for a job"""

    progress: float
    """Progress percentage of the job (0-100)"""

    source_id: str
    """ID of the source video being transcoded"""

    status: Literal[
        "queued",
        "ingesting",
        "transcoding",
        "downloading",
        "merging",
        "uploading",
        "failed",
        "completed",
        "cancelled",
        "merged",
        "downloaded",
        "transcoded",
        "waiting",
    ]
    """Current status of the job"""

    storage: Storage
    """Storage settings for where the job output will be saved"""

    transcoder: Transcoder
    """The transcoder configuration for a job"""

    updated_at: datetime
    """Last update timestamp"""

    error: Optional[ChunkifyError] = None
    """Error message for the job"""

    hls_manifest_id: Optional[str] = None
    """HLS manifest ID"""

    metadata: Optional[Dict[str, str]] = None
    """Additional metadata for the job"""

    started_at: Optional[datetime] = None
    """When the job started processing"""
