"""Level 3 — autopilot loop.

Reads a YAML list of products, and every N hours generates a fresh
batch of ads + a UGC video for each one. Survives restarts via a
simple state file tracking which product is next.

Usage:
    python autopilot.py --products products.yaml --interval 6h
    python autopilot.py --products products.yaml --once        # single pass
    python autopilot.py --stop                                 # clean shutdown signal
"""
from __future__ import annotations

import argparse
import json
import re
import signal
import sys
import time
from pathlib import Path

from src import creative_brief, image_gen, utils, video_gen

utils.load_env()

STATE_FILE = Path(__file__).resolve().parent / ".autopilot-state.json"
STOP_FILE = Path(__file__).resolve().parent / ".autopilot-stop"


def parse_interval(text: str) -> int:
    m = re.fullmatch(r"\s*(\d+)\s*([smhd])?\s*", text.lower())
    if not m:
        raise ValueError(f"Bad interval: {text}")
    n = int(m.group(1))
    mult = {"s": 1, "m": 60, "h": 3600, "d": 86400}[m.group(2) or "h"]
    return n * mult


def load_products(path: Path) -> list[dict]:
    try:
        import yaml  # type: ignore
    except ImportError:
        utils.console.print("[red]autopilot needs pyyaml. Install with: pip install pyyaml[/red]")
        sys.exit(1)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        raise ValueError("products.yaml must be a non-empty list")
    return data


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"cursor": 0, "runs": 0}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def run_one(entry: dict) -> Path:
    name = entry["name"]
    benefits = entry["benefits"]
    product_image = Path(entry.get("product_image") or utils.INPUTS / "product.png")
    run_dir = utils.new_run_dir(f"auto-{name}")

    briefs = creative_brief.write_briefs(name, benefits, run_dir)
    image_gen.generate_images(name, briefs["briefs"], product_image, run_dir)
    video_gen.make_video(briefs["briefs"][0], run_dir)
    return run_dir


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--products", type=Path, help="path to products.yaml")
    p.add_argument("--interval", default="6h", help="e.g. 30m, 6h, 1d")
    p.add_argument("--once", action="store_true", help="run a single cycle and exit")
    p.add_argument("--stop", action="store_true", help="signal a running loop to exit after the current run")
    args = p.parse_args()

    if args.stop:
        STOP_FILE.touch()
        utils.console.print(f"[yellow]Stop requested. Current run will finish, then exit.[/yellow]")
        return

    if not args.products:
        utils.console.print("[red]--products is required[/red]")
        sys.exit(2)

    products = load_products(args.products)
    interval = parse_interval(args.interval)
    state = load_state()
    STOP_FILE.unlink(missing_ok=True)

    def handle_signal(*_):
        STOP_FILE.touch()
        utils.console.print("\n[yellow]Caught Ctrl+C. Will exit after current run.[/yellow]")

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    utils.console.print(f"[bold]Autopilot up.[/bold] {len(products)} products, every {args.interval}.")
    while True:
        entry = products[state["cursor"] % len(products)]
        try:
            out = run_one(entry)
            utils.console.print(f"[green]✓[/green] {entry['name']} → {out}")
        except Exception as e:
            utils.console.print(f"[red]✗[/red] {entry['name']}: {e}")
        state["cursor"] = (state["cursor"] + 1) % len(products)
        state["runs"] += 1
        save_state(state)

        if args.once or STOP_FILE.exists():
            STOP_FILE.unlink(missing_ok=True)
            break
        utils.console.print(f"[dim]sleeping {args.interval}…[/dim]")
        slept = 0
        while slept < interval:
            if STOP_FILE.exists():
                break
            time.sleep(min(30, interval - slept))
            slept += 30


if __name__ == "__main__":
    main()
