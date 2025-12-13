"""
测试Config管理器

验证configure_settings、get_settings、create_settings和clear_settings的功能。
"""

import pytest

from df_test_framework.infrastructure.config import (
    DictSource,
    FrameworkSettings,
    SettingsAlreadyConfiguredError,
    SettingsNotConfiguredError,
    clear_settings,
    configure_settings,
    create_settings,
    get_settings,
)


class CustomSettings(FrameworkSettings):
    """自定义配置类用于测试（Pydantic v2模型）"""

    custom_field: str = "default"
    custom_number: int = 0


class TestConfigureSettings:
    """测试configure_settings函数"""

    def setup_method(self):
        """每个测试前清理"""
        clear_settings("default")
        clear_settings("test_namespace")
        clear_settings("custom_namespace")

    def teardown_method(self):
        """每个测试后清理"""
        clear_settings("default")
        clear_settings("test_namespace")
        clear_settings("custom_namespace")

    def test_configure_default_namespace(self):
        """测试配置默认命名空间"""
        configure_settings(FrameworkSettings)

        # 应该不抛出异常，说明配置成功
        settings = get_settings()
        assert isinstance(settings, FrameworkSettings)

    def test_configure_custom_namespace(self):
        """测试配置自定义命名空间"""
        configure_settings(FrameworkSettings, namespace="custom_namespace")

        settings = get_settings(namespace="custom_namespace")
        assert isinstance(settings, FrameworkSettings)

    def test_configure_with_dict_source(self):
        """测试使用DictSource配置"""
        sources = [DictSource({"app_name": "TestApp", "app_env": "test"})]

        configure_settings(
            FrameworkSettings,
            namespace="test_namespace",
            sources=sources,
        )

        settings = get_settings(namespace="test_namespace")
        assert settings.app_name == "TestApp"
        assert settings.app_env == "test"

    def test_configure_with_cache_enabled(self):
        """测试cache_enabled=True"""
        sources = [DictSource({"app_name": "CachedApp"})]

        configure_settings(
            FrameworkSettings,
            namespace="cached",
            sources=sources,
            cache_enabled=True,
        )

        settings1 = get_settings(namespace="cached")
        settings2 = get_settings(namespace="cached")

        # 应该返回同一个实例
        assert settings1 is settings2
        clear_settings("cached")

    def test_configure_with_cache_disabled(self):
        """测试cache_enabled=False"""
        sources = [DictSource({"app_name": "UncachedApp"})]

        configure_settings(
            FrameworkSettings,
            namespace="uncached",
            sources=sources,
            cache_enabled=False,
        )

        settings1 = get_settings(namespace="uncached")
        settings2 = get_settings(namespace="uncached")

        # 应该返回不同的实例
        assert settings1 is not settings2
        # 但内容应该相同
        assert settings1.app_name == settings2.app_name
        clear_settings("uncached")

    def test_configure_already_configured_raises_error(self):
        """测试重复配置同一个命名空间抛出错误"""
        configure_settings(FrameworkSettings, namespace="duplicate")

        with pytest.raises(SettingsAlreadyConfiguredError, match="already configured"):
            configure_settings(FrameworkSettings, namespace="duplicate")

        clear_settings("duplicate")

    def test_configure_custom_settings_class(self):
        """测试配置自定义Settings类"""
        sources = [DictSource({"custom_field": "test_value", "custom_number": 42})]

        configure_settings(
            CustomSettings,
            namespace="custom",
            sources=sources,
        )

        settings = get_settings(namespace="custom")
        assert isinstance(settings, CustomSettings)
        assert settings.custom_field == "test_value"
        assert settings.custom_number == 42
        clear_settings("custom")


class TestGetSettings:
    """测试get_settings函数"""

    def setup_method(self):
        """每个测试前清理"""
        clear_settings("default")
        clear_settings("test_get")

    def teardown_method(self):
        """每个测试后清理"""
        clear_settings("default")
        clear_settings("test_get")

    def test_get_not_configured_raises_error(self):
        """测试获取未配置的命名空间抛出错误"""
        with pytest.raises(SettingsNotConfiguredError, match="No settings configured"):
            get_settings(namespace="not_exist")

    def test_get_returns_cached_instance(self):
        """测试get_settings返回缓存的实例"""
        sources = [DictSource({"app_name": "CachedApp"})]
        configure_settings(
            FrameworkSettings, namespace="test_get", sources=sources, cache_enabled=True
        )

        settings1 = get_settings(namespace="test_get")
        settings2 = get_settings(namespace="test_get")

        assert settings1 is settings2

    def test_get_with_force_reload(self):
        """测试force_reload强制重新加载"""
        sources = [DictSource({"app_name": "App1"})]
        configure_settings(FrameworkSettings, namespace="reload", sources=sources)

        settings1 = get_settings(namespace="reload")
        assert settings1.app_name == "App1"

        # 使用force_reload重新加载（虽然源数据没变，但会创建新实例）
        settings2 = get_settings(namespace="reload", force_reload=True)

        # 如果cache_enabled=True，reload后应该是新实例
        # 注意：这取决于实现细节
        assert settings2.app_name == "App1"

        clear_settings("reload")

    def test_get_default_namespace(self):
        """测试获取默认命名空间"""
        sources = [DictSource({"app_name": "DefaultApp"})]
        configure_settings(FrameworkSettings, sources=sources)

        settings = get_settings()  # 不指定namespace，默认"default"
        assert settings.app_name == "DefaultApp"


class TestCreateSettings:
    """测试create_settings函数"""

    def test_create_without_sources_uses_defaults(self):
        """测试不提供sources使用默认pipeline"""
        settings = create_settings(FrameworkSettings)

        assert isinstance(settings, FrameworkSettings)
        # 应该能成功创建（使用默认源：.env + 环境变量 + 命令行参数）

    def test_create_with_dict_source(self):
        """测试使用DictSource创建"""
        sources = [DictSource({"app_name": "CreatedApp", "app_env": "test"})]

        settings = create_settings(FrameworkSettings, sources=sources)

        assert settings.app_name == "CreatedApp"
        assert settings.app_env == "test"

    def test_create_with_overrides(self):
        """测试使用overrides创建"""
        sources = [DictSource({"app_name": "SourceApp"})]
        overrides = {"app_name": "OverriddenApp", "app_env": "prod"}

        settings = create_settings(FrameworkSettings, sources=sources, overrides=overrides)

        # overrides应该覆盖sources
        assert settings.app_name == "OverriddenApp"
        assert settings.app_env == "prod"

    def test_create_custom_settings_class(self):
        """测试创建自定义Settings类"""
        sources = [DictSource({"custom_field": "created_value", "custom_number": 99})]

        settings = create_settings(CustomSettings, sources=sources)

        assert isinstance(settings, CustomSettings)
        assert settings.custom_field == "created_value"
        assert settings.custom_number == 99

    def test_create_does_not_affect_registry(self):
        """测试create_settings不影响全局registry"""
        # 确保测试命名空间未配置
        clear_settings("test_create_ns")

        # 创建settings但不注册
        settings1 = create_settings(
            FrameworkSettings, sources=[DictSource({"app_name": "Created"})]
        )

        # 尝试获取应该失败（因为没有注册）
        with pytest.raises(SettingsNotConfiguredError):
            get_settings("test_create_ns")

        # 验证创建的settings是有效的
        assert settings1.app_name == "Created"

    def test_create_multiple_instances(self):
        """测试创建多个实例（每次都是新实例）"""
        sources = [DictSource({"app_name": "MultiApp"})]

        settings1 = create_settings(FrameworkSettings, sources=sources)
        settings2 = create_settings(FrameworkSettings, sources=sources)

        # 应该是不同的实例
        assert settings1 is not settings2
        # 但内容相同
        assert settings1.app_name == settings2.app_name


class TestClearSettings:
    """测试clear_settings函数"""

    def test_clear_removes_from_cache(self):
        """测试clear从缓存和registry中移除settings"""
        sources = [DictSource({"app_name": "ToClear"})]
        configure_settings(FrameworkSettings, namespace="clear_test", sources=sources)

        # 获取一次以缓存
        settings1 = get_settings(namespace="clear_test")
        assert settings1.app_name == "ToClear"

        # 清除缓存和registry
        clear_settings(namespace="clear_test")

        # 再次配置
        configure_settings(FrameworkSettings, namespace="clear_test", sources=sources)

        # 再次获取应该创建新实例
        settings2 = get_settings(namespace="clear_test")

        # 应该是不同的实例（因为重新配置和加载）
        assert settings1 is not settings2
        assert settings2.app_name == "ToClear"

        clear_settings("clear_test")

    def test_clear_nonexistent_namespace_does_not_raise(self):
        """测试清除不存在的命名空间不抛出异常"""
        # 应该静默成功
        clear_settings("nonexistent")

    def test_clear_default_namespace(self):
        """测试清除默认命名空间"""
        sources = [DictSource({"app_name": "Default"})]
        configure_settings(FrameworkSettings, sources=sources)

        settings1 = get_settings()  # 缓存
        clear_settings()  # 清除默认命名空间（缓存和registry）

        # 重新配置
        configure_settings(FrameworkSettings, sources=sources)

        # 再次获取应该创建新实例
        settings2 = get_settings()
        assert isinstance(settings2, FrameworkSettings)
        assert settings1 is not settings2


class TestConfigIntegration:
    """集成测试：完整的配置管理流程"""

    def setup_method(self):
        """每个测试前清理"""
        clear_settings("default")
        clear_settings("integration")

    def teardown_method(self):
        """每个测试后清理"""
        clear_settings("default")
        clear_settings("integration")

    def test_complete_config_flow(self):
        """测试完整的配置流程"""
        # 1. 配置
        sources = [
            DictSource(
                {
                    "app_name": "IntegrationApp",
                    "app_env": "test",
                    "custom_field": "integration_value",
                    "custom_number": 777,
                }
            )
        ]

        configure_settings(
            CustomSettings,
            namespace="integration",
            sources=sources,
            cache_enabled=True,
        )

        # 2. 获取（第一次）
        settings1 = get_settings(namespace="integration")
        assert isinstance(settings1, CustomSettings)
        assert settings1.app_name == "IntegrationApp"
        assert settings1.app_env == "test"
        assert settings1.custom_field == "integration_value"
        assert settings1.custom_number == 777

        # 3. 获取（第二次，应该使用缓存）
        settings2 = get_settings(namespace="integration")
        assert settings1 is settings2

        # 4. 清除（同时清除缓存和registry）
        clear_settings(namespace="integration")

        # 5. 重新配置
        configure_settings(
            CustomSettings,
            namespace="integration",
            sources=sources,
            cache_enabled=True,
        )

        # 6. 再次获取（应该是新实例）
        settings3 = get_settings(namespace="integration")
        assert settings1 is not settings3
        assert settings3.app_name == "IntegrationApp"

    def test_multiple_namespaces(self):
        """测试多个命名空间共存"""
        # 配置namespace1
        sources1 = [DictSource({"app_name": "App1"})]
        configure_settings(FrameworkSettings, namespace="ns1", sources=sources1)

        # 配置namespace2
        sources2 = [DictSource({"app_name": "App2"})]
        configure_settings(FrameworkSettings, namespace="ns2", sources=sources2)

        # 获取并验证
        settings1 = get_settings(namespace="ns1")
        settings2 = get_settings(namespace="ns2")

        assert settings1.app_name == "App1"
        assert settings2.app_name == "App2"
        assert settings1 is not settings2

        # 清理
        clear_settings("ns1")
        clear_settings("ns2")

    def test_create_vs_configure(self):
        """测试create_settings和configure_settings的区别"""
        # 确保测试命名空间未配置
        test_ns = "test_create_vs_configure"
        clear_settings(test_ns)

        # create_settings不注册
        created = create_settings(
            FrameworkSettings,
            sources=[DictSource({"app_name": "Created"})],
        )

        # 尝试获取应该失败
        with pytest.raises(SettingsNotConfiguredError):
            get_settings(test_ns)

        # configure_settings注册
        configure_settings(
            FrameworkSettings,
            namespace=test_ns,
            sources=[DictSource({"app_name": "Configured"})],
        )

        # 现在应该能获取
        configured = get_settings(test_ns)
        assert configured.app_name == "Configured"

        # 验证created仍然有效
        assert created.app_name == "Created"

        # 清理
        clear_settings(test_ns)
