"""CLI命令模块

包含所有df-test命令行工具的命令实现。
"""

from .generate_cmd import (
    generate_api_client,
    generate_builder,
    generate_models_from_json,
    generate_repository,
    generate_settings,
    generate_test,
)
from .init_cmd import init_project
from .interactive import interactive_generate

# 导入 OpenAPI 生成功能（延迟导入，避免依赖问题）
try:
    from ..generators.openapi_generator import generate_from_openapi

    OPENAPI_GENERATOR_AVAILABLE = True
except ImportError:
    OPENAPI_GENERATOR_AVAILABLE = False
    generate_from_openapi = None

__all__ = [
    "init_project",
    "generate_test",
    "generate_builder",
    "generate_repository",
    "generate_api_client",
    "generate_models_from_json",
    "generate_settings",
    "interactive_generate",
    "generate_from_openapi",
    "OPENAPI_GENERATOR_AVAILABLE",
]
