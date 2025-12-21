"""
End-to-end test demonstrating the complete IDP-Lite workflow
"""
import pytest
import shutil
import subprocess
import tempfile
from pathlib import Path
from platform.cli.idp import create_service, get_available_templates, ROOT


@pytest.fixture
def temp_examples_dir():
    """Create a temporary directory for test services"""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_e2e_fastapi_service_workflow(temp_examples_dir):
    """
    End-to-end test: Create FastAPI service, verify structure, check it can start
    """
    service_name = "e2e-test-service"
    
    # Step 1: Create service
    service_path = create_service(
        name=service_name,
        template_name="fastapi_service",
        examples_dir=temp_examples_dir,
        ai_enhance=False
    )
    
    # Step 2: Verify service structure
    assert service_path.exists()
    assert (service_path / "pyproject.toml").exists()
    assert (service_path / "Dockerfile").exists()
    assert (service_path / "app" / "main.py").exists()
    assert (service_path / "app" / "routers.py").exists()
    
    # Step 3: Verify placeholders were replaced
    main_py = (service_path / "app" / "main.py").read_text()
    assert "{{service_name}}" not in main_py
    assert service_name in main_py or "e2e_test_service" in main_py
    
    # Step 4: Verify pyproject.toml has correct dependencies
    pyproject = (service_path / "pyproject.toml").read_text()
    assert "fastapi" in pyproject
    assert "prometheus-fastapi-instrumentator" in pyproject


def test_e2e_springboot_service_workflow(temp_examples_dir):
    """
    End-to-end test: Create Spring Boot service and verify structure
    """
    service_name = "e2e-java-service"
    
    # Step 1: Create service
    service_path = create_service(
        name=service_name,
        template_name="springboot_service",
        examples_dir=temp_examples_dir,
        ai_enhance=False
    )
    
    # Step 2: Verify service structure
    assert service_path.exists()
    assert (service_path / "pom.xml").exists()
    assert (service_path / "Dockerfile").exists()
    assert (service_path / "src" / "main" / "java").exists()
    
    # Step 3: Verify Java files exist
    java_dir = service_path / "src" / "main" / "java" / "com" / "example" / "service"
    assert java_dir.exists()
    assert (java_dir / "ServiceApplication.java").exists()
    assert (java_dir / "GreetingsController.java").exists()
    
    # Step 4: Verify placeholders were replaced
    pom = (service_path / "pom.xml").read_text()
    assert "{{service_name}}" not in pom
    assert service_name in pom


def test_e2e_ai_enhancement_workflow(temp_examples_dir):
    """
    End-to-end test: Create service with AI enhancement
    """
    service_name = "ai-enhanced-service"
    
    # Create service with AI enhancement
    service_path = create_service(
        name=service_name,
        template_name="fastapi_service",
        examples_dir=temp_examples_dir,
        ai_enhance=True
    )
    
    # Verify AI optimization report was created
    ai_report = service_path / "AI_OPTIMIZATION.md"
    assert ai_report.exists()
    
    report_content = ai_report.read_text()
    assert service_name in report_content
    assert "Optimization Suggestions" in report_content
    assert "Confidence Score" in report_content


def test_template_availability():
    """Verify all expected templates are available"""
    templates = get_available_templates()
    assert "fastapi_service" in templates
    assert "springboot_service" in templates
    assert len(templates) >= 2
