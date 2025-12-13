from .checker import check_admin_user as check_admin_user
from .engine import load_engine as load_engine, unload_engine as unload_engine
from .fast_api import create_init_fastapi as create_init_fastapi
from .package import load_meta_config as load_meta_config
from _typeshed import Incomplete
from fastapi import FastAPI as FastAPI
from typing import Callable

class Application:
    """应用核心类，负责初始化和管理FastAPI应用"""

    fastapi: Incomplete
    def __init__(self) -> None:
        """初始化应用核心组件"""
    def run(self) -> None: ...
    def startup(self, func: Callable):
        """装饰器或直接注册启动回调"""
