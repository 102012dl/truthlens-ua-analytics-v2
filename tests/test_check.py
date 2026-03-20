"""Tests for POST /check endpoint."""

from app.schemas.check import CheckResponse

FAKE_TEXT = "ТЕРМІНОВО!!! ЗСУ ЗДАЛИ Харків! Поширте до видалення!!!"
REAL_TEXT = "НБУ підвищив облікову ставку до 16% на засіданні Правління."

def test_check_fake_returns_verdict(client):
    r = client.post("/check", json={"text": FAKE_TEXT})
    assert r.status_code == 200
    data = r.json()
    assert data["verdict"] in ["FAKE", "SUSPICIOUS"]

def test_check_fake_detects_ipso(client):
    r = client.post("/check", json={"text": FAKE_TEXT})
    assert len(r.json()["ipso_techniques"]) >= 1

def test_check_real_returns_real(client):
    r = client.post("/check", json={"text": REAL_TEXT})
    assert r.status_code == 200
    assert r.json()["verdict"] == "REAL"

def test_check_real_high_credibility(client):
    r = client.post("/check", json={"text": REAL_TEXT})
    assert r.json()["credibility_score"] > 50

def test_check_empty_input_fails(client):
    r = client.post("/check", json={})
    assert r.status_code == 400

def test_check_response_has_all_fields(client):
    r = client.post("/check", json={"text": "Це довге тестове речення українською мовою для перевірки всіх полів."})
    assert r.status_code == 200
    data = r.json()
    for field in CheckResponse.model_fields:
        assert field in data, f"Missing: {field}"