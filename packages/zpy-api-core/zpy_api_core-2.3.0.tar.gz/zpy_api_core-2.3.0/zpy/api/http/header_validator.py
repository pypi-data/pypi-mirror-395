from typing import Optional, List, Callable, Union
from zpy.api.http.errors import BadRequest
from zpy.utils.objects import ZObjectModel

__author__ = "Noé Cruz | Zurck'z 2021"
__version__ = "1.0.0"


class ZHeader:
    """
    Zurck'z Header Wrapper
    """

    def __init__(self, raw_headers: dict):
        self.headers = raw_headers

    def to_model(self, model: Union[Callable, ZObjectModel]) -> ZObjectModel:
        return model(**self.headers)

    def to_dict(self) -> dict:
        final_headers = self.headers
        return final_headers

    @classmethod
    def from_dict(cls, raw: dict):
        return ZHeader(raw)


def get_headers_or_raise(
    request: dict,
    headers: List[str],
    throw: Optional[bool] = True,
    check_value: Optional[bool] = True,
    include_all: Optional[bool] = False,
) -> ZHeader:
    """
    Check if keys provided as headers are in the headers' dict request
    :param request: headers
    :param throw : Raise exception if some header not found
    :param check_value: Verify header are in request and value is different of null or empty
    :param include_all: return all headers
    :param headers: The headers key to validate
    :return: dict with headers
    """
    validated_headers: dict = {}
    for header in headers:
        header_value: Optional[str] = None
        if header in request:
            header_value = request[header]
            if check_value:
                if header_value is None or header_value.strip() == "" and throw:
                    raise BadRequest(
                        message=f"The value of header: '{header}' cannot be null or empty"
                    )
        elif throw:
            raise BadRequest(message=f"The header: '{header}' is missing")
        validated_headers[header] = header_value

    if include_all:
        request.update(validated_headers)
        return ZHeader.from_dict(request)

    return ZHeader.from_dict(validated_headers)
