import os
import math
import re
from pathlib import Path
from typing import Dict, Any

__all__ = ["TruthLensClassifier"]


class TruthLensClassifier:
    """
    Binary classifier: REAL vs FAKE
    Model: LinearSVC(C=1.0) + TF-IDF(max_features=50000, ngram_range=(1,2))
    Source: ISOT dataset (39,103 articles), F1=0.9947
    Fallback: rule-based if model not found
    """

    def __init__(self):
        self.model_path = os.getenv("MODEL_PATH", "artifacts/best_model.joblib")
        self.pipeline = self._load_model()

    def _load_model(self):
        """Load trained model or return None for fallback."""
        if Path(self.model_path).exists():
            try:
                import joblib
                pipeline = joblib.load(self.model_path)
                print(f"[classifier] Model loaded: {self.model_path}")
                return pipeline
            except Exception as e:
                print(f"[classifier] Error loading model: {e}")
        print("[classifier] Model not found — using rule-based fallback")
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
        """Simple rule-based fallback classifier."""
        fake_signals = [
            r'ТЕРМІНОВО|BREAKING|ЗАРАЗ',
            r'ПОШИРТЕ|поширте|Поширте',
            r'приховують|замовчують',
            r'до видалення|успіть прочитати',
        ]
        
        score = 0.0
        for pattern in fake_signals:
            if re.search(pattern, text, re.IGNORECASE):
                score += 0.25
        
        score = min(score, 0.95)
        fake_score = round(max(0.05, score), 4)
        verdict = "FAKE" if fake_score >= 0.65 else \
                 "SUSPICIOUS" if fake_score >= 0.40 else "REAL"
        
        return {
            "verdict": verdict,
            "fake_score": fake_score,
            "confidence": 0.5,
            "raw_score": fake_score,
            "method": "rule_based"
        }