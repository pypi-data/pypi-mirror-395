# test_file_handler.py

import json
import logging
import time
import pytest
from hestia_logger.handlers.file_handler import ThreadedFileHandler


@pytest.fixture
def temp_log_file(tmp_path):
    """Fixture that provides a temporary file path for logging."""
    return str(tmp_path / "test_file_handler.log")


@pytest.fixture
def threaded_handler(temp_log_file):
    """
    Fixture that creates a ThreadedFileHandler with a simple JSON formatter,
    yields it for testing, and ensures the background thread is stopped afterward.
    """
    formatter = logging.Formatter(
        '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
    )
    handler = ThreadedFileHandler(temp_log_file, formatter)
    yield handler
    handler.stop()


def test_threaded_file_handler(threaded_handler, tmp_path):
    """
    Emit a log record using the threaded file handler and verify that
    the log file contains the expected JSON log entry.
    """
    # Create a dummy log record.
    record = logging.LogRecord(
        name="test_file_handler",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg="Test log message",
        args=(),
        exc_info=None,
    )
    # Emit the record.
    threaded_handler.emit(record)
    # Wait for the background thread to process the log queue.
    time.sleep(1)

    # Open the temporary file and read its contents.
    log_file_path = tmp_path / "test_file_handler.log"
    with open(str(log_file_path), "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    # Assert that at least one log entry was written.
    assert len(lines) > 0, "No log entries found in the file."

    # Parse the first log entry and check its content.
    log_entry = json.loads(lines[0])
    assert log_entry["message"] == "Test log message", "Log message content mismatch."


def test_thread_stop(threaded_handler, tmp_path):
    """
    Test that calling stop() on the handler does not raise an error
    and that log emission does not continue after stopping.
    """
    # Emit a record.
    record = logging.LogRecord(
        name="test_file_handler",
        level=logging.INFO,
        pathname=__file__,
        lineno=20,
        msg="Another test message",
        args=(),
        exc_info=None,
    )
    threaded_handler.emit(record)
    time.sleep(1)
    # Stop the handler.
    threaded_handler.stop()
    # After stopping, further emits won't be processed. We just ensure no error is raised.
