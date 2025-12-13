#!/usr/bin/env python3
# # -*- coding:utf-8 -*-
# # @License  ：(C)Copyright 2025, 数道智融科技
# # @Author   ：Shudaodao Auto Generator
# # @Software ：PyCharm
# # @Desc     ：SQLModel classes for shudaodao_auth.t_auth_user
# 
# from datetime import datetime
# from typing import Optional
# from pydantic import ConfigDict
# 
# from sqlalchemy import BigInteger, Boolean
# 
# from shudaodao_core import SQLModel, BaseResponse, Field, get_primary_id
# from ...package_config import PackageConfig
# 
# 
# class AuthUser(PackageConfig.RegistryModel, table=True):
#     """数据库对象模型"""
# 
#     __tablename__ = "t_auth_user"
#     __table_args__ = {"schema": PackageConfig.SchemaTable, "comment": "鉴权账户"}
#     # 仅用于内部处理
#     __database_schema__ = PackageConfig.SchemaName
#     __primary_key__ = ["user_id"]
# 
#     user_id: int = Field(
#         default_factory=get_primary_id, primary_key=True, sa_type=BigInteger, description="内码"
#     )
#     username: str = Field(max_length=50, unique=True, index=True, description="账户名")
#     name: Optional[str] = Field(default=None, nullable=True, description="姓名")
#     password: str = Field(description="密码")
#     is_active: bool = Field(sa_type=Boolean, description="启用状态")
#     last_login_at: Optional[datetime] = Field(default=None, nullable=True, description="最后登录时间")
#     nickname: Optional[str] = Field(default=None, nullable=True, description="昵称")
#     picture: Optional[str] = Field(default=None, nullable=True, description="头像URL地址")
#     email: Optional[str] = Field(default=None, nullable=True, description="邮件")
#     email_verified: Optional[bool] = Field(
#         default=None, sa_type=Boolean, nullable=True, description="邮箱是否已验证"
#     )
#     totp_verified: Optional[bool] = Field(
#         default=None, sa_type=Boolean, nullable=True, description="启用身份验证器"
#     )
#     role: Optional[str] = Field(default=None, nullable=True, description="用户角色")
#     roles: Optional[str] = Field(default=None, nullable=True, description="角色列表")
#     groups: Optional[str] = Field(default=None, nullable=True, description="部门列表")
#     permissions: Optional[str] = Field(default=None, nullable=True, description="权限列表")
#     organization: Optional[str] = Field(default=None, nullable=True, description="所属组织")
#     department: Optional[str] = Field(default=None, nullable=True, description="所在部门")
#     job_title: Optional[str] = Field(default=None, nullable=True, description="职务职称")
#     create_by: Optional[str] = Field(default=None, nullable=True, description="创建人")
#     create_at: Optional[datetime] = Field(default=None, nullable=True, description="创建日期")
#     update_by: Optional[str] = Field(default=None, nullable=True, description="修改人")
#     update_at: Optional[datetime] = Field(default=None, nullable=True, description="修改日期")
#     tenant_id: Optional[int] = Field(default=None, sa_type=BigInteger, nullable=True, description="默认租户")
#     staff_id: Optional[int] = Field(default=None, sa_type=BigInteger, nullable=True)
# 
# 
# class AuthUserCreate(SQLModel):
#     """前端创建模型 - 用于接口请求"""
# 
#     username: str = Field(max_length=50, description="账户名")
#     name: Optional[str] = Field(default=None, description="姓名")
#     password: str = Field(description="密码")
#     is_active: bool = Field(description="启用状态")
#     last_login_at: Optional[datetime] = Field(default=None, description="最后登录时间")
#     nickname: Optional[str] = Field(default=None, description="昵称")
#     picture: Optional[str] = Field(default=None, description="头像URL地址")
#     email: Optional[str] = Field(default=None, description="邮件")
#     email_verified: Optional[bool] = Field(default=None, description="邮箱是否已验证")
#     totp_verified: Optional[bool] = Field(default=None, description="启用身份验证器")
#     role: Optional[str] = Field(default=None, description="用户角色")
#     roles: Optional[str] = Field(default=None, description="角色列表")
#     groups: Optional[str] = Field(default=None, description="部门列表")
#     permissions: Optional[str] = Field(default=None, description="权限列表")
#     organization: Optional[str] = Field(default=None, description="所属组织")
#     department: Optional[str] = Field(default=None, description="所在部门")
#     job_title: Optional[str] = Field(default=None, description="职务职称")
#     staff_id: Optional[int] = Field(default=None, sa_type=BigInteger)
# 
#     model_config = ConfigDict(populate_by_name=True)
# 
# 
# class AuthUserUpdate(SQLModel):
#     """前端更新模型 - 用于接口请求"""
# 
#     user_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="内码")
#     username: Optional[str] = Field(default=None, max_length=50, description="账户名")
#     name: Optional[str] = Field(default=None, description="姓名")
#     password: Optional[str] = Field(default=None, description="密码")
#     is_active: Optional[bool] = Field(default=None, description="启用状态")
#     last_login_at: Optional[datetime] = Field(default=None, description="最后登录时间")
#     nickname: Optional[str] = Field(default=None, description="昵称")
#     picture: Optional[str] = Field(default=None, description="头像URL地址")
#     email: Optional[str] = Field(default=None, description="邮件")
#     email_verified: Optional[bool] = Field(default=None, description="邮箱是否已验证")
#     totp_verified: Optional[bool] = Field(default=None, description="启用身份验证器")
#     role: Optional[str] = Field(default=None, description="用户角色")
#     roles: Optional[str] = Field(default=None, description="角色列表")
#     groups: Optional[str] = Field(default=None, description="部门列表")
#     permissions: Optional[str] = Field(default=None, description="权限列表")
#     organization: Optional[str] = Field(default=None, description="所属组织")
#     department: Optional[str] = Field(default=None, description="所在部门")
#     job_title: Optional[str] = Field(default=None, description="职务职称")
#     staff_id: Optional[int] = Field(default=None, sa_type=BigInteger)
# 
#     model_config = ConfigDict(populate_by_name=True)
# 
# 
# class AuthUserResponse(BaseResponse):
#     """前端响应模型 - 用于接口响应"""
# 
#     __database_schema__ = PackageConfig.SchemaName  # 仅用于内部处理
#     user_id: int = Field(description="内码", sa_type=BigInteger)
#     username: str = Field(description="账户名")
#     name: Optional[str] = Field(description="姓名", default=None)
#     password: str = Field(description="密码")
#     is_active: bool = Field(description="启用状态")
#     last_login_at: Optional[datetime] = Field(description="最后登录时间", default=None)
#     nickname: Optional[str] = Field(description="昵称", default=None)
#     picture: Optional[str] = Field(description="头像URL地址", default=None)
#     email: Optional[str] = Field(description="邮件", default=None)
#     email_verified: Optional[bool] = Field(description="邮箱是否已验证", default=None)
#     totp_verified: Optional[bool] = Field(description="启用身份验证器", default=None)
#     role: Optional[str] = Field(description="用户角色", default=None)
#     roles: Optional[str] = Field(description="角色列表", default=None)
#     groups: Optional[str] = Field(description="部门列表", default=None)
#     permissions: Optional[str] = Field(description="权限列表", default=None)
#     organization: Optional[str] = Field(description="所属组织", default=None)
#     department: Optional[str] = Field(description="所在部门", default=None)
#     job_title: Optional[str] = Field(description="职务职称", default=None)
#     create_by: Optional[str] = Field(description="创建人", default=None)
#     create_at: Optional[datetime] = Field(description="创建日期", default=None)
#     update_by: Optional[str] = Field(description="修改人", default=None)
#     update_at: Optional[datetime] = Field(description="修改日期", default=None)
#     staff_id: Optional[int] = Field(default=None, sa_type=BigInteger)
# 
#     model_config = ConfigDict(populate_by_name=True)
# 
