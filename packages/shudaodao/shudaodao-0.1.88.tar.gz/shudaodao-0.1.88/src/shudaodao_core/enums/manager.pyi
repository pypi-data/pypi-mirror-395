from .clazz_int import EnumInt as EnumInt
from .clazz_str import EnumStr as EnumStr
from typing import Any

class EnumManager:
    def __new__(cls):
        """线程安全的单例构造器"""
    def get_field_names(self, model_class): ...
    def register(self, schema_name: str, enum_dict: dict[str, Any]):
        """注册枚举值"""
    def is_enum_field(self, schema_name: str, field_name) -> bool: ...
    def resolve_value(self, model_class, field_name: str, value) -> dict[str, Any]:
        """获取枚举值"""
    def clear(self) -> None: ...
    def __del__(self) -> None: ...
