"""Pytest插件模块

提供 pytest 插件扩展（依赖 pytest）：
- EnvironmentMarker: 环境标记插件
- DebugPlugin: 调试插件，测试失败时收集环境信息
- 环境装饰器: dev_only, prod_only, skip_if_dev, skip_if_prod

架构说明：
- fixtures/ - pytest fixture 定义
- plugins/ - pytest hooks/markers（本模块）
- reporting/allure/ - Allure 观察者、工具类（不依赖 pytest）
- debugging/ - 调试器实现（不依赖 pytest）
"""

from .debug import DebugPlugin
from .markers import (
    EnvironmentMarker,
    dev_only,
    get_env,
    is_env,
    prod_only,
    skip_if_dev,
    skip_if_prod,
)

__all__ = [
    # 环境标记插件
    "EnvironmentMarker",
    "get_env",
    "is_env",
    "skip_if_prod",
    "skip_if_dev",
    "dev_only",
    "prod_only",
    # 调试插件
    "DebugPlugin",
]
