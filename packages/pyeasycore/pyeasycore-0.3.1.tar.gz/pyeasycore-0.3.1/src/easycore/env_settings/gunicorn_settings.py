# -*- coding: utf-8 -*-
# author: NhanDD3 <hp.duongducnhan@gmail.com>

from typing import Optional

from pydantic_settings import BaseSettings


class GunicornSettings(BaseSettings):
    GUNICORN_HOST: Optional[str] = "0.0.0.0"
    GUNICORN_PORT: Optional[str] = "5002"
    GUNICORN_BIND_PATH: Optional[str] = None
    GUNICORN_WORKER_CONCURRENCY: Optional[str] = "2"
    GUNICORN_NUMBER_OF_WORKERS: Optional[str] = "2"
