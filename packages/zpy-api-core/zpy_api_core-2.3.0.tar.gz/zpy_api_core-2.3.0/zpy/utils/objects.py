import json
import typing
from abc import ABC, abstractmethod
from copy import copy
from datetime import datetime, date
from decimal import Decimal
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, NamedTuple, Union

from marshmallow import utils
from marshmallow.fields import Field
from marshmallow_objects import models

from zpy.api.http.errors import BadRequest, ZHttpError
from zpy.utils.funcs import safely_exec
from zpy.utils.values import if_null_get
from dataclasses import dataclass, fields, is_dataclass

__author__ = "Noé Cruz | contactozurckz@gmail.com"
__copyright__ = "Copyright 2021, Small APi Project"
__credits__ = ["Noé Cruz", "Zurck'z"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Noé Cruz"
__email__ = "contactozurckz@gmail.com"
__status__ = "Dev"


# Value Objects
class IntID(NamedTuple):
    """
    Value object to represent an integer id

    Must be an integer value.
    Must be greater than or equal to 0
    """
    value: int

    @staticmethod
    def of(value: int, entity_name: str = '', validator: Optional[Callable[[int], int]] = None,
           allow_zero: bool = False):
        """
        Create new id value object
        @param allow_zero:
        @param value:
        @param entity_name: Entity to which the id belongs
        @param validator: Custom validator
        @return: IntID instance
        """
        if validator is not None:
            return IntID(validator(value))
        value = safely_exec(lambda x: int(value), [value])
        if isinstance(value, int) is False:
            raise BadRequest(f"Invalid value for {entity_name} identifier provided.",
                             "The value of id must be integer.",
                             meta={"value": value})
        if value == 0 and not allow_zero:
            raise BadRequest(f"Invalid value for {entity_name} identifier provided.",
                             "The value of id must be greater than to 0.",
                             meta={"value": value})

        if value < 0:
            raise BadRequest(f"Invalid value for {entity_name} identifier provided.",
                             "The value of id must be greater than or equal to 0.",
                             meta={"value": value})

        return IntID(value)

    @property
    def val(self):
        """
        id value
        @return: int value
        """
        return self.value


class IntValue(NamedTuple):
    """
    Value object to represent an integer id

    Must be an integer value.
    Must be greater than or equal to 0
    """
    value: int

    @staticmethod
    def of(value: Union[int, str], entity_name: str = '', validator: Optional[Callable[[int], int]] = None,
           allow_negative: bool = True):
        """
        Create new id value object
        @param allow_negative:
        @param value:
        @param entity_name: Entity to which the id belongs
        @param validator: Custom validator
        @return: IntID instance
        """
        if validator is not None:
            return IntValue(validator(value))
        value = safely_exec(lambda x: int(value), [value])
        if isinstance(value, int) is False:
            raise BadRequest(f"Invalid value for '{entity_name}' provided.",
                             "The data type of value provided must be integer.",
                             meta={"value": value})
        if not allow_negative and value < 0:
            raise BadRequest(f"Invalid provided value for '{entity_name}'.",
                             "The value must be greater than or equal to 0.",
                             meta={"value": value})

        return IntValue(value)

    @property
    def val(self):
        """
        id value
        @return: int value
        """
        return self.value


def default_remove():
    return [
        "_http_status_",
        "__dump_lock__",
        "__schema__",
        "__missing_fields__",
        "__setattr_func__",
        "_ZObjectModel__remove_keys",
        "_ZObjectModel__update_items",
        "__use_native_dumps__",
        "dump_mode"
    ]


class ZObjectModel(models.Model):
    """
    Zurckz Model
    """

    def __init__(
            self,
            exclude: Optional[List[str]] = None,
            include: Optional[Dict[Any, Any]] = None,
            context=None,
            partial=None,
            use_native_dumps=False,
            **kwargs
    ):
        super().__init__(context=context, partial=partial, **kwargs)
        self.__remove_keys = default_remove() + if_null_get(exclude, [])
        self.__update_items = if_null_get(include, {})
        self.__use_native_dumps__ = use_native_dumps

    def __str__(self):
        """
        Dump nested models by own properties
        """
        data = copy(self.__dict__)
        if self.__update_items is not None:
            data.update(self.__update_items)
        [data.pop(k, None) for k in self.__remove_keys]
        for k in data.keys():
            if isinstance(data[k], models.Model):
                data[k] = json.loads(str(data[k]))
            elif isinstance(data[k], list):
                data[k] = [json.loads(str(it)) for it in data[k]]
            elif isinstance(data[k], datetime) or isinstance(data[k], date):
                data[k] = str(data[k])
            elif isinstance(data[k], Decimal):
                data[k] = float(data[k])
        return json.dumps(data)

    def nat_dump(
            self,
            exclude_keys: Optional[List[str]] = None,
            include: Optional[Dict[Any, Any]] = None,
            mutator: Optional[Callable[[Dict], Dict]] = None,
            map_args: Optional[List[Any]] = None,
            store_ex: bool = False,
            store_in: bool = False
    ):
        """
        Dump object using native strategy
        @param exclude_keys:
        @param include:
        @param mutator:
        @param map_args:
        @param store_ex:
        @param store_in:
        @return:
        """
        return self.sdump(exclude_keys, include, mutator, map_args, store_ex, store_in, True)

    def sdump(
            self,
            exclude_keys: Optional[List[str]] = None,
            include: Optional[Dict[Any, Any]] = None,
            mutator: Optional[Callable[[Dict], Dict]] = None,
            map_args: Optional[List[Any]] = None,
            store_ex: bool = False,
            store_in: bool = False,
            use_native_dumps=False
    ):
        """
        Model dump to json safely, checking the exclude key list

        Use this function instead of zdump.

        Parameters:
        -----------

        exclude_keys: List[str], Optional,
            List of string keys of exlude in dump process
        include: Dict[Any,Any], Optional,
            Object to include in model object after exclude process before of dump process
        mutator: Callable, Optional
            Callable function to tranform object after exclude and include process
        map_args: List[Any], Optional
            Argument list to passed to map callable function
        store_ex: bool, optional
            Indicate that the exclude key added to global model exclude key array
        store_in: bool, optional
            Indicate that the include object added to global model object
        """
        data = copy(self.__dict__)

        if map_args is None:
            map_args = []

        native = use_native_dumps if use_native_dumps is True else self.__use_native_dumps__
        if native is True:
            with self.__dump_mode_on__():
                data = self.__schema__.dump(self)
        temp_exclude = copy(self.__remove_keys)
        if exclude_keys is not None:
            temp_exclude = self.__remove_keys + exclude_keys
            if store_ex:
                self.__remove_keys = self.__remove_keys + exclude_keys
        [data.pop(k, None) for k in temp_exclude]
        temp_include = copy(self.__update_items)
        if include is not None:
            temp_include.update(include)
            data.update(temp_include)
            if store_in:
                self.__update_items.update(include)
        else:
            if temp_include is not None:
                data.update(temp_include)
        if mutator is not None:
            data = mutator(data, *map_args)
        if native is True:
            return data
        # TODO Verify this process when native is False
        for k in data.keys():
            if isinstance(data[k], models.Model):
                data[k] = json.loads(str(data[k]))
            elif isinstance(data[k], list):
                inner_list = []
                for it in data[k]:
                    if isinstance(it, str):
                        inner_list.append(it)
                    else:
                        inner_list.append(json.loads(str(it)))
                data[k] = inner_list
            elif isinstance(data[k], datetime) or isinstance(data[k], date):
                data[k] = str(data[k])
            elif isinstance(data[k], Decimal):
                data[k] = float(data[k])
        return data

    def build(self):
        data = copy(self.__dict__)
        if self.__update_items is not None:
            data.update(self.__update_items)
        [data.pop(k, None) for k in self.__remove_keys]
        return data


class MutatorMode(Enum):
    DESERIALIZATION = "D"
    SERIALIZATION = "S"
    ALL = "*"


class FieldMutator(ABC):
    @abstractmethod
    def exec(self, value: Any) -> Any:
        ...


class ZMutator(FieldMutator):
    def __init__(self, mode: MutatorMode,
                 raise_err: bool = True,
                 error_to_raise: Optional[ZHttpError] = None,
                 error_msg: str = None,
                 cause_msg: str = None,
                 action=None,
                 predicate=None):
        self.mode = mode
        self.error_to_raise = error_to_raise
        self.error_msg = error_msg
        self.cause_msg = "Mutator execution failed" if cause_msg is None else cause_msg
        self.action = action
        self.raise_err = raise_err
        self.predicate = if_null_get(predicate, lambda x: True)
        self.can_run = True

    @classmethod
    def with_serialize(cls, raise_err: bool = True, error_msg: str = None, cause_msg: str = None,
                       action=None, error_to_raise: Optional[ZHttpError] = None, predicate=None):
        """
        Create mutator with serialization mode
        @param predicate:
        @param error_to_raise:
        @param raise_err:
        @param error_msg:
        @param cause_msg:
        @param action:
        @return:
        """
        return cls(MutatorMode.SERIALIZATION, raise_err, error_to_raise, error_msg, cause_msg, action, predicate)

    @classmethod
    def with_deserialize(cls, raise_err: bool = True, error_msg: str = None, cause_msg: str = None,
                         action=None, error_to_raise: Optional[ZHttpError] = None, predicate=None):
        """
        Create mutator with deserialization mode
        @param predicate:
        @param error_to_raise:
        @param raise_err:
        @param error_msg:
        @param cause_msg:
        @param action:
        @return:
        """
        return cls(MutatorMode.DESERIALIZATION, raise_err, error_to_raise, error_msg, cause_msg, action, predicate)

    @classmethod
    def with_all(cls, raise_err: bool = True, error_msg: str = None, cause_msg: str = None,
                 action=None, error_to_raise: Optional[ZHttpError] = None, predicate=None):
        """
        Create mutator with deserialization/serialization mode
        @param predicate:
        @param error_to_raise:
        @param raise_err:
        @param error_msg:
        @param cause_msg:
        @param action:
        @return:
        """
        return cls(MutatorMode.ALL, raise_err, error_to_raise, error_msg, cause_msg, action, predicate)

    def exec(self, value: str) -> str:
        if self.action is not None:
            if self.predicate(value):
                return self.action(value)
        return value


class Str(Field):
    """A string field.

    :param kwargs: The same keyword arguments that :class:`Field` receives.
    """

    #: Default error messages.
    default_error_messages = {
        "invalid": "Not a valid string.",
        "not_empty": "The string value can't be empty or null.",
        "invalid_utf8": "Not a valid utf-8 string.",
    }

    def _serialize(self, value, attr, obj, **kwargs) -> typing.Optional[str]:
        if value is None:
            return None
        return self.__apply_str_mappers(
            utils.ensure_text_type(value), MutatorMode.SERIALIZATION
        )

    def _get_mutators(self, mode: MutatorMode) -> List[ZMutator]:
        if 'mutators' in self.metadata:
            return list(filter(lambda m: m.mode == mode, self.metadata['mutators']))
        return []

    def __apply_str_mappers(self, value: str, mode: MutatorMode) -> str:
        mutators = self._get_mutators(mode)
        mutable_value: str = value
        for mutator in mutators:
            try:
                mutable_value = mutator.exec(mutable_value)
            except Exception as e:
                if mutator.raise_err is True:
                    if mutator.error_to_raise is not None:
                        mutator.error_to_raise.internal_exception = e
                        raise mutator.error_to_raise
                    raise BadRequest(message=mutator.error_msg, reason=mutator.cause_msg, parent_ex=e)
        return mutable_value

    def _deserialize(self, value, attr, data, **kwargs) -> typing.Any:

        if not isinstance(value, (str, bytes)):
            raise self.make_error("invalid")

        if 'allow_empty' in self.metadata and self.metadata['allow_empty'] is False:
            if not value.strip():
                raise self.make_error("not_empty")

        try:
            return self.__apply_str_mappers(
                utils.ensure_text_type(value), MutatorMode.DESERIALIZATION
            )
        except UnicodeDecodeError as error:
            raise self.make_error("invalid_utf8") from error


_T = typing.TypeVar("_T")


class Num(Field):
    """Base class for number fields.

    :param bool as_string: If `True`, format the serialized value as a string.
    :param kwargs: The same keyword arguments that :class:`Field` receives.
    """

    num_type = float  # type: typing.Type

    #: Default error messages.
    default_error_messages = {
        "invalid": "Not a valid number.",
        "too_large": "Number too large.",
    }

    def __init__(self, *, as_string: bool = False, **kwargs):
        self.as_string = as_string
        super().__init__(**kwargs)

    def _format_num(self, value) -> typing.Any:
        """Return the number value for value, given this field's `num_type`."""
        return self.num_type(value)

    def _validated(self, value) -> typing.Optional[_T]:
        """Format the value or raise a :exc:`ValidationError` if an error occurs."""
        if value is None:
            return None
        # (value is True or value is False) is ~5x faster than isinstance(value, bool)
        if value is True or value is False:
            raise self.make_error("invalid", input=value)
        try:
            return self._format_num(value)
        except (TypeError, ValueError) as error:
            raise self.make_error("invalid", input=value) from error
        except OverflowError as error:
            raise self.make_error("too_large", input=value) from error

    def _to_string(self, value) -> str:
        return str(value)

    def _serialize(
            self, value, attr, obj, **kwargs
    ) -> typing.Optional[typing.Union[str, _T]]:
        """Return a string if `self.as_string=True`, otherwise return this field's `num_type`."""
        if value is None:
            return None
        ret = self._format_num(value)  # type: _T
        return self._to_string(ret) if self.as_string else ret

    def _deserialize(self, value, attr, data, **kwargs) -> typing.Optional[_T]:
        return self._validated(value)


# dataclasses extensions
@dataclass
class DefaultValue:
    value: Any


@dataclass
class WithDefaults:
    def __post_init__(self):
        for field in fields(self):
            if isinstance(field.default, DefaultValue):
                field_val = getattr(self, field.name)
                if isinstance(field_val, DefaultValue) or field_val is None:
                    setattr(self, field.name, field.default.value)


def nested_dataclass(*args, **kwargs):
    def wrapper(cls):
        cls = dataclass(cls, **kwargs)
        original_init = cls.__init__

        def __init__(self, *args, **kwargs):
            for name, value in kwargs.items():
                field_type = cls.__annotations__.get(name, None)
                if is_dataclass(field_type) and isinstance(value, dict):
                    new_obj = field_type(**value)
                    kwargs[name] = new_obj
            original_init(self, *args, **kwargs)

        cls.__init__ = __init__
        return cls

    return wrapper(args[0]) if args else wrapper
