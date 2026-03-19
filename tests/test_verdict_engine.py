import pytest
from app.agents.verdict_engine import VerdictEngine

def test_verdict_engine_real():
    engine = VerdictEngine()
    # 0.3*0.1 + 0.4*0.1 + 0.3*0.0 = 0.03 + 0.04 = 0.07 (< 0.35) -> REAL
    result = engine.evaluate(0.1, 0.1, 0.0)
    assert result["verdict"] == "REAL"
    assert result["final_score"] == 0.07

def test_verdict_engine_suspicious():
    engine = VerdictEngine()
    # 0.3*0.5 + 0.4*0.5 + 0.3*0.5 = 0.15 + 0.20 + 0.15 = 0.50 (between 0.35 and 0.65) -> SUSPICIOUS
    result = engine.evaluate(0.5, 0.5, 0.5)
    assert result["verdict"] == "SUSPICIOUS"
    assert result["final_score"] == 0.50

def test_verdict_engine_fake():
    engine = VerdictEngine()
    # 0.3*0.8 + 0.4*0.9 + 0.3*0.5 = 0.24 + 0.36 + 0.15 = 0.75 (> 0.65) -> FAKE
    result = engine.evaluate(0.8, 0.9, 0.5)
    assert result["verdict"] == "FAKE"
    assert result["final_score"] == 0.75

def test_verdict_engine_ipso_penalty_override():
    engine = VerdictEngine()
    # ML and RoBERTa say it's real (low scores), but IPSO penalty is high (1.0)
    # 0.3*0.1 + 0.4*0.1 + 0.3*1.0 = 0.03 + 0.04 + 0.30 = 0.37 (Suspicious)
    result = engine.evaluate(0.1, 0.1, 1.0)
    assert result["verdict"] == "SUSPICIOUS"
    assert result["final_score"] == 0.37

def test_verdict_engine_boundaries():
    engine = VerdictEngine()
    # Exactly 0.35 -> Suspicious
    result = engine.evaluate(0.35, 0.35, 0.35)
    # 0.3*0.35 + 0.4*0.35 + 0.3*0.35 = 0.35
    assert result["verdict"] == "SUSPICIOUS"
    
    # 0.66 -> FAKE
    result = engine.evaluate(0.66, 0.66, 0.66)
    assert result["verdict"] == "FAKE"
