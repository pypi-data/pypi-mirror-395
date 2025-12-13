#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @License  ：(C)Copyright 2025, 数道智融科技
# @Author   ：李锋
# @Software ：PyCharm
# @Date     ：2025/10/22 下午9:25
# @Desc     ：

from fastapi import Path
from sqlmodel.ext.asyncio.session import AsyncSession

from shudaodao_auth import AuthAPIRouter
from shudaodao_core import Depends, ResponseUtil
from ..package_config import PackageConfig
from ..schema.enum import EnumQueryRequest
from ..tools.enum_query import EnumQuery

Meta_Enum_Router = AuthAPIRouter(
    prefix=f"/{PackageConfig.RouterPath}/enums",
    tags=[f"{PackageConfig.RouterTags} - 字典枚举"],
    db_engine_name=PackageConfig.EngineName,  # 配置文件中的数据库连接名称
)


@Meta_Enum_Router.post(path="/{schema_name}/fields", summary=["获取schema下所有枚举字段"])
async def query_schema(
        schema_name: str = Path(description="模式名称"),
        db: AsyncSession = Depends(Meta_Enum_Router.get_async_session)
):
    query_result = await EnumQuery.query_schema(
        db=db, schema_name=schema_name
    )
    return ResponseUtil.success(message="查询成功", data=query_result)


@Meta_Enum_Router.post(path="/{schema_name}/values", summary=["获取schema下指定单个或多个字段的枚举值"])
async def query_field(
        quest_request: EnumQueryRequest, schema_name: str = Path(description="模式名称"),
        db: AsyncSession = Depends(Meta_Enum_Router.get_async_session)
):
    query_result = await EnumQuery.query_field(
        db=db, schema_name=schema_name, quest_request=quest_request
    )
    return ResponseUtil.success(message="查询成功", data=query_result)
