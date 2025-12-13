#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @License  ：(C)Copyright 2025, 数道智融科技
# @Author   ：李锋
# @Software ：PyCharm
# @Date     ：2025/9/2 下午4:11
# @Desc     ：

from fastapi import Depends

from shudaodao_auth import AuthAPIRouter, AuthService
from shudaodao_auth.entity_table.t_auth_user import AuthUserResponse
from shudaodao_auth.package_config import PackageConfig as AuthMetaConfig
from shudaodao_core import ResponseUtil
from ..package_config import PackageConfig

Auth_Controller = AuthAPIRouter(
    prefix=f"/{AuthMetaConfig.RouterPath}",
    tags=[f"{AuthMetaConfig.RouterTags} - 登录、鉴权"],
    db_engine_name=PackageConfig.EngineName,
)


# 受保护的路由
@Auth_Controller.get("/me", summary="当前用户信息")
async def auth_me(
        current_user: AuthUserResponse = Depends(AuthService.get_current_user)
):
    # return ResponseUtil.success(message="获取用户信息成功", data=current_user)
    result_data = current_user.__dict__
    result_data.update({
        "desc": "-------------------以下非数据库字段，满足Art Design Pro临时登录用-------------------",
        "userId": current_user.user_id,
        "userName": current_user.name,
        "roles": ['R_SUPER', 'R_ADMIN', 'R_USER'],
        "buttons": [],
        "email": current_user.email,
        "avatar": ""
    })
    return ResponseUtil.success(
        message="获取用户信息成功",
        data=result_data
    )
