from ..engine.casbin_engine import PermissionEngine as PermissionEngine
from _typeshed import Incomplete

class PermissionService:
    """权限服务类，用于管理基于 Casbin 的 RBAC（基于角色的访问控制）权限体系。

    该类负责初始化权限规则、分配角色与权限、验证用户权限等功能，
    支持角色继承、用户-角色绑定，并与数据库持久化策略集成。
    """

    engine: Incomplete
    @classmethod
    async def initialize(cls) -> None: ...
    @classmethod
    async def has_role(cls, user, role): ...
    @classmethod
    def has_permission(cls, user, obj, act): ...
    @classmethod
    def add_policy(cls, auth_sub, auth_obj, auth_act) -> None: ...
