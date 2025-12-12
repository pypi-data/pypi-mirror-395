# -*- coding: utf-8 -*-
# author: NhanDD3 <hp.duongducnhan@gmail.com>


__version__ = "0.3.1"


from .abstractions import SingletonMeta
from .connectors import BaseAsyncApiConnector
from .ecelery import create_celery_custom_task_class
from .econnections import RedisClient, new_umongo_instance
from .efastapi import create_fastapi_api_app, create_fastapi_server_app
from .ehttpx import monkey_patch_httpx
from .elogger import (
    CorrelationIdFilter,
    EnsureValidExtraFilter,
    RequestLoggingMiddleware,
    create_json_logger,
    get_correlation_id,
    set_correlation_id,
)
from .env_settings import (
    BaseSettingMixin,
    GunicornSettings,
    MongoDBSettings,
    OpenTelemetrySettings,
    RabbitMQSettings,
    RedisSettings,
    UvicornSettings,
)
from .open_telemetry import setup_open_telemetry

__all__ = [
    "SingletonMeta",
    "BaseAsyncApiConnector",
    "create_celery_custom_task_class",
    "create_fastapi_api_app",
    "create_fastapi_server_app",
    "monkey_patch_httpx",
    "create_json_logger",
    "get_correlation_id",
    "set_correlation_id",
    "RequestLoggingMiddleware",
    "CorrelationIdFilter",
    "EnsureValidExtraFilter",
    "BaseSettingMixin",
    "GunicornSettings",
    "MongoDBSettings",
    "RedisSettings",
    "OpenTelemetrySettings",
    "RabbitMQSettings",
    "UvicornSettings",
    "setup_open_telemetry",
    "new_umongo_instance",
    "RedisClient",
]
