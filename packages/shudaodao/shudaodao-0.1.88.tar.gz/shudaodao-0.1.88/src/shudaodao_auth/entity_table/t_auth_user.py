#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @License  ：(C)Copyright 2025, 数道智融科技
# @Author   ：李锋
# @Software ：PyCharm
# @Date     ：2025/11/13 上午11:41
# @Desc     ：


from datetime import datetime
from typing import Optional

from pydantic import EmailStr, ConfigDict, BaseModel
from sqlalchemy import BigInteger, Boolean

from shudaodao_core import SQLModel, BaseResponse, Field, get_primary_id
from ..package_config import PackageConfig


class AuthUser(PackageConfig.RegistryModel, table=True):
    """数据库对象模型"""

    __tablename__ = "t_auth_user"
    __table_args__ = {"schema": PackageConfig.SchemaTable, "comment": "鉴权账户"}
    # 仅用于内部处理
    __database_schema__ = PackageConfig.SchemaName
    __primary_key__ = ["user_id"]

    user_id: int = Field(
        default_factory=get_primary_id, primary_key=True, sa_type=BigInteger, description="主键"
    )
    username: str = Field(max_length=50, unique=True, index=True, description="账户名")
    name: Optional[str] = Field(default=None, nullable=True, description="姓名")
    password: str = Field(description="密码")
    is_active: bool = Field(sa_type=Boolean, description="启用状态")
    last_login_at: Optional[datetime] = Field(default=None, nullable=True, description="最后登录时间")
    nickname: Optional[str] = Field(default=None, nullable=True, description="昵称")
    picture: Optional[str] = Field(default=None, nullable=True, description="头像URL地址")
    email: Optional[str] = Field(default=None, nullable=True, description="邮件")
    email_verified: Optional[bool] = Field(
        default=None, sa_type=Boolean, nullable=True, description="邮箱是否已验证"
    )
    totp_verified: Optional[bool] = Field(
        default=None, sa_type=Boolean, nullable=True, description="启用身份验证器"
    )
    create_by: Optional[str] = Field(default=None, nullable=True, description="创建人")
    create_at: Optional[datetime] = Field(default=None, nullable=True, description="创建日期")
    update_by: Optional[str] = Field(default=None, nullable=True, description="修改人")
    update_at: Optional[datetime] = Field(default=None, nullable=True, description="修改日期")
    tenant_id: Optional[int] = Field(default=None, sa_type=BigInteger, nullable=True, description="默认租户")


class AuthUserResponse(BaseResponse):
    """前端响应模型 - 用于接口响应"""

    __database_schema__ = PackageConfig.SchemaName  # 仅用于内部处理
    user_id: int = Field(description="主键", sa_type=BigInteger)
    username: str = Field(description="账户名")
    name: Optional[str] = Field(description="姓名", default=None)
    password: str = Field(description="密码")
    is_active: bool = Field(description="启用状态")
    last_login_at: Optional[datetime] = Field(description="最后登录时间", default=None)
    nickname: Optional[str] = Field(description="昵称", default=None)
    picture: Optional[str] = Field(description="头像URL地址", default=None)
    email: Optional[str] = Field(description="邮件", default=None)
    email_verified: Optional[bool] = Field(description="邮箱是否已验证", default=None)
    totp_verified: Optional[bool] = Field(description="启用身份验证器", default=None)
    create_by: Optional[str] = Field(description="创建人", default=None)
    create_at: Optional[datetime] = Field(description="创建日期", default=None)
    update_by: Optional[str] = Field(description="修改人", default=None)
    update_at: Optional[datetime] = Field(description="修改日期", default=None)


class AuthUserRegister(SQLModel):
    """ 注册模型 """
    username: str = Field(min_length=5, max_length=50)
    password: str = Field(min_length=5)
    # --- 核心字段 ---
    name: str = Field(default=None, nullable=True, description="姓名")
    last_login_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(), description="最后登录时间")
    # --- 可修改字段 ---
    nickname: str = Field(default=None, nullable=True, description="昵称")
    picture: Optional[str] = Field(default=None, nullable=True, description="头像URL地址")
    email: Optional[EmailStr] = Field(default=None, nullable=True, description="邮件")
    # --- 用户验证增强 ---
    # email_verified: Optional[bool] = Field(default=None, nullable=True, description="邮箱是否已验证")
    # --- 内部管理字段 ---
    tenant_id: Optional[int] = Field(default=None, nullable=True, sa_type=BigInteger, description="默认租户")


class AuthLogin(BaseModel):
    """ 登录模型 """
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=5)

    model_config = ConfigDict(
        populate_by_name=True
    )


class AuthPassword(SQLModel):
    """ 修改密码模型 """
    old_password: str
    new_password: str = Field(min_length=6, max_length=50)
