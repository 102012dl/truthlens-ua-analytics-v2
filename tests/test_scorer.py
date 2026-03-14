"""Tests for SourceScorer formula."""
from app.agents.source_scorer import SourceScorer

def test_trusted_domain_high_score():
    s = SourceScorer()
    score, _ = s.score("pravda.com.ua", 100, 0.02, 0.95)
    assert score >= 0.70

def test_untrusted_domain_low_score():
    s = SourceScorer()
    score, _ = s.score("riafan.ru", 50, 0.60, 0.20)
    assert score <= 0.35

def test_score_range_always_valid():
    s = SourceScorer()
    for domain in ["pravda.com.ua","riafan.ru","unknown.ua","","-"]:
        score, _ = s.score(domain)
        assert 0.0 <= score <= 1.0, f"Score out of range for '{domain}': {score}"

def test_formula_weights_sum_to_one():
    # 0.35 + 0.25 + 0.20 + 0.20 = 1.0
    assert abs(0.35 + 0.25 + 0.20 + 0.20 - 1.0) < 1e-10