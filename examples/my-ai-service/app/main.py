import os

import structlog
from fastapi import FastAPI

from .config_provider import EnvConfigProvider
from .logging_config import configure_logging, log_startup
from .middleware import correlation_id_middleware, metrics_stub_middleware
from .routers import router

service_env = os.environ.get("SERVICE_ENV", "dev")
config_provider = EnvConfigProvider()
config = config_provider.load(service_env)

configure_logging(service_name=config.service_name, log_level=config.log_level)
logger = structlog.get_logger()
log_startup(logger, {"service": config.service_name, "env": service_env, "version": config.version})

app = FastAPI(title=config.service_name)
app.include_router(router)
app.middleware("http")(correlation_id_middleware)
app.middleware("http")(metrics_stub_middleware)


@app.get("/")
def root() -> dict:
    return {"message": f"Welcome to {config.service_name}", "version": config.version}
