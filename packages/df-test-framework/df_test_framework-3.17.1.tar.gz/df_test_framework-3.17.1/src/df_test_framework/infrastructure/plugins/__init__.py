"""
插件系统

基于 Pluggy 的插件管理系统。

组件:
- HookSpecs: Hook 规范定义（单一数据源）
- PluggyPluginManager: 插件管理器实现
- hookimpl: Hook 实现装饰器
"""

from df_test_framework.infrastructure.plugins.hooks import (
    HookSpecs,
    hookimpl,
    hookspec,
)
from df_test_framework.infrastructure.plugins.manager import PluggyPluginManager

__all__ = [
    "HookSpecs",
    "hookspec",
    "hookimpl",
    "PluggyPluginManager",
]
