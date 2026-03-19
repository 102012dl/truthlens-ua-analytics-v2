from typing import Dict, Any

class VerdictEngine:
    """
    NMVP2 Verdict Engine
    Calculates the final Verdict Score based on the Custom Formula:
    Final_Score = (0.3 * ML_Score) + (0.4 * RoBERTa_Score) + (0.3 * IPSO_Penalty)
    """

    def __init__(self, ml_weight: float = 0.3, roberta_weight: float = 0.4, ipso_weight: float = 0.3):
        self.ml_weight = ml_weight
        self.roberta_weight = roberta_weight
        self.ipso_weight = ipso_weight

    def evaluate(self, ml_score: float, roberta_score: float, ipso_penalty: float) -> Dict[str, Any]:
        """
        Evaluate text features and return a verdict based on NMVP2 thresholds.
        Thresholds:
        - Real: < 0.35
        - Suspicious: 0.35 - 0.65
        - Fake: > 0.65
        """
        final_score = (self.ml_weight * ml_score) + \
                      (self.roberta_weight * roberta_score) + \
                      (self.ipso_weight * ipso_penalty)
                      
        final_score = min(max(final_score, 0.0), 1.0)

        if final_score < 0.35:
            verdict = "REAL"
        elif final_score <= 0.65:
            verdict = "SUSPICIOUS"
        else:
            verdict = "FAKE"

        return {
            "verdict": verdict,
            "final_score": round(final_score, 4),
            "formula_breakdown": {
                "ml_score": ml_score,
                "ml_weight": self.ml_weight,
                "ml_contribution": round(self.ml_weight * ml_score, 4),
                "roberta_score": roberta_score,
                "roberta_weight": self.roberta_weight,
                "roberta_contribution": round(self.roberta_weight * roberta_score, 4),
                "ipso_penalty": ipso_penalty,
                "ipso_weight": self.ipso_weight,
                "ipso_contribution": round(self.ipso_weight * ipso_penalty, 4)
            }
        }
