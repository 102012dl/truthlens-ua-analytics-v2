import time
import math
from typing import Dict, Any

from app.agents.classifier import TruthLensClassifier
from app.agents.ipso_detector import IPSODetector
from app.agents.source_scorer import SourceScorer

__all__ = ["TruthLensOrchestrator"]


class TruthLensOrchestrator:
    """Main analysis pipeline — sequential v1."""

    def __init__(self):
        self.classifier = TruthLensClassifier()
        self.ipso_detector = IPSODetector()
        self.source_scorer = SourceScorer()

    async def process(self, text: str, domain: str = "direct",
                      article_count: int = 0) -> Dict[str, Any]:
        """
        Full analysis pipeline:
        1. ML classification (LinearSVC or rule-based)
        2. ІПСО technique detection
        3. Verdict determination (with ІПСО override)
        4. Credibility score calculation
        5. Ukrainian explanation generation
        Returns complete verdict dict.
        """
        start = time.perf_counter()

        # Step 1: ML classification
        ml = self.classifier.classify(text)
        fake_score = ml["fake_score"]
        confidence = ml["confidence"]

        # Step 2: ІПСО detection
        ipso = self.ipso_detector.detect(text)
        override = self.ipso_detector.get_override(ipso)

        # Step 3: Verdict (ІПСО override takes priority)
        if override:
            verdict = "FAKE"
            fake_score = max(fake_score, 0.70)  # Ensure high fake_score for IPSO
        elif fake_score >= 0.55:  # Raised from 0.45 to avoid false positives
            verdict = "FAKE"
        elif fake_score >= 0.30:  # Raised from 0.25 to match SUSPICIOUS better
            verdict = "SUSPICIOUS"
        else:
            verdict = "REAL"

        # Step 4: Source credibility calculation
        source_score, _ = self.source_scorer.score(domain, article_count)
        source_credibility = round(source_score * 100, 1)

        # Step 5: Credibility score (0-100, inverse of fake_score)
        credibility = round((1.0 - fake_score) * 100, 1)

        # Step 6: Ukrainian explanation
        explanation = self._build_explanation(
            verdict, ipso, fake_score, confidence, domain)

        ms = round((time.perf_counter() - start) * 1000, 2)

        return {
            "verdict": verdict,
            "credibility_score": credibility,
            "fake_score": round(fake_score, 4),
            "confidence": round(confidence, 4),
            "ipso_techniques": ipso,
            "source_credibility": source_credibility,
            "explanation_uk": explanation,
            "processing_time_ms": ms,
            "ml_method": ml["method"],
        }

    def _build_explanation(self, verdict: str, ipso: list[str],
                           fake_score: float, conf: float,
                           domain: str) -> str:
        parts = []
        if verdict == "FAKE":
            parts.append(f"Текст класифіковано як НЕДОСТОВІРНИЙ (score={fake_score:.2f}).")
            if ipso:
                parts.append(f"Виявлено ІПСО маніпуляції: {', '.join(ipso)}.")
            else:
                parts.append("Модель виявила ознаки маніпуляції.")
        elif verdict == "SUSPICIOUS":
            parts.append(f"Текст потребує додаткової перевірки (score={fake_score:.2f}).")
        else:
            parts.append(f"Текст класифіковано як ДОСТОВІРНИЙ (score={fake_score:.2f}).")
        parts.append(f"Впевненість: {conf*100:.0f}%.")
        return " ".join(parts)