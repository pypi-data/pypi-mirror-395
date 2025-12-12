from typing import Any, Callable, List, Optional, Tuple, Union
from functools import reduce
import logging
import time
import inspect

from zpy.logger import ZLogger
from zpy.utils.values import if_null_get
from zpy.app import zapp_context as ctx


def safely_exec(callable_fn: Callable, args=None, default_value: Any = None) -> Optional[Any]:
    """
    Execute provided function in try:except block
    @param default_value:
    @param callable_fn:
    @param args:
    @return: value returned of execution or none
    """
    if args is None:
        args = []
    try:
        return callable_fn(*args)
    except Exception as e:
        logging.exception(e)
    return default_value


def safe_exec_wrapper(target: Callable, args=None, kwargs: dict = None,
                      msg: str = None,
                      notifier: Optional[Callable] = None,
                      default_ret=None, throw_ex: bool = False):
    logg = ctx().logger
    if args is None:
        args = []
    if not kwargs:
        kwargs = {}
    try:
        return target(*args, **kwargs)
    except Exception as e:
        msg = if_null_get(msg, f"An error occurred while try execute: {target.__name__} with: {args} and {kwargs}.")
        logg.exception(msg)
        if notifier:
            notifier(f"Fatal: {msg}\n{str(e)}")
        if throw_ex:
            raise
    return default_ret


def exec_if_nt_null(callable_fn: Callable, args: Optional[List[Any]] = None) -> object:
    """
    Execute function if args not null
    """
    if args is None:
        args = []
    for arg in args:
        if arg is None:
            return False
    return callable_fn(*args)


def safely_exec_with(callable_fn: Callable, default_value: Any = None, args=None) -> Optional[Any]:
    """
    Execute provided function in try:except block
    @param default_value:
    @param callable_fn:
    @param args:
    @return: value returned of execution or none
    """
    if args is None:
        args = []
    try:
        return callable_fn(*args)
    except Exception as e:
        logging.exception(e)
    return default_value


def get_class_that_defined_method(meth):
    for cls in inspect.getmro(meth.im_self):
        if meth.__name__ in cls.__dict__:
            return cls
    return None


def timeit(msg: str = None):
    """
    Time execution logger.
    @param msg:
    @return:
    """

    def _timeit_(method):
        def timed(*args, **kw):
            logg = ctx().logger
            ts = time.time()
            result = method(*args, **kw)
            te = time.time()

            method_name = ('{} -> {}'.format(method.__module__, method.__name__)) if not msg else msg
            if 'log_time' in kw:
                name = kw.get('log_name', method.__name__.upper())
                kw['log_time'][name] = int((te - ts) * 1000)
            else:
                logg.info(f"Time Execution: {method_name} :: {(te - ts) * 1000:2.2f} ms.")

            return result

        return timed

    return _timeit_


def safe(default: Any = None, notifier: Any = None, logger: ZLogger = None, err_msg: str = None):
    """
    Safe execution
    @param logger:
    @param err_msg:
    @param notifier: Error notifier
    @param default: if execution fail return default value
    @return:
    """

    def __safe_execution__(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                method_name = ('{} -> {}'.format(func.__module__, func.__name__)) if not err_msg else err_msg
                error_message = f"An error occurred while executing {method_name}. Msg: {str(e)}"
                if notifier:
                    notifier(error_message)
                if logger:
                    logger.exception(error_message, exc_info=e)
            return default

        return wrapper

    return __safe_execution__


def fn_composite(*func):
    """
    Function composition
    @param func: functions
    @return: composition
    """

    def compose(f, g):
        return lambda x: f(g(x))

    return reduce(compose, func, lambda x: x)


def if_then(value: bool, function: Callable, args: Union[List, Tuple] = None, default_value: Any = None):
    """
    If value provided is true, then execute function provided as param.
    @param value:
    @param function:
    @param args:
    @param default_value:
    @return:
    """
    if value:
        return function(*if_null_get(args, []))
    return default_value


def if_get(value: bool, if_value: Any = None, else_value: Any = None, strict=False):
    """
    If value provided is true, then return values provided as param.
    @param strict: Force boolean value to compare
    @param if_value: value returned if value is true
    @param else_value: value returned if value is false
    @param value: value to evaluate
    @return: Any
    """

    if strict is True and value is True:
        return if_value
    if strict is False and value:
        return if_value
    return else_value


def if_not_then(value: bool, function: Callable, args: Union[List, Tuple] = None, default_value: Any = None):
    """
    If value provided is true, then execute function provided as param.
    @param value:
    @param function:
    @param args:
    @param default_value:
    @return:
    """

    if not value:
        return function(*if_null_get(args, []))

    return default_value


def if_else_then(value: bool, if_func: Callable = None, if_args: Union[List, Tuple] = None, else_func: Callable = None,
                 else_args: Union[List, Tuple] = None, if_value: Any = None, else_value: Any = None):
    """
    If value provided is true, then execute if_function provided as param otherwise execute else_function
    @param else_value:
    @param if_value:
    @param else_args:
    @param else_func:
    @param if_args:
    @param value:
    @param if_func:

    @return:
    """

    if value:
        if if_func:
            return if_func(*if_null_get(if_args, []))
        return if_value
    if else_func:
        return else_func(*if_null_get(else_args, []))
    return else_value


class Maybe(object):
    """

    """

    def __init__(self, value) -> None:
        self.value = value
        self.exception = None

    @classmethod
    def unit(cls, value):
        return cls(value)

    def __getattr__(self, item):
        _field = getattr(self.value, item)
        if not callable(_field):
            return self.bind(lambda _: _field)
        return lambda *args, **kwargs: self.bind(lambda _: _field(*args, **kwargs))

    def apply(self, fn):
        if fn is None:
            return self
        fn(self.value)
        return self

    def bind(self, fn):
        if self.value is None:
            return self
        result = fn(self.value)
        if isinstance(result, Maybe):
            return result

        return Maybe.unit(result)

    def safe_bind(self, fn):
        try:
            return self.bind(fn)
        except Exception as e:
            self.exception = e
            return self

    def safe_apply(self, fn):
        try:
            return self.bind(fn)
        except Exception as e:
            self.exception = e
            return self

    def optional_bind(self, fn):
        return self.safe_bind(fn)

    def optional_apply(self, fn):
        return self.safe_apply(fn)

    def unwrap(self) -> Any:
        if self.exception:
            raise self.exception

        return self.value

    def value_or(self, default_value: Any) -> Any:
        return if_null_get(self.value, default_value)
