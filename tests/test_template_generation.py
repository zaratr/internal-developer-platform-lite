from pathlib import Path

from platform.cli import idp


def test_create_service(tmp_path: Path):
    dest = idp.create_service("demo-service", examples_dir=tmp_path)
    assert (dest / "pyproject.toml").exists()
    assert (dest / "app" / "main.py").exists()
    content = (dest / "pyproject.toml").read_text()
    assert "demo_service" in content
