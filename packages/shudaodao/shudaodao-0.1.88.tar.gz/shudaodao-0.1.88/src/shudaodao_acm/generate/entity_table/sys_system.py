#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @License  ：(C)Copyright 2025, 数道智融科技
# @Author   ：Shudaodao Auto Generator
# @Software ：PyCharm
# @Desc     ：SQLModel classes for shudaodao_acm.sys_system

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import ConfigDict

from sqlalchemy import BigInteger, Boolean

from shudaodao_core import SQLModel, BaseResponse, Field, Relationship, get_primary_id
from ...package_config import PackageConfig

if TYPE_CHECKING:
    from .sys_module import Module
    from .sys_permission import Permission
    from .sys_role import Role
    from .sys_route import Route


class System(PackageConfig.RegistryModel, table=True):
    """数据库对象模型"""

    __tablename__ = "sys_system"
    __table_args__ = {"schema": PackageConfig.SchemaTable, "comment": "系统表"}
    # 仅用于内部处理
    __database_schema__ = PackageConfig.SchemaName
    __primary_key__ = ["system_id"]

    system_id: int = Field(
        default_factory=get_primary_id, primary_key=True, sa_type=BigInteger, description="系统内码"
    )
    system_label: str = Field(max_length=100, description="系统名称")
    is_active: bool = Field(sa_type=Boolean, description="启用状态")
    sort_order: int = Field(description="排序权重")
    description: Optional[str] = Field(default=None, nullable=True, max_length=500, description="描述")
    create_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="创建人")
    create_at: Optional[datetime] = Field(default=None, nullable=True, description="创建日期")
    update_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="修改人")
    update_at: Optional[datetime] = Field(default=None, nullable=True, description="修改日期")
    tenant_id: Optional[int] = Field(default=None, sa_type=BigInteger, nullable=True, description="租户内码")
    # 正向关系 - 子对象
    Modules: list["Module"] = Relationship(
        back_populates="System", sa_relationship_kwargs={"order_by": "Module.sort_order.asc()"}
    )
    # 正向关系 - 子对象
    Permissions: list["Permission"] = Relationship(
        back_populates="System", sa_relationship_kwargs={"order_by": "Permission.sort_order.asc()"}
    )
    # 正向关系 - 子对象
    Roles: list["Role"] = Relationship(
        back_populates="System", sa_relationship_kwargs={"order_by": "Role.sort_order.asc()"}
    )
    # 正向关系 - 子对象
    Route: "Route" = Relationship(back_populates="System", cascade_delete=True)


class SystemCreate(SQLModel):
    """前端创建模型 - 用于接口请求"""

    system_label: str = Field(max_length=100, description="系统名称")
    is_active: bool = Field(description="启用状态")
    sort_order: int = Field(description="排序权重")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")

    model_config = ConfigDict(populate_by_name=True)


class SystemUpdate(SQLModel):
    """前端更新模型 - 用于接口请求"""

    system_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="系统内码")
    system_label: Optional[str] = Field(default=None, max_length=100, description="系统名称")
    is_active: Optional[bool] = Field(default=None, description="启用状态")
    sort_order: Optional[int] = Field(default=None, description="排序权重")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")

    model_config = ConfigDict(populate_by_name=True)


class SystemResponse(BaseResponse):
    """前端响应模型 - 用于接口响应"""

    __database_schema__ = PackageConfig.SchemaName  # 仅用于内部处理
    system_id: int = Field(description="系统内码", sa_type=BigInteger)
    system_label: str = Field(description="系统名称")
    is_active: bool = Field(description="启用状态")
    sort_order: int = Field(description="排序权重")
    description: Optional[str] = Field(description="描述", default=None)
    create_by: Optional[str] = Field(description="创建人", default=None)
    create_at: Optional[datetime] = Field(description="创建日期", default=None)
    update_by: Optional[str] = Field(description="修改人", default=None)
    update_at: Optional[datetime] = Field(description="修改日期", default=None)

    model_config = ConfigDict(populate_by_name=True)
