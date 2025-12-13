"""指标装饰器

提供便捷的函数/方法指标收集装饰器

v3.10.0 新增 - P2.3 Prometheus监控
"""

from __future__ import annotations

import functools
import time
from collections.abc import Callable
from typing import Any, TypeVar

from .manager import get_metrics_manager

F = TypeVar("F", bound=Callable[..., Any])


def count_calls(
    counter_name: str,
    description: str = "Function call count",
    labels: list[str] | None = None,
    label_values: dict[str, str] | None = None,
) -> Callable[[F], F]:
    """函数调用计数装饰器

    每次函数调用时增加计数器

    Args:
        counter_name: 计数器名称
        description: 计数器描述
        labels: 标签名列表
        label_values: 标签值字典

    Returns:
        装饰器函数

    示例:
        >>> @count_calls("api_calls_total", labels=["endpoint"])
        >>> def get_users():
        ...     return []
        >>>
        >>> @count_calls("db_queries_total", label_values={"operation": "select"})
        >>> def query_users():
        ...     return db.query("SELECT * FROM users")
    """

    def decorator(func: F) -> F:
        counter = None  # 延迟初始化

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            nonlocal counter

            if counter is None:
                manager = get_metrics_manager()
                if not manager.is_initialized:
                    manager.init()
                counter = manager.counter(counter_name, description, labels or [])

            # 增加计数
            if label_values:
                counter.labels(**label_values).inc()
            else:
                counter.inc()

            return func(*args, **kwargs)

        return wrapper  # type: ignore

    return decorator


def time_calls(
    histogram_name: str,
    description: str = "Function call duration",
    labels: list[str] | None = None,
    label_values: dict[str, str] | None = None,
    buckets: tuple[float, ...] | None = None,
) -> Callable[[F], F]:
    """函数调用计时装饰器

    记录函数执行时间到直方图

    Args:
        histogram_name: 直方图名称
        description: 直方图描述
        labels: 标签名列表
        label_values: 标签值字典
        buckets: 桶边界

    Returns:
        装饰器函数

    示例:
        >>> @time_calls("request_duration_seconds")
        >>> def process_request():
        ...     time.sleep(0.1)
        >>>
        >>> @time_calls("db_query_duration_seconds", label_values={"table": "users"})
        >>> def query_users():
        ...     return db.query("SELECT * FROM users")
    """

    def decorator(func: F) -> F:
        histogram = None

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            nonlocal histogram

            if histogram is None:
                manager = get_metrics_manager()
                if not manager.is_initialized:
                    manager.init()
                histogram = manager.histogram(histogram_name, description, labels or [], buckets)

            # 获取带标签的直方图
            h = histogram.labels(**label_values) if label_values else histogram

            # 计时
            start = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                duration = time.perf_counter() - start
                h.observe(duration)

        return wrapper  # type: ignore

    return decorator


def time_async_calls(
    histogram_name: str,
    description: str = "Async function call duration",
    labels: list[str] | None = None,
    label_values: dict[str, str] | None = None,
    buckets: tuple[float, ...] | None = None,
) -> Callable[[F], F]:
    """异步函数调用计时装饰器

    记录异步函数执行时间到直方图

    Args:
        histogram_name: 直方图名称
        description: 直方图描述
        labels: 标签名列表
        label_values: 标签值字典
        buckets: 桶边界

    Returns:
        装饰器函数

    示例:
        >>> @time_async_calls("async_request_duration_seconds")
        >>> async def fetch_data():
        ...     await asyncio.sleep(0.1)
        ...     return {}
    """

    def decorator(func: F) -> F:
        histogram = None

        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            nonlocal histogram

            if histogram is None:
                manager = get_metrics_manager()
                if not manager.is_initialized:
                    manager.init()
                histogram = manager.histogram(histogram_name, description, labels or [], buckets)

            h = histogram.labels(**label_values) if label_values else histogram

            start = time.perf_counter()
            try:
                return await func(*args, **kwargs)
            finally:
                duration = time.perf_counter() - start
                h.observe(duration)

        return wrapper  # type: ignore

    return decorator


def track_in_progress(
    gauge_name: str,
    description: str = "In-progress operations",
    labels: list[str] | None = None,
    label_values: dict[str, str] | None = None,
) -> Callable[[F], F]:
    """进行中操作追踪装饰器

    追踪当前进行中的操作数量

    Args:
        gauge_name: 仪表盘名称
        description: 仪表盘描述
        labels: 标签名列表
        label_values: 标签值字典

    Returns:
        装饰器函数

    示例:
        >>> @track_in_progress("active_requests")
        >>> def handle_request():
        ...     time.sleep(1)
        >>>
        >>> # 可同时追踪多个并发请求
    """

    def decorator(func: F) -> F:
        gauge = None

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            nonlocal gauge

            if gauge is None:
                manager = get_metrics_manager()
                if not manager.is_initialized:
                    manager.init()
                gauge = manager.gauge(gauge_name, description, labels or [])

            g = gauge.labels(**label_values) if label_values else gauge

            g.inc()
            try:
                return func(*args, **kwargs)
            finally:
                g.dec()

        return wrapper  # type: ignore

    return decorator


def track_async_in_progress(
    gauge_name: str,
    description: str = "In-progress async operations",
    labels: list[str] | None = None,
    label_values: dict[str, str] | None = None,
) -> Callable[[F], F]:
    """异步进行中操作追踪装饰器

    追踪当前进行中的异步操作数量

    Args:
        gauge_name: 仪表盘名称
        description: 仪表盘描述
        labels: 标签名列表
        label_values: 标签值字典

    Returns:
        装饰器函数
    """

    def decorator(func: F) -> F:
        gauge = None

        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            nonlocal gauge

            if gauge is None:
                manager = get_metrics_manager()
                if not manager.is_initialized:
                    manager.init()
                gauge = manager.gauge(gauge_name, description, labels or [])

            g = gauge.labels(**label_values) if label_values else gauge

            g.inc()
            try:
                return await func(*args, **kwargs)
            finally:
                g.dec()

        return wrapper  # type: ignore

    return decorator


__all__ = [
    "count_calls",
    "time_calls",
    "time_async_calls",
    "track_in_progress",
    "track_async_in_progress",
]
