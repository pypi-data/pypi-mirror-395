"""
HESTIA Logger - Formatters Module.

Defines structured logging formatters for consistency across the logging system.
Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import json
import logging
import datetime
from ..core.config import ENVIRONMENT, HOSTNAME, APP_VERSION


class JSONFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        # Convert the timestamp float to a UTC datetime
        dt = datetime.datetime.fromtimestamp(record.created, datetime.timezone.utc)
        if datefmt:
            # datetime.strftime supports %f (microseconds)
            s = dt.strftime(datefmt)
        else:
            s = dt.isoformat()
        return s

    def format(self, record):
        # 1. Message content extraction
        if isinstance(record.msg, dict):
            message_content = record.msg
        else:
            try:
                parsed = json.loads(record.getMessage())
                message_content = parsed if isinstance(parsed, dict) else {"message": record.getMessage()}
            except (json.JSONDecodeError, TypeError):
                message_content = {"message": record.getMessage()}

        # 2. Build the base log entry
        #    We ask formatTime for "%Y-%m-%dT%H:%M:%S.%fZ", then trim to milliseconds + "Z"
        timestamp = self.formatTime(record, "%Y-%m-%dT%H:%M:%S.%fZ")[:-3] + "Z"
        log_entry = {
            "timestamp":   timestamp,
            "level":       record.levelname,
            "service":     record.name,
            "environment": ENVIRONMENT,
            "hostname":    HOSTNAME,
            "app_version": APP_VERSION,
            "module":      getattr(record, "module", None),
            "filename":    getattr(record, "filename", None),
            "function":    getattr(record, "funcName", None),
            "line":        getattr(record, "lineno", None),
        }

        # 3. Merge in any adapter-provided metadata
        if hasattr(record, "metadata") and isinstance(record.metadata, dict):
            log_entry.update(record.metadata)

        # 4. Merge the message payload
        log_entry.update(message_content)

        # 5. Serialize to JSON (ensure Unicode like emojis is preserved)
        return json.dumps(log_entry, ensure_ascii=False)
