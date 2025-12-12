# -*- coding: utf-8 -*-
# author: NhanDD3 <hp.duongducnhan@gmail.com>

import logging
from typing import Dict, List, Optional

from fastapi import APIRouter, FastAPI

logger = logging.getLogger("console")


def create_fastapi_api_app(
    service_name: str,
    service_path: str,
    routers: List[APIRouter],
    custom_exc_handlers: Optional[Dict],
    middlewares: List = [],
    docs_url: str = "/docs",
    openapi_url: str = "/openapi.json",
):
    api_app = FastAPI(
        title=f"Service {service_name}",
        middleware=middlewares,
        docs_url=docs_url,
        openapi_url=openapi_url,
    )

    @api_app.get("/")
    async def root():
        return {"location": f"/{service_path}/api"}

    # add routers
    for x_router in routers:
        if x_router and isinstance(x_router, APIRouter):
            api_app.include_router(x_router)
            continue
        logger.warning(
            f"routers expected an instance of APIRouter but get {type(x_router)}"
        )

    # add exception handlers
    if custom_exc_handlers and isinstance(custom_exc_handlers, dict):
        for exc_class, exc_handler in custom_exc_handlers.items():
            if issubclass(exc_class, Exception) and callable(exc_handler):
                api_app.add_exception_handler(exc_class, exc_handler)
                logger.info(
                    f"add exception handler={exc_handler} for exception {exc_class}"
                )
                continue
            logger.warning(f"unexpected handler {exc_class=} | {custom_exc_handlers=}")

    return api_app
