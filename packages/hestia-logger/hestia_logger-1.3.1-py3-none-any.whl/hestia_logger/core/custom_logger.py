"""
HESTIA Logger - Custom Logger.

Defines a structured logger with thread-based asynchronous logging.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import os
import logging
from logging import LoggerAdapter
import queue
import threading
import atexit
from logging.handlers import RotatingFileHandler, QueueHandler

from ..internal_logger import hestia_internal_logger
from ..handlers import console_handler
from ..core.formatters import JSONFormatter
from ..core.config import (
    LOGS_DIR,
    LOG_FILE_PATH_APP,
    LOG_FILE_ENCODING,
    LOG_FILE_ENCODING_ERRORS,
    LOG_LEVEL,
    LOG_ROTATION_TYPE,
    LOG_ROTATION_WHEN,
    LOG_ROTATION_INTERVAL,
    LOG_ROTATION_BACKUP_COUNT,
    LOG_ROTATION_MAX_BYTES,
    ENVIRONMENT,
    HOSTNAME,
    APP_VERSION,
)

ENABLE_INTERNAL_LOGGER = os.getenv("ENABLE_INTERNAL_LOGGER", "true").lower() == "true"

# Ensure previous async workers are stopped if the module is reloaded
for _queue_ref, _thread_ref, _handler_ref in list(globals().get("_ASYNC_WORKERS", [])):
    try:
        _queue_ref.put_nowait(None)
    except Exception:
        pass
    try:
        _thread_ref.join(timeout=1)
    except Exception:
        pass
    try:
        _handler_ref.flush()
        _handler_ref.close()
    except Exception:
        pass

_LOGGERS = {}
_APP_LOG_HANDLER = None
_RESERVED_APP_NAME = "app"
_ASYNC_WORKERS = []
_SERVICE_HANDLERS = {}


def _stop_async_workers():
    for log_queue, worker_thread, handler in _ASYNC_WORKERS:
        try:
            log_queue.put_nowait(None)
        except Exception:
            pass

    for log_queue, worker_thread, handler in _ASYNC_WORKERS:
        try:
            worker_thread.join(timeout=2)
        except Exception:
            pass
        try:
            handler.flush()
            handler.close()
        except Exception:
            pass
    _ASYNC_WORKERS.clear()


atexit.register(_stop_async_workers)


def _ensure_app_handler():
    global _APP_LOG_HANDLER
    if _APP_LOG_HANDLER is None:
        json_formatter = JSONFormatter()
        os.makedirs(os.path.dirname(LOG_FILE_PATH_APP), exist_ok=True)

        app_file_handler = RotatingFileHandler(
            LOG_FILE_PATH_APP,
            maxBytes=LOG_ROTATION_MAX_BYTES,
            backupCount=LOG_ROTATION_BACKUP_COUNT,
            delay=True,
            encoding=LOG_FILE_ENCODING,
            errors=LOG_FILE_ENCODING_ERRORS,
        )
        app_file_handler.setFormatter(json_formatter)
        app_file_handler.setLevel(logging.DEBUG)
        _APP_LOG_HANDLER = _wrap_with_async_queue(app_file_handler)

    app_logger = logging.getLogger("app")
    if _APP_LOG_HANDLER not in app_logger.handlers:
        app_logger.addHandler(_APP_LOG_HANDLER)
    app_logger.setLevel(logging.DEBUG)
    app_logger.propagate = False
    return app_logger


def _create_service_handler(name: str, log_level):
    service_log_file = os.path.join(LOGS_DIR, f"{name}.log")
    os.makedirs(os.path.dirname(service_log_file), exist_ok=True)

    service_file_handler = RotatingFileHandler(
        service_log_file,
        maxBytes=LOG_ROTATION_MAX_BYTES,
        backupCount=LOG_ROTATION_BACKUP_COUNT,
        delay=True,
        encoding=LOG_FILE_ENCODING,
        errors=LOG_FILE_ENCODING_ERRORS,
    )
    service_file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    service_file_handler.setLevel(log_level)
    queue_handler = _wrap_with_async_queue(service_file_handler)
    return queue_handler, service_file_handler


def _initialize_logger(name: str, log_level):
    base_logger = logging.getLogger(name)
    base_logger.setLevel(log_level)
    base_logger.propagate = False

    if name == "app":
        _ensure_app_handler()
        if _APP_LOG_HANDLER not in base_logger.handlers:
            base_logger.addHandler(_APP_LOG_HANDLER)
    else:
        handler, file_handler = _create_service_handler(name, log_level)
        _SERVICE_HANDLERS[name] = (handler, file_handler)
        _ensure_app_handler()
        base_logger.addHandler(handler)
        if _APP_LOG_HANDLER not in base_logger.handlers:
            base_logger.addHandler(_APP_LOG_HANDLER)
    return base_logger


def _ensure_required_handlers(logger: logging.Logger, name: str):
    logger.propagate = False
    if name == "app":
        _ensure_app_handler()
        if _APP_LOG_HANDLER not in logger.handlers:
            logger.addHandler(_APP_LOG_HANDLER)
    else:
        handler_tuple = _SERVICE_HANDLERS.get(name)
        if handler_tuple is None:
            handler_tuple = _create_service_handler(name, logger.level)
            _SERVICE_HANDLERS[name] = handler_tuple
        handler = handler_tuple[0]
        if handler not in logger.handlers:
            logger.addHandler(handler)
        _ensure_app_handler()
        if _APP_LOG_HANDLER not in logger.handlers:
            logger.addHandler(_APP_LOG_HANDLER)


class HestiaLoggerAdapter(LoggerAdapter):
    def log(self, level, msg, *args, **kwargs):
        _ensure_required_handlers(self.logger, self.logger.name)
        super().log(level, msg, *args, **kwargs)


def _wrap_with_async_queue(handler):
    """
    Wraps a synchronous handler with an async queue so logging does not block.
    """
    log_queue = queue.Queue()

    def worker():
        while True:
            record = log_queue.get()
            if record is None:
                log_queue.task_done()
                break
            try:
                handler.handle(record)
            finally:
                log_queue.task_done()

    worker_thread = threading.Thread(target=worker, daemon=True)
    worker_thread.start()
    _ASYNC_WORKERS.append((log_queue, worker_thread, handler))

    queue_handler = QueueHandler(log_queue)
    queue_handler.setLevel(handler.level)

    def flush(self):
        log_queue.join()
        if hasattr(handler, "flush"):
            handler.flush()

    queue_handler.flush = flush.__get__(queue_handler, QueueHandler)
    return queue_handler


def get_logger(name: str, metadata: dict = None, log_level=None, internal=False):
    """
    Returns a structured logger for a specific service/module.
    - Ensures `app.log` is always available internally.
    - Prevents duplicate logger creation.
    """
    global _LOGGERS, _APP_LOG_HANDLER

    if name == _RESERVED_APP_NAME and not internal:
        raise ValueError(
            f'"{_RESERVED_APP_NAME}" is a reserved logger name and cannot be used directly.'
        )

    if name in _LOGGERS:
        adapter = _LOGGERS[name]
        if metadata:
            adapter.extra.setdefault("metadata", {}).update(metadata)
        _ensure_required_handlers(adapter.logger, name)
        adapter.logger.setLevel(log_level or adapter.logger.level)
        return adapter

    log_level = log_level or LOG_LEVEL

    logger = _initialize_logger(name, log_level)

    default_metadata = {
        "environment": ENVIRONMENT,
        "hostname": HOSTNAME,
        "app_version": APP_VERSION,
    }
    if metadata:
        default_metadata.update(metadata)

    adapter = HestiaLoggerAdapter(logger, {"metadata": default_metadata})
    _LOGGERS[name] = adapter
    return adapter


def apply_logging_settings():
    """
    Applies `LOG_LEVEL` settings to all handlers and ensures correct formatting.
    """
    logging.root.handlers = []
    logging.root.setLevel(LOG_LEVEL)
    console_handler.setLevel(LOG_LEVEL)

    color_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(color_formatter)

    logging.root.addHandler(console_handler)

    for handler in logging.root.handlers:
        handler.flush = lambda: handler.stream.flush()

    if hasattr(hestia_internal_logger, "setLevel"):
        hestia_internal_logger.setLevel(LOG_LEVEL)

    if hasattr(hestia_internal_logger, "disabled"):
        hestia_internal_logger.disabled = not ENABLE_INTERNAL_LOGGER

    if hasattr(hestia_internal_logger, "info") and LOG_LEVEL <= logging.INFO:
        hestia_internal_logger.info(f"Applied LOG_LEVEL: {LOG_LEVEL}")
        hestia_internal_logger.info(f"ENABLE_INTERNAL_LOGGER: {ENABLE_INTERNAL_LOGGER}")


apply_logging_settings()
