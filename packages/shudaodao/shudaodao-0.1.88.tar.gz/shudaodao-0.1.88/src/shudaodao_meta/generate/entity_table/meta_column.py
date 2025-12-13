#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @License  ：(C)Copyright 2025, 数道智融科技
# @Author   ：Shudaodao Auto Generator
# @Software ：PyCharm
# @Desc     ：SQLModel classes for shudaodao_meta.meta_column

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import ConfigDict

from sqlalchemy import BigInteger, Boolean

from shudaodao_core import SQLModel, BaseResponse, Field, Relationship, get_primary_id
from ...package_config import PackageConfig

if TYPE_CHECKING:
    from .meta_table import MetaTable
    from .meta_view import MetaView


class MetaColumn(PackageConfig.RegistryModel, table=True):
    """数据库对象模型"""

    __tablename__ = "meta_column"
    __table_args__ = {"schema": PackageConfig.SchemaTable, "comment": "字段元数据"}
    # 仅用于内部处理
    __database_schema__ = PackageConfig.SchemaName
    __primary_key__ = ["meta_column_id"]

    meta_column_id: int = Field(
        default_factory=get_primary_id, primary_key=True, sa_type=BigInteger, description="主键"
    )
    meta_table_id: Optional[int] = Field(
        default=None,
        foreign_key=f"{PackageConfig.SchemaForeignKey}meta_table.meta_table_id",
        ondelete="CASCADE",
        sa_type=BigInteger,
        nullable=True,
        description="主键",
    )
    meta_view_id: Optional[int] = Field(
        default=None,
        foreign_key=f"{PackageConfig.SchemaForeignKey}meta_view.meta_view_id",
        ondelete="CASCADE",
        sa_type=BigInteger,
        nullable=True,
        description="主键",
    )
    name: str = Field(max_length=255, description="字段名")
    alias: Optional[str] = Field(default=None, nullable=True, max_length=255, description="字段别名")
    model_type: Optional[str] = Field(default=None, nullable=True, max_length=20, description="模型类型")
    is_primary: Optional[bool] = Field(default=None, sa_type=Boolean, nullable=True, description="主键字段")
    is_increment: Optional[bool] = Field(default=None, sa_type=Boolean, nullable=True, description="启用自增")
    is_unique: Optional[bool] = Field(default=None, sa_type=Boolean, nullable=True, description="单字段唯一")
    is_index: Optional[bool] = Field(default=None, sa_type=Boolean, nullable=True, description="单字段索引")
    py_type: str = Field(max_length=30, description="python类型")
    sa_type: str = Field(max_length=30, description="sqlalchemy类型")
    db_type: str = Field(max_length=20, description="database类型[仅用于展示]")
    nullable: bool = Field(sa_type=Boolean, description="是否可空")
    default: Optional[str] = Field(default=None, nullable=True, max_length=50, description="默认值(一般不用)")
    max_length: Optional[int] = Field(default=None, nullable=True, description="最大长度")
    precision: Optional[int] = Field(default=None, nullable=True, description="总位数")
    comment: Optional[str] = Field(default=None, nullable=True, max_length=255, description="字段说明")
    is_active: bool = Field(sa_type=Boolean, description="启用状态")
    scale: Optional[int] = Field(default=None, nullable=True, description="小数位数")
    sort_order: int = Field(description="排序权重")
    description: Optional[str] = Field(default=None, nullable=True, max_length=500, description="描述")
    create_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="创建人")
    create_at: Optional[datetime] = Field(default=None, nullable=True, description="创建日期")
    update_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="修改人")
    update_at: Optional[datetime] = Field(default=None, nullable=True, description="修改日期")
    # 反向关系 - 父对象
    MetaTable: "MetaTable" = Relationship(back_populates="MetaColumns")
    # 反向关系 - 父对象
    MetaView: "MetaView" = Relationship(back_populates="MetaColumns")


class MetaColumnCreate(SQLModel):
    """前端创建模型 - 用于接口请求"""

    meta_table_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="主键")
    meta_view_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="主键")
    name: str = Field(max_length=255, description="字段名")
    alias: Optional[str] = Field(default=None, max_length=255, description="字段别名")
    model_type: Optional[str] = Field(default=None, max_length=20, description="模型类型")
    is_primary: Optional[bool] = Field(default=None, description="主键字段")
    is_increment: Optional[bool] = Field(default=None, description="启用自增")
    is_unique: Optional[bool] = Field(default=None, description="单字段唯一")
    is_index: Optional[bool] = Field(default=None, description="单字段索引")
    py_type: str = Field(max_length=30, description="python类型")
    sa_type: str = Field(max_length=30, description="sqlalchemy类型")
    db_type: str = Field(max_length=20, description="database类型[仅用于展示]")
    nullable: bool = Field(description="是否可空")
    default: Optional[str] = Field(default=None, max_length=50, description="默认值(一般不用)")
    max_length: Optional[int] = Field(default=None, description="最大长度")
    precision: Optional[int] = Field(default=None, description="总位数")
    comment: Optional[str] = Field(default=None, max_length=255, description="字段说明")
    is_active: bool = Field(description="启用状态")
    scale: Optional[int] = Field(default=None, description="小数位数")
    sort_order: int = Field(description="排序权重")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")

    model_config = ConfigDict(populate_by_name=True)


class MetaColumnUpdate(SQLModel):
    """前端更新模型 - 用于接口请求"""

    meta_column_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="主键")
    meta_table_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="主键")
    meta_view_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="主键")
    name: Optional[str] = Field(default=None, max_length=255, description="字段名")
    alias: Optional[str] = Field(default=None, max_length=255, description="字段别名")
    model_type: Optional[str] = Field(default=None, max_length=20, description="模型类型")
    is_primary: Optional[bool] = Field(default=None, description="主键字段")
    is_increment: Optional[bool] = Field(default=None, description="启用自增")
    is_unique: Optional[bool] = Field(default=None, description="单字段唯一")
    is_index: Optional[bool] = Field(default=None, description="单字段索引")
    py_type: Optional[str] = Field(default=None, max_length=30, description="python类型")
    sa_type: Optional[str] = Field(default=None, max_length=30, description="sqlalchemy类型")
    db_type: Optional[str] = Field(default=None, max_length=20, description="database类型[仅用于展示]")
    nullable: Optional[bool] = Field(default=None, description="是否可空")
    default: Optional[str] = Field(default=None, max_length=50, description="默认值(一般不用)")
    max_length: Optional[int] = Field(default=None, description="最大长度")
    precision: Optional[int] = Field(default=None, description="总位数")
    comment: Optional[str] = Field(default=None, max_length=255, description="字段说明")
    is_active: Optional[bool] = Field(default=None, description="启用状态")
    scale: Optional[int] = Field(default=None, description="小数位数")
    sort_order: Optional[int] = Field(default=None, description="排序权重")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")

    model_config = ConfigDict(populate_by_name=True)


class MetaColumnResponse(BaseResponse):
    """前端响应模型 - 用于接口响应"""

    __database_schema__ = PackageConfig.SchemaName  # 仅用于内部处理
    meta_column_id: int = Field(description="主键", sa_type=BigInteger)
    meta_table_id: Optional[int] = Field(description="主键", default=None, sa_type=BigInteger)
    meta_view_id: Optional[int] = Field(description="主键", default=None, sa_type=BigInteger)
    name: str = Field(description="字段名")
    alias: Optional[str] = Field(description="字段别名", default=None)
    model_type: Optional[str] = Field(description="模型类型", default=None)
    is_primary: Optional[bool] = Field(description="主键字段", default=None)
    is_increment: Optional[bool] = Field(description="启用自增", default=None)
    is_unique: Optional[bool] = Field(description="单字段唯一", default=None)
    is_index: Optional[bool] = Field(description="单字段索引", default=None)
    py_type: str = Field(description="python类型")
    sa_type: str = Field(description="sqlalchemy类型")
    db_type: str = Field(description="database类型[仅用于展示]")
    nullable: bool = Field(description="是否可空")
    default: Optional[str] = Field(description="默认值(一般不用)", default=None)
    max_length: Optional[int] = Field(description="最大长度", default=None)
    precision: Optional[int] = Field(description="总位数", default=None)
    comment: Optional[str] = Field(description="字段说明", default=None)
    is_active: bool = Field(description="启用状态")
    scale: Optional[int] = Field(description="小数位数", default=None)
    sort_order: int = Field(description="排序权重")
    description: Optional[str] = Field(description="描述", default=None)
    create_by: Optional[str] = Field(description="创建人", default=None)
    create_at: Optional[datetime] = Field(description="创建日期", default=None)
    update_by: Optional[str] = Field(description="修改人", default=None)
    update_at: Optional[datetime] = Field(description="修改日期", default=None)

    model_config = ConfigDict(populate_by_name=True)
