#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @License  ：(C)Copyright 2025, 数道智融科技
# @Author   ：李锋
# @Software ：PyCharm
# @Date     ：2025/11/9 下午8:38
# @Desc     ：

from typing import Union, List

from fastapi import Path

from shudaodao_auth import AuthAPIRouter
from shudaodao_core import QueryRequest
from shudaodao_meta.package_config import PackageConfig
from ..services.generic_service_v2 import GenericServiceV2

generic_router = AuthAPIRouter(
    prefix=f"/v2",
    db_engine_name=PackageConfig.EngineName,
    tags=["通用接口 - 增删改查 v2 - 支持批量操作以及更高级的查询"],
)


@generic_router.post(
    path="/{schema_path}/{entity_path}/create", summary="创建 schema - table/view 的数据，支持同时添加多条记录")
async def create_route(
        create_models: Union[dict, List[dict]],
        schema_path: str = Path(description="数据库模式名称/别名"),
        entity_path: str = Path(description="数据库实体名称/别名"),
):
    return await GenericServiceV2.create(
        schema_path=schema_path, entity_path=entity_path,
        create_models=create_models,
    )


@generic_router.post(
    path="/{schema_path}/{entity_path}/read", summary="获取 schema - table/view 的数据，支持同时获取多条记录")
async def read_route(
        read_models: Union[dict, List[dict]],
        schema_path: str = Path(description="数据库模式名称/别名"),
        entity_path: str = Path(description="数据库实体名称/别名"),
):
    return await GenericServiceV2.read(
        schema_path=schema_path, entity_path=entity_path,
        read_models=read_models,
    )


@generic_router.post(
    path="/{schema_path}/{entity_path}/update", summary="更新 schema - table/view 的数据，支持同时更新多条记录")
async def update_route(
        create_models: Union[dict, List[dict]],
        schema_path: str = Path(description="数据库模式名称/别名"),
        entity_path: str = Path(description="数据库实体名称/别名"),
):
    return await GenericServiceV2.update(
        schema_path=schema_path, entity_path=entity_path,
        update_models=create_models,
    )


@generic_router.post(
    path="/{schema_path}/{entity_path}/delete", summary="删除 schema - table/view 的数据，支持同时删除多条记录")
async def delete_route(
        delete_models: Union[dict, List[dict]],
        schema_path: str = Path(description="数据库模式名称/别名"),
        entity_path: str = Path(description="数据库实体名称/别名"),
):
    return await GenericServiceV2.delete(
        schema_path=schema_path, entity_path=entity_path,
        delete_models=delete_models,
    )


@generic_router.post(path="/{schema_path}/{entity_path}/query", summary="查询 schema - table/view 的数据，支持关系查询")
async def query_route(
        query_request: QueryRequest,
        schema_path: str = Path(description="数据库模式名称/别名"),
        entity_path: str = Path(description="数据库实体名称/别名"),
):
    return await GenericServiceV2.query(
        schema_path=schema_path, entity_path=entity_path,
        query_request=query_request,
    )
