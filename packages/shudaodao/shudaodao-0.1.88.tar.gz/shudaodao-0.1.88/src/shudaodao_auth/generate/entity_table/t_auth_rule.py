#!/usr/bin/env python3
# # -*- coding:utf-8 -*-
# # @License  ：(C)Copyright 2025, 数道智融科技
# # @Author   ：Shudaodao Auto Generator
# # @Software ：PyCharm
# # @Desc     ：SQLModel classes for shudaodao_auth.t_auth_rule
# 
# from typing import Optional
# from pydantic import ConfigDict
# 
# from shudaodao_core import SQLModel, BaseResponse, Field, get_primary_id
# from ...package_config import PackageConfig
# 
# 
# class AuthRule(PackageConfig.RegistryModel, table=True):
#     """数据库对象模型"""
# 
#     __tablename__ = "t_auth_rule"
#     __table_args__ = {"schema": PackageConfig.SchemaTable, "comment": "访问控制规则表"}
#     # 仅用于内部处理
#     __database_schema__ = PackageConfig.SchemaName
#     __primary_key__ = ["id"]
# 
#     id: int = Field(
#         default=None, primary_key=True, sa_column_kwargs={"autoincrement": True}, description="内码"
#     )
#     ptype: Optional[str] = Field(default=None, nullable=True, max_length=255, description="类型")
#     v0: Optional[str] = Field(default=None, nullable=True, max_length=255, description="角色/用户")
#     v1: Optional[str] = Field(default=None, nullable=True, max_length=255, description="资源/角色")
#     v2: Optional[str] = Field(default=None, nullable=True, max_length=255, description="动作")
#     v3: Optional[str] = Field(default=None, nullable=True, max_length=255, description="租户")
#     v4: Optional[str] = Field(default=None, nullable=True, max_length=255)
#     v5: Optional[str] = Field(default=None, nullable=True, max_length=255)
# 
# 
# class AuthRuleCreate(SQLModel):
#     """前端创建模型 - 用于接口请求"""
# 
#     ptype: Optional[str] = Field(default=None, max_length=255, description="类型")
#     v0: Optional[str] = Field(default=None, max_length=255, description="角色/用户")
#     v1: Optional[str] = Field(default=None, max_length=255, description="资源/角色")
#     v2: Optional[str] = Field(default=None, max_length=255, description="动作")
#     v3: Optional[str] = Field(default=None, max_length=255, description="租户")
#     v4: Optional[str] = Field(default=None, max_length=255)
#     v5: Optional[str] = Field(default=None, max_length=255)
# 
#     model_config = ConfigDict(populate_by_name=True)
# 
# 
# class AuthRuleUpdate(SQLModel):
#     """前端更新模型 - 用于接口请求"""
# 
#     id: Optional[int] = Field(default=None, description="内码")
#     ptype: Optional[str] = Field(default=None, max_length=255, description="类型")
#     v0: Optional[str] = Field(default=None, max_length=255, description="角色/用户")
#     v1: Optional[str] = Field(default=None, max_length=255, description="资源/角色")
#     v2: Optional[str] = Field(default=None, max_length=255, description="动作")
#     v3: Optional[str] = Field(default=None, max_length=255, description="租户")
#     v4: Optional[str] = Field(default=None, max_length=255)
#     v5: Optional[str] = Field(default=None, max_length=255)
# 
#     model_config = ConfigDict(populate_by_name=True)
# 
# 
# class AuthRuleResponse(BaseResponse):
#     """前端响应模型 - 用于接口响应"""
# 
#     __database_schema__ = PackageConfig.SchemaName  # 仅用于内部处理
#     id: int = Field(description="内码")
#     ptype: Optional[str] = Field(description="类型", default=None)
#     v0: Optional[str] = Field(description="角色/用户", default=None)
#     v1: Optional[str] = Field(description="资源/角色", default=None)
#     v2: Optional[str] = Field(description="动作", default=None)
#     v3: Optional[str] = Field(description="租户", default=None)
#     v4: Optional[str] = Field(default=None)
#     v5: Optional[str] = Field(default=None)
# 
#     model_config = ConfigDict(populate_by_name=True)
# 
