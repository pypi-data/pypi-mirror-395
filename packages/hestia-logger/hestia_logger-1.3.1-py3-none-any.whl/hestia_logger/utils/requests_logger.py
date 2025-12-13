"""
Hestia Logger - Request Logger.

Logs HTTP request and response details for API-based applications.
Supports FastAPI, Flask, and other web frameworks.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import logging
import os
from ..core.config import LOGS_DIR, LOG_LEVEL as DEFAULT_LOG_LEVEL
from ..core.formatters import JSONFormatter
from ..handlers.console_handler import console_handler  # Use global handler

__all__ = ["requests_logger"]

# Initialize request logger
requests_logger = logging.getLogger("hestia_requests")

# Allow overriding the log level specifically for the requests logger
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}
LOG_LEVEL_STR = os.getenv("REQUESTS_LOG_LEVEL", "").upper()
LOG_LEVEL = LOG_LEVELS.get(LOG_LEVEL_STR, DEFAULT_LOG_LEVEL)
requests_logger.setLevel(LOG_LEVEL)

# Use global console handler instead of redefining one
if console_handler not in requests_logger.handlers:
    requests_logger.addHandler(console_handler)

# Use JSON formatting for structured logging
json_formatter = JSONFormatter()
log_file_path = os.path.join(LOGS_DIR, "requests.log")
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

file_handler_exists = any(
    isinstance(handler, logging.FileHandler)
    and getattr(handler, "baseFilename", None) == os.path.abspath(log_file_path)
    for handler in requests_logger.handlers
)

if not file_handler_exists:
    file_handler = logging.FileHandler(log_file_path, delay=True)
    file_handler.setFormatter(json_formatter)
    requests_logger.addHandler(file_handler)

# Prevent log duplication
requests_logger.propagate = False
