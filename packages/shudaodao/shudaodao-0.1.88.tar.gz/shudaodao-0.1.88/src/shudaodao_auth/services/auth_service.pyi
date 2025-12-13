from ..entity_table.t_auth_user import (
    AuthUser as AuthUser,
    AuthUserResponse as AuthUserResponse,
)
from _typeshed import Incomplete
from fastapi import Request as Request
from fastapi.security import (
    HTTPAuthorizationCredentials as HTTPAuthorizationCredentials,
)
from sqlmodel.ext.asyncio.session import AsyncSession as AsyncSession

class AuthService:
    """认证服务类，处理用户认证、密码验证、JWT令牌管理等操作"""

    TOKEN_SECRET_KEY: Incomplete
    TOKEN_ALGORITHM: str
    TOKEN_EXPIRE_MINUTES: Incomplete
    TOKEN_REFRESH_EXPIRE_DAYS: Incomplete
    http_bearer: Incomplete
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """验证明文密码与哈希密码是否匹配。"""
    @classmethod
    def hash_password(cls, password: str) -> str:
        """对明文密码进行哈希处理。"""
    @classmethod
    def jwt_encode(cls, data: dict) -> str:
        """编码数据生成JWT令牌。

        Args:
            data: 需要编码到令牌中的数据

        Returns:
            str: 编码后的JWT令牌字符串
        """
    @classmethod
    def jwt_decode(cls, token) -> dict:
        """解码JWT令牌获取原始数据。

        Args:
            token: JWT令牌字符串

        Returns:
            dict: 解码后的令牌数据

        Raises:
            AuthError: 当令牌无效或已过期时
        """
    @classmethod
    async def get_current_user_request(
        cls, request: Request, db: AsyncSession = ...
    ): ...
    @classmethod
    async def get_current_user(
        cls, auth_bearer: HTTPAuthorizationCredentials = ..., db: AsyncSession = ...
    ): ...
    @classmethod
    async def logout(cls) -> None:
        """用户登出操作。

        Note:
            此功能尚未实现
        """
    @classmethod
    async def refresh(cls, refresh_token, db: AsyncSession):
        """刷新访问令牌。

        Note:
            此功能尚未实现

        Returns:
            待实现的刷新令牌功能
        """
    @classmethod
    async def login(cls, *, db: AsyncSession, auth_login):
        """用户登录认证。

        Args:
            db: 数据库会话
            auth_login: 登录请求数据模型

        Returns:
            str: JWT访问令牌

        Raises:
            LoginException: 当用户名密码错误、账户未激活或其他登录错误时
        """
    @classmethod
    async def modify_password(cls, db: AsyncSession, *, password_model, current_user):
        """修改用户密码。

        Args:
            db: 数据库会话
            password_model: 密码修改数据模型
            current_user: 当前用户信息

        Raises:
            AuthException: 当原始密码不正确或密码修改失败时
        """
