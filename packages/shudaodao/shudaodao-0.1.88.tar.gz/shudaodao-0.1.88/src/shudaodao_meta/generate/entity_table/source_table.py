#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @License  ：(C)Copyright 2025, 数道智融科技
# @Author   ：Shudaodao Auto Generator
# @Software ：PyCharm
# @Desc     ：SQLModel classes for shudaodao_meta.source_table

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import ConfigDict

from sqlalchemy import BigInteger, Text

from shudaodao_core import SQLModel, BaseResponse, Field, Relationship, get_primary_id
from ...package_config import PackageConfig

if TYPE_CHECKING:
    from .source_column import SourceColumn
    from .source_foreign_key import SourceForeignKey
    from .source_index import SourceIndex
    from .source_primary_key import SourcePrimaryKey
    from .source_referencing_foreign_key import SourceReferencingForeignKey
    from .source_schema import SourceSchema


class SourceTable(PackageConfig.RegistryModel, table=True):
    """数据库对象模型"""

    __tablename__ = "source_table"
    __table_args__ = {"schema": PackageConfig.SchemaTable, "comment": "表元数据"}
    # 仅用于内部处理
    __database_schema__ = PackageConfig.SchemaName
    __primary_key__ = ["source_table_id"]

    source_table_id: int = Field(
        default_factory=get_primary_id, primary_key=True, sa_type=BigInteger, description="主键"
    )
    source_schema_id: int = Field(
        foreign_key=f"{PackageConfig.SchemaForeignKey}source_schema.source_schema_id",
        ondelete="CASCADE",
        sa_type=BigInteger,
        description="外键-模式(schema)",
    )
    table_name: str = Field(max_length=255, description="表名字")
    comment: Optional[str] = Field(default=None, sa_type=Text, nullable=True, description="备注")
    sort_order: int = Field(description="排序权重")
    description: Optional[str] = Field(default=None, nullable=True, max_length=500, description="描述")
    create_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="创建人")
    create_at: Optional[datetime] = Field(default=None, nullable=True, description="创建日期")
    update_by: Optional[str] = Field(default=None, nullable=True, max_length=50, description="修改人")
    update_at: Optional[datetime] = Field(default=None, nullable=True, description="修改日期")
    # 反向关系 - 父对象
    SourceSchema: "SourceSchema" = Relationship(back_populates="SourceTables")
    # 正向关系 - 子对象
    SourceColumns: list["SourceColumn"] = Relationship(
        back_populates="SourceTable",
        cascade_delete=True,
        sa_relationship_kwargs={"order_by": "SourceColumn.sort_order.asc()"},
    )
    # 正向关系 - 子对象
    SourceForeignKeys: list["SourceForeignKey"] = Relationship(
        back_populates="SourceTable",
        cascade_delete=True,
        sa_relationship_kwargs={"order_by": "SourceForeignKey.sort_order.asc()"},
    )
    # 正向关系 - 子对象
    SourceIndexes: list["SourceIndex"] = Relationship(
        back_populates="SourceTable",
        cascade_delete=True,
        sa_relationship_kwargs={"order_by": "SourceIndex.sort_order.asc()"},
    )
    # 正向关系 - 子对象
    SourcePrimaryKey: "SourcePrimaryKey" = Relationship(back_populates="SourceTable", cascade_delete=True)
    # 正向关系 - 子对象
    SourceReferencingForeignKeys: list["SourceReferencingForeignKey"] = Relationship(
        back_populates="SourceTable",
        cascade_delete=True,
        sa_relationship_kwargs={"order_by": "SourceReferencingForeignKey.sort_order.asc()"},
    )


class SourceTableCreate(SQLModel):
    """前端创建模型 - 用于接口请求"""

    source_schema_id: int = Field(sa_type=BigInteger, description="外键-模式(schema)")
    table_name: str = Field(max_length=255, description="表名字")
    comment: Optional[str] = Field(default=None, description="备注")
    sort_order: int = Field(description="排序权重")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")

    model_config = ConfigDict(populate_by_name=True)


class SourceTableUpdate(SQLModel):
    """前端更新模型 - 用于接口请求"""

    source_table_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="主键")
    source_schema_id: Optional[int] = Field(default=None, sa_type=BigInteger, description="外键-模式(schema)")
    table_name: Optional[str] = Field(default=None, max_length=255, description="表名字")
    comment: Optional[str] = Field(default=None, description="备注")
    sort_order: Optional[int] = Field(default=None, description="排序权重")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")

    model_config = ConfigDict(populate_by_name=True)


class SourceTableResponse(BaseResponse):
    """前端响应模型 - 用于接口响应"""

    __database_schema__ = PackageConfig.SchemaName  # 仅用于内部处理
    source_table_id: int = Field(description="主键", sa_type=BigInteger)
    source_schema_id: int = Field(description="外键-模式(schema)", sa_type=BigInteger)
    table_name: str = Field(description="表名字")
    comment: Optional[str] = Field(description="备注", default=None)
    sort_order: int = Field(description="排序权重")
    description: Optional[str] = Field(description="描述", default=None)
    create_by: Optional[str] = Field(description="创建人", default=None)
    create_at: Optional[datetime] = Field(description="创建日期", default=None)
    update_by: Optional[str] = Field(description="修改人", default=None)
    update_at: Optional[datetime] = Field(description="修改日期", default=None)

    model_config = ConfigDict(populate_by_name=True)
