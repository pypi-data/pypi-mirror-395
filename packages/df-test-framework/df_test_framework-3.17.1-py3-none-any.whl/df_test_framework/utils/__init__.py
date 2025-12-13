"""工具模块"""

from .assertion import AssertHelper
from .common import load_excel, load_json, random_email, random_phone, random_string
from .data_generator import DataGenerator
from .decorator import (
    cache_result,
    deprecated,
    log_execution,
    retry_on_failure,
)
from .performance import PerformanceCollector, PerformanceTimer, track_performance
from .resilience import CircuitBreaker, CircuitOpenError, CircuitState, circuit_breaker

__all__ = [
    # 数据生成
    "DataGenerator",
    # 断言助手
    "AssertHelper",
    # 通用工具
    "random_string",
    "random_email",
    "random_phone",
    "load_json",
    "load_excel",
    # 性能监控
    "track_performance",
    "PerformanceTimer",
    "PerformanceCollector",
    # 装饰器
    "retry_on_failure",
    "log_execution",
    "deprecated",
    "cache_result",
    # 弹性工具
    "CircuitBreaker",
    "CircuitOpenError",
    "CircuitState",
    "circuit_breaker",
]
