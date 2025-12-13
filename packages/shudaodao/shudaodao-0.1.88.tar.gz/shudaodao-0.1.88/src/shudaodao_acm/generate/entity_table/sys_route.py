#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @License  ：(C)Copyright 2025, 数道智融科技
# @Author   ：Shudaodao Auto Generator
# @Software ：PyCharm
# @Desc     ：SQLModel classes for shudaodao_acm.sys_route

from typing import Optional, TYPE_CHECKING
from pydantic import ConfigDict

from sqlalchemy import BigInteger, Boolean

from shudaodao_core import SQLModel, BaseResponse, Field, Relationship, get_primary_id
from ...package_config import PackageConfig

if TYPE_CHECKING:
    from .sys_module import Module
    from .sys_system import System


class Route(PackageConfig.RegistryModel, table=True):
    """数据库对象模型"""

    __tablename__ = "sys_route"
    __table_args__ = {"schema": PackageConfig.SchemaTable, "comment": "组件路由"}
    # 仅用于内部处理
    __database_schema__ = PackageConfig.SchemaName
    __primary_key__ = ["route_id"]

    route_id: int = Field(
        default_factory=get_primary_id, primary_key=True, sa_type=BigInteger, description="路由内码"
    )
    system_id: Optional[int] = Field(
        default=None,
        foreign_key=f"{PackageConfig.SchemaForeignKey}sys_system.system_id",
        ondelete="CASCADE",
        sa_type=BigInteger,
        nullable=True,
    )
    module_id: Optional[int] = Field(
        default=None,
        foreign_key=f"{PackageConfig.SchemaForeignKey}sys_module.module_id",
        ondelete="CASCADE",
        sa_type=BigInteger,
        nullable=True,
        unique=True,
        index=True,
    )
    route_name: Optional[str] = Field(default=None, nullable=True, max_length=64, description="组件名称")
    route_path: str = Field(max_length=64, description="路由路径")
    route_comp: str = Field(max_length=128, description="组件路径/外部链接")
    route_icon: Optional[str] = Field(default=None, nullable=True, max_length=64, description="路由图标")
    route_badge: Optional[str] = Field(default=None, nullable=True, max_length=32, description="文本徽章")
    is_hide_tab: Optional[bool] = Field(default=None, sa_type=Boolean, nullable=True, description="标签隐藏")
    is_fixed_tab: Optional[bool] = Field(
        default=None, sa_type=Boolean, nullable=True, description="是否固定标签页"
    )
    is_iframe: Optional[bool] = Field(
        default=None, sa_type=Boolean, nullable=True, description="是否为内嵌框架"
    )
    is_keep_alive: Optional[bool] = Field(
        default=None, sa_type=Boolean, nullable=True, description="页面缓存"
    )
    is_show_badge: Optional[bool] = Field(
        default=None, sa_type=Boolean, nullable=True, description="显示徽章"
    )
    is_full_page: Optional[bool] = Field(default=None, sa_type=Boolean, nullable=True, description="全屏页面")
    # 反向关系 - 父对象
    Module: "Module" = Relationship(back_populates="Route")
    # 反向关系 - 父对象
    System: "System" = Relationship(back_populates="Route")


class RouteCreate(SQLModel):
    """前端创建模型 - 用于接口请求"""

    system_id: Optional[int] = Field(default=None, sa_type=BigInteger)
    module_id: Optional[int] = Field(default=None, sa_type=BigInteger)
    route_name: Optional[str] = Field(default=None, max_length=64, description="组件名称")
    route_path: str = Field(max_length=64, description="路由路径")
    route_comp: str = Field(max_length=128, description="组件路径/外部链接")
    route_icon: Optional[str] = Field(default=None, max_length=64, description="路由图标")
    route_badge: Optional[str] = Field(default=None, max_length=32, description="文本徽章")
    is_hide_tab: Optional[bool] = Field(default=None, description="标签隐藏")
    is_fixed_tab: Optional[bool] = Field(default=None, description="是否固定标签页")
    is_iframe: Optional[bool] = Field(default=None, description="是否为内嵌框架")
    is_keep_alive: Optional[bool] = Field(default=None, description="页面缓存")
    is_show_badge: Optional[bool] = Field(default=None, description="显示徽章")
    is_full_page: Optional[bool] = Field(default=None, description="全屏页面")

    model_config = ConfigDict(populate_by_name=True)


class RouteUpdate(SQLModel):
    """前端更新模型 - 用于接口请求"""

    route_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="路由内码")
    system_id: Optional[int] = Field(default=None, sa_type=BigInteger)
    module_id: Optional[int] = Field(default=None, sa_type=BigInteger)
    route_name: Optional[str] = Field(default=None, max_length=64, description="组件名称")
    route_path: Optional[str] = Field(default=None, max_length=64, description="路由路径")
    route_comp: Optional[str] = Field(default=None, max_length=128, description="组件路径/外部链接")
    route_icon: Optional[str] = Field(default=None, max_length=64, description="路由图标")
    route_badge: Optional[str] = Field(default=None, max_length=32, description="文本徽章")
    is_hide_tab: Optional[bool] = Field(default=None, description="标签隐藏")
    is_fixed_tab: Optional[bool] = Field(default=None, description="是否固定标签页")
    is_iframe: Optional[bool] = Field(default=None, description="是否为内嵌框架")
    is_keep_alive: Optional[bool] = Field(default=None, description="页面缓存")
    is_show_badge: Optional[bool] = Field(default=None, description="显示徽章")
    is_full_page: Optional[bool] = Field(default=None, description="全屏页面")

    model_config = ConfigDict(populate_by_name=True)


class RouteResponse(BaseResponse):
    """前端响应模型 - 用于接口响应"""

    __database_schema__ = PackageConfig.SchemaName  # 仅用于内部处理
    route_id: int = Field(description="路由内码", sa_type=BigInteger)
    system_id: Optional[int] = Field(default=None, sa_type=BigInteger)
    module_id: Optional[int] = Field(default=None, sa_type=BigInteger)
    route_name: Optional[str] = Field(description="组件名称", default=None)
    route_path: str = Field(description="路由路径")
    route_comp: str = Field(description="组件路径/外部链接")
    route_icon: Optional[str] = Field(description="路由图标", default=None)
    route_badge: Optional[str] = Field(description="文本徽章", default=None)
    is_hide_tab: Optional[bool] = Field(description="标签隐藏", default=None)
    is_fixed_tab: Optional[bool] = Field(description="是否固定标签页", default=None)
    is_iframe: Optional[bool] = Field(description="是否为内嵌框架", default=None)
    is_keep_alive: Optional[bool] = Field(description="页面缓存", default=None)
    is_show_badge: Optional[bool] = Field(description="显示徽章", default=None)
    is_full_page: Optional[bool] = Field(description="全屏页面", default=None)

    model_config = ConfigDict(populate_by_name=True)
