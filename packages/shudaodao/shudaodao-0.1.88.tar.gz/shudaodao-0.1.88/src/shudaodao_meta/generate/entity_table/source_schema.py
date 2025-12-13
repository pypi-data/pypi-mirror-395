#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @License  ：(C)Copyright 2025, 数道智融科技
# @Author   ：Shudaodao Auto Generator
# @Software ：PyCharm
# @Desc     ：SQLModel classes for shudaodao_meta.source_schema

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import ConfigDict

from sqlalchemy import BigInteger

from shudaodao_core import SQLModel, BaseResponse, Field, Relationship, get_primary_id
from ...package_config import PackageConfig

if TYPE_CHECKING:
    from .source_referencing_foreign_key import SourceReferencingForeignKey
    from .source_table import SourceTable
    from .source_view import SourceView


class SourceSchema(PackageConfig.RegistryModel, table=True):
    """数据库对象模型"""

    __tablename__ = "source_schema"
    __table_args__ = {"schema": PackageConfig.SchemaTable, "comment": "模式(schema)"}
    # 仅用于内部处理
    __database_schema__ = PackageConfig.SchemaName
    __primary_key__ = ["source_schema_id"]

    source_schema_id: int = Field(
        default_factory=get_primary_id, primary_key=True, sa_type=BigInteger, description="主键"
    )
    schema_label: Optional[str] = Field(default=None, nullable=True, max_length=128, description="架构中文")
    schema_name: str = Field(max_length=128, description="数据库模式")
    engine_name: str = Field(max_length=128, description="数据引擎名")
    sort_order: int = Field(description="排序权重")
    description: Optional[str] = Field(default=None, nullable=True, max_length=500, description="描述")
    create_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="创建人")
    create_at: Optional[datetime] = Field(default=None, nullable=True, description="创建日期")
    update_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="修改人")
    update_at: Optional[datetime] = Field(default=None, nullable=True, description="修改日期")
    # 正向关系 - 子对象
    SourceReferencingForeignKeys: list["SourceReferencingForeignKey"] = Relationship(
        back_populates="SourceSchema",
        cascade_delete=True,
        sa_relationship_kwargs={"order_by": "SourceReferencingForeignKey.sort_order.asc()"},
    )
    # 正向关系 - 子对象
    SourceTables: list["SourceTable"] = Relationship(
        back_populates="SourceSchema",
        cascade_delete=True,
        sa_relationship_kwargs={"order_by": "SourceTable.sort_order.asc()"},
    )
    # 正向关系 - 子对象
    SourceViews: list["SourceView"] = Relationship(
        back_populates="SourceSchema",
        cascade_delete=True,
        sa_relationship_kwargs={"order_by": "SourceView.sort_order.asc()"},
    )


class SourceSchemaCreate(SQLModel):
    """前端创建模型 - 用于接口请求"""

    schema_label: Optional[str] = Field(default=None, max_length=128, description="架构中文")
    schema_name: str = Field(max_length=128, description="数据库模式")
    engine_name: str = Field(max_length=128, description="数据引擎名")
    sort_order: int = Field(description="排序权重")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")

    model_config = ConfigDict(populate_by_name=True)


class SourceSchemaUpdate(SQLModel):
    """前端更新模型 - 用于接口请求"""

    source_schema_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="主键")
    schema_label: Optional[str] = Field(default=None, max_length=128, description="架构中文")
    schema_name: Optional[str] = Field(default=None, max_length=128, description="数据库模式")
    engine_name: Optional[str] = Field(default=None, max_length=128, description="数据引擎名")
    sort_order: Optional[int] = Field(default=None, description="排序权重")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")

    model_config = ConfigDict(populate_by_name=True)


class SourceSchemaResponse(BaseResponse):
    """前端响应模型 - 用于接口响应"""

    __database_schema__ = PackageConfig.SchemaName  # 仅用于内部处理
    source_schema_id: int = Field(description="主键", sa_type=BigInteger)
    schema_label: Optional[str] = Field(description="架构中文", default=None)
    schema_name: str = Field(description="数据库模式")
    engine_name: str = Field(description="数据引擎名")
    sort_order: int = Field(description="排序权重")
    description: Optional[str] = Field(description="描述", default=None)
    create_by: Optional[str] = Field(description="创建人", default=None)
    create_at: Optional[datetime] = Field(description="创建日期", default=None)
    update_by: Optional[str] = Field(description="修改人", default=None)
    update_at: Optional[datetime] = Field(description="修改日期", default=None)

    model_config = ConfigDict(populate_by_name=True)
