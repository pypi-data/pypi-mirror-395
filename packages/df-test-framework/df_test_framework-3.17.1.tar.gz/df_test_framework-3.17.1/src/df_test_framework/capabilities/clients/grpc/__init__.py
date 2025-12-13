"""gRPC 客户端模块

提供 gRPC 服务测试能力，支持：
- Unary RPC（一元调用）
- Server Streaming RPC（服务端流式）
- 元数据（Metadata）管理
- 拦截器（Interceptor）支持
- 健康检查
- 重试策略

注意：Client Streaming 和 Bidirectional Streaming 计划在后续版本实现。
"""

from df_test_framework.capabilities.clients.grpc.client import GrpcClient
from df_test_framework.capabilities.clients.grpc.interceptors import (
    LoggingInterceptor,
    MetadataInterceptor,
    RetryInterceptor,
)
from df_test_framework.capabilities.clients.grpc.models import GrpcError, GrpcResponse

__all__ = [
    "GrpcClient",
    "GrpcResponse",
    "GrpcError",
    "LoggingInterceptor",
    "MetadataInterceptor",
    "RetryInterceptor",
]
