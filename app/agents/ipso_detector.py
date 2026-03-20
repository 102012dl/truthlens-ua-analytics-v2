import re
from typing import List

__all__ = ["IPSODetector"]


class IPSODetector:
    """
    Detector of Information-Psychological Special Operations (ІПСО).
    10 techniques from UNLP 2025 research on Ukrainian Telegram.
    """

    TECHNIQUES = {
        "urgency_injection": r'ТЕРМІНОВО|ЗАРАЗ|BREAKING|УВАГА|НЕГАЙНО',
        "caps_abuse": None,  # special: >30% caps check
        "deletion_threat": r'до видалення|встигніть|видалять|успіть',
        "viral_call": r'поширте|пересилайте|діліться|поширюйте',
        "conspiracy_framing": r'приховують|замовчують|вони знають|правда яку',
        "anonymous_sources": r'анонімн\w+ джерел|за даними тг|джерела кажуть|експерт[и]?\s+(попереджають|стверджують|кажуть)|без посилань|стало відомо',
        "military_disinfo": r'ЗСУ здал|армія відступ|фронт прорв|позиції залиш',
        "awakening_appeal": r'прокиньтесь|відкрийте очі|вас обманюють|брешуть',
        "authority_impersonation": r'Зеленськ\w+ заявив|МОЗ повідомив|ОП підтвердив',
        "deepfake_indicator": r'фейкове відео|синтезован\w+|AI-відео|дипфейк',
    }

    OVERRIDE_THRESHOLD = 2  # ipso_count >= 2 → FAKE override

    def detect(self, text: str) -> List[str]:
        """Detect ІПСО techniques in text. Returns list of technique names."""
        detected = []

        for name, pattern in self.TECHNIQUES.items():
            if name == "caps_abuse":
                # Special case: check for excessive capital letters
                upper = sum(1 for c in text if c.isupper())
                letters = sum(1 for c in text if c.isalpha())
                if letters > 10 and upper / letters > 0.30:
                    detected.append(name)
            elif pattern and re.search(pattern, text, re.IGNORECASE):
                detected.append(name)

        return detected

    def get_override(self, techniques: List[str]) -> bool:
        """Return True if ipso count >= threshold (FAKE override rule)."""
        return len(techniques) >= self.OVERRIDE_THRESHOLD
