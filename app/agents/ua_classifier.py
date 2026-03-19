"""Ukrainian text classifier using ukr-roberta-base."""
import os
from pathlib import Path

class UkrainianClassifier:
    MODEL_NAME = "youscan/ukr-roberta-base"
    LABELS = ["REAL", "FAKE"]

    def __init__(self):
        self.pipeline = None
        self._load()

    def _load(self):
        try:
            from transformers import pipeline
            model_path = os.environ.get("UA_MODEL_PATH",
                "artifacts/ua_roberta_model")
            if Path(model_path).exists():
                self.pipeline = pipeline(
                    "text-classification",
                    model=model_path,
                    tokenizer=model_path,
                    device=-1  # CPU
                )
                print("[ua_classifier] Loaded from artifacts/")
            else:
                print("[ua_classifier] Model not found — using LinearSVC fallback")
        except ImportError:
            print("[ua_classifier] transformers not installed — using fallback")

    def classify(self, text: str) -> dict:
        if not self.pipeline:
            return {"verdict": None, "score": None, "method": "fallback"}
        
        # Max length for RoBERTa is typically 512 tokens. Let's send text slice.
        result = self.pipeline(text[:512], truncation=True)[0]
        label = result["label"].upper()
        score = result["score"]
        return {
            "verdict": label,
            "score": round(score, 4),
            "method": "ukr-roberta"
        }
