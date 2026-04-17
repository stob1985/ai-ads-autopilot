---
description: Generate a full ad bundle — 4 stills + 1 UGC video — from a product name and benefits. Uses inputs/creator.jpg and inputs/product.png.
argument-hint: <product name> — <benefits, comma-separated>
---

Run the full ai-ads-autopilot pipeline for: $ARGUMENTS

Steps:

1. **Parse the input.** Split `$ARGUMENTS` on the first em-dash, en-dash, or " -- ". Everything before = product name, everything after = benefits. If no separator, prompt the user for the benefits.

2. **Check inputs.** Verify both files exist:
   - `inputs/creator.jpg` (or `.png`/`.webp`)
   - `inputs/product.png` (or `.jpg`)
   If either is missing, tell the user exactly which file to add and stop. Do not try to proceed.

3. **Check keys.** If `.env` does not exist or `ANTHROPIC_API_KEY` / `GEMINI_API_KEY` / `HEYGEN_API_KEY` is missing, run `python setup.py` and let the user fill them in.

4. **Generate.** Run the full pipeline (images + video) in one shot:

   ```bash
   python generate.py --images --video \
       --product "<PRODUCT>" \
       --benefits "<BENEFITS>"
   ```

5. **Report.** When it finishes, show:
   - The run folder path.
   - Each ad image file name with its headline (read from `campaign-brief.md`).
   - The script used for the video.
   - The final `video.mp4` path.
   Offer to open the folder (`open <run_dir>` on macOS).

Do **not** ask the user for an "angle" or headline — the pipeline writes those. Only ask for things the user must supply: product name, benefits, and the two photos.

For the deep research flow (Reddit/Amazon mining, competitor ad scraping, Tavily reference images), invoke the `ecomm-ads` skill instead of this command. That path takes ~5 minutes and produces a richer brief; this command is the 60-second version.
