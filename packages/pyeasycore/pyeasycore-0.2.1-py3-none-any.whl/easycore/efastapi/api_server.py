# -*- coding: utf-8 -*-
# author: NhanDD3 <hp.duongducnhan@gmail.com>

from datetime import datetime
from typing import Callable, List, Optional

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from socketio import ASGIApp

default_page = """
    <!DOCTYPE html>
    <html lang="en">
    <body>
        Hello, welcome to {project_name} {service_name}
    </body>
    </html>
"""


def create_fastapi_server_app(
    project_name: str,
    service_name: str,
    service_path: str,
    serivce_port: int,
    api_app: FastAPI,
    ws_enable: bool = False,
    ws_app: Optional[ASGIApp] = None,
    ws_event_handlers_initializer: Optional[Callable] = None,
    startup_events: List[Callable] = [],
    shutdown_events: List[Callable] = [],
):
    app = FastAPI(
        title=project_name,
        description=f"{project_name} {service_name}",
        on_startup=startup_events,
        on_shutdown=shutdown_events,
        docs_url=None,
    )

    # mount api
    app.mount(f"/{service_path}/api", api_app)

    # mount ws
    if ws_enable and ws_app and ws_event_handlers_initializer:
        app.mount(f"/{service_path}/ws", ws_app)
        ws_event_handlers_initializer()

    service_home_page = default_page.format(
        project_name=project_name, service_name=service_name
    )

    @app.get("/", response_class=HTMLResponse)
    async def root():
        return service_home_page

    @app.get(f"/{service_path}", response_class=HTMLResponse)
    async def root_service():
        return service_home_page

    @app.get("/server-info")
    async def traefik_heath_check():
        resp = {
            "status": "running",
            "info": {
                "name": service_name,
                "port": serivce_port,
                "code": "python-fastapi",
            },
            "date": datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
            #  "2022-10-18T04:40:40.207Z"
        }

        return resp

    return app
