"""Tests for GET /health and GET /"""

def test_root_returns_service(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["service"] == "TruthLens UA Analytics"

def test_health_returns_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] in ["ok", "degraded"]
    assert "db" in data
    assert "timestamp" in data