#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @License  ：(C)Copyright 2025, 数道智融科技
# @Author   ：Shudaodao Auto Generator
# @Software ：PyCharm
# @Desc     ：SQLModel classes for shudaodao_meta.source_primary_key

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import ConfigDict

from sqlalchemy import BigInteger, Text

from shudaodao_core import SQLModel, BaseResponse, Field, Relationship, get_primary_id
from ...package_config import PackageConfig

if TYPE_CHECKING:
    from .source_table import SourceTable


class SourcePrimaryKey(PackageConfig.RegistryModel, table=True):
    """数据库对象模型"""

    __tablename__ = "source_primary_key"
    __table_args__ = {"schema": PackageConfig.SchemaTable, "comment": "主键表"}
    # 仅用于内部处理
    __database_schema__ = PackageConfig.SchemaName
    __primary_key__ = ["source_primary_id"]

    source_primary_id: int = Field(
        default_factory=get_primary_id, primary_key=True, sa_type=BigInteger, description="主键"
    )
    source_table_id: int = Field(
        foreign_key=f"{PackageConfig.SchemaForeignKey}source_table.source_table_id",
        ondelete="CASCADE",
        sa_type=BigInteger,
        unique=True,
        index=True,
        description="主键",
    )
    name: Optional[str] = Field(default=None, nullable=True, max_length=255, description="约束名字")
    constrained_columns: str = Field(sa_type=Text, description="字段集合")
    description: Optional[str] = Field(default=None, nullable=True, max_length=500, description="描述")
    create_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="创建人")
    create_at: Optional[datetime] = Field(default=None, nullable=True, description="创建日期")
    update_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="修改人")
    update_at: Optional[datetime] = Field(default=None, nullable=True, description="修改日期")
    # 反向关系 - 父对象
    SourceTable: "SourceTable" = Relationship(back_populates="SourcePrimaryKey")


class SourcePrimaryKeyCreate(SQLModel):
    """前端创建模型 - 用于接口请求"""

    source_table_id: int = Field(sa_type=BigInteger, description="主键")
    name: Optional[str] = Field(default=None, max_length=255, description="约束名字")
    constrained_columns: str = Field(description="字段集合")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")

    model_config = ConfigDict(populate_by_name=True)


class SourcePrimaryKeyUpdate(SQLModel):
    """前端更新模型 - 用于接口请求"""

    source_primary_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="主键")
    source_table_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="主键")
    name: Optional[str] = Field(default=None, max_length=255, description="约束名字")
    constrained_columns: Optional[str] = Field(default=None, description="字段集合")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")

    model_config = ConfigDict(populate_by_name=True)


class SourcePrimaryKeyResponse(BaseResponse):
    """前端响应模型 - 用于接口响应"""

    __database_schema__ = PackageConfig.SchemaName  # 仅用于内部处理
    source_primary_id: int = Field(description="主键", sa_type=BigInteger)
    source_table_id: int = Field(description="主键", sa_type=BigInteger)
    name: Optional[str] = Field(description="约束名字", default=None)
    constrained_columns: str = Field(description="字段集合")
    description: Optional[str] = Field(description="描述", default=None)
    create_by: Optional[str] = Field(description="创建人", default=None)
    create_at: Optional[datetime] = Field(description="创建日期", default=None)
    update_by: Optional[str] = Field(description="修改人", default=None)
    update_at: Optional[datetime] = Field(description="修改日期", default=None)

    model_config = ConfigDict(populate_by_name=True)
