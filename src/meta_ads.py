"""Meta Marketing API client — Draft-mode ad publishing.

Wraps just enough of Graph API v22.0 to:
1. Upload images to the ad account's image library.
2. Create a Campaign (PAUSED).
3. Create AdSets (PAUSED, with targeting + daily budget).
4. Create AdCreatives that pair an uploaded image with copy + CTA.
5. Create Ads that link a creative into an AdSet.

Everything is created in PAUSED state. The user reviews in Meta Ads Manager
and flips to ACTIVE manually — zero risk of unintended spend.

Auth: System User access token from .env (META_ACCESS_TOKEN).

Docs:
- https://developers.facebook.com/docs/marketing-apis/overview
- https://developers.facebook.com/docs/marketing-api/reference/ad-image
- https://developers.facebook.com/docs/marketing-api/reference/ad-campaign-group
- https://developers.facebook.com/docs/marketing-api/reference/ad-campaign
- https://developers.facebook.com/docs/marketing-api/reference/ad-creative
- https://developers.facebook.com/docs/marketing-api/reference/adgroup
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import requests

from .utils import console, require_env

API_VERSION = "v22.0"
BASE = f"https://graph.facebook.com/{API_VERSION}"


class MetaError(RuntimeError):
    """Wraps a Graph API error response with the raw body for debugging."""


class MetaClient:
    def __init__(self, ad_account_id: str, token: str | None = None) -> None:
        self.ad_account_id = ad_account_id if ad_account_id.startswith("act_") else f"act_{ad_account_id}"
        self.token = token or require_env("META_ACCESS_TOKEN", "Run setup or paste into .env.")

    # ---------- low-level ----------

    def _req(self, method: str, path: str, *, data: dict | None = None, files: dict | None = None, params: dict | None = None) -> dict:
        url = f"{BASE}/{path.lstrip('/')}"
        params = dict(params or {})
        params["access_token"] = self.token
        r = requests.request(method, url, data=data, files=files, params=params, timeout=60)
        if not r.ok:
            raise MetaError(f"{method} {path} → {r.status_code}: {r.text[:800]}")
        return r.json()

    # ---------- discovery ----------

    def me(self) -> dict:
        return self._req("GET", "me", params={"fields": "id,name"})

    def permissions(self) -> list[dict]:
        return self._req("GET", "me/permissions").get("data", [])

    def ad_account(self) -> dict:
        return self._req("GET", self.ad_account_id, params={
            "fields": "id,name,account_status,currency,timezone_name,disable_reason",
        })

    # ---------- images ----------

    def upload_image(self, path: Path) -> str:
        """Uploads a single image, returns its hash."""
        with path.open("rb") as fh:
            res = self._req("POST", f"{self.ad_account_id}/adimages", files={"file": (path.name, fh, "image/png")})
        # response: {"images": {"<filename>": {"hash": "...", "url": "..."}}}
        images = res.get("images") or {}
        if not images:
            raise MetaError(f"No image returned for {path}: {res}")
        entry = next(iter(images.values()))
        return entry["hash"]

    # ---------- campaign / adset / creative / ad ----------

    def create_campaign(self, name: str, objective: str = "OUTCOME_TRAFFIC", special_ad_categories: list[str] | None = None) -> str:
        data = {
            "name": name,
            "objective": objective,
            "status": "PAUSED",
            "special_ad_categories": json.dumps(special_ad_categories or []),
            "buying_type": "AUCTION",
        }
        res = self._req("POST", f"{self.ad_account_id}/campaigns", data=data)
        return res["id"]

    def create_adset(
        self,
        *,
        name: str,
        campaign_id: str,
        daily_budget_minor_units: int,
        targeting: dict,
        billing_event: str = "IMPRESSIONS",
        optimization_goal: str = "LINK_CLICKS",
        bid_strategy: str = "LOWEST_COST_WITHOUT_CAP",
        start_offset_minutes: int = 30,
    ) -> str:
        # start_time slightly in the future so PAUSED adsets don't ever
        # accidentally race-start if flipped to ACTIVE immediately.
        start_time = int(time.time()) + start_offset_minutes * 60
        data = {
            "name": name,
            "campaign_id": campaign_id,
            "daily_budget": daily_budget_minor_units,   # currency minor units (HUF: forint, no fractional)
            "billing_event": billing_event,
            "optimization_goal": optimization_goal,
            "bid_strategy": bid_strategy,
            "targeting": json.dumps(targeting),
            "status": "PAUSED",
            "start_time": start_time,
        }
        res = self._req("POST", f"{self.ad_account_id}/adsets", data=data)
        return res["id"]

    def create_link_creative(
        self,
        *,
        name: str,
        page_id: str,
        image_hash: str,
        link_url: str,
        message: str,
        headline: str,
        description: str = "",
        call_to_action: str = "SHOP_NOW",
    ) -> str:
        object_story_spec = {
            "page_id": page_id,
            "link_data": {
                "image_hash": image_hash,
                "link": link_url,
                "message": message,
                "name": headline,
                "description": description,
                "call_to_action": {
                    "type": call_to_action,
                    "value": {"link": link_url},
                },
            },
        }
        data = {
            "name": name,
            "object_story_spec": json.dumps(object_story_spec),
            "degrees_of_freedom_spec": json.dumps({"creative_features_spec": {"standard_enhancements": {"enroll_status": "OPT_OUT"}}}),
        }
        res = self._req("POST", f"{self.ad_account_id}/adcreatives", data=data)
        return res["id"]

    def create_ad(self, *, name: str, adset_id: str, creative_id: str) -> str:
        data = {
            "name": name,
            "adset_id": adset_id,
            "creative": json.dumps({"creative_id": creative_id}),
            "status": "PAUSED",
        }
        res = self._req("POST", f"{self.ad_account_id}/ads", data=data)
        return res["id"]


# ---------- targeting helpers ----------

def build_targeting(
    *,
    geo_locations: list[str],
    age_min: int,
    age_max: int,
    genders: list[int],
    interests: list[dict] | None = None,
    custom_audiences: list[str] | None = None,
) -> dict:
    """Build a Meta targeting dict.

    geo_locations: list of country codes (e.g. ["HU"]).
    genders: [1] men, [2] women, [1, 2] both.
    interests: list of {"id": "<fb_interest_id>", "name": "..."} dicts.
    """
    targeting: dict[str, Any] = {
        "geo_locations": {"countries": geo_locations},
        "age_min": age_min,
        "age_max": age_max,
        "genders": genders,
        "publisher_platforms": ["facebook", "instagram"],
        "facebook_positions": ["feed", "marketplace"],
        "instagram_positions": ["stream", "explore"],
    }
    if interests:
        targeting["interests"] = interests
    if custom_audiences:
        targeting["custom_audiences"] = [{"id": cid} for cid in custom_audiences]
    return targeting


def ads_manager_url(business_id: str, ad_account_id: str, campaign_id: str | None = None) -> str:
    account_num = ad_account_id.replace("act_", "")
    base = f"https://business.facebook.com/adsmanager/manage/campaigns?act={account_num}&business_id={business_id}"
    if campaign_id:
        base += f"&selected_campaign_ids={campaign_id}"
    return base
