import os

from fastapi import APIRouter, Depends

from .config_provider import ConfigProvider, EnvConfigProvider, ServiceConfig

router = APIRouter()


def get_provider() -> ConfigProvider:
    return EnvConfigProvider()


def get_config(provider: ConfigProvider = Depends(get_provider)) -> ServiceConfig:
    env = os.environ.get("SERVICE_ENV", "dev")
    return provider.load(env)


@router.get("/health/live")
def liveness() -> dict:
    return {"status": "live"}


@router.get("/health/ready")
def readiness(config: ServiceConfig = Depends(get_config)) -> dict:
    return {"status": "ready", "service": config.service_name, "version": config.version}


@router.get("/info")
def info(config: ServiceConfig = Depends(get_config)) -> dict:
    return {"service": config.service_name, "version": config.version}
