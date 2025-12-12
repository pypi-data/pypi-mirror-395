# Created by Noé Cruz | Zurckz 22 at 24/09/2022
# See https://www.linkedin.com/in/zurckz
from typing import Any

from zpy.containers.Storable import Storable, UnknownKeyException


class MemoryCacheSystem(Storable):
    """
    Simple cache implementation.
    TODO: Strategies for expiring cache
    """

    def __init__(self):
        self.values = {}

    def clear(self):
        self.values.clear()

    def set(self, key: Any, value: Any):
        self.values[key] = value

    def get(self, key: Any) -> None:
        if key in self.values:
            return self.values[key]
        raise UnknownKeyException(key=key)

    def get_or(self, key: Any, default: Any = None) -> Any:
        return self.values.get(key, default)
