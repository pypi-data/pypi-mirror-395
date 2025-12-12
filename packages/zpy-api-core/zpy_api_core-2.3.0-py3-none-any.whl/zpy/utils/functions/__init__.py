# Created by Noé Cruz | Zurckz 22 at 06/11/2022
# See https://www.linkedin.com/in/zurckz
from typing import TypeVar, Generic, Callable, Any

T = TypeVar('T')
R = TypeVar('R')


class Ok(Generic[T]):
    def __init__(self, value: T, meta=None):
        self.value = value
        self.meta = meta

    @staticmethod
    def of(value: T, meta=None) -> 'Result':
        return Result(Ok(value, meta), Failure.none())

    @classmethod
    def none(cls):
        return cls(None)


class Failure(Generic[T]):

    def __init__(self, value: T, meta=None):
        self.value = value
        self.meta = meta

    @classmethod
    def none(cls):
        return cls(None)

    @staticmethod
    def of(value: T, meta=None) -> 'Result':
        return Result(Ok.none(), Failure(value, meta))


class Result(Generic[T, R]):

    def __init__(self, ok: Ok[T], failure: Failure[R]):
        self.ok = ok
        self.failure = failure

    def unwrap(self, default=None) -> T:
        if self.ok and self.ok.value is not None:
            return self.ok.value
        return default

    def is_ok(self) -> bool:
        return self.ok and self.ok.value is not None

    def unfold(self, ok: Callable[[T], Any], fail: Callable[[R], Any]) -> Any:
        if self.is_ok():
            return ok(self.ok.value)
        return fail(self.failure.value)

    def metadata(self) -> Any:
        if self.is_ok():
            return self.ok.meta
        return self.failure.meta
