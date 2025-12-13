from ..logger.logging_ import logging as logging

class DatabaseChecker:
    @staticmethod
    async def metadata_to_database(source_metadata, engine_name):
        """安全创建表，手动检查是否存在"""
