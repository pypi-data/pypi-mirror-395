# Created by Noé Cruz | Zurckz 22 at 20/09/2022
# See https://www.linkedin.com/in/zurckz
from abc import ABC
from enum import Enum
from time import sleep
from typing import Any, Callable, List

from zpy.logger import ZLogger


class ZBuilder(ABC):

    def update(self, property_name: Any, value: Any):
        setattr(self, str(property_name), value)
        return self


class ZRetryPolicyProp(Enum):
    DELAY = 'delay'  # float: Seconds delay on each attempt
    ATTEMPTS = 'attempts'  # int: Attempts number
    LOG_MSG = 'log_message'  # str: Log error message
    DEFAULT_VALUE = 'default_value'  # Any: Default value to return
    RAISE_EXCEPT = 'raise_except'  # bool: True if raise exceptions
    ENABLE_VERBOSE = 'verbose'  # bool: True if print logs

    def __str__(self) -> str:
        return self.value


class ZRetryPolicyBuilder(ZBuilder):

    def __init__(self, *args, **kwargs) -> None:
        ZBuilder.__init__(self)
        self.delay = 0.0
        self.args = args
        self.kwargs = kwargs
        self.attempts = 1
        self.on_excepts = None
        self.on_results = None
        self.logger = None
        self.log_message = "Failed"
        self.default_value = None
        self.raise_except = False
        self.verbose = True

    def when_excepts(self, excepts: List[Exception]):
        self.on_excepts = excepts
        return self

    def when_results(self, results: List[Any]):
        self.on_results = results
        return self

    def with_logger(self, logger):
        self.logger = logger

    def update(self, property_name: ZRetryPolicyProp, value: Any) -> 'ZRetryPolicyBuilder':
        super().update(property_name, value)
        return self

    def build(self) -> 'ZRetryer':
        return ZRetryer(self)


class ZRetryer:

    def __init__(self, policy: ZRetryPolicyBuilder) -> None:
        self.policy = policy

    def with_default(self, value: Any) -> 'ZRetryer':
        self.policy.default_value = value
        return self

    def with_log_message(self, value: Any) -> 'ZRetryer':
        self.policy.log_message = value
        return self

    def __log_message(self, value: Any):
        if self.policy.verbose is True:
            print(value)

    def call(self, task: Callable[[Any], Any], *args, **kwargs):

        max_attempts = self.policy.attempts
        except_detected = None

        while max_attempts >= 0:
            if max_attempts != self.policy.attempts:
                self.__log_message(
                    "Retrying \'{}(*args)\' function invocation".format(task.__name__))
            try:
                x_result = task(*args, **kwargs)
                if self.policy.on_results and x_result in self.policy.on_results:
                    sleep(self.policy.delay)
                    max_attempts = max_attempts - 1
                    continue
                return x_result
            except Exception as e:
                except_detected = e
                if self.policy.on_excepts and type(e) not in self.policy.on_excepts:
                    return self.policy.default_value
            sleep(self.policy.delay)
            max_attempts = max_attempts - 1
        if except_detected:
            if self.policy.log_message:
                self.__log_message(
                    f"{self.policy.log_message} - [RETRYER] Failed {self.policy.attempts} times.")
            else:
                self.__log_message(
                    f"[RETRYER] Failed {self.policy.attempts} times.")
            if self.policy.raise_except is True:
                raise except_detected
        return self.policy.default_value


def retry(attempts: int = 1, delayed: float = 0.5, on_excepts: List[Exception] = None, on_results: List[Any] = None,
          default_result=None, log_message: str = None, logger: ZLogger = None, raise_except=False) -> Any:
    """
    Function decorator for retry function execution
    @param attempts: Number of attempts to retry.
    @param delayed: Time delay between each attempt
    @param on_excepts: Exceptions list to retry function execution
    @param on_results: Exceptions results to retry function execution
    @param default_result: Default value returned if the function failed
    @param log_message: Message for log
    @param logger: ZLogger instance
    @param raise_except: True if you need raise exception otherwise default value returned
    @return: Function result or default value
    """

    def decorator(fun):
        def wrapper(*args, **kwargs):
            max_attempts = attempts
            except_detected = None
            while max_attempts >= 0:
                if logger and max_attempts != attempts:
                    logger.info("Retrying \'{}(*args)\' function invocation".format(fun.__name__))
                try:
                    result = fun(*args, **kwargs)
                    if on_results and result in on_results:
                        sleep(delayed)
                        max_attempts = max_attempts - 1
                        continue
                    return result
                except Exception as e:
                    except_detected = e
                    if on_excepts and type(e) not in on_excepts:
                        return default_result
                sleep(delayed)
                max_attempts = max_attempts - 1
            if except_detected:
                if log_message and logger:
                    logger.err(f"{log_message} - [RETRYER] Failed {attempts} times.")
                if raise_except is True:
                    raise except_detected
            return default_result

        return wrapper

    return decorator
