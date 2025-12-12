# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["HlsAv1Param"]


class HlsAv1Param(TypedDict, total=False):
    id: Required[Literal["hls_av1"]]

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

    crf: int
    """
    Crf (Constant Rate Factor) controls the quality of the output video. Lower
    values mean better quality but larger file size. Range: 16 to 63. Recommended
    values: 16-35 for high quality, 35-45 for good quality, 45-63 for acceptable
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

    hls_enc: bool
    """HlsEnc enables encryption for HLS segments when set to true."""

    hls_enc_iv: str
    """HlsEncIv specifies the initialization vector for encryption.

    Maximum length: 64 characters. Required when HlsEnc is true.
    """

    hls_enc_key: str
    """HlsEncKey specifies the encryption key for HLS segments.

    Maximum length: 64 characters. Required when HlsEnc is true.
    """

    hls_enc_key_url: str
    """
    HlsEncKeyUrl specifies the URL where clients can fetch the encryption key.
    Required when HlsEnc is true.
    """

    hls_segment_type: Literal["mpegts", "fmp4"]
    """HlsSegmentType specifies the type of HLS segments. Valid values:

    - mpegts: Traditional MPEG-TS segments, better compatibility
    - fmp4: Fragmented MP4 segments, better efficiency
    """

    hls_time: int
    """HlsTime specifies the duration of each HLS segment in seconds.

    Range: 1 to 10. Shorter segments provide faster startup but more overhead,
    longer segments are more efficient.
    """

    level: Literal[30, 31, 41]
    """Level specifies the AV1 profile level.

    Valid values: 30-31 (main), 41 (main10). Higher levels support higher
    resolutions and bitrates but require more processing power.
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

    movflags: str

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

    preset: Literal["6", "7", "8", "9", "10", "11", "12", "13"]
    """Preset controls the encoding efficiency and processing intensity.

    Lower presets use more optimization features, creating smaller files with better
    quality but requiring more compute time. Higher presets encode faster but
    produce larger files.

    Preset ranges:

    - 6-7: Fast encoding for real-time applications (smaller files)
    - 8-10: Balanced efficiency and speed for general use
    - 11-13: Fastest encoding for real-time applications (larger files)
    """

    profilev: Literal["main", "main10", "mainstillpicture"]
    """Profilev specifies the AV1 profile. Valid values:

    - main: Main profile, good for most applications
    - main10: Main 10-bit profile, supports 10-bit color
    - mainstillpicture: Still picture profile, optimized for single images
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
