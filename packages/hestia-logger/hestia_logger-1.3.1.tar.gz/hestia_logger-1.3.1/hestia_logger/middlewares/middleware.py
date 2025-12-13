"""
HESTIA Logger - Logging Middleware.

Provides middleware functions for logging request and response details
in web applications using FastAPI, Flask, and other frameworks. Enhanced with structured request ID support.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import uuid
import logging
import os
from typing import Any

try:  # Optional dependency: Starlette/FastAPI stack
    from starlette.middleware.base import BaseHTTPMiddleware
    from starlette.requests import Request
    from starlette.responses import Response

    STARLETTE_AVAILABLE = True
except ImportError:  # pragma: no cover - handled via _require_starlette
    BaseHTTPMiddleware = object  # type: ignore
    Request = Response = Any
    STARLETTE_AVAILABLE = False

from ..handlers.console_handler import console_handler  # Use global console handler
from ..core.formatters import JSONFormatter  # Use JSON formatter
from ..core.config import LOGS_DIR

__all__ = ["LoggingMiddleware"]


def _require_starlette():
    if not STARLETTE_AVAILABLE:  # pragma: no cover - exercised when optional dep missing
        raise ImportError(
            "Starlette/FastAPI is required for LoggingMiddleware support. "
            "Install hestia-logger[fastapi] or add 'starlette' to your project dependencies."
        )


class LoggingMiddleware:
    """
    Middleware that logs incoming requests and outgoing responses.
    """

    def __init__(self, logger_name="hestia_middleware"):
        _require_starlette()
        """
        Initializes the middleware with a logger instance.
        """
        self.logger = logging.getLogger(logger_name)

        # Load log level from environment variable
        LOG_LEVELS = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        LOG_LEVEL_STR = os.getenv("MIDDLEWARE_LOG_LEVEL", "INFO").upper()
        LOG_LEVEL = LOG_LEVELS.get(LOG_LEVEL_STR, logging.INFO)
        self.logger.setLevel(LOG_LEVEL)

        # Use global console handler
        if console_handler not in self.logger.handlers:
            self.logger.addHandler(console_handler)

        # Use JSON formatting for structured logging
        log_file_path = os.path.join(LOGS_DIR, "middleware.log")
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        formatter = JSONFormatter()

        file_handler_exists = any(
            isinstance(handler, logging.FileHandler)
            and getattr(handler, "baseFilename", None)
            == os.path.abspath(log_file_path)
            for handler in self.logger.handlers
        )

        if not file_handler_exists:
            file_handler = logging.FileHandler(log_file_path, delay=True)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        # Prevent log duplication
        self.logger.propagate = False

    def log_request(self, request: Request):
        """
        Logs details of an incoming HTTP request.
        """
        state = getattr(request, "state", None)
        request_id = getattr(state, "request_id", "unknown") if state else "unknown"
        url = getattr(request, "url", None)
        path = getattr(url, "path", None)
        query = getattr(url, "query", "")
        client = getattr(request, "client", None)
        headers = getattr(request, "headers", {}) or {}

        log_entry = {
            "event": "incoming_request",
            "request_id": request_id,
            "method": getattr(request, "method", "UNKNOWN"),
            "path": str(path) if path is not None else str(url),
            "query": str(query),
            "client": getattr(client, "host", "unknown") if client else "unknown",
            "headers": {
                "user-agent": headers.get("user-agent"),
                "host": headers.get("host"),
            },
        }
        self.logger.info(log_entry)

    def log_response(self, request: Request, response: Response):
        """
        Logs details of an outgoing HTTP response.
        """
        state = getattr(request, "state", None)
        request_id = getattr(state, "request_id", "unknown") if state else "unknown"
        log_entry = {
            "event": "outgoing_response",
            "request_id": request_id,
            "status_code": response.status_code,
        }
        self.logger.info(log_entry)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware to inject a UUID-based request_id into the request state and response headers.
    """

    def __init__(self, *args, **kwargs):
        _require_starlette()
        super().__init__(*args, **kwargs)

    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


def setup_logging_middleware(app, logger_name="hestia_middleware"):
    """
    Apply HESTIA logging and request ID middleware to a FastAPI app.
    """
    _require_starlette()
    logger = LoggingMiddleware(logger_name)

    @app.middleware("http")
    async def log_wrapper(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id

        logger.log_request(request)
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        logger.log_response(request, response)
        return response
