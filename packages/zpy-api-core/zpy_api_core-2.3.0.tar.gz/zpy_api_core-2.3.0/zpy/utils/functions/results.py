# Created by Noé Cruz | Zurckz 22 at 12/11/2022
# See https://www.linkedin.com/in/zurckz
from zpy.utils.functions import Result, Ok, Failure


def build(wrap_ok: bool = False):
    def decorator(function):
        def wrapper(*args, **kwargs):
            try:
                result = function(*args, **kwargs)
                if wrap_ok:
                    return Ok.of(result)
                return result
            except Exception as e:
                return Failure.of(e)

        return wrapper

    return decorator
