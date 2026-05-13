# Meta Ads — Draft-mode publishing

Tools: `src/meta_ads.py` (Graph API v22.0 client) + `publish_to_meta.py` (CLI).

Everything is created in **PAUSED** state. The script never starts spend — you flip campaigns to ACTIVE manually in Meta Ads Manager.

## Prereq

1. **System User access token** with `ads_management`, `ads_read`, `pages_manage_ads`, `pages_read_engagement`, `business_management` permissions. Should be a non-expiring token.
2. **Token in `.env`**:
   ```
   META_ACCESS_TOKEN=EAA...
   ```
3. **`config/meta.yaml`** populated with `business_manager_id`, `ad_account_id`, and the page IDs you publish to.
4. **A folder of PNGs** — anything under `previews/<batch>/` works. Filenames like `{angle}_{template}_v{n}.png` are auto-grouped by the `--structure per_angle` mode.

## Note: sandbox can't reach `graph.facebook.com`

The Claude Code sandbox blocks Facebook hostnames at egress. **Run `publish_to_meta.py` on your own machine**, not from the sandbox. Workflow:

```bash
# locally
git pull origin claude/improve-usability-lPe44
pip install -r requirements.txt
cp .env.example .env   # then paste your META_ACCESS_TOKEN
```

## Dry run first

Always start with `--dry-run`. It prints the plan (campaign name, adsets, ad count, targeting) without calling the Meta API:

```bash
python publish_to_meta.py \
    --batch previews/hh-v2-batch \
    --page hormone_harmony \
    --campaign-name "HH v2 - May 2026 - Test" \
    --landing-url "https://vitalharmony.net/products/hormone-harmonia-..." \
    --primary-text "Visszakapod a régi önmagad — 12 hatóanyag, 6 hormon." \
    --headline "Hormone Harmonia™" \
    --description "72 vegán kapszula" \
    --structure per_angle \
    --daily-budget-huf 5000 \
    --dry-run
```

## Real run

Remove `--dry-run`. The script:

1. Validates `/me` and the ad account with the token (fails fast on bad token).
2. Uploads every PNG to the ad account image library.
3. Creates one PAUSED campaign (objective `OUTCOME_TRAFFIC`).
4. For each group (per `--structure`), creates a PAUSED adset with daily budget + targeting.
5. For each image, creates an AdCreative + a PAUSED Ad attached to its adset.
6. Writes `previews/<batch>/meta_manifest.json` (gitignored) with all the IDs + a direct Ads Manager link.

## Structure modes

- `single_adset` — one adset, all ads inside it. Meta's auction picks winners; fastest stat convergence but no per-angle attribution.
- `per_angle` — one adset per angle (recognises `doctor_revelation_*`, `whatsapp_chat_*`, etc.). Best for the HH v2 / Skintific v2 batches if you want angle-level reporting.
- `per_template` — one adset per (angle, template) pair. Fine-grained but more adsets to manage.

## After publishing

The manifest prints a link like:
```
https://business.facebook.com/adsmanager/manage/campaigns?act=313572470043786&business_id=478789878959559&selected_campaign_ids=<campaign-id>
```

Open it in your browser:
1. Review each ad's preview.
2. Sanity-check the targeting and budget on each adset.
3. Flip the campaign to ACTIVE when you're ready to spend.

## Troubleshooting

- **400 error: `permissions`** — token missing `ads_management` or the System User isn't assigned to the ad account / page. Re-create the token with the right asset assignments.
- **400 error: `invalid parameter` on creative** — your landing URL needs `https://` and a valid domain that Meta has crawled.
- **The ads land in `Disapproved` state immediately** — Meta's auto-review caught a policy issue. Click the disapproved ad in Ads Manager for the reason; common ones for the HH product line are weight-loss claims, before/after framing, and medical claims.
- **Token expired** — refresh in Business Settings → Users → System Users → Tokens → Refresh, then update `.env`.
