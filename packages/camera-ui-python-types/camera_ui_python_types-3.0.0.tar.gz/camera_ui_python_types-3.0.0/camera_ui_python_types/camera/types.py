"""Camera types and type aliases."""

from __future__ import annotations

from typing import Literal

# Basic camera types
CameraType = Literal["camera", "doorbell"]
ZoneType = Literal["intersect", "contain"]
ZoneFilter = Literal["include", "exclude"]
CameraRole = Literal["high-resolution", "mid-resolution", "low-resolution", "snapshot"]
StreamingRole = Literal["high-resolution", "mid-resolution", "low-resolution"]

# Decoder and image formats
DecoderFormat = Literal["nv12"]
ImageInputFormat = Literal["nv12", "rgb", "rgba", "gray"]
ImageOutputFormat = Literal["rgb", "rgba", "gray"]

# Frame worker settings
CameraFrameWorkerDecoder = Literal["pillow", "wasm", "rust"]
CameraFrameWorkerResolution = Literal["640x480", "640x360", "320x240", "320x180"]

# Codec types
AudioCodec = Literal[
    "PCMU", "PCMA", "MPEG4-GENERIC", "opus", "G722", "MPA", "PCM", "FLAC", "ELD", "PCML", "L16"
]
AudioFFmpegCodec = Literal[
    "pcm_mulaw", "pcm_alaw", "aac", "libopus", "g722", "mp3", "pcm_s16be", "pcm_s16le", "flac"
]
VideoCodec = Literal["H264", "H265", "VP8", "VP9", "AV1", "JPEG", "RAW"]
VideoFFmpegCodec = Literal["h264", "hevc", "vp8", "vp9", "av1", "mjpeg", "rawvideo"]
RTSPAudioCodec = Literal["aac", "opus", "pcma"]
ProbeAudioCodec = Literal["aac", "opus", "pcma"]

# Hardware acceleration
HwAccelMethod = Literal[
    "auto", "cuda", "vaapi", "videotoolbox", "qsv", "rkmpp", "v4l2m2m", "opencl", "vulkan", "amf", "jetson"
]

# Python version for plugins
PythonVersion = Literal["3.9", "3.10", "3.11", "3.12"]

# Streaming mode
VideoStreamingMode = Literal["auto", "webrtc", "mse", "webrtc/tcp"]
CameraAspectRatio = Literal["16:9", "8:3", "4:3", "auto"]

# Frame types
FrameType = Literal["stream", "motion"]

# Point for detection zones
Point = tuple[float, float]
