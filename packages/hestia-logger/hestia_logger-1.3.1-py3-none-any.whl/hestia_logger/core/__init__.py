"""
HESTIA Logger - Core Module.

This module contains the foundational components of HESTIA Logger:
- `config.py` - Logging configuration setup.
- `custom_logger.py` - Provides structured logging functions.
- `async_logger.py` - Manages async logging if required.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

# Define public API for `core`
__all__ = ["get_logger", "LOG_LEVEL", "ELASTICSEARCH_HOST"]

# Expose logger functions and configurations
from .custom_logger import get_logger
from .config import LOG_LEVEL, ELASTICSEARCH_HOST
