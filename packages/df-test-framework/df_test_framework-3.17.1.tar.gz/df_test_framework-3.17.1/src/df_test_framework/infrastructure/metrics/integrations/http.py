"""HTTP 请求指标集成

为 HTTP 请求提供 Prometheus 指标收集

v3.10.0 新增 - P2.3 Prometheus监控
"""

from __future__ import annotations

import time

from df_test_framework.capabilities.clients.http.core.interceptor import BaseInterceptor
from df_test_framework.capabilities.clients.http.core.request import Request
from df_test_framework.capabilities.clients.http.core.response import Response

from ..manager import get_metrics_manager
from ..types import Counter, Gauge, Histogram


class HttpMetrics:
    """HTTP 指标收集器

    提供标准的 HTTP 请求指标

    使用示例:
        >>> http_metrics = HttpMetrics()
        >>>
        >>> # 记录请求
        >>> http_metrics.record_request("GET", "/api/users", 200, 0.5)
        >>>
        >>> # 使用拦截器自动收集
        >>> client.interceptor_chain.add(http_metrics.interceptor())

    收集的指标:
        - http_requests_total: 请求总数（按方法、端点、状态码）
        - http_request_duration_seconds: 请求耗时（按方法、端点）
        - http_requests_in_flight: 进行中的请求数
        - http_request_size_bytes: 请求大小
        - http_response_size_bytes: 响应大小
    """

    def __init__(
        self,
        prefix: str = "http",
        include_path_label: bool = True,
        path_cardinality_limit: int = 100,
    ):
        """初始化 HTTP 指标收集器

        Args:
            prefix: 指标名称前缀
            include_path_label: 是否包含路径标签（高基数警告）
            path_cardinality_limit: 路径标签基数限制
        """
        self.prefix = prefix
        self.include_path_label = include_path_label
        self.path_cardinality_limit = path_cardinality_limit

        self._metrics_initialized = False
        self._requests_total: Counter | None = None
        self._request_duration: Histogram | None = None
        self._requests_in_flight: Gauge | None = None
        self._request_size: Histogram | None = None
        self._response_size: Histogram | None = None

        # 路径去重
        self._seen_paths: set[str] = set()

    def _init_metrics(self) -> None:
        """初始化指标"""
        if self._metrics_initialized:
            return

        manager = get_metrics_manager()
        if not manager.is_initialized:
            manager.init()

        # 标签定义
        labels = ["method", "status"]
        if self.include_path_label:
            labels.insert(1, "path")

        # 请求总数
        self._requests_total = manager.counter(
            f"{self.prefix}_requests_total", "Total HTTP requests", labels=labels
        )

        # 请求耗时
        duration_labels = ["method"]
        if self.include_path_label:
            duration_labels.append("path")

        self._request_duration = manager.histogram(
            f"{self.prefix}_request_duration_seconds",
            "HTTP request duration in seconds",
            labels=duration_labels,
            buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10),
        )

        # 进行中请求
        self._requests_in_flight = manager.gauge(
            f"{self.prefix}_requests_in_flight",
            "HTTP requests currently in flight",
            labels=["method"],
        )

        # 请求大小
        self._request_size = manager.histogram(
            f"{self.prefix}_request_size_bytes",
            "HTTP request size in bytes",
            labels=["method"],
            buckets=(100, 1000, 10000, 100000, 1000000),
        )

        # 响应大小
        self._response_size = manager.histogram(
            f"{self.prefix}_response_size_bytes",
            "HTTP response size in bytes",
            labels=["method"],
            buckets=(100, 1000, 10000, 100000, 1000000),
        )

        self._metrics_initialized = True

    def _normalize_path(self, path: str) -> str:
        """标准化路径（减少基数）

        Args:
            path: 原始路径

        Returns:
            标准化后的路径
        """
        # 移除查询参数
        if "?" in path:
            path = path.split("?")[0]

        # 替换数字ID为占位符
        import re

        path = re.sub(r"/\d+", "/{id}", path)
        path = re.sub(r"/[a-f0-9-]{32,}", "/{uuid}", path)

        # 基数限制
        if len(self._seen_paths) >= self.path_cardinality_limit:
            if path not in self._seen_paths:
                return "/other"

        self._seen_paths.add(path)
        return path

    def record_request(
        self,
        method: str,
        path: str,
        status_code: int,
        duration: float,
        request_size: int = 0,
        response_size: int = 0,
    ) -> None:
        """记录请求指标

        Args:
            method: HTTP 方法
            path: 请求路径
            status_code: 响应状态码
            duration: 请求耗时（秒）
            request_size: 请求大小（字节）
            response_size: 响应大小（字节）
        """
        self._init_metrics()

        normalized_path = self._normalize_path(path)
        status = str(status_code)

        # 请求计数
        if self.include_path_label:
            self._requests_total.labels(method=method, path=normalized_path, status=status).inc()
        else:
            self._requests_total.labels(method=method, status=status).inc()

        # 请求耗时
        if self.include_path_label:
            self._request_duration.labels(method=method, path=normalized_path).observe(duration)
        else:
            self._request_duration.labels(method=method).observe(duration)

        # 请求大小
        if request_size > 0:
            self._request_size.labels(method=method).observe(request_size)

        # 响应大小
        if response_size > 0:
            self._response_size.labels(method=method).observe(response_size)

    def start_request(self, method: str) -> None:
        """标记请求开始

        Args:
            method: HTTP 方法
        """
        self._init_metrics()
        self._requests_in_flight.labels(method=method).inc()

    def end_request(self, method: str) -> None:
        """标记请求结束

        Args:
            method: HTTP 方法
        """
        self._init_metrics()
        self._requests_in_flight.labels(method=method).dec()

    def interceptor(self) -> MetricsInterceptor:
        """创建 HTTP 拦截器

        Returns:
            MetricsInterceptor 实例
        """
        return MetricsInterceptor(http_metrics=self)


class MetricsInterceptor(BaseInterceptor):
    """HTTP 指标拦截器

    自动收集 HTTP 请求指标

    使用示例:
        >>> from df_test_framework.infrastructure.metrics.integrations import MetricsInterceptor
        >>>
        >>> interceptor = MetricsInterceptor()
        >>> client.interceptor_chain.add(interceptor)
        >>>
        >>> # 所有请求自动收集指标
        >>> response = await client.get("/api/users")
    """

    def __init__(
        self,
        name: str = "MetricsInterceptor",
        priority: int = 5,  # 高优先级，在追踪之前
        http_metrics: HttpMetrics | None = None,
    ):
        """初始化指标拦截器

        Args:
            name: 拦截器名称
            priority: 优先级
            http_metrics: HTTP 指标收集器
        """
        super().__init__(name=name, priority=priority)
        self.http_metrics = http_metrics or HttpMetrics()
        self._start_time_key = "_metrics_start_time"

    def before_request(self, request: Request) -> Request | None:
        """请求前：记录开始时间

        Args:
            request: 请求对象

        Returns:
            带开始时间的请求对象
        """
        # 标记请求开始
        self.http_metrics.start_request(request.method)

        # 记录开始时间
        start_time = time.perf_counter()
        return request.with_context(self._start_time_key, start_time)

    def after_response(self, response: Response) -> Response | None:
        """响应后：记录指标

        Args:
            response: 响应对象

        Returns:
            None
        """
        # 注意：当前架构中 Response 没有引用 Request
        # 这里使用 context 中存储的方法信息
        # 暂时使用默认值

        # 标记请求结束
        self.http_metrics.end_request("GET")  # TODO: 从上下文获取实际方法

        return None

    def on_error(self, error: Exception, request: Request) -> None:
        """错误处理：记录错误指标

        Args:
            error: 异常对象
            request: 请求对象
        """
        # 计算耗时
        start_time = request.get_context(self._start_time_key)
        duration = 0.0
        if start_time:
            duration = time.perf_counter() - start_time

        # 记录错误请求
        self.http_metrics.record_request(
            method=request.method,
            path=request.path,
            status_code=0,  # 错误状态
            duration=duration,
        )

        # 标记请求结束
        self.http_metrics.end_request(request.method)


__all__ = [
    "HttpMetrics",
    "MetricsInterceptor",
]
