#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @License  ：(C)Copyright 2025, 数道智融科技
# @Author   ：Shudaodao Auto Generator
# @Software ：PyCharm
# @Desc     ：SQLModel classes for shudaodao_acm.sys_staff_role

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import ConfigDict

from sqlalchemy import BigInteger

from shudaodao_core import SQLModel, BaseResponse, Field, Relationship, get_primary_id
from ...package_config import PackageConfig

if TYPE_CHECKING:
    from .sys_staff import Staff


class StaffRole(PackageConfig.RegistryModel, table=True):
    """数据库对象模型"""

    __tablename__ = "sys_staff_role"
    __table_args__ = {"schema": PackageConfig.SchemaTable}
    # 仅用于内部处理
    __database_schema__ = PackageConfig.SchemaName
    __primary_key__ = ["staff_role_id"]

    staff_role_id: int = Field(
        default_factory=get_primary_id, primary_key=True, sa_type=BigInteger, description="人员角色关系内码"
    )
    role_id: int = Field(sa_type=BigInteger, description="角色内码")
    staff_id: int = Field(
        foreign_key=f"{PackageConfig.SchemaForeignKey}sys_staff.staff_id",
        sa_type=BigInteger,
        description="人员内码",
    )
    expiry_at: Optional[datetime] = Field(default=None, nullable=True, description="过期时间")
    create_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="创建人")
    create_at: Optional[datetime] = Field(default=None, nullable=True, description="创建日期")
    update_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="修改人")
    update_at: Optional[datetime] = Field(default=None, nullable=True, description="修改日期")
    tenant_id: Optional[int] = Field(default=None, sa_type=BigInteger, nullable=True, description="租户内码")
    # 反向关系 - 父对象
    Staff: "Staff" = Relationship(back_populates="StaffRoles")


class StaffRoleCreate(SQLModel):
    """前端创建模型 - 用于接口请求"""

    role_id: int = Field(sa_type=BigInteger, description="角色内码")
    staff_id: int = Field(sa_type=BigInteger, description="人员内码")
    expiry_at: Optional[datetime] = Field(default=None, description="过期时间")

    model_config = ConfigDict(populate_by_name=True)


class StaffRoleUpdate(SQLModel):
    """前端更新模型 - 用于接口请求"""

    staff_role_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="人员角色关系内码")
    role_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="角色内码")
    staff_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="人员内码")
    expiry_at: Optional[datetime] = Field(default=None, description="过期时间")

    model_config = ConfigDict(populate_by_name=True)


class StaffRoleResponse(BaseResponse):
    """前端响应模型 - 用于接口响应"""

    __database_schema__ = PackageConfig.SchemaName  # 仅用于内部处理
    staff_role_id: int = Field(description="人员角色关系内码", sa_type=BigInteger)
    role_id: int = Field(description="角色内码", sa_type=BigInteger)
    staff_id: int = Field(description="人员内码", sa_type=BigInteger)
    expiry_at: Optional[datetime] = Field(description="过期时间", default=None)
    create_by: Optional[str] = Field(description="创建人", default=None)
    create_at: Optional[datetime] = Field(description="创建日期", default=None)
    update_by: Optional[str] = Field(description="修改人", default=None)
    update_at: Optional[datetime] = Field(description="修改日期", default=None)

    model_config = ConfigDict(populate_by_name=True)
