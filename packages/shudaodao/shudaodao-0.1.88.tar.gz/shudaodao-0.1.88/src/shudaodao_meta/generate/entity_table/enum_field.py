#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @License  ：(C)Copyright 2025, 数道智融科技
# @Author   ：Shudaodao Auto Generator
# @Software ：PyCharm
# @Desc     ：SQLModel classes for shudaodao_meta.enum_field

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import ConfigDict

from sqlalchemy import BigInteger, Boolean

from shudaodao_core import SQLModel, BaseResponse, Field, Relationship, get_primary_id
from ...package_config import PackageConfig

if TYPE_CHECKING:
    from .enum_value import EnumValue


class EnumField(PackageConfig.RegistryModel, table=True):
    """数据库对象模型"""

    __tablename__ = "enum_field"
    __table_args__ = {"schema": PackageConfig.SchemaTable, "comment": "枚举字段表"}
    # 仅用于内部处理
    __database_schema__ = PackageConfig.SchemaName
    __primary_key__ = ["field_id"]

    field_id: int = Field(
        default_factory=get_primary_id, primary_key=True, sa_type=BigInteger, description="主键"
    )
    meta_schema_id: int = Field(sa_type=BigInteger, description="主键")
    field_label: str = Field(max_length=50, description="字段标签")
    field_name: str = Field(max_length=50, description="字段列名")
    description: Optional[str] = Field(default=None, nullable=True, max_length=500, description="描述")
    is_active: bool = Field(sa_type=Boolean, description="启用状态")
    sort_order: int = Field(description="排序权重")
    create_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="创建人")
    create_at: Optional[datetime] = Field(default=None, nullable=True, description="创建日期")
    update_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="修改人")
    update_at: Optional[datetime] = Field(default=None, nullable=True, description="修改日期")
    tenant_id: Optional[int] = Field(default=None, sa_type=BigInteger, nullable=True, description="主键")
    # 正向关系 - 子对象
    EnumValues: list["EnumValue"] = Relationship(
        back_populates="EnumField",
        cascade_delete=True,
        sa_relationship_kwargs={"order_by": "EnumValue.sort_order.asc()"},
    )


class EnumFieldCreate(SQLModel):
    """前端创建模型 - 用于接口请求"""

    meta_schema_id: int = Field(sa_type=BigInteger, description="主键")
    field_label: str = Field(max_length=50, description="字段标签")
    field_name: str = Field(max_length=50, description="字段列名")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")
    is_active: bool = Field(description="启用状态")
    sort_order: int = Field(description="排序权重")

    model_config = ConfigDict(populate_by_name=True)


class EnumFieldUpdate(SQLModel):
    """前端更新模型 - 用于接口请求"""

    field_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="主键")
    meta_schema_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="主键")
    field_label: Optional[str] = Field(default=None, max_length=50, description="字段标签")
    field_name: Optional[str] = Field(default=None, max_length=50, description="字段列名")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")
    is_active: Optional[bool] = Field(default=None, description="启用状态")
    sort_order: Optional[int] = Field(default=None, description="排序权重")

    model_config = ConfigDict(populate_by_name=True)


class EnumFieldResponse(BaseResponse):
    """前端响应模型 - 用于接口响应"""

    __database_schema__ = PackageConfig.SchemaName  # 仅用于内部处理
    field_id: int = Field(description="主键", sa_type=BigInteger)
    meta_schema_id: int = Field(description="主键", sa_type=BigInteger)
    field_label: str = Field(description="字段标签")
    field_name: str = Field(description="字段列名")
    description: Optional[str] = Field(description="描述", default=None)
    is_active: bool = Field(description="启用状态")
    sort_order: int = Field(description="排序权重")
    create_by: Optional[str] = Field(description="创建人", default=None)
    create_at: Optional[datetime] = Field(description="创建日期", default=None)
    update_by: Optional[str] = Field(description="修改人", default=None)
    update_at: Optional[datetime] = Field(description="修改日期", default=None)

    model_config = ConfigDict(populate_by_name=True)
