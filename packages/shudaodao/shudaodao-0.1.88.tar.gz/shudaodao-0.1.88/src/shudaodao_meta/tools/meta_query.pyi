from ..generate.entity_table.meta_schema import MetaSchema as MetaSchema
from ..generate.entity_table.meta_table import MetaTable as MetaTable
from ..generate.entity_table.meta_view import MetaView as MetaView
from shudaodao_core import AsyncSession as AsyncSession

class MetaQuery:
    @classmethod
    async def get_schema(cls, db: AsyncSession, schema_name: str) -> MetaSchema: ...
    @classmethod
    async def get_tables_views_by_schema_name(
        cls, db: AsyncSession, schema_name: str, is_active: bool = None
    ): ...
    @classmethod
    async def query_metatable(
        cls, db: AsyncSession, schema_name: str, table_name: str, is_active: bool = None
    ): ...
    @classmethod
    async def query_metaview(
        cls, db: AsyncSession, schema_name: str, view_name: str, is_active: bool = None
    ): ...
