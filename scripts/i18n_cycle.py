"""Version 1.7 texts: the new cycle tracking section, plus updates to the pill, the 1.7 card and the FAQ.
Screen labels (Cycle, Day, Fertile window, Next period, legend, Log your day, ...) and the disclaimer
are taken verbatim from the app's own strings (l10n/strings_cycle.json). German uses the formal "Sie".
Applied on top of the base TEXT dictionaries by build_home.py."""

CYCLE = {
    "en": {
        "pill": "New in 1.7 · Cycle tracking & smarter interaction checks",
        "cy_eyebrow": "New in 1.7",
        "cy_h2": "Cycle tracking, built around you.",
        "cy_p": "A calm, private way to follow your cycle right next to your medication. Available to everyone: just turn it on in Settings.",
        "cy_t": ["A ring with your cycle day and what comes next", "A calendar with period, fertile window and ovulation forecasts", "A quick log for flow, symptoms, mood and pain", "Insights on how your cycle varies and which symptoms repeat", "Forecasts that learn from what you log"],
        "cy_note": "Forecasts are estimates based on what you log. They are not a method of contraception and not a medical diagnosis.",
        "cy_card": "Cycle", "cy_day": "Day 12", "cy_phase": "Fertile window", "cy_line": "Ovulation in 2 days",
        "cy_next": "Next period", "cy_next_in": "in 16 days",
        "cy_legend": ["Period", "Forecast", "Fertile", "Ovulation"],
        "cy_log": "Log your day", "cy_chips": ["Mood", "Pain"],
        "news17_h": "Cycle tracking and smarter interaction checks",
        "cy_news": "New cycle tracking: a ring with your cycle day and what is next, a calendar with forecasts, a quick log for flow, symptoms, mood and pain, and insights on how your cycle varies. Forecasts learn from what you log. Available to everyone, turn it on in Settings.",
        "cy_faq": ("Is cycle tracking available to everyone?", "<p>Yes. Cycle tracking is available to everyone: turn it on in Settings and it appears in the Health tab. Your cycle entries are stored on your iPhone, like the rest of your health records.</p><p>Forecasts are estimates based on what you log. They are not a method of contraception and not a medical diagnosis.</p>"),
    },
    "cs": {
        "pill": "Novinka v 1.7 · Sledování cyklu a chytřejší interakce",
        "cy_eyebrow": "Novinka v 1.7",
        "cy_h2": "Sledování cyklu na míru.",
        "cy_p": "Klidný a soukromý způsob, jak sledovat cyklus hned vedle svých léků. Pro všechny: stačí zapnout v Nastavení.",
        "cy_t": ["Kruh s dnem cyklu a tím, co přijde", "Kalendář s předpovědí menstruace, plodného období a ovulace", "Rychlý záznam menstruace, příznaků, nálady a bolesti", "Přehled, jak se váš cyklus mění a které příznaky se opakují", "Předpovědi, které se učí z vašich záznamů"],
        "cy_note": "Předpovědi jsou odhady podle vašich záznamů. Nejsou antikoncepcí ani lékařskou diagnózou.",
        "cy_card": "Cyklus", "cy_day": "Den 12", "cy_phase": "Plodné období", "cy_line": "Ovulace za 2 dny",
        "cy_next": "Další menstruace", "cy_next_in": "za 16 dní",
        "cy_legend": ["Menstruace", "Předpověď", "Plodné dny", "Ovulace"],
        "cy_log": "Zapsat den", "cy_chips": ["Nálada", "Bolest"],
        "news17_h": "Sledování cyklu a chytřejší kontrola interakcí",
        "cy_news": "Nové sledování cyklu: kruh s dnem cyklu a tím, co přijde, kalendář s předpověďmi, rychlý záznam menstruace, příznaků, nálady a bolesti a přehled, jak se váš cyklus mění. Předpovědi se učí z vašich záznamů. Pro všechny, zapnete v Nastavení.",
        "cy_faq": ("Je sledování cyklu pro všechny?", "<p>Ano. Sledování cyklu je pro všechny: zapnete ho v Nastavení a objeví se na záložce Zdraví. Záznamy cyklu jsou uložené ve vašem iPhonu stejně jako ostatní zdravotní záznamy.</p><p>Předpovědi jsou odhady podle vašich záznamů. Nejsou antikoncepcí ani lékařskou diagnózou.</p>"),
    },
    "es": {
        "pill": "Novedad en 1.7 · Seguimiento del ciclo e interacciones más inteligentes",
        "cy_eyebrow": "Novedad en 1.7",
        "cy_h2": "Seguimiento del ciclo, a tu medida.",
        "cy_p": "Una forma tranquila y privada de seguir tu ciclo junto a tus medicamentos. Para todos: solo tienes que activarlo en Ajustes.",
        "cy_t": ["Un anillo con el día de tu ciclo y lo que viene", "Un calendario con previsiones de regla, ventana fértil y ovulación", "Registro rápido de regla, síntomas, ánimo y dolor", "Un análisis de cómo varía tu ciclo y qué síntomas se repiten", "Previsiones que aprenden de lo que anotas"],
        "cy_note": "Las previsiones son estimaciones según lo que registras. No son un método anticonceptivo ni un diagnóstico médico.",
        "cy_card": "Ciclo", "cy_day": "Día 12", "cy_phase": "Ventana fértil", "cy_line": "Ovulación en 2 días",
        "cy_next": "Próxima regla", "cy_next_in": "en 16 días",
        "cy_legend": ["Regla", "Previsión", "Fértil", "Ovulación"],
        "cy_log": "Anotar el día", "cy_chips": ["Ánimo", "Dolor"],
        "news17_h": "Seguimiento del ciclo y comprobación de interacciones más inteligente",
        "cy_news": "Nuevo seguimiento del ciclo: un anillo con el día de tu ciclo y lo que viene, un calendario con previsiones, registro rápido de regla, síntomas, ánimo y dolor, y un análisis de cómo varía tu ciclo. Las previsiones aprenden de lo que anotas. Para todos, se activa en Ajustes.",
        "cy_faq": ("¿El seguimiento del ciclo está disponible para todos?", "<p>Sí. El seguimiento del ciclo es para todos: actívalo en Ajustes y aparecerá en la pestaña Salud. Tus registros del ciclo se guardan en tu iPhone, igual que el resto de tus datos de salud.</p><p>Las previsiones son estimaciones según lo que registras. No son un método anticonceptivo ni un diagnóstico médico.</p>"),
    },
    "de": {
        "pill": "Neu in 1.7 · Zyklus-Tracker & Wechselwirkungsprüfung",
        "cy_eyebrow": "Neu in 1.7",
        "cy_h2": "Zyklus-Tracking, ganz auf Sie zugeschnitten.",
        "cy_p": "Eine ruhige, private Art, Ihren Zyklus direkt neben Ihren Medikamenten im Blick zu behalten. Für alle: einfach in den Einstellungen einschalten.",
        "cy_t": ["Ein Ring mit Ihrem Zyklustag und dem, was als Nächstes kommt", "Ein Kalender mit Prognosen für Periode, fruchtbares Fenster und Eisprung", "Schnelles Eintragen von Blutung, Beschwerden, Stimmung und Schmerz", "Eine Auswertung, wie Ihr Zyklus schwankt und welche Beschwerden sich wiederholen", "Prognosen, die aus Ihren Einträgen lernen"],
        "cy_note": "Prognosen sind Schätzungen auf Basis Ihrer Einträge. Sie sind keine Verhütungsmethode und keine medizinische Diagnose.",
        "cy_card": "Zyklus", "cy_day": "Tag 12", "cy_phase": "Fruchtbares Fenster", "cy_line": "Eisprung in 2 Tagen",
        "cy_next": "Nächste Periode", "cy_next_in": "in 16 Tagen",
        "cy_legend": ["Periode", "Prognose", "Fruchtbar", "Eisprung"],
        "cy_log": "Tag eintragen", "cy_chips": ["Stimmung", "Schmerz"],
        "news17_h": "Zyklus-Tracker und intelligentere Wechselwirkungsprüfung",
        "cy_news": "Neuer Zyklus-Tracker: ein Ring mit Ihrem Zyklustag und dem, was als Nächstes kommt, ein Kalender mit Prognosen, schnelles Eintragen von Blutung, Beschwerden, Stimmung und Schmerz sowie eine Auswertung, wie Ihr Zyklus schwankt. Die Prognosen lernen aus Ihren Einträgen. Für alle, in den Einstellungen einschaltbar.",
        "cy_faq": ("Ist der Zyklus-Tracker für alle verfügbar?", "<p>Ja. Der Zyklus-Tracker ist für alle verfügbar: Schalten Sie ihn in den Einstellungen ein, dann erscheint er im Tab Gesundheit. Ihre Zykluseinträge werden auf Ihrem iPhone gespeichert, wie der Rest Ihrer Gesundheitsdaten.</p><p>Prognosen sind Schätzungen auf Basis Ihrer Einträge. Sie sind keine Verhütungsmethode und keine medizinische Diagnose.</p>"),
    },
}


def apply(TEXT):
    """Merge the 1.7 texts into the base dictionaries (in place)."""
    for lang, c in CYCLE.items():
        t = TEXT[lang]
        c = dict(c)
        news = c.pop("cy_news")
        faq = c.pop("cy_faq")
        t.update(c)
        t["news17"] = [news] + list(t["news17"])
        t["faq"] = list(t["faq"])
        t["faq"].insert(3, faq)
