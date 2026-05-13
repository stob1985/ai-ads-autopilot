"""Publish a generated image batch into Meta Ads — Draft mode.

Reads images from a `previews/<batch>/` directory (or any folder of PNGs),
plus the Meta config (`config/meta.yaml`) and a token from `.env`. Creates
one PAUSED campaign with adsets + ads ready for review in Meta Ads Manager.

Examples:
    # Dry run: print the plan, no API calls
    python publish_to_meta.py \
        --batch previews/hh-v2-batch \
        --page hormone_harmony \
        --campaign-name "HH v2 Test - May 2026" \
        --landing-url "https://vitalharmony.net/products/hormone-harmonia-..." \
        --primary-text "Visszakapod a régi önmagad — 12 hatóanyag, 6 hormon." \
        --headline "Hormone Harmonia™" \
        --description "72 vegán kapszula" \
        --dry-run

    # Real run, per-angle adsets
    python publish_to_meta.py \
        --batch previews/hh-v2-batch \
        --page hormone_harmony \
        --campaign-name "HH v2 Test" \
        --landing-url "..." \
        --primary-text "..." --headline "..." --description "..." \
        --structure per_angle \
        --daily-budget-huf 5000

Structure modes:
    single_adset  — 1 adset, all ads attached (Meta auto-optimises)
    per_angle     — 1 adset per angle (recognises filenames like
                    "doctor_revelation_*", "summer_countdown_*", etc.)
    per_template  — 1 adset per (angle, template) pair

All campaigns, adsets, and ads are created in PAUSED state. Flip them
to ACTIVE manually in Ads Manager.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

import yaml

from src import meta_ads, utils

utils.load_env()


def load_meta_config(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def resolve_page(cfg: dict, key: str) -> dict:
    pages = cfg.get("pages") or {}
    if key not in pages:
        raise SystemExit(f"Unknown page '{key}'. Available: {list(pages)}")
    return pages[key]


def collect_images(batch_dir: Path) -> list[Path]:
    images: list[Path] = []
    for p in sorted(batch_dir.rglob("*.png")):
        if p.name == "manifest.json":
            continue
        images.append(p)
    if not images:
        raise SystemExit(f"No PNGs found under {batch_dir}")
    return images


def group_for_structure(images: list[Path], structure: str) -> dict[str, list[Path]]:
    """Return {adset_label: [images]}."""
    if structure == "single_adset":
        return {"all": images}

    groups: dict[str, list[Path]] = {}
    for img in images:
        stem = img.stem  # e.g. doctor_revelation_medical_infographic_v1
        parts = stem.split("_v")
        head = parts[0]  # e.g. doctor_revelation_medical_infographic
        tokens = head.split("_")
        if structure == "per_template":
            label = head
        elif structure == "per_angle":
            # angle = first two underscore tokens for things like
            # "doctor_revelation_*", "whatsapp_chat_*", "summer_countdown_*",
            # "quiet_rebellion_*", "invisible_tax_*", "cortisol_belly_*".
            if len(tokens) >= 2:
                label = "_".join(tokens[:2])
            else:
                label = tokens[0]
        else:
            raise SystemExit(f"Unknown structure: {structure}")
        groups.setdefault(label, []).append(img)
    return groups


def plan(images: list[Path], groups: dict[str, list[Path]], cfg_defaults: dict, args) -> dict:
    return {
        "campaign_name": args.campaign_name,
        "objective": args.objective,
        "page": args.page,
        "structure": args.structure,
        "daily_budget_huf": args.daily_budget_huf,
        "landing_url": args.landing_url,
        "image_count": len(images),
        "adsets": [
            {
                "name": label,
                "ad_count": len(group),
                "ads": [img.name for img in group],
            }
            for label, group in groups.items()
        ],
        "targeting_preview": meta_ads.build_targeting(
            geo_locations=args.geo or cfg_defaults["geo_locations"],
            age_min=args.age_min or cfg_defaults["age_min"],
            age_max=args.age_max or cfg_defaults["age_max"],
            genders=args.genders or cfg_defaults["genders"],
        ),
    }


def execute(images: list[Path], groups: dict[str, list[Path]], cfg: dict, args, client: meta_ads.MetaClient) -> dict:
    page = resolve_page(cfg, args.page)
    page_id = page["id"]
    defaults = cfg.get("defaults", {})

    targeting = meta_ads.build_targeting(
        geo_locations=args.geo or defaults.get("geo_locations", ["HU"]),
        age_min=args.age_min or defaults.get("age_min", 40),
        age_max=args.age_max or defaults.get("age_max", 65),
        genders=args.genders or defaults.get("genders", [2]),
    )

    manifest: dict = {
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "campaign": {},
        "adsets": [],
        "ads": [],
        "image_uploads": [],
    }

    utils.console.print(f"[bold]Creating campaign[/bold] '{args.campaign_name}' (PAUSED, objective {args.objective})…")
    campaign_id = client.create_campaign(name=args.campaign_name, objective=args.objective)
    manifest["campaign"] = {"id": campaign_id, "name": args.campaign_name}
    utils.console.print(f"  [green]✓[/green] campaign {campaign_id}")

    # Pre-upload all images so each ad creation reuses the hash.
    utils.console.print(f"[bold]Uploading {len(images)} images…[/bold]")
    image_hashes: dict[str, str] = {}
    for i, img in enumerate(images, 1):
        try:
            h = client.upload_image(img)
            image_hashes[img.name] = h
            manifest["image_uploads"].append({"file": img.name, "hash": h})
            utils.console.print(f"  [{i}/{len(images)}] [green]✓[/green] {img.name}")
        except meta_ads.MetaError as e:
            utils.console.print(f"  [{i}/{len(images)}] [red]✗[/red] {img.name}: {e}")
            manifest["image_uploads"].append({"file": img.name, "error": str(e)})

    # Create adsets + ads per group.
    for label, group in groups.items():
        adset_name = f"{args.campaign_name} — {label}"
        utils.console.print(f"[bold]AdSet[/bold] '{label}' ({len(group)} ads)…")
        try:
            adset_id = client.create_adset(
                name=adset_name,
                campaign_id=campaign_id,
                daily_budget_minor_units=args.daily_budget_huf,   # HUF: minor unit = forint
                targeting=targeting,
                billing_event="IMPRESSIONS",
                optimization_goal="LINK_CLICKS" if args.objective == "OUTCOME_TRAFFIC" else "LINK_CLICKS",
            )
            manifest["adsets"].append({"id": adset_id, "name": adset_name, "label": label})
            utils.console.print(f"  [green]✓[/green] adset {adset_id}")
        except meta_ads.MetaError as e:
            utils.console.print(f"  [red]✗[/red] adset creation failed: {e}")
            manifest["adsets"].append({"label": label, "error": str(e)})
            continue

        for img in group:
            if img.name not in image_hashes:
                continue   # upload failed earlier
            ad_name = img.stem
            try:
                creative_id = client.create_link_creative(
                    name=f"{ad_name} creative",
                    page_id=page_id,
                    image_hash=image_hashes[img.name],
                    link_url=args.landing_url,
                    message=args.primary_text,
                    headline=args.headline,
                    description=args.description,
                    call_to_action=args.cta,
                )
                ad_id = client.create_ad(name=ad_name, adset_id=adset_id, creative_id=creative_id)
                manifest["ads"].append({"id": ad_id, "name": ad_name, "adset_id": adset_id, "creative_id": creative_id})
                utils.console.print(f"    [green]✓[/green] ad {ad_id} ({ad_name})")
            except meta_ads.MetaError as e:
                utils.console.print(f"    [red]✗[/red] ad {ad_name}: {e}")
                manifest["ads"].append({"name": ad_name, "error": str(e)})

    manifest["finished_at"] = datetime.now().isoformat(timespec="seconds")
    manifest["ads_manager_url"] = meta_ads.ads_manager_url(
        business_id=cfg["business_manager_id"],
        ad_account_id=cfg["ad_account_id"],
        campaign_id=campaign_id,
    )
    return manifest


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--batch", type=Path, required=True, help="Folder of PNGs (e.g. previews/hh-v2-batch)")
    p.add_argument("--meta-config", type=Path, default=Path("config/meta.yaml"))
    p.add_argument("--page", required=True, help="Page key from config/meta.yaml (e.g. hormone_harmony)")
    p.add_argument("--campaign-name", required=True)
    p.add_argument("--landing-url", required=True, help="URL the ads click through to")
    p.add_argument("--primary-text", required=True, help="Body text above the image (90-125 chars ideal)")
    p.add_argument("--headline", required=True, help="Short headline under the image (max 27 chars)")
    p.add_argument("--description", default="", help="Optional shorter sub-text")
    p.add_argument("--cta", default="SHOP_NOW", help="Call-to-action button (SHOP_NOW, LEARN_MORE, ORDER_NOW, …)")
    p.add_argument("--objective", default="OUTCOME_TRAFFIC", help="Campaign objective (OUTCOME_TRAFFIC, OUTCOME_SALES, …)")
    p.add_argument("--structure", default="per_angle", choices=["single_adset", "per_angle", "per_template"])
    p.add_argument("--daily-budget-huf", type=int, default=5000, help="Daily budget per adset, in HUF")
    p.add_argument("--geo", action="append", help="Geo target country codes (repeatable). Default: HU")
    p.add_argument("--age-min", type=int)
    p.add_argument("--age-max", type=int)
    p.add_argument("--genders", type=int, action="append", help="1 men, 2 women (repeatable)")
    p.add_argument("--dry-run", action="store_true", help="Print the plan but don't call Meta")
    args = p.parse_args()

    if not args.batch.exists():
        raise SystemExit(f"Batch dir not found: {args.batch}")
    if not args.meta_config.exists():
        raise SystemExit(f"Meta config not found: {args.meta_config}")

    cfg = load_meta_config(args.meta_config)
    cfg_defaults = cfg.get("defaults", {})

    # Allow `landing_url` from config if the CLI flag was left as a placeholder.
    page_cfg = resolve_page(cfg, args.page)
    if (not args.landing_url or args.landing_url == "null") and page_cfg.get("landing_url"):
        args.landing_url = page_cfg["landing_url"]

    images = collect_images(args.batch)
    groups = group_for_structure(images, args.structure)

    plan_dict = plan(images, groups, cfg_defaults, args)
    utils.console.print("[bold]Plan:[/bold]")
    utils.console.print(json.dumps(plan_dict, indent=2, ensure_ascii=False))

    if args.dry_run:
        utils.console.print("\n[yellow]--dry-run set — exiting before any Meta call.[/yellow]")
        return

    client = meta_ads.MetaClient(ad_account_id=cfg["ad_account_id"])

    # Sanity checks first so we fail fast on a bad token.
    utils.console.print("\n[bold]Validating token…[/bold]")
    try:
        me = client.me()
        utils.console.print(f"  [green]✓[/green] /me: {me}")
        acct = client.ad_account()
        utils.console.print(f"  [green]✓[/green] ad account: {acct.get('name')} ({acct.get('account_status')})")
    except meta_ads.MetaError as e:
        utils.console.print(f"  [red]✗ token validation failed:[/red] {e}")
        sys.exit(1)

    manifest = execute(images, groups, cfg, args, client)

    out_path = args.batch / "meta_manifest.json"
    out_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    utils.console.print(f"\n[bold]Done.[/bold] Manifest: {out_path}")
    utils.console.print(f"Open in Ads Manager: [blue]{manifest['ads_manager_url']}[/blue]")


if __name__ == "__main__":
    main()
