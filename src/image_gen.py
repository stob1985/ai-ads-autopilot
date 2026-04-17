"""Gemini Nano Banana 2 — generates the 4 still ad creatives.

The product image is passed as reference image #1 on EVERY call so the
packaging is reproduced pixel-accurate. See the ecomm-ads skill for why.
"""
from __future__ import annotations

import base64
from pathlib import Path

from google import genai
from google.genai import types

from .utils import console, require_env, slugify

MODEL = "gemini-3.1-flash-image-preview"

PROMPT_TEMPLATE = """You are a world-class advertising art director and commercial photographer creating a bold, conceptual advertisement. High-budget campaign shoot with full set design, styling, and art direction.

REFERENCE IMAGE 1: This is the ACTUAL {product} product. You MUST reproduce this exact product packaging with photographic accuracy — match every detail of the packaging, branding, colors, text, and logos exactly as shown. Do not invent or approximate.

CONCEPT: {concept}

COLOR WORLD: {color_world}. The ENTIRE scene is drenched in this color. Background, props, lighting, wardrobe — everything exists in this color universe. The only contrast is the product packaging and the white headline text.

VISUAL DIRECTION:
{visual_direction}

CAMERA: Hasselblad medium format, 80mm f/1.7, soft diffused studio lighting that feels premium and editorial.

TEXT OVERLAY:
- Headline at the top in large bold white sans-serif (Helvetica Neue Black or Futura Bold): "{headline}"
- Subtext at the bottom in smaller lighter weight: "{subtext}"
- CTA at the bottom right in small white text: "{cta}"
- All text must be crisp, perfectly legible, spelled correctly.

LAYOUT:
- Top third: headline.
- Center: the product and the creative visual.
- Bottom: subtext + CTA.

Do NOT produce a generic stock photo or product-on-table shot. This must look like a bold, award-winning ad campaign — the kind someone screenshots and sends to a friend."""


def generate_images(product: str, briefs: list[dict], product_image: Path, run_dir: Path) -> list[Path]:
    client = genai.Client(api_key=require_env("GEMINI_API_KEY"))
    product_bytes = product_image.read_bytes()
    product_mime = f"image/{product_image.suffix.lstrip('.').lower().replace('jpg', 'jpeg')}"

    outputs: list[Path] = []
    for i, brief in enumerate(briefs, start=1):
        prompt = PROMPT_TEMPLATE.format(
            product=product,
            concept=brief.get("concept", ""),
            color_world=brief.get("color_world", ""),
            visual_direction=brief.get("visual_direction", ""),
            headline=brief.get("headline", ""),
            subtext=brief.get("subtext", ""),
            cta=brief.get("cta", ""),
        )
        console.print(f"[dim]  ad {i}/{len(briefs)} — {brief.get('creative_type', '')}…[/dim]")

        resp = client.models.generate_content(
            model=MODEL,
            contents=[
                types.Part.from_bytes(data=product_bytes, mime_type=product_mime),
                prompt,
            ],
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
                image_config=types.ImageConfig(aspect_ratio="1:1"),
            ),
        )

        saved = _save_first_image(resp, run_dir, i, brief)
        if saved:
            outputs.append(saved)
            console.print(f"    [green]✓[/green] {saved.name}")
        else:
            console.print(f"    [yellow]⚠[/yellow] no image returned for ad {i}")

    return outputs


def _save_first_image(resp, run_dir: Path, idx: int, brief: dict) -> Path | None:
    for cand in resp.candidates or []:
        for part in cand.content.parts or []:
            if getattr(part, "inline_data", None) and part.inline_data.data:
                raw = part.inline_data.data
                img_bytes = raw if isinstance(raw, bytes) else base64.b64decode(raw)
                slug = slugify(brief.get("concept", f"ad-{idx}"))
                out = run_dir / f"ad-{idx}-{slug}.png"
                out.write_bytes(img_bytes)
                return out
    return None
