"""追踪上下文

提供追踪上下文的传播和管理

v3.10.0 新增 - P2.1 OpenTelemetry分布式追踪
"""

from __future__ import annotations

from typing import Any

from .manager import OTEL_AVAILABLE

if OTEL_AVAILABLE:
    from opentelemetry import context, trace
    from opentelemetry.baggage.propagation import W3CBaggagePropagator
    from opentelemetry.propagate import extract, inject, set_global_textmap
    from opentelemetry.propagators.composite import CompositePropagator
    from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator


class TracingContext:
    """追踪上下文管理

    处理跨进程/服务的追踪上下文传播

    使用示例:
        >>> # 注入追踪上下文到HTTP请求头
        >>> headers = {}
        >>> TracingContext.inject(headers)
        >>> response = requests.get(url, headers=headers)
        >>>
        >>> # 从HTTP请求头提取追踪上下文
        >>> ctx = TracingContext.extract(request.headers)
        >>> with TracingContext.use(ctx):
        ...     # 在提取的上下文中创建span
        ...     with tracing.start_span("handle_request"):
        ...         process_request()
    """

    _propagator_initialized = False

    @classmethod
    def init_propagator(cls) -> None:
        """初始化全局传播器

        配置 W3C TraceContext 和 Baggage 传播器
        """
        if not OTEL_AVAILABLE:
            return

        if cls._propagator_initialized:
            return

        # 使用复合传播器支持多种格式
        propagator = CompositePropagator(
            [
                TraceContextTextMapPropagator(),
                W3CBaggagePropagator(),
            ]
        )
        set_global_textmap(propagator)
        cls._propagator_initialized = True

    @classmethod
    def inject(cls, carrier: dict[str, str]) -> dict[str, str]:
        """注入追踪上下文到载体

        将当前追踪上下文注入到字典中（通常是HTTP请求头）

        Args:
            carrier: 载体字典，追踪信息将被注入到此字典

        Returns:
            注入后的载体字典

        示例:
            >>> headers = {}
            >>> TracingContext.inject(headers)
            >>> print(headers)
            >>> # {'traceparent': '00-xxx-xxx-01', 'tracestate': '...'}
        """
        if not OTEL_AVAILABLE:
            return carrier

        cls.init_propagator()
        inject(carrier)
        return carrier

    @classmethod
    def extract(cls, carrier: dict[str, str]) -> Any:
        """从载体提取追踪上下文

        从字典中提取追踪上下文（通常是HTTP请求头）

        Args:
            carrier: 包含追踪信息的载体字典

        Returns:
            提取的上下文对象

        示例:
            >>> ctx = TracingContext.extract(request.headers)
            >>> with TracingContext.use(ctx):
            ...     with tracing.start_span("handle"):
            ...         ...
        """
        if not OTEL_AVAILABLE:
            return None

        cls.init_propagator()
        return extract(carrier)

    @classmethod
    def use(cls, ctx: Any):
        """使用指定的追踪上下文

        返回一个上下文管理器，在其作用域内使用指定的追踪上下文

        Args:
            ctx: 追踪上下文对象

        Returns:
            上下文管理器

        示例:
            >>> ctx = TracingContext.extract(headers)
            >>> with TracingContext.use(ctx):
            ...     # 在提取的上下文中操作
            ...     pass
        """
        if not OTEL_AVAILABLE or ctx is None:
            from contextlib import nullcontext

            return nullcontext()

        return context.attach(ctx)

    @classmethod
    def get_trace_id(cls) -> str | None:
        """获取当前追踪ID

        Returns:
            十六进制格式的追踪ID，如果没有活动追踪则返回None

        示例:
            >>> trace_id = TracingContext.get_trace_id()
            >>> print(trace_id)  # "a1b2c3d4e5f6..."
        """
        if not OTEL_AVAILABLE:
            return None

        span = trace.get_current_span()
        if span and span.is_recording():
            return format(span.get_span_context().trace_id, "032x")

        return None

    @classmethod
    def get_span_id(cls) -> str | None:
        """获取当前span ID

        Returns:
            十六进制格式的span ID，如果没有活动span则返回None
        """
        if not OTEL_AVAILABLE:
            return None

        span = trace.get_current_span()
        if span and span.is_recording():
            return format(span.get_span_context().span_id, "016x")

        return None

    @classmethod
    def get_trace_parent(cls) -> str | None:
        """获取W3C traceparent格式的追踪信息

        Returns:
            traceparent字符串，格式: 00-{trace_id}-{span_id}-{flags}

        示例:
            >>> traceparent = TracingContext.get_trace_parent()
            >>> print(traceparent)
            >>> # "00-a1b2c3d4...-e5f6g7h8...-01"
        """
        if not OTEL_AVAILABLE:
            return None

        span = trace.get_current_span()
        if span and span.is_recording():
            ctx = span.get_span_context()
            trace_id = format(ctx.trace_id, "032x")
            span_id = format(ctx.span_id, "016x")
            flags = "01" if ctx.trace_flags.sampled else "00"
            return f"00-{trace_id}-{span_id}-{flags}"

        return None

    @classmethod
    def is_sampled(cls) -> bool:
        """检查当前追踪是否被采样

        Returns:
            是否被采样
        """
        if not OTEL_AVAILABLE:
            return False

        span = trace.get_current_span()
        if span and span.is_recording():
            return span.get_span_context().trace_flags.sampled

        return False


class Baggage:
    """追踪行李（Baggage）管理

    Baggage用于在分布式追踪中传递自定义键值对数据

    使用示例:
        >>> # 设置baggage
        >>> Baggage.set("user_id", "12345")
        >>> Baggage.set("tenant", "acme")
        >>>
        >>> # 获取baggage
        >>> user_id = Baggage.get("user_id")
        >>>
        >>> # Baggage会自动随追踪上下文传播
    """

    @classmethod
    def set(cls, key: str, value: str) -> None:
        """设置baggage值

        Args:
            key: 键名
            value: 值（必须是字符串）
        """
        if not OTEL_AVAILABLE:
            return

        from opentelemetry import baggage

        ctx = baggage.set_baggage(key, value)
        context.attach(ctx)

    @classmethod
    def get(cls, key: str) -> str | None:
        """获取baggage值

        Args:
            key: 键名

        Returns:
            值，如果不存在则返回None
        """
        if not OTEL_AVAILABLE:
            return None

        from opentelemetry import baggage

        return baggage.get_baggage(key)

    @classmethod
    def get_all(cls) -> dict[str, str]:
        """获取所有baggage

        Returns:
            所有baggage的字典
        """
        if not OTEL_AVAILABLE:
            return {}

        from opentelemetry import baggage

        return dict(baggage.get_all())

    @classmethod
    def remove(cls, key: str) -> None:
        """移除baggage

        Args:
            key: 要移除的键名
        """
        if not OTEL_AVAILABLE:
            return

        from opentelemetry import baggage

        ctx = baggage.remove_baggage(key)
        context.attach(ctx)

    @classmethod
    def clear(cls) -> None:
        """清除所有baggage"""
        if not OTEL_AVAILABLE:
            return

        from opentelemetry import baggage

        ctx = baggage.clear()
        context.attach(ctx)


__all__ = [
    "TracingContext",
    "Baggage",
]
