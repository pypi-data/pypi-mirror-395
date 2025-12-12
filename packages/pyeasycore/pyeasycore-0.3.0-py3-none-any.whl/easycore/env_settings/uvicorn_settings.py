# -*- coding: utf-8 -*-
# author: NhanDD3 <hp.duongducnhan@gmail.com>

from typing import Optional

from pydantic_settings import BaseSettings


class UvicornSettings(BaseSettings):
    UVICORN_HOST: Optional[str] = "0.0.0.0"
    UVICORN_PORT: Optional[str] = "5002"
    UVICORN_LOG_LEVEL: Optional[str] = "info"
    UVICORN_RELOAD: Optional[bool] = False
    UVICORN_BIND_PATH: Optional[str] = None
    UVICORN_WORKER_CONCURRENCY: Optional[str] = "2"
    UVICORN_NUMBER_OF_WORKERS: Optional[str] = "2"
    UVICORN_LOOP: Optional[str] = "uvloop"  # "auto", "asyncio", "uvloop"
