"""Спрощений локальний аналіз NMVP2 для Streamlit (Home, Demo Cases) без виклику API."""
from __future__ import annotations

import re
from typing import Any


def analyze_text_locally(text: str) -> dict[str, Any]:
    """Ті самі евристики, що на Home.py — для fallback коли API недоступний."""
    ml_score = 0.15
    if re.search(r"ТЕРМІНОВО|НЕГАЙНО|ШОК|УВАГА", text, re.IGNORECASE):
        ml_score = 0.75

    roberta_score = 0.20
    if re.search(r"ЗСУ|АРМІЯ|ВІЙСЬКОВІ|ОБОРОНА", text, re.IGNORECASE):
        roberta_score = 0.60

    ipso_techniques: list[str] = []
    if re.search(r"ТЕРМІНОВО|ЗАРАЗ|НЕГАЙНО|СТРИКНО", text, re.IGNORECASE):
        ipso_techniques.append("urgency_injection")
    if re.search(r"[А-Я]{3,}", text):
        ipso_techniques.append("caps_abuse")
    if re.search(r"ПОШИРТЕ|РЕПОСТ|ПОДІЛІТЬСЯ|ПЕРЕСЛАТИ", text, re.IGNORECASE):
        ipso_techniques.append("viral_call")
    if re.search(r"ВИДАЛЕННЯ|УСПІЙ|ЗАПИШИ|ЗБЕРЕГИ", text, re.IGNORECASE):
        ipso_techniques.append("deletion_threat")
    if re.search(r"ЗАМОВЧУЮТЬ|ХОВАЮТЬ|ПРАВДА|НА СПРАВДІ", text, re.IGNORECASE):
        ipso_techniques.append("conspiracy_framing")
    if re.search(
        r"ДЖЕРЕЛ[АОИ]|ЕКСПЕРТ[И]|ІНФОРМУЮТЬ|КАЖУТЬ|ПОВІДОМЛЯ[ЄЮ]ТЬСЯ|ЧУТКИ",
        text,
        re.IGNORECASE,
    ):
        ipso_techniques.append("anonymous_sources")

    ipso_penalty = min(len(ipso_techniques) / 4.0, 1.0)
    final_score = (0.3 * ml_score) + (0.4 * roberta_score) + (0.3 * ipso_penalty)
    final_score = min(max(final_score, 0.0), 1.0)

    if final_score >= 0.65:
        verdict = "FAKE"
        explanation_uk = (
            "Текст класифіковано як ФЕЙК. Виявлено високий рівень маніпулятивних технік та ознак ІПСО."
        )
    elif final_score >= 0.35:
        verdict = "SUSPICIOUS"
        explanation_uk = "Текст ПІДОЗРІЛИЙ. Присутні окремі маркери маніпуляції, що потребують уваги."
    else:
        verdict = "REAL"
        explanation_uk = "Текст виглядає ДОСТОВІРНИМ. Явних ознак маніпулятивного впливу не виявлено."

    credibility_score = round((1.0 - final_score) * 100, 1)

    return {
        "article_id": 0,
        "verdict": verdict,
        "credibility_score": credibility_score,
        "fake_score": round(final_score, 3),
        "confidence": round(0.85, 1),
        "ipso_techniques": ipso_techniques,
        "source_credibility": 50.0,
        "explanation_uk": explanation_uk,
        "source_domain": "direct_input",
        "language": "uk",
        "processing_time_ms": 12.5,
        "formula_breakdown": {
            "ml_score": ml_score,
            "ml_contribution": round(0.3 * ml_score, 3),
            "roberta_score": roberta_score,
            "roberta_contribution": round(0.4 * roberta_score, 3),
            "ipso_penalty": ipso_penalty,
            "ipso_contribution": round(0.3 * ipso_penalty, 3),
        },
    }
