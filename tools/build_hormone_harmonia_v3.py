"""Build pipeline-ready YAML for the v3 Hormone Harmonia batch.

30 prompts total = 10 doctor_revelation + 10 cortisol_belly + 10 summer.

Each prompt gets:
- `compliance` set to the angle name → routes into `<run>/<angle>/` subfolder
- `avatar` set to "hormone_harmonia_v3" → tells build_filename to use a tidy
  pid-only filename like `doctor_revelation_v3_01.png`
- the user-supplied prompt text + brand-lock + user-supplied negative suffix

Run from the repo root:
    python tools/build_hormone_harmonia_v3.py
"""
from __future__ import annotations

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "config" / "hormone_harmonia_v3_prompts.yaml"

DR_PROMPTS = [
    "Photorealistic collage layout showing 5 different doctor offices in a 2x3 grid format (5 photos + 1 text panel), top-down view from a frustrated woman's perspective in each clinic. Each photo shows a different Hungarian/Eastern European doctor (varied ages 40-65, mix male/female, white coats) at their desks, dismissive body language, looking at paperwork not the patient. Bottom-right panel: bold red text on white background \"5 ORVOS. 18 HÓNAP. SEMMI.\" Warm hospital lighting, slightly desaturated, documentary photography style. NOT a stock photo aesthetic — looks like real medical encounters. No identifying logos. 1:1 ratio.",
    "Close-up overhead photo of a tablet/iPad screen displaying a clean medical infographic with the title \"6 HORMON 40 FELETT\" in Hungarian. The infographic shows 6 hormone circles labeled in Hungarian: \"KORTIZOL, ÖSZTROGÉN, PROGESZTERON, INZULIN, PAJZSMIRIGY, DHEA\" connected by arrows in a circular flow diagram. The tablet rests on a wooden desk with a coffee cup, reading glasses, and an open medical journal nearby. Natural window light from the left. Real medical research aesthetic, NOT cartoonish. Slight muted color palette (sage green, dusty rose, navy accents). 1:1 ratio.",
    "Authentic UGC-style photo of a warm, intelligent-looking female endocrinologist (Hungarian appearance, 45-55, brunette hair in a low bun, wire-rim glasses, white coat over navy blouse) sitting at her desk explaining something with her hands. Behind her, a wall of medical textbooks and a small framed diploma. She makes eye contact directly with the camera, gentle expression. Soft natural light from a window. The image should feel like a video frame from a Hungarian medical TV interview. NOT staged stock photography. 1:1 ratio.",
    "Editorial photo of a Hungarian woman (50, natural hair with gray streaks, no makeup, comfortable home setting) sitting at her kitchen table holding a paper printout, looking down at it with surprised realization. Large white bold text overlay on the upper third: \"88%\" and below in smaller text \"a 40+ nőknek hormonális egyensúlyhiánya van\". Bottom of image: \"Csak 12% kap diagnózist.\" in red. Morning light through kitchen window. Documentary style, real-life moment. 1:1 ratio.",
    "Macro photo of a doctor's handwritten prescription note in Hungarian, slightly crumpled, lying on a wooden table. The handwriting reads: \"Diagnózis: stressz. Próbáljon meditálni.\" (Diagnosis: stress. Try meditating.) Next to it: a glass of water, a half-empty packet of generic painkillers. Bottom-right corner of the image: handwritten red text overlay \"EZ NEM A MEGOLDÁS.\" Warm desk lamp light, shallow depth of field on the prescription. Conveys frustration, dismissal. 1:1 ratio.",
    "Top-down photo of a woman's hand (50ish, natural unmanicured nails, wedding ring visible) holding open a Hungarian medical book to a page titled \"MENOPAUZA ÉS HORMONÁLIS EGYENSÚLY\". Her finger underlines a key sentence. Next to the book: a notebook with her own handwriting in Hungarian \"6 hormon? Senki nem mondta...\" (6 hormones? No one told me...) and a steaming cup of tea. Morning light. Documentary still life. 1:1 ratio.",
    "Clean editorial-style image with a soft sage-green background. Top of image: a small circular photo of a friendly female Hungarian endocrinologist (50, professional). Below in large elegant serif Hungarian text: \"Magyar orvosok átlagosan 4 órát tanulnak menopauzáról 26 év képzés alatt.\" Below in smaller italic text: \"– Dr. K. M., endokrinológus\". Bottom: small Hungarian text \"Forrás: orvosi képzési tanterv 2024\". Looks like a screenshot from a Hungarian health magazine, NOT an ad. 1:1 ratio.",
    "Photorealistic image of a modern Hungarian research lab interior with one female scientist (45, lab coat, gloves) examining a sample under a microscope. Background: shelves with labeled bottles of natural extracts (ashwagandha, maca, vitex visible on small handwritten labels in Hungarian). Cool blue-white lab lighting. Bottom of image: white bold text bar \"12 HATÓANYAG. TUDOMÁNYOSAN VIZSGÁLVA.\" in Hungarian. Looks like a still from a documentary about natural medicine research, NOT pharma marketing. 1:1 ratio.",
    "Photo of a tablet screen showing what appears to be a Hungarian scientific abstract/paper. Title visible: \"Adaptogén gyógynövények hatása a női hormonháztartásra 40 év felett\". Author byline: \"Dr. Kovács A., Semmelweis Egyetem\". Abstract paragraph visible with words highlighted in yellow: \"ashwagandha\", \"maca\", \"kortizol\", \"ösztrogén\". Tablet rests on a wooden home office desk with a printed copy and pen next to it. Side natural light. Realistic, NOT mockup. 1:1 ratio.",
    "Authentic UGC photo of a Hungarian woman (52, brunette with natural gray streaks, no makeup, wearing a beige knit sweater) sitting alone at a cozy cafe table, reading something on her phone with deep concentration. Steam rises from her coffee. Phone screen visible: a Hungarian article titled \"Hormonális egyensúly 40+ – amit nem tanítanak az orvosi egyetemen\". Soft afternoon light through the cafe window. Like a candid friend-taken photo, NOT stock photography. 1:1 ratio.",
]

CB_PROMPTS = [
    "Photorealistic top-down kitchen counter scene with multiple \"failed diet\" items arranged: a closed protein shake bottle, a half-eaten salad in a bowl, a kitchen scale, a meal plan printout in Hungarian crossed out with red marker. In the center: a single white plate with a small bold text overlay \"12 ÉV. 18 DIÉTA. 0 EREDMÉNY.\" (12 years. 18 diets. 0 result.). Warm morning light from above. Documentary style, like a real Hungarian woman's kitchen. 1:1 ratio.",
    "Clean infographic on a soft cream background with a stylized illustration of a female silhouette (from the side, no body shaming, neutral pose). An arrow from \"STRESSZ\" at the top points to \"KORTIZOL ↑\" then to \"INZULIN ↑\" then to \"HASI ZSÍR ↑\". All Hungarian text. Bottom of image: bold text \"EZ HORMONÁLIS. NEM KALÓRIA-KÉRDÉS.\" with a small subtitle \"12 hatóanyag, ami segíthet.\" Editorial magazine aesthetic, NOT cartoonish. 1:1 ratio.",
    "Photorealistic still life of a pair of well-worn women's running shoes (size ~38, neutral colors) sitting next to a stopwatch reading \"00:00\", on a wooden bench in what appears to be a home gym corner. Slight dust on the equipment in the background. Bottom-left corner of the image: handwritten note in Hungarian \"5 év edzés. Nem fogytam.\" Soft natural light from a window. Conveys quiet resignation, NOT despair. 1:1 ratio.",
    "Top-down photo of a woman's hand pointing to a printed page from a Hungarian health magazine showing a clear simple illustration of the female endocrine system with key glands labeled in Hungarian (mellékvese, pajzsmirigy, petefészek). Her finger rests on \"MELLÉKVESE → KORTIZOL\". On the side: a coffee cup, reading glasses, a notebook with her notes. Editorial still life, soft daylight. 1:1 ratio.",
    "Authentic candid photo of two Hungarian women in their late 40s sitting at a cozy cafe table, both in casual clothes (cardigans, scarves), leaning in conversation. One is gesturing with her hand, the other listens with surprised realization. Coffee cups, slice of cake. Window light. Captured like an honest moment between friends discussing women's health. Bottom text overlay (small, clean): \"Bárcsak 10 éve tudtam volna.\" (I wish I'd known 10 years ago.) 1:1 ratio.",
    "Two-panel side-by-side photo (split image). Left panel: clean fridge interior with healthy food (vegetables, eggs, yogurt). Right panel: same Hungarian woman's silhouette from behind looking at the fridge at 11pm, kitchen lights low. Both panels with caption overlay in Hungarian: LEFT \"Nem azért, amit eszem...\" (Not because of what I eat...) RIGHT \"...hanem ahogy a testem feldolgozza.\" (...but how my body processes it.) Editorial photojournalism style. 1:1 ratio.",
    "Magazine-style quote card on a warm dusty-pink background. Center: large elegant serif Hungarian text \"A 40+ nők haspuffadása 80%-ban kortizolból, NEM kalóriából származik.\" Below in smaller text: \"– Dr. Sarah Gottfried, hormon szakorvos (magyarra fordítva)\". Top corner: small framed photo of a professional woman doctor. Bottom: small Hungarian footer \"Forrás: 'The Hormone Cure' (2013)\". Looks like a screenshot from a Hungarian women's health magazine, NOT an ad. 1:1 ratio.",
    "Authentic UGC bathroom photo of a Hungarian woman (50, natural hair messy from sleep, wearing a comfortable beige robe) standing in front of a mirror in soft morning light. She's NOT looking at her body — she's looking at her reflection's eyes with calm realization, holding a glass of water and a Hormone Harmonia bottle. No body comparison shots, no shame. Just a quiet decisive morning moment. Bottom small text: \"Reggel 6:47. Új kezdet.\" 1:1 ratio.",
    "Clean editorial top-down photo of 3-4 small wooden bowls on a linen tablecloth, each holding a different natural ingredient: ashwagandha powder (golden-brown), maca powder (light tan), vitex berries (dark purple), brokkoli sprouts (bright green). Each bowl has a small handwritten Hungarian label tag: \"Ashwagandha – kortizol\", \"Maca – energia\", \"Vitex – ösztrogén\", \"Brokkoli – DIM\". Natural morning light from the side. NOT a stock photo aesthetic, looks like a real kitchen herbalist's tabletop. 1:1 ratio.",
    "Editorial-style infographic on a soft sage-green background. Title at top in elegant Hungarian: \"12 HÉT – AMIT VÁRHATSZ\". Horizontal timeline with 4 milestones, each with a tiny illustrative icon: WEEK 2 (alvás ikon) \"Mélyebb alvás\", WEEK 4 (étel ikon) \"Csökkenő cukorvágy\", WEEK 8 (test ikon) \"Lapuló has\", WEEK 12 (smile ikon) \"Visszanyert energia\". Magazine layout. NOT a typical \"before/after\" ad — more like a wellness journal infographic. 1:1 ratio.",
]

SU_PROMPTS = [
    "Top-down photo of a Hungarian wall calendar opened to May 2026, with red marker circles around today's date and a separate circle around August 1st with handwritten note in Hungarian \"Strand. Készen kell lennem.\" (Beach. I need to be ready.) Around the calendar: a coffee cup, a Hormone Harmonia bottle, reading glasses. Warm morning kitchen light from the side. Documentary style, NOT a marketing flat-lay. 1:1 ratio.",
    "Photorealistic still life on a wooden floor: a pair of new sand-colored women's beach sandals (still with tags), oversized sunglasses, a folded straw hat, and a Hormone Harmonia bottle next to them. Light streaming in from a nearby window. Bottom text overlay in soft serif Hungarian: \"84 nap. Ezért készülök.\" (84 days. That's what I'm preparing for.) Conveys hopeful anticipation, NOT urgency-panic. 1:1 ratio.",
    "Authentic UGC photo of a Hungarian woman (48, natural makeup, casual linen shirt) sitting on her sunny terrace in late spring, holding a steaming mug of tea, looking out toward her garden. On the small table next to her: a notebook open with a handwritten Hungarian list \"Nyári célok:\" (Summer goals:) and below it 3 bullet points: \"1. Aludni 8 órát\", \"2. Bikini bátorság\", \"3. Újra felismerni magam\". Soft golden hour light. Like a candid friend-taken moment. 1:1 ratio.",
    "Photorealistic close-up of a woman's hands (50ish, no body comparison) holding a printed photograph from approximately 2015 showing her smiling at Lake Balaton (Balatonfüred sign visible) wearing a summer dress, laughing. Background: today's hands holding the photo, on a kitchen table, wedding ring visible. Soft window light. Bottom-right corner small text: \"Idén újra. Csak másképp.\" (Again this year. Just differently.) Conveys nostalgia + determination, NOT regret. 1:1 ratio.",
    "Clean infographic on a sandy-beige background. Horizontal timeline with markers: \"MÁJUS 14 – MA\", \"JÚNIUS 1 – Első jelek\", \"JÚLIUS 1 – Felére csökkent puffadás\", \"AUGUSZTUS 1 – KÉSZ\". Each marker has a tiny sun icon that progressively gets brighter from left to right. Bottom: bold Hungarian text \"12 HÉT. PONT ANNYI, AMENNYI KELL.\" Magazine layout aesthetic, NOT cartoonish. 1:1 ratio.",
    "Two-panel image (split horizontally, not too dramatic). TOP panel: a Hungarian woman (50) in a baggy beige cardigan and jeans standing on a beach, looking out at the water, body partially turned away, melancholic expression. Caption overlay: \"Tavaly – elbújtam.\" (Last year – I hid.) BOTTOM panel: same woman in a similar pose but in a flowy summer dress, calm confident expression, looking forward. Caption: \"Idén – tervezem a változást.\" (This year – I'm planning the change.) NOT a typical before/after, more like emotional storytelling. 1:1 ratio.",
    "Authentic UGC top-down photo of a Hungarian woman's morning routine table: a half-glass of water, 3 Hormone Harmonia capsules in a small dish, an open journal with Hungarian handwriting \"Nap 1. Április 14.\" (Day 1. April 14.), a pen, sunglasses ready for the day. Soft morning light. Bottom small text: \"84 nap visszaszámlálás kezdődik.\" (84-day countdown begins.) Conveys quiet commitment, NOT urgency. 1:1 ratio.",
    "Photorealistic photo from behind, showing a Hungarian woman (50, natural body, NOT model-thin) walking on a Balaton beach in a flowy summer dress and straw hat, sun setting in front of her. NO body shaming angle, NO \"after photo\" feel — just a peaceful walking-toward-the-sun moment. Bottom text overlay in soft Hungarian: \"Az út már elkezdődött.\" (The path has already begun.) Conveys hope, NOT body comparison. 1:1 ratio.",
    "Photorealistic top-down still life of a packed beach bag opened on a wooden table: a polka-dot red one-piece swimsuit (NOT bikini, modest 40+ appropriate), a paperback book in Hungarian, sunscreen tube, sunglasses, Hormone Harmonia bottle nestled in the corner. Bottom text overlay handwritten style: \"Idén nem maradok ki.\" (This year I'm not missing out.) Sunny window light, summer anticipation mood. 1:1 ratio.",
    "Close-up photo of a smartphone lock screen showing a custom countdown widget reading \"84 NAP\" in large numbers, with subtitle \"Augusztus 1 – Balaton\". Background: the phone resting on a beach-themed magazine page in Hungarian. Around the phone: a pair of new sunglasses, a Hormone Harmonia bottle, small succulent plant. Soft afternoon natural light. Conveys gentle daily reminder, NOT alarm-urgency. 1:1 ratio.",
]


BRAND_LOCK = (
    "Product details (when visible): Hormone Harmonia™ — amber glass bottle with a pink/dusty-rose cap, "
    "white cardboard box with a Japanese wave pattern. Label reads 'HORMONE HARMONIA' with '72 vegan kapszula'."
)

NEGATIVE = (
    "Avoid: stock photo aesthetic, watermark, brand logos, distorted text, cartoon, illustration where not asked, "
    "low quality, blurry, overexposed, fake plastic smile, model pose, airbrushed plastic skin, "
    "isolated body part close-ups, weight loss claims, kg numbers, before/after body comparison, "
    "shaming or fear-based framing."
)


def build_full_prompt(prompt_text: str) -> str:
    return "\n\n".join([prompt_text, BRAND_LOCK, NEGATIVE])


def build_flat() -> dict:
    flat: dict = {}
    blocks = [
        ("doctor_revelation", DR_PROMPTS),
        ("cortisol_belly", CB_PROMPTS),
        ("summer", SU_PROMPTS),
    ]
    for angle, prompts in blocks:
        for i, prompt_text in enumerate(prompts, start=1):
            pid = f"{angle}_v3_{i:02d}"
            flat[pid] = {
                # compliance value = angle name → bulk_image_gen writes to
                # <run>/<angle>/<pid>.png subfolder.
                "compliance": angle,
                "avatar": "hormone_harmonia_v3",
                "angle": angle,
                "variant": i,
                "full_prompt": build_full_prompt(prompt_text),
            }
    return flat


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    flat = build_flat()
    OUT.write_text(yaml.safe_dump(flat, allow_unicode=True, sort_keys=False, width=140, default_flow_style=False), encoding="utf-8")
    print(f"wrote {OUT} ({len(flat)} prompts)")
    from collections import Counter
    print("by angle:", dict(Counter(v["angle"] for v in flat.values())))


if __name__ == "__main__":
    main()
