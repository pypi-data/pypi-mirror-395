"""
测试 v3.16.0 中间件配置系统

验证:
1. MiddlewareConfig 基类功能
2. 各种具体中间件配置类
3. 路径匹配规则
4. 配置验证
"""

import pytest

from df_test_framework.infrastructure.config import (
    BearerTokenMiddlewareConfig,
    LoggingMiddlewareConfig,
    MiddlewareConfig,
    MiddlewareType,
    RetryMiddlewareConfig,
    RetryStrategy,
    SignatureAlgorithm,
    SignatureMiddlewareConfig,
    TokenSource,
)


class TestMiddlewareConfig:
    """测试 MiddlewareConfig 基类"""

    def test_middleware_config_defaults(self):
        """测试默认值"""

        class TestMiddleware(MiddlewareConfig):
            type: MiddlewareType = MiddlewareType.LOGGING

        config = TestMiddleware()
        assert config.enabled is True
        assert config.priority == 50
        assert config.include_paths == []
        assert config.exclude_paths == []

    def test_middleware_config_with_paths(self):
        """测试路径配置"""

        class TestMiddleware(MiddlewareConfig):
            type: MiddlewareType = MiddlewareType.LOGGING

        config = TestMiddleware(
            include_paths=["/api/**", "/admin/**"],
            exclude_paths=["/api/health"],
        )
        assert config.include_paths == ["/api/**", "/admin/**"]
        assert config.exclude_paths == ["/api/health"]

    def test_normalize_paths_from_string(self):
        """测试路径标准化 - 从字符串"""

        class TestMiddleware(MiddlewareConfig):
            type: MiddlewareType = MiddlewareType.LOGGING

        config = TestMiddleware(include_paths="/api/**")
        assert config.include_paths == ["/api/**"]


class TestSignatureMiddlewareConfig:
    """测试签名中间件配置"""

    def test_signature_config_basic(self):
        """测试基础配置"""
        config = SignatureMiddlewareConfig(
            algorithm=SignatureAlgorithm.MD5,
            secret="my_secret",
        )
        assert config.type == MiddlewareType.SIGNATURE
        assert config.algorithm == SignatureAlgorithm.MD5
        assert config.secret == "my_secret"
        assert config.header == "X-Sign"
        assert config.enabled is True

    def test_signature_config_with_custom_header(self):
        """测试自定义 Header"""
        config = SignatureMiddlewareConfig(
            algorithm=SignatureAlgorithm.SHA256,
            secret="secret",
            header="Custom-Sign",
        )
        assert config.header == "Custom-Sign"

    def test_signature_config_with_paths(self):
        """测试路径过滤"""
        config = SignatureMiddlewareConfig(
            algorithm=SignatureAlgorithm.HMAC_SHA256,
            secret="secret",
            include_paths=["/master/**", "/h5/**"],
            exclude_paths=["/master/health"],
        )
        assert config.include_paths == ["/master/**", "/h5/**"]
        assert config.exclude_paths == ["/master/health"]


class TestBearerTokenMiddlewareConfig:
    """测试 Bearer Token 中间件配置"""

    def test_static_token_config(self):
        """测试静态 Token 配置"""
        config = BearerTokenMiddlewareConfig(
            source=TokenSource.STATIC,
            token="my_static_token",
        )
        assert config.source == TokenSource.STATIC
        assert config.token == "my_static_token"
        assert config.header == "Authorization"
        assert config.token_prefix == "Bearer"

    def test_login_token_config(self):
        """测试登录获取 Token 配置"""
        config = BearerTokenMiddlewareConfig(
            source=TokenSource.LOGIN,
            login_url="/auth/login",
            credentials={"username": "admin", "password": "pass"},
        )
        assert config.source == TokenSource.LOGIN
        assert config.login_url == "/auth/login"
        assert config.credentials == {"username": "admin", "password": "pass"}

    def test_custom_header_and_prefix(self):
        """测试自定义 Header 和前缀"""
        config = BearerTokenMiddlewareConfig(
            source=TokenSource.STATIC,
            token="token",
            header="X-Auth-Token",
            token_prefix="Token",
        )
        assert config.header == "X-Auth-Token"
        assert config.token_prefix == "Token"


class TestRetryMiddlewareConfig:
    """测试重试中间件配置"""

    def test_retry_config_defaults(self):
        """测试默认配置"""
        config = RetryMiddlewareConfig()
        assert config.type == MiddlewareType.RETRY
        assert config.max_retries == 3
        assert config.strategy == RetryStrategy.EXPONENTIAL
        assert config.initial_delay == 1.0
        assert config.max_delay == 60.0
        assert config.retry_on_status == [500, 502, 503, 504]

    def test_retry_config_custom(self):
        """测试自定义配置"""
        config = RetryMiddlewareConfig(
            max_retries=5,
            strategy=RetryStrategy.LINEAR,
            initial_delay=2.0,
            retry_on_status=[500, 502],
        )
        assert config.max_retries == 5
        assert config.strategy == RetryStrategy.LINEAR
        assert config.initial_delay == 2.0
        assert config.retry_on_status == [500, 502]


class TestLoggingMiddlewareConfig:
    """测试日志中间件配置"""

    def test_logging_config_defaults(self):
        """测试默认配置"""
        config = LoggingMiddlewareConfig()
        assert config.type == MiddlewareType.LOGGING
        assert config.log_request is True
        assert config.log_response is True
        assert config.log_headers is False
        assert config.log_body is True
        assert config.mask_fields == ["password", "token", "secret"]
        assert config.max_body_length == 1000

    def test_logging_config_custom(self):
        """测试自定义配置"""
        config = LoggingMiddlewareConfig(
            log_headers=True,
            mask_fields=["password", "api_key"],
            max_body_length=500,
        )
        assert config.log_headers is True
        assert config.mask_fields == ["password", "api_key"]
        assert config.max_body_length == 500


class TestMiddlewarePriority:
    """测试中间件优先级"""

    def test_priority_ordering(self):
        """测试优先级排序"""
        configs = [
            SignatureMiddlewareConfig(
                algorithm=SignatureAlgorithm.MD5,
                secret="s1",
                priority=50,
            ),
            BearerTokenMiddlewareConfig(
                source=TokenSource.STATIC,
                token="t1",
                priority=10,
            ),
            LoggingMiddlewareConfig(priority=100),
        ]

        # 按优先级排序（数字越小越先执行）
        sorted_configs = sorted(configs, key=lambda c: c.priority)
        assert sorted_configs[0].priority == 10
        assert sorted_configs[1].priority == 50
        assert sorted_configs[2].priority == 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
