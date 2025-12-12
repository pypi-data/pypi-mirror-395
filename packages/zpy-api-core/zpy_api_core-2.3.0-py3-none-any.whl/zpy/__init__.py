from enum import Enum


class EnvironmentKeys(Enum):
    ENVIRONMENT = 'ENVIRONMENT'

    def __str__(self) -> str:
        return self.value
