from __future__ import absolute_import
from mctech_core import Configure
from fastapi.responses import JSONResponse


def create_info_route(configure: Configure):
    async def info():
        return JSONResponse({
            'app': configure.get_app_info()
        })

    return info
