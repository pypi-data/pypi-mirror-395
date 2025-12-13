#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @License  ：(C)Copyright 2025, 数道智融科技
# @Author   ：Shudaodao Auto Generator
# @Software ：PyCharm
# @Desc     ：SQLModel classes for shudaodao_acm.sys_module

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import ConfigDict

from sqlalchemy import BigInteger, Boolean

from shudaodao_core import SQLModel, BaseResponse, Field, Relationship, EnumStr, get_primary_id
from ...package_config import PackageConfig

if TYPE_CHECKING:
    from .sys_permission import Permission
    from .sys_route import Route
    from .sys_system import System


class Module(PackageConfig.RegistryModel, table=True):
    """数据库对象模型"""

    __tablename__ = "sys_module"
    __table_args__ = {"schema": PackageConfig.SchemaTable, "comment": "功能模块"}
    # 仅用于内部处理
    __database_schema__ = PackageConfig.SchemaName
    __primary_key__ = ["module_id"]

    module_id: int = Field(
        default_factory=get_primary_id, primary_key=True, sa_type=BigInteger, description="模块内码"
    )
    system_id: int = Field(
        foreign_key=f"{PackageConfig.SchemaForeignKey}sys_system.system_id",
        sa_type=BigInteger,
        description="系统内码",
    )
    module_pid: int = Field(sa_type=BigInteger, description="父模块内码")
    module_name: str = Field(max_length=100, description="模块名称")
    module_code: str = Field(max_length=100, description="模块编码")
    module_icon: Optional[str] = Field(default=None, nullable=True, max_length=100, description="模块图标")
    module_type: EnumStr = Field(max_length=50, description="模块类型")
    path_router: Optional[str] = Field(
        default=None, nullable=True, max_length=200, description="前端路由路径"
    )
    path_component: Optional[str] = Field(
        default=None, nullable=True, max_length=200, description="前端组件路径"
    )
    is_active: bool = Field(sa_type=Boolean, description="启用状态")
    sort_order: int = Field(description="排序权重")
    description: Optional[str] = Field(default=None, nullable=True, max_length=500, description="描述")
    create_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="创建账户")
    create_at: Optional[datetime] = Field(default=None, nullable=True, description="创建日期")
    update_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="修改账户")
    update_at: Optional[datetime] = Field(default=None, nullable=True, description="修改日期")
    tenant_id: Optional[int] = Field(default=None, sa_type=BigInteger, nullable=True, description="租户内码")
    # 反向关系 - 父对象
    System: "System" = Relationship(back_populates="Modules")
    # 正向关系 - 子对象
    Permissions: list["Permission"] = Relationship(
        back_populates="Module", sa_relationship_kwargs={"order_by": "Permission.sort_order.asc()"}
    )
    # 正向关系 - 子对象
    Route: "Route" = Relationship(back_populates="Module", cascade_delete=True)


class ModuleCreate(SQLModel):
    """前端创建模型 - 用于接口请求"""

    system_id: int = Field(sa_type=BigInteger, description="系统内码")
    module_pid: int = Field(sa_type=BigInteger, description="父模块内码")
    module_name: str = Field(max_length=100, description="模块名称")
    module_code: str = Field(max_length=100, description="模块编码")
    module_icon: Optional[str] = Field(default=None, max_length=100, description="模块图标")
    module_type: EnumStr = Field(max_length=50, description="模块类型")
    path_router: Optional[str] = Field(default=None, max_length=200, description="前端路由路径")
    path_component: Optional[str] = Field(default=None, max_length=200, description="前端组件路径")
    is_active: bool = Field(description="启用状态")
    sort_order: int = Field(description="排序权重")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")

    model_config = ConfigDict(populate_by_name=True)


class ModuleUpdate(SQLModel):
    """前端更新模型 - 用于接口请求"""

    module_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="模块内码")
    system_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="系统内码")
    module_pid: Optional[int] = Field(default=None, sa_type=BigInteger, description="父模块内码")
    module_name: Optional[str] = Field(default=None, max_length=100, description="模块名称")
    module_code: Optional[str] = Field(default=None, max_length=100, description="模块编码")
    module_icon: Optional[str] = Field(default=None, max_length=100, description="模块图标")
    module_type: Optional[EnumStr] = Field(default=None, max_length=50, description="模块类型")
    path_router: Optional[str] = Field(default=None, max_length=200, description="前端路由路径")
    path_component: Optional[str] = Field(default=None, max_length=200, description="前端组件路径")
    is_active: Optional[bool] = Field(default=None, description="启用状态")
    sort_order: Optional[int] = Field(default=None, description="排序权重")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")

    model_config = ConfigDict(populate_by_name=True)


class ModuleResponse(BaseResponse):
    """前端响应模型 - 用于接口响应"""

    __database_schema__ = PackageConfig.SchemaName  # 仅用于内部处理
    module_id: int = Field(description="模块内码", sa_type=BigInteger)
    system_id: int = Field(description="系统内码", sa_type=BigInteger)
    module_pid: int = Field(description="父模块内码", sa_type=BigInteger)
    module_name: str = Field(description="模块名称")
    module_code: str = Field(description="模块编码")
    module_icon: Optional[str] = Field(description="模块图标", default=None)
    module_type: EnumStr = Field(description="模块类型")
    path_router: Optional[str] = Field(description="前端路由路径", default=None)
    path_component: Optional[str] = Field(description="前端组件路径", default=None)
    is_active: bool = Field(description="启用状态")
    sort_order: int = Field(description="排序权重")
    description: Optional[str] = Field(description="描述", default=None)
    create_by: Optional[str] = Field(description="创建账户", default=None)
    create_at: Optional[datetime] = Field(description="创建日期", default=None)
    update_by: Optional[str] = Field(description="修改账户", default=None)
    update_at: Optional[datetime] = Field(description="修改日期", default=None)

    model_config = ConfigDict(populate_by_name=True)
