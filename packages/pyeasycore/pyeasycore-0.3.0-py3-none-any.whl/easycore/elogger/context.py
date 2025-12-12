# -*- coding: utf-8 -*-
# author: NhanDD3 <hp.duongducnhan@gmail.com>

# -*- coding: utf-8 -*-
# author: NhanDD3 <hp.duongducnhan@gmail.com>

import threading
from contextvars import ContextVar

ctxv_correlation_id = ContextVar("correlation_id", default=None)
tlocal_correlation_id = threading.local()  # for non-async context, fallback


def set_correlation_id(correlation_id: str):
    """Set correlation ID for the current context (async or thread)."""
    try:
        ctxv_correlation_id.set(correlation_id)
    except Exception:
        pass
    tlocal_correlation_id.correlation_id = correlation_id


def get_correlation_id() -> str:
    """Get correlation ID for the current context (async or thread)."""
    try:
        cid = ctxv_correlation_id.get()
        if cid:
            return cid
    except LookupError:
        pass
    return getattr(tlocal_correlation_id, "correlation_id", None)
