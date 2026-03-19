import time
from typing import Dict, Any

from app.agents.classifier import TruthLensClassifier
from app.agents.ipso_detector import IPSODetector
from app.agents.source_scorer import SourceScorer
from app.agents.verdict_engine import VerdictEngine
from app.agents.ua_classifier import UkrainianClassifier

__all__ = ["TruthLensOrchestrator"]


class TruthLensOrchestrator:
    """Main analysis pipeline — NMVP2."""

    def __init__(self):
        self.classifier = TruthLensClassifier()
        self.ipso_detector = IPSODetector()
        self.source_scorer = SourceScorer()
        self.ua_classifier = UkrainianClassifier()
        self.verdict_engine = VerdictEngine()

    async def process(self, text: str, domain: str = "direct",
                      article_count: int = 0, language: str = "uk") -> Dict[str, Any]:
        """
        Full analysis pipeline:
        1. ML classification (LinearSVC)
        2. Semantic Analysis (Mocked ukr-roberta-base)
        3. ІПСО technique detection -> IPSO penalty
        4. Verdict determination via VerdictEngine
        5. Credibility score calculation
        6. Ukrainian explanation generation
        Returns complete verdict dict.
        """
        start = time.perf_counter()

        # Step 1: ML classification
        ml = self.classifier.classify(text)
        fake_score = ml["fake_score"]
        confidence = ml["confidence"]

        # Step 2: Semantic Analysis (Mocked RoBERTa)
        roberta_score = fake_score
        if language == "uk" and self.ua_classifier.pipeline:
            ua = self.ua_classifier.classify(text)
            if ua["verdict"] is not None:
                roberta_score = 1.0 - ua["score"] if ua["verdict"] == "REAL" else ua["score"]
                ml["method"] += " + ukr-roberta"

        # Step 3: ІПСО detection
        ipso = self.ipso_detector.detect(text)
        # Normalize IPSO penalty from 0 to 1 based on detected techniques 
        # (Assuming 4 detected techniques is max manipulation score 1.0)
        ipso_penalty = min(len(ipso) / 4.0, 1.0)

        # Step 4: Source Scoring (Adds penalty to fake_score if suspicious)
        source_score, _ = self.source_scorer.score(domain, article_count)
        source_penalty = 0.2 if domain in ["blacklisted_domain.com"] else 0.0 # simplified logic
        
        # In NMVP2 prompt: "If source in blacklist, add +0.2 to P_final."
        # We handle source score separately or add to ipso_penalty

        # Step 5: VerdictEngine evaluation
        verdict_result = self.verdict_engine.evaluate(fake_score, roberta_score, ipso_penalty)
        final_score = verdict_result["final_score"]
        verdict = verdict_result["verdict"]
        
        # Apply source penalty if any
        if source_penalty > 0:
            final_score = min(final_score + source_penalty, 1.0)
            if final_score < 0.35: verdict = "REAL"
            elif final_score <= 0.65: verdict = "SUSPICIOUS"
            else: verdict = "FAKE"

        # Credibility is inverse of final score
        credibility = round((1.0 - final_score) * 100, 1)

        # Ukrainian explanation
        explanation = self._build_explanation(
            verdict, ipso, final_score, confidence, domain)

        ms = round((time.perf_counter() - start) * 1000, 2)

        return {
            "verdict": verdict,
            "credibility_score": credibility,
            "fake_score": round(final_score, 4),
            "ml_score": round(fake_score, 4),
            "roberta_score": round(roberta_score, 4),
            "ipso_penalty": round(ipso_penalty, 4),
            "confidence": round(confidence, 4),
            "ipso_techniques": ipso,
            "source_credibility": round(source_score * 100, 1),
            "explanation_uk": explanation,
            "processing_time_ms": ms,
            "ml_method": ml["method"],
            "formula_breakdown": verdict_result["formula_breakdown"]
        }

    def _build_explanation(self, verdict: str, ipso: list[str],
                           final_score: float, conf: float,
                           domain: str) -> str:
        parts = []
        if verdict == "FAKE":
            parts.append(f"Текст класифіковано як ВІДВЕРТИЙ ФЕЙК (score={final_score:.2f}).")
            if ipso:
                parts.append(f"Виявлено ІПСО маніпуляції: {', '.join(ipso)}.")
        elif verdict == "SUSPICIOUS":
            parts.append(f"Текст ПІДОЗРІЛИЙ та потребує додаткової перевірки (score={final_score:.2f}).")
            if ipso:
                parts.append(f"Присутні маніпулятивні маркери: {', '.join(ipso)}.")
        else:
            parts.append(f"Текст класифіковано як ДОСТОВІРНИЙ (score={final_score:.2f}). Він не містить ознак ІПСО.")
            
        parts.append(f"Впевненість алгоритмів: {conf*100:.0f}%.")
        return " ".join(parts)
