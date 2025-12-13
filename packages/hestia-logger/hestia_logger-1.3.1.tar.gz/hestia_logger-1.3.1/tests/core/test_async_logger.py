# test_async_logger.py

import asyncio
import json
import logging
import pytest
from hestia_logger.core.async_logger import AsyncFileLogger
from hestia_logger.core.formatters import JSONFormatter


@pytest.mark.asyncio
async def test_async_file_logger(tmp_path):
    # Create a temporary log file path
    log_file = tmp_path / "test_async.log"

    # Initialize the AsyncFileLogger with the temporary file
    handler = AsyncFileLogger(str(log_file))
    formatter = JSONFormatter()
    handler.setFormatter(formatter)

    # Create a dummy log record with a dictionary as the message
    record = logging.LogRecord(
        name="test_async",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg={"message": "Async test", "event": "async_event"},
        args=(),
        exc_info=None,
    )

    # Emit the log record asynchronously.
    handler.emit(record)

    # Allow some time for the async write to complete.
    await asyncio.sleep(0.5)

    # Read and verify the content of the log file.
    with open(log_file, "r", encoding="utf-8") as f:
        lines = f.read().strip().splitlines()

    # There should be at least one log entry.
    assert len(lines) >= 1

    # Parse the first log entry from JSON.
    log_entry = json.loads(lines[0])

    # Check that the standardized keys and message content are present.
    assert "timestamp" in log_entry
    assert log_entry["level"] == "INFO"
    assert log_entry["service"] == "test_async"
    assert log_entry["message"] == "Async test"
    assert log_entry["event"] == "async_event"
