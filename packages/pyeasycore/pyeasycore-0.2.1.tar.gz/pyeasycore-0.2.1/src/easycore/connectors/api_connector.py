# -*- coding: utf-8 -*-
# author: NhanDD3 <hp.duongducnhan@gmail.com>

import asyncio
import logging
from typing import Any, Dict

import httpx

from ..abstractions import SingletonMeta


class BaseAsyncApiConnector(metaclass=SingletonMeta):
    def __init__(
        self, base_url: str, timeout: int = 10, ssl_verify: bool = False, **kwargs
    ):
        self._httpx_client: httpx.AsyncClient = None
        self._base_url = base_url
        self._timeout = timeout
        self._ssl_verify = ssl_verify
        self._logger = kwargs.get("logger", logging.getLogger(__name__))

    def _init_httpx_async_client(self):
        if not self._httpx_client or not isinstance(
            self._httpx_client, httpx.AsyncClient
        ):
            self._httpx_client = httpx.AsyncClient(
                base_url=self._base_url, timeout=self._timeout, verify=self._ssl_verify
            )

    def get_httpx_async_client(self) -> httpx.AsyncClient:
        self._init_httpx_async_client()
        return self._httpx_client

    def close(self):
        if self._httpx_client:
            asyncio.run(self._httpx_client.aclose())
            self._httpx_client = None

    async def _fetch(
        self,
        method: str,
        url: str,
        headers: Dict = {},
        params: Dict = {},
        payload: Any = None,
        files: Any = None,
        auth: Any = None,
        ssl_verify: bool = False,
        **kwargs
    ) -> httpx.Response:
        if not self._httpx_client:
            self._httpx_client = httpx.AsyncClient(
                base_url=self._base_url, timeout=self._timeout, verify=ssl_verify
            )

        response = await self._httpx_client.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=payload,
            files=files,
            auth=auth,
            **kwargs
        )
        response.raise_for_status()
        return response

    async def _fetch_get_json_or_none(
        self,
        url: str,
        headers: Dict = {},
        params: Dict = {},
        auth: Any = None,
        ssl_verify: bool = False,
        **kwargs
    ) -> Any:
        try:
            response = await self._fetch(
                method="GET",
                url=url,
                headers=headers,
                params=params,
                auth=auth,
                ssl_verify=ssl_verify,
                **kwargs
            )

            return response.json()
        except Exception as e:
            raise e
