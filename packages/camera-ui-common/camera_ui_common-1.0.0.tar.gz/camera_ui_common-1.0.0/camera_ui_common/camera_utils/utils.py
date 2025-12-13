"""Camera utility functions."""

from __future__ import annotations

from urllib.parse import urlparse

from camera_ui_python_types import RTSPUrlOptions


def build_target_url(rtsp_url: str, options: RTSPUrlOptions | None = None) -> str:
    """
    Build a target URL with streaming options.

    Args:
        rtsp_url: The base RTSP URL
        options: Optional streaming options

    Returns:
        The constructed URL with query parameters
    """
    if options is None:
        options = {}

    parsed = urlparse(rtsp_url)
    base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    # Extract options with defaults
    video = options.get("video", True)
    audio = options.get("audio", True)
    audio_single_track = options.get("audioSingleTrack", True)
    backchannel = options.get("backchannel", False)
    timeout = options.get("timeout", 15)
    gop = options.get("gop", True)
    prebuffer = options.get("prebuffer", False)

    # Validate timeout (5-30 seconds)
    validated_timeout = min(max(5, timeout), 30)

    params: list[str] = []

    # Video parameter
    if video:
        params.append("video")

    # Audio parameter
    if audio:
        if isinstance(audio, bool):
            params.append("audio")
        elif isinstance(audio, list):
            if audio_single_track:
                # Single track with multiple codecs
                params.append(f"audio={','.join(audio)}")
            else:
                # Multiple tracks
                for codec in audio:
                    params.append(f"audio={codec}")
        else:
            params.append(f"audio={audio}")

    # Backchannel parameter
    if backchannel:
        params.append("backchannel=1")

    # GOP parameter
    if gop:
        params.append("gop=1")

    # Prebuffer parameter
    if prebuffer:
        params.append("prebuffer=5")

    # Timeout parameter
    params.append(f"timeout={validated_timeout}")

    return f"{base_url}?{'&'.join(params)}"
