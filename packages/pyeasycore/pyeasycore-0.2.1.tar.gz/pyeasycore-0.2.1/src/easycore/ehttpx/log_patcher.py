# -*- coding: utf-8 -*-
# author: NhanDD3 <hp.duongducnhan@gmail.com>

import logging
import time


def monkey_patch_httpx(logger: logging.Logger):
    """Monkey patch httpx to log request/response information"""
    try:
        import httpx
    except ImportError:
        logger.warning("httpx is not installed, skipping httpx monkey patch")
        return

    def _wrap_sync_send(original_send):
        def new_send(self, request, *args, **kwargs):
            start_time = time.time_ns()
            has_exc = False
            try:
                response = original_send(self, request, *args, **kwargs)
                return response
            except Exception as e:
                has_exc = True
                logger.exception(
                    f"httpx sync request {request.url} failed: {e}",
                    extra={
                        "req_to_url": str(request.url),
                        "req_to_method": str(request.method),
                        "req_to_headers": str(dict(request.headers)),
                        "resp_from_status": -1,
                        "loc": "core0001",
                    },
                )
                raise
            finally:
                if not has_exc:
                    resp_status = response.status_code if "response" in locals() else 0
                    elapsed_ms = (time.time_ns() - start_time) / 1_000_000
                    logger.info(
                        f"httpx sync request {request.url} {resp_status} {elapsed_ms}ms",
                        extra={
                            "req_to_url": str(request.url),
                            "req_to_method": str(request.method),
                            "req_to_headers": str(dict(request.headers)),
                            "resp_from_status": resp_status,
                            "resp_from_headers": (
                                str(dict(response.headers))
                                if "response" in locals()
                                else ""
                            ),
                            "loc": "core0002",
                        },
                    )

        return new_send

    def _wrap_async_send(original_send):
        async def new_send(self, request, *args, **kwargs):
            start_time = time.time_ns()
            has_exc = False
            try:
                response = await original_send(self, request, *args, **kwargs)
                return response
            except Exception as e:
                has_exc = True
                logger.exception(
                    f"httpx async request {request.url} failed: {e}",
                    extra={
                        "req_to_url": str(request.url),
                        "req_to_method": str(request.method),
                        "req_to_headers": str(dict(request.headers)),
                        "resp_from_status": -1,
                        "loc": "core0003",
                    },
                )
                raise
            finally:
                if not has_exc:
                    resp_status = response.status_code if "response" in locals() else 0
                    elapsed_ms = (time.time_ns() - start_time) / 1_000_000
                    logger.info(
                        f"httpx async request {request.url} {resp_status} {elapsed_ms}ms",
                        extra={
                            "req_to_url": str(request.url),
                            "req_to_method": str(request.method),
                            "req_to_headers": str(dict(request.headers)),
                            "resp_from_status": resp_status,
                            "resp_from_headers": (
                                str(dict(response.headers))
                                if "response" in locals()
                                else ""
                            ),
                            "loc": "core0004",
                        },
                    )

        return new_send

    if not getattr(httpx, "_patched", False):
        httpx.Client.send = _wrap_sync_send(httpx.Client.send)
        httpx.AsyncClient.send = _wrap_async_send(httpx.AsyncClient.send)
        httpx._patched = True
        logger.info(
            "httpx has been monkey patched for logging", extra={"loc": "core0005"}
        )
