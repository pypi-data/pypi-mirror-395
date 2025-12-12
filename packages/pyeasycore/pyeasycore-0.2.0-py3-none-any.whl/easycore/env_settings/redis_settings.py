# -*- coding: utf-8 -*-
from typing import Optional

from pydantic_settings import BaseSettings


class RedisSettings(BaseSettings):
    REDIS_URL: Optional[str] = "mongodb://localhost:27017"
