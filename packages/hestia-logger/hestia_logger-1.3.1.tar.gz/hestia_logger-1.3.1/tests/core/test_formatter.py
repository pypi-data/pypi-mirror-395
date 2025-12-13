# test_json_formatter.py

import json
import logging
import pytest
from hestia_logger.core.formatters import JSONFormatter


@pytest.fixture
def log_record_dict():
    """Create a LogRecord with a dictionary as its message."""
    record = logging.LogRecord(
        name="test_service",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        func="dict_test",
        msg={"message": "Test log", "event": "unit_test"},
        args=(),
        exc_info=None,
    )
    return record


@pytest.fixture
def log_record_string():
    """Create a LogRecord with a JSON string as its message."""
    record = logging.LogRecord(
        name="test_service",
        level=logging.WARNING,
        pathname=__file__,
        lineno=20,
        func="string_test",
        msg='{"message": "Another test", "event": "string_test"}',
        args=(),
        exc_info=None,
    )
    return record


def test_json_formatter_with_dict(log_record_dict):
    formatter = JSONFormatter()
    formatted = formatter.format(log_record_dict)
    log_json = json.loads(formatted)

    # Verify standardized keys
    assert "timestamp" in log_json, "Missing timestamp"
    assert log_json["level"] == "INFO", "Incorrect log level"
    assert log_json["service"] == "test_service", "Incorrect service name"
    assert log_json["filename"].endswith("test_formatter.py")
    assert log_json["line"] == 10
    assert log_json["function"] == "dict_test"
    # Verify merged message content
    assert log_json["message"] == "Test log", "Incorrect message content"
    assert log_json["event"] == "unit_test", "Incorrect event content"


def test_json_formatter_with_string(log_record_string):
    formatter = JSONFormatter()
    formatted = formatter.format(log_record_string)
    log_json = json.loads(formatted)

    # Verify standardized keys
    assert "timestamp" in log_json, "Missing timestamp"
    assert log_json["level"] == "WARNING", "Incorrect log level"
    assert log_json["service"] == "test_service", "Incorrect service name"
    assert log_json["filename"].endswith("test_formatter.py")
    assert log_json["line"] == 20
    assert log_json["function"] == "string_test"
    # Verify that the JSON string was parsed correctly
    assert log_json["message"] == "Another test", "Incorrect message content"
    assert log_json["event"] == "string_test", "Incorrect event content"
