# Created by Noé Cruz | Zurckz 22 at 22/01/2023
# See https://www.linkedin.com/in/zurckz


from abc import ABC, abstractmethod
from typing import Union, Any, List

from zpy.app.usecase import UseCase


class SdkCommand(ABC):
    pass


class SdkQuery(ABC):
    pass


class SdkClient(ABC):

    @abstractmethod
    def init(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def send(self, command: Union[Any, SdkCommand]) -> Any:
        pass


class CommandFinder:

    def __init__(self, handlers: List[Union[UseCase, Any]]):
        self.commands = {x.command: x for x in handlers}

    def find(self, command: Union[SdkCommand, Any]) -> Any:
        current_command: UseCase[Any, Any] = self.commands.get(command, None)
        if not current_command:
            raise ValueError(f"Command: {str(command)} not found")
        return current_command
