from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# ✅ Test 1 — health check
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# ✅ Test 2 — ingest events successfully
def test_ingest_events():
    response = client.post("/events", json=[
        {
            "eventId": "test001",
            "source": "web",
            "type": "click",
            "timestamp": "2026-06-06T12:00:00",
            "payload": {"page": "home"}
        }
    ])
    assert response.status_code == 201
    assert response.json()["saved"] == 1
    assert response.json()["rejected"] == 0

# ✅ Test 3 — duplicate rejection
def test_duplicate_event():
    payload = [{
        "eventId": "dup001",
        "source": "web",
        "type": "click",
        "timestamp": "2026-06-06T12:00:00",
        "payload": {}
    }]
    client.post("/events", json=payload)  # first insert
    response = client.post("/events", json=payload)  # duplicate
    assert response.status_code == 201
    assert response.json()["rejected"] == 1

# ✅ Test 4 — get event by id
def test_get_event():
    client.post("/events", json=[{
        "eventId": "get001",
        "source": "web",
        "type": "view",
        "timestamp": "2026-06-06T12:00:00",
        "payload": {}
    }])
    response = client.get("/events/get001")
    assert response.status_code == 200
    assert response.json()["eventId"] == "get001"

# ✅ Test 5 — 404 for missing event
def test_get_event_not_found():
    response = client.get("/events/doesnotexist")
    assert response.status_code == 404

# ✅ Test 6 — invalid event type
def test_invalid_event_type():
    response = client.post("/events", json=[{
        "eventId": "bad001",
        "source": "web",
        "type": "invalid_type",
        "timestamp": "2026-06-06T12:00:00",
        "payload": {}
    }])
    assert response.status_code == 422

# ✅ Test 7 — summary returns all types
def test_summary():
    response = client.get("/events/summary")
    assert response.status_code == 200
    data = response.json()
    assert "click" in data
    assert "view" in data
    assert "purchase" in data