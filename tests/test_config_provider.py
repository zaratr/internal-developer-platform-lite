import os
from pathlib import Path

from platform.templates.fastapi_service.app.config_provider import EnvConfigProvider


def test_env_provider_reads_yaml_and_env(tmp_path: Path, monkeypatch):
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "dev.yaml").write_text("""
service_name: test-service
log_level: INFO
version: 1.2.3
""")
    monkeypatch.setenv("SERVICE_SECRET_TOKEN", "token123")

    provider = EnvConfigProvider(root=tmp_path)
    config = provider.load("dev")

    assert config.service_name == "test-service"
    assert config.log_level == "INFO"
    assert config.version == "1.2.3"
