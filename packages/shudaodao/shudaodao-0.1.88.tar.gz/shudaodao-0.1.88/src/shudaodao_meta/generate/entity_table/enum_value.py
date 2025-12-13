#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @License  ：(C)Copyright 2025, 数道智融科技
# @Author   ：Shudaodao Auto Generator
# @Software ：PyCharm
# @Desc     ：SQLModel classes for shudaodao_meta.enum_value

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import ConfigDict

from sqlalchemy import BigInteger, Boolean

from shudaodao_core import SQLModel, BaseResponse, Field, Relationship, get_primary_id
from ...package_config import PackageConfig

if TYPE_CHECKING:
    from .enum_field import EnumField


class EnumValue(PackageConfig.RegistryModel, table=True):
    """数据库对象模型"""

    __tablename__ = "enum_value"
    __table_args__ = {"schema": PackageConfig.SchemaTable, "comment": "枚举值表"}
    # 仅用于内部处理
    __database_schema__ = PackageConfig.SchemaName
    __primary_key__ = ["enum_id"]

    enum_id: int = Field(
        default_factory=get_primary_id, primary_key=True, sa_type=BigInteger, description="主键"
    )
    field_id: int = Field(
        foreign_key=f"{PackageConfig.SchemaForeignKey}enum_field.field_id",
        ondelete="CASCADE",
        sa_type=BigInteger,
        description="主键",
    )
    enum_pid: int = Field(sa_type=BigInteger, description="上级枚举")
    enum_label: str = Field(max_length=50, description="枚举名")
    enum_value: str = Field(max_length=50, description="枚举值")
    enum_disabled: bool = Field(sa_type=Boolean, description="可选状态")
    is_active: bool = Field(sa_type=Boolean, description="启用状态")
    sort_order: int = Field(description="排序权重")
    description: Optional[str] = Field(default=None, nullable=True, max_length=500, description="描述")
    create_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="创建人")
    create_at: Optional[datetime] = Field(default=None, nullable=True, description="创建日期")
    update_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="修改人")
    update_at: Optional[datetime] = Field(default=None, nullable=True, description="修改日期")
    tenant_id: Optional[int] = Field(default=None, sa_type=BigInteger, nullable=True, description="主键")
    # 反向关系 - 父对象
    EnumField: "EnumField" = Relationship(back_populates="EnumValues")


class EnumValueCreate(SQLModel):
    """前端创建模型 - 用于接口请求"""

    field_id: int = Field(sa_type=BigInteger, description="主键")
    enum_pid: int = Field(sa_type=BigInteger, description="上级枚举")
    enum_label: str = Field(max_length=50, description="枚举名")
    enum_value: str = Field(max_length=50, description="枚举值")
    enum_disabled: bool = Field(description="可选状态")
    is_active: bool = Field(description="启用状态")
    sort_order: int = Field(description="排序权重")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")

    model_config = ConfigDict(populate_by_name=True)


class EnumValueUpdate(SQLModel):
    """前端更新模型 - 用于接口请求"""

    enum_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="主键")
    field_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="主键")
    enum_pid: Optional[int] = Field(default=None, sa_type=BigInteger, description="上级枚举")
    enum_label: Optional[str] = Field(default=None, max_length=50, description="枚举名")
    enum_value: Optional[str] = Field(default=None, max_length=50, description="枚举值")
    enum_disabled: Optional[bool] = Field(default=None, description="可选状态")
    is_active: Optional[bool] = Field(default=None, description="启用状态")
    sort_order: Optional[int] = Field(default=None, description="排序权重")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")

    model_config = ConfigDict(populate_by_name=True)


class EnumValueResponse(BaseResponse):
    """前端响应模型 - 用于接口响应"""

    __database_schema__ = PackageConfig.SchemaName  # 仅用于内部处理
    enum_id: int = Field(description="主键", sa_type=BigInteger)
    field_id: int = Field(description="主键", sa_type=BigInteger)
    enum_pid: int = Field(description="上级枚举", sa_type=BigInteger)
    enum_label: str = Field(description="枚举名")
    enum_value: str = Field(description="枚举值")
    enum_disabled: bool = Field(description="可选状态")
    is_active: bool = Field(description="启用状态")
    sort_order: int = Field(description="排序权重")
    description: Optional[str] = Field(description="描述", default=None)
    create_by: Optional[str] = Field(description="创建人", default=None)
    create_at: Optional[datetime] = Field(description="创建日期", default=None)
    update_by: Optional[str] = Field(description="修改人", default=None)
    update_at: Optional[datetime] = Field(description="修改日期", default=None)

    model_config = ConfigDict(populate_by_name=True)
