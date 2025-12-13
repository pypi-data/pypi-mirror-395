"""
HESTIA Logger - Middlewares Module.

Provides middleware for request logging in web frameworks.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

# Expose middleware module
from .middleware import LoggingMiddleware
from .middleware import setup_logging_middleware


# Define public API for `middlewares`
__all__ = ["LoggingMiddleware", "setup_logging_middleware"]
