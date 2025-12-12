# -*- coding: utf-8 -*-
# author: NhanDD3 <hp.duongducnhan@gmail.com>

from typing import Optional

from pydantic_settings import BaseSettings


class RedisSettings(BaseSettings):
    REDIS_URL: Optional[str] = "mongodb://localhost:27017"
