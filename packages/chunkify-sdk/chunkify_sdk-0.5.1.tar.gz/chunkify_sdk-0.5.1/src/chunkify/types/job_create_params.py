# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .jpg_param import JpgParam
from .hls_av1_param import HlsAv1Param
from .mp4_av1_param import MP4Av1Param
from .hls_h264_param import HlsH264Param
from .hls_h265_param import HlsH265Param
from .mp4_h264_param import MP4H264Param
from .mp4_h265_param import MP4H265Param
from .webm_vp9_param import WebmVp9Param

__all__ = ["JobCreateParams", "Format", "Storage", "Transcoder"]


class JobCreateParams(TypedDict, total=False):
    format: Required[Format]
    """
    Required format configuration, one and only one valid format configuration must
    be provided. If you want to use a format without specifying any configuration,
    use an empty object in the corresponding field.
    """

    source_id: Required[str]
    """The ID of the source file to transcode"""

    hls_manifest_id: str
    """
    Optional HLS manifest configuration Use the same hls manifest ID to group
    multiple jobs into a single HLS manifest By default, it's automatically
    generated if no set for HLS jobs
    """

    metadata: Dict[str, str]
    """Optional metadata to attach to the job (max 1024 bytes)"""

    storage: Storage
    """Optional storage configuration"""

    transcoder: Transcoder
    """Optional transcoder configuration.

    If not provided, the system will automatically calculate the optimal quantity
    and CPU type based on the source file specifications and output requirements.
    This auto-scaling ensures efficient resource utilization.
    """


Format: TypeAlias = Union[
    MP4Av1Param, MP4H264Param, MP4H265Param, WebmVp9Param, HlsAv1Param, HlsH264Param, HlsH265Param, JpgParam
]


class Storage(TypedDict, total=False):
    id: str
    """
    Storage Id specifies the storage configuration to use from pre-configured
    storage options. Must be 4-64 characters long and contain only alphanumeric
    characters, underscores and hyphens. Optional if Storage Path is provided.
    """

    path: str
    """
    Storage Path specifies a custom storage path where processed files will be
    stored. Must be a valid file path with max length of 1024 characters. Optional
    if Storage Id is provided.
    """


class Transcoder(TypedDict, total=False):
    quantity: int
    """Quantity specifies the number of transcoder instances. Required if Type is set."""

    type: Literal["4vCPU", "8vCPU", "16vCPU"]
    """
    Type specifies the CPU configuration for each transcoder instance. Required if
    Quantity is set.
    """
