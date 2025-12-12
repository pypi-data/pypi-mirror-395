# -*- coding: utf-8 -*-
# author: NhanDD3 <hp.duongducnhan@gmail.com>

from typing import Optional

from pydantic_settings import BaseSettings


class OpenTelemetrySettings(BaseSettings):
    OTEL_ENABLE: Optional[bool] = False
    OTEL_ENDPOINT: Optional[str] = "http://otel-collector-hni01.ftel.scc/v1/traces"
    OTEL_SERVICE_NAME: Optional[str] = "EasyCore"
    OTEL_ENVIRONMENT: Optional[str] = "dev"
