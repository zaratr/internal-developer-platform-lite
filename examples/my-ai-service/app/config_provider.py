from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

import yaml
from pydantic import BaseModel


class ServiceConfig(BaseModel):
    service_name: str
    log_level: str = "INFO"
    version: str = "0.1.0"

    class Config:
        extra = "ignore"


class ConfigProvider:
    """Abstract config provider.

    In production this can be swapped with Vault, Secrets Manager, etc.
    """

    def load(self, env: str) -> ServiceConfig:
        raise NotImplementedError


class EnvConfigProvider(ConfigProvider):
    def __init__(self, root: Path | None = None):
        self.root = root or Path(__file__).resolve().parent.parent

    def _load_yaml(self, env: str) -> Dict[str, Any]:
        config_path = self.root / "config" / f"{env}.yaml"
        if not config_path.exists():
            raise FileNotFoundError(f"Missing config file for env {env}: {config_path}")
        with config_path.open() as f:
            return yaml.safe_load(f) or {}

    def load(self, env: str) -> ServiceConfig:
        base = self._load_yaml(env)
        # Secrets are expected to be injected as env vars to avoid hardcoding.
        env_overrides = {k: v for k, v in os.environ.items() if k.startswith("SERVICE_")}
        merged = {**base, **env_overrides}
        return ServiceConfig(**merged)
