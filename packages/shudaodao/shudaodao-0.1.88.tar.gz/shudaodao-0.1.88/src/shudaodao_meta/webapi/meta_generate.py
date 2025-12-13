#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @License  ：(C)Copyright 2025, 数道智融科技
# @Author   ：李锋
# @Software ：PyCharm
# @Date     ：2025/10/25 下午6:42
# @Desc     ：


from fastapi import Path
from sqlmodel.ext.asyncio.session import AsyncSession

from shudaodao_auth import AuthAPIRouter
from shudaodao_core import Depends, ResponseUtil
from ..package_config import PackageConfig
from ..tools.meta_template import MetaTemplate

Meta_Generate_Router = AuthAPIRouter(
    prefix=f"/{PackageConfig.RouterPath}",
    tags=[f"{PackageConfig.RouterTags} - 生成代码"],
    db_engine_name=PackageConfig.EngineName,
    auth_role="admin",
)


@Meta_Generate_Router.post(
    path="/schemas/{schema_name}/tables/{table_name}/generate",
    summary=["生成 schema - table 代码"]
)
async def schemas_tables_generate(
        schema_name: str = Path(description="数据库模式(schema)"), table_name: str = Path(description="表名"),
        db: AsyncSession = Depends(Meta_Generate_Router.get_async_session)
):
    return ResponseUtil.success(
        message=f"生成表 {table_name} 代码成功",
        data=await MetaTemplate(db=db).render_table(schema_name, table_name, [])
    )


@Meta_Generate_Router.post(
    path="/schemas/{schema_name}/views/{view_name}/generate",  summary=["生成 schema - view 代码"]
)
async def schemas_views_generate(
        schema_name: str = Path(description="数据库模式(schema)"), view_name: str = Path(description="视图名"),
        db: AsyncSession = Depends(Meta_Generate_Router.get_async_session)
):
    return ResponseUtil.success(
        message=f"生成视图 {view_name} 代码成功",
        data=await MetaTemplate(db=db).render_view(schema_name, view_name, [""])
    )


@Meta_Generate_Router.post(
    path="/schemas/{schema_name}/generate", auth_role="admin", summary=["生成 schema - 全部代码"]
)
async def schemas_views_generate(
        schema_name: str = Path(description="数据库模式(schema)"),
        *, db: AsyncSession = Depends(Meta_Generate_Router.get_async_session)
):
    return ResponseUtil.success(
        message="生成模式代码成功",
        data=await MetaTemplate(db=db).render_schema(schema_name)
    )
