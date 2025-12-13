"""
监控插件

提供性能监控、指标采集等功能。

v3.14.0: 从 extensions/builtin/monitoring/ 迁移。
"""

from df_test_framework.plugins.builtin.monitoring.plugin import MonitoringPlugin

__all__ = ["MonitoringPlugin"]
