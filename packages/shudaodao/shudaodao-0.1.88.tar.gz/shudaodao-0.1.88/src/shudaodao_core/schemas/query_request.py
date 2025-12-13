from typing import List, Optional, Literal, Union

from pydantic import BaseModel, Field


# 基础条件
class Condition(BaseModel):
    field: str = Field(..., description="要查询的字段名")
    op: str = Field(..., description="逻辑运算符")
    val: Union[str, int, float, bool, List, None] = Field(..., description="要查询的值")


# 条件组（递归结构）
class FilterGroup(BaseModel):
    and_: Optional[List[Union[Condition, 'FilterGroup']]] = Field(None, alias="and")
    or_: Optional[List[Union[Condition, 'FilterGroup']]] = Field(None, alias="or")


FilterGroup.model_rebuild()

# filter 字段可以是单个条件或分组
Filter = Union[Condition, FilterGroup]


class QueryRequest(BaseModel):
    fields: Optional[Union[List[str], str]] = Field(None, description="指定要返回的字段 select fields")
    filter: Optional[Union[Filter, List]] = Field(None, description="过滤条件 - where")
    sort: Optional[Union[List[str], str]] = Field(None, description="排序条件列表")
    relation: Optional[List[str]] = Field(None, description="包含父子关系")
    filter_relation: Optional[Union[Filter, List]] = Field(None, description="过滤关系条件 - where")
    tag: Optional[List[str]] = Field(None, description="标签 Format=Tree 时")
    format: Literal["list", "tree", "page"] = "list"
    page: Optional[int] = Field(None, ge=1, description="第几页")
    size: Optional[int] = Field(None, ge=1, le=1000, description="每页多少个")
