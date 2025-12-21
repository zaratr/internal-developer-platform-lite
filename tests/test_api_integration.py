"""
Integration tests for the Control Plane API
"""
import pytest
from fastapi.testclient import TestClient
from platform.api.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test API health check"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_templates():
    """Test listing available templates"""
    response = client.get("/api/v1/services/templates")
    assert response.status_code == 200
    templates = response.json()
    assert isinstance(templates, list)
    assert "fastapi_service" in templates
    assert "springboot_service" in templates


def test_list_services():
    """Test listing services"""
    response = client.get("/api/v1/services/")
    assert response.status_code == 200
    services = response.json()
    assert isinstance(services, list)


def test_create_service_invalid_template():
    """Test creating service with invalid template"""
    response = client.post(
        "/api/v1/services/",
        json={
            "name": "test-service",
            "template": "nonexistent-template",
            "ai_enhance": False
        }
    )
    assert response.status_code == 400
    assert "Invalid template" in response.json()["detail"]


def test_create_service_invalid_name():
    """Test creating service with invalid name"""
    response = client.post(
        "/api/v1/services/",
        json={
            "name": "Invalid Service Name!",
            "template": "fastapi_service",
            "ai_enhance": False
        }
    )
    # Should fail validation or creation
    assert response.status_code in [400, 422, 500]
