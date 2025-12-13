# tests/middlewares/test_middleware.py

import io
import logging
from pathlib import Path

import pytest

pytest.importorskip("starlette")

from hestia_logger.middlewares.middleware import LoggingMiddleware


# --- Dummy request/response classes --- #


class DummyState:
    request_id = "test-request-id"


class DummyURL:
    def __init__(self, path="/test", query=""):
        self.path = path
        self.query = query

    def __str__(self):
        if self.query:
            return f"http://localhost{self.path}?{self.query}"
        return f"http://localhost{self.path}"


class DummyRequest:
    method = "GET"
    url = DummyURL()
    client = type("Client", (), {"host": "127.0.0.1"})()
    headers = {"user-agent": "pytest", "host": "localhost"}
    state = DummyState()


class DummyResponse:
    status_code = 200


# --- Middleware capture fixture --- #


@pytest.fixture
def capture_middleware_logs(monkeypatch, tmp_path):
    """
    Fixture to capture log output from the LoggingMiddleware.
    It attaches a StreamHandler that writes to an in-memory StringIO.
    """
    monkeypatch.setattr(
        "hestia_logger.middlewares.middleware.LOGS_DIR", str(tmp_path)
    )
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter("%(message)s"))

    middleware = LoggingMiddleware(logger_name="test_middleware")
    middleware.logger.addHandler(handler)

    yield stream, handler, middleware, tmp_path

    middleware.logger.removeHandler(handler)
    stream.close()


# --- Tests --- #


def test_log_request(capture_middleware_logs):
    stream, handler, middleware, _ = capture_middleware_logs
    dummy_request = DummyRequest()
    dummy_request.url = DummyURL(path="/test", query="foo=bar")
    middleware.log_request(dummy_request)
    handler.flush()
    output = stream.getvalue()

    assert "incoming_request" in output
    assert "GET" in output
    assert "/test" in output
    assert "foo=bar" in output
    assert "test-request-id" in output
    assert "127.0.0.1" in output
    assert "'user-agent': 'pytest'" in output
    assert output.count("incoming_request") == 1


def test_log_request_without_request_id(capture_middleware_logs):
    stream, handler, middleware, _ = capture_middleware_logs
    dummy_request = DummyRequest()
    dummy_request.state = type("State", (), {})()  # remove request_id
    dummy_request.client = None
    middleware.log_request(dummy_request)
    handler.flush()
    output = stream.getvalue()

    assert "'request_id': 'unknown'" in output
    assert "'client': 'unknown'" in output


def test_log_response(capture_middleware_logs):
    stream, handler, middleware, _ = capture_middleware_logs
    dummy_request = DummyRequest()
    dummy_response = DummyResponse()

    middleware.log_response(dummy_request, dummy_response)
    handler.flush()
    output = stream.getvalue()

    assert "outgoing_response" in output
    assert "200" in output


def test_middleware_log_file_created_on_first_log(capture_middleware_logs):
    _, _, middleware, logs_dir = capture_middleware_logs
    log_path = Path(logs_dir) / "middleware.log"

    assert not log_path.exists()
    middleware.log_request(DummyRequest())

    for handler in middleware.logger.handlers:
        if isinstance(handler, logging.FileHandler):
            handler.flush()

    assert log_path.exists()
