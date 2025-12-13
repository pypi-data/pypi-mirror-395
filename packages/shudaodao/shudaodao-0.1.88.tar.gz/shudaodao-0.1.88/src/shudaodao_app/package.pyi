from .checker import check_metadata_to_database as check_metadata_to_database

def load_router(fastapi) -> None:
    """从 AppConfig 加载并注册所有启用的路由模块"""

async def load_meta_config() -> None: ...
