"""
HESTIA Logger - Threaded Async File Handlers.

Implements non-blocking file logging using a background worker thread.
Ensures high-performance, structured logging for ELK and human-readable logs.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import logging
import threading
import queue
import os
import json
from ..core.config import LOG_FILE_PATH_APP, LOG_LEVEL
from ..internal_logger import hestia_internal_logger

# Ensure log directory exists
os.makedirs(os.path.dirname(LOG_FILE_PATH_APP), exist_ok=True)


class ThreadedFileHandler(logging.Handler):
    """
    A threaded file handler that writes logs asynchronously in the background.
    """

    def __init__(self, log_file, formatter):
        super().__init__()
        self.log_file = log_file
        self.log_queue = queue.Queue()
        self.formatter = formatter
        self._stop_event = threading.Event()

        # Start the background thread
        self.worker_thread = threading.Thread(target=self._process_logs, daemon=True)
        self.worker_thread.start()
        hestia_internal_logger.info(f"Started threaded log writer for {self.log_file}")

    def _process_logs(self):
        """
        Continuously processes log records from the queue and writes them to the file.
        """
        while not self._stop_event.is_set():
            try:
                record = self.log_queue.get(timeout=1)
                log_entry = self.format(record)

                # Explicitly write and flush to disk
                with open(self.log_file, mode="a", encoding="utf-8") as f:
                    f.write(log_entry + "\n")
                    f.flush()  # Ensure logs are immediately written to disk

                hestia_internal_logger.debug(
                    f"Successfully wrote log to {self.log_file}."
                )

            except queue.Empty:
                continue  # No logs in queue, loop again
            except Exception as e:
                hestia_internal_logger.error(f"Error writing to {self.log_file}: {e}")

    def emit(self, record):
        """
        Adds formatted log records to the queue for background writing.
        """
        try:
            self.log_queue.put_nowait(record)
        except queue.Full:
            hestia_internal_logger.warning(
                f"Log queue is full! Dropping log: {record.getMessage()}"
            )

    def stop(self):
        """
        Gracefully stops the logging thread.
        """
        self._stop_event.set()
        self.worker_thread.join()
        hestia_internal_logger.info(f"Stopped threaded log writer for {self.log_file}")


# Define structured formatter for JSON logs
json_formatter = logging.Formatter(
    '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
)

# Create threaded file handler only for `app.log`
file_handler_app = ThreadedFileHandler(
    LOG_FILE_PATH_APP, json_formatter
)  # JSON format for ELK

# Apply `LOG_LEVEL` to handlers
file_handler_app.setLevel(LOG_LEVEL)
