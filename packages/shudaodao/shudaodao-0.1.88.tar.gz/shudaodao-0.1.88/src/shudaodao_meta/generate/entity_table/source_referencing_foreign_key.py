#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @License  ：(C)Copyright 2025, 数道智融科技
# @Author   ：Shudaodao Auto Generator
# @Software ：PyCharm
# @Desc     ：SQLModel classes for shudaodao_meta.source_referencing_foreign_key

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import ConfigDict

from sqlalchemy import BigInteger, Boolean, Text

from shudaodao_core import SQLModel, BaseResponse, Field, Relationship, get_primary_id
from ...package_config import PackageConfig

if TYPE_CHECKING:
    from .source_foreign_key import SourceForeignKey
    from .source_schema import SourceSchema
    from .source_table import SourceTable


class SourceReferencingForeignKey(PackageConfig.RegistryModel, table=True):
    """数据库对象模型"""

    __tablename__ = "source_referencing_foreign_key"
    __table_args__ = {"schema": PackageConfig.SchemaTable, "comment": "引用当前表的外键"}
    # 仅用于内部处理
    __database_schema__ = PackageConfig.SchemaName
    __primary_key__ = ["source_referencing_foreign_key_id"]

    source_referencing_foreign_key_id: int = Field(
        default_factory=get_primary_id, primary_key=True, sa_type=BigInteger, description="主键"
    )
    source_schema_id: int = Field(
        foreign_key=f"{PackageConfig.SchemaForeignKey}source_schema.source_schema_id",
        ondelete="CASCADE",
        sa_type=BigInteger,
        description="数据库模式",
    )
    source_foreign_key_id: int = Field(
        foreign_key=f"{PackageConfig.SchemaForeignKey}source_foreign_key.source_foreign_key_id",
        ondelete="CASCADE",
        sa_type=BigInteger,
        description="主键",
    )
    source_table_id: int = Field(
        foreign_key=f"{PackageConfig.SchemaForeignKey}source_table.source_table_id",
        ondelete="CASCADE",
        sa_type=BigInteger,
        description="表",
    )
    name: Optional[str] = Field(default=None, nullable=True, max_length=255, description="约束名称")
    unique: bool = Field(sa_type=Boolean, description="是否唯一")
    constrained_schema: Optional[str] = Field(
        default=None, nullable=True, max_length=128, description="当前架构"
    )
    constrained_table: Optional[str] = Field(
        default=None, nullable=True, max_length=255, description="当前表"
    )
    constrained_columns: str = Field(max_length=255, description="当前字段集合")
    referred_schema: Optional[str] = Field(
        default=None, nullable=True, max_length=128, description="引用架构"
    )
    referred_table: str = Field(max_length=255, description="引用表")
    referred_columns: Optional[str] = Field(
        default=None, sa_type=Text, nullable=True, description="引用字段集合"
    )
    referred_orderby: Optional[bool] = Field(
        default=None, sa_type=Boolean, nullable=True, description="包含排序字段"
    )
    options: Optional[str] = Field(default=None, nullable=True, max_length=255, description="行为选项")
    sort_order: int = Field(description="排序权重")
    description: Optional[str] = Field(default=None, nullable=True, max_length=500, description="描述")
    create_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="创建人")
    create_at: Optional[datetime] = Field(default=None, nullable=True, description="创建日期")
    update_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="修改人")
    update_at: Optional[datetime] = Field(default=None, nullable=True, description="修改日期")
    # 反向关系 - 父对象
    SourceForeignKey: "SourceForeignKey" = Relationship(back_populates="SourceReferencingForeignKeys")
    # 反向关系 - 父对象
    SourceSchema: "SourceSchema" = Relationship(back_populates="SourceReferencingForeignKeys")
    # 反向关系 - 父对象
    SourceTable: "SourceTable" = Relationship(back_populates="SourceReferencingForeignKeys")


class SourceReferencingForeignKeyCreate(SQLModel):
    """前端创建模型 - 用于接口请求"""

    source_schema_id: int = Field(sa_type=BigInteger, description="数据库模式")
    source_foreign_key_id: int = Field(sa_type=BigInteger, description="主键")
    source_table_id: int = Field(sa_type=BigInteger, description="表")
    name: Optional[str] = Field(default=None, max_length=255, description="约束名称")
    unique: bool = Field(description="是否唯一")
    constrained_schema: Optional[str] = Field(default=None, max_length=128, description="当前架构")
    constrained_table: Optional[str] = Field(default=None, max_length=255, description="当前表")
    constrained_columns: str = Field(max_length=255, description="当前字段集合")
    referred_schema: Optional[str] = Field(default=None, max_length=128, description="引用架构")
    referred_table: str = Field(max_length=255, description="引用表")
    referred_columns: Optional[str] = Field(default=None, description="引用字段集合")
    referred_orderby: Optional[bool] = Field(default=None, description="包含排序字段")
    options: Optional[str] = Field(default=None, max_length=255, description="行为选项")
    sort_order: int = Field(description="排序权重")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")

    model_config = ConfigDict(populate_by_name=True)


class SourceReferencingForeignKeyUpdate(SQLModel):
    """前端更新模型 - 用于接口请求"""

    source_referencing_foreign_key_id: Optional[int] = Field(
        default=None, sa_type=BigInteger, description="主键"
    )
    source_schema_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="数据库模式")
    source_foreign_key_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="主键")
    source_table_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="表")
    name: Optional[str] = Field(default=None, max_length=255, description="约束名称")
    unique: Optional[bool] = Field(default=None, description="是否唯一")
    constrained_schema: Optional[str] = Field(default=None, max_length=128, description="当前架构")
    constrained_table: Optional[str] = Field(default=None, max_length=255, description="当前表")
    constrained_columns: Optional[str] = Field(default=None, max_length=255, description="当前字段集合")
    referred_schema: Optional[str] = Field(default=None, max_length=128, description="引用架构")
    referred_table: Optional[str] = Field(default=None, max_length=255, description="引用表")
    referred_columns: Optional[str] = Field(default=None, description="引用字段集合")
    referred_orderby: Optional[bool] = Field(default=None, description="包含排序字段")
    options: Optional[str] = Field(default=None, max_length=255, description="行为选项")
    sort_order: Optional[int] = Field(default=None, description="排序权重")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")

    model_config = ConfigDict(populate_by_name=True)


class SourceReferencingForeignKeyResponse(BaseResponse):
    """前端响应模型 - 用于接口响应"""

    __database_schema__ = PackageConfig.SchemaName  # 仅用于内部处理
    source_referencing_foreign_key_id: int = Field(description="主键", sa_type=BigInteger)
    source_schema_id: int = Field(description="数据库模式", sa_type=BigInteger)
    source_foreign_key_id: int = Field(description="主键", sa_type=BigInteger)
    source_table_id: int = Field(description="表", sa_type=BigInteger)
    name: Optional[str] = Field(description="约束名称", default=None)
    unique: bool = Field(description="是否唯一")
    constrained_schema: Optional[str] = Field(description="当前架构", default=None)
    constrained_table: Optional[str] = Field(description="当前表", default=None)
    constrained_columns: str = Field(description="当前字段集合")
    referred_schema: Optional[str] = Field(description="引用架构", default=None)
    referred_table: str = Field(description="引用表")
    referred_columns: Optional[str] = Field(description="引用字段集合", default=None)
    referred_orderby: Optional[bool] = Field(description="包含排序字段", default=None)
    options: Optional[str] = Field(description="行为选项", default=None)
    sort_order: int = Field(description="排序权重")
    description: Optional[str] = Field(description="描述", default=None)
    create_by: Optional[str] = Field(description="创建人", default=None)
    create_at: Optional[datetime] = Field(description="创建日期", default=None)
    update_by: Optional[str] = Field(description="修改人", default=None)
    update_at: Optional[datetime] = Field(description="修改日期", default=None)

    model_config = ConfigDict(populate_by_name=True)
