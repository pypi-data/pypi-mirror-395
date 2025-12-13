"""监控指标模块

基于 Prometheus 提供监控指标收集能力

核心组件:
- MetricsManager: 指标管理器，负责初始化和配置
- MetricsRegistry: 指标注册表，管理所有指标
- 内置指标: HTTP请求、数据库查询、自定义业务指标

支持的指标类型:
- Counter: 计数器（只增不减）
- Gauge: 仪表盘（可增可减）
- Histogram: 直方图（分布统计）
- Summary: 摘要（百分位统计）

使用示例:
    >>> from df_test_framework.infrastructure.metrics import MetricsManager, Counter
    >>>
    >>> # 初始化指标管理器
    >>> metrics = MetricsManager(service_name="my-service")
    >>> metrics.init()
    >>>
    >>> # 创建计数器
    >>> requests_total = metrics.counter(
    ...     "http_requests_total",
    ...     "Total HTTP requests",
    ...     labels=["method", "endpoint", "status"]
    ... )
    >>>
    >>> # 记录指标
    >>> requests_total.labels(method="GET", endpoint="/api/users", status="200").inc()
    >>>
    >>> # 启动指标服务器
    >>> metrics.start_server(port=8000)

v3.10.0 新增 - P2.3 Prometheus监控
"""

from .decorators import (
    count_calls,
    time_calls,
    track_in_progress,
)
from .manager import PROMETHEUS_AVAILABLE, MetricsConfig, MetricsManager
from .registry import MetricsRegistry
from .types import (
    Counter,
    Gauge,
    Histogram,
    MetricWrapper,
    Summary,
)

__all__ = [
    # 核心
    "MetricsManager",
    "MetricsConfig",
    "MetricsRegistry",
    "PROMETHEUS_AVAILABLE",
    # 指标类型
    "Counter",
    "Gauge",
    "Histogram",
    "Summary",
    "MetricWrapper",
    # 装饰器
    "count_calls",
    "time_calls",
    "track_in_progress",
]
