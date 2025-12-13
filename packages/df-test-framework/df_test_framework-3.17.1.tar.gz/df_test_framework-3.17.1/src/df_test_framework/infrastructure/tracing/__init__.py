"""分布式追踪模块

基于 OpenTelemetry 提供分布式链路追踪能力

核心组件:
- TracingManager: 追踪管理器，负责初始化和配置
- TracingDecorator: 追踪装饰器，简化span创建
- TracingContext: 追踪上下文，传递trace信息

拦截器组件（位于 interceptors 子模块）:
- TracingInterceptor: HTTP请求追踪拦截器
- SpanContextCarrier: Span上下文载体

集成组件（位于 integrations 子模块）:
- DatabaseTracer: 数据库查询追踪器
- TracedDatabase: 带追踪的数据库包装器
- instrument_sqlalchemy: SQLAlchemy自动仪表化

支持的导出器:
- Console: 控制台输出（开发调试）
- Jaeger: Jaeger后端
- OTLP: OpenTelemetry Protocol（推荐）
- Zipkin: Zipkin后端

使用示例:
    >>> from df_test_framework.infrastructure.tracing import (
    ...     TracingManager, trace_span, TracingInterceptor
    ... )
    >>>
    >>> # 初始化追踪
    >>> tracing = TracingManager(service_name="my-test-service")
    >>> tracing.init()
    >>>
    >>> # 使用装饰器
    >>> @trace_span("my_operation")
    >>> def my_function():
    ...     pass
    >>>
    >>> # 手动创建span
    >>> with tracing.start_span("custom_operation") as span:
    ...     span.set_attribute("key", "value")
    ...     # 业务逻辑
    >>>
    >>> # HTTP请求追踪
    >>> client.interceptor_chain.add(TracingInterceptor())
    >>>
    >>> # 数据库追踪
    >>> from df_test_framework.infrastructure.tracing.integrations import TracedDatabase
    >>> traced_db = TracedDatabase(db)

v3.10.0 新增 - P2.1 OpenTelemetry分布式追踪
"""

from .context import Baggage, TracingContext
from .decorators import TraceClass, trace_async_span, trace_span
from .exporters import ExporterType
from .interceptors import SpanContextCarrier, TracingInterceptor
from .manager import (
    OTEL_AVAILABLE,
    TracingConfig,
    TracingManager,
    get_tracing_manager,
    set_tracing_manager,
)

__all__ = [
    # 核心
    "TracingManager",
    "TracingConfig",
    "get_tracing_manager",
    "set_tracing_manager",
    "OTEL_AVAILABLE",
    # 上下文
    "TracingContext",
    "Baggage",
    # 装饰器
    "trace_span",
    "trace_async_span",
    "TraceClass",
    # 导出器
    "ExporterType",
    # 拦截器
    "TracingInterceptor",
    "SpanContextCarrier",
]
