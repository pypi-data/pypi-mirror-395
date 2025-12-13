from ..exception.service_exception import ValidError as ValidError
from ..schemas.element import Paging as Paging
from ..schemas.query_request import QueryRequest as QueryRequest
from ..tools.query_builder import QueryBuilder as QueryBuilder
from ..tools.tenant_manager import TenantManager as TenantManager
from ..type.var import SQLModelDB as SQLModelDB, SQLModelResponse as SQLModelResponse
from .data_service import DataService as DataService
from sqlalchemy import ColumnElement
from sqlmodel.ext.asyncio.session import AsyncSession as AsyncSession
from typing import Any

class QueryService:
    @classmethod
    def check_query_request(cls, query: QueryRequest): ...
    @classmethod
    async def query_columns_one(
        cls,
        db: AsyncSession,
        *,
        model_class: type[SQLModelDB],
        condition: list[ColumnElement] | ColumnElement | Any,
    ) -> SQLModelDB:
        """根据列条件查询唯一记录"""
    @classmethod
    async def query_columns_first(
        cls,
        db: AsyncSession,
        *,
        model_class: type[SQLModelDB],
        condition: list[ColumnElement] | ColumnElement | Any,
    ) -> SQLModelDB:
        """根据列条件查询单条记录"""
    @classmethod
    async def query_columns_all(
        cls,
        db: AsyncSession,
        *,
        model_class: type[SQLModelDB],
        condition: list[ColumnElement] | ColumnElement | Any,
    ):
        """根据列条件查询所有记录"""
    @classmethod
    def get_condition_from_columns(cls, condition, model_class): ...
    @classmethod
    async def db_query_one(
        cls,
        db: AsyncSession,
        *,
        query_request: QueryRequest,
        model_class: type[SQLModelDB],
    ): ...
    @classmethod
    async def db_query_first(
        cls,
        db: AsyncSession,
        *,
        query_request: QueryRequest,
        model_class: type[SQLModelDB],
    ): ...
    @classmethod
    async def db_query_all(
        cls,
        db: AsyncSession,
        *,
        query_request: QueryRequest,
        model_class: type[SQLModelDB],
    ): ...
    @classmethod
    async def query(
        cls,
        db: AsyncSession,
        *,
        query_request: QueryRequest,
        model_class: type[SQLModelDB],
        response_class: type[SQLModelResponse],
    ): ...
    @classmethod
    def get_order_by(cls, statement, model_class, query_sort): ...
    @classmethod
    async def get_count_where(
        cls, *, statement, model_class: type[SQLModelDB], query_request: QueryRequest
    ) -> Any: ...
    @classmethod
    async def get_where(
        cls,
        *,
        statement,
        model_class: type[SQLModelDB],
        relation_class,
        query_request: QueryRequest,
    ) -> Any: ...
    @classmethod
    async def get_select(cls, model_class, query_request: QueryRequest): ...
    @classmethod
    async def serialize_nested(
        cls,
        obj: Any,
        *,
        model_class: type[SQLModelDB],
        relation_fields: dict | None = None,
        relation_class: dict | None = None,
        response_class: Any = None,
        query_request: QueryRequest = None,
    ) -> Any: ...
