# -*- coding: utf-8 -*-
# author: NhanDD3 <hp.duongducnhan@gmail.com>

import logging
import time
from typing import Any
from uuid import uuid4

from fastapi import FastAPI
from starlette.datastructures import MutableHeaders
from starlette.types import Message, Receive, Scope, Send

from .context import get_correlation_id, set_correlation_id
from .log_filter import CorrelationIdFilter, EnsureValidExtraFilter


class RequestLoggingMiddleware:
    def __init__(
        self,
        app: FastAPI,
        header_name: str = "X-Request-ID",
        to_logger: str = "omnichannel-console",
    ):
        self.app = app
        self.header_name = header_name
        self.logger = logging.getLogger(to_logger)
        if not any(isinstance(f, CorrelationIdFilter) for f in self.logger.filters):
            self.logger.addFilter(CorrelationIdFilter())

        if not any(isinstance(f, EnsureValidExtraFilter) for f in self.logger.filters):
            self.logger.addFilter(EnsureValidExtraFilter())

        self._change_uvicorn_fastapi_log_level()

    def _change_uvicorn_fastapi_log_level(self, level: int = logging.ERROR):
        """Change uvicorn and fastapi log level to reduce noise in logs"""
        uvicorn_loggers = ["uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"]
        for logger_name in uvicorn_loggers:
            logger = logging.getLogger(logger_name)
            logger.setLevel(level)

    def _get_client_ip(self, scope: Scope) -> str:
        client = scope.get("client")
        if client:
            return client[0]

        # Check for forwarded headers
        headers = dict(scope.get("headers", []))
        try:
            x_forwarded_for = headers.get(b"x-forwarded-for")
            if x_forwarded_for:
                return x_forwarded_for.decode().split(",")[0].strip()

            x_real_ip = headers.get(b"x-real-ip")
            if x_real_ip:
                return x_real_ip.decode()
            return "unknown"
        except Exception as e:
            return f"unknown-exc-{e}"

    def _get_request_path(self, scope: Scope, with_params: bool = False) -> str:
        path = scope.get("path", "")
        if with_params:
            query_string = scope.get("query_string", b"").decode()
            if query_string:
                return f"{path}?{query_string}"
        return path

    def _get_request_method(self, scope: Scope) -> str:
        return scope.get("method", "unknown")

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> Any:
        """
        Main middleware function to capture request/response data and log it
        """
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        start_time = time.time_ns()
        status_code = 0
        headers = MutableHeaders(scope=scope)
        header_value = headers.get(self.header_name.lower())
        id_value = header_value if header_value else str(uuid4())
        set_correlation_id(id_value)

        em_group_id = headers.get("x-em-group-id")

        async def send_wrapper(message: Message) -> None:
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message.get("status", -1)
                resp_cid = get_correlation_id()
                if resp_cid:
                    message_headers = MutableHeaders(scope=message)
                    message_headers.append(self.header_name, resp_cid)

            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            req_url = self._get_request_path(scope, with_params=True)
            req_resp_time = (time.time_ns() - start_time) / 1_000_000  # in ms
            req_resp_extra = {
                "req_client_ip": self._get_client_ip(scope),
                "req_url": req_url,
                "req_method": self._get_request_method(scope),
                "resp_status": status_code,
                "loc": "core0000",
            }
            if em_group_id:
                req_resp_extra["em_group_id"] = em_group_id

            self.logger.info(
                f"api request {req_url} {status_code} {req_resp_time}ms",
                extra=req_resp_extra,
            )
