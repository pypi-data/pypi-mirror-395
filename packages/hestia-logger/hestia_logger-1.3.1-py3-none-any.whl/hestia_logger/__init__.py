"""
HESTIA Logger - Asynchronous & Structured Logging System.

This package provides a high-performance, structured logging system that supports:
- Thread-based logging for performance and scalability.
- JSON and plain-text log formats.
- Internal logging for debugging HESTIA Logger itself.
- Compatibility with FastAPI, Flask, standalone scripts, and microservices.
- Optional Elasticsearch integration for centralized logging.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

# Define public API for `hestia_logger`
__all__ = ["get_logger", "LOG_LEVEL", "ELASTICSEARCH_HOST", "log_execution"]

# Expose only necessary functions/classes for clean imports
from .core.custom_logger import get_logger
from .core.config import LOG_LEVEL, ELASTICSEARCH_HOST
from .decorators.decorators import log_execution
