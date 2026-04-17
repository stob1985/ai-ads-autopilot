"""Level 1 wizard: collect API keys, validate each, write .env.

Usage:
    python setup.py                  # interactive
    python setup.py --heygen-avatar  # upload inputs/creator.jpg, save avatar id to .env
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

ROOT = Path(__file__).resolve().parent
ENV_PATH = ROOT / ".env"
ENV_EXAMPLE = ROOT / ".env.example"

console = Console()

KEYS = [
    ("ANTHROPIC_API_KEY", "Claude (writes the creative briefs + script)", "https://console.anthropic.com/"),
    ("GEMINI_API_KEY", "Gemini Nano Banana 2 (generates the still ads)", "https://aistudio.google.com/app/apikey"),
    ("HEYGEN_API_KEY", "HeyGen (renders the UGC video)", "https://app.heygen.com/settings?nav=API"),
]


def read_env() -> dict[str, str]:
    if not ENV_PATH.exists():
        if ENV_EXAMPLE.exists():
            ENV_PATH.write_text(ENV_EXAMPLE.read_text(), encoding="utf-8")
        else:
            ENV_PATH.write_text("", encoding="utf-8")
    parsed: dict[str, str] = {}
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            k, _, v = line.partition("=")
            parsed[k.strip()] = v.strip()
    return parsed


def write_env(updates: dict[str, str]) -> None:
    existing = ENV_PATH.read_text(encoding="utf-8") if ENV_PATH.exists() else ""
    lines = existing.splitlines()
    seen: set[str] = set()
    for i, line in enumerate(lines):
        if "=" in line and not line.lstrip().startswith("#"):
            k = line.split("=", 1)[0].strip()
            if k in updates:
                lines[i] = f"{k}={updates[k]}"
                seen.add(k)
    for k, v in updates.items():
        if k not in seen:
            lines.append(f"{k}={v}")
    ENV_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def prompt_key(name: str, label: str, signup_url: str, current: str) -> str:
    masked = f"{current[:4]}…{current[-4:]}" if current and len(current) > 8 else current
    console.print(f"\n[bold cyan]{name}[/bold cyan] — {label}")
    if current:
        console.print(f"  current: [dim]{masked}[/dim]")
    console.print(f"  sign up: [blue]{signup_url}[/blue]")
    entered = input(f"  paste {name} (or press Enter to keep current): ").strip()
    return entered or current


def validate(name: str, value: str) -> bool:
    if not value:
        return False
    try:
        if name == "ANTHROPIC_API_KEY":
            from anthropic import Anthropic
            Anthropic(api_key=value).models.list()
        elif name == "GEMINI_API_KEY":
            from google import genai
            list(genai.Client(api_key=value).models.list())
        elif name == "HEYGEN_API_KEY":
            import requests
            r = requests.get(
                "https://api.heygen.com/v2/voices",
                headers={"X-Api-Key": value},
                timeout=15,
            )
            r.raise_for_status()
        return True
    except Exception as e:
        console.print(f"  [red]✗ validation failed:[/red] {e}")
        return False


def run_interactive() -> None:
    console.print(Panel.fit(
        "[bold]ai-ads-autopilot setup[/bold]\nWe'll collect 3 API keys, validate each, and write your .env.",
        border_style="cyan",
    ))
    env = read_env()
    updates: dict[str, str] = {}
    for name, label, url in KEYS:
        updates[name] = prompt_key(name, label, url, env.get(name, ""))

    write_env(updates)
    console.print("\n[bold]Validating…[/bold]")
    os.environ.update(updates)
    all_ok = True
    for name, _, _ in KEYS:
        val = updates[name]
        ok = validate(name, val)
        console.print(f"  {name}: {'[green]✓[/green]' if ok else '[red]✗[/red]'}")
        all_ok = all_ok and ok

    if all_ok:
        console.print("\n[green bold]All keys valid.[/green bold] Next: drop inputs/creator.jpg + inputs/product.png, then:")
        console.print('  [cyan]python generate.py --images --product "Your product" --benefits "benefit 1, benefit 2"[/cyan]')
    else:
        console.print("\n[yellow]Some keys didn't validate.[/yellow] Re-run setup.py to fix.")
        sys.exit(1)


def run_heygen_avatar(wait: bool) -> None:
    from src import heygen, utils
    utils.load_env()
    photo = utils.creator_image()
    tid = heygen.upload_talking_photo(photo)
    write_env({"HEYGEN_AVATAR_ID": tid})
    console.print(f"[green]✓[/green] HEYGEN_AVATAR_ID saved to .env")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--heygen-avatar", action="store_true", help="upload inputs/creator.jpg as a HeyGen talking photo")
    p.add_argument("--wait", action="store_true", help="unused placeholder for future training-wait flows")
    args = p.parse_args()

    if args.heygen_avatar:
        run_heygen_avatar(wait=args.wait)
    else:
        run_interactive()


if __name__ == "__main__":
    main()
