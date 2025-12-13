"""gRPC 追踪拦截器

为 gRPC 请求添加分布式追踪支持

v3.12.0 新增 - 基础设施层 gRPC 追踪
"""

from __future__ import annotations

import time
from typing import Any

from df_test_framework.capabilities.clients.grpc.interceptors import BaseInterceptor

from ..context import TracingContext
from ..manager import OTEL_AVAILABLE, get_tracing_manager

if OTEL_AVAILABLE:
    from opentelemetry import trace


class GrpcTracingInterceptor(BaseInterceptor):
    """gRPC 追踪拦截器

    自动为 gRPC 请求创建追踪 span，记录:
    - RPC 方法名称
    - 请求/响应元数据（可选）
    - 状态码
    - 响应时间
    - 异常信息

    使用示例:
        >>> from df_test_framework.infrastructure.tracing.interceptors import (
        ...     GrpcTracingInterceptor
        ... )
        >>>
        >>> # 基础用法
        >>> interceptor = GrpcTracingInterceptor()
        >>> client.add_interceptor(interceptor)
        >>>
        >>> # 自定义配置
        >>> interceptor = GrpcTracingInterceptor(
        ...     record_metadata=True,
        ...     propagate_context=True
        ... )

    追踪属性:
        - rpc.system: "grpc"
        - rpc.service: 服务名称
        - rpc.method: 方法名称
        - rpc.grpc.status_code: gRPC 状态码
        - rpc.request.duration_ms: 请求耗时（毫秒）
    """

    # W3C Trace Context 标准头名称
    TRACEPARENT_HEADER = "traceparent"
    TRACESTATE_HEADER = "tracestate"

    def __init__(
        self,
        record_metadata: bool = False,
        propagate_context: bool = True,
        sensitive_keys: list[str] | None = None,
    ):
        """初始化 gRPC 追踪拦截器

        Args:
            record_metadata: 是否记录请求/响应元数据
            propagate_context: 是否传播追踪上下文（注入 traceparent 头）
            sensitive_keys: 敏感元数据键列表，记录时会脱敏
        """
        self.record_metadata = record_metadata
        self.propagate_context = propagate_context
        self.sensitive_keys = sensitive_keys or [
            "authorization",
            "x-api-key",
            "x-auth-token",
            "cookie",
        ]

        # 用于存储调用开始时间（通过元数据传递）
        self._start_time_key = "x-tracing-start-time"
        self._span_id_key = "x-tracing-span-id"

    def intercept_unary(
        self,
        method: str,
        request: Any,
        metadata: list[tuple[str, str]],
    ) -> tuple[Any, list[tuple[str, str]]]:
        """拦截一元调用 - 创建 span 并注入追踪上下文

        Args:
            method: 方法名（格式: /package.Service/Method）
            request: 请求对象
            metadata: 元数据列表

        Returns:
            (请求对象, 注入追踪头后的元数据)
        """
        if not OTEL_AVAILABLE:
            return request, metadata

        manager = get_tracing_manager()

        # 解析服务名和方法名
        service_name, method_name = self._parse_method(method)

        # 创建 span
        span_name = f"gRPC {service_name}/{method_name}"
        attributes = self._build_request_attributes(method, service_name, method_name, metadata)
        span = manager.start_span_no_context(span_name, attributes=attributes)

        # 记录开始时间
        start_time = time.perf_counter()

        # 将 span 信息添加到元数据中传递
        metadata_dict = dict(metadata)
        metadata_dict[self._start_time_key] = str(start_time)

        # 存储 span 以便后续使用（使用 span 的 context）
        if span:
            span_context = span.get_span_context()
            metadata_dict[self._span_id_key] = format(span_context.span_id, "016x")

        # 传播追踪上下文
        if self.propagate_context:
            TracingContext.inject(metadata_dict)

        # 转换回元数据列表
        new_metadata = [(k, v) for k, v in metadata_dict.items()]

        return request, new_metadata

    def intercept_response(
        self,
        method: str,
        response: Any,
        metadata: dict[str, str],
    ) -> Any:
        """拦截响应 - 完成 span 并记录响应信息

        Args:
            method: 方法名
            response: 响应对象
            metadata: 响应元数据

        Returns:
            响应对象（不修改）
        """
        if not OTEL_AVAILABLE:
            return response

        span = trace.get_current_span()

        if span and span.is_recording():
            # 计算耗时
            start_time_str = metadata.get(self._start_time_key)
            if start_time_str:
                try:
                    start_time = float(start_time_str)
                    duration_ms = (time.perf_counter() - start_time) * 1000
                    span.set_attribute("rpc.request.duration_ms", duration_ms)
                except ValueError:
                    pass

            # 记录响应元数据
            if self.record_metadata:
                for key, value in metadata.items():
                    if key.startswith("x-tracing-"):
                        continue  # 跳过内部键
                    sanitized = self._sanitize_value(key, value)
                    span.set_attribute(f"rpc.response.metadata.{key}", sanitized)

            # 设置成功状态
            span.set_attribute("rpc.grpc.status_code", 0)  # OK
            span.set_status(trace.Status(trace.StatusCode.OK))
            span.end()

        return response

    def on_error(self, method: str, error: Exception, status_code: int) -> None:
        """错误处理 - 记录异常并结束 span

        Args:
            method: 方法名
            error: 异常对象
            status_code: gRPC 状态码
        """
        if not OTEL_AVAILABLE:
            return

        span = trace.get_current_span()

        if span and span.is_recording():
            # 记录异常
            span.record_exception(error)
            span.set_attribute("rpc.grpc.status_code", status_code)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(error)))
            span.end()

    def _parse_method(self, method: str) -> tuple[str, str]:
        """解析 gRPC 方法名

        Args:
            method: 完整方法名（格式: /package.Service/Method）

        Returns:
            (服务名, 方法名)
        """
        # 格式: /package.Service/Method
        parts = method.strip("/").split("/")
        if len(parts) >= 2:
            return parts[0], parts[1]
        return method, "unknown"

    def _build_request_attributes(
        self,
        full_method: str,
        service_name: str,
        method_name: str,
        metadata: list[tuple[str, str]],
    ) -> dict[str, Any]:
        """构建请求属性

        Args:
            full_method: 完整方法名
            service_name: 服务名
            method_name: 方法名
            metadata: 元数据列表

        Returns:
            属性字典
        """
        attrs: dict[str, Any] = {
            "rpc.system": "grpc",
            "rpc.service": service_name,
            "rpc.method": method_name,
            "rpc.grpc.full_method": full_method,
        }

        # 记录请求元数据
        if self.record_metadata:
            for key, value in metadata:
                if key.startswith("x-tracing-"):
                    continue  # 跳过内部键
                sanitized = self._sanitize_value(key, value)
                attrs[f"rpc.request.metadata.{key}"] = sanitized

        return attrs

    def _sanitize_value(self, key: str, value: str) -> str:
        """脱敏元数据值

        Args:
            key: 键名
            value: 值

        Returns:
            脱敏后的值
        """
        if key.lower() in self.sensitive_keys:
            return "***"
        return value


__all__ = ["GrpcTracingInterceptor"]
