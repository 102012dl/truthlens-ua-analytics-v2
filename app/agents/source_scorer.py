from typing import Dict, Tuple

__all__ = ["SourceScorer"]


class SourceScorer:
    """
    Source Credibility Formula (Author: 102012dl, Neoversity MSCS 2026):
    
    credibility = (
        0.35 * evidence_overlap          # how many articles confirm each other
        0.25 * (1 - contradiction_rate)  # inverse of contradictions
        0.20 * source_consistency        # publication pattern consistency
        0.20 * domain_trust_prior        # prior trust from known domains registry
    )
    
    Range: [0.0, 1.0] where 1.0 = fully trusted source
    Documented in: docs/metrics/FORMULAS.md
    """

    # Ukrainian trusted domains registry (initial priors based on
    # StopFake credibility assessments and journalistic standards)
    TRUSTED_DOMAINS = {
        "pravda.com.ua": 0.92, "ukrinform.ua": 0.91,
        "hromadske.ua": 0.89, "nv.ua": 0.87, "zn.ua": 0.88,
        "unian.ua": 0.84, "liga.net": 0.83, "voxukraine.org": 0.90,
        "stopfake.org": 0.92, "fakty.ua": 0.80,
    }
    UNTRUSTED_DOMAINS = {
        "riafan": 0.04, "anna-news": 0.05, "imperiya.by": 0.08,
        "politnavigator": 0.07, "newsland": 0.15, "topwar.ru": 0.10,
        "russian-disinfo": 0.03,
    }

    def get_domain_prior(self, domain: str) -> float:
        """Look up domain in registry. Returns 0.5 for unknown."""
        domain_lower = domain.lower()
        for d, score in self.TRUSTED_DOMAINS.items():
            if d in domain_lower:
                return score
        for d, score in self.UNTRUSTED_DOMAINS.items():
            if d in domain_lower:
                return score
        return 0.50

    def score(self, domain: str, article_count: int = 0,
              contradiction_rate: float = 0.10,
              consistency_rate: float = 0.70) -> Tuple[float, Dict[str, float]]:
        """
        Calculate credibility score.
        Returns (score_0_to_1, breakdown_dict)
        """
        prior = self.get_domain_prior(domain)
        evidence = min(1.0, article_count / 100.0)

        breakdown = {
            "evidence_overlap": round(evidence, 3),
            "contradiction_inverse": round(1.0 - contradiction_rate, 3),
            "source_consistency": round(consistency_rate, 3),
            "domain_trust_prior": round(prior, 3),
        }
        raw = (
            0.35 * breakdown["evidence_overlap"] +
            0.25 * breakdown["contradiction_inverse"] +
            0.20 * breakdown["source_consistency"] +
            0.20 * breakdown["domain_trust_prior"]
        )
        final = round(min(1.0, max(0.0, raw)), 4)
        return final, breakdown

    def label(self, score: float) -> str:
        if score >= 0.75: return "HIGH"
        if score >= 0.45: return "MEDIUM"
        return "LOW"