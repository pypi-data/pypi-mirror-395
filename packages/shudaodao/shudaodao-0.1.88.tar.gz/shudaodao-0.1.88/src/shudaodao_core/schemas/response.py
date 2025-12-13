#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @License  ：(C)Copyright 2025, 数道智融科技
# @Author   ：李锋
# @Software ：PyCharm
# @Date     ：2025/8/18 下午7:43
# @Desc     ：
from datetime import datetime, date, time
from typing import Any, Dict
from typing import Optional

from pydantic import Field, BaseModel
from sqlalchemy import BigInteger
from sqlmodel import SQLModel

from ..enums.manager import EnumManager
from ..utils.core_utils import CoreUtil


class BaseResponse(SQLModel):
    """
    支持 sa_type=BigInteger 转 字符串
    支持 日期格式化
    支持 枚举转化，新增字段 key_label
    支持嵌套模型递归转换
    """

    def model_dump(self, *args, **kwargs) -> Dict[str, Any]:
        # 先获取原始 dump 结果（不包含嵌套模型的转换）
        data = super().model_dump(*args, **kwargs)

        # 遍历所有字段定义
        for field_name, field_info in self.model_fields.items():
            # value = data.get(field_name)  # 从原始数据字典获取 无法进行实例判断
            value = getattr(self, field_name)  # 从模型实例获取 才能判断类型
            if value is None:
                continue

            # 1. BigInteger → str  雪花算法ID
            if hasattr(field_info, 'sa_type') and field_info.sa_type is BigInteger:
                data[field_name] = str(value)
            # 2. datetime → ISO 8601 字符串
            elif isinstance(value, datetime):
                data[field_name] = CoreUtil.format_datatime(value.isoformat())
            # 3. date → YYYY-MM-DD
            elif isinstance(value, date):
                data[field_name] = value.isoformat()  # "2025-09-22"
            # 4. time → HH:MM:SS
            elif isinstance(value, time):
                data[field_name] = value.isoformat()  # "10:30:00"
            # 5. BaseReadModel 实例 → 递归转换
            elif isinstance(value, BaseResponse):
                dump_value = value.model_dump(*args, **kwargs)
                data[field_name] = self.base_response_format_enum(value.__class__, dump_value)
            # 6. 字段是列表，且元素是 BaseReadModel → 递归转换每个元素
            elif isinstance(value, list):
                rows = []
                for item in value:
                    if isinstance(item, BaseResponse):
                        dump_value = item.model_dump(*args, **kwargs)
                        rows.append(self.base_response_format_enum(item.__class__, dump_value))
                    else:
                        rows.append(item)
                data[field_name] = rows
        return data

    @staticmethod
    def base_response_format_enum(model_class, dump_value):
        # 获取枚举字段
        enum_fields = EnumManager().get_field_names(model_class)
        if not enum_fields:
            return dump_value

        enum_dict = {}
        for key, val in dump_value.items():
            enum_dict[key] = val
            if key not in enum_fields:
                continue
            # 处理枚举
            enum_dict[key + "_label"] = EnumManager().resolve_value(model_class, key, val)
        return enum_dict

    # 兼容 Pydantic v1 / jsonable_encoder
    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        return self.model_dump(*args, **kwargs)


class SuccessResponse(BaseResponse):
    code: int = Field(200, description="Response code")
    msg: str = ""
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    code: int = Field(..., description="Response code")
    msg: str = ""
    error: Optional[Any] = None


class TokenResponse(BaseModel):
    token_type: str = "Bearer"
    # 成功
    access_token: str
    expires_in: int
    # 刷新
    refresh_token: Optional[str] = None
    refresh_expires_in: int
    # scope: Optional[str] = None # 暂时用不上

    user: str  # Dict[str, Any]  # 暂时用不上
    # Art Design Pro
    # token: str
    # id_token: Optional[str] = None  # 暂时用不上


# class TokenErrorResponse(BaseModel):
#     error: str
#     error_description: str
#     error_code: Optional[str] = None
#     timestamp: str = Field(default_factory=lambda: datetime.now().timestamp())


class TokenRefreshModel(BaseModel):
    refresh_token: str
