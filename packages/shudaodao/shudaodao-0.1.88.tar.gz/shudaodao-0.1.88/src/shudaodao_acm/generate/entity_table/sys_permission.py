#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @License  ：(C)Copyright 2025, 数道智融科技
# @Author   ：Shudaodao Auto Generator
# @Software ：PyCharm
# @Desc     ：SQLModel classes for shudaodao_acm.sys_permission

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import ConfigDict

from sqlalchemy import BigInteger, Boolean

from shudaodao_core import SQLModel, BaseResponse, Field, Relationship, get_primary_id
from ...package_config import PackageConfig

if TYPE_CHECKING:
    from .sys_module import Module
    from .sys_system import System


class Permission(PackageConfig.RegistryModel, table=True):
    """数据库对象模型"""

    __tablename__ = "sys_permission"
    __table_args__ = {"schema": PackageConfig.SchemaTable, "comment": "功能模块"}
    # 仅用于内部处理
    __database_schema__ = PackageConfig.SchemaName
    __primary_key__ = ["permission_id"]

    permission_id: int = Field(
        default_factory=get_primary_id, primary_key=True, sa_type=BigInteger, description="模块内码"
    )
    system_id: int = Field(
        foreign_key=f"{PackageConfig.SchemaForeignKey}sys_system.system_id",
        sa_type=BigInteger,
        description="模块内码",
    )
    module_id: int = Field(
        foreign_key=f"{PackageConfig.SchemaForeignKey}sys_module.module_id",
        sa_type=BigInteger,
        description="模块内码",
    )
    permission_name: Optional[str] = Field(
        default=None, nullable=True, max_length=100, description="权限名称"
    )
    permission_type: Optional[str] = Field(default=None, nullable=True, max_length=20, description="权限类型")
    permission_code: Optional[str] = Field(default=None, nullable=True, max_length=50, description="权限编码")
    page_active: Optional[bool] = Field(default=None, sa_type=Boolean, nullable=True, description="页面启用")
    element_active: Optional[bool] = Field(
        default=None, sa_type=Boolean, nullable=True, description="元素可见"
    )
    api_active: Optional[bool] = Field(default=None, sa_type=Boolean, nullable=True, description="接口启用")
    api_method: Optional[str] = Field(default=None, nullable=True, max_length=200, description="api方法")
    api_url: Optional[str] = Field(default=None, nullable=True, max_length=200, description="api地址")
    api_role: Optional[str] = Field(default=None, nullable=True, max_length=200, description="api验证角色")
    api_obj: Optional[str] = Field(default=None, nullable=True, max_length=200, description="api对象")
    api_act: Optional[str] = Field(default=None, nullable=True, max_length=200, description="api动作")
    sort_order: int = Field(description="排序权重")
    description: Optional[str] = Field(default=None, nullable=True, max_length=500, description="描述")
    create_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="创建账户")
    create_at: Optional[datetime] = Field(default=None, nullable=True, description="创建日期")
    update_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="修改账户")
    update_at: Optional[datetime] = Field(default=None, nullable=True, description="修改日期")
    tenant_id: Optional[int] = Field(default=None, sa_type=BigInteger, nullable=True, description="租户内码")
    # 反向关系 - 父对象
    Module: "Module" = Relationship(back_populates="Permissions")
    # 反向关系 - 父对象
    System: "System" = Relationship(back_populates="Permissions")


class PermissionCreate(SQLModel):
    """前端创建模型 - 用于接口请求"""

    system_id: int = Field(sa_type=BigInteger, description="模块内码")
    module_id: int = Field(sa_type=BigInteger, description="模块内码")
    permission_name: Optional[str] = Field(default=None, max_length=100, description="权限名称")
    permission_type: Optional[str] = Field(default=None, max_length=20, description="权限类型")
    permission_code: Optional[str] = Field(default=None, max_length=50, description="权限编码")
    page_active: Optional[bool] = Field(default=None, description="页面启用")
    element_active: Optional[bool] = Field(default=None, description="元素可见")
    api_active: Optional[bool] = Field(default=None, description="接口启用")
    api_method: Optional[str] = Field(default=None, max_length=200, description="api方法")
    api_url: Optional[str] = Field(default=None, max_length=200, description="api地址")
    api_role: Optional[str] = Field(default=None, max_length=200, description="api验证角色")
    api_obj: Optional[str] = Field(default=None, max_length=200, description="api对象")
    api_act: Optional[str] = Field(default=None, max_length=200, description="api动作")
    sort_order: int = Field(description="排序权重")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")

    model_config = ConfigDict(populate_by_name=True)


class PermissionUpdate(SQLModel):
    """前端更新模型 - 用于接口请求"""

    permission_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="模块内码")
    system_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="模块内码")
    module_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="模块内码")
    permission_name: Optional[str] = Field(default=None, max_length=100, description="权限名称")
    permission_type: Optional[str] = Field(default=None, max_length=20, description="权限类型")
    permission_code: Optional[str] = Field(default=None, max_length=50, description="权限编码")
    page_active: Optional[bool] = Field(default=None, description="页面启用")
    element_active: Optional[bool] = Field(default=None, description="元素可见")
    api_active: Optional[bool] = Field(default=None, description="接口启用")
    api_method: Optional[str] = Field(default=None, max_length=200, description="api方法")
    api_url: Optional[str] = Field(default=None, max_length=200, description="api地址")
    api_role: Optional[str] = Field(default=None, max_length=200, description="api验证角色")
    api_obj: Optional[str] = Field(default=None, max_length=200, description="api对象")
    api_act: Optional[str] = Field(default=None, max_length=200, description="api动作")
    sort_order: Optional[int] = Field(default=None, description="排序权重")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")

    model_config = ConfigDict(populate_by_name=True)


class PermissionResponse(BaseResponse):
    """前端响应模型 - 用于接口响应"""

    __database_schema__ = PackageConfig.SchemaName  # 仅用于内部处理
    permission_id: int = Field(description="模块内码", sa_type=BigInteger)
    system_id: int = Field(description="模块内码", sa_type=BigInteger)
    module_id: int = Field(description="模块内码", sa_type=BigInteger)
    permission_name: Optional[str] = Field(description="权限名称", default=None)
    permission_type: Optional[str] = Field(description="权限类型", default=None)
    permission_code: Optional[str] = Field(description="权限编码", default=None)
    page_active: Optional[bool] = Field(description="页面启用", default=None)
    element_active: Optional[bool] = Field(description="元素可见", default=None)
    api_active: Optional[bool] = Field(description="接口启用", default=None)
    api_method: Optional[str] = Field(description="api方法", default=None)
    api_url: Optional[str] = Field(description="api地址", default=None)
    api_role: Optional[str] = Field(description="api验证角色", default=None)
    api_obj: Optional[str] = Field(description="api对象", default=None)
    api_act: Optional[str] = Field(description="api动作", default=None)
    sort_order: int = Field(description="排序权重")
    description: Optional[str] = Field(description="描述", default=None)
    create_by: Optional[str] = Field(description="创建账户", default=None)
    create_at: Optional[datetime] = Field(description="创建日期", default=None)
    update_by: Optional[str] = Field(description="修改账户", default=None)
    update_at: Optional[datetime] = Field(description="修改日期", default=None)

    model_config = ConfigDict(populate_by_name=True)
