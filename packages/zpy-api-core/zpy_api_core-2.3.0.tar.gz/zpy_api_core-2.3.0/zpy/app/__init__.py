# Created by Noé Cruz | Zurckz 22 at 05/03/2022
# See https://www.linkedin.com/in/zurckz
import logging
from typing import Optional
from zpy.utils import get_env
from zpy.utils.values import if_null_get
from zpy.logger import zL, ZLFormat, ZLogger


class ZContext(object):

    def __init__(self, logger: Optional[ZLogger] = None, app_name: str = None, env: str = None, flow: str = None):
        self.logger = logger
        self.app_name = if_null_get(app_name, get_env("APP_NAME", "UNKNOWN"))
        self.environment = if_null_get(env, get_env("APP_ENVIRONMENT", "local"))
        self.app_version = if_null_get(env, get_env("APP_VERSION", "UNKNOWN"))
        self.main_flow = if_null_get(flow, get_env("FLOW", ""))
        self.flow = self.main_flow
        if not logger:
            self.logger = zL(self.app_name, logging.INFO, ZLFormat.LM)

    def release_logger(self, name: str = "Z-API"):
        self.logger.release(name)

    def update_flow(self, flow: str):
        self.flow = f'{self.flow}#{flow}'

    def get_flow(self):
        return self.flow

    def reset_flow(self):
        self.flow = self.main_flow


context: Optional[ZContext] = None


def setup_context(ctx: Optional[ZContext] = None) -> ZContext:
    global context
    if ctx:
        context = ctx
    if not ctx:
        context = ZContext()
    return context


def zapp_context() -> ZContext:
    global context
    if not context:
        return setup_context()
    return context
