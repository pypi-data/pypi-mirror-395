"""
HTTP 客户端

v3.14.0 增强：
- 统一中间件系统（洋葱模型）
- 可观测性集成
- 上下文传播

导入示例：
    from df_test_framework.capabilities.clients.http import HttpClient
    from df_test_framework.capabilities.clients.http.middleware import (
        SignatureMiddleware,
        BearerTokenMiddleware,
    )
"""

# 重导出原有客户端
from df_test_framework.capabilities.clients.http.core.request import Request
from df_test_framework.capabilities.clients.http.core.response import Response
from df_test_framework.capabilities.clients.http.rest.httpx.async_client import AsyncHttpClient
from df_test_framework.capabilities.clients.http.rest.httpx.client import HttpClient

__all__ = [
    "HttpClient",
    "AsyncHttpClient",
    "Request",
    "Response",
]
