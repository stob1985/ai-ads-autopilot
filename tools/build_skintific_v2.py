"""Convert the v2 Skintific brief into pipeline-ready YAML.

Run from the repo root:
    python tools/build_skintific_v2.py

Outputs:
    config/skintific_prompts_v2_source.yaml   — verbatim record (id + metadata)
    config/skintific_prompts.yaml             — flat, pipeline-ready
"""
from __future__ import annotations

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "config" / "skintific_prompts_v2_source.yaml"
OUT = ROOT / "config" / "skintific_prompts.yaml"

# Fields per prompt:
# (id, avatar, angle, compliance_meta, expected_ctr, stop_mechanism,
#  overlay_top, overlay_bottom, overlay_style, prompt_text)

PROMPTS = [
    # === A1. INSECURITY-DRIVEN (10) ===
    ("ugc_insec_01", "efficient_perfectionist", "Pore discovery shock", "BURNER", "5-7%",
     "pore disgust trigger + mirror neuron shock",
     "Why is no one talking about this 😭", "B1G1 — $19.99",
     "white sans-serif with black drop shadow (Instagram Story aesthetic)",
     "Front-facing iPhone selfie in messy bathroom mirror, woman 32 white American with brown hair pulled back, NO MAKEUP, leaning close to mirror with finger pointing to enlarged pores on her nose, mouth slightly open in disgusted-shocked expression, harsh fluorescent overhead bathroom light flattening her skin, Skintific Alaska Volcano clay stick visible held in other hand near collarbone, raw unfiltered phone photo with slight grain, candid 7am bathroom energy, towel hanging blurred in background, NOT professional photography, 1:1"),
    ("ugc_insec_02", "sensitive_skin", "Visible texture frustration", "BURNER", "5-7%",
     "skin texture insecurity + age-based fear",
     "this skin texture??? at 27???", "buy 1 get 1 — $19.99",
     "yellow highlighter behind black bold handwritten text",
     "iPhone selfie macro of woman 27 Latina cheek skin showing visible bumpy texture and small clogged pores in harsh natural window light, finger from below pointing up to her cheek, raised eyebrow tired expression, no makeup, Skintific Alaska Volcano clay stick blurred in foreground bottom corner being held, looks like she just got out of bed, raw phone camera quality with motion blur, completely candid not posed, 1:1"),
    ("ugc_insec_03", "convenience_seeker", "Bedside table 2am scroll discovery", "META-SAFE", "4-6%",
     "FOMO + discovery + relatable insomnia scroll",
     "found this at 2am... ordered immediately", "$19.99 + got 2 free shipping idk",
     "TikTok caption style — white text with subtle drop shadow",
     "iPhone POV from bed, woman 28 Black American in white t-shirt lying on pillow at night, dim bedside lamp light, holding phone showing a Skintific Alaska Volcano clay stick product page on screen, surprised wide-eyes expression, hair in messy bun, sheets visible, looks like 2am late-night scroll, harsh phone screen glow on face, raw bedroom selfie aesthetic, slight grain, 1:1"),
    ("ugc_insec_04", "efficient_perfectionist", "Magnifying mirror horror", "BURNER", "5-7%",
     "pore horror + relatable mistake",
     "POV: you just bought a magnifying mirror", "B1G1 free — $19.99",
     "Instagram Reels caption — white impact font",
     "Selfie of woman 34 Asian American examining her face in 10x magnifying makeup mirror on bathroom counter, visible enlarged pores on nose and cheeks under harsh ring light, mouth open in concerned-disgusted expression pointing finger at her own pore, Skintific Alaska Volcano clay stick standing on counter next to mirror, raw iPhone selfie quality, completely unposed, 1:1"),
    ("ugc_insec_05", "sensitive_skin", "Concealer doesn't work anymore", "META-SAFE", "5-6%",
     "concealer relatability + emotional truth",
     "no amount of concealer hides texture", "skintific 2-pack: $19.99",
     "minimal white text, looks like Instagram caption screenshot",
     "iPhone selfie of woman 29 white with red rosacea-prone reactive cheeks, half her face has heavy concealer that's caking and patching over textured skin, the other half raw natural, frustrated tearful expression, harsh bathroom light, Skintific Alaska Volcano clay stick held up to camera in foreground, raw unfiltered phone photo, 1:1"),
    ("ugc_insec_06", "efficient_perfectionist", "Office bathroom panic", "META-SAFE", "4-6%",
     "professional anxiety + relatable timing fear",
     "before my 2pm presentation 💀", "B1G1 / $19.99",
     "iMessage screenshot aesthetic",
     "Selfie in corporate office bathroom mirror, woman 33 white American in business blazer, pointing in horror at chin breakout that just appeared, harsh fluorescent office lighting making skin look terrible, Skintific Alaska Volcano clay stick visible in her purse half-hidden, candid 'caught at work' phone photo energy, modern hotel-style bathroom tiles in background, raw phone quality, 1:1"),
    ("ugc_insec_07", "convenience_seeker", "Kid stole my mirror moment", "META-SAFE", "5-7%",
     "mom relatability + identity validation",
     "mom skin is REAL", "2 sticks $19.99 (im screaming)",
     "TikTok caption with emoji",
     "Bathroom selfie of mother 32 Latina, toddler hands visible reaching up at edge of frame, woman trying to look at her own clogged-pore nose in mirror, exhausted bags-under-eyes expression, no makeup, hair in messy bun, Skintific Alaska Volcano clay stick on counter behind her, raw iPhone candid mom-life photo, harsh morning light, 1:1"),
    ("ugc_insec_08", "sensitive_skin", "After workout flush + breakouts", "META-SAFE", "4-6%",
     "gym flush relatability + workout audience",
     "post workout face is humbling", "B1G1 — $19.99 thank god",
     "Instagram Story handwritten white text",
     "iPhone selfie of woman 26 mixed-race in sweaty gym tank top, flushed red post-workout face with visible breakouts and clogged pores on forehead, sweaty hair stuck to face, gym locker room mirror in background blurry, Skintific Alaska Volcano clay stick held up next to face, raw candid post-gym energy, 1:1"),
    ("ugc_insec_09", "efficient_perfectionist", "Sunday self-discovery", "META-SAFE", "4-5%",
     "weekend self-care relatability",
     "Sunday reset = humbling", "buy one get one $19.99",
     "Pinterest caption style minimal",
     "Selfie of woman 35 white American in cozy sweater on Sunday morning, soft window light, examining nose in handheld mirror with shocked surprise expression, finger pointing to discovered blackheads, Skintific Alaska Volcano clay stick on coffee table next to laptop and journal, raw weekend phone photo, completely candid, 1:1"),
    ("ugc_insec_10", "convenience_seeker", "Car visor mirror reality", "META-SAFE", "4-6%",
     "car/commute relatability + mom audience",
     "school pickup line revelations", "$19.99 — buy 1 get 1",
     "white sans serif with subtle shadow",
     "iPhone selfie POV in car visor mirror, woman 30 Black American in driver's seat parked, harsh midday sun through windshield, examining her chin breakouts and pore congestion in tiny mirror, frustrated expression, Skintific Alaska Volcano clay stick visible in cup holder, raw real-life phone photo aesthetic, 1:1"),

    # === A2. DISCOVERY/SECRET (8) ===
    ("ugc_disc_01", "efficient_perfectionist", "TikTok ordered me to buy", "META-SAFE", "5-7%",
     "social proof + algorithm trust",
     "tiktok made me buy this", "B1G1 free $19.99",
     "TikTok native caption font",
     "iPhone selfie of woman 31 white American in pajamas on couch, holding phone screen showing Skintific Alaska Volcano product page visible, other hand holding two unboxed Skintific clay sticks, mouth open in 'wait what' surprise, messy living room background with blanket, raw candid evening photo, soft warm lamp lighting, 1:1"),
    ("ugc_disc_02", "sensitive_skin", "Boyfriend doesn't know", "META-SAFE", "5-7%",
     "relationship humor + secret purchase relatability",
     "don't tell my boyfriend i did it again", "$19.99 for TWO 🫣",
     "iMessage aesthetic",
     "Selfie of woman 28 Asian American whispering toward camera with finger to lips, holding two Skintific Alaska Volcano clay sticks, conspiratorial look, bathroom counter behind her with other skincare visible, slight smile suggesting secret purchase, raw iPhone photo, soft bathroom light, 1:1"),
    ("ugc_disc_03", "convenience_seeker", "Amazon vs direct site savings", "BURNER", "5-7%",
     "insider info + savings reveal",
     "amazon: $24/each. direct site:", "B1G1 → $19.99 TOTAL",
     "yellow highlighter + red arrow drawn over",
     "iPhone POV looking down at desk with laptop showing Amazon page on left side and Skintific direct website on right, woman's hand pointing to price difference, two Skintific clay sticks unboxed on desk, dramatic gesture revealing hidden info, raw phone photo from above, harsh overhead light, 1:1"),
    ("ugc_disc_04", "efficient_perfectionist", "Esthetician told me to", "META-SAFE", "5-7%",
     "authority transfer (esthetician credibility)",
     "my esthetician told me to stop spending $80/visit", "she sent me here: $19.99 (B1G1)",
     "Instagram Story handwritten",
     "iPhone selfie of woman 36 white in athleisure, sitting in car after appointment, two Skintific Alaska Volcano clay sticks visible in passenger seat shopping bag, small knowing smile, hair in topknot, post-spa glow, raw candid phone photo afternoon light through windshield, 1:1"),
    ("ugc_disc_05", "sensitive_skin", "Reddit r/SkincareAddiction recommended", "META-SAFE", "4-6%",
     "community validation + skeptical-buyer trust",
     "reddit was right (rare)", "B1G1 / $19.99",
     "Reddit-inspired typography",
     "iPhone screenshot-style selfie, woman 25 mixed-race holding her phone showing a Reddit thread blurred in background, two Skintific Alaska Volcano clay sticks held up to camera, slight smile of validation, bedroom background blurred with fairy lights, raw evening selfie, 1:1"),
    ("ugc_disc_06", "convenience_seeker", "Hotel discovery moment", "META-SAFE", "4-5%",
     "travel/aspirational + budget-savvy",
     "packed these instead of the $200 spa kit", "B1G1 $19.99 = no regrets",
     "minimal white sans serif",
     "Selfie of woman 29 Latina in hotel bathrobe in chic boutique hotel bathroom, holding two Skintific clay sticks she packed, surprised happy expression, marble counter visible, raw vacation phone photo, soft hotel lighting, 1:1"),
    ("ugc_disc_07", "efficient_perfectionist", "Sister's recommendation", "META-SAFE", "4-5%",
     "social proof + family endorsement",
     "ordered 4 between us", "B1G1 = perfect for sisters $19.99",
     "casual handwritten",
     "Group selfie of two sisters 30 and 33 white American, both holding Skintific Alaska Volcano clay sticks toward camera, kitchen background, both laughing, golden hour light through window, raw family iPhone photo, candid not posed, 1:1"),
    ("ugc_disc_08", "sensitive_skin", "Dermatologist won't tell you", "BURNER", "6-8%",
     "anti-establishment + insider feeling",
     "what my derm won't recommend (she sells $200 serums)", "this: B1G1 $19.99",
     "yellow highlighter aesthetic",
     "iPhone selfie of woman 32 white in cozy reading chair, holding Skintific Alaska Volcano clay stick up to camera with raised conspiratorial eyebrow, warm lamp lighting evening, books in background blurred, raw candid living room photo, 1:1"),

    # === A3. SKEPTIC CONVERSION (7) ===
    ("ugc_skep_01", "efficient_perfectionist", "Bought as joke", "META-SAFE", "5-7%",
     "skeptic-to-believer relatability",
     "bought it ironically. JOKE'S ON ME.", "$19.99 / B1G1 free",
     "Twitter screenshot aesthetic",
     "iPhone selfie of woman 34 white American in bathroom, half-laughing-half-shocked expression, holding two unboxed Skintific Alaska Volcano clay sticks, eyebrows raised in 'okay fine' surrender, raw morning bathroom selfie, harsh overhead light, no makeup, 1:1"),
    ("ugc_skep_02", "sensitive_skin", "Expected garbage", "META-SAFE", "5-7%",
     "low-expectation reversal + price-quality surprise",
     "$19.99 for two? expected garbage.", "...i was wrong (B1G1)",
     "iMessage chat aesthetic",
     "iPhone selfie of woman 27 Black American mid-laugh shaking her head in disbelief, hand on her cheek showing visibly clearer skin, Skintific Alaska Volcano clay stick held up to camera, bedroom mirror selfie, warm lamp light, raw candid moment of realization, 1:1"),
    ("ugc_skep_03", "convenience_seeker", "Husband made fun of me", "META-SAFE", "5-6%",
     "relationship humor + vindication trigger",
     "my husband: 'another tiktok scam' — me:", "B1G1 / $19.99 / vindicated",
     "casual sans serif",
     "iPhone selfie of woman 31 Latina, sticking tongue out playfully at camera, holding two Skintific Alaska Volcano clay sticks like trophy, kitchen background with husband blurred laughing in distance, raw candid family photo, warm afternoon light, 1:1"),
    ("ugc_skep_04", "efficient_perfectionist", "I research everything", "META-SAFE", "4-5%",
     "due-diligence audience validation",
     "i research EVERYTHING. this passed.", "B1G1 deal: $19.99",
     "minimal academic-feel typography",
     "Selfie of woman 38 Asian American at desk surrounded by laptop and notebook with research notes, holding Skintific Alaska Volcano clay stick toward camera with reluctant smile, glasses pushed up, raw work-from-home photo, soft natural light, 1:1"),
    ("ugc_skep_05", "sensitive_skin", "13 products failed", "META-SAFE", "5-7%",
     "exhaustion validation + survivor identity",
     "13 products failed. one $19.99 deal worked.", "B1G1 — never going back",
     "Pinterest caption with white box",
     "iPhone selfie POV of woman 26 white pointing camera down at bathroom counter showing 5-6 half-used skincare bottles cluttered, central focus on two Skintific Alaska Volcano clay sticks, hand frustrated/defeated, raw overhead bathroom photo, harsh light, 1:1"),
    ("ugc_skep_06", "convenience_seeker", "Lazy girl test", "META-SAFE", "5-7%",
     "low-effort identity validation",
     "lazy girl skincare review:", "actually works?? B1G1 $19.99",
     "TikTok caption white text",
     "iPhone selfie of woman 28 mixed-race lying on bed in oversized t-shirt, holding Skintific Alaska Volcano clay stick lazily in one hand, surprised eyebrows raised expression, messy bedroom background, soft afternoon nap light, raw candid bedroom photo, 1:1"),
    ("ugc_skep_07", "efficient_perfectionist", "Marketing was suspicious", "META-SAFE", "5-6%",
     "ad-skepticism meta-acknowledgment",
     "the ads looked sketchy. it works.", "B1G1 / $19.99",
     "casual italics",
     "Selfie of woman 33 white American with raised skeptical eyebrow then breaking into reluctant smile, holding Skintific Alaska Volcano clay stick, kitchen counter background with coffee mug, raw morning photo, natural window light, 1:1"),

    # === B1. VS PREMIUM SKINCARE BRANDS (10) ===
    ("comp_brand_01", "efficient_perfectionist", "vs Sephora prices", "BURNER", "6-8%",
     "price-anchoring rage + savings shock",
     "Sephora: $68 — This: $19.99 (TWO)", "B1G1 — same ingredients btw",
     "yellow highlighter behind black bold + red strikethrough on '$68'",
     "iPhone POV looking down at Sephora black-and-white striped shopping bag on left side of frame, two Skintific Alaska Volcano clay sticks placed on right side, woman's hand making 'why?' gesture between them, harsh overhead light on white kitchen counter, raw flat-lay phone photo, 1:1"),
    ("comp_brand_02", "sensitive_skin", "vs Drunk Elephant", "BURNER", "6-7%",
     "buyer's remorse + competitor takedown",
     "spent $87 on this →", "← shouldve bought this. B1G1 $19.99",
     "two arrows pointing different directions, casual typography",
     "iPhone selfie of woman 29 white holding empty Drunk Elephant-style colorful skincare bottle in left hand and Skintific Alaska Volcano clay stick in right hand, eye-roll expression, bathroom counter background, raw candid bathroom photo, harsh overhead light, 1:1"),
    ("comp_brand_03", "convenience_seeker", "vs Glossier hype", "BURNER", "5-7%",
     "brand-loyalty shift + millennial reference",
     "Glossier mood died, this lives", "B1G1 → $19.99",
     "pink and red marker handwritten aesthetic",
     "iPhone POV flat-lay on pink bedroom blanket, pink Glossier-style packaging on left crossed out with red marker drawn through it, two Skintific Alaska Volcano clay sticks on right with green checkmarks, raw overhead phone photo, soft pink bedroom light, 1:1"),
    ("comp_brand_04", "efficient_perfectionist", "vs The Ordinary cult", "META-SAFE", "5-6%",
     "stack-overload validation + simplicity hook",
     "TWELVE Ordinary serums vs ONE $19.99 deal", "B1G1 — i did the math",
     "spreadsheet-screenshot aesthetic",
     "iPhone flat-lay on white desk, multiple small white-labeled minimalist skincare bottles on left side scattered, two Skintific Alaska Volcano clay sticks centered on right, woman's hand pointing to the sticks, raw phone photo, harsh afternoon light, 1:1"),
    ("comp_brand_05", "sensitive_skin", "vs Korean 10-step", "META-SAFE", "5-7%",
     "complexity exhaustion + simplicity reward",
     "10-step Korean routine: $400. This: $19.99", "B1G1 / pick your fighter",
     "comparison-chart casual handwritten",
     "iPhone flat-lay overhead shot on white surface, 10+ tiny Korean-style skincare bottles arranged in a chaotic line on left, two Skintific Alaska Volcano clay sticks alone on right with arrow drawn pointing to them, raw phone photo, harsh light, 1:1"),
    ("comp_brand_06", "convenience_seeker", "vs Estee Lauder counter", "BURNER", "5-7%",
     "luxury-defiance identity",
     "walked past the $190 cream", "got 2 of these for $19.99",
     "white text iMessage style",
     "iPhone selfie of woman 35 mixed-race in department store mirror near luxury skincare counter, holding Skintific Alaska Volcano clay stick from her purse, smug small smile, harsh fluorescent retail lighting, raw candid mall photo, 1:1"),
    ("comp_brand_07", "efficient_perfectionist", "vs Tatcha cult favorite", "BURNER", "6-7%",
     "luxury price-shock + cult brand takedown",
     "Tatcha: $135 — This: $19.99 for TWO", "B1G1 / I'm not a math person but",
     "yellow highlighter + bold strikethrough",
     "iPhone overhead flat-lay, fancy gold-accented Japanese-style skincare jar on left side, two Skintific Alaska Volcano clay sticks on right, both labeled with price tags showing massive difference, raw phone photo from above, harsh overhead light, 1:1"),
    ("comp_brand_08", "sensitive_skin", "vs Kiehl's overpriced", "BURNER", "5-7%",
     "heritage-brand vs upstart drama",
     "Kiehl's $58 vs Skintific $19.99 (B1G1)", "guess which one cleared my pores",
     "minimal white text",
     "iPhone selfie of woman 31 white American with raised eyebrow in bathroom, holding old-fashioned amber Kiehl's-style bottle in left hand and Skintific Alaska Volcano clay stick in right, comparing them, harsh overhead light, raw candid photo, 1:1"),
    ("comp_brand_09", "convenience_seeker", "vs CeraVe + Cetaphil pharmacy", "META-SAFE", "4-6%",
     "tier-upgrade aspiration",
     "drugstore basics vs THIS", "B1G1 deal — $19.99 / level up",
     "bold sans serif with arrow",
     "iPhone overhead flat-lay on white pharmacy-aesthetic surface, big drugstore CeraVe and Cetaphil-style white pump bottles on left, two Skintific Alaska Volcano clay sticks on right with sparkle/shine effect, raw flat-lay phone photo, harsh light, 1:1"),
    ("comp_brand_10", "efficient_perfectionist", "vs influencer brand markup", "META-SAFE", "5-6%",
     "influencer-fatigue + authentic-find",
     "influencer brand: $48 + meh — this:", "$19.99 + B1G1 + actually works",
     "casual sans serif",
     "iPhone selfie of woman 30 white with disappointed face holding empty influencer-celebrity-branded pink skincare bottle in one hand, Skintific Alaska Volcano clay stick in other, raw bedroom mirror photo, soft afternoon light, 1:1"),

    # === B2. VS TREATMENTS (8) ===
    ("comp_treat_01", "efficient_perfectionist", "vs $200 facial", "BURNER", "6-8%",
     "spa-luxury defiance + savings rage",
     "$200 facial vs THIS:", "$19.99 / B1G1 / same energy",
     "yellow highlighter behind bold black",
     "iPhone selfie of woman 34 white American in pajamas in messy bathroom, holding two Skintific Alaska Volcano clay sticks toward camera triumphantly, raised eyebrow sarcastic expression, harsh overhead bathroom light, raw candid morning photo, 1:1"),
    ("comp_treat_02", "sensitive_skin", "vs HydraFacial", "BURNER", "6-7%",
     "medical-spa procedural defiance",
     "HydraFacial: $250 / 6 weeks. This: $19.99 / now.", "B1G1 — buy 1 give 1 to your sister",
     "casual italics",
     "iPhone selfie of woman 28 Latina with crossed arms confidently, two Skintific Alaska Volcano clay sticks visible on counter behind her, slight smug smile, raw bathroom photo, harsh overhead light, no makeup, 1:1"),
    ("comp_treat_03", "convenience_seeker", "vs Botox preventative", "BURNER", "6-8%",
     "preventative-care rage-bait",
     "preventative botox: $600. preventative pores:", "$19.99 (B1G1) / same energy",
     "pink-accented casual",
     "iPhone selfie of woman 29 mixed-race making 'mind blown' gesture with hands near her head, two Skintific Alaska Volcano clay sticks visible on bedroom dresser, raw playful photo, soft afternoon light, 1:1"),
    ("comp_treat_04", "efficient_perfectionist", "vs Accutane prescription", "BURNER", "7-9%",
     "anti-prescription identity + savings",
     "my derm: 'try Accutane' — me, with $20:", "skintific B1G1 $19.99",
     "rebel handwritten",
     "iPhone selfie of woman 32 white in robe, defiant raised chin, holding Skintific Alaska Volcano clay stick like trophy, raw bathroom photo, harsh light, slight smile of vindication, 1:1"),
    ("comp_treat_05", "sensitive_skin", "vs chemical peel cost", "BURNER", "6-7%",
     "cumulative-cost shock",
     "chemical peels over 5 yrs: $3,000+", "this: $19.99 ONCE (B1G1)",
     "calculator/spreadsheet aesthetic",
     "iPhone POV looking down at calculator on phone showing $3000 figure, two Skintific Alaska Volcano clay sticks on either side of phone, raw flat-lay overhead photo on bed sheets, soft light, 1:1"),
    ("comp_treat_06", "convenience_seeker", "vs LED mask gadget", "META-SAFE", "5-6%",
     "gadget-buyer regret + practicality",
     "$400 LED mask collecting dust", "vs $19.99 (B1G1) actually used daily",
     "minimal sans serif comparison",
     "iPhone overhead flat-lay, expensive futuristic-looking LED face mask gadget on left in box, two Skintific Alaska Volcano clay sticks on right, raw phone photo from above, harsh light, 1:1"),
    ("comp_treat_07", "efficient_perfectionist", "vs microneedling", "BURNER", "6-7%",
     "professional-treatment skip identity",
     "skipped $400 microneedling appointment", "for $19.99 B1G1 / no regrets",
     "casual italics",
     "iPhone selfie of woman 36 white American touching her cheek with confident smile, holding Skintific Alaska Volcano clay stick visible to camera, raw bedroom mirror selfie, golden hour light, 1:1"),
    ("comp_treat_08", "sensitive_skin", "vs prescription topical cost", "BURNER", "6-7%",
     "healthcare-cost defiance",
     "Rx topical (with insurance): $80/mo", "this: $19.99 / B1G1 / one time",
     "medical-form aesthetic",
     "iPhone selfie of woman 27 Black American holding prescription pill bottle in one hand and Skintific Alaska Volcano clay stick in other, eyebrow raised questioning, raw bathroom photo, harsh light, 1:1"),

    # === B3. VS JAR MASKS / FORMAT (7) ===
    ("comp_jar_01", "convenience_seeker", "Messy jar disaster", "META-SAFE", "5-7%",
     "mess-frustration relatability",
     "your $40 jar mask vs $19.99 (TWO)", "B1G1 / no mess / no brush",
     "before/after caption style",
     "iPhone overhead flat-lay on white bathroom counter, traditional clay mask jar tipped over with gray clay spilled messily, brush dirty next to it, two clean Skintific Alaska Volcano clay sticks standing pristine on right side, raw chaos vs order phone photo, harsh light, 1:1"),
    ("comp_jar_02", "efficient_perfectionist", "Travel jar broke", "META-SAFE", "5-6%",
     "travel-disaster relatability",
     "she took the jar to Mexico", "be smart: B1G1 $19.99 (sticks travel)",
     "travel-blog aesthetic",
     "iPhone POV looking into open suitcase, broken clay mask jar with gray clay smeared all over white clothes inside suitcase, two Skintific Alaska Volcano clay sticks placed neatly intact, raw overhead travel-disaster phone photo, hotel room light, 1:1"),
    ("comp_jar_03", "sensitive_skin", "Dipping fingers bacteria", "META-SAFE", "5-7%",
     "hygiene disgust trigger",
     "jar masks = bacteria soup 🦠", "stick = clean. B1G1 $19.99",
     "TikTok caption with emoji",
     "iPhone close-up overhead of woman's hand fingers visibly dirty about to dip into clay mask jar, gross-out angle, two Skintific Alaska Volcano clay sticks standing clean on right, raw bathroom counter photo, harsh light, 1:1"),
    ("comp_jar_04", "convenience_seeker", "Brush vs stick application", "META-SAFE", "5-6%",
     "skill-gap relatability",
     "jar = patchy. stick = perfect.", "B1G1 → $19.99",
     "split-screen caption",
     "Side-by-side iPhone selfie split-comparison of same woman 30 mixed-race, left side has clay mask sloppily applied with fingers/brush in patchy mess, right side has clean smooth Skintific stick application, harsh bathroom light, raw selfie split, 1:1"),
    ("comp_jar_05", "efficient_perfectionist", "Time waste comparison", "META-SAFE", "5-6%",
     "complexity-fatigue resolution",
     "jar setup: 8 things. stick: ONE thing.", "$19.99 / B1G1 / less is more",
     "minimalist before/after",
     "iPhone overhead flat-lay, jar mask + brush + spatula + headband + cleansing cloth all spread out on left side, two Skintific Alaska Volcano clay sticks alone on right, woman's hand pointing to right side, raw flat-lay photo, harsh light, 1:1"),
    ("comp_jar_06", "sensitive_skin", "Wasted product", "META-SAFE", "4-5%",
     "waste-frustration relatability",
     "wasted half this jar", "switched to B1G1 sticks: $19.99",
     "minimal handwritten",
     "iPhone overhead photo of half-empty clay mask jar with old crusty product around the rim, looking unappetizing, two clean fresh Skintific Alaska Volcano clay sticks beside it, raw bathroom counter close-up, harsh light, 1:1"),
    ("comp_jar_07", "convenience_seeker", "Stick is foolproof", "META-SAFE", "5-6%",
     "mom-life practicality",
     "one hand. mom-proof. B1G1.", "$19.99 — try doing that with a jar",
     "casual mom-blogger aesthetic",
     "iPhone selfie of woman 26 Black American applying Skintific Alaska Volcano clay stick to face one-handed while toddler hugs her leg in frame, mom-life chaos energy, raw candid bathroom photo, harsh light, 1:1"),
]

# ---- Globals appended to every full_prompt ----

CRITICAL_STYLE = (
    "CRITICAL STYLE: shot on iPhone 13, front camera, JPEG compression visible, slight motion blur or hand-held wobble, "
    "no bokeh, no shallow depth of field, flash glare on skin allowed, harsh fluorescent overhead bathroom light "
    "or harsh natural window light, amateur phone photography aesthetic, candid not posed, looks like a real screenshot "
    "from Instagram Story or TikTok. NOT a commercial photo, NOT magazine quality, NOT studio."
)

NO_TEXT_DIRECTIVE = (
    "ABSOLUTE RULE: DO NOT add any text, captions, headlines, watermarks, price tags, or written words anywhere on the "
    "image. The image MUST be completely text-free except for the product label that exists on the physical product. "
    "Any text overlay will be added in post-production — leave space at the top and bottom 25% of the frame relatively "
    "uncluttered for that overlay."
)

BRAND_LOCK = (
    "Product details (must reproduce exactly): Skintific Alaska Volcano Pore Clay Stick — gray cylindrical stick with "
    "a white label that reads 'SKINTIFIC ALASKA VOLCANO PORE CLAY STICK', '40g / 1.41 FL.OZ'. The brand on the label "
    "must say 'SKINTIFIC' — NOT 'BARUBT' or any other brand name."
)

NEGATIVE = (
    "Avoid: no professional studio lighting, no clean composition, no commercial photography aesthetic, no DSLR shallow "
    "depth of field, no perfect retouched skin, no styled background, no fashion photography, no magazine cover quality, "
    "no BARUBT branding, no other clay stick brands, no fake distorted product label, no extra fingers, no AI artifacts, "
    "no watermarks, no overlay text, no headlines, no captions."
)


def normalize_compliance(meta: str) -> str:
    return "aggressive" if "BURNER" in meta.upper() else "compliant"


def build_full_prompt(prompt_text: str) -> str:
    return "\n\n".join([prompt_text, CRITICAL_STYLE, NO_TEXT_DIRECTIVE, BRAND_LOCK, NEGATIVE])


def build_source() -> dict:
    return {
        "global_settings": {
            "aspect_ratio": "1:1",
            "resolution": "1080x1080",
            "product_image": "inputs/products/alaska_volcano_stick.jpg",
            "brand_lock": BRAND_LOCK,
            "critical_style": CRITICAL_STYLE,
            "no_text_directive": NO_TEXT_DIRECTIVE,
            "negative_prompt": NEGATIVE,
            "totals": {
                "prompts": len(PROMPTS),
                "by_compliance": {
                    "aggressive": sum(1 for p in PROMPTS if normalize_compliance(p[3]) == "aggressive"),
                    "compliant": sum(1 for p in PROMPTS if normalize_compliance(p[3]) == "compliant"),
                },
                "by_avatar": {
                    a: sum(1 for p in PROMPTS if p[1] == a)
                    for a in sorted({p[1] for p in PROMPTS})
                },
            },
        },
        "prompts": [
            {
                "id": pid,
                "avatar": avatar,
                "angle": angle,
                "compliance": normalize_compliance(meta),
                "compliance_meta": meta,
                "expected_ctr": ctr,
                "stop_mechanism": stop,
                "overlay_top": overlay_top,
                "overlay_bottom": overlay_bottom,
                "overlay_style": overlay_style,
                "prompt": prompt_text,
            }
            for (pid, avatar, angle, meta, ctr, stop, overlay_top, overlay_bottom, overlay_style, prompt_text) in PROMPTS
        ],
    }


def build_flat() -> dict:
    flat: dict = {}
    for (pid, avatar, angle, meta, ctr, stop, overlay_top, overlay_bottom, overlay_style, prompt_text) in PROMPTS:
        flat[pid] = {
            "avatar": avatar,
            "compliance": normalize_compliance(meta),
            "compliance_meta": meta,
            "angle": angle,
            "expected_ctr": ctr,
            "stop_mechanism": stop,
            "overlay_top": overlay_top,
            "overlay_bottom": overlay_bottom,
            "overlay_style": overlay_style,
            "full_prompt": build_full_prompt(prompt_text),
        }
    return flat


def main() -> None:
    SRC.parent.mkdir(parents=True, exist_ok=True)
    SRC.write_text(yaml.safe_dump(build_source(), allow_unicode=True, sort_keys=False, width=120, default_flow_style=False), encoding="utf-8")
    OUT.write_text(yaml.safe_dump(build_flat(), allow_unicode=True, sort_keys=False, width=120, default_flow_style=False), encoding="utf-8")
    print(f"wrote {SRC} and {OUT} ({len(PROMPTS)} prompts)")


if __name__ == "__main__":
    main()
