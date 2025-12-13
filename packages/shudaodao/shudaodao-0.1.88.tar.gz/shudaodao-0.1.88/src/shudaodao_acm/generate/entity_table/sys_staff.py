#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @License  ：(C)Copyright 2025, 数道智融科技
# @Author   ：Shudaodao Auto Generator
# @Software ：PyCharm
# @Desc     ：SQLModel classes for shudaodao_acm.sys_staff

from datetime import datetime, date
from typing import Optional, TYPE_CHECKING
from pydantic import ConfigDict

from sqlalchemy import BigInteger

from shudaodao_core import SQLModel, BaseResponse, Field, Relationship, get_primary_id
from ...package_config import PackageConfig

if TYPE_CHECKING:
    from .sys_department import Department
    from .sys_staff_role import StaffRole


class Staff(PackageConfig.RegistryModel, table=True):
    """数据库对象模型"""

    __tablename__ = "sys_staff"
    __table_args__ = {"schema": PackageConfig.SchemaTable, "comment": "人员表"}
    # 仅用于内部处理
    __database_schema__ = PackageConfig.SchemaName
    __primary_key__ = ["staff_id"]

    staff_id: int = Field(
        default_factory=get_primary_id, primary_key=True, sa_type=BigInteger, description="人员内码"
    )
    department_id: int = Field(
        foreign_key=f"{PackageConfig.SchemaForeignKey}sys_department.department_id",
        sa_type=BigInteger,
        description="部门ID",
    )
    username: str = Field(max_length=100, description="登录账户")
    name: str = Field(max_length=100, description="姓名")
    number: Optional[str] = Field(default=None, nullable=True, max_length=50, description="工号")
    id_number: Optional[str] = Field(default=None, nullable=True, max_length=18, description="身份证号")
    gender: Optional[int] = Field(default=None, nullable=True, description="性别")
    birthday: Optional[date] = Field(default=None, nullable=True, description="出生日期")
    mobile: Optional[str] = Field(default=None, nullable=True, max_length=50, description="手机号码")
    email: Optional[str] = Field(default=None, nullable=True, max_length=100, description="邮箱")
    address: Optional[str] = Field(default=None, nullable=True, max_length=200, description="地址")
    status: Optional[int] = Field(default=None, nullable=True, description="人员状态")
    entry_date: Optional[date] = Field(default=None, nullable=True, description="入职日期")
    leave_date: Optional[date] = Field(default=None, nullable=True, description="离职日期")
    sort_order: Optional[int] = Field(default=None, nullable=True, description="排序权重")
    description: Optional[str] = Field(default=None, nullable=True, max_length=500, description="描述")
    create_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="创建人")
    create_at: Optional[datetime] = Field(default=None, nullable=True, description="创建日期")
    update_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="修改人")
    update_at: Optional[datetime] = Field(default=None, nullable=True, description="修改日期")
    tenant_id: Optional[int] = Field(default=None, sa_type=BigInteger, nullable=True, description="租户内码")
    # 反向关系 - 父对象
    Department: "Department" = Relationship(back_populates="Staffs")
    # 正向关系 - 子对象
    StaffRoles: list["StaffRole"] = Relationship(back_populates="Staff")


class StaffCreate(SQLModel):
    """前端创建模型 - 用于接口请求"""

    department_id: int = Field(sa_type=BigInteger, description="部门ID")
    username: str = Field(max_length=100, description="登录账户")
    name: str = Field(max_length=100, description="姓名")
    number: Optional[str] = Field(default=None, max_length=50, description="工号")
    id_number: Optional[str] = Field(default=None, max_length=18, description="身份证号")
    gender: Optional[int] = Field(default=None, description="性别")
    birthday: Optional[date] = Field(default=None, description="出生日期")
    mobile: Optional[str] = Field(default=None, max_length=50, description="手机号码")
    email: Optional[str] = Field(default=None, max_length=100, description="邮箱")
    address: Optional[str] = Field(default=None, max_length=200, description="地址")
    status: Optional[int] = Field(default=None, description="人员状态")
    entry_date: Optional[date] = Field(default=None, description="入职日期")
    leave_date: Optional[date] = Field(default=None, description="离职日期")
    sort_order: Optional[int] = Field(default=None, description="排序权重")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")

    model_config = ConfigDict(populate_by_name=True)


class StaffUpdate(SQLModel):
    """前端更新模型 - 用于接口请求"""

    staff_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="人员内码")
    department_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="部门ID")
    username: Optional[str] = Field(default=None, max_length=100, description="登录账户")
    name: Optional[str] = Field(default=None, max_length=100, description="姓名")
    number: Optional[str] = Field(default=None, max_length=50, description="工号")
    id_number: Optional[str] = Field(default=None, max_length=18, description="身份证号")
    gender: Optional[int] = Field(default=None, description="性别")
    birthday: Optional[date] = Field(default=None, description="出生日期")
    mobile: Optional[str] = Field(default=None, max_length=50, description="手机号码")
    email: Optional[str] = Field(default=None, max_length=100, description="邮箱")
    address: Optional[str] = Field(default=None, max_length=200, description="地址")
    status: Optional[int] = Field(default=None, description="人员状态")
    entry_date: Optional[date] = Field(default=None, description="入职日期")
    leave_date: Optional[date] = Field(default=None, description="离职日期")
    sort_order: Optional[int] = Field(default=None, description="排序权重")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")

    model_config = ConfigDict(populate_by_name=True)


class StaffResponse(BaseResponse):
    """前端响应模型 - 用于接口响应"""

    __database_schema__ = PackageConfig.SchemaName  # 仅用于内部处理
    staff_id: int = Field(description="人员内码", sa_type=BigInteger)
    department_id: int = Field(description="部门ID", sa_type=BigInteger)
    username: str = Field(description="登录账户")
    name: str = Field(description="姓名")
    number: Optional[str] = Field(description="工号", default=None)
    id_number: Optional[str] = Field(description="身份证号", default=None)
    gender: Optional[int] = Field(description="性别", default=None)
    birthday: Optional[date] = Field(description="出生日期", default=None)
    mobile: Optional[str] = Field(description="手机号码", default=None)
    email: Optional[str] = Field(description="邮箱", default=None)
    address: Optional[str] = Field(description="地址", default=None)
    status: Optional[int] = Field(description="人员状态", default=None)
    entry_date: Optional[date] = Field(description="入职日期", default=None)
    leave_date: Optional[date] = Field(description="离职日期", default=None)
    sort_order: Optional[int] = Field(description="排序权重", default=None)
    description: Optional[str] = Field(description="描述", default=None)
    create_by: Optional[str] = Field(description="创建人", default=None)
    create_at: Optional[datetime] = Field(description="创建日期", default=None)
    update_by: Optional[str] = Field(description="修改人", default=None)
    update_at: Optional[datetime] = Field(description="修改日期", default=None)

    model_config = ConfigDict(populate_by_name=True)
