#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @License  ：(C)Copyright 2025, 数道智融科技
# @Author   ：Shudaodao Auto Generator
# @Software ：PyCharm
# @Desc     ：SQLModel classes for shudaodao_acm.sys_role

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import ConfigDict

from sqlalchemy import BigInteger, Boolean

from shudaodao_core import SQLModel, BaseResponse, Field, Relationship, EnumStr, get_primary_id
from ...package_config import PackageConfig

if TYPE_CHECKING:
    from .sys_system import System


class Role(PackageConfig.RegistryModel, table=True):
    """数据库对象模型"""

    __tablename__ = "sys_role"
    __table_args__ = {"schema": PackageConfig.SchemaTable}
    # 仅用于内部处理
    __database_schema__ = PackageConfig.SchemaName
    __primary_key__ = ["role_id"]

    role_id: int = Field(
        default_factory=get_primary_id, primary_key=True, sa_type=BigInteger, description="角色内码"
    )
    system_id: int = Field(
        foreign_key=f"{PackageConfig.SchemaForeignKey}sys_system.system_id",
        sa_type=BigInteger,
        description="系统内码",
    )
    role_pid: int = Field(sa_type=BigInteger, description="上级角色")
    role_name: Optional[str] = Field(default=None, nullable=True, max_length=100, description="角色名称")
    role_code: Optional[str] = Field(default=None, nullable=True, max_length=100, description="角色编码")
    role_type: EnumStr = Field(max_length=50, description="角色类型")
    is_active: bool = Field(sa_type=Boolean, description="启用状态")
    sort_order: int = Field(description="排序权重")
    description: Optional[str] = Field(default=None, nullable=True, max_length=500, description="描述")
    create_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="创建人")
    create_at: Optional[datetime] = Field(default=None, nullable=True, description="创建日期")
    update_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="修改人")
    update_at: Optional[datetime] = Field(default=None, nullable=True, description="修改日期")
    tenant_id: Optional[int] = Field(default=None, sa_type=BigInteger, nullable=True, description="租户内码")
    # 反向关系 - 父对象
    System: "System" = Relationship(back_populates="Roles")


class RoleCreate(SQLModel):
    """前端创建模型 - 用于接口请求"""

    system_id: int = Field(sa_type=BigInteger, description="系统内码")
    role_pid: int = Field(sa_type=BigInteger, description="上级角色")
    role_name: Optional[str] = Field(default=None, max_length=100, description="角色名称")
    role_code: Optional[str] = Field(default=None, max_length=100, description="角色编码")
    role_type: EnumStr = Field(max_length=50, description="角色类型")
    is_active: bool = Field(description="启用状态")
    sort_order: int = Field(description="排序权重")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")

    model_config = ConfigDict(populate_by_name=True)


class RoleUpdate(SQLModel):
    """前端更新模型 - 用于接口请求"""

    role_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="角色内码")
    system_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="系统内码")
    role_pid: Optional[int] = Field(default=None, sa_type=BigInteger, description="上级角色")
    role_name: Optional[str] = Field(default=None, max_length=100, description="角色名称")
    role_code: Optional[str] = Field(default=None, max_length=100, description="角色编码")
    role_type: Optional[EnumStr] = Field(default=None, max_length=50, description="角色类型")
    is_active: Optional[bool] = Field(default=None, description="启用状态")
    sort_order: Optional[int] = Field(default=None, description="排序权重")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")

    model_config = ConfigDict(populate_by_name=True)


class RoleResponse(BaseResponse):
    """前端响应模型 - 用于接口响应"""

    __database_schema__ = PackageConfig.SchemaName  # 仅用于内部处理
    role_id: int = Field(description="角色内码", sa_type=BigInteger)
    system_id: int = Field(description="系统内码", sa_type=BigInteger)
    role_pid: int = Field(description="上级角色", sa_type=BigInteger)
    role_name: Optional[str] = Field(description="角色名称", default=None)
    role_code: Optional[str] = Field(description="角色编码", default=None)
    role_type: EnumStr = Field(description="角色类型")
    is_active: bool = Field(description="启用状态")
    sort_order: int = Field(description="排序权重")
    description: Optional[str] = Field(description="描述", default=None)
    create_by: Optional[str] = Field(description="创建人", default=None)
    create_at: Optional[datetime] = Field(description="创建日期", default=None)
    update_by: Optional[str] = Field(description="修改人", default=None)
    update_at: Optional[datetime] = Field(description="修改日期", default=None)

    model_config = ConfigDict(populate_by_name=True)
