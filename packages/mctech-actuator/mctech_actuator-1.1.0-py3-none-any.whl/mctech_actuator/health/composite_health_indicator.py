from __future__ import absolute_import
from typing import Dict, Mapping, Any, List, Optional
from .health import Health, Status
from .indicator import Indicator


class CompositeHealthIndicator(Indicator):
    _indicators: Dict[str, Indicator]
    _health_aggregator: "HealthAggregator"

    def __init__(self, indicators: Optional[Mapping[str, Indicator]] = None):
        self._indicators = dict(indicators) if indicators else {}
        self._health_aggregator = HealthAggregator()

    def add_indicator(self, name: str, indicator):
        self._indicators[name] = indicator

    def health(self) -> Health:
        healths: Dict[str, Health] = {}
        for key, value in self._indicators.items():
            try:
                healths[key] = value.health()
            except Exception as ex:
                healths[key] = Health.unknown("ERROR: " + str(ex)).build()
        return self._health_aggregator.aggregate(healths)

    @property
    def name(self) -> str:
        return "composte"


__STATUS_ORDERS = ['DOWN', 'OUT_OF_SERVICE', 'UP', 'UNKNOWN']


def aggregate_status(candidates: List[Status]):
    # Only sort those status instances that we know about
    filtered_candidates: List[Status] = []
    for candidate in candidates:
        if next(
                filter(lambda code: candidate.code == code, __STATUS_ORDERS),
                None):
            filtered_candidates.append(candidate)

    # If no status is given return UNKNOWN
    if len(filtered_candidates) == 0:
        return Status.UNKNOWN

    if len(filtered_candidates) == 1:
        return filtered_candidates[0]

    # Sort given Status instances by configured order
    filtered_candidates.sort(key=lambda s: __STATUS_ORDERS.index(s.code))
    return filtered_candidates[0]


def aggregate_details(healths: Dict[str, Health]) -> Dict[str, Any]:
    return dict(healths)


class HealthAggregator:
    def aggregate(self, healths: Dict[str, Health]) -> Health:
        status_candidates: List[Status] = []
        for health in healths.values():
            status_candidates.append(health.get_status())
        status = aggregate_status(status_candidates)
        details = aggregate_details(healths)
        return Health.new_builder(status, details).build()
