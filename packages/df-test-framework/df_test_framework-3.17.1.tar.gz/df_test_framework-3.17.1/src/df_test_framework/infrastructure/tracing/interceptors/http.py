"""HTTP追踪拦截器

为HTTP请求添加分布式追踪支持

v3.10.0 新增 - P2.1 OpenTelemetry分布式追踪
"""

from __future__ import annotations

import time
from typing import Any

from df_test_framework.capabilities.clients.http.core import Request, Response
from df_test_framework.core.middleware import BaseMiddleware

from ..context import TracingContext
from ..manager import OTEL_AVAILABLE, get_tracing_manager

if OTEL_AVAILABLE:
    from opentelemetry import trace


class TracingInterceptor(BaseMiddleware[Request, Response]):
    """HTTP追踪拦截器

    自动为HTTP请求创建追踪span，记录:
    - HTTP方法和URL
    - 请求/响应头（可选）
    - 状态码
    - 响应时间
    - 异常信息

    使用示例:
        >>> from df_test_framework.capabilities.clients.http.interceptors import TracingInterceptor
        >>>
        >>> # 基础用法
        >>> interceptor = TracingInterceptor()
        >>> client.interceptor_chain.add(interceptor)
        >>>
        >>> # 自定义配置
        >>> interceptor = TracingInterceptor(
        ...     record_headers=True,
        ...     record_body=False,
        ...     propagate_context=True
        ... )

    追踪属性:
        - http.method: HTTP方法
        - http.url: 请求URL
        - http.status_code: 响应状态码
        - http.response_content_length: 响应体长度
        - http.request.duration_ms: 请求耗时（毫秒）
    """

    def __init__(
        self,
        name: str = "TracingInterceptor",
        priority: int = 10,  # 高优先级，最先执行
        record_headers: bool = False,
        record_body: bool = False,
        propagate_context: bool = True,
        sensitive_headers: list[str] | None = None,
    ):
        """初始化追踪拦截器

        Args:
            name: 拦截器名称
            priority: 优先级（数字越小越先执行）
            record_headers: 是否记录请求/响应头
            record_body: 是否记录请求/响应体
            propagate_context: 是否传播追踪上下文（注入traceparent头）
            sensitive_headers: 敏感头列表，记录时会脱敏
        """
        super().__init__(name=name, priority=priority)
        self.record_headers = record_headers
        self.record_body = record_body
        self.propagate_context = propagate_context
        self.sensitive_headers = sensitive_headers or [
            "authorization",
            "x-api-key",
            "x-auth-token",
            "cookie",
            "set-cookie",
        ]
        self._span_key = "_tracing_span"
        self._start_time_key = "_tracing_start_time"

    async def __call__(self, request: Request, call_next) -> Response:
        """中间件调用：在请求前后添加追踪

        Args:
            request: 请求对象
            call_next: 调用下一个中间件的函数

        Returns:
            响应对象
        """
        if not OTEL_AVAILABLE:
            return await call_next(request)

        manager = get_tracing_manager()

        # 创建span
        span_name = f"HTTP {request.method} {request.path}"
        span = manager.start_span_no_context(
            span_name, attributes=self._build_request_attributes(request)
        )

        # 记录开始时间
        start_time = time.perf_counter()

        # 传播追踪上下文
        if self.propagate_context:
            headers = dict(request.headers)
            TracingContext.inject(headers)
            request = request.with_headers(headers)

        try:
            # 调用下一个中间件
            response = await call_next(request)

            # 记录响应信息
            if span and span.is_recording():
                span.set_attribute("http.status_code", response.status_code)

                if response.body:
                    span.set_attribute("http.response_content_length", len(response.body))

                # 记录响应头
                if self.record_headers and response.headers:
                    for key, value in response.headers.items():
                        if key.lower() in self.sensitive_headers:
                            span.set_attribute(f"http.response.header.{key}", "***")
                        else:
                            span.set_attribute(f"http.response.header.{key}", value)

                # 计算耗时
                duration_ms = (time.perf_counter() - start_time) * 1000
                span.set_attribute("http.request.duration_ms", duration_ms)

                # 设置状态
                if response.status_code >= 400:
                    span.set_status(
                        trace.Status(trace.StatusCode.ERROR, f"HTTP {response.status_code}")
                    )

                span.end()

            return response

        except Exception as error:
            # 错误处理：记录异常
            if span and span.is_recording():
                # 计算耗时
                duration_ms = (time.perf_counter() - start_time) * 1000
                span.set_attribute("http.request.duration_ms", duration_ms)

                # 记录异常
                span.record_exception(error)
                span.set_status(trace.Status(trace.StatusCode.ERROR, str(error)))
                span.end()

            raise

    def _build_request_attributes(self, request: Request) -> dict[str, Any]:
        """构建请求属性

        Args:
            request: 请求对象

        Returns:
            属性字典
        """
        attrs: dict[str, Any] = {
            "http.method": request.method,
            "http.url": request.url,
            "http.target": request.path,
        }

        # 记录请求头
        if self.record_headers and request.headers:
            for key, value in request.headers.items():
                if key.lower() in self.sensitive_headers:
                    attrs[f"http.request.header.{key}"] = "***"
                else:
                    attrs[f"http.request.header.{key}"] = value

        # 记录请求参数
        if request.params:
            attrs["http.request.params_count"] = len(request.params)

        # 记录请求体大小
        if self.record_body:
            if request.json:
                import json

                body_str = json.dumps(request.json)
                attrs["http.request_content_length"] = len(body_str)
            elif request.data:
                attrs["http.request_content_length"] = len(str(request.data))

        return attrs

    def _sanitize_header(self, key: str, value: str) -> str:
        """脱敏请求头

        Args:
            key: 头名称
            value: 头值

        Returns:
            脱敏后的值
        """
        if key.lower() in self.sensitive_headers:
            return "***"
        return value


class SpanContextCarrier:
    """Span上下文载体

    用于在拦截器间传递span上下文
    """

    _current_span = None
    _start_time = None

    @classmethod
    def set(cls, span: Any, start_time: float) -> None:
        """设置当前span

        Args:
            span: Span对象
            start_time: 开始时间
        """
        cls._current_span = span
        cls._start_time = start_time

    @classmethod
    def get(cls) -> tuple[Any, float | None]:
        """获取当前span

        Returns:
            (span, start_time) 元组
        """
        return cls._current_span, cls._start_time

    @classmethod
    def clear(cls) -> None:
        """清除当前span"""
        cls._current_span = None
        cls._start_time = None


__all__ = ["TracingInterceptor", "SpanContextCarrier"]
