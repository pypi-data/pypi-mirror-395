from ..enums.manager import EnumManager as EnumManager
from ..exception.service_exception import ValidError as ValidError
from ..logger.logging_ import logging as logging
from ..schemas.query_request import (
    Condition as Condition,
    Filter as Filter,
    FilterGroup as FilterGroup,
    QueryRequest as QueryRequest,
)
from ..utils.core_utils import CoreUtil as CoreUtil
from .class_scaner import ClassScanner as ClassScanner
from sqlalchemy import ColumnElement as ColumnElement
from typing import Any

class QueryBuilder:
    @classmethod
    def get_condition(
        cls,
        *,
        model_class,
        is_relation: bool,
        field_name: str,
        field_op: str,
        field_val: str | int | float | bool | list | None,
    ): ...
    @staticmethod
    def get_condition_python_value(field, field_type, field_value): ...
    @classmethod
    async def get_relation_where(
        cls, *, relation_class: dict, filter_obj: Filter | list
    ): ...
    @classmethod
    async def get_table_where(
        cls, *, model_class, filter_obj: Filter | list, is_relation: bool = False
    ) -> ColumnElement | None:
        """主表的查询条件"""
    @classmethod
    async def get_query_relation(
        cls, *, model_class, model_name, include_path, query_tags, query_format
    ): ...
    @classmethod
    async def deep_serialize_sqlmodel(
        cls,
        obj: Any,
        *,
        response_fields: dict,
        is_tree_node,
        relation_fields: dict | None = None,
        tag_name=None,
    ) -> Any: ...
    @classmethod
    def build_children_tree(cls, flat_list): ...
    @classmethod
    def sqlmodel_format_datetime(cls, value): ...
    @classmethod
    def get_fields(
        cls, *, model_class, relation_class, response_class, query_request: QueryRequest
    ): ...
