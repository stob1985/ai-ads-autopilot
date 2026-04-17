"""Shared helpers: env loading, run folders, console printing."""
from __future__ import annotations

import os
import re
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console

ROOT = Path(__file__).resolve().parent.parent
INPUTS = ROOT / "inputs"
WORKSPACE = ROOT / "ad-workspace"

console = Console()


def load_env() -> None:
    load_dotenv(ROOT / ".env")


def require_env(key: str, hint: str = "") -> str:
    val = os.environ.get(key, "").strip()
    if not val:
        console.print(f"[red]Missing {key}[/red]. {hint}")
        console.print(f"Run [cyan]python setup.py[/cyan] to configure keys.")
        sys.exit(1)
    return val


def slugify(text: str, max_len: int = 40) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return s[:max_len] or "run"


def new_run_dir(label: str | None = None) -> Path:
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    name = f"{stamp}_{slugify(label)}" if label else stamp
    path = WORKSPACE / name
    path.mkdir(parents=True, exist_ok=True)
    return path


def creator_image() -> Path:
    for ext in ("jpg", "jpeg", "png", "webp"):
        p = INPUTS / f"creator.{ext}"
        if p.exists():
            return p
    console.print("[red]No creator photo found.[/red] Drop one at inputs/creator.jpg")
    sys.exit(1)


def product_image(override: Path | None = None) -> Path:
    if override and override.exists():
        return override
    for ext in ("png", "jpg", "jpeg", "webp"):
        p = INPUTS / f"product.{ext}"
        if p.exists():
            return p
    console.print("[red]No product photo found.[/red] Drop one at inputs/product.png")
    sys.exit(1)
