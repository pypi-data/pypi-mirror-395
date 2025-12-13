import io
import logging
import threading
import time
from pathlib import Path
import pytest
from logging import LoggerAdapter
from hestia_logger.core.custom_logger import get_logger, apply_logging_settings

# Apply global logger config
apply_logging_settings()


@pytest.fixture
def capture_stream():
    """Fixture to capture log output using an in-memory stream."""
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setLevel(logging.DEBUG)  # Required for visible output
    yield stream, handler
    stream.close()


import os
import tempfile


import os
import tempfile
import importlib
import pytest
from logging import LoggerAdapter


def test_get_logger_creates_adapter(monkeypatch):
    # Set LOGS_DIR to a temporary writable location
    tmp_log_dir = tempfile.mkdtemp()
    monkeypatch.setenv("LOGS_DIR", tmp_log_dir)

    # Reload config first to pick up new LOGS_DIR
    from hestia_logger.core import config

    importlib.reload(config)

    # Now reload the logger module that depends on config
    from hestia_logger.core import custom_logger

    importlib.reload(custom_logger)

    logger = custom_logger.get_logger(
        "test_service", metadata={"custom_key": "custom_value"}
    )

    assert isinstance(logger, LoggerAdapter)
    assert "metadata" in logger.extra
    assert logger.extra["metadata"].get("custom_key") == "custom_value"


def test_get_logger_duplicate():
    logger1 = get_logger("dup_service")
    logger2 = get_logger("dup_service")
    assert logger1 is logger2


def test_get_logger_app_reserved():
    with pytest.raises(ValueError):
        get_logger("app")


def test_logger_output(capture_stream):
    stream, handler = capture_stream
    logger = get_logger("output_test")
    logger.logger.setLevel(logging.DEBUG)
    logger.logger.addHandler(handler)

    test_message = "Hello, logging test"
    logger.info(test_message)
    handler.flush()

    output = stream.getvalue()
    assert test_message in output

    logger.logger.removeHandler(handler)


def _wait_for_file(path, timeout=1.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if path.exists():
            return True
        time.sleep(0.05)
    return path.exists()


def test_lazy_file_creation(monkeypatch, tmp_path):
    import importlib
    from hestia_logger.core import config as core_config
    from hestia_logger.core import custom_logger as core_custom_logger

    monkeypatch.setenv("LOGS_DIR", str(tmp_path))
    importlib.reload(core_config)
    custom_logger = importlib.reload(core_custom_logger)

    logger = custom_logger.get_logger("lazy_service")
    log_dir = Path(core_config.LOGS_DIR)
    service_log = log_dir / "lazy_service.log"
    app_log = log_dir / "app.log"

    assert not service_log.exists()
    assert not app_log.exists()

    logger.info("trigger write")
    for handler in logger.logger.handlers:
        if hasattr(handler, "flush"):
            handler.flush()

    assert _wait_for_file(service_log)
    assert _wait_for_file(app_log)

    monkeypatch.delenv("LOGS_DIR", raising=False)
    importlib.reload(core_config)
    importlib.reload(core_custom_logger)


def test_logger_thread_safety(monkeypatch, tmp_path):
    import importlib
    from hestia_logger.core import config as core_config
    from hestia_logger.core import custom_logger as core_custom_logger

    monkeypatch.setenv("LOGS_DIR", str(tmp_path))
    importlib.reload(core_config)
    custom_logger = importlib.reload(core_custom_logger)

    logger = custom_logger.get_logger("concurrent_service")
    log_dir = Path(core_config.LOGS_DIR)

    def worker(idx):
        for i in range(20):
            logger.info(f"worker-{idx}-message-{i}")

    threads = []
    for idx in range(5):
        thread = threading.Thread(target=worker, args=(idx,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    for handler in logger.logger.handlers:
        if hasattr(handler, "flush"):
            handler.flush()

    service_log = log_dir / "concurrent_service.log"
    assert _wait_for_file(service_log)
    with open(service_log, "r", encoding="utf-8") as f:
        lines = f.readlines()

    assert len(lines) == 100

    monkeypatch.delenv("LOGS_DIR", raising=False)
    importlib.reload(core_config)
    importlib.reload(core_custom_logger)
