
from __future__ import absolute_import
from fastapi.responses import JSONResponse
from mctech_core import Configure

from ...health import get_health_manager


def create_health_route(configure: Configure):
    async def health():
        try:
            health = get_health_manager.get_health()
            result = health.__json__()
        except Exception as e:
            result = {
                'status': 'DOWN',
                'error': str(e)
            }
        return JSONResponse(result)
    return health
