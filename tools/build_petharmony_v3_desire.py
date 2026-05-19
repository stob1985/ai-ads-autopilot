"""Build pipeline-ready YAML for the PetHarmony v3 Desire Test batch.

This batch rewrites all 12 prompts per Anthony Camacho's native-image rule:
- NO product (PetHarmony jar) in any frame
- NO text overlays
- NO posed human subjects centered in the shot
- focus is on the PROBLEM itself, captured like a Reddit r/DogAdvice phone snap

Desires (same as v2):
  D1 = sleep   (Végre aludni akarok)
  D2 = oldDog  (Régi kutyám vissza)
  D3 = noVet   (Nem akarok többé állatorvoshoz)
  D4 = natural (Természetes megoldást akarok)

Aspect ratio is still mixed per the brief — added as per-entry override.

The pipeline is now run WITHOUT --product-image so Gemini doesn't bias
toward including the jar.
"""
from __future__ import annotations

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "config" / "petharmony_v3_desire_prompts.yaml"

# (desire_code, creative_n, aspect_ratio, prompt_text)
PROMPTS = [
    # ---------- D1: VÉGRE ALUDNI AKAROK ----------
    ("D1", 1, "4:5",
     "Raw, unfiltered close-up smartphone photo of a dog's paw being licked obsessively, shot from very close "
     "(almost macro). Visible saliva-stained fur with rusty brown discoloration between the toes — this is the "
     "tell-tale sign every dog owner with allergies recognizes. Raw pink irritated skin visible between paw pads. "
     "Dim warm light from a single bedroom lamp at night. The dog's body is blurred in the background (couch or "
     "carpet visible). The photo is slightly tilted, slightly out of focus on the edges — looks like a worried "
     "owner just grabbed their phone and shot this. NO PRODUCT in frame. NO TEXT overlay. NO logo. Authentic "
     "shitty smartphone photo aesthetic, NOT professional. The kind of photo a real dog owner would post on "
     "Reddit r/DogAdvice at 3am."),
    ("D1", 2, "4:5",
     "Authentic phone-snapped photo from a bedside angle — the bottom of the bed visible in foreground (blurred "
     "white sheets), and beyond it on a carpet or rug, a dog (any breed — golden retriever, vizsla, mudi, or "
     "french bulldog) caught mid-scratch, hind leg raised, scratching its belly aggressively. Visible red patches "
     "on the belly skin, some hair loss. Dim warm yellowish light from a single nightstand lamp — the rest of the "
     "room is in shadow. Photo is slightly motion-blurred on the dog (because the scratching is fast). NOT staged "
     "— looks like the owner woke up, saw this, and snapped a photo in frustration/sadness. NO PRODUCT. NO TEXT "
     "overlay. NO model person in frame. Just the bed corner and the dog. Slight grain, slight phone-quality "
     "imperfection."),
    ("D1", 3, "1:1",
     "Extreme close-up smartphone photo of a dog's ear and side of head, the dog is mid-shake (motion blur on the "
     "ears as they flap). The visible inner ear is red, irritated, possibly with some brown waxy discharge. "
     "Owner's hand barely visible in corner, holding the dog's head still. Living room background blurred (TV "
     "light or warm lamp). Natural indoor lighting, not bright. Looks like the owner finally caught the dog "
     "mid-head-shake to inspect what's wrong. NO PRODUCT. NO TEXT. NO logo. Authentic worried-owner phone snap "
     "aesthetic. The kind of photo someone would send to their vet via text asking 'is this serious?'."),
    # ---------- D2: AKAROM HOGY A KUTYÁM ÚJRA Ő LEGYEN ----------
    ("D2", 1, "1:1",
     "Raw smartphone photo of a small to medium-sized dog (french bulldog, beagle, or labrador) lying on its back "
     "on a regular home couch, exposing its belly. The belly shows distinctive allergy patches — rosacea-like red "
     "blotchy skin, some areas with thin or missing fur, slightly inflamed appearance. The pose is the kind of "
     "'show me your belly' moment dogs naturally do. Background is a normal lived-in living room — blanket on "
     "couch, maybe a TV remote, normal Hungarian home. Indoor warm afternoon lighting through window. NOT a posed "
     "studio shot — the dog is just chilling, and the owner photographed the visible problem. NO PRODUCT in "
     "frame. NO TEXT overlay. NO logo. The image looks like exactly what a worried owner would post on Reddit "
     "asking 'is this normal? what can I do?'. Slight phone blur and grain."),
    ("D2", 2, "4:5",
     "Authentic smartphone photo of a tennis ball or rope toy lying alone on a carpet or wood floor in a normal "
     "home. Out of focus in the background: a dog (any breed) lying down with its head on its paws, looking "
     "listless, not interested in the toy. Maybe the dog is half-heartedly looking at the toy but won't get up. "
     "Natural afternoon light from window. The composition emphasizes the abandoned toy with the unmotivated dog "
     "in the background. NOT staged — feels like the owner threw the toy expecting the dog to play, and the dog "
     "didn't react. NO PRODUCT. NO TEXT overlay. NO model person. Slight phone blur. The kind of melancholic "
     "phone-photo a sad dog owner would post with caption 'he doesn't even want to play anymore'."),
    ("D2", 3, "4:5",
     "Smartphone photo of a phone or laptop screen displaying an old photo album or Instagram of the SAME dog "
     "from 2 years ago — bright, healthy, running in autumn leaves in a park, energetic, full of life. The screen "
     "is the focus, but in the slightly out-of-focus foreground/edge of the frame, we can see the actual current "
     "dog lying on a couch in the present, looking dull-coated and tired (only partially visible, blurred). The "
     "contrast is implied not stated — past photo on screen vs current dog blurred in real life. Natural indoor "
     "lighting. NOT a split-screen composition — just a photo of a screen showing the past, with the present "
     "hinted at in the background. NO PRODUCT. NO TEXT overlay. NO logo. Authentic moment of nostalgic comparison."),
    # ---------- D3: NEM ÁLLATORVOS ----------
    ("D3", 1, "1:1",
     "Top-down smartphone photo (taken from above) of a Hungarian kitchen table or kitchen counter covered with "
     "crumpled and folded paper veterinary bills / invoices / receipts. Multiple papers visible — some folded, "
     "some flat, with visible Hungarian text reading 'Számla', 'Állatorvosi rendelő', and visible amounts like "
     "'45.000 Ft', '38.000 Ft', '52.000 Ft' partially readable. Mixed in: empty white prescription pill bottles "
     "tipped over, maybe a folded prescription paper. A coffee mug at the edge of the frame. Morning natural "
     "light from window. NOT a flat lay — this is a real messy scene of someone tallying up months of vet costs. "
     "NO PRODUCT (no PetHarmony). NO TEXT overlay added. The text is just on the receipts themselves naturally. "
     "Authentic phone-snap from above, slight angle."),
    ("D3", 2, "4:5",
     "Close-up smartphone photo of a small empty prescription pill bottle (corticosteroid or antihistamine — "
     "generic looking, no specific brand visible) lying on a kitchen counter or bathroom counter, tipped over on "
     "its side. The cap is off, the bottle is empty. Behind the bottle slightly out of focus: a dog visible from "
     "the side, sitting and scratching its ear or neck (because the medication is gone and not really working). "
     "Natural indoor lighting. The composition emphasizes the empty bottle in focus, dog scratching out of focus "
     "— implying 'we ran out of meds and it's still happening'. NO PRODUCT (no PetHarmony jar). NO TEXT overlay. "
     "NO logo. Authentic frustrated-owner photo aesthetic."),
    ("D3", 3, "4:5",
     "Authentic phone-snapped photo from the perspective of someone sitting in a veterinary clinic waiting room. "
     "In the foreground (lower part of frame, slightly blurred): the corner of an exam table or the photographer's "
     "lap with a leash. In the background (sharp focus): an empty veterinary waiting room with a 'Pénztár' or "
     "'Recepció' sign visible in Hungarian. Fluorescent overhead lighting. Maybe another anxious dog owner with "
     "their dog visible in the distance. NOT staged — just a moment captured while waiting for the umpteenth "
     "appointment. NO PRODUCT. NO TEXT overlay. NO logo. The fluorescent light gives it that distinct 'clinic' "
     "feeling everyone recognizes. Slight phone grain."),
    # ---------- D4: TERMÉSZETES MEGOLDÁS ----------
    ("D4", 1, "1:1",
     "Extreme close-up macro smartphone photo of a generic dog food bag's ingredient label (no specific brand "
     "name visible — generic looking commercial pet food bag). A finger is pointing at specific words in the "
     "ingredient list — the words 'BHA', 'BHT', or 'ethoxyquin' are barely visible in the small ingredient text. "
     "The finger is in sharp focus, the rest of the label is slightly blurred. Natural kitchen window light. The "
     "composition is intimate and investigative — like the photographer just discovered something disturbing. "
     "NO PRODUCT (no PetHarmony). NO TEXT overlay added. The text is just the natural ingredient list on the bag. "
     "The vibe: 'I read the label for the first time and oh god'."),
    ("D4", 2, "1:1",
     "Photo from a slight overhead angle of a wooden kitchen cutting board or marble counter. On the LEFT side: a "
     "small pile of white prescription pills (generic looking, no brand) and an empty pill bottle tipped over. On "
     "the RIGHT side, naturally arranged (NOT in a perfect line): a fresh piece of pineapple, some dried stinging "
     "nettle root pieces, a small bunch of fresh quercetin-source greens (like a piece of onion or fresh apple), "
     "and a small glass bottle with light amber liquid. The composition naturally divides the image into "
     "'synthetic vs natural' without a hard line. Soft natural morning light from window. NOT a staged commercial "
     "photo — looks like someone laid these out to decide between the two paths. NO PRODUCT (no PetHarmony jar). "
     "NO TEXT overlay added. Authentic phone photo with slight imperfection."),
    ("D4", 3, "4:5",
     "Authentic smartphone photo of a fresh pineapple sitting on a wooden cutting board in a Hungarian kitchen, "
     "with some dried herbs (nettle, fresh greens) arranged casually next to it — NOT a perfect flat lay. Morning "
     "natural light from window. In the slightly blurred foreground edge: a curious dog's nose or head visible, "
     "sniffing at the ingredients (just barely in frame). Warm earth tones, natural and homely. NOT a staged food "
     "photography shot — just a moment of preparing something for the dog. NO PRODUCT (no PetHarmony jar). NO "
     "TEXT overlay added. The vibe is 'natural healing, made at home, transparency'."),
]

DESIRE_LABEL = {
    "D1": "sleep",
    "D2": "oldDog",
    "D3": "noVet",
    "D4": "natural",
}

# No brand-lock this time — the prompts explicitly exclude the product.

NEGATIVE = (
    "Avoid: stock photo aesthetic, polished commercial photography, magazine cover composition, editorial "
    "lighting, plastic skin, oversaturated colors, AI hands, distorted face, six fingers, any product packaging "
    "or jar visible in frame, any brand name or logo, any text or caption overlay on the image, posed human "
    "model centered in shot, perfect symmetrical composition. The image MUST read like a worried dog owner "
    "snapped a quick phone photo and posted it on Reddit, NOT like an ad."
)


def build_full_prompt(prompt_text: str) -> str:
    return "\n\n".join([prompt_text, NEGATIVE])


def build_flat() -> dict:
    flat: dict = {}
    for desire, creative_n, aspect_ratio, prompt_text in PROMPTS:
        label = DESIRE_LABEL[desire]
        pid = f"ph_v3_{desire}_C{creative_n}"
        flat[pid] = {
            "compliance": label,           # → run_dir/<label>/ subfolder
            "avatar": "petharmony_v3_native",
            "desire": desire,
            "desire_label": label,
            "creative": creative_n,
            "aspect_ratio": aspect_ratio,
            "full_prompt": build_full_prompt(prompt_text),
        }
    return flat


def main() -> None:
    flat = build_flat()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(yaml.safe_dump(flat, allow_unicode=True, sort_keys=False, width=140, default_flow_style=False), encoding="utf-8")
    print(f"wrote {OUT} ({len(flat)} prompts)")
    from collections import Counter
    print("by desire:", dict(Counter(v["desire"] for v in flat.values())))
    print("by aspect_ratio:", dict(Counter(v["aspect_ratio"] for v in flat.values())))


if __name__ == "__main__":
    main()
