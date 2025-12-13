"""
报告插件

提供 Allure 等报告集成。

v3.14.0: 从 extensions/builtin/reporting/ 迁移。
"""

from df_test_framework.plugins.builtin.reporting.allure_plugin import AllurePlugin

__all__ = ["AllurePlugin"]
