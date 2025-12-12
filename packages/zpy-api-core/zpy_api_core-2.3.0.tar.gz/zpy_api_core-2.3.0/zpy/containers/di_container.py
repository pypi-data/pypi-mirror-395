# Created by Noé Cruz | Zurckz 22 at 01/08/2022
# See https://www.linkedin.com/in/zurckz
from __future__ import annotations

import dataclasses
import time
from typing import Any, Callable, Generic, Optional, TypeVar, overload
from zpy.logger import ZLogger
from zpy.utils.values import if_null_get
from zpy.app import zapp_context as ctx

T = TypeVar("T")


@dataclasses.dataclass
class DLazy(Generic[T]):
    type: type[T]
    initializer: Callable[["DIContainer"], T]


class DIContainer:
    """
    Basic Dependency Container (type-safe)
    Keys are types; values are instances of those types (or DLazy[T] until resolved).
    """

    def __init__(
        self,
        timeit: bool = False,
        x_logger: Optional[ZLogger] = None,
        notifier: Optional[Callable[[Any, Optional[Any]], None]] = None,
    ) -> None:
        # Dict that maps a type to its instance (or a DLazy[T] placeholder)
        self.container: dict[type[Any], Any] = {}
        self.logger: ZLogger = if_null_get(x_logger, ctx().logger)
        self.timeit: bool = timeit
        self.notifier: Optional[Callable[[Any, Optional[Any]], None]] = notifier
        self.throw_ex = True
        self.error_message_prefix = "Fatal"
        self.max_time_allowed = 5

    def with_notifier(self, notifier: Callable[[Any, Optional[Any]], None]) -> None:
        self.notifier = notifier

    @classmethod
    def create(
        cls, timeit: bool = False, logger: Optional[ZLogger] = None
    ) -> "DIContainer":
        return cls(timeit, logger)

    def setup(self, init_fn: Callable[["DIContainer"], None]) -> "DIContainer":
        try:
            te = time.time()
            init_fn(self)
            ts = time.time()
            self.logger.info(
                f"🚀 Dependencies loaded successfully... {(ts - te) * 1000:2.2f} ms."
            )
        except Exception as e:
            self.logger.err("Failed to load dependencies... ☠")
            if self.notifier:
                self.notifier(
                    f"{self.error_message_prefix} - Failed to load dependencies: {str(e)}"
                )
            if self.throw_ex:
                raise
        return self

    # ---------- Registration ----------

    def register(self, x_type: type[T], value: T) -> None:
        """Register an already-created instance."""
        self.container[x_type] = value

    def factory_register(
        self, x_type: type[T], initializer: Callable[["DIContainer"], T]
    ) -> None:
        """
        Register using factory strategy (eager).
        Evaluates and stores the created instance (with optional timing).
        """
        self.container[x_type] = self.__timeit_generic__(
            self.timeit, initializer, x_type, self
        )

    def lazy_register(
        self, x_type: type[T], initializer: Callable[["DIContainer"], T]
    ) -> None:
        """
        Register using lazy strategy (deferred).
        Stores DLazy[T], resolved on first access.
        """
        self.container[x_type] = DLazy[T](x_type, initializer)

    # ---------- Retrieval ----------

    @overload
    def get(self, x_type: type[T]) -> Optional[T]: ...
    @overload
    def get(self, x_type: type[T], default: T) -> T: ...
    @overload
    def get(self, x_type: type[T], default: None) -> Optional[T]: ...

    def get(self, x_type: type[T], default: Optional[T] = None) -> Optional[T]:
        """
        Retrieve object registered under the given type.
        Returns default if not found.
        """
        obj = self.container.get(x_type, default)

        # Resolve lazy
        if isinstance(obj, DLazy):
            # mypy understands obj is DLazy[Any], but we know the concrete T by key
            created = self.__timeit_generic__(
                self.timeit, obj.initializer, x_type, self
            )
            self.container[x_type] = created
            return created  # type: ignore[return-value]

        return obj  # type: ignore[return-value]

    # If you use non-type keys elsewhere, keep this helper. Otherwise, you can drop it.
    def take(
        self, key: Any, x_type: type[T], default: Optional[T] = None
    ) -> Optional[T]:
        return self.get(x_type if key is None else key, default)  # type: ignore[arg-type]

    # Enable bracket syntax: zdi[Foo] -> Foo instance
    @overload
    def __getitem__(self, item: type[T]) -> T: ...
    def __getitem__(self, item: type[T]) -> T:
        value = self.get(item)
        if value is None:
            raise KeyError(f"Type not registered: {item!r}")
        return value

    # Optional: if you truly want attribute fallback (not recommended for typing),
    # you can keep this, but it will be typed as Any.
    # def __getattr__(self, item: str) -> Any:
    #     return self.container.get(item)

    # ---------- Internals ----------

    def __timeit_generic__(
        self,
        timeit: bool,
        fn: Callable[["DIContainer"], T],
        x_type: type[T],
        *args: Any,
    ) -> T:
        if not timeit:
            return fn(self)
        te = time.time()
        result = fn(self)
        ts = time.time()
        taken = ts - te
        self.logger.info(f"Dependency load time: {x_type} :: {taken * 1000:2.2f} ms.")
        if taken >= self.max_time_allowed:
            msg = (
                f"The dependency: {x_type!r} is exceeding the allowed time. "
                f"Taken: {taken:2.2f}s - Max: {self.max_time_allowed}s."
            )
            self.logger.warn(msg)
            if self.notifier:
                self.notifier(msg)
        return result


zdi = DIContainer().create()


# def populate(initializer, container):
#     print(initializer)
#     parameters_name: Tuple[str, ...] = tuple(signature(initializer).parameters.keys())
#     parameters: Tuple[str, ...] = tuple(signature(initializer).parameters.items())
#     print(parameters_name)
#     print(parameters)

#     @wraps(initializer)
#     def _decorated(*args, **kwargs):
#         # all arguments were passed
#         # if len(args) == len(parameters_name):
#         #    return service(*args, **kwargs)

#         # if parameters_name == tuple(kwargs.keys()):
#         #    return service(**kwargs)

#         # all_kwargs = _resolve_kwargs(args, kwargs)
#         return initializer(1, 2, 3)

#     return _decorated


# def inject(container: DIContainer = zdi):
#     def _decorator(_service: Any) -> Any:
#         if isclass(_service):
#             setattr(
#                 _service, "__init__", populate(getattr(_service, "__init__"), container)
#             )
#             return _service

#         return _service

#     return _decorator
