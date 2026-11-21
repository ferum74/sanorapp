#!/usr/bin/env python3
"""
Builds the Sanor home page in four languages from one template.

    python3 scripts/build_home.py

Writes:  index.html (EN),  cz/index.html (Czech),  es/index.html (Spanish),  de/index.html (German)

To change text: edit the TEXT dictionary below (en / cs / es blocks; German is in scripts/i18n_de.py) and re-run.
To change layout: edit render() below. Shared styles live in assets/site.css.
The legal pages (support / privacy / terms / delete-account) are plain HTML files.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.sanorapp.com"
APPSTORE = "https://apps.apple.com/cz/app/sanor/id6766075127"
EMAIL = "sanor.help@gmail.com"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i18n_de import DE, AWARD_DE  # noqa: E402
from i18n_cycle import apply as apply_cycle  # noqa: E402

# (language key, label in the switcher, URL path). The Czech key stays "cs" (the ISO code used in
# hreflang / <html lang>), but the site address and the label are "cz".
LANGS = [("en", "EN", "/"), ("cs", "CZ", "/cz/"), ("es", "ES", "/es/"), ("de", "DE", "/de/")]

# ── Icons (inline SVG, Feather-style) ─────────────────────────────────────────
_ICONS = {
    "bell": '<path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.7 21a2 2 0 0 1-3.4 0"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    "box": '<path d="M21 16V8a2 2 0 0 0-1-1.7l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.7l7 4a2 2 0 0 0 2 0l7-4a2 2 0 0 0 1-1.7z"/><path d="M3.3 7 12 12l8.7-5M12 22V12"/>',
    "activity": '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/>',
    "heart": '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1 1.1L12 21.2l7.8-7.7 1-1.1a5.5 5.5 0 0 0 0-7.8z"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "award": '<circle cx="12" cy="8" r="6"/><path d="M15.5 13.9 17 23l-5-3-5 3 1.5-9.1"/>',
    "lock": '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "alert": '<path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/>',
    "phone": '<rect x="5" y="2" width="14" height="20" rx="2"/><path d="M12 18h.01"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "down": '<path d="M12 3v12m0 0-5-5m5 5 5-5M5 21h14"/>',
    "chev": '<path d="m6 9 6 6 6-6"/>',
    "undo": '<path d="M3 7v6h6"/><path d="M21 17a9 9 0 0 0-15-6.7L3 13"/>',
    "flame": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.4-.5-2-1-3-1.1-2.1-.2-4 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.2.4-2.4 1-3 0 1.3 1 2.5 2.5 2.5z"/>',
    "wifi": '<path d="M5 12.6a10 10 0 0 1 14 0M8.5 16.1a5 5 0 0 1 7 0M2 9a15 15 0 0 1 20 0M12 20h.01"/>',
    "drop": '<path d="M12 2.7 5.6 9.1a9 9 0 1 0 12.8 0z"/>',
    "arrow": '<path d="M5 12h14m-6-6 6 6-6 6"/>',
}


def ico(name, cls="ico"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{_ICONS[name]}</svg>'


# ── Text ─────────────────────────────────────────────────────────────────────
# Award names are taken verbatim from the app's own Localizable.xcstrings.
AWARDS = [
    # (image, en, cs, es)
    ("hello", "Hello, Sanor", "Ahoj, Sanor", "Hola, Sanor"),
    ("fifty_doses", "Getting the Hang of It", "Už mi to jde", "Cogiendo el ritmo"),
    ("seven_day", "Week Strong", "Celý týden", "Semana firme"),
    ("early_bird", "Early Bird", "Ranní ptáče", "Madrugador"),
    ("thirty_day", "Monthly Champion", "Šampion měsíce", "Campeón del mes"),
    ("night_owl", "Night Owl", "Noční sova", "Noctámbulo"),
    ("hundred_days", "Hundred Days", "Sto dní", "Cien días"),
    ("year_of_care", "Year of Care", "Rok péče", "Un año de cuidado"),
]

TEXT = {
    "en": {
        "html_lang": "en",
        "title": "Sanor – Medication reminders, supply tracker & health diary for iPhone",
        "desc": "Sanor is a free iPhone app that reminds you to take your medication, tracks your supply, logs symptoms and mood, and creates PDF reports for your doctor. Your health data stays on your phone.",
        "og_title": "Sanor – Never miss a dose ever again",
        "skip": "Skip to content",
        "nav_tour": "App tour", "nav_features": "Features", "nav_rewards": "Rewards", "nav_faq": "FAQ", "nav_support": "Support",
        "nav_cta": "Download",
        "pill": "Free for iPhone · Android coming soon",
        "h1": "Never miss a dose <em>ever again.</em>",
        "sub": "Sanor is a friendly medication companion: reminders you can answer right from the notification, a supply tracker, a symptom and mood diary, and reports ready for your doctor. Your health data stays on your phone.",
        "btn_store": "Download on the App Store",
        "btn_how": "See how it works",
        "chips": ["Free to download", "Data stays on your iPhone", "No ads, no tracking", "iOS 17 or later"],
        "float_streak": ("21-day streak", "Keep it going!"),
        "float_taken": ("Omega-3 · 8:00 PM", "Marked as taken"),
        "float_supply": ("About 5 days left", "Time to buy a new pack"),
        "stats": [("Free", "to download"), ("7", "app languages"), ("24", "otter awards"), ("0", "ads or trackers")],
        "tour_eyebrow": "Take a tour",
        "tour_h2": "Everything you need, calmly in one place.",
        "tour_p": "From the first reminder to the doctor's visit, Sanor keeps your routine simple.",
        "r1_h": "Reminders you can answer in one tap",
        "r1_p": "Mark a dose as Taken, Snooze it or Skip it right from the notification. Forgot? Sanor nudges you again, and you choose how often.",
        "r1_t": ["Taken, Snooze and Skip in the notification", "Repeat reminders until you mark the dose", "Hide medicine names on the lock screen", "Turn reminders off for a single medicine"],
        "r2_h": "Know when to buy the next pack",
        "r2_p": "Enter how many tablets are in the box. Sanor shows how many days they will last, how many you need to finish a course, and warns you before they run out.",
        "r2_t": ["Days left and the date your supply lasts until", "A heads-up before the pack is empty", "One tap on “I bought a pack” to update it"],
        "r3_h": "See how doses, symptoms and mood fit together",
        "r3_p": "Doses, symptoms and mood side by side, day by day, for a week, a month or three months, so patterns become easy to notice.",
        "r3_t": ["Week, month and 3-month views", "Log symptoms with intensity and notes", "Optional cycle tracking with predictions"],
        "r4_h": "Bring a report to your next appointment",
        "r4_p": "Export a PDF for the last week, last month, all time or any custom range: missed doses, symptoms, mood and averages from Apple Health.",
        "r4_t": ["Share the PDF with your doctor in a tap", "Add your daily doses to iPhone Calendar", "Streaks and adherence at a glance"],
        "more_eyebrow": "And more",
        "more_h2": "Small details, big peace of mind.",
        "more_p": "Sanor is built around the little things that make a daily routine easier to keep.",
        "new": "New in 1.7",
        "b1_h": "Smarter interaction checks",
        "b1_p": "Sanor now spots two medicines of the same kind (for example two statins or two painkillers from one group), risky combinations by mechanism, and medicines that should be taken at different times. If a medicine could not be checked, the app says so instead of staying silent.",
        "b2_h": "Food and alcohol notes",
        "b2_p": "Short notes on grapefruit, dairy, vitamin K and alcohol right in each medicine’s card.",
        "b3_h": "A medicine database that speaks your language",
        "b3_p": "Find your medicine by the name on the box: thousands of local brand names from Czech, Slovak, Ukrainian, Russian and Spanish registers.",
        "b4_h": "Apple Health, if you want it",
        "b4_p": "With your permission, Sanor shows steps, heart rate and activity next to your medication log. You stay in control in iOS settings.",
        "b5_h": "Fix a mistaken tap",
        "b5_p": "Marked the wrong dose? Undo it right away, or flip a dose between Taken and Missed with one tap.",
        "rw_eyebrow": "Rewards",
        "rw_h2": "Meet the otters that cheer you on.",
        "rw_p": "Take your doses, keep a rhythm and look after yourself to unlock 24 otter awards for milestones, daily habits and caring for your health.",
        "news_eyebrow": "What’s new",
        "news_h2": "Sanor keeps getting better.",
        "news_p": "Regular updates, shaped by what people actually need.",
        "ver17": "Version 1.7",
        "news17_h": "Smarter, more honest interaction checks",
        "news17": ["Spots two medicines of the same kind, risky combinations by mechanism, and medicines that should be taken at different times.", "Short notes on alcohol and food (grapefruit, dairy, vitamin K) in a medicine’s card.", "Honest status: if a medicine could not be checked, the app says so instead of showing nothing."],
        "old": [
            ("1.6", "Over 110 new medicines and thousands of local brand names from Czech, Slovak, Ukrainian, Russian and Spanish registers. New warnings about risky combinations."),
            ("1.5", "Correct a mistaken mark with Undo, or flip Taken and Missed with a tap."),
            ("1.4", "Spanish is here: the app and the medicine database now speak Spanish, including Spanish brand names."),
        ],
        "pl_eyebrow": "Where to get it",
        "pl_h2": "On your phone, in your language.",
        "pl_p": "Sanor speaks seven languages, so your routine feels natural wherever you are.",
        "pl_ios": "iPhone", "pl_ios_s": "Available now", "pl_ios_p": "Free on the App Store. Requires iOS 17 or later. Sign in with Apple or email.",
        "pl_and": "Android", "pl_and_s": "In development", "pl_and_p": "An Android version is on the way. This page will link to Google Play as soon as it is ready.",
        "pl_soon": "Coming soon",
        "langs": ["English", "Čeština", "Slovenčina", "Deutsch", "Русский", "Українська", "Español"],
        "pv_h2": "Your health data stays yours.",
        "pv_p": "Sanor was designed to collect as little as possible. No ads, no analytics, no data sales.",
        "pv": [("phone", "On your iPhone", "Medications, doses, symptoms, mood and cycle entries are stored on your device."), ("lock", "A small profile online", "Only your sign-in and a small profile are stored, so you can sign back in on a new phone."), ("shield", "You are in control", "Export or share data only if you choose to, and delete your account any time in the app.")],
        "pv_more": "Read the Privacy Policy",
        "faq_eyebrow": "FAQ",
        "faq_h2": "Quick answers.",
        "faq": [
            ("Is Sanor really free?", "<p>Yes. Sanor is free to download on the App Store. It requires iOS 17 or later, and you sign in with Apple or email.</p>"),
            ("Is Sanor a medical app?", "<p>No. Sanor does not replace a doctor, a pharmacist or medical advice. It helps you organize your schedule and stay consistent. If Sanor shows a possible interaction, talk to your doctor or pharmacist. Not seeing a warning does not mean a combination is safe.</p>"),
            ("Where is my health data stored?", "<p>Your medications, doses, symptoms, mood notes and cycle entries are stored on your iPhone. Your account and a small profile are stored with Google Firebase so you can sign back in on a new phone. We do not sell data, show ads or track you.</p>"),
            ("Do reminders work offline?", "<p>Yes. Reminders are scheduled on your phone, so they work without an internet connection.</p>"),
            ("Is there an Android version?", "<p>It is in development. Once it is ready, this page will link to Google Play.</p>"),
        ],
        "faq_more": "More answers in the Help Center →",
        "cta_h2": "Start your healthier routine today.",
        "cta_p": "Free to download. Requires iOS 17 or later. Sign in with Apple or email.",
        "foot_p": "A smart medication companion for a healthier, more consistent life.",
        "foot_product": "Product", "foot_legal": "Legal", "foot_support": "Support",
        "foot_tour": "App tour", "foot_download": "Download",
        "foot_privacy": "Privacy Policy", "foot_terms": "Terms of Use", "foot_delete": "Delete account",
        "foot_help": "Help Center", "foot_faq": "FAQ", "foot_contact": "Contact us", "foot_how": "How to use",
        "foot_credit": "Czech medicine names: SÚKL open data · Spanish: AEMPS CIMA.",
        "foot_disc": "Sanor is not a medical device and does not replace professional medical advice.",
        "alt_home": "Sanor home screen with today’s medicines, a 21-day streak and the otter mascot",
        "alt_reminders": "Reminder settings: remind me again, snooze and hide medicine names",
        "alt_supply": "Medication supply screen showing about 5 days left",
        "alt_timeline": "Timeline of doses, symptoms and mood for the week",
        "alt_reports": "Reports screen with PDF export for last week, last month, all time or custom range",
        "alt_rewards": "Rewards screen showing 16 of 24 otter awards unlocked",
        "alt_otter": "Sanor otter mascot",
    },
    "cs": {
        "html_lang": "cs",
        "title": "Sanor – Připomínky léků, zásoby a zdravotní deník pro iPhone",
        "desc": "Sanor je bezplatná aplikace pro iPhone, která vám připomene užít léky, hlídá zásoby, zapisuje příznaky a náladu a vytvoří PDF zprávu pro lékaře. Vaše zdravotní data zůstávají v telefonu.",
        "og_title": "Sanor – Nikdy už nezapomeňte na dávku",
        "skip": "Přeskočit na obsah",
        "nav_tour": "Prohlídka", "nav_features": "Funkce", "nav_rewards": "Odměny", "nav_faq": "Časté dotazy", "nav_support": "Podpora",
        "nav_cta": "Stáhnout",
        "pill": "Zdarma pro iPhone · Android již brzy",
        "h1": "Nikdy už <em>nezapomeňte na dávku.</em>",
        "sub": "Sanor je přátelský společník pro vaše léky: připomínky, na které odpovíte přímo z upozornění, přehled zásob, deník příznaků a nálady a zprávy pro lékaře. Vaše zdravotní data zůstávají v telefonu.",
        "btn_store": "Stáhnout z App Store",
        "btn_how": "Jak to funguje",
        "chips": ["Zdarma ke stažení", "Data zůstávají v iPhonu", "Bez reklam a sledování", "iOS 17 nebo novější"],
        "float_streak": ("Série 21 dní", "Jen tak dál!"),
        "float_taken": ("Omega-3 · 20:00", "Označeno jako užité"),
        "float_supply": ("Zbývá asi 5 dní", "Čas koupit nové balení"),
        "stats": [("Zdarma", "ke stažení"), ("7", "jazyků aplikace"), ("24", "odměn s vydrou"), ("0", "reklam a trackerů")],
        "tour_eyebrow": "Prohlídka aplikace",
        "tour_h2": "Všechno, co potřebujete, na jednom klidném místě.",
        "tour_p": "Od první připomínky po návštěvu lékaře: Sanor vám usnadní každodenní rutinu.",
        "r1_h": "Připomínky, na které odpovíte jedním klepnutím",
        "r1_p": "Dávku označte jako užitou, odložte ji nebo přeskočte přímo z upozornění. Zapomněli jste? Sanor vám ji připomene znovu a vy si zvolíte, jak často.",
        "r1_t": ["Vzal(a) jsem, Odložit a Přeskočit přímo v upozornění", "Opakované připomínky, dokud dávku neoznačíte", "Skrytí názvů léků na zamčené obrazovce", "Připomínky lze vypnout u jednoho léku"],
        "r2_h": "Vězte, kdy koupit další balení",
        "r2_p": "Zadejte, kolik tablet je v balení. Sanor ukáže, na kolik dní vystačí, kolik jich potřebujete na dokončení kúry, a upozorní vás dřív, než dojdou.",
        "r2_t": ["Zbývající dny a datum, do kterého zásoba vystačí", "Upozornění před koncem balení", "Jedno klepnutí na „Koupil(a) jsem balení“"],
        "r3_h": "Uvidíte, jak spolu souvisí dávky, příznaky a nálada",
        "r3_p": "Dávky, příznaky a nálada vedle sebe, den po dni, za týden, měsíc nebo tři měsíce, abyste si snadno všimli souvislostí.",
        "r3_t": ["Zobrazení za týden, měsíc a 3 měsíce", "Zápis příznaků s intenzitou a poznámkami", "Volitelné sledování cyklu s předpovědí"],
        "r4_h": "Přineste si zprávu na další návštěvu",
        "r4_p": "Exportujte PDF za poslední týden, měsíc, celou dobu nebo libovolné období: vynechané dávky, příznaky, nálada a průměry z Apple Zdraví.",
        "r4_t": ["PDF pošlete lékaři jedním klepnutím", "Denní dávky přidáte do kalendáře iPhonu", "Série a pravidelnost na první pohled"],
        "more_eyebrow": "A dál",
        "more_h2": "Drobnosti, díky kterým je to snazší.",
        "more_p": "Sanor je postavený na maličkostech, které pomáhají udržet každodenní rutinu.",
        "new": "Novinka v 1.7",
        "b1_h": "Chytřejší kontrola interakcí",
        "b1_p": "Sanor nově pozná dva léky stejného druhu (např. dva statiny nebo dvě léčiva proti bolesti ze stejné skupiny), rizikové kombinace podle mechanismu účinku a léky, které se mají užívat v jiný čas. Pokud lék nešlo zkontrolovat, aplikace to řekne, místo aby mlčela.",
        "b2_h": "Poznámky k jídlu a alkoholu",
        "b2_p": "Krátké poznámky ke grapefruitu, mléčným výrobkům, vitaminu K a alkoholu přímo v kartě léku.",
        "b3_h": "Databáze léků, která mluví vaším jazykem",
        "b3_p": "Lék najdete podle názvu na krabičce: tisíce místních názvů z českého, slovenského, ukrajinského, ruského a španělského registru.",
        "b4_h": "Apple Zdraví, pokud chcete",
        "b4_p": "S vaším svolením Sanor zobrazí kroky, tep a aktivitu vedle záznamu o lécích. Oprávnění můžete kdykoli změnit v nastavení iOS.",
        "b5_h": "Oprava omylem označené dávky",
        "b5_p": "Označili jste špatnou dávku? Hned ji vraťte zpět, nebo jedním klepnutím přepněte mezi Užito a Vynecháno.",
        "rw_eyebrow": "Odměny",
        "rw_h2": "Seznamte se s vydrami, které vám fandí.",
        "rw_p": "Plňte dávky, držte rytmus a pečujte o sebe: odemknete 24 odměn s vydrou za milníky, denní rytmus i péči o zdraví.",
        "news_eyebrow": "Novinky",
        "news_h2": "Sanor se neustále zlepšuje.",
        "news_p": "Pravidelné aktualizace podle toho, co lidé skutečně potřebují.",
        "ver17": "Verze 1.7",
        "news17_h": "Chytřejší a upřímnější kontrola interakcí",
        "news17": ["Pozná dva léky stejného druhu, rizikové kombinace podle mechanismu účinku a léky, které se mají užívat v jiný čas.", "Krátké poznámky k alkoholu a jídlu (grapefruit, mléčné výrobky, vitamin K) v kartě léku.", "Upřímný stav: pokud lék nešlo zkontrolovat, aplikace to řekne, místo aby nezobrazila nic."],
        "old": [
            ("1.6", "Přes 110 nových léků a tisíce místních názvů z českého, slovenského, ukrajinského, ruského a španělského registru. Nová upozornění na rizikové kombinace."),
            ("1.5", "Chybné označení opravíte tlačítkem Zpět, nebo jedním klepnutím přepnete Užito a Vynecháno."),
            ("1.4", "Přibyla španělština: aplikace i databáze léků nově mluví španělsky, včetně španělských obchodních názvů."),
        ],
        "pl_eyebrow": "Kde ji získat",
        "pl_h2": "V telefonu a ve vašem jazyce.",
        "pl_p": "Sanor mluví sedmi jazyky, takže vaše rutina působí přirozeně, ať jste kdekoli.",
        "pl_ios": "iPhone", "pl_ios_s": "Již dostupné", "pl_ios_p": "Zdarma v App Store. Vyžaduje iOS 17 nebo novější. Přihlášení přes Apple nebo e-mail.",
        "pl_and": "Android", "pl_and_s": "Ve vývoji", "pl_and_p": "Verze pro Android se připravuje. Jakmile bude hotová, najdete tady odkaz na Google Play.",
        "pl_soon": "Již brzy",
        "langs": ["English", "Čeština", "Slovenčina", "Deutsch", "Русский", "Українська", "Español"],
        "pv_h2": "Vaše zdravotní data zůstávají vaše.",
        "pv_p": "Sanor je navržený tak, aby sbíral co nejméně. Žádné reklamy, žádná analytika, žádný prodej dat.",
        "pv": [("phone", "V iPhonu", "Léky, dávky, příznaky, nálada i záznamy cyklu jsou uložené ve vašem zařízení."), ("lock", "Malý profil online", "Online je uložené jen vaše přihlášení a malý profil, abyste se mohli přihlásit na novém telefonu."), ("shield", "Rozhodujete vy", "Data exportujete nebo sdílíte jen tehdy, když chcete, a účet můžete kdykoli smazat v aplikaci.")],
        "pv_more": "Přečtěte si Zásady ochrany soukromí (EN)",
        "faq_eyebrow": "Časté dotazy",
        "faq_h2": "Rychlé odpovědi.",
        "faq": [
            ("Je Sanor opravdu zdarma?", "<p>Ano. Sanor je v App Store zdarma. Vyžaduje iOS 17 nebo novější a přihlašujete se přes Apple nebo e-mail.</p>"),
            ("Je Sanor zdravotnická aplikace?", "<p>Ne. Sanor nenahrazuje lékaře, lékárníka ani lékařskou radu. Pomáhá vám uspořádat si rozvrh a být důsledný. Když Sanor zobrazí možnou interakci, poraďte se s lékařem nebo lékárníkem. Pokud upozornění nevidíte, neznamená to, že je kombinace bezpečná.</p>"),
            ("Kde jsou uložená moje zdravotní data?", "<p>Léky, dávky, příznaky, poznámky o náladě a záznamy cyklu jsou uložené ve vašem iPhonu. Účet a malý profil jsou uložené u Google Firebase, abyste se mohli přihlásit na novém telefonu. Data neprodáváme, nezobrazujeme reklamy a nesledujeme vás.</p>"),
            ("Fungují připomínky offline?", "<p>Ano. Připomínky se plánují přímo v telefonu, takže fungují i bez připojení k internetu.</p>"),
            ("Existuje verze pro Android?", "<p>Připravuje se. Jakmile bude hotová, najdete na této stránce odkaz na Google Play.</p>"),
        ],
        "faq_more": "Další odpovědi v centru nápovědy (EN) →",
        "cta_h2": "Začněte zdravější rutinu ještě dnes.",
        "cta_p": "Zdarma ke stažení. Vyžaduje iOS 17 nebo novější. Přihlášení přes Apple nebo e-mail.",
        "foot_p": "Chytrý společník pro vaše léky a zdravější, pravidelnější život.",
        "foot_product": "Produkt", "foot_legal": "Právní informace", "foot_support": "Podpora",
        "foot_tour": "Prohlídka", "foot_download": "Stáhnout",
        "foot_privacy": "Zásady ochrany soukromí (EN)", "foot_terms": "Podmínky použití (EN)", "foot_delete": "Smazání účtu (EN)",
        "foot_help": "Centrum nápovědy (EN)", "foot_faq": "Časté dotazy (EN)", "foot_contact": "Kontakt", "foot_how": "Jak aplikaci používat (EN)",
        "foot_credit": "České názvy léků: otevřená data SÚKL · španělské: AEMPS CIMA.",
        "foot_disc": "Sanor není zdravotnický prostředek a nenahrazuje odbornou lékařskou radu.",
        "alt_home": "Úvodní obrazovka Sanor s dnešními léky, sérií 21 dní a vydrou",
        "alt_reminders": "Nastavení připomínek: připomenout znovu, odložit a skrýt názvy léků",
        "alt_supply": "Obrazovka zásob léku, zbývá asi 5 dní",
        "alt_timeline": "Časová osa dávek, příznaků a nálady za týden",
        "alt_reports": "Obrazovka zpráv s exportem PDF za týden, měsíc, celou dobu nebo vlastní období",
        "alt_rewards": "Odměny: odemčeno 16 z 24 odměn s vydrou",
        "alt_otter": "Vydra, maskot aplikace Sanor",
    },
    "es": {
        "html_lang": "es",
        "title": "Sanor – Recordatorios de medicación, existencias y diario de salud para iPhone",
        "desc": "Sanor es una app gratuita para iPhone que te recuerda tomar tus medicamentos, controla tus existencias, registra síntomas y ánimo y crea informes en PDF para tu médico. Tus datos de salud se quedan en tu teléfono.",
        "og_title": "Sanor – Nunca más olvides una toma",
        "skip": "Saltar al contenido",
        "nav_tour": "Recorrido", "nav_features": "Funciones", "nav_rewards": "Logros", "nav_faq": "Preguntas", "nav_support": "Ayuda",
        "nav_cta": "Descargar",
        "pill": "Gratis para iPhone · Android próximamente",
        "h1": "Nunca más <em>olvides una toma.</em>",
        "sub": "Sanor es un compañero amable para tus medicamentos: recordatorios que respondes desde la propia notificación, control de existencias, diario de síntomas y ánimo, e informes listos para tu médico. Tus datos de salud se quedan en tu teléfono.",
        "btn_store": "Descargar en App Store",
        "btn_how": "Ver cómo funciona",
        "chips": ["Descarga gratuita", "Los datos se quedan en tu iPhone", "Sin anuncios ni seguimiento", "iOS 17 o posterior"],
        "float_streak": ("Racha de 21 días", "¡Sigue así!"),
        "float_taken": ("Omega-3 · 20:00", "Marcada como tomada"),
        "float_supply": ("Quedan unos 5 días", "Hora de comprar un envase nuevo"),
        "stats": [("Gratis", "para descargar"), ("7", "idiomas en la app"), ("24", "logros de nutria"), ("0", "anuncios o rastreadores")],
        "tour_eyebrow": "Recorrido por la app",
        "tour_h2": "Todo lo que necesitas, en un lugar tranquilo.",
        "tour_p": "Desde el primer recordatorio hasta la visita al médico, Sanor simplifica tu rutina.",
        "r1_h": "Recordatorios que respondes con un toque",
        "r1_p": "Marca la toma como Tomado, pospónla u omítela directamente desde la notificación. ¿Se te olvida? Sanor te lo recuerda de nuevo y tú eliges con qué frecuencia.",
        "r1_t": ["Tomado, Posponer y Omitir en la notificación", "Recordatorios repetidos hasta que marques la toma", "Oculta los nombres de los medicamentos en la pantalla de bloqueo", "Desactiva los recordatorios de un solo medicamento"],
        "r2_h": "Sabe cuándo comprar el siguiente envase",
        "r2_p": "Indica cuántas pastillas trae el envase. Sanor te muestra para cuántos días te alcanzan, cuántas necesitas para terminar el tratamiento y te avisa antes de que se acaben.",
        "r2_t": ["Días restantes y fecha hasta la que llegan", "Un aviso antes de que se acabe el envase", "Un toque en «He comprado un envase» para actualizarlo"],
        "r3_h": "Descubre cómo se relacionan tomas, síntomas y ánimo",
        "r3_p": "Tomas, síntomas y estado de ánimo juntos, día a día, durante una semana, un mes o tres meses, para que los patrones se vean fácilmente.",
        "r3_t": ["Vistas de semana, mes y 3 meses", "Registra síntomas con intensidad y notas", "Seguimiento del ciclo opcional con predicciones"],
        "r4_h": "Lleva un informe a tu próxima cita",
        "r4_p": "Exporta un PDF de la última semana, el último mes, todo el historial o cualquier rango: tomas omitidas, síntomas, estado de ánimo y promedios de Salud de Apple.",
        "r4_t": ["Comparte el PDF con tu médico con un toque", "Añade tus tomas diarias al Calendario del iPhone", "Rachas y constancia de un vistazo"],
        "more_eyebrow": "Y más",
        "more_h2": "Pequeños detalles, mucha tranquilidad.",
        "more_p": "Sanor se centra en los detalles que hacen más fácil mantener la rutina diaria.",
        "new": "Novedad en 1.7",
        "b1_h": "Comprobación de interacciones más inteligente",
        "b1_p": "Sanor ahora detecta dos medicamentos del mismo tipo (por ejemplo, dos estatinas o dos analgésicos del mismo grupo), combinaciones de riesgo por mecanismo y medicamentos que conviene tomar a horas distintas. Si un medicamento no se pudo comprobar, la app lo dice en lugar de callarse.",
        "b2_h": "Notas sobre comida y alcohol",
        "b2_p": "Notas breves sobre pomelo, lácteos, vitamina K y alcohol directamente en la ficha de cada medicamento.",
        "b3_h": "Una base de medicamentos que habla tu idioma",
        "b3_p": "Encuentra tu medicamento por el nombre de la caja: miles de nombres comerciales locales de los registros de Chequia, Eslovaquia, Ucrania, Rusia y España.",
        "b4_h": "Salud de Apple, si quieres",
        "b4_p": "Con tu permiso, Sanor muestra pasos, frecuencia cardíaca y actividad junto a tu registro de medicación. Tú decides en los ajustes de iOS.",
        "b5_h": "Corrige un toque equivocado",
        "b5_p": "¿Marcaste la toma equivocada? Deshazlo al instante, o cambia una toma entre Tomada y Omitida con un toque.",
        "rw_eyebrow": "Logros",
        "rw_h2": "Conoce a las nutrias que te animan.",
        "rw_p": "Completa tus tomas, mantén el ritmo y cuídate para desbloquear 24 logros de nutria por hitos, rutina diaria y cuidado de tu salud.",
        "news_eyebrow": "Novedades",
        "news_h2": "Sanor sigue mejorando.",
        "news_p": "Actualizaciones periódicas, pensadas según lo que la gente realmente necesita.",
        "ver17": "Versión 1.7",
        "news17_h": "Comprobación de interacciones más inteligente y honesta",
        "news17": ["Detecta dos medicamentos del mismo tipo, combinaciones de riesgo por mecanismo y medicamentos que conviene tomar a horas distintas.", "Notas breves sobre alcohol y comida (pomelo, lácteos, vitamina K) en la ficha del medicamento.", "Estado honesto: si un medicamento no se pudo comprobar, la app lo dice en lugar de no mostrar nada."],
        "old": [
            ("1.6", "Más de 110 medicamentos nuevos y miles de nombres comerciales locales de los registros de Chequia, Eslovaquia, Ucrania, Rusia y España. Nuevos avisos sobre combinaciones de riesgo."),
            ("1.5", "Corrige una marca equivocada con Deshacer, o cambia entre Tomada y Omitida con un toque."),
            ("1.4", "Ya en español: la app y la base de datos de medicamentos hablan español, con sus nombres comerciales."),
        ],
        "pl_eyebrow": "Dónde conseguirla",
        "pl_h2": "En tu teléfono y en tu idioma.",
        "pl_p": "Sanor habla siete idiomas, para que tu rutina resulte natural estés donde estés.",
        "pl_ios": "iPhone", "pl_ios_s": "Disponible ya", "pl_ios_p": "Gratis en App Store. Requiere iOS 17 o posterior. Inicia sesión con Apple o con correo.",
        "pl_and": "Android", "pl_and_s": "En desarrollo", "pl_and_p": "La versión para Android está en camino. Esta página enlazará a Google Play en cuanto esté lista.",
        "pl_soon": "Próximamente",
        "langs": ["English", "Čeština", "Slovenčina", "Deutsch", "Русский", "Українська", "Español"],
        "pv_h2": "Tus datos de salud son tuyos.",
        "pv_p": "Sanor está diseñada para recopilar lo mínimo. Sin anuncios, sin analíticas, sin venta de datos.",
        "pv": [("phone", "En tu iPhone", "Medicamentos, tomas, síntomas, estado de ánimo y entradas del ciclo se guardan en tu dispositivo."), ("lock", "Un perfil pequeño en línea", "Solo se guarda tu inicio de sesión y un perfil pequeño, para que puedas volver a entrar en un teléfono nuevo."), ("shield", "Tú tienes el control", "Exporta o comparte datos solo si quieres, y elimina tu cuenta cuando quieras desde la app.")],
        "pv_more": "Lee la Política de privacidad (EN)",
        "faq_eyebrow": "Preguntas",
        "faq_h2": "Respuestas rápidas.",
        "faq": [
            ("¿Sanor es realmente gratis?", "<p>Sí. Sanor se descarga gratis en App Store. Requiere iOS 17 o posterior e inicias sesión con Apple o con correo.</p>"),
            ("¿Sanor es una app médica?", "<p>No. Sanor no sustituye a un médico, a un farmacéutico ni a un consejo médico. Te ayuda a organizar tu horario y a ser constante. Si Sanor muestra una posible interacción, consúltalo con tu médico o farmacéutico. Que no aparezca un aviso no significa que una combinación sea segura.</p>"),
            ("¿Dónde se guardan mis datos de salud?", "<p>Tus medicamentos, tomas, síntomas, notas de ánimo y entradas del ciclo se guardan en tu iPhone. Tu cuenta y un perfil pequeño se guardan en Google Firebase para que puedas volver a entrar en un teléfono nuevo. No vendemos datos, no mostramos anuncios y no te rastreamos.</p>"),
            ("¿Funcionan los recordatorios sin conexión?", "<p>Sí. Los recordatorios se programan en tu teléfono, así que funcionan sin conexión a internet.</p>"),
            ("¿Hay versión para Android?", "<p>Está en desarrollo. Cuando esté lista, esta página enlazará a Google Play.</p>"),
        ],
        "faq_more": "Más respuestas en el Centro de ayuda (EN) →",
        "cta_h2": "Empieza hoy una rutina más saludable.",
        "cta_p": "Descarga gratuita. Requiere iOS 17 o posterior. Inicia sesión con Apple o con correo.",
        "foot_p": "Un compañero inteligente para tus medicamentos y una vida más sana y constante.",
        "foot_product": "Producto", "foot_legal": "Legal", "foot_support": "Ayuda",
        "foot_tour": "Recorrido", "foot_download": "Descargar",
        "foot_privacy": "Política de privacidad (EN)", "foot_terms": "Condiciones de uso (EN)", "foot_delete": "Eliminar cuenta (EN)",
        "foot_help": "Centro de ayuda (EN)", "foot_faq": "Preguntas frecuentes (EN)", "foot_contact": "Contacto", "foot_how": "Cómo usar la app (EN)",
        "foot_credit": "Nombres de medicamentos checos: datos abiertos de SÚKL · españoles: AEMPS CIMA.",
        "foot_disc": "Sanor no es un producto sanitario y no sustituye el consejo médico profesional.",
        "alt_home": "Pantalla de inicio de Sanor con los medicamentos de hoy, una racha de 21 días y la nutria",
        "alt_reminders": "Ajustes de recordatorios: recordar de nuevo, posponer y ocultar nombres",
        "alt_supply": "Pantalla de existencias con unos 5 días restantes",
        "alt_timeline": "Cronología de tomas, síntomas y ánimo de la semana",
        "alt_reports": "Pantalla de informes con exportación a PDF de semana, mes, todo el historial o rango personalizado",
        "alt_rewards": "Pantalla de logros con 16 de 24 logros de nutria desbloqueados",
        "alt_otter": "La nutria, mascota de Sanor",
    },
}


TEXT["de"] = DE
apply_cycle(TEXT)  # version 1.7: cycle tracking section, 1.7 card, FAQ, hero pill


def cycle_card(t):
    """Illustration of the cycle ring (drawn in SVG/CSS, sample values), not a screenshot."""
    import math
    C, R, day_len = 2 * math.pi * 92, 92, 2 * math.pi * 92 / 28

    def pt(day):  # centre of a given cycle day on the ring
        a = (day - 0.5) / 28 * 2 * math.pi - math.pi / 2
        return 120 + R * math.cos(a), 120 + R * math.sin(a)

    tx, ty = pt(12)
    ox, oy = pt(14)
    arc = lambda start, n, color: (
        f'<circle cx="120" cy="120" r="{R}" fill="none" stroke="{color}" stroke-width="20" '
        f'stroke-dasharray="{n * day_len:.1f} {C:.1f}" stroke-dashoffset="{-start * day_len:.1f}" '
        f'transform="rotate(-90 120 120)"/>')
    svg = (f'<svg viewBox="0 0 240 240" aria-hidden="true">'
           f'<circle cx="120" cy="120" r="{R}" fill="none" stroke="#e3ebff" stroke-width="20"/>'
           + arc(0, 5, "#ff7b5c") + arc(9, 6, "#2fc88c")
           + f'<circle cx="{ox:.1f}" cy="{oy:.1f}" r="9" fill="#8b6cf6" stroke="#fff" stroke-width="3"/>'
           + f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="11" fill="#fff" stroke="#2f5bdb" stroke-width="4"/></svg>')
    leg = t["cy_legend"]
    legend = "".join(f'<li><i class="{c}"></i>{x}</li>' for c, x in zip(("lp", "lf", "lg", "lo"), leg))
    return f'''<div class="cy-visual">
          <div class="cy-card" aria-hidden="true">
            <div class="cy-head"><span class="tagico bg-coral">{ico("drop")}</span><b>{t["cy_card"]}</b></div>
            <div class="cy-ring">{svg}<div class="cy-center"><b>{t["cy_day"]}</b><span>{t["cy_phase"]}</span></div></div>
            <p class="cy-line">{t["cy_line"]}</p>
            <div class="cy-next"><span>{t["cy_next"]}</span><b>{t["cy_next_in"]}</b></div>
            <ul class="cy-legend">{legend}</ul>
            <div class="cy-actions"><span class="cy-chip">{t["cy_chips"][0]}</span><span class="cy-chip">{t["cy_chips"][1]}</span><span class="cy-btn">{t["cy_log"]}</span></div>
          </div>
          <img class="cy-otter" src="/assets/otters/otter_mood_diary.webp" alt="" width="400" height="400" loading="lazy" decoding="async">
        </div>'''


def phone(name, alt, width=620, height=1348, eager=False):
    loading = "" if eager else ' loading="lazy"'
    fetch = ' fetchpriority="high"' if eager else ""
    return (f'<div class="phone"><img src="/assets/shots/{name}.webp" alt="{alt}" '
            f'width="{width}" height="{height}"{loading}{fetch} decoding="async"></div>')


def row(n, icon, color, shot, alt, t, flip=False):
    ticks = "".join(f"<li>{ico('check')}<span>{x}</span></li>" for x in t[f"r{n}_t"])
    return f'''
      <div class="row{" flip" if flip else ""} reveal">
        <div class="row-media">{phone(shot, alt)}</div>
        <div class="row-text">
          <div class="tagico {color}">{ico(icon)}</div>
          <h3>{t[f"r{n}_h"]}</h3>
          <p>{t[f"r{n}_p"]}</p>
          <ul class="ticks">{ticks}</ul>
        </div>
      </div>'''


def card(span, icon, color, h, p, new=None):
    cls = "card card-new" if new else "card"
    badge = f'<span class="badge-new">{new}</span>' if new else ""
    return f'''
        <div class="{cls} {span} reveal">{badge}
          <div class="tagico {color}">{ico(icon)}</div>
          <h3>{h}</h3>
          <p>{p}</p>
        </div>'''


def render(lang):
    t = TEXT[lang]
    idx = {"en": 0, "cs": 1, "es": 2}.get(lang)
    path = dict((l, p) for l, _, p in LANGS)[lang]
    url = SITE + path

    # language switcher
    sw = "".join(
        f'<a href="{p}" hreflang="{l}" lang="{l}"' + (' aria-current="true"' if l == lang else "") + f">{lbl}</a>"
        for l, lbl, p in LANGS
    )
    alternates = "\n  ".join(
        f'<link rel="alternate" hreflang="{l}" href="{SITE}{p}" />' for l, _, p in LANGS
    ) + f'\n  <link rel="alternate" hreflang="x-default" href="{SITE}/" />'

    chips = "".join(f"<li>{ico('check')}{c}</li>" for c in t["chips"])
    stats = "".join(f'<div class="stat"><b>{a}</b><span>{b}</span></div>' for a, b in t["stats"])
    awards = "".join(
        f'<div class="card award reveal"><img src="/assets/otters/otter_{a[0]}.webp" alt="" width="400" height="400" loading="lazy" decoding="async"><h3>{AWARD_DE[a[0]] if lang == "de" else a[1 + idx]}</h3></div>'
        for a in AWARDS
    )
    news_ticks = "".join(f"<li>{ico('check')}<span>{x}</span></li>" for x in t["news17"])
    olds = "".join(f'<div class="old reveal"><b>{v}</b><p>{p}</p></div>' for v, p in t["old"])
    langs = "".join(f"<li>{x}</li>" for x in t["langs"])
    pv = "".join(
        f'<div>{ico(i)}<b>{h}</b><span>{p}</span></div>' for i, h, p in t["pv"]
    )
    faq = "".join(
        f'''<div class="faq-item{" open" if i == 0 else ""}"><button class="faq-q" type="button">{q}{ico("chev")}</button><div class="faq-a">{a}</div></div>'''
        for i, (q, a) in enumerate(t["faq"])
    )

    ld = {
        "@context": "https://schema.org",
        "@type": "MobileApplication",
        "name": "Sanor",
        "description": t["desc"],
        "applicationCategory": "HealthApplication",
        "operatingSystem": "iOS 17+",
        "inLanguage": ["en", "cs", "sk", "de", "ru", "uk", "es"],
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "downloadUrl": APPSTORE,
        "url": url,
        "image": SITE + "/icon.jpeg",
        "author": {"@type": "Person", "name": "Platon Fedotov"},
    }

    return f'''<!DOCTYPE html>
<html lang="{t["html_lang"]}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{t["title"]}</title>
  <meta name="description" content="{t["desc"]}" />
  <meta name="theme-color" content="#e7f0ff" />
  <link rel="icon" href="/icon.jpeg" />
  <link rel="apple-touch-icon" href="/icon.jpeg" />
  <link rel="canonical" href="{url}" />
  {alternates}
  <meta name="apple-itunes-app" content="app-id=6766075127" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Sanor" />
  <meta property="og:title" content="{t["og_title"]}" />
  <meta property="og:description" content="{t["desc"]}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{SITE}/icon.jpeg" />
  <meta name="twitter:card" content="summary" />
  <link rel="preload" as="image" href="/assets/shots/home.webp" type="image/webp" />
  <link rel="stylesheet" href="/assets/site.css" />
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<a class="sr-only" href="#main">{t["skip"]}</a>

<header class="nav">
  <div class="wrap nav-in">
    <a class="brand" href="{path}" aria-label="Sanor"><img src="/icon.jpeg" alt="" width="38" height="38" />Sanor</a>
    <ul class="nav-links">
      <li><a href="#tour">{t["nav_tour"]}</a></li>
      <li><a href="#features">{t["nav_features"]}</a></li>
      <li><a href="#rewards">{t["nav_rewards"]}</a></li>
      <li><a href="#faq">{t["nav_faq"]}</a></li>
      <li><a href="/support.html">{t["nav_support"]}</a></li>
    </ul>
    <nav class="lang" aria-label="Language">{sw}</nav>
    <a class="btn btn-primary btn-sm" href="{APPSTORE}">{t["nav_cta"]}</a>
  </div>
</header>

<main id="main">

  <!-- HERO -->
  <section class="hero">
    <div class="wrap hero-grid">
      <div>
        <a class="pill" href="#cycle"><i></i><span>{t["pill"]}</span>{ico("arrow")}</a>
        <h1>{t["h1"]}</h1>
        <p class="hero-sub">{t["sub"]}</p>
        <div class="hero-cta">
          <a class="btn btn-primary" href="{APPSTORE}">{ico("down")}{t["btn_store"]}</a>
          <a class="btn btn-ghost" href="#tour">{t["btn_how"]}</a>
        </div>
        <ul class="chips">{chips}</ul>
      </div>
      <div class="hero-visual">
        {phone("home", t["alt_home"], eager=True)}
        <img class="hero-otter" src="/assets/otters/otter_hello.webp" alt="{t["alt_otter"]}" width="400" height="400" />
        <div class="float float-a"><div class="dot dot-orange">{ico("flame")}</div><div><b>{t["float_streak"][0]}</b><span>{t["float_streak"][1]}</span></div></div>
        <div class="float float-b"><div class="dot dot-green">{ico("check")}</div><div><b>{t["float_taken"][0]}</b><span>{t["float_taken"][1]}</span></div></div>
        <div class="float float-c"><div class="dot dot-blue">{ico("box")}</div><div><b>{t["float_supply"][0]}</b><span>{t["float_supply"][1]}</span></div></div>
      </div>
    </div>
  </section>

  <div class="strip wrap"><div class="strip-card reveal">{stats}</div></div>

  <!-- TOUR -->
  <section class="section" id="tour">
    <div class="wrap">
      <div class="head reveal">
        <span class="eyebrow">{t["tour_eyebrow"]}</span>
        <h2>{t["tour_h2"]}</h2>
        <p>{t["tour_p"]}</p>
      </div>
      {row(1, "bell", "bg-amber", "reminders", t["alt_reminders"], t)}
      {row(2, "box", "bg-blue", "supply", t["alt_supply"], t, flip=True)}
      {row(3, "activity", "bg-coral", "timeline", t["alt_timeline"], t)}
      {row(4, "file", "bg-purple", "reports", t["alt_reports"], t, flip=True)}
    </div>
  </section>

  <!-- CYCLE (new in 1.7) -->
  <section class="section section-warm" id="cycle">
    <div class="wrap">
      <div class="row flip reveal">
        <div class="row-media">{cycle_card(t)}</div>
        <div class="row-text">
          <span class="eyebrow eyebrow-coral">{t["cy_eyebrow"]}</span>
          <h3>{t["cy_h2"]}</h3>
          <p>{t["cy_p"]}</p>
          <ul class="ticks">{"".join(f"<li>{ico('check')}<span>{x}</span></li>" for x in t["cy_t"])}</ul>
          <p class="cy-note">{t["cy_note"]}</p>
        </div>
      </div>
    </div>
  </section>

  <!-- FEATURES -->
  <section class="section section-tint" id="features">
    <div class="wrap">
      <div class="head reveal">
        <span class="eyebrow">{t["more_eyebrow"]}</span>
        <h2>{t["more_h2"]}</h2>
        <p>{t["more_p"]}</p>
      </div>
      <div class="bento">
        {card("span-4", "alert", "bg-blue", t["b1_h"], t["b1_p"], new=t["new"])}
        {card("span-2", "heart", "bg-coral", t["b2_h"], t["b2_p"])}
        {card("span-2", "search", "bg-blue", t["b3_h"], t["b3_p"])}
        {card("span-2", "activity", "bg-green", t["b4_h"], t["b4_p"])}
        {card("span-2", "undo", "bg-purple", t["b5_h"], t["b5_p"])}
      </div>
    </div>
  </section>

  <!-- REWARDS -->
  <section class="section" id="rewards">
    <div class="wrap">
      <div class="head reveal">
        <span class="eyebrow">{t["rw_eyebrow"]}</span>
        <h2>{t["rw_h2"]}</h2>
        <p>{t["rw_p"]}</p>
      </div>
      <div class="rewards-grid">{awards}</div>
    </div>
  </section>

  <!-- WHAT'S NEW -->
  <section class="section section-tint" id="news">
    <div class="wrap">
      <div class="head reveal">
        <span class="eyebrow">{t["news_eyebrow"]}</span>
        <h2>{t["news_h2"]}</h2>
        <p>{t["news_p"]}</p>
      </div>
      <div class="news">
        <div class="news-main reveal">
          <span class="ver">{ico("flame")}{t["ver17"]}</span>
          <h3>{t["news17_h"]}</h3>
          <ul class="ticks">{news_ticks}</ul>
        </div>
        <div class="old-list">{olds}</div>
      </div>
    </div>
  </section>

  <!-- PLATFORMS -->
  <section class="section" id="download-info">
    <div class="wrap">
      <div class="head reveal">
        <span class="eyebrow">{t["pl_eyebrow"]}</span>
        <h2>{t["pl_h2"]}</h2>
        <p>{t["pl_p"]}</p>
      </div>
      <div class="plat">
        <div class="card reveal">
          <span class="status live">{t["pl_ios_s"]}</span>
          <h3>{t["pl_ios"]}</h3>
          <p>{t["pl_ios_p"]}</p>
          <a class="btn btn-primary btn-sm" href="{APPSTORE}">{ico("down")}{t["btn_store"]}</a>
        </div>
        <div class="card reveal">
          <span class="status soon">{t["pl_and_s"]}</span>
          <h3>{t["pl_and"]}</h3>
          <p>{t["pl_and_p"]}</p>
          <span class="btn btn-ghost btn-sm" aria-disabled="true" style="pointer-events:none;opacity:.7">{t["pl_soon"]}</span>
        </div>
      </div>
      <ul class="langs reveal">{langs}</ul>
    </div>
  </section>

  <!-- PRIVACY -->
  <section class="section" style="padding-top:0">
    <div class="wrap">
      <div class="privacy-band reveal">
        <h2>{t["pv_h2"]}</h2>
        <p>{t["pv_p"]}</p>
        <div class="p3">{pv}</div>
        <a class="more" href="/privacy.html">{t["pv_more"]} →</a>
      </div>
    </div>
  </section>

  <!-- FAQ -->
  <section class="section section-tint" id="faq">
    <div class="wrap">
      <div class="head reveal">
        <span class="eyebrow">{t["faq_eyebrow"]}</span>
        <h2>{t["faq_h2"]}</h2>
      </div>
      <div class="faq reveal">{faq}</div>
      <p class="faq-more"><a href="/support.html#faq">{t["faq_more"]}</a></p>
    </div>
  </section>

  <!-- CTA -->
  <section class="cta" id="download" style="padding-top:100px">
    <div class="wrap">
      <div class="cta-card reveal">
        <div>
          <h2>{t["cta_h2"]}</h2>
          <p>{t["cta_p"]}</p>
          <a class="btn btn-light" href="{APPSTORE}">{ico("down")}{t["btn_store"]}</a>
        </div>
        <img src="/assets/otters/otter_weekend_hero.webp" alt="{t["alt_otter"]}" width="400" height="400" loading="lazy" />
      </div>
    </div>
  </section>

</main>

<footer class="footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="brand" href="{path}"><img src="/icon.jpeg" alt="" width="38" height="38" />Sanor</a>
        <p>{t["foot_p"]}</p>
      </div>
      <div>
        <h4>{t["foot_product"]}</h4>
        <ul>
          <li><a href="#features">{t["nav_features"]}</a></li>
          <li><a href="#tour">{t["foot_tour"]}</a></li>
          <li><a href="#download">{t["foot_download"]}</a></li>
        </ul>
      </div>
      <div>
        <h4>{t["foot_legal"]}</h4>
        <ul>
          <li><a href="/privacy.html">{t["foot_privacy"]}</a></li>
          <li><a href="/terms.html">{t["foot_terms"]}</a></li>
          <li><a href="/delete-account.html">{t["foot_delete"]}</a></li>
        </ul>
      </div>
      <div>
        <h4>{t["foot_support"]}</h4>
        <ul>
          <li><a href="/support.html">{t["foot_help"]}</a></li>
          <li><a href="/support.html#faq">{t["foot_faq"]}</a></li>
          <li><a href="/support.html#how-to">{t["foot_how"]}</a></li>
          <li><a href="mailto:{EMAIL}">{t["foot_contact"]}</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom">
      <p>© 2026 Platon Fedotov · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p>{t["foot_credit"]}</p>
      <p>{t["foot_disc"]}</p>
    </div>
  </div>
</footer>

<script src="/assets/site.js" defer></script>
</body>
</html>
'''


if __name__ == "__main__":
    for lang, _, path in LANGS:
        out_dir = os.path.join(ROOT, path.strip("/"))
        os.makedirs(out_dir, exist_ok=True)
        out = os.path.join(out_dir, "index.html")
        with open(out, "w", encoding="utf-8") as f:
            f.write(render(lang))
        print("wrote", os.path.relpath(out, ROOT))
