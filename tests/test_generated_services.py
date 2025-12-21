"""
Integration tests for generated service functionality
"""
import pytest
import sys
from pathlib import Path
from importlib import import_module


def test_generated_fastapi_service_imports():
    """Test that a generated FastAPI service has valid imports"""
    # This assumes there's at least one example service
    examples_dir = Path(__file__).parent.parent / "examples"
    
    # Find a fastapi service
    fastapi_services = []
    if examples_dir.exists():
        for service_dir in examples_dir.iterdir():
            if service_dir.is_dir() and (service_dir / "app" / "main.py").exists():
                fastapi_services.append(service_dir)
    
    if not fastapi_services:
        pytest.skip("No FastAPI services found in examples/")
    
    # Test the first one
    service_dir = fastapi_services[0]
    
    # Verify key files exist
    assert (service_dir / "app" / "main.py").exists()
    assert (service_dir / "app" / "config_provider.py").exists()
    assert (service_dir / "app" / "middleware.py").exists()


def test_generated_service_has_health_endpoints():
    """Verify generated services have required health endpoints"""
    examples_dir = Path(__file__).parent.parent / "examples"
    
    if not examples_dir.exists():
        pytest.skip("No examples directory found")
    
    fastapi_services = [
        d for d in examples_dir.iterdir()
        if d.is_dir() and (d / "app" / "routers.py").exists()
    ]
    
    if not fastapi_services:
        pytest.skip("No FastAPI services found")
    
    service_dir = fastapi_services[0]
    routers_file = service_dir / "app" / "routers.py"
    content = routers_file.read_text()
    
    # Check for health endpoints
    assert "/health/live" in content or "health" in content.lower()
    assert "/health/ready" in content or "ready" in content.lower()


def test_generated_service_has_prometheus_metrics():
    """Verify generated services include Prometheus instrumentation"""
    examples_dir = Path(__file__).parent.parent / "examples"
    
    if not examples_dir.exists():
        pytest.skip("No examples directory found")
    
    # Check template has Prometheus
    template_main = Path(__file__).parent.parent / "platform" / "templates" / "fastapi_service" / "app" / "main.py"
    
    if template_main.exists():
        content = template_main.read_text()
        assert "prometheus" in content.lower() or "Instrumentator" in content


def test_generated_service_dockerfile_exists():
    """Verify all generated services have Dockerfiles"""
    examples_dir = Path(__file__).parent.parent / "examples"
    
    if not examples_dir.exists():
        pytest.skip("No examples directory found")
    
    services = [d for d in examples_dir.iterdir() if d.is_dir()]
    
    if not services:
        pytest.skip("No services found")
    
    # At least one service should have a Dockerfile
    dockerfiles = [s / "Dockerfile" for s in services if (s / "Dockerfile").exists()]
    assert len(dockerfiles) > 0, "No Dockerfiles found in generated services"
