from typing import Any, List, Callable, Optional, TypeVar

T = TypeVar('T')


def first(collection: List[T], fn: Callable[[T], Any] = None, default: Optional[T] = None) -> T:
    value = collection[0] if collection else default
    return fn(value) if fn and value else value


def last(collection: List[T], fn: Callable[[T], Any] = None, default: Optional[T] = None) -> T:
    value = collection[-1] if collection else default
    return fn(value) if fn and value else value


def find(any_list: List[Any], x_filter: Callable, default_value: Any = None) -> Optional[object]:
    """
    Find item in provided list according filter
    @param default_value: if not found element will be returned
    @param any_list: List of any values
    @param x_filter: Filter to apply the search
    @return: element that filter return true otherwise None
    """
    for x in any_list:
        if x_filter(x):
            return x
    return default_value


def walk_and_apply(dict_value: dict, func: Callable[[str, Any], Any], skip_keys: List[str] = None):
    """
    Iterate over dict and apply function for override value.
    """
    if not skip_keys:
        skip_keys = []

    for k in dict_value.keys():
        if isinstance(dict_value[k], dict):
            walk_and_apply(dict_value[k], func)
            continue
        if k in skip_keys:
            continue
        dict_value[k] = func(k, dict_value[k])
