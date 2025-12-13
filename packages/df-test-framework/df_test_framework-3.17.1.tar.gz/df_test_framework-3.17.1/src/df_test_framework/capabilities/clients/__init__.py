"""
客户端能力层

包含：
- http/: HTTP/REST 客户端
- graphql/: GraphQL 客户端
- grpc/: gRPC 客户端

v3.14.0: 从顶级 clients/ 迁移，添加中间件系统。
"""

# 重导出原有模块
from df_test_framework.capabilities.clients.http import AsyncHttpClient, HttpClient
from df_test_framework.capabilities.clients.http.core import Request, Response

__all__ = [
    "HttpClient",
    "AsyncHttpClient",
    "Request",
    "Response",
]
