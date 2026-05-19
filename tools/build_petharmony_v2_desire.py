"""Build pipeline-ready YAML for the PetHarmony v2 Desire Test batch.

12 prompts = 4 desires (D1..D4) x 3 creatives (C1..C3).

Desires:
  D1 = sleep   (Végre aludni akarok)
  D2 = oldDog  (Régi kutyám vissza)
  D3 = noVet   (Nem akarok többé állatorvoshoz)
  D4 = natural (Természetes megoldást akarok)

Per the brief, aspect ratio is mixed:
  D3-C1, D3-C2, D4-C1, D4-C2 are 1:1
  the other 8 are 4:5

Each entry carries:
  - compliance = desire code  → bulk_image_gen writes <run>/<desire>/
  - avatar     = "petharmony_v2_desire"
  - aspect_ratio = "1:1" or "4:5" (per-prompt override added to the pipeline)
  - pid format = ph_v2_<desire>_C<N>

Brand-lock: petharmony jar at inputs/products/petharmony_jar.png (passed
as reference image to every call). Most prompts don't show the product
on-screen, so Gemini will simply ignore the reference for those.
"""
from __future__ import annotations

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "config" / "petharmony_v2_desire_prompts.yaml"

# (desire_code, creative_n, aspect_ratio, prompt_text)
PROMPTS = [
    # ----- D1: VÉGRE ALUDNI AKAROK -----
    ("D1", 1, "4:5",
     "Authentic UGC bedside smartphone photo at night, low warm light from bedside lamp only. "
     "Hungarian woman in her mid-40s lying in bed, exhausted face, hair messy, dark circles under eyes, "
     "looking down at the floor where her golden retriever or vizsla is sitting and aggressively scratching "
     "its belly with hind leg. Digital alarm clock visible on nightstand showing \"03:47\" in red digits. "
     "Soft shadows, real bedroom mess — blanket disheveled, glass of water, phone face-down. "
     "Authentic phone photo aesthetic, slight grain. NOT staged, NOT professional. Photo looks like the "
     "woman just woke up and took a quick photo out of exhaustion."),
    ("D1", 2, "4:5",
     "Authentic UGC ground-level close-up photo of dog's paw being licked obsessively in dim bedroom light. "
     "Visible saliva staining on golden fur between paw pads (rusty discoloration), raw irritated skin. "
     "Dog's silhouette blurred in background, just the paw and tongue in focus. Bedroom carpet visible. "
     "Soft moody night lighting from a single bedroom lamp. Slightly disturbing but NOT graphic. "
     "Smartphone macro photo quality, slight motion blur."),
    ("D1", 3, "4:5",
     "Authentic UGC smartphone photo from bedroom doorway perspective at night. Hungarian woman in her 40s "
     "sitting on the edge of a bed in pajamas, head in hands, looking exhausted and defeated. "
     "Behind her: empty pillow on the other side of the bed (partner has left to sleep elsewhere). "
     "On the floor next to bed: golden retriever scratching itself. Single warm lamp lighting from "
     "nightstand. Real Hungarian bedroom — IKEA-style furniture, family photo on nightstand. "
     "NOT staged — looks like a documentary moment of family stress."),
    # ----- D2: RÉGI KUTYÁM VISSZA -----
    ("D2", 1, "4:5",
     "Vertical split-screen authentic UGC smartphone photo. LEFT SIDE: Happy golden retriever 2 years ago, "
     "running joyfully in green Hungarian backyard, sunny day, healthy shiny coat, tongue out, eyes bright, "
     "full of energy — looks like a candid family photo from a happier time. RIGHT SIDE: Same dog today, "
     "lying on a bed indoors looking sad and tired, visible red irritated skin on belly, dull coat, "
     "missing fur patches, head down. Same dog, completely different energy. Thin white vertical divider "
     "in middle. Authentic phone photo aesthetic, NOT professional."),
    ("D2", 2, "4:5",
     "Authentic UGC photo from a family album style. Soft vintage filter aesthetic. Happy dog (golden "
     "retriever or vizsla) running through autumn leaves in a Hungarian park, mid-air, ears flapping, "
     "complete joy. Sunny golden hour lighting. The photo has slight imperfections — finger blur on edge, "
     "slightly off-center composition. Looks like a phone photo a dog owner snapped 2 years ago and saved "
     "on their camera roll. Bottom corner small text overlay in Hungarian: \"Tavaly októberben\"."),
    ("D2", 3, "4:5",
     "Authentic UGC smartphone photo. Hungarian park scene, spring afternoon, golden hour. A woman in her "
     "late 30s walking her healthy-looking dog (golden retriever or vizsla) off-leash in green grass. "
     "The dog is mid-run, tail up, ears alert, joyful. Woman has a relaxed happy smile — NOT posed, "
     "NOT staged — looks like a real moment caught between strides. Background: typical Hungarian "
     "residential park with trees. Slight motion blur on dog, perfect freeze on woman."),
    # ----- D3: NEM ÁLLATORVOS -----
    ("D3", 1, "1:1",
     "Top-down overhead authentic UGC smartphone photo of a Hungarian kitchen table. On the table: "
     "a calculator, multiple veterinary bills crumpled and stacked (some visible amounts in Hungarian "
     "forints: \"45.000 Ft\", \"38.000 Ft\", \"52.000 Ft\"), empty prescription medicine bottles, a "
     "half-finished dog food bag (generic, no specific brand visible), and a worried hand holding a coffee "
     "mug. Morning natural daylight from window. Real messy kitchen counter aesthetic. NOT professional "
     "flat lay — looks like an exhausted moment of reckoning."),
    ("D3", 2, "1:1",
     "Authentic UGC close-up photo of a hand holding a generic prescription bottle of corticosteroid pills "
     "(label blurred to be generic, no real brand visible). In background: dog visibly scratching its skin "
     "out of focus. The pill bottle is in sharp focus, dog is blurred symbolizing that the medication isn't "
     "really helping. Natural window light, kitchen counter setting. NOT staged commercial photography — "
     "looks like a moment of realization. Slight smartphone blur."),
    ("D3", 3, "4:5",
     "Authentic UGC smartphone photo, slightly out of focus. Hungarian woman in her 40s sitting at a "
     "kitchen table, calculator and bills spread out, hand pressed to her forehead in frustration. "
     "Behind her: dog visible through doorway, scratching on the floor. Warm afternoon light from window. "
     "Real Hungarian apartment setting. The image captures financial stress AND emotional exhaustion in "
     "one frame. NOT staged."),
    # ----- D4: TERMÉSZETES MEGOLDÁS -----
    ("D4", 1, "1:1",
     "Editorial flat lay photo on a white marble kitchen counter. Four small ceramic bowls arranged in a "
     "row, each containing one natural ingredient: 1) fresh pineapple chunks (representing bromelain), "
     "2) dried stinging nettle root pieces, 3) bright green leafy quercetin-source plants (like onion or "
     "apple), 4) a small clear glass vial of light amber liquid (representing plasma). Each bowl has a "
     "small handwritten Hungarian label card placed next to it. PetHarmony jar visible in the corner of "
     "the frame. Natural daylight from above, soft shadows. Clean minimalist editorial composition, warm "
     "earth tones. Photorealistic, not illustration."),
    ("D4", 2, "1:1",
     "Authentic editorial-style infographic photo. Clean white background. Center: a generic prescription "
     "pill bottle with red X mark crossing it out (subtle, not too aggressive). Around it in a circle: "
     "small icons/symbols representing side effects — a weight scale (weight gain), a liver outline "
     "(liver damage), water drop (excessive thirst), immune cell (suppressed immunity). On the other "
     "side, partially shown: PetHarmony jar with green checkmark and small natural ingredient icons "
     "(leaf, plant, drop). Editorial pharmacy aesthetic, soft natural lighting. NOT cartoon — looks like "
     "a science magazine photo."),
    ("D4", 3, "4:5",
     "Authentic UGC smartphone macro close-up photo. A person's hand (visible to wrist) holding up a "
     "generic dog food bag, finger pointing at small ingredient text on the back label. The label shows "
     "blurred text but readable enough to look like a real label. Background is blurred Hungarian kitchen "
     "with potted herbs visible. Natural window light. The photo captures a moment of discovery / "
     "investigation."),
]

DESIRE_LABEL = {
    "D1": "sleep",
    "D2": "oldDog",
    "D3": "noVet",
    "D4": "natural",
}

BRAND_LOCK = (
    "Product details (when visible): PetHarmony — clear plastic jar with black screw cap, white label "
    "with a blue dog graphic, prominent 'ALLERGIA' text and 'PetHarmony' wordmark, '60 puha rágótabletta'. "
    "Soft brown chewable tablets visible inside the jar."
)

NEGATIVE = (
    "Avoid: stock photo aesthetic, plastic skin, oversaturated colors, AI hands, distorted face, six "
    "fingers, perfect studio lighting, fake commercial smile, generic dog stock photo, brand logos other "
    "than PetHarmony, watermark, fake science labels, anything that looks like a polished advertisement. "
    "Authenticity rule: the image must look like a friend's WhatsApp photo, not an ad."
)


def build_full_prompt(prompt_text: str) -> str:
    return "\n\n".join([prompt_text, BRAND_LOCK, NEGATIVE])


def build_flat() -> dict:
    flat: dict = {}
    for desire, creative_n, aspect_ratio, prompt_text in PROMPTS:
        label = DESIRE_LABEL[desire]
        pid = f"ph_v2_{desire}_C{creative_n}"
        flat[pid] = {
            # compliance value = desire label → bulk_image_gen writes
            # <run>/<label>/<pid>.png subfolder.
            "compliance": label,
            "avatar": "petharmony_v2_desire",
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
