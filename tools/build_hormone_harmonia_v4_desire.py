"""Build pipeline-ready YAML for the v4 Desire Test batch.

30 prompts = 6 desires x 5 styles per desire.
Desires:  weightloss, energy, sleep, mood, hotflash, brainfog
Styles:   anatomical_infographic, ugc_iphone, bold_color_block,
          vintage_scientific, testimonial_portrait

Each prompt gets:
- compliance = desire name  → bulk_image_gen writes into <run>/<desire>/
- avatar     = "hormone_harmonia_v4_desire" → tidy filename = pid + .png
- pid format = hh_v4_<desire>_<NN>          (NN = 01..05)
- the user-supplied prompt + brand-lock + user-supplied negative suffix
"""
from __future__ import annotations

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "config" / "hormone_harmonia_v4_desire_prompts.yaml"

STYLES = [
    "anatomical_infographic",
    "ugc_iphone",
    "bold_color_block",
    "vintage_scientific",
    "testimonial_portrait",
]

# Each block has exactly 5 prompts, ordered to match STYLES above.

WEIGHTLOSS = [
    # 1.1 anatomical_infographic
    "A clean, scientific medical infographic style image in 4:5 portrait format.\n"
    "LEFT SIDE: A clean modern anatomical illustration of a 50-year-old woman's torso (front view, neutral pose, fully clothed, abstract line drawing on cream parchment background). The cortisol-affected abdominal area is subtly highlighted with a soft warm glow. Two glands are labeled with thin elegant arrows: \"MELLÉKVESE (kortizol ↑)\" pointing to upper abdomen, \"PETESZÁK (ösztrogén ↓)\" pointing to lower pelvis.\n"
    "TOP BANNER: Hungarian text overlay in serif science-magazine font: \"A 3 HORMON, AMI A HASI ZSÍRT RAKTÁROZZA 45 FELETT\". Subline in smaller font: \"...és miért nem segít a diéta\".\n"
    "BOTTOM RIGHT CORNER: Small product mockup of Hormone Harmonia bottle (white plastic, purple-pink label, \"72 kapszula\" visible) with subtle drop shadow.\n"
    "COLOR PALETTE: Cream/parchment (#F5E6D3), warm sepia accents, dark brown labels (#3D2817), bright accent (#D4A574).\n"
    "STYLE: Editorial science magazine aesthetic, like Scientific American 1960s. Serif typography (Caslon, Garamond style). Generous negative space. NOT cluttered.",
    # 1.2 ugc_iphone
    "A native UGC-style iPhone photo, 4:5 portrait format, slightly imperfect framing.\n"
    "SUBJECT: A 48-year-old Hungarian woman in casual home clothing (oversized cotton sweater, minimal makeup), standing in a typical modern Hungarian apartment kitchen. She holds a Hormone Harmonia bottle in one hand and looks at it with a neutral, contemplative expression — NOT smiling broadly, NOT staged. Morning light from a side window, slightly warm tones.\n"
    "ENVIRONMENT: Tile countertop, a half-empty coffee mug on the side, a folded newspaper. Slightly messy real-life kitchen, NOT a magazine shoot.\n"
    "NO TEXT OVERLAY (pure native style — text goes in primary copy only).\n"
    "STYLE: Like a friend posting on Instagram stories — handheld phone aesthetic, slight motion blur on the bottle, real human imperfection. The woman looks like someone you'd see at a grocery store, not a model. Age 45-55, Central European features, brown/auburn hair with subtle grays.",
    # 1.3 bold_color_block
    "A bold, attention-grabbing graphic design poster, 4:5 portrait format.\n"
    "BACKGROUND: Solid magenta-pink color block (#E91E63) covering top 70%. Bottom 30%: Cream/off-white (#F5E6D3).\n"
    "MAIN HEADLINE (top, white bold sans-serif, large): \"A KALÓRIA NEM A PROBLÉMA.\"\n"
    "SUBLINE (white, slightly smaller, italics): \"A KORTIZOL AZ.\"\n"
    "MIDDLE TEXT BLOCK (cream area, dark brown serif font):\n"
    "\"3 hormon, ami a hasi zsírt raktározza 45 felett.\n"
    "↳ Minden 100 nőből 73 érintett.\n"
    "↳ A diéta NEM oldja meg.\"\n"
    "BOTTOM RIGHT CORNER: Small Hormone Harmonia mockup in the cream area, with thin caption: \"Hormone Harmonia — természetes megoldás\".\n"
    "TYPOGRAPHY: Display sans-serif (like Druk, Tungsten) for headline, elegant serif (like Caslon) for body. NO PHOTOS, ALL GRAPHIC DESIGN, like a Black Girl Vitamins / Girls Gone Strong ad.",
    # 1.4 vintage_scientific
    "A vintage scientific illustration aesthetic, 4:5 portrait format, like a page from a 1890s anatomical atlas.\n"
    "BACKGROUND: Aged sepia parchment with soft brown coffee-stain texture and slight edge browning. NOT pristine — looks like a real old book page.\n"
    "CENTRAL ILLUSTRATION: Hand-drawn ink anatomical sketch of female abdominal cavity (technical, NOT graphic — like Vesalius/Gray's Anatomy style). Visible: adrenal glands (kidneys area), ovaries, midriff. Labels in elegant cursive script (Hungarian): \"Mellékvese — kortizol forrás\", \"Petefészek — ösztrogén forrás\", \"Hasi régió — kortizol-okozta zsírraktározás\".\n"
    "TOP TEXT (vintage serif): \"Az Endokrinológia Elfeledett Fejezete\". Subtitle smaller: \"A perimenopauza alatti hasi zsír valódi oka\".\n"
    "BOTTOM TEXT (book-style attribution, faded): \"Hormonális Egyensúly — Modern Megoldások, 2024\".\n"
    "PRODUCT: Bottom-right corner, Hormone Harmonia bottle integrated as if sketched on the same page — drawn in the same ink style as the anatomy, not photographic, with hand-drawn label \"Hormone Harmonia™\".\n"
    "COLOR PALETTE: Sepia (#8B7355), aged cream (#E8DDC4), ink brown (#3D2817).\n"
    "STYLE: Like Modere or BHRT Training Academy ads — authoritative, scholarly.",
    # 1.5 testimonial_portrait
    "A documentary-style portrait photo, 4:5 portrait format.\n"
    "SUBJECT: A real-looking 49-year-old Hungarian woman named \"Anna\" sitting at her dining table in soft natural morning light. She wears a simple linen blouse, hair in a low ponytail, slight smile (NOT toothy — gentle, real). She looks slightly off-camera, holding a coffee cup.\n"
    "ENVIRONMENT: Hungarian apartment kitchen background — bookshelf with magyar könyvek visible, a vase of dried flowers. Slight depth-of-field blur.\n"
    "LEFT-SIDE QUOTE OVERLAY (large serif quote marks). Hungarian text in elegant serif:\n"
    "\"Az első, amit észrevettem: már nem kívántam az édességet 4-kor délután. Aztán a puffadás eltűnt. 8 hét alatt 6 kilóval vagyok kevesebb — diéta nélkül.\"\n"
    "ATTRIBUTION (small bottom-left): \"— Anna, 49 éves, Budapest\".\n"
    "BOTTOM RIGHT: Discrete Hormone Harmonia bottle on the table next to Anna, slightly out of focus, NOT advertised — just present.\n"
    "STYLE: Like a New York Times \"Real Stories\" portrait. Subtle age signs visible (slight crow's feet, natural hair texture). 100% Hungarian appearance, NOT a Western European model.",
]

ENERGY = [
    # 2.1
    "A clean scientific medical infographic, 4:5 portrait format.\n"
    "LEFT SIDE: Anatomical illustration of female body with TWO highlighted regions: 1) Thyroid gland (neck area) labeled \"PAJZSMIRIGY (lassul)\". 2) Cellular mitochondria zoomed-in inset (circular detail) labeled \"MITOKONDRIUMOK (energia gyár)\". A subtle arrow connects them showing \"hormonális signal\".\n"
    "TOP HEADLINE (Hungarian serif): \"NEM AZ ÖREGEDÉSTŐL FÁRADSZ — A HORMONJAID FELBORULTAK\". Subline: \"A 3 mechanizmus, ami az energiát ellopja 45 után\".\n"
    "RIGHT SIDE: 3 small horizontal bar charts going down: \"Mitokondrium aktivitás\", \"Pajzsmirigy hormon\", \"Sejtszintű energia\".\n"
    "BOTTOM RIGHT: Hormone Harmonia bottle, subtle integration.\n"
    "COLOR PALETTE: Cream parchment, deep teal accent (#005F73), warm sepia.\n"
    "STYLE: Editorial science, like Pendulum (Halle Berry) ads.",
    # 2.2
    "A native UGC iPhone selfie style, 4:5 portrait format.\n"
    "SUBJECT: A 47-year-old Hungarian woman in her bedroom, sitting on the edge of her bed, still in pajamas. She holds her phone for a selfie — looking tired but not exhausted, slight under-eye circles, hair messy bedhead.\n"
    "EXPRESSION: Half-smile, eye-roll humor — like \"lol, look at me, what is happening\" — NOT depression, NOT model glamour. Real human \"ugh, mornings\" vibe.\n"
    "ENVIRONMENT: Unmade bed visible, morning light through curtains, a nightstand with water glass and Hormone Harmonia bottle naturally placed.\n"
    "NO TEXT OVERLAY (pure native).\n"
    "COLOR PALETTE: Cool morning blue-grey light, neutral skin tones.\n"
    "STYLE: Sarah Mitchell / Becca Fisher feel. Very Instagram-real. Imperfect framing, slight tilt.",
    # 2.3
    "A bold graphic design poster, 4:5 portrait format.\n"
    "BACKGROUND: Bright energizing yellow-orange (#FFB84D) top 60%. Bottom 40%: dark navy (#0A2540).\n"
    "HEADLINE (top, navy bold serif on yellow): \"FÁRADT VAGY — 30 ÉVES KORODBAN IS LEHETTÉL VOLNA.\". SUBLINE (smaller, italic): \"Most miért tűnik mindennap maratonnak?\".\n"
    "MIDDLE: Simple minimal icons — battery icon with low charge, clock icon, a tired face emoji-style illustration.\n"
    "BOTTOM BLOCK (navy, yellow text):\n"
    "\"NEM AZ ÖREGEDÉS A HIBÁS. A 3 HORMON AMI ELLOPJA AZ ENERGIÁD:\n"
    "↳ KORTIZOL (állandóan magas)\n"
    "↳ PAJZSMIRIGY (lassul)\n"
    "↳ ÖSZTROGÉN (ingadozik)\"\n"
    "BOTTOM RIGHT CORNER: Hormone Harmonia mockup small, navy section.\n"
    "TYPOGRAPHY: Display sans-serif headline, serif body. High contrast, Health Insider style.",
    # 2.4
    "A vintage scientific page aesthetic, 4:5 portrait format.\n"
    "BACKGROUND: Aged sepia parchment with subtle aging.\n"
    "CENTRAL: Hand-drawn line graph showing \"Női energia szint\" (Y-axis), age 20-60 (X-axis). The line drops dramatically around age 42-45, with hand-drawn annotation: \"PERIMENOPAUZA — hormonális zuhanás\".\n"
    "Below the graph, three smaller circular ink illustrations: mitochondria (cellular energy), thyroid gland, adrenal gland. Each with cursive Hungarian labels.\n"
    "TOP TEXT (vintage book title): \"Az Energia Görbéje — Mit nem mond el az orvosod\".\n"
    "BOTTOM RIGHT: Hand-sketched Hormone Harmonia bottle, with cursive label \"Hormone Harmonia — természetes támogatás\".\n"
    "COLOR: Sepia, dark brown ink, aged paper.\n"
    "STYLE: 1920s medical journal page. Modere / BHRT vibe.",
    # 2.5
    "A documentary portrait, 4:5 portrait format.\n"
    "SUBJECT: A 51-year-old Hungarian woman \"Réka\" in her home office or living room, captured in candid mid-action — maybe organizing papers, or coming back from a morning walk (jacket still on her shoulder). She has more vitality than Anna — slightly more present, energetic, BUT realistic, not influencer-energy.\n"
    "EXPRESSION: Looking at camera with a quiet, confident smile.\n"
    "ENVIRONMENT: Hungarian-style apartment, books in background, a plant.\n"
    "QUOTE OVERLAY (left side, serif):\n"
    "\"Régen mindig energikus voltam. Aztán egyik napról a másikra úgy éreztem, kicseréltek. 3 hónappal később újra látom magam a tükörben.\"\n"
    "ATTRIBUTION: \"— Réka, 51 éves, Debrecen\".\n"
    "BOTTOM RIGHT: Hormone Harmonia bottle on a side table.\n"
    "COLOR PALETTE: Warm autumn tones, soft afternoon light.\n"
    "STYLE: Magazine portrait, NOT stock photo. Real woman energy.",
]

SLEEP = [
    # 3.1
    "Scientific infographic, 4:5 portrait format.\n"
    "CENTRAL ELEMENT: Cross-section illustration of brain/head profile (side view, woman, age 50), highlighting: pineal gland (small purple-glowing dot) labeled \"TOBOZMIRIGY (melatonin)\"; hypothalamus (small orange-glowing dot) labeled \"HIPOTALAMUSZ (hőszabályozás)\".\n"
    "Below brain illustration, two small icons — estrogen molecule diagram (chemistry style) and progesterone molecule diagram, with Hungarian labels: \"Ösztrogén — ingadozik\" and \"Progeszteron — csökken\".\n"
    "TOP HEADLINE: \"MIÉRT NEM TUDSZ ALUDNI 45 FELETT?\". Subline: \"A 4 hormon, ami az éjszakai hőhullámot okozza\".\n"
    "BACKGROUND: Deep midnight blue gradient (#0F2027 to #2C5364), suggesting nighttime. TEXT COLOR: Cream/off-white for contrast.\n"
    "BOTTOM RIGHT: Hormone Harmonia bottle, subtle moonlight glow effect.\n"
    "STYLE: National Geographic dark-mode science illustration.",
    # 3.2
    "Native UGC style iPhone photo, 4:5 portrait format.\n"
    "SUBJECT: A 49-year-old Hungarian woman lying in bed at 3 AM (visible alarm clock on nightstand showing \"03:14\"), looking up at the ceiling. She has thrown off the blanket — visible only sheets, no nudity. Her hair is slightly damp from sweating. Expression: tired frustration, eyes open but exhausted.\n"
    "LIGHT: Only the alarm clock glow + soft moonlight from window.\n"
    "NO TEXT OVERLAY.\n"
    "ENVIRONMENT: Typical Hungarian bedroom, partner sleeping next to her (out of focus). Water glass and Hormone Harmonia bottle on nightstand.\n"
    "COLOR PALETTE: Deep blues, soft alarm clock red glow accent.\n"
    "STYLE: Candid documentary, like Sarah Mitchell night ad. Feels like a 3 AM real moment captured.",
    # 3.3
    "Bold graphic poster, 4:5 portrait format.\n"
    "BACKGROUND: Deep midnight purple (#1A1B41) top 65%. Bottom 35%: cream off-white (#F5E6D3).\n"
    "HEADLINE (top, cream serif on purple): \"03:47. ÚJRA FELRIADTÁL.\". SUBLINE (italic cream): \"Az 5. éjszaka egymás után.\".\n"
    "MIDDLE: A simple line drawing of an alarm clock and a pillow, minimal.\n"
    "BOTTOM (cream block, dark purple text):\n"
    "\"A HŐHULLÁMOS ÉJSZAKA NEM AZ ÉLETKOR. A HORMONJAID PRÓBÁLNAK SZÓLNI:\n"
    "↳ Ösztrogén ingadozás\n"
    "↳ Progeszteron hiány\n"
    "↳ Hipotalamusz tengely zavart\"\n"
    "BOTTOM RIGHT: Hormone Harmonia mockup in cream section.\n"
    "TYPOGRAPHY: Bold serif headline (Playfair Display style), sans-serif body.\n"
    "STYLE: High contrast, Bonafide / MenoLabs aesthetic.",
    # 3.4
    "Vintage scientific aesthetic, 4:5 portrait format.\n"
    "BACKGROUND: Aged paper with subtle browning.\n"
    "CENTRAL: Hand-drawn 24-hour clock face, with a sleep cycle diagram overlaid — showing \"normál ciklus\" (gentle waves) vs \"perimenopauza ciklus\" (jagged, interrupted waves). Hungarian annotations.\n"
    "Around the clock, 4 small hand-drawn ink illustrations: pineal gland in brain, estrogen/progesterone molecule, hot flash thermal map of body, adrenal gland with cortisol arrow. Hungarian cursive labels.\n"
    "TOP TEXT (book title style): \"A Női Alvás Megzavart Ritmusa\". Subtitle: \"Miért riadsz fel 3-kor? — A hormonális magyarázat\".\n"
    "BOTTOM RIGHT: Hand-sketched Hormone Harmonia bottle, integrated.\n"
    "COLOR: Sepia, faded blue accents, ink brown.\n"
    "STYLE: Old medical encyclopedia page.",
    # 3.5
    "Documentary portrait, 4:5 portrait format.\n"
    "SUBJECT: A 52-year-old Hungarian woman \"Judit\" sitting at her kitchen table in MORNING light (suggesting she finally slept well). She holds a steaming cup of tea with both hands, looking down at it with a quiet, relieved smile — NOT joyful, just \"finally rested\" calm.\n"
    "ENVIRONMENT: Hungarian kitchen, soft 7 AM light through a window with sheer curtains. A small breakfast plate visible. Slight bedhead in her hair.\n"
    "QUOTE OVERLAY (right side, serif):\n"
    "\"Hónapok óta minden hajnalban felriadtam — szívdobogás, pánik. Az első hét után végre átaludtam az éjszakát. Mintha visszakaptam volna a saját testemet.\"\n"
    "ATTRIBUTION: \"— Judit, 52 éves, Szeged\".\n"
    "BOTTOM RIGHT: Hormone Harmonia bottle on the kitchen table, naturally placed.\n"
    "COLOR PALETTE: Warm morning cream and gold tones, gentle.\n"
    "STYLE: Quiet, intimate documentary moment.",
]

MOOD = [
    # 4.1
    "Scientific infographic, 4:5 portrait format.\n"
    "CENTRAL: Side-profile silhouette of a woman's head with brain visible, showing hormone pathways with thin elegant arrows: limbic system (highlighted soft pink) labeled \"ÉRZELMI KÖZPONT\"; hypothalamus labeled \"Hormonális karmester\"; serotonin pathway labeled \"Boldogság-hormon (zavart)\"; estrogen receptor labeled \"Ösztrogén kötődés\".\n"
    "TOP HEADLINE: \"A HANGULATINGADOZÁS NEM A SZEMÉLYISÉGED — A HORMONJAID.\". Subline: \"Miért érzed, hogy nem te vagy önmagad 45 felett?\".\n"
    "COLOR: Soft pinks, dusty rose, cream parchment.\n"
    "BOTTOM RIGHT: Hormone Harmonia bottle.\n"
    "STYLE: Soft scientific, like a Through Menopause ad.",
    # 4.2
    "Native iPhone-style photo, 4:5 portrait, slightly bittersweet.\n"
    "SUBJECT: A 50-year-old Hungarian mother sitting alone at a dining table that has clear \"family just left\" energy — empty plates, a child's homework book, a husband's coffee mug. She holds her face in her hands, NOT sobbing — just a quiet \"ugh\" moment, exhausted.\n"
    "She is realistically dressed (jeans, sweater), no makeup, hair tied back.\n"
    "NO TEXT OVERLAY.\n"
    "ENVIRONMENT: Hungarian apartment dining room, after-dinner mess, late afternoon golden hour light from a window.\n"
    "COLOR: Warm golden, shadows that feel emotionally heavy but not sad.\n"
    "STYLE: Becca Fisher ad — relatable, mid-action, not posed. Friend, not model.",
    # 4.3
    "Bold graphic, 4:5 portrait format.\n"
    "BACKGROUND: Deep coral pink (#E76F51) top 65%. Bottom 35%: warm cream (#F5E6D3).\n"
    "HEADLINE (top, white bold sans-serif): \"AZ ELŐBB ÚJBÓL FELKAPTAM A VIZET.\". SUBLINE (italic): \"...és nem értem miért.\".\n"
    "MIDDLE: Simple line illustration of two faces — same woman with two expressions (calm and tense), suggesting mood swings.\n"
    "BOTTOM (cream, dark text):\n"
    "\"A HORMONÁLIS HULLÁMVASÚT NEM A FEJEDBEN VAN. 3 HORMON OKOZZA A MOOD SWING-EKET 45 UTÁN:\n"
    "↳ Ösztrogén (ingadozik)\n"
    "↳ Progeszteron (csökken)\n"
    "↳ Szerotonin (érintett)\"\n"
    "BOTTOM RIGHT: Hormone Harmonia mockup.\n"
    "TYPOGRAPHY: Bold display sans, body serif.\n"
    "STYLE: Wellbrooke / Becca Fisher — emotional, real.",
    # 4.4
    "Vintage scientific page, 4:5 portrait format.\n"
    "BACKGROUND: Aged paper with slight pink-coral tint.\n"
    "CENTRAL: Hand-drawn diagram showing a brain cross-section with hormone receptors illustrated. Multiple small drawings around it: limbic system close-up, hormone molecules, a vintage \"ANGER vs CALM\" mood scale. Hungarian cursive annotations throughout.\n"
    "TOP TEXT (book title style): \"A Nőiség Hormonális Lélektana\". Subtitle: \"A perimenopauza érzelmi viharának valódi forrása\".\n"
    "BOTTOM: Hand-sketched Hormone Harmonia bottle integrated.\n"
    "COLOR: Sepia with subtle coral/rose accents.\n"
    "STYLE: Old Freudian-era psychology textbook page, but accurate.",
    # 4.5
    "Documentary portrait, 4:5 portrait format.\n"
    "SUBJECT: A 48-year-old Hungarian woman \"Eszter\" with her teenage daughter in a candid hug from behind — Eszter's eyes closed in a calm, restored moment. The daughter (16-ish) is hugging from behind with a slight smile. This is the \"got my mom back\" emotional moment.\n"
    "EXPRESSION: Eszter looks restored, calm, eyes closed in a quiet moment.\n"
    "ENVIRONMENT: Hungarian home interior, soft afternoon light, slightly out-of-focus background.\n"
    "QUOTE OVERLAY (right side):\n"
    "\"3 hónapja nem ismertem magamra a saját családomban. Ma este a lányom azt mondta: 'Anya, megint olyan vagy mint régen.'\"\n"
    "ATTRIBUTION: \"— Eszter, 48 éves, Pécs\".\n"
    "BOTTOM RIGHT: Hormone Harmonia bottle on a shelf in background, subtle.\n"
    "COLOR PALETTE: Warm golden hour, soft skin tones, family-intimate.\n"
    "STYLE: Real moment — like a family photographer captured it.",
]

HOTFLASH = [
    # 5.1
    "Scientific infographic, 4:5 portrait format.\n"
    "CENTRAL: Cross-section illustration of female head/brain side profile. HIGHLIGHTED: hypothalamus glowing soft orange-red (heat dysregulation). Arrow labels: \"HIPOTALAMUSZ — hőszabályozás központja\", \"ÖSZTROGÉN-RECEPTOR — érzékeny zóna\".\n"
    "Body illustration on right side with thermal-map style red hotspots: face flushing, chest/neck flushing, back of neck heat.\n"
    "TOP HEADLINE: \"A HŐHULLÁM 4 PERCBEN — MI TÖRTÉNIK A TESTBEN\". Subline: \"A hipotalamusz hormonális zavarának vizuális magyarázata\".\n"
    "COLOR PALETTE: Cream parchment, warm reds and oranges as heat indicators.\n"
    "BOTTOM RIGHT: Hormone Harmonia bottle with cooling-blue accent.\n"
    "STYLE: Editorial science — Halsten / Hinge Health vibe.",
    # 5.2
    "Native iPhone photo, 4:5 portrait format.\n"
    "SUBJECT: A 51-year-old Hungarian woman sitting at her desk in an open-plan office, holding a small portable fan to her face. Her cheeks are flushed, neckline slightly damp, hair stuck to forehead. She's trying to be discrete but obviously uncomfortable.\n"
    "EXPRESSION: Self-conscious half-smile, \"this is happening at work\" energy.\n"
    "ENVIRONMENT: Hungarian office (visible co-worker out of focus, computer screen, papers). Mid-day natural light.\n"
    "NO TEXT OVERLAY.\n"
    "COLOR PALETTE: Office cool blue-grey, with warm flushed face as focal point.\n"
    "STYLE: Candid moment, like a friend texted you a \"OMG help\" selfie.",
    # 5.3
    "Bold graphic, 4:5 portrait format.\n"
    "BACKGROUND: Fiery orange-red gradient (#F4511E to #BF360C) top 65%. Bottom 35%: cool ice blue (#E0F4F8).\n"
    "HEADLINE (top, white bold sans-serif on red): \"5 ORVOS MONDTA, HOGY 'CSAK STRESSZ'.\". SUBLINE (italic, white): \"Aztán megtudtam az igazat.\".\n"
    "MIDDLE: Simple thermometer icon with high reading, surrounded by sweat-drop icons.\n"
    "BOTTOM (blue section, dark text):\n"
    "\"A HŐHULLÁM NEM SZTRESSZ. A HIPOTALAMUSZ HORMONÁLIS ZAVARA OKOZZA:\n"
    "↳ Ösztrogén ingadozás\n"
    "↳ Hipotalamusz tengely\n"
    "↳ Termoregulációs zavar\"\n"
    "BOTTOM RIGHT: Hormone Harmonia mockup in blue cool section.\n"
    "TYPOGRAPHY: Bold sans display, serif body.\n"
    "STYLE: High-contrast Best Probiotics / Halsten ad style.",
    # 5.4
    "Vintage scientific page, 4:5 portrait format.\n"
    "BACKGROUND: Aged parchment with subtle warm tones.\n"
    "CENTRAL: Hand-drawn vintage anatomical illustration of female body with \"thermal flushing zones\" indicated by hand-shaded watercolor reds — face, neck, chest. Like an 1890s thermal map.\n"
    "Small inset diagrams: hypothalamus close-up, estrogen molecule, a vintage thermometer. Hungarian cursive annotations.\n"
    "TOP TEXT (book title): \"A Klimax Hőhullámának Anatómiai Magyarázata\". Subtitle: \"A hipotalamusz és az ösztrogén szerepe — modern megértés\".\n"
    "BOTTOM RIGHT: Hand-drawn Hormone Harmonia bottle integration.\n"
    "COLOR: Sepia with warm watercolor red accents.\n"
    "STYLE: 1890s medical illustration page.",
    # 5.5
    "Documentary portrait, 4:5 portrait format.\n"
    "SUBJECT: A 53-year-old Hungarian woman \"Katalin\" outdoors in a Hungarian summer setting — perhaps a Balaton lakeside café terrace or a city park bench. She wears a light summer dress, no jacket needed (the \"I can finally wear summer clothes again\" moment). Slight wind in her hair, sunlight on her face, calm relieved expression.\n"
    "ENVIRONMENT: Hungarian outdoor summer scene — Balaton in background, or Margitsziget Budapest. Soft warm light.\n"
    "QUOTE OVERLAY (left side, serif):\n"
    "\"Tavaly nyáron mindig kabátot vittem magammal — nem tudtam mikor jön a következő hőhullám. Idén nyáron először érzem, hogy a testem újra az enyém.\"\n"
    "ATTRIBUTION: \"— Katalin, 53 éves, Veszprém\".\n"
    "BOTTOM RIGHT: Hormone Harmonia bottle on the café table next to her glass.\n"
    "COLOR PALETTE: Warm summer golden tones, blue sky/lake in background.\n"
    "STYLE: Magazine summer editorial, documentary feel, not fashion.",
]

BRAINFOG = [
    # 6.1
    "Scientific infographic, 4:5 portrait format.\n"
    "CENTRAL: Brain side-profile illustration with cognitive regions highlighted: hippocampus (memory) labeled \"EMLÉKEZET KÖZPONT\"; prefrontal cortex labeled \"DÖNTÉSI KÖZPONT\"; estrogen receptor map across brain labeled \"ÖSZTROGÉN-RECEPTOROK\".\n"
    "Below brain, a hormone-cognition link diagram showing how estrogen drop affects cognitive function.\n"
    "TOP HEADLINE: \"A BRAIN FOG NEM A KOR — A HORMONJAID.\". Subline: \"Miért ködös a fejed 45 felett? — Az ösztrogén-agy tengely magyarázata\".\n"
    "COLOR PALETTE: Cream parchment, deep purple-blue (#5C6BC0) accents.\n"
    "BOTTOM RIGHT: Hormone Harmonia bottle with subtle clarity-suggesting glow.\n"
    "STYLE: Halle Berry Pendulum cognitive ad / Black Girl Vitamins.",
    # 6.2
    "Native iPhone photo, 4:5 portrait format.\n"
    "SUBJECT: A 48-year-old Hungarian woman sitting at her home office desk, both hands on her temples, looking down at a laptop screen filled with text she can't focus on. Reading glasses pushed up on her forehead.\n"
    "EXPRESSION: Frustrated concentration loss — NOT crying, just \"I can't think today, what's happening to me\" exhausted.\n"
    "ENVIRONMENT: Home office with bookshelf, half-drunk coffee, scattered papers. Mid-day natural light.\n"
    "NO TEXT OVERLAY.\n"
    "COLOR PALETTE: Cool office light, slightly desaturated.\n"
    "STYLE: Real moment, like a friend captured it. Becca Fisher feel.",
    # 6.3
    "Bold graphic, 4:5 portrait format.\n"
    "BACKGROUND: Foggy gradient grey-blue (#B0BEC5 to #455A64) top 65%. Bottom 35%: bright clarity yellow (#FFD600).\n"
    "HEADLINE (top, white bold serif on grey): \"...HOGY IS HÍVTÁK?\". SUBLINE (white italic): \"Mit akartam mondani?\".\n"
    "MIDDLE: Simple graphic — a brain silhouette half-obscured by literal fog illustration.\n"
    "BOTTOM (yellow section, dark text):\n"
    "\"A BRAIN FOG NEM ÖREGEDÉS. A 3 HORMON, AMI A KONCENTRÁCIÓT ELLOPJA:\n"
    "↳ Ösztrogén (kognitív funkció)\n"
    "↳ Pajzsmirigy (mentális energia)\n"
    "↳ Kortizol (memória zavar)\"\n"
    "BOTTOM RIGHT: Hormone Harmonia mockup in yellow section.\n"
    "TYPOGRAPHY: Bold display serif, sans body.\n"
    "STYLE: High-contrast The New Knew / Halle Berry style.",
    # 6.4
    "Vintage scientific page, 4:5 portrait format.\n"
    "BACKGROUND: Aged paper with subtle blue-grey tint.\n"
    "CENTRAL: Hand-drawn anatomical brain illustration with old-style phrenology-inspired labels (but accurate modern anatomy). Small diagrams: hippocampus close-up, estrogen-receptor binding diagram, a vintage \"memory test\" chart. Hungarian cursive annotations.\n"
    "TOP TEXT (book title): \"A Női Agy Kognitív Változásai\". Subtitle: \"A perimenopauza alatti memóriazavar hormonális háttere\".\n"
    "BOTTOM RIGHT: Hand-sketched Hormone Harmonia bottle.\n"
    "COLOR: Sepia with subtle blue accents.\n"
    "STYLE: 1890s neurology textbook page.",
    # 6.5
    "Documentary portrait, 4:5 portrait format.\n"
    "SUBJECT: A 50-year-old Hungarian woman \"Marianna\" in a professional office setting, but candid — perhaps mid-presentation moment where she's confidently making a point. She wears smart-casual professional attire (blazer, simple blouse), age-appropriate, NOT corporate stereotype.\n"
    "EXPRESSION: Confident, focused, mid-thought. The \"I have my brain back\" energy.\n"
    "ENVIRONMENT: Modern Hungarian office with subtle local cues (Hungarian flag visible somewhere subtle, or Budapest skyline through a window).\n"
    "QUOTE OVERLAY (right side, serif):\n"
    "\"47 évesen majdnem felmondtam. A brain fog tönkretette a prezentációkat, a meetingeket. Most újra én vezetem a csapatom — és újra emlékszem a nevekre.\"\n"
    "ATTRIBUTION: \"— Marianna, 50 éves, Budapest\".\n"
    "BOTTOM RIGHT: Hormone Harmonia bottle on her desk.\n"
    "COLOR PALETTE: Modern professional cool tones with warm portrait lighting.\n"
    "STYLE: Forbes-magazine style portrait, but authentic.",
]

BLOCKS = [
    ("weightloss", WEIGHTLOSS),
    ("energy", ENERGY),
    ("sleep", SLEEP),
    ("mood", MOOD),
    ("hotflash", HOTFLASH),
    ("brainfog", BRAINFOG),
]

BRAND_LOCK = (
    "Product details (when visible): Hormone Harmonia — white plastic bottle with a purple/pink label, "
    "label reads 'Hormone Harmonia' and '72 vegán kapszula'. Optional cardboard box next to it."
)

NEGATIVE = (
    "Avoid: plastic skin, oversaturated colors, AI hands, distorted face, six fingers, blurry text, "
    "asymmetric eyes, perfect studio lighting, stock photo aesthetic, white teeth perfection, "
    "generic woman smiling, before-after collage, weight loss progress, body comparison, "
    "medical certificate, doctor's coat with name tag, fake science labels, watermark, brand logos, "
    "western model or American suburban setting (subject must read Hungarian)."
)


def build_full_prompt(prompt_text: str) -> str:
    return "\n\n".join([prompt_text, BRAND_LOCK, NEGATIVE])


def build_flat() -> dict:
    flat: dict = {}
    for desire, prompts in BLOCKS:
        assert len(prompts) == 5, f"{desire} has {len(prompts)} prompts, expected 5"
        for i, (style, prompt_text) in enumerate(zip(STYLES, prompts), start=1):
            pid = f"hh_v4_{desire}_{i:02d}"
            flat[pid] = {
                "compliance": desire,            # bulk_image_gen → subdir <desire>/
                "avatar": "hormone_harmonia_v4_desire",
                "angle": desire,
                "style": style,
                "variant": i,
                "full_prompt": build_full_prompt(prompt_text),
            }
    return flat


def main() -> None:
    flat = build_flat()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(yaml.safe_dump(flat, allow_unicode=True, sort_keys=False, width=140, default_flow_style=False), encoding="utf-8")
    print(f"wrote {OUT} ({len(flat)} prompts)")
    from collections import Counter
    print("by desire:", dict(Counter(v["angle"] for v in flat.values())))
    print("by style:", dict(Counter(v["style"] for v in flat.values())))


if __name__ == "__main__":
    main()
