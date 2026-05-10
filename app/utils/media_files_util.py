from mimetypes import guess_type

import subprocess, json

def get_video_duration(filepath: str) -> float:
    result = subprocess.run(
        [
            "ffprobe", "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            filepath
        ],
        capture_output=True, text=True, check=True
    )
    info = json.loads(result.stdout)
    return float(info["format"]["duration"])  # secondes, float

def get_media_kind(filepath: str) -> str:
    mime, _ = guess_type(filepath)
    if mime is None:
        return None
    if mime.startswith("image/"):
        return "image"
    if mime.startswith("video/"):
        return "video"
    if mime.startswith("audio/"):
        return "audio"
    return None

def is_image(filepath: str) -> bool:
    return get_media_kind(filepath) == "image"

def is_video(filepath: str) -> bool:
    return get_media_kind(filepath) == "video"

def is_audio(filepath: str) -> bool:
    return get_media_kind(filepath) == "audio"
    