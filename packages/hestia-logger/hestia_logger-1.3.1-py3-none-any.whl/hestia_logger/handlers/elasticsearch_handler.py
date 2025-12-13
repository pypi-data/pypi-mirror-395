"""
HESTIA Logger - Elasticsearch Handler.

Provides optional integration with Elasticsearch for centralized logging.

Requires:
- The `elasticsearch` Python package.
- A valid Elasticsearch endpoint in `ELASTICSEARCH_HOST`.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import logging
import json
from ..core.config import ELASTICSEARCH_HOST, LOG_LEVEL
from ..internal_logger import hestia_internal_logger

try:
    from elasticsearch import Elasticsearch

    class ElasticsearchHandler(logging.Handler):
        """
        Elasticsearch log handler that sends structured log events to an Elasticsearch cluster.
        """

        def __init__(self, index="hestia-logs", log_level=logging.INFO):
            super().__init__()
            self.index = index
            self.setLevel(log_level)
            self.es = (
                Elasticsearch([ELASTICSEARCH_HOST]) if ELASTICSEARCH_HOST else None
            )

        def emit(self, record):
            """
            Sends log events to Elasticsearch.
            """
            if not self.es:
                return  # Elasticsearch is disabled

            try:
                log_entry = self.format(record)

                # Ensure valid JSON before sending
                if isinstance(log_entry, str):
                    log_entry = json.loads(log_entry)

                self.es.index(index=self.index, body=log_entry)
                hestia_internal_logger.debug(
                    f"Successfully sent log to Elasticsearch index: {self.index}"
                )
            except Exception as e:
                hestia_internal_logger.error(
                    f"ERROR SENDING LOG TO ELASTICSEARCH: {e}"
                )

    def get_es_handler(index="hestia-logs", log_level=LOG_LEVEL):
        """
        Returns an instance of ElasticsearchHandler if enabled.
        """
        if not ELASTICSEARCH_HOST:
            hestia_internal_logger.warning(
                "Elasticsearch is not configured. Disabling handler."
            )
            return None
        return ElasticsearchHandler(index=index, log_level=log_level)

except ImportError:
    hestia_internal_logger.warning(
        "Elasticsearch package not installed. Disabling Elasticsearch logging."
    )

    def get_es_handler(*args, **kwargs):
        """Returns None if Elasticsearch is unavailable."""
        return None
