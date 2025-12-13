#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @License  ：(C)Copyright 2025, 数道智融科技
# @Author   ：李锋
# @Software ：PyCharm
# @Date     ：2025/8/26 下午12:11
# @Desc     ：

# 其他类库的引用
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import Relationship, SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from .config.app_config import AppConfig
from .config.running_config import RunningConfig
from .engine.database_engine import DatabaseEngine
from .engine.disk_engine import DiskEngine
from .engine.redis_engine import RedisEngine
from .enums.clazz_int import EnumInt
from .enums.clazz_str import EnumStr
from .exception.service_exception import (
    AuthError,
    ValidError,
    PermError,
    ServiceError,
    DataNotFoundException,
)
from .logger.logging_ import logging
from .package.config_setting import PackageConfigSetting
from .schemas.query_request import QueryRequest
from .schemas.response import BaseResponse
from .services.data_service import DataService
from .services.query_service import QueryService
from .services.session_service import AsyncSessionService
from .sqlmodel_ext.field import Field
from .utils.core_utils import CoreUtil
from .utils.generate_unique_id import get_primary_str, get_primary_id
from .utils.response_utils import ResponseUtil
from .enums.manager import EnumManager

__all__ = [
    # FastAPI & SQLModel 快捷导出
    "Depends",
    "SQLModel",
    "Relationship",
    "create_engine",
    "create_async_engine",
    "AsyncSession",
    "Field",  # SQLModel.Field 的封装

    # 核心应用与配置
    "RunningConfig",
    "AppConfig",
    "PackageConfigSetting",

    # 引擎
    "DatabaseEngine",
    "DiskEngine",
    "RedisEngine",

    # 枚举
    "EnumStr",
    "EnumInt",
    "EnumManager",

    # 异常
    "AuthError",
    "ValidError",
    "PermError",
    "ServiceError",
    "DataNotFoundException",

    # 日志
    "logging",

    # 请求与响应
    "QueryRequest",
    "BaseResponse",

    # 服务类
    "DataService",
    "QueryService",
    "AsyncSessionService",

    # 工具类与函数
    "CoreUtil",
    "ResponseUtil",
    "get_primary_str",
    "get_primary_id",
]
