"""
HESTIA Logger - Console Handler.

Defines a structured console handler that outputs logs to the terminal
with proper formatting, including optional colored logs for better visibility.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import logging
import sys

try:
    import colorama
except ImportError:  # pragma: no cover - optional dependency
    colorama = None

import colorlog  # Provides colored console output

__all__ = ["console_handler"]


def _supports_color():
    """
    Detect whether the current platform supports ANSI colors without extra helpers.
    """
    if sys.platform == "win32":
        return False
    return getattr(sys.stdout, "isatty", lambda: False)()


def _get_formatter():
    format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    if colorama is not None:
        colorama.just_fix_windows_console()
    if colorama or _supports_color():
        return colorlog.ColoredFormatter(
            "%(log_color)s" + format_string,
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )
    return logging.Formatter(format_string)


console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(_get_formatter())
