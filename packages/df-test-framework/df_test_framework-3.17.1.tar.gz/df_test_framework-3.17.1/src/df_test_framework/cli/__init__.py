"""Command line utilities for df-test-framework.

提供项目脚手架生成功能，快速创建标准化的测试项目结构。
"""

from .commands import (
    generate_api_client,
    generate_builder,
    generate_repository,
    generate_test,
    init_project,
)
from .main import main

__all__ = [
    "main",
    "init_project",
    "generate_test",
    "generate_builder",
    "generate_repository",
    "generate_api_client",
]
