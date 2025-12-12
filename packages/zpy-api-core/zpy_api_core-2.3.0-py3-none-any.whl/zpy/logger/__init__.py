import logging
import traceback
from abc import ABC, abstractmethod
from enum import Enum
from io import StringIO
from typing import Union, Any, Optional, Callable


class ZLFormat(Enum):
    M = "%(message)s"
    NM = "%(name)s %(message)s"
    LNM = "%(name)s %(levelname)s %(message)s"
    TM = "%(asctime)s %(message)s"
    LM = "%(levelname)s - %(message)s"
    TLM = "%(asctime)s - %(levelname)s - %(message)s"
    TNLM = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def setup_global_logger(log_format: str = ZLFormat.LM.value, level: int = logging.INFO, reset: Optional[bool] = False):
    if reset is True:
        if logging.getLogger().hasHandlers() is True:
            logger = logging.getLogger()
            for h in logger.handlers:
                logger.removeHandler(h)
    logging.basicConfig(format=log_format, level=level)


class ZLogger(ABC):
    """
    Simple Logger
    """

    @classmethod
    @abstractmethod
    def create(cls, name: str):
        ...

    @abstractmethod
    def raw(self, value: Any, shippable: Optional[bool] = False, **kwargs) -> None:
        ...

    @abstractmethod
    def info(self, value: Any, shippable: Optional[bool] = False, **kwargs) -> None:
        ...

    @abstractmethod
    def warn(self, value: Any, shippable: Optional[bool] = False, **kwargs) -> None:
        ...

    @abstractmethod
    def err(self, value: Any, shippable: Optional[bool] = False, **kwargs) -> None:
        ...

    @abstractmethod
    def ex(self, value: Any, shippable: Optional[bool] = False, **kwargs) -> None:
        ...

    @abstractmethod
    def exception(self, value: Any, shippable: Optional[bool] = False, **kwargs) -> None:
        ...

    @abstractmethod
    def release(self, name: Optional[str] = None) -> None:
        ...

    @abstractmethod
    def close(self) -> None:
        ...


class Shippable:

    def __init__(self):
        self.senders = []

    def emit_if(self, value: Any, predicate):
        if predicate:
            self.emit(value)

    def emit(self, value: Any):
        for sender in self.senders:
            sender(value)

    def add_sender(self, sender: Callable[[Any], None]) -> None:
        self.senders.append(sender)


class ZStreamLogger(ZLogger, Shippable):
    """
    Stream Logger
    """

    def __init__(self, name: str, level: int, log_format: Union[str, ZLFormat]) -> None:
        super().__init__()
        self._level = level
        self._name = name
        self._log_format = format if isinstance(format, str) else log_format.value
        self._formatter = logging.Formatter(self._log_format)
        self._logger = None
        self._stream = None
        self._handler = None
        self.release(name)

    @classmethod
    def create(cls, name: str):
        return cls(name, logging.INFO, ZLFormat.TNLM)

    def raw(self, value: Any, shippable: Optional[bool] = False, **kwargs) -> None:
        self._logger.log(self._level, value, **kwargs)

    def info(self, value: Any, shippable: Optional[bool] = False, **kwargs) -> None:
        self._logger.info(value, **kwargs)

    def warn(self, value: Any, shippable: Optional[bool] = False, **kwargs) -> None:
        self._logger.warning(value, **kwargs)

    def err(self, value: Any, shippable: Optional[bool] = False, **kwargs) -> None:
        self._logger.error(value, *kwargs)

    def ex(self, value: Any, shippable: Optional[bool] = False, **kwargs) -> None:
        self._logger.exception(msg=value, **kwargs)

    def exception(self, value: Any, shippable: Optional[bool] = False, **kwargs) -> None:
        self._logger.exception(msg=value, **kwargs)

    def release(self, name: Optional[str] = None) -> None:
        self.close()
        self._logger = logging.getLogger(self._name if not name else name)
        for h in self._logger.handlers:
            self._logger.removeHandler(h)
        self._logger.setLevel(self._level)
        self._stream = StringIO()
        self._handler = logging.StreamHandler(stream=self._stream)
        self._handler.setLevel(self._level)
        self._handler.setFormatter(self._formatter)
        self._logger.addHandler(self._handler)
        self._logger.propagate = False

    def close(self) -> None:
        if self._handler:
            self._handler.flush()
            self._handler.close()
        if self._logger:
            self._logger.removeHandler(self._handler)
        if self._stream:
            self._stream.close()
            self._stream = None

    def str_value(self) -> str:
        return self._stream.getvalue()

    def send(self):
        if self._stream:
            self.emit(self._stream.getvalue())


class zL(ZLogger, Shippable):
    """
    Logger Wrapper
    """

    def __init__(self, name: str, level: int, log_format: Union[str, ZLFormat]) -> None:
        super().__init__()
        self._level = level
        self._name = name
        self._log_format = format if isinstance(format, str) else log_format.value
        self._formatter = logging.Formatter(self._log_format)
        self._logger = None
        self._handler = None
        self.release(name)

    def release(self, name: Optional[str] = None):
        self._logger = logging.getLogger(self._name if not name else name)
        for h in self._logger.handlers:
            self._logger.removeHandler(h)
        self._logger.setLevel(self._level)
        self._handler = logging.StreamHandler()
        self._handler.setLevel(self._level)
        self._handler.setFormatter(self._formatter)
        self._logger.addHandler(self._handler)
        self._logger.propagate = False

    @classmethod
    def create(cls, name: str):
        return cls(name, logging.INFO, ZLFormat.TNLM)

    @classmethod
    def create_for_cloud(cls, name: str):
        return cls(name, logging.INFO, ZLFormat.LM)

    def raw(self, value: Any, shippable: bool = False, *args, **kwargs):
        self.emit_if(value, shippable)
        self._logger.log(self._level, value, *args, **kwargs)

    def info(self, value: Any, shippable: bool = False, **kwargs) -> None:
        self.emit_if(value, shippable)
        self._logger.info(value, **kwargs)

    def warn(self, value: Any, shippable: bool = False, **kwargs) -> None:
        self.emit_if(value, shippable)
        self._logger.warning(value, **kwargs)

    def err(self, value: Any, shippable: bool = False, **kwargs) -> None:
        self.emit_if(value, shippable)
        self.emit_if(traceback.format_exc(), shippable)
        self._logger.error(value, *kwargs)

    def exception(self, value: Any, shippable: bool = False, **kwargs) -> None:
        self.emit_if(value, shippable)
        self.emit_if(traceback.format_exc(), shippable)
        self._logger.exception(msg=value, **kwargs)

    def close(self):
        if self._handler:
            self._handler.flush()
            self._handler.close()
        if self._logger:
            self._logger.removeHandler(self._handler)

    @staticmethod
    def w(msg: object, *args):
        logging.warning(msg=msg, *args)

    @staticmethod
    def i(msg: object, *args):
        """Information Level Log

        Args:
            msg (object): value
        """
        logging.info(msg=msg, *args)

    @staticmethod
    def e(msg: object, exc_info=None, *args):
        """Error Level Log

        Args:
            @param msg:
            @param exc_info:
        """
        logging.error(msg=msg, exc_info=exc_info, *args)

    @staticmethod
    def ex(msg: object, **kwargs):
        """Exception Level Log

        Args:
            @param msg:
        """
        logging.exception(msg=msg, **kwargs)

    @staticmethod
    def d(msg: object, *args):
        """Debug Level Log

        Args:
            msg (object): value
        """
        logging.debug(msg=msg, *args)
