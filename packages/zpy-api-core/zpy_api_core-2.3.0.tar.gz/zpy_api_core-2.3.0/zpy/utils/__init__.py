import warnings
from typing import Optional
import os


def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    """Get environment value by key

    Parameters:
        key (str): environment variable name
        default (Optional[str]): default value if environment variable not found

    Returns:
        Optional[str]:Returning environment varibale value or default value
    """

    try:
        value: str = os.getenv(key, default)
        return value if value is not None else default
    except Exception as _:
        return default


def get_env_or_throw(key: str) -> str:
    """Get environment value by key

    Parameters:
        key (str): environment variable name
    Raises:
        RuntimeError: Variable name not found
    Returns:
        str:Returning environment variable value or default value
    """

    if key not in os.environ:
        raise Exception(f"Environment variable '{key}' not found")

    return os.environ[key]


def deprecated(message):
    """
        This is a decorator which can be used to mark functions
        as deprecated. It will result in a warning being emitted
        when the function is used.
    """

    def deprecated_decorator(func):
        def deprecated_func(*args, **kwargs):
            warnings.warn("{} is a deprecated function. {}".format(func.__name__, message),
                          category=DeprecationWarning,
                          stacklevel=2)
            warnings.simplefilter('default', DeprecationWarning)
            return func(*args, **kwargs)

        return deprecated_func

    return deprecated_decorator
