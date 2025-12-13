# test_internal_logger.py

import io
import logging
import pytest
from hestia_logger.internal_logger import hestia_internal_logger


def test_internal_logger_configuration():
    """
    Verify that if internal logging is enabled, the logger is a logging.Logger
    with expected settings; otherwise, if it's a NullLogger, calling its methods
    doesn't raise exceptions.
    """
    if isinstance(hestia_internal_logger, logging.Logger):
        # Check that the logger's level is DEBUG and propagation is disabled.
        assert (
            hestia_internal_logger.level == logging.DEBUG
        ), "Internal logger level is not DEBUG"
        assert (
            hestia_internal_logger.propagate is False
        ), "Internal logger should not propagate"
        # Verify that it has at least one handler attached (e.g. file or console handler).
        assert (
            len(hestia_internal_logger.handlers) > 0
        ), "Internal logger should have handlers when enabled"
    else:
        # For NullLogger, simply ensure that logging methods don't raise exceptions.
        try:
            hestia_internal_logger.debug("Test message")
            hestia_internal_logger.info("Test message")
            hestia_internal_logger.warning("Test message")
            hestia_internal_logger.error("Test message")
            hestia_internal_logger.critical("Test message")
        except Exception as e:
            pytest.fail(f"NullLogger methods raised an exception: {e}")


def test_internal_logger_output_capture():
    """
    If internal logging is enabled, attach a temporary StreamHandler to capture
    log output, then verify that a test log message appears in the captured output.
    """
    if isinstance(hestia_internal_logger, logging.Logger):
        stream = io.StringIO()
        handler = logging.StreamHandler(stream)
        handler.setFormatter(logging.Formatter("%(message)s"))
        hestia_internal_logger.addHandler(handler)

        test_message = "Internal log test"
        hestia_internal_logger.info(test_message)
        handler.flush()
        output = stream.getvalue()

        # Check that our test message is present in the output.
        assert (
            test_message in output
        ), "Test message not found in internal logger output"

        # Clean up by removing the temporary handler.
        hestia_internal_logger.removeHandler(handler)
        stream.close()
    else:
        pytest.skip("Internal logger is disabled (NullLogger)")
