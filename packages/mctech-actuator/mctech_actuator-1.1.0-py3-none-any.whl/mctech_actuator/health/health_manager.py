from __future__ import absolute_import
from typing import List
from .composite_health_indicator import CompositeHealthIndicator
from .indicator import Indicator, MetricIndicator
from .health import Health


class HealthManager:
    def __init__(self):
        self._indicator = CompositeHealthIndicator()
        self._metrics: List[MetricIndicator] = []

    def get_metrics(self) -> List[MetricIndicator]:
        return self._metrics

    def add_metric(self, metric: MetricIndicator):
        self._metrics.append(metric)

    def get_health(self) -> Health:
        return self._indicator.health()

    def add_indicator(self, indicator: Indicator):
        holder = IndicatorHolder(indicator)
        self._indicator.add_indicator(indicator.name, holder)


class IndicatorHolder:
    def __init__(self, indicator):
        self.name = None
        self.indicator = indicator

    def health(self):
        try:
            h = self.indicator.health()
        except BaseException as e:
            h = Health.down(type(e).__name__ + ':' + str(e)).build()
        return h


_manager = HealthManager()


def get_health_manager() -> HealthManager:
    return _manager
