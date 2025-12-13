from ..services.auth_service import AuthService as AuthService
from _typeshed import Incomplete
from collections.abc import Generator
from fastapi import APIRouter

class AuthAPIRouter(APIRouter):
    """增强版 APIRouter，支持自动注入权限校验依赖。

    在路由注册时自动绑定用户认证、角色检查、数据权限（Casbin）等依赖。
    同时收集权限规则用于后续初始化默认策略（如插入数据库）。

    Class Attributes:
        permission_rules (dict): 静态字典，用于收集所有默认角色的权限规则，
            格式：{role: {obj: [act1, act2, ...]}}，供应用启动时批量初始化 Casbin 策略。
    """

    curr_user: Incomplete
    auth_role: Incomplete
    auth_obj: Incomplete
    auth_act: Incomplete
    db_engine_name: Incomplete
    auth_sub: Incomplete
    def __init__(
        self,
        auth_role: str | None = None,
        auth_sub: str | None = None,
        auth_obj: str | None = None,
        auth_act: str | None = None,
        db_engine_name: str | None = None,
        *args,
        **kwargs,
    ) -> None:
        """初始化 AuthAPIRouter 实例。

        Args:
            auth_role (Optional[str]): 指定角色校验（可被单个路由覆盖）。
            auth_sub (Optional[str]): 指定验证主体（一般是schema_name，Casbin 中的 sub）。
            auth_obj (Optional[str]): 指定验证对象（一般是table_name\x0biew_name，Casbin 中的 obj，可被单个路由覆盖）。
            auth_act (Optional[str]): 指定验证操作（crud、query、list、tree，Casbin 中的 act）。
            db_engine_name (Optional[str]): 数据库配置名称，用于 get_async_session。
            *args: 透传给父类 APIRouter。
            **kwargs: 透传给父类 APIRouter。
        """
    async def get_async_session(self) -> Generator[Incomplete]:
        """提供依赖注入用的异步数据库会话"""
    def check_auth(self, auth_role: str, auth_obj: str, auth_act: str): ...
    def api_route(
        self,
        path: str,
        *,
        auth: bool = True,
        auth_sub: str | None = None,
        auth_role: str | None = None,
        auth_obj: str | None = None,
        auth_act: str | None = None,
        **kwargs,
    ):
        """注册路由并自动注入权限依赖。
        支持按需启用用户认证、角色校验、数据权限校验。
        Args:
            path (str): 路由路径。
            auth (bool): 是否启用认证（默认 True）。
            auth_role (Optional[str]): 指定角色校验。
            auth_sub (Optional[str]): 指定验证主体（Casbin sub）。
            auth_obj (Optional[str]): 指定验证对象（Casbin obj）。
            auth_act (Optional[str]): 指定验证操作（Casbin act）。
            **kwargs: 透传给父类 api_route。
        Returns:
            Callable: 路由装饰器。
        """
    def get(
        self,
        path: str,
        *,
        auth: bool = True,
        auth_role: str | None = None,
        auth_sub: str | None = None,
        auth_obj: str | None = None,
        auth_act: str | None = None,
        **kwargs,
    ):
        """注册 GET 路由并自动注入权限依赖。

        Args:
            path (str): 路由路径。
            auth (bool): 是否启用认证。
            auth_role (Optional[str]): 指定角色校验。
            auth_sub (Optional[str]): 指定验证主体（Casbin sub）。
            auth_obj (Optional[str]): 指定验证对象（Casbin obj）。
            auth_act (Optional[str]): 指定验证操作（Casbin act）。
            **kwargs: 透传参数。

        Returns:
            Callable: 路由装饰器。
        """
    def post(
        self,
        path: str,
        *,
        auth: bool = True,
        auth_role: str | None = None,
        auth_sub: str | None = None,
        auth_obj: str | None = None,
        auth_act: str | None = None,
        **kwargs,
    ):
        """注册 POST 路由并自动注入权限依赖。

        Args:
            path (str): 路由路径。
            auth (bool): 是否启用认证。
            auth_role (Optional[str]): 指定角色校验。
            auth_sub (Optional[str]): 指定验证主体（Casbin sub）。
            auth_obj (Optional[str]): 指定验证对象（Casbin obj）。
            auth_act (Optional[str]): 指定验证操作（Casbin act）。
            **kwargs: 透传参数。

        Returns:
            Callable: 路由装饰器。
        """
    def put(
        self,
        path: str,
        *,
        auth: bool = True,
        auth_role: str | None = None,
        auth_sub: str | None = None,
        auth_obj: str | None = None,
        auth_act: str | None = None,
        **kwargs,
    ):
        """注册 PUT 路由并自动注入权限依赖。

        Args:
            path (str): 路由路径。
            auth (bool): 是否启用认证。
            auth_role (Optional[str]): 指定角色校验。
            auth_sub (Optional[str]): 指定验证主体（Casbin sub）。
            auth_obj (Optional[str]): 指定验证对象（Casbin obj）。
            auth_act (Optional[str]): 指定验证操作（Casbin act）。
            **kwargs: 透传参数。

        Returns:
            Callable: 路由装饰器。
        """
    def patch(
        self,
        path: str,
        *,
        auth: bool = True,
        auth_role: str | None = None,
        auth_sub: str | None = None,
        auth_obj: str | None = None,
        auth_act: str | None = None,
        **kwargs,
    ):
        """注册 PATCH 路由并自动注入权限依赖。

        Args:
            path (str): 路由路径。
            auth (bool): 是否启用认证。
            auth_role (Optional[str]): 指定角色校验。
            auth_sub (Optional[str]): 指定验证主体（Casbin sub）。
            auth_obj (Optional[str]): 指定验证对象（Casbin obj）。
            auth_act (Optional[str]): 指定验证操作（Casbin act）。
            **kwargs: 透传参数。

        Returns:
            Callable: 路由装饰器。
        """
    def delete(
        self,
        path: str,
        *,
        auth: bool = True,
        auth_role: str | None = None,
        auth_sub: str | None = None,
        auth_obj: str | None = None,
        auth_act: str | None = None,
        **kwargs,
    ):
        """注册 DELETE 路由并自动注入权限依赖。

        Args:
            path (str): 路由路径。
            auth (bool): 是否启用认证。
            auth_role (Optional[str]): 指定角色校验。
            auth_sub (Optional[str]): 指定验证主体（Casbin sub）。
            auth_obj (Optional[str]): 指定验证对象（Casbin obj）。
            auth_act (Optional[str]): 指定验证操作（Casbin act）。
            **kwargs: 透传参数。

        Returns:
            Callable: 路由装饰器。
        """
