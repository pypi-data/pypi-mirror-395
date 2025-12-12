import json
from abc import ABC, abstractmethod
from datetime import timedelta
from functools import wraps
from timeit import default_timer as timer
from typing import Any, Optional, List, Dict, Tuple
from typing import Callable

from zpy.api.http.errors import ZHttpError
from zpy.api.http.response import _useAwsRequestId
from zpy.api.http.status_codes import HttpMethods
from zpy.app import zapp_context as api
from zpy.app import zapp_context as ctx
from zpy.containers import shared_container
from zpy.logger import zL
from zpy.utils.values import if_null_get

DEFAULT_RESPONSE = {'statusCode': '500', 'headers': {'Content-Type': 'application/json', 'Content-Length': '120',
                                                     'Access-Control-Allow-Origin': '*'}, 'isBase64Encoded': False,
                    'body': '{"code":"INTERNAL SERVER ERROR","details":["The execution of a hook failed before reaching the main process."],"message":"The process could not be completed due to a semantics error."}'}


class AWSEventStep(ABC):
    """
     Event Step
    """
    name: str
    raise_fails: Any
    response: dict

    def __init__(self, name: str, raise_fails: bool = True, response: dict = None):
        self.name = name
        self.raise_fails = raise_fails
        self.response = if_null_get(response, DEFAULT_RESPONSE)

    @abstractmethod
    def before(self, event: dict, contex: dict, *args, **kwargs) -> Tuple[Dict, Dict]:
        ...

    @abstractmethod
    def after(self, response: dict, *args, **kwargs) -> dict:
        """"""
        ...


class EventMapper(ABC):
    @abstractmethod
    def configure(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        pass


class RequestEventMapper(EventMapper):
    @abstractmethod
    def configure(self, event: dict, context: Any, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def execute(self, event: dict, context: Any, *args, **kwargs) -> Tuple[Any, Any]:
        pass


class ResponseEventMapper(EventMapper):
    @abstractmethod
    def configure(self, response: dict, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def execute(self, response: dict, *args, **kwargs) -> Any:
        pass


class RouteEventMapper:
    """

    """

    def __init__(self, route: str, http_method: HttpMethods = HttpMethods.GET,
                 full_request_mapper: Optional[RequestEventMapper] = None,
                 request: EventMapper = None,
                 response: ResponseEventMapper = None,
                 headers: EventMapper = None,
                 query: EventMapper = None,
                 path: EventMapper = None, *args, **kwargs) -> None:
        self.route = route
        self.http_method = http_method
        self.full_request_mapper: RequestEventMapper = full_request_mapper
        self.request_mappers: Dict[str, EventMapper] = {
            'request': request,
            'headers': headers,
            'query_params': query,
            'path_params': path
        }
        self.response_mapper: ResponseEventMapper = response
        self.extra_args = args
        self.extra_kwargs = kwargs

    def for_request(self, mapper: RequestEventMapper):
        self.request_mappers['request'] = mapper
        return self

    def for_response(self, mapper: ResponseEventMapper):
        self.response_mapper = mapper
        return self

    def for_headers(self, mapper: RequestEventMapper):
        self.request_mappers['headers'] = mapper
        return self

    def for_params(self, mapper: RequestEventMapper):
        self.request_mappers['query_params'] = mapper
        return self

    def for_path(self, mapper: RequestEventMapper):
        self.request_mappers['path_params'] = mapper
        return self

    def with_method(self, method: HttpMethods):
        self.http_method = method
        return self

    def with_meta(self, key: str, value: Any):
        self.extra_kwargs[key] = value
        return self

    def with_post(self):
        """
        Configure POST http method
        @return:
        """
        self.http_method = HttpMethods.POST
        return self

    def with_get(self):
        """
        Configure GET http method
        @return:
        """
        self.http_method = HttpMethods.GET
        return self

    def with_put(self):
        """
        Configure GET http method
        @return:
        """
        self.http_method = HttpMethods.PUT
        return self

    def with_patch(self):
        """
        Configure PATCH http method
        @return:
        """
        self.http_method = HttpMethods.PATCH
        return self

    def with_delete(self):
        """
        Configure DELETE http method
        @return:
        """
        self.http_method = HttpMethods.DELETE
        return self

    def configure_request_mappers(self, event: Dict, context: Any, *args, **kwargs):
        if self.full_request_mapper:
            self.full_request_mapper.configure(event, context, *(args + self.extra_args),
                                               **{**kwargs, **self.extra_kwargs})

        for k in self.request_mappers:
            if self.request_mappers[k] and self.request_mappers[k] != self.full_request_mapper:
                self.request_mappers[k].configure(event, context, *(args + self.extra_args),
                                                  **{**kwargs, **self.extra_kwargs})

    def configure_response_mappers(self, response: Any, *args, **kwargs):
        if self.response_mapper:
            self.response_mapper.configure(response, *(args + self.extra_args),
                                           **{**kwargs, **self.extra_kwargs})

    @classmethod
    def from_dict(cls, config: Dict[str, Dict[str, Any]], key: str = None):
        if not config:
            raise ValueError('Config cannot be null.')
        keys: List[str] = list(config.keys())
        if not keys:
            raise ValueError('Config should be a key')

        str_route: str = if_null_get(key, keys[0])

        def get_map(x):
            return x.get('mapper', None)

        def get(x, k) -> Dict:
            return x.get(k, {})

        spec = get(config, str_route)
        default_mapper = get(spec, 'default').get('mapper', None)

        return cls(route=str_route, full_request_mapper=default_mapper, request=get_map(get(spec, 'request')),
                   response=get_map(get(spec, 'response')), headers=get_map(get(spec, 'headers')),
                   query=get_map(get(spec, 'query_params')), path=get_map(get(spec, 'path_params')))


class RouteEventMapperManager(AWSEventStep):

    def __init__(self, configs: List[RouteEventMapper] = None, name: str = 'RouteEventMapperManager',
                 strict: bool = False, initializer: Callable[[Any, Any, Any, Any], None] = None, *args, **kwargs):
        super().__init__(name)
        if not configs:
            configs = []
        self.configs: Dict[str, RouteEventMapper] = {f'{k.route}:{k.http_method.value}': k for k in configs}
        self.current: Optional[RouteEventMapper] = None
        self.config_found = False
        self.strict = strict
        self.extra_args = args
        self.extra_kwargs = kwargs
        self.initializer = initializer

    def add(self, route_config: RouteEventMapper) -> 'RouteEventMapperManager':
        self.configs[f'{route_config.route}:{route_config.http_method.value}'] = route_config
        return self

    def add_meta(self, key: str, value: Any) -> 'RouteEventMapperManager':
        self.extra_kwargs[key] = value
        return self

    @classmethod
    def from_dict(cls, configs: Dict, name: str):
        configurations = [RouteEventMapper.from_dict(configs, k) for k in configs.keys()]
        return cls(configurations, name)

    def before(self, event: dict, context: dict, *args, **kwargs) -> Tuple[Dict, Any]:
        if not event:
            return event, context
        if 'resource' not in event or 'httpMethod' not in event:
            return event, context
        current_route = f'{event["resource"]}:{event["httpMethod"]}'
        self.config_found = False
        if current_route in self.configs:
            if self.initializer:
                self.initializer(event, context, *self.extra_args, **self.extra_kwargs)
            self.current = self.configs[current_route]
            self.current.configure_request_mappers(event, context, *self.extra_args, **self.extra_kwargs)
            self.config_found = True
            if self.current.full_request_mapper:
                event, context = self.current.full_request_mapper.execute(event=event, context=context,
                                                                          *self.extra_args,
                                                                          **self.extra_kwargs)
            for x_mapper in self.current.request_mappers.values():
                if x_mapper is not None:
                    event, context = x_mapper.execute(event, context=context, *self.extra_args,
                                                      **self.extra_kwargs)
        return event, context

    def after(self, response: dict, *args, **kwargs) -> dict:
        if self.config_found and self.current.response_mapper is not None:
            self.current.configure_response_mappers(response, *self.extra_args, **self.extra_kwargs)
            return self.current.response_mapper.execute(response=response, *self.extra_args, **self.extra_kwargs)
        return response


def prepare_event_pipe_exception(e: ZHttpError) -> dict:
    body = {"code": f"{e.get_str_code()}", "details": e.details,
            "message": f"{e.get_message()}"}
    body = json.dumps(body)
    return {'statusCode': f'{e.get_http_code()}',
            'headers': {'Content-Type': 'application/json', 'Content-Length': len(body),
                        'Access-Control-Allow-Origin': '*'}, 'isBase64Encoded': False,
            'body': body}


def lambda_event_pipe(event: dict, context: dict,
                      processor: Callable[[Dict, Dict], Dict],
                      steps: Optional[List[AWSEventStep]] = None):
    logger = ctx().logger
    response = None
    if not steps:
        steps = []
    for mw in steps:
        try:
            event, context = mw.before(event, context)
        except ZHttpError as e:
            logger.exception(f"An error occurred when execute before: {mw.name}. ", exc_info=e)
            return prepare_event_pipe_exception(e)
        except Exception as e:
            logger.exception(f"An error occurred when execute before: {mw.name}. ", exc_info=e)
            if mw.raise_fails:
                return mw.response
    try:
        response = processor(event, context)
    except Exception as e:
        logger.exception(f"An error occurred when execute processor... ", exc_info=e)
        return DEFAULT_RESPONSE

    for mw in reversed(steps):
        try:
            response = mw.after(response)
        except ZHttpError as e:
            logger.exception(f"An error occurred when execute after: {mw.name}. ", exc_info=e)
            return prepare_event_pipe_exception(e)
        except Exception as e:
            logger.exception(f"An error occurred when execute after: {mw.name}. ", exc_info=e)
            if mw.raise_fails:
                return mw.response
    return response


class LambdaEventPipe:

    def __init__(self, event: dict, context: Any):
        self.event = event
        self.context = context
        self.steps = []

    def add(self, step: AWSEventStep) -> 'LambdaEventPipe':
        self.steps.append(step)
        return self

    def run(self, event_processor: Callable[[Dict, Any], Dict]) -> dict:
        return lambda_event_pipe(self.event, self.context, event_processor, self.steps)


def store_request_id(context) -> Optional[str]:
    """Extract aws request id from context

    Args:
        context ([type]): Lambda context
    """
    try:
        shared_container["aws_request_id"] = context.aws_request_id
        return context.aws_request_id
    except Exception as e:
        zL.ex("An error occurred while extracting aws request id", exc_info=e)
        return None


def event_processors(storage: dict, use_id: bool, logs: bool, send_logs: bool, *args, **kwargs):
    """Lambda event processors

    Args:
        @param storage:
        @param use_id:
        @param logs:
        @param send_logs:
    """
    try:
        if len(args) >= 2:
            event = args[0]
            storage['request'] = event
            if logs:
                api().logger.info(f"Request: {event}", shippable=send_logs)
            if _useAwsRequestId or use_id:
                storage['request_id'] = store_request_id(args[1])

        else:
            if "event" in kwargs:
                storage['request'] = kwargs['event']
                if logs:
                    api().logger.info(f"Request: {kwargs['event']}", shippable=send_logs)
            if "context" in kwargs:
                if _useAwsRequestId or use_id:
                    storage['request_id'] = store_request_id(args[1])
    except Exception as e:
        api().logger.ex("An error occurred while processing event!", exc_info=e)


def aws_lambda(logs: bool = True, save_id: bool = False, measure_time: bool = True, send_logs: bool = False,
               event_sender: Optional[Callable[[dict], Any]] = None):
    """Lambda Handler

    Args:
        @param event_sender:
        @param logs: (bool, optional): Logging request and response. Defaults to False.
        @param save_id: (bool, optional): Register aws lambda request id. Defaults to True.
        @param measure_time: (bool, optional): Measure elapsed execution time. Defaults to True.
        @param send_logs: Send event logs by log sender configured
    """
    api().release_logger()
    event = {'request_id': '-'}

    def callable_fn(invoker: Callable):
        @wraps(invoker)
        def wrapper(*args, **kwargs):
            event_processors(event, save_id, logs, send_logs, *args, **kwargs)
            start = 0.0
            if if_null_get(measure_time, False):
                start = timer()
            result = invoker(*args, **kwargs)
            event['response'] = result
            if logs:
                api().logger.info(f"Response: {result}", shippable=send_logs)
            if if_null_get(measure_time, False):
                end = timer()
                api().logger.info(f"Elapsed execution time: {timedelta(seconds=end - start)}", shippable=send_logs)
            if event_sender:
                event_sender(event)
            return result

        return wrapper

    return callable_fn
