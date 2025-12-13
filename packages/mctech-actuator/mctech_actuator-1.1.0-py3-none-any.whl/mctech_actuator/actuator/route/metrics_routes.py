from __future__ import absolute_import
from typing import Dict
from mctech_core import Configure
from ...health import get_health_manager, MetricEndPoint

METRICS_PATH = '/metrics'


def create_metrics_routers(configure: Configure) -> Dict[str, MetricEndPoint]:
    routers: Dict[str, MetricEndPoint] = {}
    for m in get_health_manager().get_metrics():
        routers[METRICS_PATH + m.path] = m.endpoint
    return routers
