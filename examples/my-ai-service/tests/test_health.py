from fastapi.testclient import TestClient

from app.main import app


def test_health_live():
    client = TestClient(app)
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json()["status"] == "live"


def test_health_ready():
    client = TestClient(app)
    response = client.get("/health/ready")
    data = response.json()
    assert data["status"] == "ready"
    assert "service" in data
