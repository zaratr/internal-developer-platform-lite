import logging
import sys
from typing import Any, Dict

import structlog


def configure_logging(service_name: str, log_level: str = "INFO") -> None:
    level = logging.getLevelName(log_level.upper())
    logging.basicConfig(stream=sys.stdout, level=level)
    processors = [
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),
    ]

    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(level),
    )


def bind_request(logger: structlog.BoundLogger, request_id: str) -> structlog.BoundLogger:
    return logger.bind(request_id=request_id)


def log_startup(logger: structlog.BoundLogger, config: Dict[str, Any]) -> None:
    logger.info("service.startup", **config)
