"""追踪管理器

TracingManager 是分布式追踪的核心管理类

核心功能:
- 初始化 OpenTelemetry 追踪器
- 管理 TracerProvider 和 SpanProcessor
- 提供便捷的 span 创建接口
- 支持多种导出器配置

v3.10.0 新增 - P2.1 OpenTelemetry分布式追踪
"""

from __future__ import annotations

import threading
from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any

from .exporters import ExporterType, create_exporter

# 检查 OpenTelemetry 是否可用
try:
    from opentelemetry import trace
    from opentelemetry.sdk.resources import SERVICE_NAME, Resource
    from opentelemetry.sdk.trace import Span, TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, SimpleSpanProcessor

    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False
    trace = None  # type: ignore
    TracerProvider = None  # type: ignore
    Span = None  # type: ignore


@dataclass
class TracingConfig:
    """追踪配置

    Attributes:
        service_name: 服务名称，用于标识追踪来源
        exporter_type: 导出器类型
        endpoint: 导出端点URL（用于OTLP/Jaeger/Zipkin）
        batch_export: 是否使用批量导出（生产环境推荐True）
        sample_rate: 采样率 (0.0-1.0)，1.0表示全采样
        enabled: 是否启用追踪
        extra_attributes: 额外的资源属性
    """

    service_name: str = "df-test-framework"
    exporter_type: ExporterType = ExporterType.CONSOLE
    endpoint: str | None = None
    batch_export: bool = True
    sample_rate: float = 1.0
    enabled: bool = True
    extra_attributes: dict[str, str] = field(default_factory=dict)


class TracingManager:
    """追踪管理器

    管理 OpenTelemetry 追踪的生命周期和配置

    使用示例:
        >>> # 基础用法
        >>> tracing = TracingManager(service_name="my-service")
        >>> tracing.init()
        >>>
        >>> # 创建span
        >>> with tracing.start_span("operation") as span:
        ...     span.set_attribute("key", "value")
        ...     # 业务逻辑
        >>>
        >>> # 使用配置
        >>> config = TracingConfig(
        ...     service_name="my-service",
        ...     exporter_type=ExporterType.JAEGER,
        ...     endpoint="localhost:6831"
        ... )
        >>> tracing = TracingManager(config=config)
        >>> tracing.init()
        >>>
        >>> # 关闭追踪
        >>> tracing.shutdown()
    """

    def __init__(self, service_name: str | None = None, config: TracingConfig | None = None):
        """初始化追踪管理器

        Args:
            service_name: 服务名称（简化配置）
            config: 完整配置对象（优先级高于service_name）
        """
        if config:
            self.config = config
        else:
            self.config = TracingConfig(service_name=service_name or "df-test-framework")

        self._provider: TracerProvider | None = None
        self._tracer = None
        self._initialized = False

    def init(self) -> TracingManager:
        """初始化追踪器

        配置 TracerProvider、导出器和处理器

        Returns:
            self，支持链式调用

        Raises:
            ImportError: 未安装 opentelemetry-sdk
            RuntimeError: 重复初始化
        """
        if not OTEL_AVAILABLE:
            raise ImportError(
                "OpenTelemetry追踪需要安装: pip install opentelemetry-sdk opentelemetry-api"
            )

        if self._initialized:
            return self

        if not self.config.enabled:
            # 追踪禁用时，设置NoOp追踪器
            self._tracer = trace.get_tracer(self.config.service_name)
            self._initialized = True
            return self

        # 创建资源
        resource_attributes = {
            SERVICE_NAME: self.config.service_name,
            **self.config.extra_attributes,
        }
        resource = Resource.create(resource_attributes)

        # 创建 TracerProvider
        self._provider = TracerProvider(resource=resource)

        # 创建导出器
        exporter = create_exporter(self.config.exporter_type, endpoint=self.config.endpoint)

        # 创建处理器
        if self.config.batch_export:
            processor = BatchSpanProcessor(exporter)
        else:
            processor = SimpleSpanProcessor(exporter)

        self._provider.add_span_processor(processor)

        # 设置全局 TracerProvider
        trace.set_tracer_provider(self._provider)

        # 获取追踪器
        self._tracer = trace.get_tracer(
            self.config.service_name, schema_url="https://opentelemetry.io/schemas/1.11.0"
        )

        self._initialized = True
        return self

    def shutdown(self) -> None:
        """关闭追踪器

        刷新并关闭所有span处理器
        """
        if self._provider:
            self._provider.shutdown()
            self._provider = None

        self._initialized = False

    @property
    def tracer(self):
        """获取追踪器实例

        Returns:
            OpenTelemetry Tracer实例

        Raises:
            RuntimeError: 未初始化
        """
        if not self._initialized:
            # 自动初始化
            self.init()

        return self._tracer

    @contextmanager
    def start_span(
        self, name: str, attributes: dict[str, Any] | None = None, kind: Any = None
    ) -> Generator[Any, None, None]:
        """创建并启动一个span

        Args:
            name: span名称
            attributes: span属性
            kind: span类型（CLIENT/SERVER/PRODUCER/CONSUMER/INTERNAL）

        Yields:
            Span对象

        示例:
            >>> with tracing.start_span("http_request") as span:
            ...     span.set_attribute("http.method", "GET")
            ...     span.set_attribute("http.url", "/api/users")
            ...     response = make_request()
            ...     span.set_attribute("http.status_code", response.status_code)
        """
        if not self._initialized:
            self.init()

        # 确定span类型
        if kind is None and OTEL_AVAILABLE:
            kind = trace.SpanKind.INTERNAL

        with self.tracer.start_as_current_span(name, kind=kind, attributes=attributes) as span:
            yield span

    def start_span_no_context(self, name: str, attributes: dict[str, Any] | None = None):
        """创建span但不设置为当前span

        用于需要手动管理span生命周期的场景

        Args:
            name: span名称
            attributes: span属性

        Returns:
            Span对象
        """
        if not self._initialized:
            self.init()

        return self.tracer.start_span(name, attributes=attributes)

    def get_current_span(self):
        """获取当前活动的span

        Returns:
            当前Span对象，如果没有则返回无效span
        """
        if not OTEL_AVAILABLE:
            return None

        return trace.get_current_span()

    def add_event(self, name: str, attributes: dict[str, Any] | None = None) -> None:
        """向当前span添加事件

        Args:
            name: 事件名称
            attributes: 事件属性

        示例:
            >>> tracing.add_event("cache_miss", {"key": "user:123"})
        """
        span = self.get_current_span()
        if span:
            span.add_event(name, attributes=attributes)

    def set_attribute(self, key: str, value: Any) -> None:
        """设置当前span的属性

        Args:
            key: 属性键
            value: 属性值
        """
        span = self.get_current_span()
        if span:
            span.set_attribute(key, value)

    def record_exception(self, exception: Exception) -> None:
        """记录异常到当前span

        Args:
            exception: 异常对象
        """
        span = self.get_current_span()
        if span:
            span.record_exception(exception)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(exception)))

    @property
    def is_enabled(self) -> bool:
        """追踪是否启用"""
        return self.config.enabled and self._initialized

    @property
    def is_initialized(self) -> bool:
        """是否已初始化"""
        return self._initialized


# 全局默认追踪管理器（线程安全）
_default_manager: TracingManager | None = None
_manager_lock = threading.Lock()


def get_tracing_manager() -> TracingManager:
    """获取全局追踪管理器（线程安全）

    使用双重检查锁定模式确保线程安全的单例创建。

    Returns:
        TracingManager实例
    """
    global _default_manager
    if _default_manager is None:
        with _manager_lock:
            # 双重检查：获取锁后再次检查
            if _default_manager is None:
                _default_manager = TracingManager()
    return _default_manager


def set_tracing_manager(manager: TracingManager) -> None:
    """设置全局追踪管理器（线程安全）

    Args:
        manager: TracingManager实例
    """
    global _default_manager
    with _manager_lock:
        _default_manager = manager


__all__ = [
    "TracingManager",
    "TracingConfig",
    "get_tracing_manager",
    "set_tracing_manager",
    "OTEL_AVAILABLE",
]
