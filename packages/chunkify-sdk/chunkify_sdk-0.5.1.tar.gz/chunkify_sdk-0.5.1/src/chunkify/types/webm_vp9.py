# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["WebmVp9"]


class WebmVp9(BaseModel):
    id: Literal["webm_vp9"]

    audio_bitrate: Optional[int] = None
    """
    AudioBitrate specifies the audio bitrate in bits per second. Must be between
    32Kbps and 512Kbps.
    """

    bufsize: Optional[int] = None
    """
    Bufsize specifies the video buffer size in bits. Must be between 100Kbps and
    50Mbps.
    """

    channels: Optional[Literal[1, 2, 5, 7]] = None
    """
    Channels specifies the number of audio channels. Valid values: 1 (mono), 2
    (stereo), 5 (5.1), 7 (7.1)
    """

    cpu_used: Optional[Literal["0", "1", "2", "3", "4", "5", "6", "7", "8"]] = None
    """CpuUsed specifies the CPU usage level for VP9 encoding.

    Range: 0 to 8. Lower values mean better quality but slower encoding, higher
    values mean faster encoding but lower quality. Recommended values: 0-2 for high
    quality, 2-4 for good quality, 4-6 for balanced, 6-8 for speed
    """

    crf: Optional[int] = None
    """
    Crf (Constant Rate Factor) controls the quality of the output video. Lower
    values mean better quality but larger file size. Range: 15 to 35. Recommended
    values: 18-28 for high quality, 23-28 for good quality, 28-35 for acceptable
    quality.
    """

    disable_audio: Optional[bool] = None
    """DisableAudio indicates whether to disable audio processing."""

    disable_video: Optional[bool] = None
    """DisableVideo indicates whether to disable video processing."""

    duration: Optional[int] = None
    """
    Duration specifies the duration to process in seconds. Must be a positive value.
    """

    framerate: Optional[float] = None
    """
    Framerate specifies the output video frame rate. Must be between 15 and 120 fps.
    """

    gop: Optional[int] = None
    """Gop specifies the Group of Pictures (GOP) size. Must be between 1 and 300."""

    height: Optional[int] = None
    """Height specifies the output video height in pixels. Must be between -2 and 7680.

    Use -2 for automatic calculation while maintaining aspect ratio.
    """

    maxrate: Optional[int] = None
    """
    Maxrate specifies the maximum video bitrate in bits per second. Must be between
    100Kbps and 50Mbps.
    """

    minrate: Optional[int] = None
    """
    Minrate specifies the minimum video bitrate in bits per second. Must be between
    100Kbps and 50Mbps.
    """

    pixfmt: Optional[
        Literal[
            "yuv410p",
            "yuv411p",
            "yuv420p",
            "yuv422p",
            "yuv440p",
            "yuv444p",
            "yuvJ411p",
            "yuvJ420p",
            "yuvJ422p",
            "yuvJ440p",
            "yuvJ444p",
            "yuv420p10le",
            "yuv422p10le",
            "yuv440p10le",
            "yuv444p10le",
            "yuv420p12le",
            "yuv422p12le",
            "yuv440p12le",
            "yuv444p12le",
            "yuv420p10be",
            "yuv422p10be",
            "yuv440p10be",
            "yuv444p10be",
            "yuv420p12be",
            "yuv422p12be",
            "yuv440p12be",
            "yuv444p12be",
        ]
    ] = None
    """PixFmt specifies the pixel format. Valid value: yuv420p"""

    quality: Optional[Literal["good", "best", "realtime"]] = None
    """Quality specifies the VP9 encoding quality preset. Valid values:

    - good: Balanced quality preset, good for most applications
    - best: Best quality preset, slower encoding
    - realtime: Fast encoding preset, suitable for live streaming
    """

    seek: Optional[int] = None
    """
    Seek specifies the timestamp to start processing from (in seconds). Must be a
    positive value.
    """

    video_bitrate: Optional[int] = None
    """
    VideoBitrate specifies the video bitrate in bits per second. Must be between
    100Kbps and 50Mbps.
    """

    width: Optional[int] = None
    """Width specifies the output video width in pixels. Must be between -2 and 7680.

    Use -2 for automatic calculation while maintaining aspect ratio.
    """
