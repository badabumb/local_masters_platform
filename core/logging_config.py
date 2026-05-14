import json
import logging
from datetime import datetime


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "timestamp": datetime.utcnow().isoformat(),
            "service": "local_masters_platform",
            "message": record.getMessage(),
        }

        if hasattr(record, "request_id"):
            log_record["request_id"] = record.request_id

        if hasattr(record, "path"):
            log_record["path"] = record.path

        if hasattr(record, "method"):
            log_record["method"] = record.method

        return json.dumps(log_record, ensure_ascii=False)
