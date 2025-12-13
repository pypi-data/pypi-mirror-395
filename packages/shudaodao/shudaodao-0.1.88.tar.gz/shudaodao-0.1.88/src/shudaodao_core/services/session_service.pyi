from ..engine.database_engine import DatabaseEngine as DatabaseEngine
from ..exception.service_exception import ShudaodaoException as ShudaodaoException
from ..logger.logging_ import logging as logging
from _typeshed import Incomplete
from collections.abc import Generator
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator

class AsyncSessionService:
    def __new__(cls):
        """线程安全单例构造器"""
    def get_session_factory(self, name) -> async_sessionmaker:
        """获取指定数据源的会话工厂（动态创建如果不存在）"""
    @asynccontextmanager
    async def get_session(self, name) -> AsyncGenerator[AsyncSession, None]:
        """获取指定数据源的异步会话上下文管理器（动态创建如果不存在）"""
    async def get_raw_session(self, name) -> AsyncSession:
        """直接获取原始会话对象（需要手动管理生命周期，动态创建如果不存在）"""
    async def health_check(self, name, timeout: float = 5.0) -> bool:
        """检查指定数据源的连接健康状态（动态创建如果不存在）。

        Args:
            name (str): 数据源名称
            timeout (float): 检查超时时间（秒）

        Returns:
            bool: 连接健康返回 True，否则 False
        """
    def support_schema(self, name: str) -> bool:
        """判断指定数据源是否支持 schema（委托给 DatabaseEngine）。
        Args:
            name (str): 数据源名称

        Returns:
            bool: 支持 schema 返回 True，否则 False
        """
    async def close_session_factory(self, name: str):
        """关闭指定数据源的会话工厂并释放资源。

        Args:
            name (str): 数据源名称
        """
    async def close_all(self) -> None:
        """关闭所有会话工厂并释放数据库引擎资源。

        应在应用关闭时调用，确保资源正确释放。
        """
    def __del__(self) -> None:
        """析构函数，尝试同步关闭资源"""
    @classmethod
    async def get_async_session(cls, name: str):
        """快捷函数：用于 FastAPI 依赖注入系统。"""
    @classmethod
    async def get_auth_async_session(cls) -> Generator[Incomplete]:
        """快捷函数：用于 FastAPI 依赖注入系统。"""
