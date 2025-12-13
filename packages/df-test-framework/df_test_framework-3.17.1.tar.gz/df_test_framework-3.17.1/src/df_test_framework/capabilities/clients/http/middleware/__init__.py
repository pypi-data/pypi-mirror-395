"""
HTTP 中间件

v3.14.0: 基于洋葱模型的 HTTP 中间件系统。
v3.17.0: 新增 LoginTokenProvider、create_env_token_provider 支持动态 Token 获取。

替代 v3.x 的 interceptors 系统，提供更简洁的 API。

示例:
    from df_test_framework.capabilities.clients.http.middleware import (
        SignatureMiddleware,
        BearerTokenMiddleware,
        RetryMiddleware,
        LoginTokenProvider,
        create_env_token_provider,
    )

    # 静态 Token
    client = HttpClient(
        base_url="https://api.example.com",
        middlewares=[
            RetryMiddleware(max_attempts=3),
            SignatureMiddleware(secret="xxx"),
            BearerTokenMiddleware(token="my_token"),
        ]
    )

    # 动态登录获取 Token (v3.17.0+)
    login_provider = LoginTokenProvider(
        login_url="/admin/login",
        credentials={"username": "admin", "password": "pass"},
    )
    middleware = BearerTokenMiddleware(login_token_provider=login_provider)

    # 环境变量 Token (v3.17.0+)
    middleware = BearerTokenMiddleware(
        token_provider=create_env_token_provider("MY_API_TOKEN")
    )
"""

from df_test_framework.capabilities.clients.http.middleware.auth import (
    ApiKeyMiddleware,
    BearerTokenMiddleware,
    LoginTokenProvider,
    create_env_token_provider,
)

# v3.16.0: 中间件工厂
from df_test_framework.capabilities.clients.http.middleware.factory import (
    MiddlewareFactory,
    PathFilteredMiddleware,
)
from df_test_framework.capabilities.clients.http.middleware.logging import (
    LoggingMiddleware,
)
from df_test_framework.capabilities.clients.http.middleware.retry import (
    RetryMiddleware,
)
from df_test_framework.capabilities.clients.http.middleware.signature import (
    SignatureMiddleware,
)
from df_test_framework.capabilities.clients.http.middleware.telemetry import (
    HttpTelemetryMiddleware,
)

__all__ = [
    # 具体中间件类
    "SignatureMiddleware",
    "BearerTokenMiddleware",
    "ApiKeyMiddleware",
    "RetryMiddleware",
    "LoggingMiddleware",
    "HttpTelemetryMiddleware",
    # v3.17.0: Token 提供器
    "LoginTokenProvider",
    "create_env_token_provider",
    # v3.16.0: 工厂和工具类
    "MiddlewareFactory",
    "PathFilteredMiddleware",
]
