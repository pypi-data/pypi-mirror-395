"""
KSfaceAPI - A simple Face++ API wrapper

This package provides a simple interface for Face++ face recognition API.
"""

from .core import KSface

__version__ = "1.1.0"
__author__ = "KSfaceAPI Team"
__all__ = ["KSface"]

# 简短的包描述
__description__ = "A simple Python SDK for Face++ face recognition API"

# 当用户直接导入包时显示友好信息
print(f"KSfaceAPI {__version__} - {__description__}")
print("Usage: from KSfaceAPI import KSface")