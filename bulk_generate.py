"""Bulk image generation entry point.

Reads a YAML of full Gemini prompts (each with a `full_prompt` field) and
generates an image for each, optionally with N variants. Skips the Claude
brief step — use this when you already have hand-written prompts.

Examples:
    # Phase 1 only (5 prompts), 1 variant each = 5 images
    python bulk_generate.py --prompts config/prompts.yaml \
        --product-image inputs/products/hormone_harmonia_box.png --phase 1

    # All 10 prompts, 5 variants each = 50 images
    python bulk_generate.py --prompts config/prompts.yaml \
        --product-image inputs/products/hormone_harmonia_box.png --variants 5

    # Single prompt, 3 variants
    python bulk_generate.py --prompts config/prompts.yaml \
        --product-image inputs/products/hormone_harmonia_box.png \
        --only prompt_001_cortisol_diagram --variants 3
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src import bulk_image_gen, utils

utils.load_env()


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--prompts", type=Path, required=True, help="YAML of prompt_id -> {full_prompt, angle, template, phase}")
    p.add_argument("--product-image", type=Path, default=None, help="Reference product image (passed to every Gemini call). Omit when the prompts intentionally exclude the product.")
    p.add_argument("--phase", type=int, default=None, help="Only run prompts with this phase number")
    p.add_argument("--avatar", default=None, help="Only run prompts with this avatar tag")
    p.add_argument("--compliance", choices=["compliant", "aggressive"], default=None, help="Only run prompts with this compliance tag")
    p.add_argument("--only", action="append", default=None, help="Run only these prompt ids (repeatable)")
    p.add_argument("--variants", type=int, default=1, help="How many variants per prompt (default 1)")
    p.add_argument("--aspect-ratio", default="1:1", choices=["1:1", "4:5", "9:16", "16:9", "3:4", "4:3"], help="Output aspect ratio (default 1:1)")
    p.add_argument("--label", default="hormone-harmonia", help="Run folder label")
    args = p.parse_args()

    if not args.prompts.exists():
        utils.console.print(f"[red]Prompts file not found:[/red] {args.prompts}")
        sys.exit(2)
    if args.product_image and not args.product_image.exists():
        utils.console.print(f"[red]Product image not found:[/red] {args.product_image}")
        utils.console.print(f"[dim]Drop the product PNG at that path, then re-run.[/dim]")
        sys.exit(2)

    prompts = bulk_image_gen.load_prompts(args.prompts)
    selected = bulk_image_gen.filter_prompts(prompts, args.phase, args.only, args.avatar, args.compliance)
    if not selected:
        utils.console.print("[yellow]No prompts matched the filter.[/yellow]")
        sys.exit(1)

    run_dir = utils.new_run_dir(args.label)
    total = len(selected) * args.variants
    utils.console.print(
        f"[bold]Bulk generate.[/bold] {len(selected)} prompt(s) × {args.variants} variant(s) = {total} image(s). "
        f"Aspect: {args.aspect_ratio}. Output: {run_dir}"
    )

    manifest = bulk_image_gen.run_bulk(
        prompts=selected,
        product_image=args.product_image,
        run_dir=run_dir,
        aspect_ratio=args.aspect_ratio,
        variants=args.variants,
    )
    ok, fail = bulk_image_gen.summarize(manifest)
    utils.console.print(f"\n[bold]Done.[/bold] [green]{ok} succeeded[/green], [red]{fail} failed[/red].")
    utils.console.print(f"Manifest: {run_dir / 'manifest.json'}")


if __name__ == "__main__":
    main()
