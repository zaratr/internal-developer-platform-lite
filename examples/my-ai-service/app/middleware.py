import structlog
from fastapi import Request

from .logging_config import bind_request

logger = structlog.get_logger()


async def correlation_id_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or request.state.request_id if hasattr(request.state, "request_id") else None
    if not request_id:
        request_id = request.scope.get("request_id") or request.headers.get("X-Correlation-ID") or "generated"
    bound = bind_request(logger, request_id)
    request.state.logger = bound
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


async def metrics_stub_middleware(request: Request, call_next):
    # Placeholder to emit metrics to Prometheus/OpenTelemetry.
    return await call_next(request)
