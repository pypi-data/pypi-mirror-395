#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @License  ：(C)Copyright 2025, 数道智融科技
# @Author   ：李锋
# @Software ：PyCharm
# @Date     ：2025/11/13 上午12:58
# @Desc     ：


from fastapi import Path
from sqlmodel.ext.asyncio.session import AsyncSession

from shudaodao_auth import AuthAPIRouter
from shudaodao_core import Depends, ResponseUtil
from ..package_config import PackageConfig
from ..tools.meta_store import MetaStore
from ..tools.source_store import SourceStore

Meta_Source_Router = AuthAPIRouter(
    prefix=f"/{PackageConfig.RouterPath}",
    tags=[f"{PackageConfig.RouterTags} - 数据来源"],
    db_engine_name=PackageConfig.EngineName,  # 配置文件中的数据库连接名称
    auth_role="admin",
    auth_sub=PackageConfig.SchemaName
)


@Meta_Source_Router.get(
    path="/sources/{sources_engine}/schemas/{schema_name}/discover",
    summary=["获取(不保存)数据库元数据"], auth_obj="source", auth_act="query",
)
async def sources_discover(
        sources_engine: str = Path(description="数据库配置名称"),
        schema_name: str = Path(description="数据库模式(schema)"),
        *, db: AsyncSession = Depends(Meta_Source_Router.get_async_session)
):
    meta_store = SourceStore(db=db, engine_name=sources_engine, schema_name=schema_name)
    inspector_dict = meta_store.inspect()
    return ResponseUtil.success(message="获取元数据成功", data=inspector_dict)


@Meta_Source_Router.post(
    path="/sources/{sources_engine}/schemas/{schema_name}/sync",
    summary=["同步(获取+保存)元数据原始来源 - 从 数据库 database 同步到 原始来源"]
)
async def sources_sync(
        sources_engine: str = Path(description="数据库配置名称"),
        schema_name: str = Path(description="数据库模式(schema)"),
        *, db: AsyncSession = Depends(Meta_Source_Router.get_async_session)
):
    meta_store = SourceStore(db=db, engine_name=sources_engine, schema_name=schema_name)
    inspector_dict = meta_store.inspect()
    await meta_store.save_meta(metadata=inspector_dict)
    return ResponseUtil.success(message="同步成功", data=inspector_dict)


@Meta_Source_Router.post(
    path="/schemas/{schema_name}/sync", summary=["同步(获取+保存)元数据 - 从 原始来源 source 同步管理库"]
)
async def schemas_sync(
        schema_name: str = Path(description="数据库模式(schema)"),
        *, db: AsyncSession = Depends(Meta_Source_Router.get_async_session)
):
    sqlmodel_store = MetaStore(db=db, schema_name=schema_name)
    await sqlmodel_store.save_sqlmodel()
    return ResponseUtil.success(message="同步成功")
