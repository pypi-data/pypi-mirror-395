"""追踪拦截器

提供不同协议的追踪拦截器实现：
- TracingInterceptor - HTTP 追踪拦截器
- GrpcTracingInterceptor - gRPC 追踪拦截器 (v3.12.0)
- 未来可扩展 WebSocket 等拦截器
"""

from .grpc import GrpcTracingInterceptor
from .http import SpanContextCarrier, TracingInterceptor

__all__ = [
    # HTTP
    "TracingInterceptor",
    "SpanContextCarrier",
    # gRPC
    "GrpcTracingInterceptor",
]
