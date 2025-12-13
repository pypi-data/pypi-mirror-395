from _typeshed import Incomplete
from typing import Any

class ShudaodaoException(Exception):
    code: Incomplete
    errors: Incomplete
    message: Incomplete
    def __init__(self, *, code: int, message: str, errors: Any = None) -> None: ...

class ValidError(ShudaodaoException):
    def __init__(
        self,
        *,
        message: str = None,
        fields: list[str] | str = None,
        errors: list[str] | str = None,
    ) -> None: ...

class AuthError(ShudaodaoException):
    def __init__(self, message: str, errors: Any = None) -> None: ...

class PermError(ShudaodaoException):
    """自定义 权限异常"""
    def __init__(self, message: str, errors: Any = None) -> None: ...

class ServiceError(ShudaodaoException):
    """自定义 服务异常"""
    def __init__(self, *, message: str, errors: Any = None) -> None: ...

class DataNotFoundException(ShudaodaoException):
    """自定义项目未找到异常"""
    def __init__(
        self,
        *,
        message: str = "数据未找到",
        model_class: str | None = None,
        primary_id: int | None = None,
        primary_field: str | list[str] | None = None,
    ) -> None: ...
