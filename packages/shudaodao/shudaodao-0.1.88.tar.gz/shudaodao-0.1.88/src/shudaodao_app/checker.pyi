async def check_metadata_to_database(source_metadata, engine_name):
    """在开发环境下自动同步数据库表结构"""

async def check_admin_user() -> None:
    """在开发环境下检查并创建默认管理员账户。
    遍历 AppConfig.auth.default_admin_users 中定义的用户名，
    若数据库中不存在，则使用用户名作为密码（明文哈希后）创建新用户。
    仅在 AppConfig.environment.model == "dev" 时执行。
    """
