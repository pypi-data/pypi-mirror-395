"""Streaming types and URL structures."""

from __future__ import annotations

from typing import NotRequired, TypedDict

from .types import (
    AudioCodec,
    AudioFFmpegCodec,
    DecoderFormat,
    ImageInputFormat,
    ProbeAudioCodec,
    RTSPAudioCodec,
    VideoCodec,
    VideoFFmpegCodec,
)


class Go2RtcWSSource(TypedDict):
    """Go2RTC WebSocket source URLs."""

    webrtc: str
    mse: str


class Go2RtcRTSPSource(TypedDict):
    """Go2RTC RTSP source URLs."""

    base: str
    default: str
    muted: str
    aac: str
    opus: str
    pcma: str
    onvif: str
    prebuffered: str


class Go2RtcSnapshotSource(TypedDict):
    """Go2RTC snapshot source URLs."""

    mp4: str
    jpeg: str
    mjpeg: str


class StreamUrls(TypedDict):
    """Stream URLs for a camera source."""

    ws: Go2RtcWSSource
    rtsp: Go2RtcRTSPSource
    snapshot: Go2RtcSnapshotSource


class ProbeConfig(TypedDict, total=False):
    """Probe configuration for stream discovery."""

    video: bool
    audio: bool | str | list[ProbeAudioCodec]  # 'all' | ProbeAudioCodec[]
    microphone: bool


class FMTPInfo(TypedDict):
    """FMTP (Format Parameters) information."""

    payload: int
    config: str


class AudioCodecProperties(TypedDict):
    """Audio codec properties."""

    sampleRate: int
    channels: int
    payloadType: int
    fmtpInfo: NotRequired[FMTPInfo]


class VideoCodecProperties(TypedDict):
    """Video codec properties."""

    clockRate: int
    payloadType: int
    fmtpInfo: NotRequired[FMTPInfo]


class AudioStreamInfo(TypedDict):
    """Audio stream information from probing."""

    codec: AudioCodec
    ffmpegCodec: AudioFFmpegCodec
    properties: AudioCodecProperties
    direction: str  # 'sendonly' | 'recvonly' | 'sendrecv' | 'inactive'


class VideoStreamInfo(TypedDict):
    """Video stream information from probing."""

    codec: VideoCodec
    ffmpegCodec: VideoFFmpegCodec
    properties: VideoCodecProperties
    direction: str  # 'sendonly' | 'recvonly' | 'sendrecv' | 'inactive'


class ProbeStream(TypedDict):
    """Probed stream information."""

    sdp: str
    audio: list[AudioStreamInfo]
    video: list[VideoStreamInfo]


class RTSPUrlOptions(TypedDict, total=False):
    """RTSP URL generation options."""

    video: bool
    audio: bool | RTSPAudioCodec | list[RTSPAudioCodec]
    gop: bool
    prebuffer: bool
    audioSingleTrack: bool
    backchannel: bool
    timeout: int


# Frame types (relevant for Python plugins)


class FrameMetadata(TypedDict):
    """Frame metadata from decoder."""

    format: DecoderFormat
    frameSize: int
    width: int
    height: int
    origWidth: int
    origHeight: int


class ImageInformation(TypedDict):
    """Image information."""

    width: int
    height: int
    channels: int
    format: ImageInputFormat


class FrameData(TypedDict):
    """Frame data from decoder."""

    id: str
    data: bytes
    timestamp: int
    metadata: FrameMetadata
    info: ImageInformation


class ImageCrop(TypedDict):
    """Image crop settings."""

    top: int
    left: int
    width: int
    height: int


class ImageResize(TypedDict):
    """Image resize settings."""

    width: int
    height: int


class ImageFormat(TypedDict):
    """Image format conversion settings."""

    to: str  # ImageOutputFormat


class ImageOptions(TypedDict, total=False):
    """Image processing options."""

    format: ImageFormat
    crop: ImageCrop
    resize: ImageResize


class FrameBuffer(TypedDict):
    """Frame buffer with image data."""

    image: bytes
    info: ImageInformation


class IceServer(TypedDict, total=False):
    """ICE server for WebRTC."""

    urls: list[str]
    username: str
    credential: str
