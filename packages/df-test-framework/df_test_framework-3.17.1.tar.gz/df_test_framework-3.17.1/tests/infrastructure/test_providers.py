"""
测试Provider体系

验证SingletonProvider的线程安全性、生命周期管理和ProviderRegistry的功能。

v3.16.0: Providers 已迁移到 bootstrap/ (Layer 4)
"""

import threading
from dataclasses import dataclass

import pytest

from df_test_framework.bootstrap import (
    ProviderRegistry,
    SingletonProvider,
)


class Counter:
    """简单的计数器类，用于验证单例"""

    _instance_count = 0

    def __init__(self):
        Counter._instance_count += 1
        self.id = Counter._instance_count
        self.closed = False

    def close(self):
        self.closed = True

    @classmethod
    def reset_count(cls):
        cls._instance_count = 0


@dataclass
class MockRuntime:
    """模拟RuntimeContext"""

    settings: object = None


class TestSingletonProvider:
    """测试SingletonProvider"""

    def setup_method(self):
        """每个测试前重置计数器"""
        Counter.reset_count()

    def test_singleton_returns_same_instance(self):
        """测试单例返回相同的实例"""
        provider = SingletonProvider(lambda ctx: Counter())
        runtime = MockRuntime()

        # 多次调用应该返回同一个实例
        instance1 = provider.get(runtime)
        instance2 = provider.get(runtime)
        instance3 = provider.get(runtime)

        assert instance1 is instance2
        assert instance2 is instance3
        assert instance1.id == 1
        assert Counter._instance_count == 1, "应该只创建一个实例"

    def test_singleton_thread_safety(self):
        """测试SingletonProvider在多线程下的线程安全性（关键测试）"""
        provider = SingletonProvider(lambda ctx: Counter())
        runtime = MockRuntime()
        instances = []
        exceptions = []

        def worker():
            try:
                instance = provider.get(runtime)
                instances.append(instance)
            except Exception as e:
                exceptions.append(e)

        # 启动20个线程同时访问
        threads = [threading.Thread(target=worker) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # 验证没有异常
        assert len(exceptions) == 0, f"不应该有异常: {exceptions}"

        # 验证所有线程获取的是同一个实例
        assert len(instances) == 20
        unique_instances = set(id(inst) for inst in instances)
        assert len(unique_instances) == 1, f"应该只有一个实例，但有{len(unique_instances)}个"

        # 验证只创建了一个Counter实例
        assert Counter._instance_count == 1, (
            f"应该只创建1个实例，但创建了{Counter._instance_count}个"
        )

        # 验证所有实例的id都是1
        for inst in instances:
            assert inst.id == 1

    def test_singleton_reset(self):
        """测试reset方法可以重置单例"""
        provider = SingletonProvider(lambda ctx: Counter())
        runtime = MockRuntime()

        # 获取第一个实例
        instance1 = provider.get(runtime)
        assert instance1.id == 1
        assert not instance1.closed

        # 重置
        provider.reset()

        # 验证实例已被关闭
        assert instance1.closed

        # 再次获取应该创建新实例
        instance2 = provider.get(runtime)
        assert instance2.id == 2
        assert instance1 is not instance2

    def test_singleton_shutdown(self):
        """测试shutdown方法关闭并释放资源"""
        provider = SingletonProvider(lambda ctx: Counter())
        runtime = MockRuntime()

        # 获取实例
        instance = provider.get(runtime)
        assert not instance.closed

        # 关闭
        provider.shutdown()

        # 验证实例已被关闭
        assert instance.closed

        # 再次获取应该创建新实例
        instance2 = provider.get(runtime)
        assert instance2.id == 2
        assert not instance2.closed

    def test_singleton_with_factory_using_context(self):
        """测试工厂函数使用context"""

        class ConfigurableService:
            def __init__(self, config):
                self.config = config

        @dataclass
        class RuntimeWithSettings:
            settings: object

        @dataclass
        class Settings:
            value: str

        settings = Settings(value="test_value")
        runtime = RuntimeWithSettings(settings=settings)

        provider = SingletonProvider(lambda ctx: ConfigurableService(ctx.settings.value))

        service = provider.get(runtime)
        assert service.config == "test_value"

    def test_singleton_provider_with_exception_in_factory(self):
        """测试工厂函数抛出异常"""

        def failing_factory(ctx):
            raise ValueError("Factory failed")

        provider = SingletonProvider(failing_factory)
        runtime = MockRuntime()

        with pytest.raises(ValueError, match="Factory failed"):
            provider.get(runtime)

        # 再次调用应该再次抛出异常（因为实例未成功创建）
        with pytest.raises(ValueError, match="Factory failed"):
            provider.get(runtime)


class TestProviderRegistry:
    """测试ProviderRegistry"""

    def setup_method(self):
        """每个测试前重置计数器"""
        Counter.reset_count()

    def test_register_and_get_provider(self):
        """测试注册和获取Provider"""
        registry = ProviderRegistry(providers={})
        runtime = MockRuntime()

        # 注册Provider
        provider = SingletonProvider(lambda ctx: Counter())
        registry.register("counter", provider)

        # 获取资源
        instance1 = registry.get("counter", runtime)
        instance2 = registry.get("counter", runtime)

        assert instance1 is instance2
        assert instance1.id == 1

    def test_get_nonexistent_provider_raises_error(self):
        """测试获取不存在的Provider抛出异常"""
        registry = ProviderRegistry(providers={})
        runtime = MockRuntime()

        with pytest.raises(KeyError, match="Provider 'nonexistent' not registered"):
            registry.get("nonexistent", runtime)

    def test_extend_providers(self):
        """测试扩展Providers"""
        registry = ProviderRegistry(providers={})
        runtime = MockRuntime()

        # 初始注册
        registry.register("service1", SingletonProvider(lambda ctx: Counter()))

        # 扩展
        new_providers = {
            "service2": SingletonProvider(lambda ctx: Counter()),
            "service3": SingletonProvider(lambda ctx: Counter()),
        }
        registry.extend(new_providers)

        # 验证所有Provider都可用
        s1 = registry.get("service1", runtime)
        s2 = registry.get("service2", runtime)
        s3 = registry.get("service3", runtime)

        assert s1.id == 1
        assert s2.id == 2
        assert s3.id == 3

    def test_shutdown_all_providers(self):
        """测试关闭所有Providers"""
        Counter.reset_count()
        registry = ProviderRegistry(providers={})
        runtime = MockRuntime()

        # 注册多个Providers
        registry.register("service1", SingletonProvider(lambda ctx: Counter()))
        registry.register("service2", SingletonProvider(lambda ctx: Counter()))

        # 获取实例
        s1 = registry.get("service1", runtime)
        s2 = registry.get("service2", runtime)

        assert not s1.closed
        assert not s2.closed

        # 关闭所有
        registry.shutdown()

        # 验证所有实例都已关闭
        assert s1.closed
        assert s2.closed
