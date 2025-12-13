from _typeshed import Incomplete
from pydantic import BaseModel

class AuthItem(BaseModel):
    """权限项"""

    title: str
    authMark: str

class Meta(BaseModel):
    """菜单元数据"""

    title: str
    icon: str | None
    showBadge: bool | None
    showTextBadge: str | None
    isHide: bool | None
    isHideTab: bool | None
    link: str | None
    isIframe: bool | None
    keepAlive: bool | None
    authList: list[AuthItem] | None
    isFirstLevel: bool | None
    roles: list[str] | None
    fixedTab: bool | None

class MenuItem(BaseModel):
    """菜单项（支持无限嵌套）"""

    name: str
    path: str
    component: str | None
    meta: Meta
    children: list["MenuItem"] | None
    model_config: Incomplete
