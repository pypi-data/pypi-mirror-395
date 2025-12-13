"""
HESTIA Logger - Async Logger.

Provides a non-blocking file handler that writes log records on a
background thread. This handler is useful for optional async use cases
that cannot rely on the default thread-based handlers.
"""

import logging
import json
import queue
import threading

from ..internal_logger import hestia_internal_logger
from ..core.custom_logger import JSONFormatter

__all__ = ["AsyncFileLogger"]


class AsyncFileLogger(logging.Handler):
    """
    Asynchronous file logger backed by a worker thread.
    """

    def __init__(self, log_file: str):
        super().__init__()
        self.log_file = log_file
        self.formatter = JSONFormatter()
        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._worker = threading.Thread(target=self._process_logs, daemon=True)
        self._worker.start()

    def _process_logs(self):
        while not self._stop_event.is_set():
            try:
                record = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            if record is None:
                self._queue.task_done()
                break

            try:
                log_entry = self.format(record)
                if isinstance(log_entry, str):
                    log_entry = json.loads(log_entry)
                message = json.dumps(log_entry, ensure_ascii=False)
                with open(self.log_file, mode="a", encoding="utf-8") as f:
                    f.write(message + "\n")
                    f.flush()
            except Exception as e:  # pragma: no cover - best effort logging
                hestia_internal_logger.error(
                    f"ERROR WRITING TO FILE {self.log_file}: {e}"
                )
            finally:
                self._queue.task_done()

    def emit(self, record):
        try:
            self._queue.put_nowait(record)
        except queue.Full:
            hestia_internal_logger.warning(
                f"AsyncFileLogger queue full, dropping log for {self.log_file}"
            )

    def flush(self):
        self._queue.join()

    def close(self):
        try:
            self._stop_event.set()
            self._queue.put_nowait(None)
            self._worker.join(timeout=1)
        except Exception:
            pass
        super().close()
