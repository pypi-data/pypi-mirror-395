# Created by Noé Cruz | Zurckz 22 at 11/09/2022
# See https://www.linkedin.com/in/zurckz
from logging import INFO, WARN, ERROR
from typing import Optional

from zpy.logger import ZLogger
from zpy.app import zapp_context as ctx, ZContext
from zpy.utils.values import if_null_get
from zpy.logger.structured import StructuredLog


class Loggable:

    def __init__(self, logger: Optional[ZLogger] = None):
        self.logger: ZLogger = if_null_get(logger, ctx().logger)
        self.app = ctx().app_name
        self.context: ZContext = ctx()

    def log_exception(self, value: any, shippable: bool = False, **kwargs):
        self.logger.exception(value, shippable, **kwargs)

    def log_error(self, value: any, exc_info: any, shippable: bool = False):
        self.logger.err(value, shippable, exc_info=exc_info)

    def log_info(self, value: any, shippable: bool = False, **kwargs):
        self.logger.info(value, shippable, **kwargs)

    def log_warn(self, value: any, shippable: bool = False, **kwargs):
        self.logger.warn(value, shippable, **kwargs)

    def log_struct_info(self, message: str, flow: str = None, description: str = None, meta: Optional[dict] = None,
                        **kwargs) -> StructuredLog:
        _flow = if_null_get(flow, self.context.get_flow())
        log = StructuredLog(_flow, message, self.app, description, INFO, meta, **kwargs)
        self.logger.info(log)
        return log

    def log_struct_warn(self, message: str, flow: str = None, description: str = None, meta: Optional[dict] = None,
                        **kwargs) -> 'StructuredLog':
        log = StructuredLog(if_null_get(flow, self.context.get_flow()), message, self.app, description, WARN, meta,
                            **kwargs)
        self.logger.warn(log)
        return log

    def log_struct_error(self, message: str, flow: str = None, description: str = None, meta: Optional[dict] = None,
                         **kwargs) -> 'StructuredLog':
        log = StructuredLog(if_null_get(flow, self.context.get_flow()), message, self.app, description, ERROR, meta,
                            **kwargs)
        self.logger.err(log)
        return log
