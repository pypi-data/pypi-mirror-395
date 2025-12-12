from enum import Enum
from dataclasses import dataclass
from typing import Tuple, Union


@dataclass
class DynamicHttpStatus:
    value: Tuple[int, str, str]


class HttpMethods(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'
    OPTIONS = 'OPTIONS'


class HttpStatus(Enum):
    """
    Common HTTP status codes

    CODE | SHORT DESCRIPTION | STATUS DETAILS
    """

    SUCCESS                = (200, "SUCCEEDED", "The request has succeeded")
    CREATED                = (201, "CREATED","The request has been fulfilled and resulted in a new resource being created.")
    ACCEPTED               = (202, "ACCEPTED","The request has been accepted for processing, but the processing has not been completed.")
    NO_CONTENT             = (204, "NO CONTENT","The request has been completed successfully but your response has no content, although the headers can be useful.",)
    PARTIAL_CONTENT        = (206, "PARTIAL CONTENT", "Partial content")

    BAD_REQUEST            = (400, "BAD REQUEST","The request could not be understood by the server due to malformed syntax. The client SHOULD NOT repeat the request without modifications.",)
    UNAUTHORIZED           = (401, "UNAUTHORIZED", "The request requires user authentication.")
    FORBIDDEN              = (403, "FORBIDDEN","The server understood the request, but is refusing to fulfill it.")
    NOT_FOUND              = (404, "NOT FOUND","The server has not found anything matching the Request-URI.",)
    METHOD_NOT_ALLOWED     = (405, "METHOD NOT ALLOWED","The method specified in the Request-Line is not allowed for the resource identified by the Request-URI.",)
    CONTENT_NOT_ACCEPTABLE = (406, "METHOD NOT ACCEPTABLE","The resource identified by the request is only capable of generating response entities which have content characteristics not acceptable according to the accept headers sent in the request.",)
    REQUEST_TIMEOUT        = (408, "REQUEST TIMEOUT", "Time out")
    PRE_CONDITION_FAILED   = (412, "PRECONDITION FAILED","The client has indicated preconditions in their headers which the server does not meet.",)
    UNSUPPORTED_MEDIA_TYPE = (415, "UNSUPPORTED MEDIA TYPE","The multimedia format of the requested data is not supported by the server, therefore the server rejects the request.",)
    IM_A_TEAPOT            = (418, "IM A TEAPOT","The server refuses to try to make coffee with a kettle.",)
    CONFLICT               = (409, "CONFLICT", "The server found conflict with request supplied.")
    UNPROCESSABLE          = (422, "UNPROCESSABLE ENTITY","The process could not be completed due to a semantics error.",)
    LOCKED                 = (423, "LOCKED","The source or destination resource of a method is locked.",)

    INTERNAL_SERVER_ERROR  = (500, "INTERNAL SERVER ERROR","The server encountered an unexpected condition which prevented it from fulfilling the request.",)
    NOT_IMPLEMENTED         = (501, "NOT IMPLEMENTED","The server does not support the functionality required to fulfill the request",)
    SERVICE_UNAVAIBLE      = (503, "SERVICE UNAVAIBLE","The server is currently unable to handle the request due to a temporary overloading or maintenance of the server.",)
    GATEWAY_TIMEOUT        = (503, "GATEWAY TIMEOUT", "Timeout")
    LOOP_DETECTED          = (508, "LOOP DETECTED","The server encountered an infinite loop while processing the request. ",)

    @staticmethod
    def dynamic(code: int, status: str, message: str) -> Union['HttpStatus', DynamicHttpStatus]:
        """
        Build custom http status from values
        @param code: http status code
        @param status: status description
        @param message: status message
        @return: DynamicHttpStatus
        """
        return DynamicHttpStatus((code, status, message))
