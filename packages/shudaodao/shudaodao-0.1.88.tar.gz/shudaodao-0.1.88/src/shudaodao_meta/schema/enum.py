#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @License  ：(C)Copyright 2025, 数道智融科技
# @Author   ：李锋
# @Software ：PyCharm
# @Date     ：2025/10/23 下午12:49
# @Desc     ：

from typing import List, Optional, Union

from pydantic import BaseModel, Field, model_validator

from shudaodao_core import ValidError


class EnumQueryRequest(BaseModel):
    # schema_name: str = Field(..., description="数据库schema名称", alias="schema")
    key: Optional[Union[List[str], str]] = Field(default=None, description="查询枚举字段名[str|list]")
    name: Optional[Union[List[str], str]] = Field(default=None, description="返回枚举字段名[str|list]")
    pid: Optional[Union[List[str], str]] = Field(default=None, description="父ID[str|list]")

    @model_validator(mode="after")
    def lists_must_have_same_length(self) -> "EnumQueryRequest":
        """验证所有列表长度一致"""
        if isinstance(self.key, str):
            self.key = [self.key]
        if isinstance(self.name, str):
            self.name = [self.name]
        if isinstance(self.pid, str):
            self.pid = [self.pid]
        key_len = len(self.key) if self.key else 0
        name_len = len(self.name) if self.name else 0
        pid_len = len(self.pid) if self.pid else 0

        if self.key and self.name and key_len != name_len:
            raise ValidError(
                message="验证失败: 查询参数不正确",
                fields="key、name",
                errors="key、name 列表长度必须相同"
            )
        if self.key and self.pid and key_len != pid_len:
            raise ValidError(
                message="验证失败: 查询参数不正确",
                fields="pid",
                errors="key、name 列表长度必须相同"
            )

        return self
