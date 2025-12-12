# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["WebmVp9Param"]


class WebmVp9Param(TypedDict, total=False):
    id: Required[Literal["webm_vp9"]]

    audio_bitrate: int
    """
    AudioBitrate specifies the audio bitrate in bits per second. Must be between
    32Kbps and 512Kbps.
    """

    bufsize: int
    """
    Bufsize specifies the video buffer size in bits. Must be between 100Kbps and
    50Mbps.
    """

    channels: Literal[1, 2, 5, 7]
    """
    Channels specifies the number of audio channels. Valid values: 1 (mono), 2
    (stereo), 5 (5.1), 7 (7.1)
    """

    cpu_used: Literal["0", "1", "2", "3", "4", "5", "6", "7", "8"]
    """CpuUsed specifies the CPU usage level for VP9 encoding.

    Range: 0 to 8. Lower values mean better quality but slower encoding, higher
    values mean faster encoding but lower quality. Recommended values: 0-2 for high
    quality, 2-4 for good quality, 4-6 for balanced, 6-8 for speed
    """

    crf: int
    """
    Crf (Constant Rate Factor) controls the quality of the output video. Lower
    values mean better quality but larger file size. Range: 15 to 35. Recommended
    values: 18-28 for high quality, 23-28 for good quality, 28-35 for acceptable
    quality.
    """

    disable_audio: bool
    """DisableAudio indicates whether to disable audio processing."""

    disable_video: bool
    """DisableVideo indicates whether to disable video processing."""

    duration: int
    """
    Duration specifies the duration to process in seconds. Must be a positive value.
    """

    framerate: float
    """
    Framerate specifies the output video frame rate. Must be between 15 and 120 fps.
    """

    gop: int
    """Gop specifies the Group of Pictures (GOP) size. Must be between 1 and 300."""

    height: int
    """Height specifies the output video height in pixels. Must be between -2 and 7680.

    Use -2 for automatic calculation while maintaining aspect ratio.
    """

    maxrate: int
    """
    Maxrate specifies the maximum video bitrate in bits per second. Must be between
    100Kbps and 50Mbps.
    """

    minrate: int
    """
    Minrate specifies the minimum video bitrate in bits per second. Must be between
    100Kbps and 50Mbps.
    """

    pixfmt: Literal[
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
    """PixFmt specifies the pixel format. Valid value: yuv420p"""

    quality: Literal["good", "best", "realtime"]
    """Quality specifies the VP9 encoding quality preset. Valid values:

    - good: Balanced quality preset, good for most applications
    - best: Best quality preset, slower encoding
    - realtime: Fast encoding preset, suitable for live streaming
    """

    seek: int
    """
    Seek specifies the timestamp to start processing from (in seconds). Must be a
    positive value.
    """

    video_bitrate: int
    """
    VideoBitrate specifies the video bitrate in bits per second. Must be between
    100Kbps and 50Mbps.
    """

    width: int
    """Width specifies the output video width in pixels. Must be between -2 and 7680.

    Use -2 for automatic calculation while maintaining aspect ratio.
    """
