# -*- coding: utf-8 -*-
import os

from taskiq import AsyncBroker
from taskiq_aio_pika import AioPikaBroker

from .mongo_result_backend import MongoDBResultBackend


def new_taskiq_broker(
    broker_rabbitmq_url: str,
    result_mongo_url: str,
    result_mongo_db: str = "taskiq",
    result_mongo_collection: str = "results",
    broker_qos: int = os.cpu_count(),
    middlewares: list = [],
) -> AioPikaBroker:
    result_backend = MongoDBResultBackend(
        mongo_url=result_mongo_url,
        database_name=result_mongo_db,
        collection_name=result_mongo_collection,
    )

    broker: AsyncBroker = AioPikaBroker(
        url=broker_rabbitmq_url,
        qos=broker_qos,
    ).with_result_backend(result_backend)

    if middlewares:
        broker.add_middlewares(*middlewares)

    return broker
