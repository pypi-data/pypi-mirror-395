"""
HESTIA Logger - Handlers Module.

Defines threaded log handlers for asynchronous file-based logging,
console logging, and optional Elasticsearch logging.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

# Expose handlers
from .file_handler import file_handler_app
from .console_handler import console_handler
from .elasticsearch_handler import get_es_handler  # Ensure this exists

es_handler = get_es_handler()

# Define public API for `handlers`
__all__ = ["file_handler_app", "console_handler", "es_handler"]
