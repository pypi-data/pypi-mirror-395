from shudaodao_core import AsyncSession as AsyncSession

class EnumService:
    @classmethod
    async def initialize(cls, db: AsyncSession): ...
    @classmethod
    async def clear(cls) -> None: ...
