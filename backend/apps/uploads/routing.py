"""Decides what happens to a file based on its extension. Lane B extends this."""

CONVERT_WITH_MARKITDOWN = {"pdf", "pptx", "docx", "xlsx", "html", "htm", "csv", "md", "txt"}
IMAGE = {"png", "jpg", "jpeg", "gif", "webp"}
AUDIO_VIDEO = {"mp3", "wav", "m4a", "mp4", "mov"}  # v2


def route_for(extension: str) -> str:
    ext = extension.lower().lstrip(".")
    if ext in CONVERT_WITH_MARKITDOWN:
        return "markitdown"
    if ext in IMAGE:
        return "image"
    if ext in AUDIO_VIDEO:
        return "audio_video"
    return "reject"
