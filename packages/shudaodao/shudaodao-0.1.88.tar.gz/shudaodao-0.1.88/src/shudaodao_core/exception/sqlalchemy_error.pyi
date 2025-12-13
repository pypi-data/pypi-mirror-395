from sqlalchemy.exc import SQLAlchemyError as SQLAlchemyError

def format_sqlalchemy_error(exc: SQLAlchemyError) -> tuple[str, str]:
    """
    格式化 SQLAlchemy 异常，返回 (友好提示, 原始错误信息)

    :param exc: SQLAlchemy 异常实例
    :return: (message: 友好提示, error: 原始错误信息)
    """
