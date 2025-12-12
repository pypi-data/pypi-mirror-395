# -*- coding: utf-8 -*-
from typing import Optional

from pydantic_settings import BaseSettings


class MongoDBSettings(BaseSettings):
    MONGO_URL: Optional[str] = "mongodb://localhost:27017"
    MONGO_DB_NAME: Optional[str] = "EasyCore"
