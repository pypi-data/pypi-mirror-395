"""FastAPI Vite Integration - Seamless Vite asset management for FastAPI applications."""

from importlib.metadata import version

from .config import ViteConfig
from .integration import setup_vite
from .logger import logger

__version__ = version("fastapi-vite-assets")
__all__ = ["ViteConfig", "setup_vite", "logger"]
