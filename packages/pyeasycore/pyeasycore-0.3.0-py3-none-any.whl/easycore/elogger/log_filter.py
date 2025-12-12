# -*- coding: utf-8 -*-
# author: NhanDD3 <hp.duongducnhan@gmail.com>

import logging
from typing import Any

from .context import get_correlation_id


class CorrelationIdFilter(logging.Filter):
    """Logging filter to attach request/response information to log records"""

    def __init__(self, name: str = "correlation_id"):
        super().__init__(name=name)

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Attach request/response information to the log record.

        This includes correlation ID, request details, response details,
        timing information, and exception details if any.
        """
        # Basic correlation
        record.cid = get_correlation_id()
        return True


class EnsureValidExtraFilter(logging.Filter):
    def __init__(self, name="ensure_valid_extra", strict: bool = False):
        super().__init__(name)
        self.strict = strict
        self.by_pass_keys = {
            "name",
            "msg",
            "args",
            "levelname",
            "levelno",
            "pathname",
            "filename",
            "module",
            "exc_info",
            "exc_text",
            "stack_info",
            "lineno",
            "funcName",
            "created",
            "msecs",
            "relativeCreated",
            "thread",
            "threadName",
            "processName",
            "process",
            "message",
            "asctime",
        }

    def _validate_value(self, value: Any) -> Any:
        """Check kiểu dữ liệu hợp lệ."""
        if isinstance(value, (str, int, float)):
            return value
        elif isinstance(value, dict):
            if all(
                isinstance(k, str) and isinstance(v, (str, int, float))
                for k, v in value.items()
            ):
                return value
        elif isinstance(value, list):
            if all(isinstance(v, (str, int, float)) for v in value):
                return value

        if self.strict:
            raise TypeError(f"Invalid extra value type: {value!r} ({type(value)})")
        return str(value)  # fallback: convert sang string

    def filter(self, record: logging.LogRecord) -> bool:
        if hasattr(record, "__dict__"):
            for k, v in record.__dict__.items():
                if k in self.by_pass_keys:
                    continue
                if v is None or isinstance(v, (str, int, float)):
                    continue
                elif isinstance(v, dict):
                    if all(
                        isinstance(kk, str) and isinstance(vv, (str, int, float))
                        for kk, vv in v.items()
                    ):
                        continue
                    else:
                        record.__dict__[k] = str(v)
                elif isinstance(v, list):
                    if all(isinstance(vv, (str, int, float)) for vv in v):
                        continue
                    else:
                        record.__dict__[k] = str(v)
                else:
                    record.__dict__[k] = str(v)
        return True
