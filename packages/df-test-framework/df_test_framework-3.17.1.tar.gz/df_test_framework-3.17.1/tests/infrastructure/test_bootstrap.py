"""
测试Bootstrap启动流程

验证Bootstrap配置构建、BootstrapApp运行和RuntimeContext创建的完整流程。

v3.16.0: Bootstrap、Providers、Runtime 已迁移到 bootstrap/ (Layer 4)
"""

from df_test_framework.bootstrap import (
    Bootstrap,
    BootstrapApp,
    ProviderRegistry,
    RuntimeContext,
)
from df_test_framework.infrastructure import (
    FrameworkSettings,
    LoguruStructuredStrategy,
    NoOpStrategy,
    clear_settings,
)
from df_test_framework.infrastructure.config import (
    DictSource,
)
from df_test_framework.infrastructure.plugins import PluggyPluginManager


class CustomSettings(FrameworkSettings):
    """自定义配置类用于测试（Pydantic v2模型）"""

    custom_field: str = "default_value"


class TestBootstrap:
    """测试Bootstrap构建器"""

    def test_default_bootstrap_creation(self):
        """测试创建默认Bootstrap实例"""
        bootstrap = Bootstrap()

        assert bootstrap.settings_cls == FrameworkSettings
        assert bootstrap.namespace == "default"
        assert bootstrap.sources is None
        assert bootstrap.cache_enabled is True
        assert isinstance(bootstrap.logger_strategy, LoguruStructuredStrategy)
        assert bootstrap.provider_factory is None
        assert bootstrap.plugins == []

    def test_with_settings(self):
        """测试with_settings流式配置"""
        sources = [DictSource({"app_name": "test"})]

        bootstrap = Bootstrap().with_settings(
            CustomSettings,
            namespace="test",
            sources=sources,
            cache_enabled=False,
        )

        assert bootstrap.settings_cls == CustomSettings
        assert bootstrap.namespace == "test"
        assert bootstrap.sources == sources
        assert bootstrap.cache_enabled is False

    def test_with_settings_profile(self):
        """测试with_settings支持profile参数（v3.5 Phase 3）"""
        bootstrap = Bootstrap().with_settings(
            CustomSettings,
            namespace="test",
            profile="dev",
        )

        assert bootstrap.settings_cls == CustomSettings
        assert bootstrap.namespace == "test"
        assert bootstrap.profile == "dev"

    def test_with_logging(self):
        """测试with_logging流式配置"""
        noop_strategy = NoOpStrategy()
        bootstrap = Bootstrap().with_logging(noop_strategy)

        assert bootstrap.logger_strategy is noop_strategy

    def test_with_provider_factory(self):
        """测试with_provider_factory流式配置"""

        def custom_factory():
            return ProviderRegistry(providers={})

        bootstrap = Bootstrap().with_provider_factory(custom_factory)

        assert bootstrap.provider_factory is custom_factory

    def test_with_plugin(self):
        """测试with_plugin流式配置"""
        plugin1 = "path.to.plugin1"
        plugin2 = object()

        bootstrap = Bootstrap().with_plugin(plugin1).with_plugin(plugin2)

        assert len(bootstrap.plugins) == 2
        assert bootstrap.plugins[0] == plugin1
        assert bootstrap.plugins[1] is plugin2

    def test_fluent_chaining(self):
        """测试流式链式调用"""
        sources = [DictSource({"app_name": "test"})]
        noop_strategy = NoOpStrategy()

        bootstrap = (
            Bootstrap()
            .with_settings(CustomSettings, namespace="test", sources=sources)
            .with_logging(noop_strategy)
            .with_plugin("plugin1")
            .with_plugin("plugin2")
        )

        assert bootstrap.settings_cls == CustomSettings
        assert bootstrap.namespace == "test"
        assert bootstrap.sources == sources
        assert bootstrap.logger_strategy is noop_strategy
        assert len(bootstrap.plugins) == 2

    def test_build_returns_bootstrap_app(self):
        """测试build方法返回BootstrapApp"""
        bootstrap = Bootstrap().with_settings(CustomSettings, namespace="test")
        app = bootstrap.build()

        assert isinstance(app, BootstrapApp)
        assert app.settings_cls == CustomSettings
        assert app.namespace == "test"
        assert app.cache_enabled is True


class TestBootstrapApp:
    """测试BootstrapApp运行"""

    def setup_method(self):
        """每个测试前清理配置"""
        clear_settings("default")
        clear_settings("test")

    def teardown_method(self):
        """每个测试后清理配置"""
        clear_settings("default")
        clear_settings("test")

    def test_run_creates_runtime_context(self):
        """测试run方法创建RuntimeContext"""
        app = Bootstrap().with_logging(NoOpStrategy()).build()
        runtime = app.run()

        try:
            assert isinstance(runtime, RuntimeContext)
            assert runtime.settings is not None
            assert runtime.logger is not None
            assert runtime.providers is not None
        finally:
            runtime.close()

    def test_run_with_custom_settings(self):
        """测试使用自定义配置运行"""
        sources = [DictSource({"custom_field": "test_value"})]

        app = (
            Bootstrap()
            .with_settings(CustomSettings, namespace="custom", sources=sources)
            .with_logging(NoOpStrategy())
            .build()
        )

        runtime = app.run()

        try:
            assert isinstance(runtime.settings, CustomSettings)
            assert runtime.settings.custom_field == "test_value"
        finally:
            runtime.close()
            clear_settings("custom")

    def test_run_with_force_reload(self):
        """测试force_reload强制重新加载配置"""
        sources1 = [DictSource({"app_name": "app1"})]
        app1 = (
            Bootstrap()
            .with_settings(FrameworkSettings, namespace="reload_test", sources=sources1)
            .with_logging(NoOpStrategy())
            .build()
        )

        runtime1 = app1.run()
        try:
            assert runtime1.settings.app_name == "app1"
        finally:
            runtime1.close()

        # 第二次运行，使用force_reload
        sources2 = [DictSource({"app_name": "app2"})]
        app2 = (
            Bootstrap()
            .with_settings(FrameworkSettings, namespace="reload_test", sources=sources2)
            .with_logging(NoOpStrategy())
            .build()
        )

        runtime2 = app2.run(force_reload=True)
        try:
            assert runtime2.settings.app_name == "app2"
        finally:
            runtime2.close()
            clear_settings("reload_test")

    def test_run_handles_already_configured_settings(self):
        """测试处理已配置的settings（不使用force_reload）"""
        sources = [DictSource({"app_name": "first"})]
        app = (
            Bootstrap()
            .with_settings(FrameworkSettings, namespace="duplicate_test", sources=sources)
            .with_logging(NoOpStrategy())
            .build()
        )

        # 第一次运行
        runtime1 = app.run()
        try:
            assert runtime1.settings.app_name == "first"
        finally:
            runtime1.close()

        # 第二次运行（不使用force_reload，应该使用缓存）
        runtime2 = app.run()
        try:
            # 应该使用缓存的配置
            assert runtime2.settings.app_name == "first"
        finally:
            runtime2.close()
            clear_settings("duplicate_test")

    def test_run_initializes_providers(self):
        """测试运行初始化Providers"""
        app = Bootstrap().with_logging(NoOpStrategy()).build()
        runtime = app.run()

        try:
            # 验证默认providers已初始化
            assert runtime.providers is not None
            assert isinstance(runtime.providers, ProviderRegistry)
        finally:
            runtime.close()

    def test_run_with_custom_provider_factory(self):
        """测试使用自定义Provider工厂"""
        custom_providers_called = []

        def custom_provider_factory():
            custom_providers_called.append(True)
            return ProviderRegistry(providers={})

        app = (
            Bootstrap()
            .with_logging(NoOpStrategy())
            .with_provider_factory(custom_provider_factory)
            .build()
        )

        runtime = app.run()

        try:
            assert len(custom_providers_called) == 1
            assert runtime.providers is not None
        finally:
            runtime.close()

    def test_run_initializes_extensions(self):
        """测试运行初始化扩展系统"""
        app = Bootstrap().with_logging(NoOpStrategy()).build()
        runtime = app.run()

        try:
            assert runtime.extensions is not None
            assert isinstance(runtime.extensions, PluggyPluginManager)
        finally:
            runtime.close()

    def test_run_with_multiple_plugins(self):
        """测试使用多个插件运行"""

        # 使用实际的对象而非字符串路径
        class MockPlugin:
            def __init__(self, name):
                self.name = name

        plugin1 = MockPlugin("plugin1")
        plugin2 = MockPlugin("plugin2")

        app = (
            Bootstrap()
            .with_logging(NoOpStrategy())
            .with_plugin(plugin1)
            .with_plugin(plugin2)
            .build()
        )

        runtime = app.run()

        try:
            assert runtime.extensions is not None
            # 插件已被注册到扩展管理器
        finally:
            runtime.close()


class TestBootstrapIntegration:
    """集成测试：完整的Bootstrap流程"""

    def setup_method(self):
        """每个测试前清理"""
        clear_settings("default")
        clear_settings("integration_test")

    def teardown_method(self):
        """每个测试后清理"""
        clear_settings("default")
        clear_settings("integration_test")

    def test_complete_bootstrap_flow(self):
        """测试完整的Bootstrap流程"""
        # 准备配置
        config_data = {
            "app_name": "IntegrationTest",
            "app_env": "test",
            "custom_field": "integration_value",
        }
        sources = [DictSource(config_data)]

        # 构建并运行
        runtime = (
            Bootstrap()
            .with_settings(CustomSettings, namespace="integration_test", sources=sources)
            .with_logging(NoOpStrategy())
            .build()
            .run()
        )

        try:
            # 验证RuntimeContext
            assert isinstance(runtime, RuntimeContext)

            # 验证Settings
            assert isinstance(runtime.settings, CustomSettings)
            assert runtime.settings.app_name == "IntegrationTest"
            assert runtime.settings.app_env == "test"
            assert runtime.settings.custom_field == "integration_value"

            # 验证Logger
            assert runtime.logger is not None

            # 验证Providers
            assert runtime.providers is not None

            # 验证Extensions
            assert runtime.extensions is not None

        finally:
            runtime.close()

    def test_bootstrap_with_minimal_config(self):
        """测试最小配置的Bootstrap"""
        runtime = Bootstrap().with_logging(NoOpStrategy()).build().run()

        try:
            # 使用默认配置应该也能成功运行
            assert runtime.settings is not None
            assert runtime.logger is not None
            assert runtime.providers is not None
        finally:
            runtime.close()

    def test_bootstrap_with_profile(self):
        """测试Bootstrap使用profile参数（v3.5 Phase 3）"""
        # 创建临时.env.dev文件
        import os
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmpdir:
            # 保存当前目录
            original_cwd = os.getcwd()
            try:
                # 切换到临时目录
                os.chdir(tmpdir)

                # 创建.env.dev文件
                env_dev_path = Path(tmpdir) / ".env.dev"
                env_dev_path.write_text("APP_NAME=DevApp\nAPP_ENV=dev")

                # 使用profile="dev"启动
                runtime = (
                    Bootstrap()
                    .with_settings(FrameworkSettings, namespace="profile_test", profile="dev")
                    .with_logging(NoOpStrategy())
                    .build()
                    .run()
                )

                try:
                    # 验证加载了.env.dev的配置
                    assert runtime.settings.app_name == "DevApp"
                    assert runtime.settings.app_env == "dev"
                finally:
                    runtime.close()
                    clear_settings("profile_test")

            finally:
                # 恢复原目录
                os.chdir(original_cwd)
