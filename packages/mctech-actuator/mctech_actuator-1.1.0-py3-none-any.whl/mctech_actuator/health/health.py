from __future__ import absolute_import
from typing import Any, Union, Optional, Dict, Mapping


class Status:
    UP = 'UP'
    DOWN = 'DOWN'
    SARTING = 'STARTING'
    OUT_OF_SERVICE = 'OUT_OF_SERVICE'
    UNKNOWN = 'UNKNOWN'

    code: str
    description: Optional[str]

    def __init__(self, code: str, description: Optional[str] = None):
        self.code = code
        self.description = description


HealthStatus = Union[str, Status]


class Health:
    _status: Status
    _details: Dict[str, Any]

    def __init__(self, status: Status, details: Mapping[str, Any]):
        self._status = status
        self._details = dict(details) if details else {}

    def get_status(self) -> Status:
        return self._status

    def get_details(self) -> Mapping[str, Any]:
        return self._details

    def __json__(self):
        json = {
            'status': self._status.code,
            'description': self._status.description
        }

        for key, value in self._details.items():
            if hasattr(value, '__json__'):
                json[key] = value.__json__()
            else:
                json[key] = value
        return json

    @staticmethod
    def unknown(description: Optional[str] = None):
        s = Status(Status.UNKNOWN, description)
        return HealthBuilder(s)

    @staticmethod
    def down(description: Optional[str] = None):
        s = Status(Status.DOWN, description)
        return HealthBuilder(s)

    @staticmethod
    def up(description: Optional[str] = None):
        s = Status(Status.UP, description)
        return HealthBuilder(s)

    @staticmethod
    def out_of_service(description: Optional[str] = None):
        s = Status(Status.OUT_OF_SERVICE, description)
        return HealthBuilder(s)

    @staticmethod
    def status(code: str, description: Optional[str] = None):
        s = Status(code, description)
        return HealthBuilder(s)

    @staticmethod
    def new_builder(status: HealthStatus, details: Optional[Mapping[str, Any]] = None) -> "HealthBuilder":
        return HealthBuilder(status, details)


class HealthBuilder:
    def __init__(self, status: HealthStatus, details: Optional[Mapping[str, Any]] = None):
        self.status(status)
        self._details = dict(details) if details else {}

    def status(self, status: HealthStatus, **kwargs):
        if status:
            if isinstance(status, Status):
                self._status = status
            else:
                description: Optional[str] = kwargs.get('description')
                self._status = Status(status, description)
        return self

    def down(self, message: str):
        self._status = Status(Status.DOWN, message)
        return self

    def add_detail(self, name: str, item: Any):
        self._details[name] = item
        return self

    def build(self):
        return Health(self._status, self._details)
