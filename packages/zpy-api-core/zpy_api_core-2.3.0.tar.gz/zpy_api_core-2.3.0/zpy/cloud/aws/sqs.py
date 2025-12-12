# Created by Noé Cruz | Zurckz 22 at 15/04/2022
# See https://www.linkedin.com/in/zurckz
from dataclasses import dataclass
from typing import Any, Callable, Optional
from zpy.app import zapp_context as ctx
from zpy.utils.funcs import safe_exec_wrapper
from zpy.utils.values import if_null_get


@dataclass
class SQSResource:
    event: str
    name: str
    attributes: Optional[dict]


def get_sqs_url_from(sqs_client: Any, sqs_name: str) -> str:
    """
    Retrieve sqs url from name
    @param sqs_client:
    @param sqs_name:
    @return: url
    """
    return sqs_client.get_queue_url(
        QueueName=sqs_name,
    )['QueueUrl']


def send_secure_message_to_sqs(sqs_client: Any, payload: str, origin: str, attributes=None, sqs_name: str = None,
                               sqs_url: str = None, delay: int = 0,
                               error_notifier: Optional[Callable[[str], None]] = None) -> Optional[dict]:
    """
    Helper declarative function to send sqs message


    @param sqs_client: SQS Client built from boto3
    @param payload: Message to send
    @param attributes: Custom attributes to send
    @param origin: Origin of emitted message
    @param sqs_name: SQS Name
    @param sqs_url: SQS Url
    @param delay: Delay seconds
    @param error_notifier: Error reporting function

    @note If sqs name is null, sqs url is required or if sqs_url is null, sqs_name is required

    @return: sqs response
    """
    return safe_exec_wrapper(
        target=send_message_to_sqs,
        args=[sqs_client, payload, origin, attributes, sqs_name, sqs_url, delay],
        kwargs=None,
        msg=f"An error occurred while try to send message to: {if_null_get(sqs_name, sqs_url)}",
        notifier=error_notifier,
        default_ret=None
    )


def send_message_to_sqs(sqs_client: Any, payload: str, origin: str, attributes=None, sqs_name: str = None,
                        sqs_url: str = None, delay: int = 0) -> dict:
    """
    Helper declarative function to send sqs message

    @param sqs_client: SQS Client built from boto3
    @param payload: Message to send
    @param attributes: Custom attributes to send
    @param origin: Origin of emitted message
    @param sqs_name: SQS Name
    @param sqs_url: SQS Url
    @param delay: Delay seconds

    @note If sqs name is null, sqs url is required or if sqs_url is null, sqs_name is required

    @return: sqs response
    """

    if not sqs_name and not sqs_url:
        raise ValueError("SQS Name or SQS Url is required")

    if attributes is None:
        attributes = {}

    if 'ZOrigin' not in attributes:
        attributes['ZOrigin'] = {
            'DataType': 'String',
            'StringValue': origin if origin else 'Unknown'
        }

    return sqs_client.send_message(
        QueueUrl=get_sqs_url_from(sqs_client, sqs_name) if sqs_name else sqs_url,
        DelaySeconds=delay,
        MessageAttributes=attributes,
        MessageBody=payload
    )


def send_message_to_fifo_sqs(sqs_client: Any, payload: str, origin: str, attributes=None, sqs_name: str = None,
                             sqs_url: str = None, delay: int = 0, group_id: str = None,
                             deduplication_id: str = None) -> dict:
    """
    Helper declarative function to send sqs message

    @param deduplication_id: Only for fifo
    @param group_id: Only for Fifo
    @param sqs_client: SQS Client built from boto3
    @param payload: Message to send
    @param attributes: Custom attributes to send
    @param origin: Origin of emitted message
    @param sqs_name: SQS Name
    @param sqs_url: SQS Url
    @param delay: Delay seconds

    @note If sqs name is null, sqs url is required or if sqs_url is null, sqs_name is required

    @return: sqs response
    """

    if not sqs_name and not sqs_url:
        raise ValueError("SQS Name or SQS Url is required")

    if attributes is None:
        attributes = {}

    if 'ZOrigin' not in attributes:
        attributes['ZOrigin'] = {
            'DataType': 'String',
            'StringValue': origin if origin else 'Unknown'
        }

    return sqs_client.send_message(
        QueueUrl=get_sqs_url_from(sqs_client, sqs_name) if sqs_name else sqs_url,
        DelaySeconds=delay,
        MessageAttributes=attributes,
        MessageBody=payload,
        MessageDeduplicationId=deduplication_id,
        MessageGroupId=group_id
    )


def send_wake_up_signal(sqs_client: Any, metadata: str, sqs_name: str = None, sqs_url: str = None,
                        origin: str = "Unknown"):
    logg = ctx().logger
    destination = if_null_get(sqs_name, sqs_url)
    try:
        response = send_message_to_sqs(
            sqs_client=sqs_client,
            payload=metadata,
            origin=origin,
            attributes={
                'ZType': {
                    'DataType': 'String',
                    'StringValue': 'WakeUpSignal'
                }
            },
            sqs_name=sqs_name,
            sqs_url=sqs_url)
        logg.info(f"Wake up signal was sent successfully to {destination}, id: {response['MessageId']}")
    except Exception as e:
        logg.err(f"An error occurred while try to send Wake up signal to: {destination}", exc_info=e)
