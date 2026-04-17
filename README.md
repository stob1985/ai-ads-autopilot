# ai-ads-autopilot

Generate scroll-stopping product ads from a creator photo, a product photo, and a couple of benefits. Start with static images (Gemini Nano Banana 2), then progress to talking-head UGC videos (HeyGen), then flip it on autopilot.

No UI. Pure CLI. Designed so you can follow along with the video.

---

## What you get

| Level | Command | What happens | Output |
|---|---|---|---|
| **1** | `python setup.py` | Interactive wizard: grabs API keys, validates them, saves `.env` | `.env` ready |
| **1** | `python generate.py --images` | Creator photo + product photo + benefits → 4 static ad creatives | `ad-workspace/<run>/ad-1…4.png` |
| **2** | `python generate.py --video` | Picks the best still + a script → HeyGen talking UGC video | `ad-workspace/<run>/video.mp4` |
| **3** | `python autopilot.py` | Loops: every N hours, pulls new briefs and ships a fresh batch | rolling output in `ad-workspace/` |

The three levels map to the three chapters of the video walkthrough.

---

## Level 1 — Keys & first still ad

### 1. Clone and install

```bash
git clone https://github.com/Samin12/ai-ads-autopilot.git
cd ai-ads-autopilot
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Drop your inputs in `inputs/`

Two files — that is it.

```
inputs/
├── creator.jpg   # a clean photo of you (or your avatar's face)
└── product.png   # the product, ideally on a plain background
```

(See `inputs/README.md` for photo tips — front-facing, good lighting, no sunglasses.)

### 3. Run the setup wizard

```bash
python setup.py
```

It will:

1. Prompt for each API key (Gemini, Anthropic, HeyGen).
2. Link you straight to the sign-up page if you are missing one.
3. Test each key with a tiny live call so you know it actually works.
4. Write `.env` for you.

### 4. Ship your first static ad

```bash
python generate.py --images \
    --product "Matcha protein stick" \
    --benefits "30g plant protein, zero crash, tastes like dessert"
```

What happens under the hood:

1. **Brief** — Claude reads your benefits, picks a tone, writes 4 creative briefs (hook, headline, visual direction) grounded in the `ecomm-ads` skill.
2. **Images** — Gemini Nano Banana 2 generates all 4 ads using your `product.png` as a reference image on every call so the packaging stays pixel-accurate.
3. **Output** — timestamped folder under `ad-workspace/` with the images plus a `campaign-brief.md` you can hand to a designer or paste into Meta Ads Manager.

---

## Level 2 — HeyGen video

Once you have a still ad you love, turn it into a UGC-style talking video.

### 1. One-time: register your photo avatar

```bash
python setup.py --heygen-avatar
```

This uploads `inputs/creator.jpg` to HeyGen, waits for the photo avatar to finish training, and writes the `HEYGEN_AVATAR_ID` + a default `HEYGEN_VOICE_ID` back into `.env`.

(You can skip this if you already have an avatar id — paste it into `.env` directly.)

### 2. Generate the video

```bash
python generate.py --video \
    --from-run 2026-04-17_143022    # reuse the brief + images from Level 1
```

Or do both levels in one go:

```bash
python generate.py --images --video \
    --product "Matcha protein stick" \
    --benefits "30g plant protein, zero crash, tastes like dessert"
```

What happens:

1. Claude writes a 15-30s UGC script from the winning creative brief.
2. HeyGen renders your photo avatar reading the script, with the product image overlaid as a B-roll shot.
3. The mp4 lands in `ad-workspace/<run>/video.mp4`.

---

## Level 3 — Autopilot

For when you stop wanting to touch it.

```bash
python autopilot.py --interval 6h --products products.yaml
```

`products.yaml` example:

```yaml
- name: Matcha protein stick
  benefits: 30g plant protein, zero crash, tastes like dessert
  product_image: inputs/products/matcha.png

- name: Hydration drops
  benefits: 2x the electrolytes, zero sugar, tastes like real lemon
  product_image: inputs/products/drops.png
```

Every interval the loop:

1. Picks the next product.
2. Runs the full Level 1 + Level 2 pipeline.
3. Stashes the output under `ad-workspace/<product>/<run>/`.
4. (Optional) posts the video to a webhook you configure — hand it off to Blotato, Zapier, n8n, whatever you ship with.

Stop it with `Ctrl+C` or `python autopilot.py --stop`.

---

## Using it from Claude Code

The repo ships a Claude Code slash command. With Claude Code open in this folder:

```
/generate-ad matcha protein stick — 30g plant protein, zero crash, tastes like dessert
```

Claude will run the creative brief + image + video pipeline for you, asking for the input photos if they are not already in `inputs/`. Full definition in [`.claude/commands/generate-ad.md`](.claude/commands/generate-ad.md).

The deep creative-strategy skill (4-phase research → brief → generate) is at [`.claude/skills/ecomm-ads/SKILL.md`](.claude/skills/ecomm-ads/SKILL.md).

---

## Repo layout

```
ai-ads-autopilot/
├── setup.py                # Level 1 wizard
├── generate.py             # Level 1 + 2 entry point
├── autopilot.py            # Level 3 loop
├── src/
│   ├── creative_brief.py   # Claude → 4 briefs
│   ├── image_gen.py        # Gemini Nano Banana 2
│   ├── heygen.py           # HeyGen API client (photo avatar + video generate)
│   ├── video_gen.py        # orchestrates brief → video
│   └── utils.py            # env loading, path helpers
├── inputs/                 # your creator + product photos (gitignored)
├── ad-workspace/           # generated output (gitignored)
└── .claude/
    ├── commands/generate-ad.md   # slash command
    └── skills/ecomm-ads/SKILL.md # deep research → brief skill
```

---

## Costs (rough, per 1 run)

| Step | Provider | ~Cost |
|---|---|---|
| Brief | Claude Sonnet | $0.02 |
| 4 still ads | Gemini Nano Banana 2 | $0.12 |
| 1 UGC video (~20s) | HeyGen | $0.30–1.00 |

Plan on ~$1 per fully-generated ad, less if you skip video.

---

## Troubleshooting

- **HeyGen "avatar not ready"** — photo avatar training takes 2–5 min. Re-run `python setup.py --heygen-avatar --wait`.
- **Gemini returns no image** — check your Gemini project has Nano Banana 2 enabled (`gemini-3.1-flash-image-preview`).
- **Wrong product in the output** — your `product.png` is probably low-res. Swap in a 2000px+ PNG with transparent or white background.

Inspired by [Samin12/Seedance-2.0-AI-UGC](https://github.com/Samin12/Seedance-2.0-AI-UGC) — same idea, simpler surface, HeyGen instead of Seedance.
