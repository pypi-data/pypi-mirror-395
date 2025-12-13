
from __future__ import absolute_import
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from mctech_core import Configure
from .route import create_info_route, create_env_route, create_health_route, create_metrics_routers


def create_actuator_route(configure: Configure, app: FastAPI):
    async def empty():
        res = PlainTextResponse('Actuator Not Found')
        res.status_code = 404
        return res

    management = configure.get_config('management')
    prefix = management.get('context-path') or \
        management.get('contextPath') or '/actuator'

    app.add_api_route(f"{prefix}/info", endpoint=create_info_route(configure))
    app.add_api_route(f"{prefix}/health", endpoint=create_health_route(configure))
    app.add_api_route(f"{prefix}/env", endpoint=create_env_route(configure))
    app.add_api_route(f"{prefix}/shutdown", endpoint=empty)

    app.add_api_route(f"{prefix}/loggers", endpoint=empty)
    app.add_api_route(f"{prefix}/loggers", methods=['head'], endpoint=empty)
    app.add_api_route(f"{prefix}/loggers/:category", endpoint=empty)

    metric_routers = create_metrics_routers(configure)
    for path, endpoint in metric_routers.items():
        app.add_api_route(f"{prefix}/{path}", endpoint=endpoint)


__all__ = [
    "create_actuator_route"
]
