#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @License  ：(C)Copyright 2025, 数道智融科技
# @Author   ：Shudaodao Auto Generator
# @Software ：PyCharm
# @Desc     ：SQLModel classes for shudaodao_meta.meta_table

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import ConfigDict

from sqlalchemy import BigInteger, Text, Boolean

from shudaodao_core import SQLModel, BaseResponse, Field, Relationship, get_primary_id
from ...package_config import PackageConfig

if TYPE_CHECKING:
    from .meta_column import MetaColumn
    from .meta_constraint import MetaConstraint
    from .meta_schema import MetaSchema


class MetaTable(PackageConfig.RegistryModel, table=True):
    """数据库对象模型"""

    __tablename__ = "meta_table"
    __table_args__ = {"schema": PackageConfig.SchemaTable, "comment": "表元数据"}
    # 仅用于内部处理
    __database_schema__ = PackageConfig.SchemaName
    __primary_key__ = ["meta_table_id"]

    meta_table_id: int = Field(
        default_factory=get_primary_id, primary_key=True, sa_type=BigInteger, description="主键"
    )
    meta_schema_id: int = Field(
        foreign_key=f"{PackageConfig.SchemaForeignKey}meta_schema.meta_schema_id",
        ondelete="CASCADE",
        sa_type=BigInteger,
        description="主键",
    )
    table_name: str = Field(max_length=255, description="表名字")
    router_path: str = Field(max_length=128, description="API路由名")
    comment: Optional[str] = Field(default=None, sa_type=Text, nullable=True, description="备注")
    class_name: Optional[str] = Field(default=None, nullable=True, max_length=50, description="类名")
    default_column: Optional[str] = Field(default=None, nullable=True, max_length=64, description="默认列")
    api_acts: Optional[str] = Field(default=None, nullable=True, max_length=128, description="接口操作集合")
    is_active: bool = Field(sa_type=Boolean, description="启用状态")
    sort_order: int = Field(description="排序权重")
    description: Optional[str] = Field(default=None, nullable=True, max_length=500, description="描述")
    create_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="创建人")
    create_at: Optional[datetime] = Field(default=None, nullable=True, description="创建日期")
    update_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="修改人")
    update_at: Optional[datetime] = Field(default=None, nullable=True, description="修改日期")
    # 反向关系 - 父对象
    MetaSchema: "MetaSchema" = Relationship(back_populates="MetaTables")
    # 正向关系 - 子对象
    MetaColumns: list["MetaColumn"] = Relationship(
        back_populates="MetaTable",
        cascade_delete=True,
        sa_relationship_kwargs={"order_by": "MetaColumn.sort_order.asc()"},
    )
    # 正向关系 - 子对象
    MetaConstraints: list["MetaConstraint"] = Relationship(
        back_populates="MetaTable",
        cascade_delete=True,
        sa_relationship_kwargs={"order_by": "MetaConstraint.sort_order.asc()"},
    )


class MetaTableCreate(SQLModel):
    """前端创建模型 - 用于接口请求"""

    meta_schema_id: int = Field(sa_type=BigInteger, description="主键")
    table_name: str = Field(max_length=255, description="表名字")
    router_path: str = Field(max_length=128, description="API路由名")
    comment: Optional[str] = Field(default=None, description="备注")
    class_name: Optional[str] = Field(default=None, max_length=50, description="类名")
    default_column: Optional[str] = Field(default=None, max_length=64, description="默认列")
    api_acts: Optional[str] = Field(default=None, max_length=128, description="接口操作集合")
    is_active: bool = Field(description="启用状态")
    sort_order: int = Field(description="排序权重")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")

    model_config = ConfigDict(populate_by_name=True)


class MetaTableUpdate(SQLModel):
    """前端更新模型 - 用于接口请求"""

    meta_table_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="主键")
    meta_schema_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="主键")
    table_name: Optional[str] = Field(default=None, max_length=255, description="表名字")
    router_path: Optional[str] = Field(default=None, max_length=128, description="API路由名")
    comment: Optional[str] = Field(default=None, description="备注")
    class_name: Optional[str] = Field(default=None, max_length=50, description="类名")
    default_column: Optional[str] = Field(default=None, max_length=64, description="默认列")
    api_acts: Optional[str] = Field(default=None, max_length=128, description="接口操作集合")
    is_active: Optional[bool] = Field(default=None, description="启用状态")
    sort_order: Optional[int] = Field(default=None, description="排序权重")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")

    model_config = ConfigDict(populate_by_name=True)


class MetaTableResponse(BaseResponse):
    """前端响应模型 - 用于接口响应"""

    __database_schema__ = PackageConfig.SchemaName  # 仅用于内部处理
    meta_table_id: int = Field(description="主键", sa_type=BigInteger)
    meta_schema_id: int = Field(description="主键", sa_type=BigInteger)
    table_name: str = Field(description="表名字")
    router_path: str = Field(description="API路由名")
    comment: Optional[str] = Field(description="备注", default=None)
    class_name: Optional[str] = Field(description="类名", default=None)
    default_column: Optional[str] = Field(description="默认列", default=None)
    api_acts: Optional[str] = Field(description="接口操作集合", default=None)
    is_active: bool = Field(description="启用状态")
    sort_order: int = Field(description="排序权重")
    description: Optional[str] = Field(description="描述", default=None)
    create_by: Optional[str] = Field(description="创建人", default=None)
    create_at: Optional[datetime] = Field(description="创建日期", default=None)
    update_by: Optional[str] = Field(description="修改人", default=None)
    update_at: Optional[datetime] = Field(description="修改日期", default=None)

    model_config = ConfigDict(populate_by_name=True)
