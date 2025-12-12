from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Union, Any, Dict, Callable, Optional
from copy import copy

from zpy.api.http.errors import ZHttpError, BadRequest
from zpy.api.http.status_codes import HttpStatus
from zpy.utils.funcs import Maybe, if_get
from zpy.utils.values import if_null_get
from zpy.app import zapp_context as ctx

T = TypeVar("T")
S = TypeVar("S")


class UCMeta:
    def __init__(self, identifier: str, key_identifier: str = None) -> None:
        self.id = identifier
        if key_identifier:
            setattr(self, key_identifier, identifier)


class Selectable:
    def __init__(self, identifier: str, key_identifier: str = None, weight: float = 1.0) -> None:
        """

        @param identifier: value of selector based. E.g. UserCreator
        @param key_identifier: key of selector based. E.g. action
        """
        # if not key_identifier:
        #     key_identifier = 'id'
        self.weight = weight
        self.name = identifier
        # self.identifiers: Dict[str, Dict[str, str]] = {
        #     key_identifier: {"value": identifier, "weight": weight}
        # }
        self.identifiers_v2: List[Dict[str, str]] = [{"value": identifier, "weight": weight}]

    def configure_for_all(self, weight: float = 2.0):
        # self.identifiers['*'] = {"value": '*', "weight": weight}
        self.identifiers_v2.append({"value": '*', "weight": weight})

    def configure(self, uc_identifier: Any, weight: float):
        # self.identifiers[key_identifier] = {
        #     "value": uc_identifier,
        #     "weight": weight
        # }
        self.identifiers_v2.append({
            "value": uc_identifier,
            "weight": weight
        })

    def execute_when(self, event: str, sort_weight: float, key_identifier: Any = 'id'):
        """
        The use case will be executed when event arrive to selector.
        @param event: Event name to associate
        @param sort_weight: weight for sort case execution
        @param key_identifier:
        @return:
        """
        self.configure(event, sort_weight)

    def execute_always(self, sort_weight: float = 2.0):
        """
        The use case will be executed on all events that arrive and are executed.
        @param sort_weight:
        @return: None
        """
        # self.identifiers['*'] = {"value": '*', "weight": sort_weight}
        self.identifiers_v2.append({"value": '*', "weight": sort_weight})


class UseCase(ABC, Generic[T, S]):
    def __init__(self, name: Any = None):
        self.name = name

    def before(self, *args, **kwargs):
        pass

    @abstractmethod
    def execute(self, payload: T, *args, **kwargs) -> S:
        """Execute use case"""
        pass

    def after(self, *args, **kwargs):
        pass


class UseCaseSelector(UseCase, UCMeta):

    def __init__(self, use_cases: List[Union[UseCase, UCMeta, Any]], action_keys: List[str] = None,
                 key_uc_identifier: str = 'id', selector_id='default', payload_keys: List[str] = None):
        UCMeta.__init__(self, identifier=selector_id)
        self.cases = {getattr(x, key_uc_identifier): x for x in use_cases}
        self.action_keys = if_null_get(action_keys, ['action'])
        self.key_identifier = key_uc_identifier
        self.payload_keys = if_null_get(payload_keys, ['payload'])

    def execute(self, data: dict, context: Any = None, *args, **kwargs) -> dict:
        action = None
        for key_action in self.action_keys:
            if key_action in data:
                action = key_action
                break
        if action is None:
            raise ValueError(f'Request provided is malformed. Missing {action} key!')

        operation: Union[UseCase, UCMeta] = self.cases.get(data[action], None)

        if not operation:
            raise ValueError(f"Use case for action: {data['action']} not registered in selector.")

        payload_key = None
        for pk in self.payload_keys:
            if pk in data:
                payload_key = pk
                break

        payload = data.get(payload_key, data)
        return operation.execute(payload, context=context)


class CaseSelector(UseCase, Selectable):

    def __init__(self, use_cases: List[Union[UseCase, Selectable, Any]], action_keys: List[str] = None,
                 key_uc_identifier: str = 'id', selector_id='default', payload_keys: List[str] = None,
                 payload_mutation: bool = False, safe_execution: bool = False):
        """
        Use Case router

        Allow configuring many use cases and expose "execute" or "handle" method for future use case execution
        @param use_cases: Use case instance list, that will be available for execution
        @param action_keys: Key or keys for identify what use case must be executed. E.g: "event", "id" or "action"
        @param key_uc_identifier: Key for retrieve use case identifier
        @param selector_id: Identifier for case selector
        @param payload_keys: Key or keys for retrieve use case payload
        @param payload_mutation: Flag for allow mutation payload between use cases
        @param safe_execution: Flag for safe execution, the proces raise error if one case fail
        """
        Selectable.__init__(self, identifier=selector_id, key_identifier=key_uc_identifier)
        self.action_keys = if_null_get(action_keys, ['action'])
        self.payload_keys = if_null_get(payload_keys, ['payload'])
        self.multi_cases_key = 'cases'
        self.allow_payload_mutation = payload_mutation
        self.on_before = None
        self.on_after = None
        self.on_error = None
        self.on_case: Optional[Callable[[str, Dict], Dict]] = None
        self.before_continue: Optional[Callable[[str, Dict, Dict, Dict], Dict]] = None
        self.safe_execution = safe_execution
        self.cases = Maybe(use_cases) \
            .bind(self.__group_cases) \
            .bind(self.__sort_cases) \
            .value

    def configure_for_multiple(self, multiple_main_key: str) -> 'CaseSelector':
        self.multi_cases_key = multiple_main_key
        return self

    def configure_error_notifier(self, error_notifier: Callable[[Any, Any, Any], Any]):
        self.on_error = error_notifier

    @staticmethod
    def __group_cases(cases: List[Union[UseCase, Selectable, Any]]):
        group_to_sort = {}
        for case in cases:
            for v in case.identifiers_v2:
                if v['value'] not in group_to_sort:
                    group_to_sort[v['value']] = {
                        v['weight']: case
                    }
                    continue
                group_to_sort[v['value']][v['weight']] = case

        return group_to_sort

    @staticmethod
    def __sort_cases(cases: Dict[str, Dict[Any, Union[UseCase, Selectable, Any]]]):
        return {c: [x[1] for x in sorted(cases[c].items())] for c in cases}

    def handle(self, data: dict, context: Any = None, *args, **kwargs) -> dict:
        """
        Handle multiple cases
        @param data: event
        @param context:
        @param args:
        @param kwargs:
        @return:
        """

        def build_result(x_status: tuple, content_result: Any, metadata: Any, details: Any) -> dict:
            return {
                'status': {
                    "code": x_status[0],
                    "status": x_status[1],
                    "message": x_status[2],
                    'details': details
                },
                'body': content_result,
                'metadata': metadata,
            }

        def find_identifier(raw_payload: dict, identifiers: List[str]) -> str:
            action = None
            for key_action in identifiers:
                if key_action in raw_payload:
                    action = key_action
                    break
            if action is None:
                raise ValueError(f'Request provided is malformed. Missing event identifier!')
            return action

        if self.on_before:
            self.on_before()
        current_case_execution = None
        final_results = []
        case_id_to_execute = None
        try:
            if not data or self.multi_cases_key not in data:
                raise BadRequest(f'Request provided is malformed. Missing {self.multi_cases_key} key!')
            raw_cases_to_execute = data[self.multi_cases_key]
            print("Raw cases: ", raw_cases_to_execute)
            for case in raw_cases_to_execute:
                current_case_result = {
                    "event": None,
                    "executions": []
                }
                try:
                    case_id_to_execute = find_identifier(case, self.action_keys)
                    cases_to_execute: List[Union[UseCase, Selectable]] = self.cases.get(case[case_id_to_execute], [])
                    cases_to_execute = sorted(cases_to_execute + self.cases.get('*', []), key=lambda x: x.weight)

                    current_case_result['event'] = case.get(case_id_to_execute, None)
                    current_case_execution = current_case_result['event']
                    if not cases_to_execute:
                        raise ValueError(f"Use case for event: {case[case_id_to_execute]} not registered in selector.")
                    print("Raw inner cases: ", cases_to_execute)
                    payload_key = find_identifier(case, self.payload_keys)
                    payload = case.get(payload_key, None)
                    for x_case in cases_to_execute:
                        ctx().logger.info(f'⚡ Running case: {x_case.name}...')
                        payload = if_get(self.allow_payload_mutation, payload, copy(payload))
                        meta = case.get('metadata', None)
                        if self.on_case:
                            payload = self.on_case(x_case.name, payload)
                        x_case.before(payload=payload, context=context, metadata=meta)
                        result = x_case.execute(payload, context=context, metadata=meta)
                        x_case.after(payload=payload, context=context, metadata=meta, result=result)
                        current_case_result['executions'].append({
                            "event": x_case.name,
                            "body": result
                        })
                        if self.before_continue:
                            self.before_continue(x_case.name, payload, meta, result)
                    final_results.append(current_case_result)
                except Exception as e:
                    ctx().logger.exception(
                        f"An error occurred while processing task: {case.get(case_id_to_execute, '')} ",
                        exc_info=e)
                    current_case_result['error'] = str(e)
                    current_case_result['executions'].append({
                        "event": case.get(case_id_to_execute, ''),
                        "body": None
                    })
                    final_results.append(current_case_result)
                    if self.safe_execution is True:
                        raise
            return build_result(HttpStatus.SUCCESS.value, final_results, None, None)
        except ZHttpError as e:
            ctx().logger.exception("An error occurred while processing task ", exc_info=e)
            status = e.status.value
            if self.on_error:
                self.on_error(data, context, e, status, if_null_get(e.reason, status[2]), current_case_execution)
            details = if_null_get(e.details, [])
            if e.message:
                status = (status[0], status[1], e.message)
            if e.reason:
                details.append(e.reason)
            if self.on_after:
                self.on_after()
            return build_result(status, final_results, e.metadata, e.details)
        except Exception as e:
            ctx().logger.exception("An error occurred while processing case ", exc_info=e)
            status = HttpStatus.INTERNAL_SERVER_ERROR.value
            if self.on_error:
                self.on_error(data, context, e, status, status[2], current_case_execution)
            if self.on_after:
                self.on_after()
            return build_result(status, final_results, None, [str(e)])

    def execute(self, data: dict, context: Any = None, *args, **kwargs) -> List[Any]:
        action = None
        for key_action in self.action_keys:
            if key_action in data:
                action = key_action
                break

        if action is None:
            raise ValueError(f'Request provided is malformed. Missing {action} key!')

        cases_to_execute: List[Union[UseCase, Selectable]] = self.cases.get(data[action], [])
        cases_to_execute = sorted(cases_to_execute + self.cases.get('*', []), key=lambda x: x.weight)

        if not cases_to_execute:
            raise ValueError(f"Use case for action: {data[action]} not registered in selector.")

        payload_key = None
        for pk in self.payload_keys:
            if pk in data:
                payload_key = pk
                break

        payload = data.get(payload_key, data)
        results = []
        if self.on_before:
            self.on_before()
        for x_case in cases_to_execute:
            ctx().logger.info(f'⚡ Running case: {x_case.name}...')
            try:
                _payload = if_get(self.allow_payload_mutation, payload, copy(payload))
                x_case.before(payload=_payload, context=context)
                result = x_case.execute(_payload, context=context)
                if isinstance(result, dict):
                    result['event'] = data[action]
                results.append(result)
                x_case.after(payload=_payload, context=context, result=result)
                if self.before_continue:
                    self.before_continue(x_case.name, payload, context, result)
            except Exception as e:
                ctx().logger.exception(f"An error occurred while processing case: {x_case.name} ", exc_info=e)
                if self.safe_execution is True:
                    break
        if self.on_after:
            self.on_after()
        return results
