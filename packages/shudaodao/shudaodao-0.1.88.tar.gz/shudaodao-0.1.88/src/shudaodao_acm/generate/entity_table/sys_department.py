#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @License  ：(C)Copyright 2025, 数道智融科技
# @Author   ：Shudaodao Auto Generator
# @Software ：PyCharm
# @Desc     ：SQLModel classes for shudaodao_acm.sys_department

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import ConfigDict

from sqlalchemy import BigInteger

from shudaodao_core import SQLModel, BaseResponse, Field, Relationship, get_primary_id
from ...package_config import PackageConfig

if TYPE_CHECKING:
    from .sys_staff import Staff


class Department(PackageConfig.RegistryModel, table=True):
    """数据库对象模型"""

    __tablename__ = "sys_department"
    __table_args__ = {"schema": PackageConfig.SchemaTable}
    # 仅用于内部处理
    __database_schema__ = PackageConfig.SchemaName
    __primary_key__ = ["department_id"]

    department_id: int = Field(
        default_factory=get_primary_id, primary_key=True, sa_type=BigInteger, description="部门ID"
    )
    department_pid: int = Field(sa_type=BigInteger, description="父部门ID")
    name: str = Field(max_length=100, description="部门名称")
    sort_order: Optional[int] = Field(default=None, nullable=True, description="排序权重")
    description: Optional[str] = Field(default=None, nullable=True, max_length=500, description="描述")
    create_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="创建人")
    create_at: Optional[datetime] = Field(default=None, nullable=True, description="创建日期")
    update_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="修改人")
    update_at: Optional[datetime] = Field(default=None, nullable=True, description="修改日期")
    tenant_id: Optional[int] = Field(default=None, sa_type=BigInteger, nullable=True, description="租户内码")
    # 正向关系 - 子对象
    Staffs: list["Staff"] = Relationship(
        back_populates="Department", sa_relationship_kwargs={"order_by": "Staff.sort_order.asc()"}
    )


class DepartmentCreate(SQLModel):
    """前端创建模型 - 用于接口请求"""

    department_pid: int = Field(sa_type=BigInteger, description="父部门ID")
    name: str = Field(max_length=100, description="部门名称")
    sort_order: Optional[int] = Field(default=None, description="排序权重")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")

    model_config = ConfigDict(populate_by_name=True)


class DepartmentUpdate(SQLModel):
    """前端更新模型 - 用于接口请求"""

    department_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="部门ID")
    department_pid: Optional[int] = Field(default=None, sa_type=BigInteger, description="父部门ID")
    name: Optional[str] = Field(default=None, max_length=100, description="部门名称")
    sort_order: Optional[int] = Field(default=None, description="排序权重")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")

    model_config = ConfigDict(populate_by_name=True)


class DepartmentResponse(BaseResponse):
    """前端响应模型 - 用于接口响应"""

    __database_schema__ = PackageConfig.SchemaName  # 仅用于内部处理
    department_id: int = Field(description="部门ID", sa_type=BigInteger)
    department_pid: int = Field(description="父部门ID", sa_type=BigInteger)
    name: str = Field(description="部门名称")
    sort_order: Optional[int] = Field(description="排序权重", default=None)
    description: Optional[str] = Field(description="描述", default=None)
    create_by: Optional[str] = Field(description="创建人", default=None)
    create_at: Optional[datetime] = Field(description="创建日期", default=None)
    update_by: Optional[str] = Field(description="修改人", default=None)
    update_at: Optional[datetime] = Field(description="修改日期", default=None)

    model_config = ConfigDict(populate_by_name=True)
