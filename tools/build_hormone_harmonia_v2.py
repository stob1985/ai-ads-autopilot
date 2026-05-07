"""Convert the v2 Hormone Harmonia brief into pipeline-ready YAML.

Mirrors the Skintific v2 builder pattern: 50 prompts inline, brand-lock and
"Avoid" suffix appended to every full_prompt, flat YAML output keyed by id.

Run from the repo root:
    python tools/build_hormone_harmonia_v2.py

Outputs:
    config/hormone_harmonia_v2_source.yaml   — verbatim source record
    config/hormone_harmonia_v2_prompts.yaml  — flat, pipeline-ready
"""
from __future__ import annotations

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "config" / "hormone_harmonia_v2_source.yaml"
OUT = ROOT / "config" / "hormone_harmonia_v2_prompts.yaml"

# (angle, template, variant, prompt_text)
PROMPTS = [
    # ============================================================
    # ANGLE 1 — DOCTOR REVELATION
    # ============================================================
    ("doctor_revelation", "medical_infographic", 1,
     "Medical infographic style image, vertical 4:5 ratio. "
     "Clean white/cream background. Professional medical aesthetic.\n\n"
     "MAIN ELEMENT: A simple line drawing of a female silhouette in the center, "
     "with anatomical callouts pointing to internal organs:\n"
     "- Adrenal glands (above kidneys) → \"KORTIZOL\"\n"
     "- Ovaries → \"ÖSZTROGÉN + PROGESZTERON\"\n"
     "- Pancreas → \"INZULIN\"\n"
     "- Thyroid (neck) → \"PAJZSMIRIGY\"\n\n"
     "Dark grey thin lines connecting labels to organs. Each callout has a small bullet point with \"↑↓\" arrows showing imbalance.\n\n"
     "TOP TEXT (bold serif font, dark grey): \"Ezt EGYETLEN orvosi vérvizsgálat sem mutatja\"\n"
     "BELOW TITLE (smaller, italic): \"A 6 hormon, ami felborul 40 felett\"\n\n"
     "BOTTOM:\n- Small footnote: \"Forrás: Endokrinológiai Szakkönyv 2024\"\n- Tiny Hormone Harmonia bottle in lower right corner.\n\n"
     "STYLE: Looks like a page torn from a medical textbook. Authoritative, scientific, NOT a typical Facebook ad."),
    ("doctor_revelation", "medical_infographic", 2,
     "Medical chart / lab report style image, vertical 4:5.\n\n"
     "Background: Mockup of a printed lab test report on white paper, slightly crumpled, with \"BLOOD TEST RESULTS\" header. "
     "Top of page shows red stamp: \"ALL VALUES NORMAL\".\n\n"
     "OVERLAY TEXT (large, handwritten style red marker): \"DE NEM ÉRZEM MAGAM JÓL!\" with a hand-drawn arrow pointing to the report.\n\n"
     "Below the report (educational style): \"A vérvizsgálat csak az alapszinteket méri. A hormonális RITMUS nem látszik benne.\"\n\n"
     "Bottom: small Hormone Harmonia product image with text: \"12 hatóanyag - mind a 6 hormonra\".\n\n"
     "STYLE: Frustrated patient meets scientific reveal."),
    ("doctor_revelation", "medical_infographic", 3,
     "Split-screen medical infographic, vertical 4:5.\n\n"
     "LEFT SIDE: \"AMIT AZ ORVOS LÁT\" — small chart with green \"NORMAL\" indicators, 5-6 standard blood test markers (TSH, glucose, cholesterol). Clean, simple, OK feeling.\n\n"
     "RIGHT SIDE: \"AMIT VALÓJÁBAN ÉRZEL\" — same female silhouette but with red \"WARNING\" indicators. Multiple symptom callouts: \"Álmatlanság\", \"Hasi puffadás\", \"Fáradtság\", \"Hangulatingadozás\", \"Hőhullámok\". Red glow around problem areas.\n\n"
     "TOP TEXT (centered): \"AMIT AZ ORVOS NEM LÁT\"\n"
     "BOTTOM: \"A választ a hormonok adják - nem a vérképek.\" + small product placement.\n\n"
     "STYLE: Educational, authoritative, comparison-based."),
    ("doctor_revelation", "medical_infographic", 4,
     "Vintage medical poster style, vertical 4:5. Sepia/cream tones, old paper texture.\n\n"
     "TOP: \"AZ ENDOKRINOLÓGUSOK 80%-A NEM TUD ELÉG A PERIMENOPAUZÁRÓL\".\n\n"
     "MIDDLE: Vintage illustration of a woman's body with hormonal system highlighted. Old-fashioned anatomical drawing aesthetic. "
     "Side annotations (handwritten cursive): \"Cortisol spike\", \"Estrogen-Progesterone imbalance\", \"Insulin resistance\".\n\n"
     "BOTTOM: \"A modern megoldás: Hormone Harmonia™ — 12 természetes hatóanyag\".\n\n"
     "STYLE: Looks like a vintage scientific poster from a 1950s medical journal. Authoritative, educational, NOT salesy."),
    ("doctor_revelation", "medical_infographic", 5,
     "Modern medical chart with statistics, vertical 4:5. Clean white background, minimalist design.\n\n"
     "TOP STATISTIC (huge, bold black): \"80%\". Below in smaller text: \"of women aged 40+ have hormonal imbalance\" / \"but only 12% are properly diagnosed\".\n\n"
     "MIDDLE: Simple bar chart — Red bar: \"80% has imbalance\" / Green bar: \"12% gets diagnosed\" / Yellow bar: \"5% gets effective treatment\". Caption below: \"A magyar és nemzetközi adatok alapján\".\n\n"
     "BOTTOM: \"Ne legyél te is a 88%-ban, akiknek senki nem segít.\" + small Hormone Harmonia bottle.\n\n"
     "STYLE: Data-driven, modern infographic. Looks like content from Forbes Health or a medical journal."),
    ("doctor_revelation", "doctor_scene", 1,
     "Photorealistic medical office scene, vertical 4:5.\n\n"
     "A 48-year-old European woman sits across from a male doctor at his desk. The doctor is looking at his computer screen, NOT at her. "
     "The woman has a frustrated, tired expression — holding lab results papers.\n\n"
     "Visible: doctor's office setting — medical books, framed certificates, stethoscope on desk, computer monitor showing charts. Soft natural lighting from window.\n\n"
     "OVERLAY TEXT (top, white text on dark band): \"Ön teljesen egészséges - mondja az orvos.\"\n"
     "BOTTOM TEXT (red highlight): \"DE TE TUDOD, HOGY VALAMI BAJ VAN.\"\n\n"
     "STYLE: Documentary photo, NOT staged commercial. Captures real frustration moment."),
    ("doctor_revelation", "doctor_scene", 2,
     "Close-up portrait of woman holding crumpled lab results, vertical 4:5.\n\n"
     "A 50-year-old woman sitting in her car (after leaving the doctor's office). Hands holding a printed lab report. "
     "Her expression: defeated, frustrated, sad. Slight tears in her eyes.\n\n"
     "Background: blurred view through windshield — parking lot, gray day. Soft natural light from side.\n\n"
     "OVERLAY TEXT (top): \"Megint ugyanaz: 'Minden rendben.'\"\n"
     "MIDDLE (smaller): \"De a hasam puffadt, nem alszom, és nem ismerek magamra.\"\n"
     "BOTTOM: \"Talán senki sem figyel oda?\"\n\n"
     "STYLE: Intimate, emotional documentary moment. Real frustration, NOT staged."),
    ("doctor_revelation", "doctor_scene", 3,
     "Split image, vertical 4:5.\n\n"
     "TOP HALF: Doctor (smiling, dismissive) saying — speech bubble in cartoon style: \"Csak öregszik, nincs vele semmi baj.\"\n\n"
     "BOTTOM HALF: The same woman at home, in pajamas, looking defeated. Tears in her eyes. Time on clock visible: 3:47 AM.\n\n"
     "Connecting text in middle (red): \"DE A TÜNETEK CSAK ROMLANAK...\"\n\n"
     "BOTTOM (educational): \"12 hatóanyag, ami mind a 6 hormonra hat.\" + Hormone Harmonia logo.\n\n"
     "STYLE: Comic-strip meets reality. Educational with emotional punch."),
    ("doctor_revelation", "doctor_scene", 4,
     "Top-down view of a desk, vertical 4:5.\n\n"
     "On desk: 3 different lab result papers (slightly different doctors), all with green \"NORMAL\" stamps. A coffee cup, a pen, a tissue (used). "
     "A smartphone showing a Google search: \"miért érzem úgy magam?\". A woman's hands visible at edge of frame, holding her head in despair.\n\n"
     "OVERLAY TEXT (white box): \"3 orvos. 3 'minden rendben'. 0 megoldás.\"\n"
     "BOTTOM: \"Itt az idő, hogy te magad cselekedj.\"\n\n"
     "STYLE: Personal artifact arrangement. Documentary feel."),
    ("doctor_revelation", "doctor_scene", 5,
     "Modern healthcare scene, vertical 4:5.\n\n"
     "Younger female doctor (40s) showing concern, holding patient's hand. Patient (50s) is crying softly.\n\n"
     "Doctor speaks (subtitle text on image): \"A vérvizsgálat nem mutat mindent. A perimenopauzát máshol kell keresni.\"\n\n"
     "OVERLAY TEXT (top): \"VÉGRE EGY ORVOS, AKI MEGÉRT.\"\n"
     "BOTTOM: \"A modern endokrinológia már másképp gondolkodik.\" + Hormone Harmonia information.\n\n"
     "STYLE: Hopeful, supportive, validating moment."),

    # ============================================================
    # ANGLE 2 — WHATSAPP CHAT
    # ============================================================
    ("whatsapp_chat", "screenshot", 1,
     "Realistic WhatsApp group chat screenshot, vertical 9:16 (Story format).\n\n"
     "Group name at top: \"Bestik 💕\". Members visible: 4 women's profile pictures.\n\n"
     "MESSAGES (timestamps visible):\n\n"
     "22:47 - Andi: \"Lányok... megint nem aludtam. 3 órakor kalapált a szívem. ÚJRA.\"\n\n"
     "22:48 - Eszti: \"Andi, nálam ez van 6 hónapja. Az orvos azt mondja, csak stresszes vagyok 🙄\"\n\n"
     "22:50 - Kata: \"Várjatok... mind a hárman? És mi a helyzet a hasunkkal? Mintha 6 hónapos terhes lennék reggelre\"\n\n"
     "22:51 - Andi: \"OMG IGEN! És semmi sem segít. Mindent kipróbáltam\"\n\n"
     "22:53 - Zsuzsi: \"Lányok, nézzetek fel: HORMONE HARMONIA. Egy hónapja szedem és ÉLET-VÁLTOZÁS 🙏\" [Link mockup with Hormone Harmonia website]\n\n"
     "22:54 - Andi: \"Komolyan?? Megrendelem MOST\"\n\n"
     "STYLE: Authentic WhatsApp interface, realistic emojis, natural conversation. Time indicator at top, battery icon, etc. — looks like a REAL screenshot."),
    ("whatsapp_chat", "screenshot", 2,
     "WhatsApp 1-on-1 chat screenshot, vertical 9:16. Chat header: \"Anya 💝\".\n\n"
     "MESSAGES:\n\n"
     "MAMA (gray bubble): \"Drágám, hogy érzed magad mostanában?\"\n\n"
     "ME (green bubble): \"Anya... nem akarok panaszkodni, de... nem aludtam rendesen 4 hónapja.\"\n\n"
     "MAMA: \"Tudtam, hogy valami baj van. Múltkor olyan fáradtnak láttalak.\"\n\n"
     "ME: \"A hasam is felfújódott. Semmi nem megy fel rám. És mindenért kiborulok.\"\n\n"
     "MAMA: \"Drágám, EZ A PERIMENOPAUZA. Nálam is így kezdődött.\"\n\n"
     "ME: \"Komolyan? Mit csináltál?\"\n\n"
     "MAMA: \"Egy magyar készítmény segített: Hormone Harmonia. Próbáld ki, drágám. ÉN VISSZAKAPTAM ÖNMAGAM TŐLE.\" [Link]\n\n"
     "ME: \"Megrendelem ma 💕\"\n\n"
     "STYLE: Mother-daughter intimate conversation, hangulatos."),
    ("whatsapp_chat", "screenshot", 3,
     "WhatsApp story screenshot mockup, vertical 9:16. User profile at top: \"Kata Tamás (43)\".\n\n"
     "STORY CONTENT (text overlay on photo): \"Csajok, valami HIHETETLEN történt...\"\n\n"
     "Then transition to: photo of Hormone Harmonia bottle on bedside table, with handwritten note:\n\n"
     "\"Nem aludtam 8 hónapja. A férjem már az elválást fontolgatta volna 😅\n\n"
     "Ma reggel 7-kor ébredtem fel. NEM 3:14-kor.\n\n"
     "NE KÖSSETEK BELÉM, hogy reklámozok valamit. De ha valakinek segít, akkor szólok.\" [Link to product]\n\n"
     "BOTTOM (call-to-action style): \"Tap to swipe up\".\n\n"
     "STYLE: Authentic IG/WhatsApp story, NOT a polished ad."),
    ("whatsapp_chat", "screenshot", 4,
     "WhatsApp voice message visual, vertical 9:16.\n\n"
     "Single chat bubble showing voice message playing — Sender: \"Anyu (61)\", voice waveform visible, Duration: 1:47, \"Listening...\" indicator.\n\n"
     "OVERLAY TEXT (transcription style):\n\n"
     "\"Drágám, küldöm ezt a hangüzenetet, mert nem akartam gépelni. Tudod, hogy minden este sírtam emiatt...\" (waveform continues)\n\n"
     "\"...és a te nagymamád is ezzel küzdött. Senki nem segített neki. Én nem akarom, hogy te is így szenvedj...\" (more waveform)\n\n"
     "\"Próbáld meg ezt: HORMONE HARMONIA. Megváltoztatta az életem 60 évesen. Nálad még jobban fog működni.\"\n\n"
     "BOTTOM (small text): \"Az anyám hangját hallom, amikor használom.\"\n\n"
     "STYLE: Personal voice message, intimate, emotional."),
    ("whatsapp_chat", "screenshot", 5,
     "WhatsApp group chat with screenshots being shared, vertical 9:16. Group name: \"Anyukák 40 felett 👵\".\n\n"
     "One member shares 3 screenshots in succession:\n"
     "1. A \"before\" photo (caption: \"Január, 8 hónapja nem aludtam\")\n"
     "2. A Hormone Harmonia product photo (caption: \"Ezt szedtem 8 hetet\")\n"
     "3. An \"after\" photo — same woman, fresher (caption: \"Most. Aludtam reggelig.\")\n\n"
     "Other members reactions: \"OMG!! Mit szedtél??\", \"Ez te vagy??\", \"Megrendelem ma\", 12 ❤️ reactions.\n\n"
     "BOTTOM: \"Az igaz történetek megosztásáért indul minden...\" + Link.\n\n"
     "STYLE: Real group dynamic, multiple voices."),
    ("whatsapp_chat", "coffee_chat", 1,
     "Two women sitting at a coffee shop, vertical 4:5.\n\n"
     "Realistic scene: cozy coffee shop background, blurred. Both women 45-55, casual but stylish. Coffee cups visible, half empty. "
     "One woman leaning in, listening intently. Other woman gesturing while speaking, slight smile. Phones on table (one visible with Hormone Harmonia website).\n\n"
     "OVERLAY TEXT (top, conversation bubble style): \"Mióta szeded? És tényleg működik?\"\n"
     "BOTTOM TEXT: \"Néha a legjobb tanács nem az orvostól érkezik...\"\n\n"
     "STYLE: Authentic friendship moment, natural lighting."),
    ("whatsapp_chat", "coffee_chat", 2,
     "Mother and adult daughter at home, vertical 4:5.\n\n"
     "Setting: Cozy living room, evening warm light. Mother (60s, with grace) showing daughter (40s) something on her phone. "
     "Both women looking at phone screen with interest. On phone screen: Hormone Harmonia website (visible).\n\n"
     "OVERLAY TEXT: \"Anyu adott egy tippet, ami megváltoztatta az életem.\"\n"
     "BOTTOM: \"A bölcsesség generációkat ölel át.\"\n\n"
     "STYLE: Generational wisdom transfer, warm intimate moment."),
    ("whatsapp_chat", "coffee_chat", 3,
     "Group of 4 women at a wine night, vertical 4:5.\n\n"
     "Cozy living room. 4 women on a couch and chairs, wine glasses, snacks. They're all 42-55, casual evening attire. "
     "One woman is showing something on her phone to the others. The others are leaning in with curious expressions. Visible on phone: Hormone Harmonia bottle photo.\n\n"
     "OVERLAY TEXT: \"Csajok, MEG KELL nézzétek ezt...\"\n"
     "BOTTOM: \"Ami a barátnők között körözik, az tényleg működik.\"\n\n"
     "STYLE: Intimate friend group, authentic discovery moment."),
    ("whatsapp_chat", "coffee_chat", 4,
     "Two women at a yoga / gym class, vertical 4:5.\n\n"
     "After class scene. Both women in athletic wear, post-workout glow. Sitting on yoga mats, hydrating with water bottles. "
     "One woman is showing the other something on her phone.\n\n"
     "OVERLAY TEXT: \"Te is ennyi energiát nyertél vissza?\"\n"
     "BOTTOM: \"Két nő. Két különböző életkor. Egy közös titok.\"\n\n"
     "STYLE: Wellness-focused friendship, healthy lifestyle."),
    ("whatsapp_chat", "coffee_chat", 5,
     "Phone call screenshot mockup, vertical 9:16.\n\n"
     "Active phone call interface — Profile photo: \"Eszter 💕\", Call duration: 24:17, Speaker on.\n\n"
     "Above the call interface, transcribed conversation:\n\n"
     "\"Barátnőm, esküszöm... 8 hete szedem. A hasam lapos. Alszom reggelig. A férjem RÁNÉZ újra úgy, mint régen.\n\n"
     "Nem tudom, hogy ÉN vagyok-e még az a fáradt nő, aki 6 hónapja voltam.\n\n"
     "Ne vársz, próbáld ki MA.\"\n\n"
     "BOTTOM: \"Néha 24 perces telefonbeszélgetés többet ér, mint 12 orvosi konzultáció.\"\n\n"
     "STYLE: Modern phone interface, intimate confession."),

    # ============================================================
    # ANGLE 3 — SUMMER COUNTDOWN
    # ============================================================
    ("summer_countdown", "calendar", 1,
     "Calendar countdown visual, vertical 4:5. Background: light sunny yellow/cream gradient.\n\n"
     "MAIN ELEMENT: Large calendar pages flying off in chronological order — May 1, June 1, July 1, August 1 (highlighted).\n"
     "Above: Stopwatch icon with \"12 hét\".\n\n"
     "TOP TEXT (huge, bold): \"12 HÉT A NYÁRIG\".\n"
     "BELOW (smaller): \"Annyi idő, amennyi alatt visszakaphatod a régi tested - és magabiztosságod.\"\n\n"
     "BOTTOM: Hormone Harmonia product. Small text: \"8-12 hét: a hormonális egyensúly visszaállásának ideje\". Call-to-action: \"MOST KEZDD EL!\".\n\n"
     "STYLE: Energetic, motivational, time-pressured but hopeful."),
    ("summer_countdown", "calendar", 2,
     "Visual showing the same woman in 4 stages, vertical 4:5. Layout: 4 vertical panels showing transformation:\n\n"
     "Panel 1 (May): Tired, puffy, oversized clothes.\n"
     "Panel 2 (June): Slightly improved, less puffy.\n"
     "Panel 3 (July): Visibly healthier, more energy.\n"
     "Panel 4 (August): Confident, summer dress, beach background.\n\n"
     "Each panel labeled with month + week count from \"today\".\n\n"
     "TOP TEXT: \"EZ TÖRTÉNHET 12 HÉT ALATT.\"\n"
     "BOTTOM: \"Vagy maradhatsz, ahol most vagy. A választás a tied.\"\n\n"
     "STYLE: Aspirational transformation timeline."),
    ("summer_countdown", "calendar", 3,
     "Hand turning a vintage calendar page, vertical 4:5.\n\n"
     "Close-up of woman's hand turning calendar pages. Visible months: April → May → June → July → August. "
     "On August page: \"Saját esküvőm\" or \"Nyaralás Görögországban\" (handwritten in red). Top corner: a small Hormone Harmonia bottle on the desk.\n\n"
     "OVERLAY TEXT: \"Mit fog jelenteni augusztus számodra?\"\n"
     "BOTTOM: \"12 hét. 1 döntés. Új lehetőség.\"\n\n"
     "STYLE: Personal, nostalgic, decision-moment."),
    ("summer_countdown", "calendar", 4,
     "Sand timer / hourglass visual, vertical 4:5. Center: beautiful hourglass with golden sand falling. Half the sand is at top, half at bottom.\n\n"
     "Sand at top labeled: \"12 HÉT\". Sand at bottom labeled: \"AZ IDŐ MÚLIK\".\n\n"
     "TOP TEXT: \"Minden hét, amit elhalasztassz... egy hét, amit ELVESZÍTESZ.\"\n"
     "BOTTOM: \"Most 12 hét van a nyárig. Holnap már csak 11.\" + Hormone Harmonia product.\n\n"
     "STYLE: Symbolic, time-pressure, motivational."),
    ("summer_countdown", "calendar", 5,
     "Modern minimalist countdown poster, vertical 4:5. Background: soft pastel beach sunset gradient (peach, pink, orange).\n\n"
     "CENTER: Large countdown style: \"T - 84 NAP\" (= 12 weeks until summer).\n"
     "BELOW: \"Az idő, ami eldönti, milyen lesz a nyarad.\"\n\n"
     "Smaller bullet points:\n"
     "✓ Lapos has\n"
     "✓ Magabiztosság a fürdőruhában\n"
     "✓ Energia és vitalitás\n"
     "✓ Régi önbizalom\n\n"
     "BOTTOM: \"Kezdj el MOST. Köszönd meg magadnak augusztusban.\" + Hormone Harmonia product visible.\n\n"
     "STYLE: Modern, minimalist, aspirational."),
    ("summer_countdown", "summer_event", 1,
     "Beautiful 50-year-old woman at beach, vertical 4:5.\n\n"
     "Real Hungarian summer scene — Balaton beach. Woman in flattering swimsuit (one-piece or tankini), CONFIDENT pose. "
     "NOT model-thin, but REALISTIC and HEALTHY-looking. Smiling genuinely, hair blowing in wind. "
     "Background: Lake Balaton, blue sky, family in distance.\n\n"
     "OVERLAY TEXT (handwritten style): \"Először 5 év óta...\"\n"
     "BOTTOM: \"Visszakaptam a nyarat - és önmagam.\" + small Hormone Harmonia.\n\n"
     "STYLE: Authentic Hungarian beach moment, joyful."),
    ("summer_countdown", "summer_event", 2,
     "Woman at outdoor wedding, vertical 4:5.\n\n"
     "50-year-old woman in a beautiful summer dress. Outdoor wedding venue, garden setting, late afternoon golden light. "
     "She's standing alone, looking confident, slight smile.\n\n"
     "OVERLAY TEXT: \"A lányom esküvője. És MEGJELENTEM rajta.\"\n"
     "BOTTOM: \"(Tavaly még nem mertem volna.)\"\n\n"
     "STYLE: Confident, dressed up, special occasion."),
    ("summer_countdown", "summer_event", 3,
     "Garden party scene, vertical 4:5.\n\n"
     "Cozy backyard summer party. 4-5 women in summer dresses. The main subject (52) is CONFIDENT, gesturing while telling a story. "
     "Other women laughing, attentive.\n\n"
     "OVERLAY TEXT: \"Tavaly bujkáltam. Idén ÉN VAGYOK A LÉLEK.\"\n"
     "BOTTOM: + Hormone Harmonia product. \"Hogyan? Olvasd el az utamat.\"\n\n"
     "STYLE: Social, vibrant, confident comeback."),
    ("summer_countdown", "summer_event", 4,
     "Woman trying on a summer dress in store, vertical 4:5.\n\n"
     "Boutique fitting room. Woman 47 years old, mirror visible. Wearing a beautiful flowing summer dress. "
     "Smiling at her reflection, hands on hips, confident pose. A friend visible in mirror reflection, giving thumbs up.\n\n"
     "OVERLAY TEXT: \"VÁRJ. Ez az én testem??\"\n"
     "BOTTOM: \"8 hét. 1 döntés. Új ruhatár.\"\n\n"
     "STYLE: Joyful shopping moment, transformation reveal."),
    ("summer_countdown", "summer_event", 5,
     "Family vacation by pool, vertical 4:5.\n\n"
     "Mother (49) playing with kids/grandkids by hotel pool. She's IN THE WATER, laughing, splashing. Wearing fun colorful swimsuit. "
     "NOT hiding, NOT in cover-up, NOT on a chair watching. She's PARTICIPATING.\n\n"
     "OVERLAY TEXT: \"Először 6 év után BENT VAGYOK.\"\n"
     "BOTTOM: \"Nem a tükör mellett. NEM köntösben. Hanem ÉLŐBEN.\" + Hormone Harmonia.\n\n"
     "STYLE: Active, joyful, family bonding."),

    # ============================================================
    # ANGLE 4 — QUIET REBELLION
    # ============================================================
    ("quiet_rebellion", "typography", 1,
     "Typography-focused design, vertical 4:5. Bold dark red/burgundy background.\n\n"
     "CENTER (huge bold serif font, white): \"ELÉG VOLT\".\n\n"
     "BELOW (smaller, italic): \"Az 'ez csak a kor' válaszokból. Az 'csak stresszes' diagnózisokból. Abból, hogy senki nem hallgat meg minket.\"\n\n"
     "MIDDLE (medium): \"A 40+ NŐK ÚJ KORSZAKA.\"\n\n"
     "BOTTOM (small): \"Hormone Harmonia™ — Természetes válasz arra, amit az orvosok elmulasztottak elmondani.\"\n\n"
     "STYLE: Strong, manifesto-like, NOT a typical ad. Looks like a movement poster."),
    ("quiet_rebellion", "typography", 2,
     "Typography poster style, vertical 4:5. Cream background, dark green text.\n\n"
     "TOP (small): \"KEDVES ORVOS,\"\n\n"
     "MAIN BLOCK (large): \"AMIT NEKEM 'NORMÁLISKÉNT' DIAGNOSZTIZÁLSZ, AZ NEKEM ELVISELHETETLEN.\n\n"
     "AMIKOR AZT MONDOD, 'ÖREGSZIK', ÉN ÉLETET VESZÍTEK.\"\n\n"
     "BOTTOM: \"Üdvözlettel, Egy nő, aki MAGA TALÁLT MEGOLDÁST.\" + small Hormone Harmonia logo.\n\n"
     "STYLE: Open letter format, powerful, defiant."),
    ("quiet_rebellion", "typography", 3,
     "Statistics poster, vertical 4:5. Dark navy blue background, white text.\n\n"
     "TOP (large): \"HUSZONHAT ÉV.\"\n"
     "MIDDLE (smaller): \"Ennyit várunk átlagosan, hogy diagnosztizáljanak minket a perimenopauzával.\"\n"
     "(gap) \"EZ TARTHATATLAN.\"\n\n"
     "BOTTOM: \"Mi nem vársz további 26 évet. Mi MOST teszünk valamit.\" + Hormone Harmonia.\n\n"
     "STYLE: Statistical revelation, anger-based."),
    ("quiet_rebellion", "typography", 4,
     "Pull quote style design, vertical 4:5. White background, dark text. Large quotation marks at top.\n\n"
     "MAIN QUOTE: \"A férfi orvosok egy évtizedig mondták nekem, hogy 'csak stresszes vagyok.'\n\n"
     "Egy női gyógyszerész 5 perc alatt mondta el az IGAZAT.\n\n"
     "A különbség?\n\n"
     "Ő MAGA IS ÁTÉLTE.\"\n\n"
     "ATTRIBUTION: \"— Anna, 52 éves\".\n\n"
     "BOTTOM: \"Hormone Harmonia™ — Női fejlesztés, női nőknek.\"\n\n"
     "STYLE: Editorial, magazine-quote style."),
    ("quiet_rebellion", "typography", 5,
     "List-based manifesto, vertical 4:5. Black background, gold/yellow text.\n\n"
     "TITLE: \"MIT ÉRDEMLÜNK 40 FELETT?\"\n\n"
     "NUMBERED LIST:\n"
     "\"1. Azt, hogy meghallgassanak.\n"
     "2. Azt, hogy ne 'öregedés' legyen a diagnózis.\n"
     "3. Azt, hogy az alvás emberi jog legyen.\n"
     "4. Azt, hogy a tested ne legyen ellenség.\n"
     "5. Azt, hogy újra ÖNMAGUNK lehessünk.\"\n\n"
     "BOTTOM: \"5 alapvető jog. 1 természetes megoldás.\" + Hormone Harmonia.\n\n"
     "STYLE: Demanding, list-format, empowering."),
    ("quiet_rebellion", "powerful_women", 1,
     "Group of 5 women, ages 45-65, vertical 4:5.\n\n"
     "Standing together, slightly elevated angle. Diverse looks (hair, body types) but ALL CONFIDENT. "
     "Direct gaze at camera. NO smiling — serious, determined expression. Casual but stylish clothes (sweaters, jackets). Background: plain dark gray.\n\n"
     "OVERLAY TEXT (top): \"MI VAGYUNK A 88%.\"\n"
     "BOTTOM: \"Akiket évekig elhanyagoltak. És akik MOST cselekszünk.\"\n\n"
     "STYLE: Powerful, manifesto-style, NOT typical 'happy women' ad."),
    ("quiet_rebellion", "powerful_women", 2,
     "Single powerful woman portrait, vertical 4:5.\n\n"
     "A 55-year-old woman, silver hair (natural, beautiful). Direct, intense gaze. Strong jawline. Wearing simple black turtleneck.\n\n"
     "OVERLAY TEXT: \"Nem öregszem. NEM ROMLOM EL. ÉLEK.\"\n"
     "BOTTOM: \"Hormone Harmonia™ Természetes támogatás 40 felettiek számára.\"\n\n"
     "STYLE: Editorial portrait, strong female empowerment."),
    ("quiet_rebellion", "powerful_women", 3,
     "Women's protest-style image, vertical 4:5. But peaceful — several women holding handwritten signs at a coffee shop / community space (not actual protest).\n\n"
     "Signs read: \"MEGHALLGATÁST KÖVETELEK\", \"ALVÁS = JOGEMBER\", \"NE NEVEZD 'ÖREGEDÉSNEK'\", \"VISSZAKAPOM MAGAM\". Women smiling, supportive of each other, but signs serious.\n\n"
     "OVERLAY TEXT: \"NEMI EGYENLŐSÉGET A GYÓGYÍTÁSBAN.\"\n"
     "BOTTOM: \"Csendes forradalom kezdődik. Csatlakozz.\" + Hormone Harmonia.\n\n"
     "STYLE: Movement-style, community-driven."),
    ("quiet_rebellion", "powerful_women", 4,
     "Confident woman in suit, vertical 4:5.\n\n"
     "A 50-year-old woman in business attire (blazer, smart blouse). In an office or boardroom setting. "
     "Standing confidently, hands on hips. Slight smile, but eyes serious.\n\n"
     "OVERLAY TEXT: \"Ledelem a fortune 500 céget.\"\n"
     "BELOW: \"De nem tudtam ledelni a saját testem - amíg meg nem találtam ezt.\"\n\n"
     "BOTTOM: + Hormone Harmonia. \"12 hatóanyag = 6 hormon szabályozása\".\n\n"
     "STYLE: Professional, executive woman, capability-focused."),
    ("quiet_rebellion", "powerful_women", 5,
     "Three generations of women, vertical 4:5.\n\n"
     "Grandmother (78), Mother (52), Daughter (28) standing together. All confident, direct gaze.\n\n"
     "OVERLAY TEXT: \"A NAGYANYÁM CSENDBEN SZENVEDETT. AZ ANYÁM IS. ÉN NEM FOGOK.\"\n"
     "BOTTOM: \"Megtörjük a csendet. Megtaláljuk a megoldást. Természetesen.\" + Hormone Harmonia.\n\n"
     "STYLE: Generational empowerment, breaking cycles."),

    # ============================================================
    # ANGLE 5 — INVISIBLE TAX
    # ============================================================
    ("invisible_tax", "calculator", 1,
     "Calculator visualization, vertical 4:5. Center: large smartphone calculator showing complex calculation:\n\n"
     "27.000 Ft (havi alvássegítő)\n"
     "+ 15.000 Ft (anti-aging krém)\n"
     "+ 8.000 Ft (extra koffein)\n"
     "+ 35.000 Ft (új ruhák, mert a régiek nem mennek fel)\n"
     "+ 12.000 Ft (terápia)\n"
     "+ 23.000 Ft (étrend-kiegészítők)\n"
     "___________________\n"
     "= 120.000 Ft / hó\n"
     "= 1.440.000 Ft / év\n\n"
     "OVERLAY TEXT (top, red): \"AMIT VALÓJÁBAN FIZETSZ MOST\".\n\n"
     "BOTTOM: \"Hormone Harmonia™: 17.800 Ft (3 hónapra). MEGTAKARÍTÁS: 442.200 Ft / év.\"\n\n"
     "STYLE: Financial reveal, shocking."),
    ("invisible_tax", "calculator", 2,
     "Bills and receipts collage, vertical 4:5.\n\n"
     "Top-down view of various medical/wellness bills scattered: doctor visit receipts, lab test bills, pharmacy receipts (sleeping pills, antidepressants), beauty treatments, therapy sessions.\n\n"
     "Total scribbled in red marker on top: \"4.5 MILLIÓ FT / 5 ÉV\".\n\n"
     "OVERLAY TEXT: \"Mennyit költöttél eddig a TÜNETEKRE?\"\n"
     "BOTTOM: \"A megoldás 17.800 Ft volt mindvégig. Csak senki nem mondta el.\" + Hormone Harmonia.\n\n"
     "STYLE: Documentary, evidence-based."),
    ("invisible_tax", "calculator", 3,
     "Time-cost visualization, vertical 4:5. Horizontal timeline graphic.\n\n"
     "Title at top: \"MENNYIT VESZÍTESZ ÉVENTE?\"\n\n"
     "Sections of timeline:\n"
     "- \"🕐 240 óra elveszett alvás (= 30 nap!)\"\n"
     "- \"⏰ 156 óra orvosi várótermek\"\n"
     "- \"💊 365 nap stresszhormon kortizol-csúcs\"\n"
     "- \"💔 12 elszalasztott esemény (bujkálás miatt)\"\n\n"
     "Total at bottom: \"= 1 ÉV ÉLETSŰRŰSÉG\".\n\n"
     "OVERLAY TEXT: \"MIT VESZÍTESZ? Nem csak pénzt - ÉLETET.\"\n"
     "BOTTOM: Hormone Harmonia.\n\n"
     "STYLE: Time-impact visualization."),
    ("invisible_tax", "calculator", 4,
     "ROI / Investment visualization, vertical 4:5. Two columns side by side:\n\n"
     "LEFT COLUMN (red): \"BEFEKTETÉS\"\n"
     "- 17.800 Ft\n"
     "- 1 doboz / hónap\n"
     "- 3 kapszula / nap\n\n"
     "RIGHT COLUMN (green): \"MEGTÉRÜLÉS\"\n"
     "- 8 órás alvás (= 30 nap / év)\n"
     "- Lapos has (= 10 új ruhadarab)\n"
     "- Energia (= +200 produktív óra)\n"
     "- Magabiztosság (= felbecsülhetetlen)\n\n"
     "BOTTOM TEXT: \"ROI: 2,400% / év\".\n\n"
     "STYLE: Business presentation aesthetic."),
    ("invisible_tax", "calculator", 5,
     "\"Cost per day\" visualization, vertical 4:5. Center: large coin/currency illustration showing 200 Ft.\n\n"
     "MAIN TEXT: \"200 FT / NAP.\"\n\n"
     "Below: \"Pontosan ennyibe kerül a Hormone Harmonia.\n\n"
     "Ennyit fizetsz a NYUGODT ALVÁSÉRT. A LAPOS HASÉRT. A RÉGI ÖNMAGADÉRT.\"\n\n"
     "Comparison line:\n"
     "\"Egy kávé: 800 Ft\n"
     "Egy ebéd: 2.500 Ft\n"
     "Egy másfél órás Netflix: 1.200 Ft\n"
     "Hormone Harmonia: 200 Ft\"\n\n"
     "BOTTOM: \"Mi ér többet?\" + Hormone Harmonia.\n\n"
     "STYLE: Day-by-day breakdown, relatability."),
    ("invisible_tax", "life_cost", 1,
     "Sad realization moment, vertical 4:5.\n\n"
     "Woman in 50s sitting at kitchen table with calculator and notebook. Visible calculations on paper. Tears in her eyes, hand covering mouth.\n\n"
     "OVERLAY TEXT: \"Most kiszámoltam. 5.4 millió Ft-ot költöttem 5 év alatt tüneti kezelésre.\"\n"
     "BOTTOM: \"És még mindig itt vagyok. Még mindig nem aludtam. Még mindig sújtanak a tünetek.\" + small Hormone Harmonia. \"17.800 Ft. 30 nap garancia. Kiderül-e?\"\n\n"
     "STYLE: Realization moment, emotional but factual."),
    ("invisible_tax", "life_cost", 2,
     "Closet full of unworn clothes, vertical 4:5.\n\n"
     "Walk-in closet view. Lots of clothes still with tags on them. Designer labels visible. Most look 'summer,' 'elegant,' 'form-fitting.' "
     "A woman's hand visible, touching one dress sadly.\n\n"
     "OVERLAY TEXT: \"120.000 Ft ruha. Egyszer sem voltak rajtam.\"\n"
     "BOTTOM: \"Mert a hasam nem engedte. Hat hónapra ott álltak. 17.800 Ft. Ennyibe került volna a megoldás.\" + Hormone Harmonia.\n\n"
     "STYLE: Personal artifact, emotional."),
    ("invisible_tax", "life_cost", 3,
     "Empty seat at dinner table, vertical 4:5.\n\n"
     "Family dinner scene. Multiple people, but ONE empty seat with place setting still set. Slight blur on the empty space.\n\n"
     "OVERLAY TEXT: \"Ezen a vacsorán nem voltam ott. Mert nem mertem ránézni a tükörbe.\"\n"
     "BOTTOM: \"Az 5 elszalasztott családi vacsora ára: FELBECSÜLHETETLEN. A megoldás ára: 17.800 Ft.\" + Hormone Harmonia.\n\n"
     "STYLE: Emotional, family loss visualization."),
    ("invisible_tax", "life_cost", 4,
     "Two side-by-side scenes, vertical 4:5.\n\n"
     "LEFT: Woman alone, in oversized clothes, sitting on bed, surrounded by pill bottles and empty coffee cups.\n"
     "RIGHT: Same woman, well-dressed, with friends laughing at outdoor cafe.\n\n"
     "DIVIDER LINE in middle: \"17.800 Ft\".\n\n"
     "OVERLAY TEXT (top): \"Ennyi a különbség.\"\n"
     "BOTTOM: \"Egy doboz Hormone Harmonia: 17.800 Ft. A nyári élet visszanyerése: ÁRA NINCS.\"\n\n"
     "STYLE: Direct before/after with cost emphasis."),
    ("invisible_tax", "life_cost", 5,
     "Woman holding her grandchildren photo, vertical 4:5.\n\n"
     "50-something woman holding a photo of grandkids. She's smiling sadly at the photo. A wedding ring visible on her hand.\n\n"
     "OVERLAY TEXT: \"Az unokáim emlékezni fognak rám? Vagy csak arra, hogy 'nagymama mindig fáradt volt'?\"\n"
     "BOTTOM: \"Az emlékek értéke: felbecsülhetetlen. A megoldás: 17.800 Ft. Melyik számít többet?\" + Hormone Harmonia.\n\n"
     "STYLE: Emotional grandmother angle, legacy thinking."),
]


# ---- Globals appended to every full_prompt ----

BRAND_LOCK = (
    "Product details (must reproduce accurately): Hormone Harmonia™ — amber glass bottle with a "
    "pink/dusty-rose cap, white cardboard box with a Japanese wave pattern (gray/black on white). "
    "Label reads 'HORMONE HARMONIA' with '72 vegan kapszula' subtitle."
)

NEGATIVE = (
    "Avoid: stock photo aesthetics, airbrushed plasticky skin, model-thin idealized bodies, "
    "supplement industry clichés, generic clinical/medical blue palette where not appropriate, "
    "men as the primary subject, fake-looking transformations, AI artifacts, extra fingers, watermarks."
)


def build_full_prompt(prompt_text: str) -> str:
    return "\n\n".join([prompt_text, BRAND_LOCK, NEGATIVE])


def build_source() -> dict:
    return {
        "global_settings": {
            "brand_name": "Vital Harmony",
            "product_line": "Hormone Harmonia",
            "language": "hu-HU",
            "market": "HU",
            "aspect_ratio": "4:5",
            "product_image": "inputs/products/hormone_harmonia_box.png",
            "brand_lock": BRAND_LOCK,
            "negative_prompt": NEGATIVE,
            "totals": {
                "prompts": len(PROMPTS),
                "by_angle": {
                    a: sum(1 for p in PROMPTS if p[0] == a)
                    for a in sorted({p[0] for p in PROMPTS})
                },
                "by_template": {
                    t: sum(1 for p in PROMPTS if p[1] == t)
                    for t in sorted({p[1] for p in PROMPTS})
                },
            },
        },
        "prompts": [
            {
                "id": f"{angle}_{template}_v{variant}",
                "angle": angle,
                "template": template,
                "variant": variant,
                "prompt": prompt_text,
            }
            for (angle, template, variant, prompt_text) in PROMPTS
        ],
    }


def build_flat() -> dict:
    flat: dict = {}
    for (angle, template, variant, prompt_text) in PROMPTS:
        pid = f"{angle}_{template}_v{variant}"
        flat[pid] = {
            # `avatar` is set to a constant tag so build_filename uses the
            # tidy pid-based name (avoids the legacy verbose form). It also
            # stays consistent with how the Skintific v2 batch was tagged.
            "avatar": "hormone_harmonia_v2",
            "angle": angle,
            "template": template,
            "variant": variant,
            "phase": 1,
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
