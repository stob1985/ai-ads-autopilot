"""Level 1 + 2 entry point.

Examples:
    # Level 1 — still ads only
    python generate.py --images --product "Matcha protein stick" \\
        --benefits "30g plant protein, zero crash, tastes like dessert"

    # Level 2 — video on top of a previous image run
    python generate.py --video --from-run 2026-04-17_143022

    # Both in one go
    python generate.py --images --video --product "..." --benefits "..."
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from src import creative_brief, image_gen, utils, video_gen

utils.load_env()


def resolve_run(from_run: str | None, product: str | None) -> Path:
    if from_run:
        p = utils.WORKSPACE / from_run
        if not p.exists():
            utils.console.print(f"[red]No such run:[/red] {p}")
            sys.exit(1)
        return p
    return utils.new_run_dir(product)


def load_existing_briefs(run_dir: Path) -> list[dict]:
    src = run_dir / "briefs.json"
    if not src.exists():
        utils.console.print(f"[red]No briefs.json in {run_dir}[/red] — pass --images or a run that has one.")
        sys.exit(1)
    return json.loads(src.read_text())["briefs"]


def pick_winner(briefs: list[dict], choice: int | None) -> dict:
    if choice is not None:
        return briefs[choice - 1]
    return briefs[0]


def main() -> None:
    p = argparse.ArgumentParser(description="Generate AI product ads — stills (Gemini) and/or UGC video (HeyGen).")
    p.add_argument("--images", action="store_true", help="Level 1 — generate 4 static ad creatives")
    p.add_argument("--video", action="store_true", help="Level 2 — generate HeyGen UGC video")
    p.add_argument("--product", help="product name, e.g. 'Matcha protein stick'")
    p.add_argument("--benefits", help="1-3 benefits, free text")
    p.add_argument("--product-image", type=Path, help="override path to the product image")
    p.add_argument("--from-run", help="reuse a previous run's brief (e.g. 2026-04-17_143022)")
    p.add_argument("--use-brief", type=int, default=None, help="which of the 4 briefs drives the video (1-4)")
    args = p.parse_args()

    if not (args.images or args.video):
        utils.console.print("Pick at least one: [cyan]--images[/cyan] or [cyan]--video[/cyan]")
        sys.exit(2)

    product = args.product or "product"
    run_dir = resolve_run(args.from_run, product)

    briefs_data: dict | None = None
    image_paths: list[Path] = []

    if args.images:
        if not args.product or not args.benefits:
            utils.console.print("[red]--images requires --product and --benefits[/red]")
            sys.exit(2)
        briefs_data = creative_brief.write_briefs(args.product, args.benefits, run_dir)
        image_paths = image_gen.generate_images(
            args.product,
            briefs_data["briefs"],
            utils.product_image(args.product_image),
            run_dir,
        )
        utils.console.print(f"\n[bold green]Level 1 done.[/bold green] {len(image_paths)} ads in {run_dir}")

    if args.video:
        if briefs_data is None:
            briefs = load_existing_briefs(run_dir)
        else:
            briefs = briefs_data["briefs"]
        winning = pick_winner(briefs, args.use_brief)
        video_path = video_gen.make_video(winning, run_dir)
        utils.console.print(f"\n[bold green]Level 2 done.[/bold green] Video: {video_path}")

    utils.console.print(f"\nOpen the folder: [cyan]open {run_dir}[/cyan]")


if __name__ == "__main__":
    main()
