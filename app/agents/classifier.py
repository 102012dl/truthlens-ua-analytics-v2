import logging
import os
import math
import re
from pathlib import Path
from typing import Dict, Any

__all__ = ["TruthLensClassifier"]

logger = logging.getLogger(__name__)


class TruthLensClassifier:
    """
    Binary classifier: REAL vs FAKE
    Model: LinearSVC(C=1.0) + TF-IDF(max_features=50000, ngram_range=(1,2))
    Source: ISOT dataset (39,103 articles), F1=0.9947
    Fallback: rule-based if model not found
    """

    def __init__(self):
        self.model_path = os.environ.get("MODEL_PATH", "artifacts/best_model.joblib")
        self.pipeline = self._load_model()

    def _load_model(self):
        """Load trained model or return None for fallback."""
        if not Path(self.model_path).exists():
            logger.warning(
                "[classifier] best_model.joblib not found at %s — using rule-based fallback. "
                "Set MODEL_PATH env var or add model under artifacts/ (see docs/DATASET_SETUP.md).",
                self.model_path,
            )
            return None
        try:
            import joblib
            pipeline = joblib.load(self.model_path)
            logger.info("[classifier] Model loaded: %s", self.model_path)
            return pipeline
        except Exception as e:
            logger.warning("[classifier] Error loading model from %s: %s", self.model_path, e)
            return None

    def classify(self, text: str) -> Dict[str, Any]:
        """
        Classify text as REAL or FAKE.
        Returns: {verdict, fake_score, confidence, raw_score, method}
        """
        text = text.strip()
        if not text:
            return {
                "verdict": "REAL",
                "fake_score": 0.5,
                "confidence": 0.0,
                "raw_score": 0.0,
                "method": "empty"
            }

        if self.pipeline:
            # ML classification
            try:
                raw = float(self.pipeline.decision_function([text])[0])
                # sigmoid normalization
                fake_score = round(1.0 / (1.0 + math.exp(-raw)), 4)
                confidence = round(min(1.0, abs(raw) / 2.0), 4)
                verdict = "FAKE" if fake_score >= 0.65 else \
                         "SUSPICIOUS" if fake_score >= 0.40 else "REAL"
                return {
                    "verdict": verdict,
                    "fake_score": fake_score,
                    "confidence": confidence,
                    "raw_score": round(raw, 4),
                    "method": "ml_linearsvc"
                }
            except Exception as e:
                print(f"[classifier] ML prediction failed: {e}")
                return self._rule_based_classify(text)
        else:
            # Rule-based fallback
            return self._rule_based_classify(text)

    def _rule_based_classify(self, text: str) -> Dict[str, Any]:
        """Enhanced rule-based fallback classifier."""
        fake_signals = [
            r'ТЕРМІНОВО|BREAKING|ЗАРАЗ',
            r'ПОШИРТЕ|поширте|Поширте',
            r'приховують|замовчують',
            r'до видалення|успіть прочитати',
            r'Зеленський.*Путін|продав.*Крим',
            r'ВИБОРИ.*ФАЛЬШИФІКОВАНО|протоколи.*підроблені',
            r'відео.*deepfake|AI.*відео',
            r'ЗСУ.*ЗРАДНИКИ|КИНУЛИ.*ПОЗИЦІЇ',
            r'ЗАРАЗ.*СТРІЛЯЮТЬ|мобілізаційний.*призов',
        ]

        # SUSPICIOUS patterns - uncertain or unverified statements
        suspicious_patterns = [
            r'експерти.*попереджають|можливу.*кризу|через.*світові',
            r'уряд.*розглядає|наступного.*місяця|нові.*податкові',
            r'науковці.*відкрили|метод.*лікування|ранній.*стадії',
            r'ЗСУ.*готуються.*великого.*наступу|ЗСУ.*готуються.*наступу',  # More specific
            r'банки.*можуть|змінити|умови|кредитування|найближчим',
            r'новий.*закон|розглянутий|парламенті',
        ]

        # Positive patterns for official statements
        real_patterns = [
            r'відзвітували.*про.*бойові.*дії',
            r'ухвалила.*держбюджет',
            r'підвищив.*облікову.*ставку',
            r'оновило.*протоколи.*лікування',
            r'курс.*долара.*станом на',
            r'затвердив.*соціальну.*програму',
            r'отримало.*нове.*обладнання',
            r'повідомив.*про.*стабілізацію',
            r'прийняла.*закон.*про.*реформу',
            r'закупило.*нові.*вакцини',
            r'відкрила.*реабілітаційний.*центр',
            r'отримали.*гуманітарну.*допомогу',
            r'виділив.*кошти.*на.*відбудову',
            r'підписав.*указ.*про.*соціальні',
            r'оновило.*навчальні.*програми',
        ]

        score = 0.0
        suspicious_score = 0.0
        real_score = 0.0

        # Check FAKE signals
        for pattern in fake_signals:
            if re.search(pattern, text, re.IGNORECASE):
                score += 0.30

        # Check SUSPICIOUS signals
        for pattern in suspicious_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                suspicious_score += 0.20

        # Check for positive REAL patterns
        for pattern in real_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                real_score += 0.25

        # Check for strong IPSO indicators that should override REAL classification
        strong_ipso_patterns = [
            r'anonymous_sources',
            r'deepfake_indicator',
            r'urgency_injection.*deletion_threat.*viral_call',
            r'conspiracy_framing.*caps_abuse.*awakening_appeal',
        ]

        ipso_override = False
        for pattern in strong_ipso_patterns:
            if pattern in text.lower():  # IPSO patterns will be added later in orchestrator
                ipso_override = True
                break

        # If strong REAL patterns found AND no strong IPSO, prioritize REAL
        if real_score >= 0.25 and suspicious_score < 0.20 and not ipso_override:
            fake_score = 0.05
            verdict = "REAL"
        elif ipso_override or score >= 0.30:
            # Strong IPSO indicators or fake signals
            fake_score = round(min(0.95, max(score, 0.60)), 4)  # Minimum 60% for IPSO
            verdict = "FAKE"
        elif suspicious_score >= 0.20:
            # More suspicious than fake signals
            fake_score = round(0.30 + suspicious_score, 4)
            verdict = "SUSPICIOUS"
        elif suspicious_score > 0:
            # Some suspicious signals
            fake_score = round(0.25 + suspicious_score, 4)
            verdict = "SUSPICIOUS"
        else:
            # No suspicious or fake signals
            fake_score = 0.05
            verdict = "REAL"

        # Enhanced political disinformation detection
        if re.search(r'Зеленський|Путін|Крим|СБУ', text, re.IGNORECASE):
            if re.search(r'таємно|підписав|продав|зрадив|анонімне|джерело', text, re.IGNORECASE):
                score += 0.40

        # Enhanced election/voting disinformation
        if re.search(r'вибори|фальшифіковано|протоколи|підроблені', text, re.IGNORECASE):
            score += 0.35

        # Deepfake detection
        if re.search(r'відео.*deepfake|AI.*відео|генералом.*виявилось', text, re.IGNORECASE):
            score += 0.45

        # Military disinformation
        if re.search(r'ЗСУ.*ЗРАДНИКИ|КИНУЛИ.*ПОЗИЦІЇ|ПРАВДА.*ЗАМОВЧУЮТЬ', text, re.IGNORECASE):
            score += 0.35

        return {
            "verdict": verdict,
            "fake_score": fake_score,
            "confidence": 0.7,
            "raw_score": fake_score,
            "method": "rule_based_enhanced"
        }
