import importlib
import io
import json
import logging
from pathlib import Path

import pytest
from hestia_logger.core.formatters import JSONFormatter

MODULE_NAME = "hestia_logger.utils.requests_logger"


@pytest.fixture
def fresh_requests_logger(monkeypatch, tmp_path):
    """
    Reload the requests logger module with a temporary LOGS_DIR to
    avoid touching the real filesystem and to make assertions deterministic.
    """
    from hestia_logger.core import config as core_config

    logger = logging.getLogger("hestia_requests")
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        try:
            handler.close()
        except Exception:
            pass

    monkeypatch.setenv("LOGS_DIR", str(tmp_path))
    importlib.reload(core_config)
    module = importlib.import_module(MODULE_NAME)
    module = importlib.reload(module)

    yield module

    for handler in list(module.requests_logger.handlers):
        module.requests_logger.removeHandler(handler)
        try:
            handler.close()
        except Exception:
            pass

    monkeypatch.delenv("LOGS_DIR", raising=False)
    importlib.reload(core_config)
    importlib.reload(module)


def test_requests_logger_output(fresh_requests_logger):
    module = fresh_requests_logger
    logger = module.requests_logger

    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(JSONFormatter())

    previous_handlers = list(logger.handlers)
    for existing in previous_handlers:
        logger.removeHandler(existing)
    logger.addHandler(handler)

    test_message = "Test requests logger message"
    logger.info(test_message)

    handler.flush()
    output = stream.getvalue().strip()

    logger.removeHandler(handler)
    for existing in previous_handlers:
        logger.addHandler(existing)
    stream.close()

    lines = output.splitlines()
    assert len(lines) >= 1, "No log output captured."

    log_entry = json.loads(lines[0])
    assert "timestamp" in log_entry, "Missing 'timestamp' key."
    assert log_entry.get("level") == "INFO", "Incorrect or missing 'level' key."
    assert "service" in log_entry, "Missing 'service' key."

    found = test_message in json.dumps(log_entry)
    assert found, "Test message not found in log entry."


def test_requests_logger_respects_logs_dir(fresh_requests_logger, tmp_path):
    module = fresh_requests_logger
    file_handlers = [
        handler
        for handler in module.requests_logger.handlers
        if isinstance(handler, logging.FileHandler)
    ]
    assert file_handlers, "Expected a file handler on the requests logger."

    for handler in file_handlers:
        assert Path(handler.baseFilename).parent == tmp_path

    log_path = tmp_path / "requests.log"
    assert not log_path.exists()


def test_requests_logger_creates_file_only_after_log(fresh_requests_logger, tmp_path):
    module = fresh_requests_logger
    log_path = tmp_path / "requests.log"

    assert not log_path.exists()
    module.requests_logger.info("first log")

    for handler in module.requests_logger.handlers:
        if hasattr(handler, "flush"):
            handler.flush()

    assert log_path.exists()
