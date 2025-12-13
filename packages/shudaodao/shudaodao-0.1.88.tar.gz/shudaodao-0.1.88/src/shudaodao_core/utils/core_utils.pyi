from functools import cache
from pathlib import Path

class CoreUtil:
    """核心库的工具类"""
    @classmethod
    def remove_node_attr(cls, *, nodes, children_node_name, remove_attrs): ...
    @staticmethod
    def format_datatime(dt_str):
        """
        将 ISO 8601 格式（含T）的时间字符串转换为 'YYYY-MM-DD HH:MM:SS' 格式
        支持：2025-09-22T10:30:00, 2025-09-22T10:30:00Z, 2025-09-22T10:30:00+08:00 等
        """
    @classmethod
    @cache
    def get_root_path(cls) -> Path:
        """递归向上查找项目根目录（包含特定标识文件）
        Returns:
            Path: 项目根目录路径
        """
    @classmethod
    def get_path(cls, path: str | Path) -> Path:
        """获取绝对路径，支持~扩展和相对路径解析
        Args:
            path: 输入路径，可以是字符串或Path对象
        Returns:
            Path: 解析后的绝对路径
        """
    @classmethod
    def get_config_path(cls) -> Path:
        """获取配置目录路径"""
    @classmethod
    def get_web_path(cls) -> Path:
        """获取web目录路径"""
    @classmethod
    def get_admin_path(cls) -> Path:
        """获取admin目录路径"""
    @staticmethod
    def remove_path(file_or_path: str | Path | None) -> None:
        """安全删除文件
        Args:
            file_or_path: 要删除的文件路径
        """
    @staticmethod
    def hide_db_password(connection_string): ...
