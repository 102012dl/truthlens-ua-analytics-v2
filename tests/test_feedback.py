def test_feedback_valid(client):
    # First create a check
    r = client.post("/check", json={"text": "ТЕРМІНОВО!!! Харків!!!"})
    check_id = r.json().get("article_id", 1)  # Fallback to 1 if not present
    
    # Submit feedback
    r2 = client.post("/api/v1/feedback", json={
        "check_id": check_id,
        "correct_verdict": "FAKE",
        "user_type": "test_user"
    })
    assert r2.status_code == 200
    assert r2.json()["status"] == "received"
