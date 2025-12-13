from ..exception.service_exception import ValidError as ValidError
from ..logger.logging_ import logging as logging
from typing import Any, Callable

class ClassScanner:
    """
    通用类扫描器：递归扫描包，找出满足条件的类
    """
    @staticmethod
    def find_class_in_package(package_name: str, class_name: str) -> type | None:
        """
        在指定包（含子模块/子包）中查找名为 class_name 的类。

        :param package_name: 包名，如 'mypackage'
        :param class_name: 要查找的类名，如 'MyClass'
        :return: 找到的第一个匹配类，否则 None
        """
    @classmethod
    def find_class_with_suffix(
        cls, original_class: type[Any], suffix: str = "Response"
    ) -> type[Any]: ...
    @staticmethod
    def import_class(module_or_full_name: str, class_name: str = None) -> type[Any]:
        """
        从字符串路径导入类，例如：
        'mypackage.utils.helpers.MyClass'
        """
    @classmethod
    def find_classes(
        cls,
        package_name: str,
        base_class: type = ...,
        predicate: Callable[[type], bool] | None = None,
    ) -> dict[str, type]:
        """
        扫描指定包，找出所有继承自 base_class 且满足 predicate 条件的类
        :param package_name: 要扫描的包名（如 "myapp.models"）
        :param base_class: 基类（默认 object，即所有类）
        :param predicate: 额外筛选条件（函数，接收类对象，返回 bool）
        :return: {完整类名: 类对象} 的字典
        """
    @classmethod
    def find_classes_instances(
        cls,
        package_name: str,
        base_class: type = ...,
        predicate: Callable[[Any], bool] | None = None,
    ) -> dict[str, Any]:
        """
        扫描包中所有模块，找出所有类型的实例对象
        可选 predicate 用于进一步筛选实例（如根据 .prefix 属性）
        返回: {变量名（完整路径）: 实例对象}
        """
