# Created by Noé Cruz | Zurckz 22 at 24/09/2022
# See https://www.linkedin.com/in/zurckz
from abc import ABC, abstractmethod
from typing import Any


class UnknownKeyException(Exception):
    def __init__(self, key: str, message: str = "The provided key does not exist"):
        super().__init__(message)
        self.key = key


class Storable(ABC):
    """
    Simple Storable Definition
    """

    @abstractmethod
    def clear(self):
        """
        Clear all data stored
        @return:
        """
        pass

    @abstractmethod
    def set(self, key: Any, value: Any):
        """
        Store some data by key
        @param key: key for identifier value
        @param value: value to store
        @return: None
        """
        pass

    @abstractmethod
    def get(self, key: Any) -> None:
        """
        Retrieve data by key
        @param key:
        @return:
        """
        pass

    @abstractmethod
    def get_or(self, key: Any, default: Any = None) -> None:
        """
        Retrieve data by key
        @param default:
        @param key:
        @return:
        """
        pass
