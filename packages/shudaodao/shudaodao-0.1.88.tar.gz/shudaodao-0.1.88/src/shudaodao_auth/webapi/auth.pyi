from ..auth.auth_router import AuthAPIRouter as AuthAPIRouter
from ..entity_table.t_auth_user import (
    AuthLogin as AuthLogin,
    AuthPassword as AuthPassword,
    AuthUser as AuthUser,
    AuthUserRegister as AuthUserRegister,
    AuthUserResponse as AuthUserResponse,
)
from ..package_config import PackageConfig as PackageConfig
from ..services.auth_service import AuthService as AuthService
from _typeshed import Incomplete
from fastapi.security import OAuth2PasswordRequestForm as OAuth2PasswordRequestForm
from shudaodao_core.schemas.response import TokenRefreshModel as TokenRefreshModel
from sqlmodel.ext.asyncio.session import AsyncSession as AsyncSession

Auth_Controller: Incomplete

async def auth_register(register_model: AuthUserRegister, db: AsyncSession = ...): ...
async def auth_login(login_model: AuthLogin, db: AsyncSession = ...): ...
async def auth_token(
    form_data: OAuth2PasswordRequestForm = ..., db: AsyncSession = ...
): ...
async def auth_refresh(refresh_model: TokenRefreshModel, db: AsyncSession = ...): ...
async def auth_logout(): ...
async def auth_me_password(
    password_model: AuthPassword,
    db: AsyncSession = ...,
    current_user: AuthUserResponse = ...,
): ...
