"""Bulk image generator: takes a YAML of full Gemini prompts and runs each.

Unlike `image_gen.py`, this skips the Claude brief step. Each prompt's
`full_prompt` is sent directly to Gemini, with the product image attached
as reference image #1 (per CLAUDE.md: never skip this).

Use this when you already have hand-written, fully-formed image prompts
and just want bulk generation.
"""
from __future__ import annotations

import base64
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Iterable

from google import genai
from google.genai import types

from .utils import console, require_env

MODEL = "gemini-3.1-flash-image-preview"


def load_prompts(path: Path) -> dict[str, dict]:
    import yaml  # type: ignore
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must be a top-level mapping of prompt_id -> {{full_prompt, ...}}")
    cleaned: dict[str, dict] = {}
    for pid, entry in data.items():
        if not isinstance(entry, dict) or "full_prompt" not in entry:
            console.print(f"[yellow]skipping {pid}: no full_prompt[/yellow]")
            continue
        cleaned[pid] = entry
    return cleaned


def filter_prompts(
    prompts: dict[str, dict],
    phase: int | None,
    only: list[str] | None,
    avatar: str | None = None,
    compliance: str | None = None,
) -> dict[str, dict]:
    if only:
        missing = [o for o in only if o not in prompts]
        if missing:
            raise ValueError(f"Unknown prompt id(s): {missing}")
        return {k: v for k, v in prompts.items() if k in only}
    out = prompts
    if phase is not None:
        out = {k: v for k, v in out.items() if v.get("phase") == phase}
    if avatar:
        out = {k: v for k, v in out.items() if v.get("avatar") == avatar}
    if compliance:
        out = {k: v for k, v in out.items() if v.get("compliance") == compliance}
    return out


def build_filename(pid: str, entry: dict, variant: int) -> str:
    # If the prompt is tagged with a compliance/avatar (e.g. Skintific), use a
    # tidy id-based name; otherwise fall back to the legacy angle_template form.
    if entry.get("compliance") or entry.get("avatar"):
        if variant == 1:
            return f"{pid}.png"
        return f"{pid}_v{variant}.png"
    angle = entry.get("angle", "angle")
    template = entry.get("template", "tpl")
    date = datetime.now().strftime("%Y-%m-%d")
    return f"{angle}_{template}_v{variant}_{date}_{pid}.png"


def generate_one(
    client: genai.Client,
    prompt_text: str,
    product_bytes: bytes | None,
    product_mime: str | None,
    aspect_ratio: str,
) -> bytes | None:
    contents: list = []
    if product_bytes and product_mime:
        contents.append(types.Part.from_bytes(data=product_bytes, mime_type=product_mime))
    contents.append(prompt_text)

    resp = client.models.generate_content(
        model=MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(aspect_ratio=aspect_ratio),
        ),
    )
    for cand in resp.candidates or []:
        for part in cand.content.parts or []:
            if getattr(part, "inline_data", None) and part.inline_data.data:
                raw = part.inline_data.data
                return raw if isinstance(raw, bytes) else base64.b64decode(raw)
    return None


def run_bulk(
    prompts: dict[str, dict],
    product_image: Path | None,
    run_dir: Path,
    aspect_ratio: str = "1:1",
    variants: int = 1,
    sleep_between: float = 0.5,
) -> dict:
    client = genai.Client(api_key=require_env("GEMINI_API_KEY"))
    if product_image:
        product_bytes = product_image.read_bytes()
        product_mime = f"image/{product_image.suffix.lstrip('.').lower().replace('jpg', 'jpeg')}"
    else:
        product_bytes = None
        product_mime = None

    manifest: dict = {
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "model": MODEL,
        "aspect_ratio": aspect_ratio,
        "variants_per_prompt": variants,
        "product_image": str(product_image) if product_image else None,
        "results": [],
    }

    total = len(prompts) * variants
    done = 0
    for pid, entry in prompts.items():
        full_prompt = entry["full_prompt"]
        prompt_aspect = entry.get("aspect_ratio") or aspect_ratio
        for v in range(1, variants + 1):
            done += 1
            label = f"[{done}/{total}] {pid} v{v}"
            console.print(f"[dim]{label}…[/dim]")
            try:
                img = generate_one(client, full_prompt, product_bytes, product_mime, prompt_aspect)
            except Exception as e:
                console.print(f"  [red]✗[/red] {e}")
                manifest["results"].append({"prompt_id": pid, "variant": v, "error": str(e)})
                continue

            if not img:
                console.print(f"  [yellow]⚠[/yellow] no image returned")
                manifest["results"].append({"prompt_id": pid, "variant": v, "error": "no image"})
                continue

            fname = build_filename(pid, entry, v)
            subdir = entry.get("compliance")
            out_dir = run_dir / subdir if subdir else run_dir
            out_dir.mkdir(parents=True, exist_ok=True)
            out = out_dir / fname
            out.write_bytes(img)
            rel = str(out.relative_to(run_dir))
            console.print(f"  [green]✓[/green] {rel}")
            manifest["results"].append({"prompt_id": pid, "variant": v, "file": rel})

            if sleep_between:
                time.sleep(sleep_between)

    manifest["finished_at"] = datetime.now().isoformat(timespec="seconds")
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return manifest


def summarize(manifest: dict) -> tuple[int, int]:
    ok = sum(1 for r in manifest["results"] if "file" in r)
    fail = sum(1 for r in manifest["results"] if "error" in r)
    return ok, fail
