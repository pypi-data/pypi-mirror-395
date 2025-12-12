# Created by Noé Cruz | Zurckz 22 at 20/03/2022
# See https://www.linkedin.com/in/zurckz
from typing import Callable, Optional, Any, Union, Dict
from zpy.app import zapp_context as ctx
from zpy.containers import shared_container
import json
import copy


class SQSHandler(object):
    _DEFAULT_ERR_MSG = 'An error occurred while processing record data'

    def __init__(
            self,
            processor: Optional[Callable[[dict, dict], Any]],
            single: Optional[bool] = False,
            strict=False,
            verbose: bool = False,
            jsonfy=True,
            re_enqueue: bool = False,
            signal_processor: Optional[Callable[[dict, dict], dict]] = None
    ):
        self.processor = processor
        self.single_item = single
        self.strict = strict
        self.verbose = verbose
        self.response_builder = None
        self.request_parser = None
        self.error_notifier = None
        self.send_str_exception = True
        self.starting_process_logger = None
        self.jsonfy = jsonfy
        self.re_enqueue = re_enqueue
        self.common_fatal_error_msg = f'Fatal :: {self._DEFAULT_ERR_MSG}'
        self.signal_processor = signal_processor
        self.before: Optional[Callable[[Dict], None]] = None
        self.after: Optional[Callable[[Dict], None]] = None
        self.on_body: Optional[Callable[[Dict, Dict, str], Dict]] = None

    def configure(
            self,
            response_builder: Callable[[Any], Any] = None,
            request_parser: Callable[[Any], Any] = None,
            error_notifier: Callable[[Any, Any], None] = None, send_str_exception: bool = True,
            starting_process_logger: Callable[[Any, Any], None] = None,
            common_error_msg: str = None
    ) -> 'SQSHandler':
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
    def of(
            cls,
            processor: Optional[Callable[[dict, dict], Any]],
            single: Optional[bool] = False,
            strict=False,
            verbose=False,
            jsonfy=True
    ):
        return cls(processor, single, strict, verbose, jsonfy)

    @staticmethod
    def proxy(event, handler):
        return handler.run(event)

    def __notify_error(self, record, msg):
        if self.error_notifier:
            self.error_notifier(record, msg)

    @staticmethod
    def is_wake_up_signal(record: dict):
        if not record:
            return False
        msg_attrs = record.get('messageAttributes', None)
        if msg_attrs:
            attrs: dict = msg_attrs.get('ZType', None)
            if not attrs:
                return False
            value = attrs.get('stringValue', None)
            return value == 'WakeUpSignal'
        return False

    def run(self, event):
        logger = ctx().logger
        failed = False

        if self.before:
            try:
                self.before(event)
            except Exception as e:
                logger.exception("An error occurred execute on simple before hook", exc_info=e)

        if self.request_parser:
            event = self.request_parser(event)

        if not self.processor:
            msg = "The sqs record processor cant be null."
            self.__notify_error(None, msg)
            return msg

        if 'Records' not in event:
            if self.strict:
                msg = "Fatal :: Could not continue processing, invalid event. Missing {Records} key."
                self.__notify_error(event, msg)
                logger.err(msg)
                return msg
            event = {'Records': [event]}
        batch_results = []
        for index, record in enumerate(event["Records"]):
            body: Optional[Union[dict, str]] = None
            x_record = copy.copy(record)
            record_id = index if 'messageId' not in record else record['messageId']
            shared_container["aws_sqs_message_id"] = record_id
            try:
                if 'body' not in record:
                    if self.strict:
                        msg = "Fatal :: Invalid item, could not continue processing. Missing {body} key."
                        self.__notify_error(x_record, msg)
                        if self.single_item:
                            return msg
                        continue
                    body = record
                else:
                    body = record.pop('body')
                if type(body) is not dict:
                    if self.jsonfy:
                        body = json.loads(body)
                if self.verbose:
                    logger.info(f"Starting record processing: {record_id} with data: {body}")
                if self.starting_process_logger:
                    self.starting_process_logger(body, record)
                result = None
                if self.on_body:
                    body = self.on_body(body, record, record_id)
                if SQSHandler.is_wake_up_signal(record):
                    result = "Wake up signal received successfully"
                    if self.signal_processor:
                        result = self.signal_processor(body, record)
                else:
                    result = self.processor(body, record)
                if self.verbose:
                    logger.info(result)
                batch_results.append({
                    "result": result,
                    "message_id": record_id
                })
                if self.single_item:
                    break
            except Exception as e:
                failed = True
                msg_err = f'{self.common_fatal_error_msg}... {str(e) if self.send_str_exception else ""}'
                self.__notify_error(x_record, msg_err)
                logger.exception(f"{self.common_fatal_error_msg}: {body}\n", exc_info=e)
                if self.re_enqueue:
                    raise Exception("Exception autogenerated for re enqueue record...")
        response = {
            'message': "Finished Process." if not failed else "Finished process with errors.",
            "results": batch_results
        }
        if self.after:
            try:
                self.after(response)
            except Exception as e:
                logger.exception("An error occurred execute on simple after hook", exc_info=e)
        if self.response_builder:
            response = self.response_builder(response)
        return response

    def single(self, body, context):
        ...
