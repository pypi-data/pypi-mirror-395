"""
测试 v3.16.0 拦截器到中间件的自动迁移

验证 HTTPConfig.migrate_interceptors_to_middlewares() 功能
"""

import pytest

from df_test_framework.infrastructure.config import (
    BearerTokenInterceptorConfig,
    BearerTokenMiddlewareConfig,
    HTTPConfig,
    SignatureInterceptorConfig,
    SignatureMiddlewareConfig,
    TokenSource,
)


class TestInterceptorMigration:
    """测试拦截器自动迁移功能"""

    def test_migrate_signature_interceptor(self):
        """测试签名拦截器迁移"""
        # 使用旧的 interceptors 配置
        config = HTTPConfig(
            base_url="http://localhost:8000",
            interceptors=[
                SignatureInterceptorConfig(
                    type="signature",
                    enabled=True,
                    priority=10,
                    algorithm="md5",
                    secret="test_secret",
                    header_name="X-Sign",
                    include_paths=["/api/**"],
                    exclude_paths=["/api/health"],
                )
            ],
        )

        # 验证自动迁移
        assert len(config.middlewares) == 1
        middleware = config.middlewares[0]
        assert isinstance(middleware, SignatureMiddlewareConfig)
        assert middleware.algorithm == "md5"
        assert middleware.secret == "test_secret"
        assert middleware.header == "X-Sign"
        assert middleware.enabled is True
        assert middleware.priority == 10
        assert middleware.include_paths == ["/api/**"]
        assert middleware.exclude_paths == ["/api/health"]

    def test_migrate_bearer_token_interceptor_login(self):
        """测试 Bearer Token 拦截器迁移（登录模式）"""
        config = HTTPConfig(
            base_url="http://localhost:8000",
            interceptors=[
                BearerTokenInterceptorConfig(
                    type="bearer_token",
                    token_source="login",
                    login_url="/auth/login",
                    login_credentials={"username": "admin", "password": "pass"},
                    include_paths=["/admin/**"],
                )
            ],
        )

        # 验证迁移
        assert len(config.middlewares) == 1
        middleware = config.middlewares[0]
        assert isinstance(middleware, BearerTokenMiddlewareConfig)
        assert middleware.source == TokenSource.LOGIN
        assert middleware.login_url == "/auth/login"
        assert middleware.credentials == {"username": "admin", "password": "pass"}
        assert middleware.include_paths == ["/admin/**"]

    def test_migrate_bearer_token_interceptor_static(self):
        """测试 Bearer Token 拦截器迁移（静态模式）"""
        config = HTTPConfig(
            base_url="http://localhost:8000",
            interceptors=[
                BearerTokenInterceptorConfig(
                    type="bearer_token",
                    token_source="static",
                    static_token="my_static_token",
                )
            ],
        )

        # 验证迁移
        assert len(config.middlewares) == 1
        middleware = config.middlewares[0]
        assert isinstance(middleware, BearerTokenMiddlewareConfig)
        assert middleware.source == TokenSource.STATIC
        assert middleware.token == "my_static_token"

    def test_migrate_multiple_interceptors(self):
        """测试迁移多个拦截器"""
        config = HTTPConfig(
            base_url="http://localhost:8000",
            interceptors=[
                SignatureInterceptorConfig(
                    type="signature",
                    algorithm="md5",
                    secret="secret1",
                    priority=10,
                ),
                BearerTokenInterceptorConfig(
                    type="bearer_token",
                    token_source="static",
                    static_token="token1",
                    priority=20,
                ),
            ],
        )

        # 验证迁移
        assert len(config.middlewares) == 2
        assert isinstance(config.middlewares[0], SignatureMiddlewareConfig)
        assert isinstance(config.middlewares[1], BearerTokenMiddlewareConfig)

    def test_no_migration_when_middlewares_exists(self):
        """测试当 middlewares 已存在时不执行迁移"""
        existing_middleware = SignatureMiddlewareConfig(
            algorithm="sha256",
            secret="new_secret",
        )

        config = HTTPConfig(
            base_url="http://localhost:8000",
            middlewares=[existing_middleware],
            interceptors=[
                SignatureInterceptorConfig(
                    type="signature",
                    algorithm="md5",
                    secret="old_secret",
                )
            ],
        )

        # 验证不执行迁移，保持原有 middlewares
        assert len(config.middlewares) == 1
        assert config.middlewares[0].algorithm == "sha256"
        assert config.middlewares[0].secret == "new_secret"

    def test_no_migration_when_interceptors_empty(self):
        """测试当 interceptors 为空时不执行迁移"""
        config = HTTPConfig(
            base_url="http://localhost:8000",
            interceptors=[],
        )

        # 验证不执行迁移
        assert len(config.middlewares) == 0

    def test_direct_middlewares_config(self):
        """测试直接使用 middlewares 配置（推荐方式）"""
        config = HTTPConfig(
            base_url="http://localhost:8000",
            middlewares=[
                SignatureMiddlewareConfig(
                    algorithm="md5",
                    secret="secret",
                    priority=10,
                ),
                BearerTokenMiddlewareConfig(
                    source=TokenSource.STATIC,
                    token="token",
                    priority=20,
                ),
            ],
        )

        # 验证配置
        assert len(config.middlewares) == 2
        assert isinstance(config.middlewares[0], SignatureMiddlewareConfig)
        assert isinstance(config.middlewares[1], BearerTokenMiddlewareConfig)
        assert len(config.interceptors) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
