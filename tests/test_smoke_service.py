from pathlib import Path

from fastapi.testclient import TestClient

from platform.cli import idp


def test_generated_service_health(tmp_path: Path):
    dest = idp.create_service("smoke-service", examples_dir=tmp_path)
    import importlib.util
    import sys

    sys.path.insert(0, str(dest))
    spec = importlib.util.spec_from_file_location("app.main", dest / "app" / "main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore
    app = module.app

    client = TestClient(app)
    response = client.get("/health/live")
    assert response.status_code == 200
    response_ready = client.get("/health/ready")
    assert response_ready.status_code == 200
