from ..exception.service_exception import (
    DataNotFoundException as DataNotFoundException,
    ValidError as ValidError,
)
from ..tools.tenant_manager import TenantManager as TenantManager
from ..type.var import (
    SQLModelCreate as SQLModelCreate,
    SQLModelDB as SQLModelDB,
    SQLModelResponse as SQLModelResponse,
    SQLModelUpdate as SQLModelUpdate,
)
from sqlmodel.ext.asyncio.session import AsyncSession as AsyncSession
from typing import Any

class DataService:
    """通用数据服务类，提供基于 SQLModel 的 CRUD 及高级查询能力。

    支持多租户隔离、自动字段填充（如创建人、租户ID）、分页/列表/树形查询格式，
    并可灵活指定响应模型（response_class）以实现数据脱敏或转换。
    """
    @classmethod
    def db_insert(
        cls,
        db: AsyncSession,
        *,
        model_class: type[SQLModelDB],
        create_model: SQLModelCreate | dict[str, Any],
    ) -> SQLModelDB: ...
    @classmethod
    async def create(
        cls,
        db: AsyncSession,
        *,
        model_class: type[SQLModelDB],
        create_model: SQLModelCreate | dict[str, Any],
        response_class: type[SQLModelResponse] = None,
    ) -> SQLModelDB | SQLModelResponse:
        """创建新记录并可选自动提交。

        Args:
            db (AsyncSession): 异步数据库会话。
            model_class (Type[SQLModelDB]): 数据库模型类。
            create_model (SQLModelCreate | dict[str, Any]): 创建数据。
            response_class (Type[SQLModelResponse], optional): 响应模型类，用于返回转换后的数据。

        Returns:
            SQLModelDB | SQLModelResponse: 创建成功的模型实例或其响应表示。
        """
    @classmethod
    async def db_get(
        cls,
        db: AsyncSession,
        primary_id: Any | tuple[Any, ...],
        *,
        model_class: type[SQLModelDB],
    ) -> SQLModelDB | None: ...
    @classmethod
    async def read(
        cls,
        db: AsyncSession,
        primary_id: Any | tuple[Any, ...],
        *,
        model_class: type[SQLModelDB],
        response_class: type[SQLModelResponse] = None,
    ) -> SQLModelDB | SQLModelResponse:
        """读取指定 ID 的记录，若不存在则抛出异常。

        Args:
            db (AsyncSession): 异步数据库会话。
            primary_id (Union[Any, Tuple[Any, ...]]): 主键 ID。
            model_class (Type[SQLModelDB]): 数据库模型类。
            response_class (Type[SQLModelResponse], optional): 响应模型类。

        Returns:
            SQLModelDB | SQLModelResponse: 查询到的记录。

        Raises:
            DataNotFoundException: 若记录不存在或无权限访问。
        """
    @classmethod
    async def db_update(
        cls,
        db: AsyncSession,
        primary_id: Any | tuple[Any, ...],
        *,
        model_class: type[SQLModelDB],
        update_model: SQLModelUpdate | dict[str, Any],
    ) -> SQLModelDB | None: ...
    @classmethod
    async def update(
        cls,
        db: AsyncSession,
        primary_id: Any | tuple[Any, ...],
        *,
        model_class: type[SQLModelDB],
        update_model: SQLModelUpdate | dict[str, Any],
        response_class: type[SQLModelResponse] = None,
    ) -> SQLModelDB | SQLModelResponse:
        """更新记录并可选自动提交。

        Args:
            db (AsyncSession): 异步数据库会话。
            primary_id (Union[Any, Tuple[Any, ...]]): 主键 ID。
            model_class (Type[SQLModelDB]): 数据库模型类。
            update_model (SQLModelUpdate | dict[str, Any]): 更新数据。
            response_class (Type[SQLModelResponse], optional): 响应模型类。

        Returns:
            SQLModelDB | SQLModelResponse: 更新后的记录。

        Raises:
            DataNotFoundException: 若记录不存在或无权限访问。
        """
    @classmethod
    async def db_delete(
        cls,
        db: AsyncSession,
        primary_id: Any | tuple[Any, ...],
        *,
        model_class: type[SQLModelDB],
    ) -> bool:
        """删除指定 ID 的记录（不提交事务，不抛异常）。

        Args:
            db (AsyncSession): 异步数据库会话。
            primary_id (Union[Any, Tuple[Any, ...]]): 主键 ID。
            model_class (Type[SQLModelDB]): 数据库模型类。

        Returns:
            bool: 若成功删除返回 True；若记录不存在或无权限，返回 False。
        """
    @classmethod
    async def delete(
        cls,
        db: AsyncSession,
        primary_id: Any | tuple[Any, ...],
        *,
        model_class: type[SQLModelDB],
    ) -> bool:
        """删除记录并可选自动提交。

        Args:
            db (AsyncSession): 异步数据库会话。
            primary_id (Union[Any, Tuple[Any, ...]]): 主键 ID。
            model_class (Type[SQLModelDB]): 数据库模型类。

        Returns:
            bool: 删除成功返回 True。

        Raises:
            DataNotFoundException: 若记录不存在或无权限访问。
        """
    @staticmethod
    def reset_schema(db: AsyncSession, model_class: type[SQLModelDB]):
        """重置模型的 schema，以兼容 SQLite 等不支持 schema 的数据库。

        Args:
            db (AsyncSession): 数据库会话。
            model_class (Type[SQLModelDB]): 数据库模型类。
        """
    @classmethod
    def get_primary_id(cls, data_model, model_class): ...
    @classmethod
    def get_primary_key_name(
        cls, model_class: type[SQLModelDB]
    ) -> str | list[str] | None:
        """获取模型的主键字段名称。

        Args:
            model_class (type[SQLModelDB]): SQLModel 模型类。

        Returns:
            Union[str, list[str], None]:
                - 单个主键时返回字段名（str），
                - 复合主键时返回字段名列表（list[str]），
                - 无主键时返回 None。
        """
