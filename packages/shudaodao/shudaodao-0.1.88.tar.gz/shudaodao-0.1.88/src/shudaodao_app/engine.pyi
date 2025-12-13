def load_engine() -> None:
    """初始化底层引擎组件。

    包括：
    - RedisEngine：Redis连接池
    - DatabaseEngine：SQLAlchemy异步引擎
    - DiskEngine：本地磁盘存储
    - PermissionEngine：Casbin权限引擎
    """

async def unload_engine() -> None: ...
