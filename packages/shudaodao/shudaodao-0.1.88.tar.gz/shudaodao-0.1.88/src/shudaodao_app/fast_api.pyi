from .package import load_router as load_router
from fastapi import FastAPI

def create_init_fastapi(lifespan) -> FastAPI:
    """创建并配置FastAPI应用实例"""
