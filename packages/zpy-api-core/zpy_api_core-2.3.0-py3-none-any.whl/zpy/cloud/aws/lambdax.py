# Created by Noé Cruz | Zurckz 22 at 20/03/2022
# See https://www.linkedin.com/in/zurckz
import dataclasses
import json
from typing import Callable, Optional, Any, Union, Tuple, Dict

from zpy.api.http.errors import ZHttpError
from zpy.api.http.status_codes import HttpStatus
from zpy.app import zapp_context as ctx


class LambdaEventHandler(object):
    """
    Lambda event handler
    """
    _DEFAULT_ERR_MSG = 'An error occurred while processing event data'
    CORS_HEADERS = {
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST"
    }

    def __init__(self, processor: Optional[Callable[[dict, Any], Any]], strict=False, verbose: bool = False,
                 jsonfy=True, signal_processor: Optional[Callable[[dict, Any], Any]] = None,
                 on_before: Optional[Callable[[dict, Any], Tuple[Dict, Any]]] = None,
                 on_after: Optional[Callable[[dict], Dict]] = None):
        self.processor = processor
        self.strict = strict
        self.verbose = verbose
        self.jsonfy = jsonfy
        self.request_parser = None
        self.response_builder = None
        self.error_notifier = None
        self.send_str_exception = True
        self.starting_process_logger = None
        self.common_fatal_error_msg = f'Fatal :: {self._DEFAULT_ERR_MSG}'
        self.signal_processor = signal_processor
        self.signal_event_key = 'zpy_event_action'
        self.on_before = on_before
        self.on_after = on_after
        self.before: Optional[Callable[[], None]] = None
        self.after: Optional[Callable[[], None]] = None

    def configure(self, response_builder: Callable[[Any, Any], Any] = None,
                  request_parser: Callable[[Any, Any], Any] = None,
                  error_notifier: Callable[[Any, Any], None] = None, send_str_exception: bool = True,
                  starting_process_logger: Callable[[Any, Any], None] = None,
                  common_error_msg: str = None) -> 'LambdaEventHandler':
        self.response_builder = response_builder
        self.request_parser = request_parser
        self.error_notifier = error_notifier
        self.send_str_exception = send_str_exception
        self.starting_process_logger = starting_process_logger
        self.configure_error_msg(self._DEFAULT_ERR_MSG if common_error_msg is None else common_error_msg)
        return self

    def configure_error_msg(self, msg: str) -> None:
        self.common_fatal_error_msg = f'Fatal :: {msg}'

    @classmethod
    def of(cls, processor: Optional[Callable[[dict, dict], Any]], strict=False, verbose=False, jsonfy=True):
        return cls(processor, strict, verbose, jsonfy)

    @staticmethod
    def proxy(event, context, handler):
        return handler.run(event, context)

    def __notify_error(self, record, msg):
        if self.error_notifier:
            self.error_notifier(record, msg)

    def is_wake_up_signal(self, record: dict):
        if not record:
            return False
        prop_key = record.get(self.signal_event_key, None)
        return prop_key == 'WakeUpSignal'

    def run(self, event, context) -> Any:
        logger = ctx().logger
        result = None
        try:
            if self.on_before:
                e, c = self.on_before(event, context)
                event = e
                context = context
            if self.before:
                self.before()

            if self.request_parser:
                event = self.request_parser(event, context)

            if not self.processor:
                msg = "The lambda event processor cant be null."
                self.__notify_error(event, msg)
                return msg
            if type(event) is not dict:
                if self.jsonfy:
                    event = json.loads(event)

            if self.verbose:
                logger.info(f"Starting event processing with data: {event}")
            if self.starting_process_logger:
                self.starting_process_logger(event, context)

            if self.is_wake_up_signal(event):
                result = "Wake up signal received successfully"
                if self.signal_processor:
                    result = self.signal_processor(event, context)
            else:
                result = self.processor(event, context)
            if self.verbose:
                logger.info(result)
        except Exception as e:
            logger.exception("An error occurred processing event", exc_info=e)
            self.__notify_error(event, str(e))
        if self.on_after:
            try:
                result = self.on_after(result)
            except Exception as e:
                logger.exception("An error occurred execute on after hook", exc_info=e)
        if self.after:
            try:
                self.after()
            except Exception as e:
                logger.exception("An error occurred execute on simple after hook", exc_info=e)
        return {"results": result}


@dataclasses.dataclass
class LambdaEventResult(object):
    status: HttpStatus
    payload: dict
    success: bool
    event: str

    def __init__(self, code: HttpStatus, payload: dict, success: bool, event: str = None):
        self.status = code
        self.payload = payload
        self.success = success
        self.event = event


@dataclasses.dataclass
class SuccessEventResult(LambdaEventResult):

    def __init__(self, payload: Union[dict, Any], status: HttpStatus = HttpStatus.SUCCESS):
        LambdaEventResult.__init__(self, status, payload, True, None)


def build_response(status: HttpStatus, payload: dict, success: bool, message: str = None, reason: str = None):
    return {
        "status": {
            "code": status.value[0],
            "message": message if message else status.value[2],
            "details": [reason] if reason else None,
            "status": status.value[1]
        },
        "payload": json.dumps(payload),
        "success": success
    }


def lambda_response(default_status: HttpStatus = HttpStatus.SUCCESS, notifier: Callable[[str], None] = None,
                    raise_exc=False):
    """
    HTTP Response builder, build response from data provided
    @return: None

    @contact https://www.linkedin.com/in/zurckz
    @author Noé Cruz | Zurck'z 20
    @since 16-05-2020
    """

    def lambda_inner_builder(invoker: Callable):
        def wrapper_lambda_handler(*args, **kwargs):
            try:
                response: Any = invoker(*args, **kwargs)
                if isinstance(response, LambdaEventResult) or isinstance(response, SuccessEventResult):
                    return build_response(response.status, response.payload, response.success)
                return build_response(default_status, response, True)
            except ZHttpError as e:
                msg = f"An error occurred while processing event: Reason: {e.reason}. Message: {e.message}"
                ctx().logger.exception(msg, exc_info=e)
                if notifier:
                    notifier(msg)
                if raise_exc is True:
                    raise Exception("An error occurred while processing main process")
                return build_response(e.status, e.metadata, False, e.message, e.reason)
            except Exception as e:
                msg = f"An error occurred while processing event. {str(e)}"
                ctx().logger.exception(msg, exc_info=e)
                if notifier:
                    notifier(msg)
                if raise_exc is True:
                    raise Exception("An error occurred while processing main process")
                return build_response(HttpStatus.INTERNAL_SERVER_ERROR, None, False)

        wrapper_lambda_handler.__name__ = invoker.__name__
        return wrapper_lambda_handler

    return lambda_inner_builder


def lambda_api_response(content_type: Optional[str] = 'application/json', default_code: int = 200,
                        cors: bool = True):
    """
    HTTP Response builder, build response from data provided
    @param cors:
    @param default_code:
    @param content_type: Response content type. Default: application/json
    @return: None

    @contact https://www.linkedin.com/in/zurckz
    @author Noé Cruz | Zurck'z 20
    @since 16-05-2020
    """
    extra_headers = {'Content-Type': content_type}

    def lambda_inner_builder(invoker: Callable):
        def wrapper_lambda_handler(*args, **kwargs):
            response: Any = invoker(*args, **kwargs)
            if isinstance(response, tuple) and len(response) == 3:
                data, code, header = response
                if not header:
                    header = extra_headers
                header.update(extra_headers)
            else:
                data = response
                code = default_code
                header = extra_headers

            if cors:
                header.update(LambdaEventHandler.CORS_HEADERS)

            return {
                "statusCode": code,
                "body": json.dumps(data),
                "headers": header
            }

        wrapper_lambda_handler.__name__ = invoker.__name__
        return wrapper_lambda_handler

    return lambda_inner_builder
