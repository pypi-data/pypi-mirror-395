# -*- coding: utf-8 -*-
# author: NhanDD3 <hp.duongducnhan@gmail.com>

from .api_app import create_fastapi_api_app
from .api_server import create_fastapi_server_app

__all__ = [
    "create_fastapi_api_app",
    "create_fastapi_server_app",
]
