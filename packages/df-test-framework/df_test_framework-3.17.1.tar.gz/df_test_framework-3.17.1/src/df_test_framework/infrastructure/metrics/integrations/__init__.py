"""指标集成模块

提供与各种组件的指标收集集成

v3.10.0 新增 - P2.3 Prometheus监控
"""

from .database import (
    DatabaseMetrics,
    MetricsTracedDatabase,
)
from .http import (
    HttpMetrics,
    MetricsInterceptor,
)

__all__ = [
    # HTTP 指标
    "MetricsInterceptor",
    "HttpMetrics",
    # 数据库指标
    "DatabaseMetrics",
    "MetricsTracedDatabase",
]
