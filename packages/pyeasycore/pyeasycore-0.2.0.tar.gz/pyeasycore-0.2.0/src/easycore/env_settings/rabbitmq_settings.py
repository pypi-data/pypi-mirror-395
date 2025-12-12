# -*- coding: utf-8 -*-
from typing import Optional

from pydantic_settings import BaseSettings


class RabbitMQSettings(BaseSettings):
    RBMQ_URL: Optional[str] = "amqp://username:password@localhost:5672,localhost:5673//"
    RBMQ_CONSUMER_PREFETCH_COUNT: Optional[int] = 20
