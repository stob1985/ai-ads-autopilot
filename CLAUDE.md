# Claude Code context — ai-ads-autopilot

This repo generates product ads end-to-end: Gemini Nano Banana 2 for still creatives, HeyGen for talking-head UGC video. Purpose is an interactive tutorial the owner walks through on camera, so **clarity beats cleverness** in code and copy.

## Three-level model

Users progress through three levels. Never mix them up.

1. **Level 1 — setup + static ads.** Entry points: `setup.py`, `generate.py --images`.
2. **Level 2 — HeyGen video.** Entry points: `setup.py --heygen-avatar`, `generate.py --video`.
3. **Level 3 — autopilot.** Entry point: `autopilot.py`.

When the user asks for "an ad," default to Level 1. Only reach for video or autopilot when they explicitly ask.

## Inputs contract

Every run expects:

- `inputs/creator.jpg` — user's face photo (for HeyGen photo avatar).
- `inputs/product.png` — product shot (passed as reference image to Gemini on every call — this is how the packaging stays accurate).
- A product name + 1-3 benefits (passed as CLI args or picked up from `products.yaml` in Level 3).

The AI generates the *creative angles* — hooks, headlines, tone. Do **not** ask the user for an "ad angle." That is the pipeline's job.

## Output contract

Every run writes to a timestamped folder under `ad-workspace/`:

```
ad-workspace/2026-04-17_143022/
├── campaign-brief.md      # the 4 creative briefs + ICP + tone
├── ad-1-<slug>.png        # 4 still ads
├── ad-2-<slug>.png
├── ad-3-<slug>.png
├── ad-4-<slug>.png
├── video-script.md        # (Level 2) the HeyGen script
└── video.mp4              # (Level 2) the rendered UGC video
```

Never overwrite a prior run — always a fresh timestamp.

## Skills

- `.claude/skills/ecomm-ads/SKILL.md` — the deep creative-strategy skill (4-phase research → brief). Invoke when the user wants Reddit/Amazon research folded into the brief, not for quick runs.
- `.claude/commands/generate-ad.md` — the `/generate-ad` slash command. Thin wrapper around `generate.py` that fills in sensible defaults.

## Style rules

- Stills commit to **one saturated color world**. Tell the model so every time.
- Headlines are **3-6 words, punchy fragments.** Not sentences.
- The product image is **always** passed as reference image #1 to Gemini. Never skip this.
- HeyGen scripts are **15-30s, first-person, one benefit per sentence.**

## Don't

- Don't build a web UI. This is intentionally CLI-only so the tutorial viewer can follow each command.
- Don't collapse the three levels into one mega-command. Each level is a separate chapter of the video.
- Don't ask the user to write copy. They supply inputs; the pipeline writes the copy.
