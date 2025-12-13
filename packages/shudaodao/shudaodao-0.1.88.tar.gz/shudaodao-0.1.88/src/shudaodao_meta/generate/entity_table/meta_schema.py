#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @License  ：(C)Copyright 2025, 数道智融科技
# @Author   ：Shudaodao Auto Generator
# @Software ：PyCharm
# @Desc     ：SQLModel classes for shudaodao_meta.meta_schema

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import ConfigDict

from sqlalchemy import BigInteger, Boolean

from shudaodao_core import SQLModel, BaseResponse, Field, Relationship, get_primary_id
from ...package_config import PackageConfig

if TYPE_CHECKING:
    from .meta_table import MetaTable
    from .meta_view import MetaView


class MetaSchema(PackageConfig.RegistryModel, table=True):
    """数据库对象模型"""

    __tablename__ = "meta_schema"
    __table_args__ = {"schema": PackageConfig.SchemaTable, "comment": "代码元数据"}
    # 仅用于内部处理
    __database_schema__ = PackageConfig.SchemaName
    __primary_key__ = ["meta_schema_id"]

    meta_schema_id: int = Field(
        default_factory=get_primary_id, primary_key=True, sa_type=BigInteger, description="主键"
    )
    schema_label: Optional[str] = Field(
        default=None, nullable=True, max_length=128, description="数据库-模式标签"
    )
    schema_name: str = Field(max_length=128, description="数据库-模式(schema)")
    engine_name: Optional[str] = Field(
        default=None, nullable=True, max_length=128, description="数据库-配置名称"
    )
    router_path: Optional[str] = Field(
        default=None, nullable=True, max_length=128, description="API路由-路径名称"
    )
    router_tags: Optional[str] = Field(
        default=None, nullable=True, max_length=256, description="API路由-分组标签"
    )
    output_frontend: Optional[str] = Field(
        default=None, nullable=True, max_length=256, description="前端路径"
    )
    output_backend: Optional[str] = Field(default=None, nullable=True, max_length=256, description="后端路径")
    sort_order: int = Field(description="排序权重")
    is_active: Optional[bool] = Field(default=None, sa_type=Boolean, nullable=True, description="是否启用")
    description: Optional[str] = Field(default=None, nullable=True, max_length=500, description="描述")
    create_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="创建人")
    create_at: Optional[datetime] = Field(default=None, nullable=True, description="创建日期")
    update_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="修改人")
    update_at: Optional[datetime] = Field(default=None, nullable=True, description="修改日期")
    # 正向关系 - 子对象
    MetaTables: list["MetaTable"] = Relationship(
        back_populates="MetaSchema",
        cascade_delete=True,
        sa_relationship_kwargs={"order_by": "MetaTable.sort_order.asc()"},
    )
    # 正向关系 - 子对象
    MetaViews: list["MetaView"] = Relationship(
        back_populates="MetaSchema",
        cascade_delete=True,
        sa_relationship_kwargs={"order_by": "MetaView.sort_order.asc()"},
    )


class MetaSchemaCreate(SQLModel):
    """前端创建模型 - 用于接口请求"""

    schema_label: Optional[str] = Field(default=None, max_length=128, description="数据库-模式标签")
    schema_name: str = Field(max_length=128, description="数据库-模式(schema)")
    engine_name: Optional[str] = Field(default=None, max_length=128, description="数据库-配置名称")
    router_path: Optional[str] = Field(default=None, max_length=128, description="API路由-路径名称")
    router_tags: Optional[str] = Field(default=None, max_length=256, description="API路由-分组标签")
    output_frontend: Optional[str] = Field(default=None, max_length=256, description="前端路径")
    output_backend: Optional[str] = Field(default=None, max_length=256, description="后端路径")
    sort_order: int = Field(description="排序权重")
    is_active: Optional[bool] = Field(default=None, description="是否启用")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")

    model_config = ConfigDict(populate_by_name=True)


class MetaSchemaUpdate(SQLModel):
    """前端更新模型 - 用于接口请求"""

    meta_schema_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="主键")
    schema_label: Optional[str] = Field(default=None, max_length=128, description="数据库-模式标签")
    schema_name: Optional[str] = Field(default=None, max_length=128, description="数据库-模式(schema)")
    engine_name: Optional[str] = Field(default=None, max_length=128, description="数据库-配置名称")
    router_path: Optional[str] = Field(default=None, max_length=128, description="API路由-路径名称")
    router_tags: Optional[str] = Field(default=None, max_length=256, description="API路由-分组标签")
    output_frontend: Optional[str] = Field(default=None, max_length=256, description="前端路径")
    output_backend: Optional[str] = Field(default=None, max_length=256, description="后端路径")
    sort_order: Optional[int] = Field(default=None, description="排序权重")
    is_active: Optional[bool] = Field(default=None, description="是否启用")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")

    model_config = ConfigDict(populate_by_name=True)


class MetaSchemaResponse(BaseResponse):
    """前端响应模型 - 用于接口响应"""

    __database_schema__ = PackageConfig.SchemaName  # 仅用于内部处理
    meta_schema_id: int = Field(description="主键", sa_type=BigInteger)
    schema_label: Optional[str] = Field(description="数据库-模式标签", default=None)
    schema_name: str = Field(description="数据库-模式(schema)")
    engine_name: Optional[str] = Field(description="数据库-配置名称", default=None)
    router_path: Optional[str] = Field(description="API路由-路径名称", default=None)
    router_tags: Optional[str] = Field(description="API路由-分组标签", default=None)
    output_frontend: Optional[str] = Field(description="前端路径", default=None)
    output_backend: Optional[str] = Field(description="后端路径", default=None)
    sort_order: int = Field(description="排序权重")
    is_active: Optional[bool] = Field(description="是否启用", default=None)
    description: Optional[str] = Field(description="描述", default=None)
    create_by: Optional[str] = Field(description="创建人", default=None)
    create_at: Optional[datetime] = Field(description="创建日期", default=None)
    update_by: Optional[str] = Field(description="修改人", default=None)
    update_at: Optional[datetime] = Field(description="修改日期", default=None)

    model_config = ConfigDict(populate_by_name=True)
