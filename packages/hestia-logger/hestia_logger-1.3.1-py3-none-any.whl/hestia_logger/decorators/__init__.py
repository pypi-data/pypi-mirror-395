"""
HESTIA Logger - Decorators Module.

Provides logging decorators that:
- Log function entry, exit, and execution time.
- Support both synchronous and asynchronous functions.
- Use `structlog` for structured JSON logging.
- Mask sensitive parameters like passwords and API keys.

Available Decorators:
- `log_execution`: Logs function calls, execution time, and errors.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from .decorators import log_execution

__all__ = ["log_execution"]
