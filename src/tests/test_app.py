import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app, follow_redirects=False)

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data
    assert "participants" in data["Basketball Team"]

def test_signup_success():
    response = client.post("/activities/Basketball%20Team/signup?email=test@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up test@example.com for Basketball Team" in data["message"]

def test_signup_already_signed_up():
    # First signup
    client.post("/activities/Tennis%20Club/signup?email=duplicate@example.com")
    # Second signup
    response = client.post("/activities/Tennis%20Club/signup?email=duplicate@example.com")
    assert response.status_code == 400
    data = response.json()
    assert "Student already signed up for this activity" in data["detail"]

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent%20Activity/signup?email=test@example.com")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_unregister_success():
    # First signup
    client.post("/activities/Art%20Studio/signup?email=unregister@example.com")
    # Then unregister
    response = client.delete("/activities/Art%20Studio/participants?email=unregister@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered unregister@example.com from Art Studio" in data["message"]

def test_unregister_not_signed_up():
    response = client.delete("/activities/Drama%20Club/participants?email=notsigned@example.com")
    assert response.status_code == 400
    data = response.json()
    assert "Student not signed up for this activity" in data["detail"]

def test_unregister_activity_not_found():
    response = client.delete("/activities/Nonexistent%20Activity/participants?email=test@example.com")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]