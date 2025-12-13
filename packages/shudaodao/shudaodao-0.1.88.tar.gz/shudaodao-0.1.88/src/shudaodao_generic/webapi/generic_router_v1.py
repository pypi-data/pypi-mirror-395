#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @License  ：(C)Copyright 2025, 数道智融科技
# @Author   ：李锋
# @Software ：PyCharm
# @Date     ：2025/11/9 下午8:38
# @Desc     ：

from typing import Optional

from fastapi import Path

from shudaodao_auth import AuthAPIRouter
from shudaodao_meta.package_config import PackageConfig
from ..services.generic_service_v1 import GenericServiceV1

generic_router = AuthAPIRouter(
    prefix=f"/v1",
    db_engine_name=PackageConfig.EngineName,
    tags=["通用接口 - 增删改查 v1 - 标准功能，更倾向去兼容java版接口"],
)


@generic_router.post(path="/{schema_path}/{entity_path}/create", summary="创建 schema - table/view 的数据")
async def create_route(
        create_model: dict,
        schema_path: str = Path(description="数据库模式名称/别名"),
        entity_path: str = Path(description="数据库实体名称/别名"),
):
    return await GenericServiceV1.create(
        schema_path=schema_path, entity_path=entity_path,
        create_models=create_model,
    )


@generic_router.get(
    path="/{schema_path}/{entity_path}/{primary_id}/read", summary="获取 schema - table/view 的数据")
async def read_route(
        primary_id: Optional[int] = Path(description="主键ID值]"),
        schema_path: str = Path(description="数据库模式名称/别名"),
        entity_path: str = Path(description="数据库实体名称/别名"),
):
    return await GenericServiceV1.read(
        schema_path=schema_path, entity_path=entity_path,
        primary_id=primary_id
    )


@generic_router.post(
    path="/{schema_path}/{entity_path}/{primary_id}/update", summary="更新 schema - table/view 的数据")
async def update_route(
        update_models: dict,
        primary_id: Optional[int] = Path(description="主键ID值,int或List[int]"),
        schema_path: str = Path(description="数据库模式名称/别名"),
        entity_path: str = Path(description="数据库实体名称/别名"),
):
    return await GenericServiceV1.update(
        schema_path=schema_path, entity_path=entity_path,
        primary_id=primary_id, update_models=update_models
    )


@generic_router.post(
    path="/{schema_path}/{entity_path}/{primary_id}/delete", summary="获取 schema - table/view 的数据")
async def delete_route(
        primary_id: Optional[int] = Path(description="主键ID值]"),
        schema_path: str = Path(description="数据库模式名称/别名"),
        entity_path: str = Path(description="数据库实体名称/别名"),
):
    return await GenericServiceV1.delete(
        schema_path=schema_path, entity_path=entity_path,
        primary_id=primary_id,
    )
