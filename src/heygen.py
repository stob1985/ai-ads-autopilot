"""HeyGen API client — photo avatar + video generate.

Docs: https://docs.heygen.com/reference
"""
from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import requests

from .utils import console, require_env

API_BASE = "https://api.heygen.com"
UPLOAD_BASE = "https://upload.heygen.com"
DEFAULT_VOICE_ID = "1bd001e7e50f421d891986aad5158bc8"  # generic male-US; override in .env


def _headers() -> dict[str, str]:
    return {"X-Api-Key": require_env("HEYGEN_API_KEY"), "Content-Type": "application/json"}


def upload_talking_photo(image_path: Path) -> str:
    """Upload a face photo and return a talking_photo_id."""
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}[
        image_path.suffix.lstrip(".").lower()
    ]
    console.print(f"[dim]Uploading creator photo to HeyGen ({image_path.name})…[/dim]")
    resp = requests.post(
        f"{UPLOAD_BASE}/v1/talking_photo",
        headers={"X-Api-Key": require_env("HEYGEN_API_KEY"), "Content-Type": mime},
        data=image_path.read_bytes(),
        timeout=120,
    )
    resp.raise_for_status()
    data = resp.json()
    tid = data.get("data", {}).get("talking_photo_id") or data.get("talking_photo_id")
    if not tid:
        raise RuntimeError(f"HeyGen upload returned no talking_photo_id: {data}")
    console.print(f"[green]✓[/green] talking_photo_id: {tid}")
    return tid


def generate_video(
    script: str,
    talking_photo_id: str,
    voice_id: str | None = None,
    width: int = 720,
    height: int = 1280,  # vertical for social
    background_color: str = "#000000",
) -> str:
    """Kick off a video generation. Returns video_id."""
    payload: dict[str, Any] = {
        "video_inputs": [
            {
                "character": {
                    "type": "talking_photo",
                    "talking_photo_id": talking_photo_id,
                    "talking_photo_style": "square",
                    "scale": 1.0,
                },
                "voice": {
                    "type": "text",
                    "input_text": script,
                    "voice_id": voice_id or DEFAULT_VOICE_ID,
                },
                "background": {"type": "color", "value": background_color},
            }
        ],
        "dimension": {"width": width, "height": height},
    }
    resp = requests.post(f"{API_BASE}/v2/video/generate", headers=_headers(), json=payload, timeout=60)
    resp.raise_for_status()
    body = resp.json()
    vid = body.get("data", {}).get("video_id") or body.get("video_id")
    if not vid:
        raise RuntimeError(f"HeyGen generate returned no video_id: {body}")
    console.print(f"[dim]HeyGen job queued — video_id={vid}[/dim]")
    return vid


def wait_for_video(video_id: str, poll_seconds: int = 10, timeout_seconds: int = 900) -> str:
    """Poll until the video is ready. Returns the download URL."""
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        resp = requests.get(
            f"{API_BASE}/v1/video_status.get",
            params={"video_id": video_id},
            headers={"X-Api-Key": require_env("HEYGEN_API_KEY")},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json().get("data", {})
        status = data.get("status")
        if status == "completed":
            url = data.get("video_url")
            if not url:
                raise RuntimeError(f"HeyGen completed but no video_url: {data}")
            return url
        if status == "failed":
            raise RuntimeError(f"HeyGen video failed: {data.get('error')}")
        console.print(f"[dim]  status={status}… waiting {poll_seconds}s[/dim]")
        time.sleep(poll_seconds)
    raise TimeoutError(f"HeyGen video {video_id} did not finish within {timeout_seconds}s")


def download_video(url: str, out_path: Path) -> Path:
    console.print(f"[dim]Downloading mp4 to {out_path.name}…[/dim]")
    resp = requests.get(url, stream=True, timeout=300)
    resp.raise_for_status()
    with out_path.open("wb") as f:
        for chunk in resp.iter_content(chunk_size=1 << 15):
            if chunk:
                f.write(chunk)
    return out_path
