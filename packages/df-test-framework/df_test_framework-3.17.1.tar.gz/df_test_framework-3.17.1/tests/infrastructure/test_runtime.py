"""
测试RuntimeContext和RuntimeBuilder

验证运行时上下文的构建、资源访问和生命周期管理。

v3.16.0: Runtime、Providers 已迁移到 bootstrap/ (Layer 4)
"""

import pytest

from df_test_framework.bootstrap import (
    ProviderRegistry,
    RuntimeBuilder,
    RuntimeContext,
    SingletonProvider,
)
from df_test_framework.infrastructure import FrameworkSettings
from df_test_framework.infrastructure.logging import logger
from df_test_framework.infrastructure.plugins import PluggyPluginManager


class MockResource:
    """模拟资源类"""

    def __init__(self, name: str):
        self.name = name
        self.closed = False

    def close(self):
        self.closed = True


class TestRuntimeBuilder:
    """测试RuntimeBuilder"""

    def test_builder_creation(self):
        """测试创建RuntimeBuilder实例"""
        builder = RuntimeBuilder()

        assert builder is not None
        assert builder._settings is None
        assert builder._logger is None
        assert builder._providers_factory is None
        assert builder._extensions is None

    def test_with_settings(self):
        """测试with_settings方法"""
        settings = FrameworkSettings(app_name="test")
        builder = RuntimeBuilder().with_settings(settings)

        assert builder._settings is settings

    def test_with_logger(self):
        """测试with_logger方法"""
        test_logger = logger
        builder = RuntimeBuilder().with_logger(test_logger)

        assert builder._logger is test_logger

    def test_with_providers(self):
        """测试with_providers方法"""

        def provider_factory():
            return ProviderRegistry(providers={})

        builder = RuntimeBuilder().with_providers(provider_factory)

        assert builder._providers_factory is provider_factory

    def test_with_extensions(self):
        """测试with_extensions方法"""
        extensions = PluggyPluginManager()
        builder = RuntimeBuilder().with_extensions(extensions)

        assert builder._extensions is extensions

    def test_fluent_chaining(self):
        """测试流式链式调用"""
        settings = FrameworkSettings(app_name="test")
        test_logger = logger
        extensions = PluggyPluginManager()

        def provider_factory():
            return ProviderRegistry(providers={})

        builder = (
            RuntimeBuilder()
            .with_settings(settings)
            .with_logger(test_logger)
            .with_providers(provider_factory)
            .with_extensions(extensions)
        )

        assert builder._settings is settings
        assert builder._logger is test_logger
        assert builder._providers_factory is provider_factory
        assert builder._extensions is extensions

    def test_build_without_settings_raises_error(self):
        """测试缺少settings时build抛出错误"""
        builder = RuntimeBuilder().with_logger(logger)

        with pytest.raises(ValueError, match="Settings must be provided"):
            builder.build()

    def test_build_without_logger_raises_error(self):
        """测试缺少logger时build抛出错误"""
        settings = FrameworkSettings(app_name="test")
        builder = RuntimeBuilder().with_settings(settings)

        with pytest.raises(ValueError, match="Logger must be provided"):
            builder.build()

    def test_build_creates_runtime_context(self):
        """测试build创建RuntimeContext"""
        settings = FrameworkSettings(app_name="test")
        builder = RuntimeBuilder().with_settings(settings).with_logger(logger)

        runtime = builder.build()

        try:
            assert isinstance(runtime, RuntimeContext)
            assert runtime.settings is settings
            assert runtime.logger is logger
            assert runtime.providers is not None
        finally:
            runtime.close()

    def test_build_with_custom_providers(self):
        """测试build使用自定义Providers"""
        settings = FrameworkSettings(app_name="test")
        custom_providers = ProviderRegistry(providers={})

        builder = (
            RuntimeBuilder()
            .with_settings(settings)
            .with_logger(logger)
            .with_providers(lambda: custom_providers)
        )

        runtime = builder.build()

        try:
            assert runtime.providers is custom_providers
        finally:
            runtime.close()

    def test_build_without_providers_uses_default(self):
        """测试build不提供providers时使用默认"""
        settings = FrameworkSettings(app_name="test")
        builder = RuntimeBuilder().with_settings(settings).with_logger(logger)

        runtime = builder.build()

        try:
            # 应该使用default_providers()
            assert runtime.providers is not None
            assert isinstance(runtime.providers, ProviderRegistry)
        finally:
            runtime.close()

    def test_build_with_extensions(self):
        """测试build包含extensions"""
        settings = FrameworkSettings(app_name="test")
        extensions = PluggyPluginManager()

        builder = (
            RuntimeBuilder().with_settings(settings).with_logger(logger).with_extensions(extensions)
        )

        runtime = builder.build()

        try:
            assert runtime.extensions is extensions
        finally:
            runtime.close()


class TestRuntimeContext:
    """测试RuntimeContext"""

    def test_runtime_context_creation(self):
        """测试创建RuntimeContext"""
        settings = FrameworkSettings(app_name="test")
        providers = ProviderRegistry(providers={})

        runtime = RuntimeContext(
            settings=settings,
            logger=logger,
            providers=providers,
        )

        assert runtime.settings is settings
        assert runtime.logger is logger
        assert runtime.providers is providers
        assert runtime.extensions is None

    def test_runtime_context_with_extensions(self):
        """测试RuntimeContext包含extensions"""
        settings = FrameworkSettings(app_name="test")
        providers = ProviderRegistry(providers={})
        extensions = PluggyPluginManager()

        runtime = RuntimeContext(
            settings=settings,
            logger=logger,
            providers=providers,
            extensions=extensions,
        )

        assert runtime.extensions is extensions

    def test_runtime_context_is_frozen(self):
        """测试RuntimeContext是frozen的（不可变）"""
        settings = FrameworkSettings(app_name="test")
        providers = ProviderRegistry(providers={})

        runtime = RuntimeContext(
            settings=settings,
            logger=logger,
            providers=providers,
        )

        # 尝试修改frozen dataclass应该抛出异常
        with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
            runtime.settings = FrameworkSettings(app_name="modified")

    def test_get_provider_by_key(self):
        """测试通过key获取Provider资源"""
        settings = FrameworkSettings(app_name="test")
        resource = MockResource("test_resource")

        providers = ProviderRegistry(providers={})
        providers.register("test_key", SingletonProvider(lambda ctx: resource))

        runtime = RuntimeContext(
            settings=settings,
            logger=logger,
            providers=providers,
        )

        retrieved = runtime.get("test_key")
        assert retrieved is resource

    def test_http_client_shortcut(self):
        """测试http_client快捷方法"""
        settings = FrameworkSettings(app_name="test")
        mock_client = MockResource("http_client")

        providers = ProviderRegistry(providers={})
        providers.register("http_client", SingletonProvider(lambda ctx: mock_client))

        runtime = RuntimeContext(
            settings=settings,
            logger=logger,
            providers=providers,
        )

        client = runtime.http_client()
        assert client is mock_client

    def test_database_shortcut(self):
        """测试database快捷方法"""
        settings = FrameworkSettings(app_name="test")
        mock_db = MockResource("database")

        providers = ProviderRegistry(providers={})
        providers.register("database", SingletonProvider(lambda ctx: mock_db))

        runtime = RuntimeContext(
            settings=settings,
            logger=logger,
            providers=providers,
        )

        db = runtime.database()
        assert db is mock_db

    def test_redis_shortcut(self):
        """测试redis快捷方法"""
        settings = FrameworkSettings(app_name="test")
        mock_redis = MockResource("redis")

        providers = ProviderRegistry(providers={})
        providers.register("redis", SingletonProvider(lambda ctx: mock_redis))

        runtime = RuntimeContext(
            settings=settings,
            logger=logger,
            providers=providers,
        )

        redis = runtime.redis()
        assert redis is mock_redis

    def test_close_shuts_down_providers(self):
        """测试close方法关闭所有providers"""
        settings = FrameworkSettings(app_name="test")
        resource1 = MockResource("resource1")
        resource2 = MockResource("resource2")

        providers = ProviderRegistry(providers={})
        providers.register("res1", SingletonProvider(lambda ctx: resource1))
        providers.register("res2", SingletonProvider(lambda ctx: resource2))

        runtime = RuntimeContext(
            settings=settings,
            logger=logger,
            providers=providers,
        )

        # 先获取资源以初始化它们
        runtime.get("res1")
        runtime.get("res2")

        # 验证资源未关闭
        assert not resource1.closed
        assert not resource2.closed

        # 关闭runtime
        runtime.close()

        # 验证资源已关闭
        assert resource1.closed
        assert resource2.closed

    def test_with_overrides_nested_dict(self):
        """测试with_overrides支持嵌套字典覆盖（v3.5 Phase 3）

        v3.16.0: 使用 HTTPConfig 替代 HTTPSettings
        """
        from df_test_framework.infrastructure.config.schema import HTTPConfig

        settings = FrameworkSettings(
            app_name="test",
            http=HTTPConfig(base_url="http://original.com", timeout=30, max_retries=3),
        )
        providers = ProviderRegistry(providers={})

        runtime = RuntimeContext(
            settings=settings,
            logger=logger,
            providers=providers,
        )

        # 使用嵌套字典覆盖http配置
        new_runtime = runtime.with_overrides({"http": {"timeout": 10, "max_retries": 1}})

        # 验证原runtime未修改
        assert runtime.settings.http.timeout == 30
        assert runtime.settings.http.max_retries == 3
        assert runtime.settings.http.base_url == "http://original.com"

        # 验证新runtime的配置已覆盖
        assert new_runtime.settings.http.timeout == 10
        assert new_runtime.settings.http.max_retries == 1
        assert new_runtime.settings.http.base_url == "http://original.com"  # 未覆盖的保持不变

        # ✅ 修复验证: logger共享,但providers必须不共享(避免SingletonProvider缓存问题)
        assert new_runtime.logger is runtime.logger  # logger可共享(无状态)
        assert new_runtime.providers is not runtime.providers  # ✅ providers不共享(避免配置污染)

    def test_with_overrides_dot_notation(self):
        """测试with_overrides支持点号路径覆盖（v3.5 Phase 3）

        v3.16.0: 使用 HTTPConfig 替代 HTTPSettings
        """
        from df_test_framework.infrastructure.config.schema import HTTPConfig

        settings = FrameworkSettings(
            app_name="test", http=HTTPConfig(base_url="http://original.com", timeout=30)
        )
        providers = ProviderRegistry(providers={})

        runtime = RuntimeContext(
            settings=settings,
            logger=logger,
            providers=providers,
        )

        # 使用点号路径覆盖 http 配置
        new_runtime = runtime.with_overrides(
            {"http.timeout": 5, "http.base_url": "http://mock.local"}
        )

        # 验证原runtime未修改
        assert runtime.settings.http.timeout == 30
        assert runtime.settings.http.base_url == "http://original.com"

        # 验证新runtime的配置已覆盖
        assert new_runtime.settings.http.timeout == 5
        assert new_runtime.settings.http.base_url == "http://mock.local"

    def test_with_overrides_multiple_fields(self):
        """测试with_overrides同时覆盖多个字段（v3.5 Phase 3）

        v3.16.0: 使用 HTTPConfig 替代 HTTPSettings
        """
        from df_test_framework.infrastructure.config.schema import DatabaseConfig, HTTPConfig

        settings = FrameworkSettings(
            app_name="test",
            app_env="prod",
            http=HTTPConfig(base_url="http://prod.com", timeout=30),
            db=DatabaseConfig(host="prod.db.com", port=3306, name="prod_db"),
        )
        providers = ProviderRegistry(providers={})

        runtime = RuntimeContext(
            settings=settings,
            logger=logger,
            providers=providers,
        )

        # 同时覆盖多个配置
        new_runtime = runtime.with_overrides(
            {
                "app_env": "test",
                "http": {"timeout": 5},
                "db.host": "localhost",
                "db.name": "test_db",
            }
        )

        # 验证所有覆盖都生效
        assert new_runtime.settings.app_env == "test"
        assert new_runtime.settings.http.timeout == 5
        assert new_runtime.settings.http.base_url == "http://prod.com"  # 未覆盖
        assert new_runtime.settings.db.host == "localhost"
        assert new_runtime.settings.db.name == "test_db"
        assert new_runtime.settings.db.port == 3306  # 未覆盖

    def test_with_overrides_immutability(self):
        """测试with_overrides不可变特性（v3.5 Phase 3）"""
        settings = FrameworkSettings(app_name="original")
        providers = ProviderRegistry(providers={})

        runtime = RuntimeContext(
            settings=settings,
            logger=logger,
            providers=providers,
        )

        # 创建多个覆盖实例
        runtime1 = runtime.with_overrides({"app_name": "override1"})
        runtime2 = runtime.with_overrides({"app_name": "override2"})

        # 验证原runtime未修改
        assert runtime.settings.app_name == "original"

        # 验证每个新runtime独立
        assert runtime1.settings.app_name == "override1"
        assert runtime2.settings.app_name == "override2"

        # 验证它们是不同的实例
        assert runtime1 is not runtime2
        assert runtime1 is not runtime


class TestRuntimeIntegration:
    """集成测试：RuntimeBuilder + RuntimeContext完整流程"""

    def test_complete_runtime_creation_flow(self):
        """测试完整的Runtime创建流程"""
        # 准备组件
        settings = FrameworkSettings(app_name="IntegrationTest", app_env="test")
        extensions = PluggyPluginManager()
        resource = MockResource("test_resource")

        def provider_factory():
            providers = ProviderRegistry(providers={})
            providers.register("test_resource", SingletonProvider(lambda ctx: resource))
            return providers

        # 使用Builder构建Runtime
        runtime = (
            RuntimeBuilder()
            .with_settings(settings)
            .with_logger(logger)
            .with_providers(provider_factory)
            .with_extensions(extensions)
            .build()
        )

        try:
            # 验证RuntimeContext
            assert isinstance(runtime, RuntimeContext)
            assert runtime.settings.app_name == "IntegrationTest"
            assert runtime.settings.app_env == "test"
            assert runtime.logger is logger
            assert runtime.extensions is extensions

            # 验证可以获取资源
            retrieved_resource = runtime.get("test_resource")
            assert retrieved_resource is resource

            # 验证资源未关闭
            assert not resource.closed

        finally:
            # 清理
            runtime.close()
            # 验证资源已关闭
            assert resource.closed

    def test_minimal_runtime_creation(self):
        """测试最小配置的Runtime创建"""
        settings = FrameworkSettings()

        runtime = RuntimeBuilder().with_settings(settings).with_logger(logger).build()

        try:
            assert runtime.settings is not None
            assert runtime.logger is not None
            assert runtime.providers is not None
            # extensions是可选的
        finally:
            runtime.close()
