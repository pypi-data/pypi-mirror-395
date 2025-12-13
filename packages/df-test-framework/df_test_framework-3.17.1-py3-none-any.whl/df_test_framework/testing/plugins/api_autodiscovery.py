"""API 自动发现 pytest 插件

自动将 @api_class 装饰的类注册为 pytest fixture。
"""

import pytest


def pytest_configure(config):
    """Pytest hook: 配置阶段"""
    # 注册插件
    config.pluginmanager.register(APIAutoDiscoveryPlugin(), "api_autodiscovery")


class APIAutoDiscoveryPlugin:
    """API 自动发现插件"""

    @pytest.fixture(scope="session", autouse=False)
    def _api_registry_loaded(self):
        """确保 API 注册表已加载（内部使用）"""
        return True


def pytest_generate_tests(metafunc):
    """Pytest hook: 动态生成 fixture

    为所有 @api_class 注册的 API 类动态创建 fixture。
    """
    # 获取注册表
    from ..decorators.api_class import _api_registry

    # 检查测试函数需要哪些 fixture
    for fixture_name in metafunc.fixturenames:
        if fixture_name in _api_registry:
            # 这个 fixture 是自动注册的 API
            # pytest 会自动处理，无需额外操作
            pass


# 导出给 conftest.py 使用的辅助函数
def register_api_fixtures(config):
    """在 conftest.py 中调用，注册所有 API fixture

    Example:
        >>> # conftest.py
        >>> from df_test_framework.testing.plugins.api_autodiscovery import register_api_fixtures
        >>>
        >>> def pytest_configure(config):
        ...     register_api_fixtures(config)
    """
    from ..decorators.api_class import create_api_fixtures

    # 创建所有 fixture
    fixtures = create_api_fixtures()

    # 将 fixture 添加到模块级别
    import sys

    # 获取 conftest 模块
    for module_name, module in sys.modules.items():
        if "conftest" in module_name:
            # 添加 fixture 到 conftest
            for fixture_name, fixture_func in fixtures.items():
                setattr(module, fixture_name, fixture_func)


__all__ = [
    "pytest_configure",
    "pytest_generate_tests",
    "register_api_fixtures",
]
