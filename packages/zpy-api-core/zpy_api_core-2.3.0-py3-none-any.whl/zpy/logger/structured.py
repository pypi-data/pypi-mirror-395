# Created by Noé Cruz | Zurckz 22 at 24/07/2022
# See https://www.linkedin.com/in/zurckz
from typing import Optional, Any, List

from zpy.logger import ZLogger
from zpy.utils.values import if_null_get
from zpy.utils import get_env
from logging import getLevelName, INFO, WARN, ERROR, DEBUG
from zpy.utils.collections import walk_and_apply
from copy import copy
from zpy.app import zapp_context as ctx

sensitive_data_filters = []
main_logger: Optional[ZLogger] = None
main_logger_app: Optional[str] = None


def init_mask_meta_keys_filter(keys: List[str] = None):
    keys = ['pass', 'password', 'bank', 'pwd', 'contraseña', 'contra', 'priv', 'banc', 'secret', 'clave']

    def mask_meta_keys_filter(log: dict) -> dict:
        def sensitive_data_masker(key, value) -> Any:
            for sk in keys:
                if isinstance(key, str) and sk in copy(key).lower():
                    return f"******{str(value)[-2:]}"
            return value

        if 'meta' in log and isinstance(log['meta'], dict):
            walk_and_apply(log['meta'], sensitive_data_masker)
        return log

    return mask_meta_keys_filter


class StructuredLog(object):

    @staticmethod
    def add_sensitive_filter(log_filter):
        global sensitive_data_filters
        sensitive_data_filters.append(log_filter)

    @staticmethod
    def configure_logger(logger, app_name: str):
        global main_logger
        main_logger = logger
        global main_logger_app
        main_logger_app = app_name

    def __init__(self, flow: str, message: str, app: str = None, description: str = None, level: int = INFO,
                 meta: Optional[dict] = None, **kwargs) -> None:
        metadata = if_null_get(meta, {})
        metadata.update(kwargs)
        self.log: dict = {
            'application': if_null_get(app, get_env("APP_NAME", "Unknown")),
            'flow': flow,
            'message': message,
            'description': description,
            'level': getLevelName(level),
            'meta': metadata
        }
        if sensitive_data_filters:
            self.log = [sf(self.log) for sf in sensitive_data_filters][0]

    def __str__(self):
        return f'{self.log}'

    @staticmethod
    def log_info(flow: str, message: str, description: str = None, meta: Optional[dict] = None,
                 **kwargs) -> 'StructuredLog':
        log = StructuredLog(flow, message, main_logger_app, description, INFO, meta, **kwargs)
        if_null_get(main_logger, ctx().logger).info(log)
        return log

    @staticmethod
    def log_warn(flow: str, message: str, description: str = None, meta: Optional[dict] = None,
                 **kwargs) -> 'StructuredLog':
        log = StructuredLog(flow, message, main_logger_app, description, WARN, meta, **kwargs)
        if_null_get(main_logger, ctx().logger).warn(log)
        return log

    @staticmethod
    def log_error(flow: str, message: str, description: str = None, meta: Optional[dict] = None,
                  **kwargs) -> 'StructuredLog':
        log = StructuredLog(flow, message, main_logger_app, description, ERROR, meta, **kwargs)
        if_null_get(main_logger, ctx().logger).err(log)
        return log
