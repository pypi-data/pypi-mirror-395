from __future__ import absolute_import
import abc

from typing import Callable, Coroutine, NamedTuple, Any
from fastapi import Response
from .health import Health

MetricEndPoint = Callable[..., Coroutine[Any, Any, Response]]


class Indicator:
    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass

    @abc.abstractmethod
    def health(self) -> Health:
        pass


class MetricIndicator(NamedTuple):
    path: str
    endpoint: MetricEndPoint
