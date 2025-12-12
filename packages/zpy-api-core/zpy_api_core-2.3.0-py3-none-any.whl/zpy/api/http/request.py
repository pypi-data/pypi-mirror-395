from abc import abstractmethod
from typing import List, Tuple, Union, Any, TypeVar

from marshmallow.exceptions import ValidationError

from zpy.api.http.errors import BadRequest, ZHttpError
from zpy.utils.objects import ZObjectModel

R = TypeVar('R')


class ZRequest:

    @abstractmethod
    def verify(self, *args, **kwargs):
        """
        Execute extra validations over data
        @param args:
        @param kwargs:
        @return:
        """
        pass

    @abstractmethod
    def patch(self, *args, **kwargs):
        """
        Update properties values
        @param args:
        @param kwargs:
        @return:
        """
        pass


def query(queries: dict, name: str, default: Any = None, raise_errors=True, type_data: Any = None):
    """
    Extract query param from dict
    @param queries:
    @param name:
    @param default:
    @param raise_errors:
    @param type_data:
    @return:
    """

    def raise_or_return(msg: str):
        if raise_errors:
            raise BadRequest(reason=msg)
        return default

    if not queries or name not in queries:
        return raise_or_return(f"Missing query param: {name}")
    value = queries.get(name, None)
    if not value:
        return raise_or_return(f"Missing value query param: {name}")
    if type_data and not isinstance(value, type_data):
        return raise_or_return(
            f"Unexpected type data for query param value: {name}. Expected type: {type_data.__name__}")
    return value


def parse_request(
        request: dict, model: Union[R, Any], raise_err: bool = True
) -> Tuple[Union[R, Any], ZHttpError]:
    """
    Parse and validate request according model specification.

    @param request:
    @param model:
    @param raise_err:
    @return:
    """

    model_result: Union[List, ZObjectModel, Any] = None
    errors: Union[List, None, BadRequest] = None
    try:
        if request is None or len(request.items()) == 0:
            error = BadRequest(
                "The request was not provided, validation request error",
                f"Missing fields {model().__missing_fields__} not provided",
            )
            if raise_err:
                raise error
            return None, error
        model_result = model(**request)
    except ValidationError as e:
        model_result = e.valid_data
        # if isinstance(e.messages, Dict):
        #     errors = [e.messages]
        # else:
        #     errors = e.messages
        errors = BadRequest(None, f"{e.messages}")
        if raise_err:
            raise errors
    return model_result, errors
