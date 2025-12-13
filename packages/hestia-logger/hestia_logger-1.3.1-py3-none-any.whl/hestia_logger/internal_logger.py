"""
HESTIA Logger - Internal Debug Logger.

Provides a separate internal logging system for debugging the HESTIA Logger package.
Used to capture errors and diagnostic information about the logging process itself.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import logging
import os
import colorlog
from logging.handlers import RotatingFileHandler
from .core.config import (
    LOG_FILE_PATH_INTERNAL,
    LOG_FILE_ENCODING,
    LOG_FILE_ENCODING_ERRORS,
    ENABLE_INTERNAL_LOGGER,
)
from .core.formatters import JSONFormatter

__all__ = ["hestia_internal_logger"]


class NullLogger:
    """
    A dummy logger that ignores all messages. Used when internal logging is disabled.
    """

    def debug(self, *args, **kwargs):
        pass

    def info(self, *args, **kwargs):
        pass

    def warning(self, *args, **kwargs):
        pass

    def error(self, *args, **kwargs):
        pass

    def critical(self, *args, **kwargs):
        pass


# If internal logging is disabled, use NullLogger
if not ENABLE_INTERNAL_LOGGER:
    hestia_internal_logger = NullLogger()
else:
    # Ensure log directory exists only if logging is enabled
    os.makedirs(os.path.dirname(LOG_FILE_PATH_INTERNAL), exist_ok=True)

    # Initialize internal logger
    hestia_internal_logger = logging.getLogger("hestia_internal_logger")
    hestia_internal_logger.setLevel(logging.DEBUG)

    # Define plain text formatter for file logging
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Define colored formatter for console logging
    color_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "black",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )

    # Add rotating file handler for internal log storage to prevent unlimited growth
    file_handler = RotatingFileHandler(
        LOG_FILE_PATH_INTERNAL.replace("main.log", "main_module.log"),
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        delay=True,
        encoding=LOG_FILE_ENCODING,
        errors=LOG_FILE_ENCODING_ERRORS,
    )
    file_handler.setFormatter(file_formatter)
    hestia_internal_logger.addHandler(file_handler)

    # Add console handler for colored terminal logging
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(color_formatter)
    hestia_internal_logger.addHandler(console_handler)

    # Prevent log duplication
    hestia_internal_logger.propagate = False
