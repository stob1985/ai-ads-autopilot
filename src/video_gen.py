"""Orchestrate the Level 2 video pipeline:
brief → script → HeyGen talking photo → download mp4."""
from __future__ import annotations

import os
from pathlib import Path

from . import creative_brief, heygen
from .utils import console, creator_image, require_env


def make_video(brief: dict, run_dir: Path, talking_photo_id: str | None = None) -> Path:
    talking_photo_id = talking_photo_id or os.environ.get("HEYGEN_AVATAR_ID", "").strip()
    if not talking_photo_id:
        talking_photo_id = heygen.upload_talking_photo(creator_image())
        console.print(
            "[yellow]Tip:[/yellow] paste this into .env as HEYGEN_AVATAR_ID to skip uploading next time."
        )

    script = creative_brief.write_script(brief, run_dir)
    voice_id = os.environ.get("HEYGEN_VOICE_ID", "").strip() or None
    _ = require_env("HEYGEN_API_KEY")

    video_id = heygen.generate_video(script, talking_photo_id, voice_id=voice_id)
    url = heygen.wait_for_video(video_id)
    return heygen.download_video(url, run_dir / "video.mp4")
