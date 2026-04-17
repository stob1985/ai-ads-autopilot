"""Claude writes the 4 creative briefs + the video script.

Inputs: product name + benefits (free text). Outputs: structured briefs
that the image + video stages consume downstream.
"""
from __future__ import annotations

import json
from pathlib import Path

from anthropic import Anthropic

from .utils import console, require_env

MODEL = "claude-sonnet-4-6"

BRIEF_SYSTEM = """You are an elite DTC creative strategist. You write ad briefs that stop the scroll in 0.5 seconds.

Non-negotiables:
- Headlines are punchy fragments, 3-6 words MAX. Not sentences. "Knock Yourself Out." not "This product will help you sleep better."
- Each brief commits to ONE saturated color world. The whole scene — set, props, wardrobe, lighting — is drenched in that color.
- Features don't sell. Identity and emotion do.
- The product packaging must be reproduced pixel-accurate from the reference image the image model receives.

Output strict JSON. No prose, no markdown fences."""

BRIEF_USER = """Product: {product}
Benefits: {benefits}

Output JSON with this schema:

{{
  "icp": "one sentence describing the ideal customer — specific, not demographic",
  "tone": "one of: dark-emotional | funny-sharable | premium-aspirational | educational-trust",
  "briefs": [
    {{
      "concept": "one-line creative idea",
      "creative_type": "monochromatic-world | visual-metaphor | impossible-perspective | ingredient-explosion | color-drenched-aspiration",
      "headline": "3-6 word punchy fragment",
      "subtext": "one short line, optional",
      "cta": "2-4 words",
      "color_world": "specific hex + name, e.g. 'saturated purple #6B3FA0'",
      "visual_direction": "3-5 sentences. Describe the scene as if briefing a $50k photo shoot. Where is the product? What is the concept? What color dominates every pixel?"
    }},
    ... 4 total briefs, each with a DIFFERENT creative_type ...
  ]
}}

At least 2 of the 4 must be monochromatic-world, visual-metaphor, or impossible-perspective (the boldest types)."""

SCRIPT_USER = """Based on this winning ad brief, write a 20-second UGC-style script. First person, conversational, like a creator talking to the camera about a product they actually use.

Rules:
- 45-55 words total (20 seconds at natural pace)
- Open with a pattern interrupt hook in the first 3 words
- One benefit per sentence, max three
- End with a subtle CTA, not a hard sell
- NO emojis, NO stage directions, NO "[pause]" markers — just the spoken words

Brief:
{brief}

Output the script as plain text. No quotes, no markdown."""


def write_briefs(product: str, benefits: str, run_dir: Path) -> dict:
    client = Anthropic(api_key=require_env("ANTHROPIC_API_KEY"))
    console.print(f"[dim]Drafting 4 creative briefs for [cyan]{product}[/cyan]…[/dim]")

    resp = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        system=BRIEF_SYSTEM,
        messages=[{"role": "user", "content": BRIEF_USER.format(product=product, benefits=benefits)}],
    )
    raw = resp.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1].lstrip("json").strip()
    data = json.loads(raw)

    out = run_dir / "campaign-brief.md"
    out.write_text(_render_brief_md(product, benefits, data), encoding="utf-8")
    (run_dir / "briefs.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    console.print(f"[green]✓[/green] Briefs written to {out.relative_to(run_dir.parent.parent)}")
    return data


def write_script(brief: dict, run_dir: Path) -> str:
    client = Anthropic(api_key=require_env("ANTHROPIC_API_KEY"))
    console.print("[dim]Writing UGC script for the HeyGen video…[/dim]")

    resp = client.messages.create(
        model=MODEL,
        max_tokens=400,
        messages=[{"role": "user", "content": SCRIPT_USER.format(brief=json.dumps(brief, indent=2))}],
    )
    script = resp.content[0].text.strip()
    (run_dir / "video-script.md").write_text(f"# Video script\n\n{script}\n", encoding="utf-8")
    console.print(f"[green]✓[/green] Script ready ({len(script.split())} words)")
    return script


def _render_brief_md(product: str, benefits: str, data: dict) -> str:
    lines = [f"# Campaign brief — {product}", "", f"**Benefits:** {benefits}", "",
             f"**ICP:** {data.get('icp', '')}", f"**Tone:** {data.get('tone', '')}", ""]
    for i, b in enumerate(data.get("briefs", []), start=1):
        lines += [
            f"## Ad {i} — {b.get('creative_type', '')}",
            "", f"**Concept:** {b.get('concept', '')}",
            f"**Headline:** {b.get('headline', '')}",
            f"**Subtext:** {b.get('subtext', '')}",
            f"**CTA:** {b.get('cta', '')}",
            f"**Color world:** {b.get('color_world', '')}",
            "", "**Visual direction:**", b.get("visual_direction", ""), "",
        ]
    return "\n".join(lines)
