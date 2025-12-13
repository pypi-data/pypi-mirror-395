# test_elasticsearch_handler.py

import json
import logging
import pytest
from hestia_logger.handlers.elasticsearch_handler import ElasticsearchHandler


# Create a dummy Elasticsearch client that records calls to its index method.
class DummyElasticsearch:
    def __init__(self):
        self.calls = []

    def index(self, index, body):
        self.calls.append((index, body))


@pytest.fixture
def dummy_es():
    return DummyElasticsearch()


@pytest.fixture
def es_handler(dummy_es):
    # Instantiate the ElasticsearchHandler with a test index.
    handler = ElasticsearchHandler(index="test-index", log_level=logging.INFO)
    # Override the real Elasticsearch client with our dummy.
    handler.es = dummy_es
    # Set a simple JSON formatter.
    from hestia_logger.core.formatters import JSONFormatter

    handler.setFormatter(JSONFormatter())
    return handler


def test_elasticsearch_handler_emit(es_handler, dummy_es):
    # Create a dummy log record with a dictionary message.
    record = logging.LogRecord(
        name="test_es",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg={"message": "Elasticsearch test", "event": "es_event"},
        args=(),
        exc_info=None,
    )

    # Emit the log record.
    es_handler.emit(record)

    # Verify that the dummy Elasticsearch client's index method was called exactly once.
    assert len(dummy_es.calls) == 1, "Expected one call to dummy_es.index"

    # Unpack the call parameters.
    index_name, body = dummy_es.calls[0]

    # Check that the correct index is used.
    assert index_name == "test-index", "Index name does not match"

    # Verify that the JSON log entry contains the expected fields.
    assert body.get("message") == "Elasticsearch test", "Message content mismatch"
    assert body.get("event") == "es_event", "Event content mismatch"
