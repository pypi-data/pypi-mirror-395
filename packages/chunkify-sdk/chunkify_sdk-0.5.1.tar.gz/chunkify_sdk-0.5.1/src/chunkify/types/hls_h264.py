# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["HlsH264"]


class HlsH264(BaseModel):
    id: Literal["hls_h264"]

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

    crf: Optional[int] = None
    """
    Crf (Constant Rate Factor) controls the quality of the output video. Lower
    values mean better quality but larger file size. Range: 16 to 35. Recommended
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

    hls_enc: Optional[bool] = None
    """HlsEnc enables encryption for HLS segments when set to true."""

    hls_enc_iv: Optional[str] = None
    """HlsEncIv specifies the initialization vector for encryption.

    Maximum length: 64 characters. Required when HlsEnc is true.
    """

    hls_enc_key: Optional[str] = None
    """HlsEncKey specifies the encryption key for HLS segments.

    Maximum length: 64 characters. Required when HlsEnc is true.
    """

    hls_enc_key_url: Optional[str] = None
    """
    HlsEncKeyUrl specifies the URL where clients can fetch the encryption key.
    Required when HlsEnc is true.
    """

    hls_segment_type: Optional[Literal["mpegts", "fmp4"]] = None
    """HlsSegmentType specifies the type of HLS segments. Valid values:

    - mpegts: Traditional MPEG-TS segments, better compatibility
    - fmp4: Fragmented MP4 segments, better efficiency
    """

    hls_time: Optional[int] = None
    """HlsTime specifies the duration of each HLS segment in seconds.

    Range: 1 to 10. Shorter segments provide faster startup but more overhead,
    longer segments are more efficient.
    """

    level: Optional[Literal[10, 11, 12, 13, 20, 21, 22, 30, 31, 32, 40, 41, 42, 50, 51]] = None
    """Level specifies the H.264 profile level.

    Valid values: 10-13 (baseline), 20-22 (main), 30-32 (high), 40-42 (high), 50-51
    (high). Higher levels support higher resolutions and bitrates but require more
    processing power.
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

    movflags: Optional[str] = None

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

    preset: Optional[Literal["ultrafast", "superfast", "veryfast", "faster", "fast", "medium"]] = None
    """Preset specifies the encoding speed preset.

    Valid values (from fastest to slowest):

    - ultrafast: Fastest encoding, lowest quality
    - superfast: Very fast encoding, lower quality
    - veryfast: Fast encoding, moderate quality
    - faster: Faster encoding, good quality
    - fast: Fast encoding, better quality
    - medium: Balanced preset, best quality
    """

    profilev: Optional[Literal["baseline", "main", "high", "high10", "high422", "high444"]] = None
    """Profilev specifies the H.264 profile. Valid values:

    - baseline: Basic profile, good for mobile devices
    - main: Main profile, good for most applications
    - high: High profile, best quality but requires more processing
    - high10: High 10-bit profile, supports 10-bit color
    - high422: High 4:2:2 profile, supports 4:2:2 color sampling
    - high444: High 4:4:4 profile, supports 4:4:4 color sampling
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

    x264_keyint: Optional[int] = None
    """
    X264KeyInt specifies the maximum number of frames between keyframes for H.264
    encoding. Range: 1 to 300. Higher values can improve compression but may affect
    seeking.
    """
