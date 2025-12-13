"""
测试 MiddlewareFactory

验证从配置创建中间件实例的功能
"""

import pytest

from df_test_framework.capabilities.clients.http.middleware import (
    BearerTokenMiddleware,
    LoggingMiddleware,
    MiddlewareFactory,
    PathFilteredMiddleware,
    RetryMiddleware,
    SignatureMiddleware,
)
from df_test_framework.infrastructure.config import (
    BearerTokenMiddlewareConfig,
    LoggingMiddlewareConfig,
    RetryMiddlewareConfig,
    RetryStrategy,
    SignatureAlgorithm,
    SignatureMiddlewareConfig,
    TokenSource,
)


class TestMiddlewareFactory:
    """测试 MiddlewareFactory"""

    def test_create_signature_middleware(self):
        """测试创建签名中间件"""
        config = SignatureMiddlewareConfig(
            algorithm=SignatureAlgorithm.MD5,
            secret="test_secret",
            header="X-Sign",
            priority=10,
        )

        middleware = MiddlewareFactory.create(config)

        assert isinstance(middleware, SignatureMiddleware)
        assert middleware.secret == "test_secret"
        assert middleware.algorithm == "md5"
        assert middleware.header_name == "X-Sign"
        assert middleware.priority == 10

    def test_create_bearer_token_middleware_static(self):
        """测试创建 Bearer Token 中间件（静态模式）"""
        config = BearerTokenMiddlewareConfig(
            source=TokenSource.STATIC,
            token="my_token",
            header="Authorization",
            token_prefix="Bearer",
            priority=20,
        )

        middleware = MiddlewareFactory.create(config)

        assert isinstance(middleware, BearerTokenMiddleware)
        assert middleware._token == "my_token"
        assert middleware.header_name == "Authorization"
        assert middleware.header_prefix == "Bearer"
        assert middleware.priority == 20

    def test_create_bearer_token_middleware_login(self):
        """测试创建 Bearer Token 中间件（登录模式）- v3.17.0 已实现"""
        config = BearerTokenMiddlewareConfig(
            source=TokenSource.LOGIN,
            login_url="/auth/login",
            credentials={"username": "admin", "password": "pass"},
            token_path="data.token",
            priority=20,
        )

        middleware = MiddlewareFactory.create(config)

        assert isinstance(middleware, BearerTokenMiddleware)
        assert middleware._login_token_provider is not None
        assert middleware._login_token_provider.login_url == "/auth/login"
        assert middleware._login_token_provider.credentials == {
            "username": "admin",
            "password": "pass",
        }
        assert middleware._login_token_provider.token_path == "data.token"
        assert middleware.priority == 20

    def test_create_bearer_token_middleware_env(self):
        """测试创建 Bearer Token 中间件（环境变量模式）- v3.17.0 已实现"""
        config = BearerTokenMiddlewareConfig(
            source=TokenSource.ENV,
            env_var="MY_API_TOKEN",
            priority=25,
        )

        middleware = MiddlewareFactory.create(config)

        assert isinstance(middleware, BearerTokenMiddleware)
        assert middleware._token_provider is not None
        assert middleware.priority == 25

    def test_create_retry_middleware(self):
        """测试创建重试中间件"""
        config = RetryMiddlewareConfig(
            max_retries=5,
            strategy=RetryStrategy.EXPONENTIAL,
            initial_delay=2.0,
            retry_on_status=[500, 502],
            priority=30,
        )

        middleware = MiddlewareFactory.create(config)

        assert isinstance(middleware, RetryMiddleware)
        assert middleware.max_retries == 5
        assert middleware.initial_delay == 2.0
        assert middleware.retry_on_status == [500, 502]
        assert middleware.priority == 30

    def test_create_logging_middleware(self):
        """测试创建日志中间件"""
        config = LoggingMiddlewareConfig(
            log_request=True,
            log_response=True,
            log_headers=False,
            mask_fields=["password"],
            max_body_length=500,
            priority=100,
        )

        middleware = MiddlewareFactory.create(config)

        assert isinstance(middleware, LoggingMiddleware)
        assert middleware.log_request is True
        assert middleware.log_response is True
        assert middleware.log_headers is False
        assert middleware.log_body is True
        assert middleware.mask_fields == ["password"]
        assert middleware.max_body_length == 500
        assert middleware.priority == 100

    def test_create_disabled_middleware_returns_none(self):
        """测试禁用的中间件返回 None"""
        config = SignatureMiddlewareConfig(
            algorithm=SignatureAlgorithm.MD5,
            secret="secret",
            enabled=False,
        )

        middleware = MiddlewareFactory.create(config)

        assert middleware is None

    def test_create_multiple_middlewares(self):
        """测试批量创建中间件"""
        configs = [
            SignatureMiddlewareConfig(
                algorithm=SignatureAlgorithm.MD5,
                secret="s1",
                priority=10,
            ),
            BearerTokenMiddlewareConfig(
                source=TokenSource.STATIC,
                token="t1",
                priority=20,
            ),
            RetryMiddlewareConfig(priority=30),
            LoggingMiddlewareConfig(priority=100),
        ]

        middlewares = [MiddlewareFactory.create(c) for c in configs]

        assert len(middlewares) == 4
        assert isinstance(middlewares[0], SignatureMiddleware)
        assert isinstance(middlewares[1], BearerTokenMiddleware)
        assert isinstance(middlewares[2], RetryMiddleware)
        assert isinstance(middlewares[3], LoggingMiddleware)


class TestPathFilteredMiddleware:
    """测试 PathFilteredMiddleware"""

    def test_create_path_filtered_middleware(self):
        """测试创建路径过滤中间件"""
        base_middleware = SignatureMiddleware(secret="secret", priority=10)

        filtered = PathFilteredMiddleware(
            middleware=base_middleware,
            include_paths=["/api/**"],
            exclude_paths=["/api/health"],
        )

        assert filtered.name == "PathFiltered[SignatureMiddleware]"
        assert filtered.priority == 10
        assert filtered._include_paths == ["/api/**"]
        assert filtered._exclude_paths == ["/api/health"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
