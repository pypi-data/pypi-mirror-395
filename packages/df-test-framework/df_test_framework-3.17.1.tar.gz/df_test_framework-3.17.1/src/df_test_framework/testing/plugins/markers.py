"""环境标记插件

提供基于环境的测试标记和跳过功能:
- 环境特定的测试跳过
- 环境标记自动化
- 条件测试执行
"""

import os

import pytest
from _pytest.config import Config
from _pytest.config.argparsing import Parser
from _pytest.nodes import Item

from ...core.types import Environment


def pytest_addoption(parser: Parser) -> None:
    """
    添加pytest命令行选项

    Args:
        parser: pytest参数解析器
    """
    parser.addoption(
        "--env",
        action="store",
        default=None,
        help="指定测试环境: dev/test/staging/prod",
    )


def pytest_configure(config: Config) -> None:
    """
    配置pytest环境

    Args:
        config: pytest配置对象
    """
    # 注册自定义标记
    config.addinivalue_line(
        "markers",
        "env(name): 标记测试只在指定环境运行",
    )
    config.addinivalue_line(
        "markers",
        "skip_env(name): 标记测试在指定环境跳过",
    )
    config.addinivalue_line(
        "markers",
        "require_env(*names): 标记测试只在指定的多个环境之一运行",
    )


def pytest_collection_modifyitems(config: Config, items: list[Item]) -> None:
    """
    根据环境标记修改测试集合

    Args:
        config: pytest配置对象
        items: 测试项列表
    """
    # 获取当前环境
    current_env = config.getoption("--env") or os.getenv("ENV", "test")

    # 验证环境值
    try:
        env = Environment(current_env.lower())
    except ValueError:
        pytest.exit(
            f"无效的环境值: {current_env}. 有效值: {', '.join([e.value for e in Environment])}"
        )

    for item in items:
        # 处理 @pytest.mark.env() 标记
        env_marker = item.get_closest_marker("env")
        if env_marker:
            target_env = env_marker.args[0] if env_marker.args else None
            if target_env and env.value != target_env:
                item.add_marker(pytest.mark.skip(reason=f"仅在 {target_env} 环境运行"))
                continue

        # 处理 @pytest.mark.skip_env() 标记
        skip_env_marker = item.get_closest_marker("skip_env")
        if skip_env_marker:
            skip_envs = skip_env_marker.args
            if env.value in skip_envs:
                item.add_marker(pytest.mark.skip(reason=f"在 {env.value} 环境跳过"))
                continue

        # 处理 @pytest.mark.require_env() 标记
        require_env_marker = item.get_closest_marker("require_env")
        if require_env_marker:
            required_envs = require_env_marker.args
            if env.value not in required_envs:
                item.add_marker(
                    pytest.mark.skip(reason=f"需要以下环境之一: {', '.join(required_envs)}")
                )


class EnvironmentMarker:
    """环境标记辅助类"""

    @staticmethod
    def get_current_env() -> Environment:
        """
        获取当前环境

        Returns:
            当前环境枚举值
        """
        env_name = os.getenv("ENV", "test")
        try:
            return Environment(env_name.lower())
        except ValueError:
            return Environment.TEST

    @staticmethod
    def is_env(env: str | Environment) -> bool:
        """
        检查是否为指定环境

        Args:
            env: 环境名称或枚举值

        Returns:
            是否为指定环境
        """
        current = EnvironmentMarker.get_current_env()
        if isinstance(env, str):
            return current.value == env.lower()
        return current == env

    @staticmethod
    def skip_if_env(env: str | Environment, reason: str | None = None):
        """
        如果是指定环境则跳过测试(装饰器)

        Args:
            env: 环境名称或枚举值
            reason: 跳过原因

        Example:
            @EnvironmentMarker.skip_if_env("prod", "生产环境禁止运行")
            def test_dangerous_operation():
                pass
        """
        is_target_env = EnvironmentMarker.is_env(env)
        env_name = env.value if isinstance(env, Environment) else env
        default_reason = f"在 {env_name} 环境跳过"

        return pytest.mark.skipif(is_target_env, reason=reason or default_reason)

    @staticmethod
    def skip_unless_env(env: str | Environment, reason: str | None = None):
        """
        除非是指定环境否则跳过测试(装饰器)

        Args:
            env: 环境名称或枚举值
            reason: 跳过原因

        Example:
            @EnvironmentMarker.skip_unless_env("dev", "仅在开发环境运行")
            def test_dev_only():
                pass
        """
        is_target_env = EnvironmentMarker.is_env(env)
        env_name = env.value if isinstance(env, Environment) else env
        default_reason = f"仅在 {env_name} 环境运行"

        return pytest.mark.skipif(not is_target_env, reason=reason or default_reason)

    @staticmethod
    def require_any_env(*envs: str | Environment, reason: str | None = None):
        """
        要求在指定环境之一运行(装饰器)

        Args:
            envs: 环境名称或枚举值列表
            reason: 跳过原因

        Example:
            @EnvironmentMarker.require_any_env("dev", "test")
            def test_non_prod():
                pass
        """
        current = EnvironmentMarker.get_current_env()
        env_values = [e.value if isinstance(e, Environment) else e.lower() for e in envs]
        is_valid_env = current.value in env_values
        default_reason = f"需要以下环境之一: {', '.join(env_values)}"

        return pytest.mark.skipif(not is_valid_env, reason=reason or default_reason)


# 便捷函数
def get_env() -> Environment:
    """获取当前环境"""
    return EnvironmentMarker.get_current_env()


def is_env(env: str | Environment) -> bool:
    """检查是否为指定环境"""
    return EnvironmentMarker.is_env(env)


def skip_if_prod(reason: str | None = None):
    """生产环境跳过(装饰器)"""
    return EnvironmentMarker.skip_if_env(Environment.PROD, reason)


def skip_if_dev(reason: str | None = None):
    """开发环境跳过(装饰器)"""
    return EnvironmentMarker.skip_if_env(Environment.DEV, reason)


def dev_only(reason: str | None = None):
    """仅在开发环境运行(装饰器)"""
    return EnvironmentMarker.skip_unless_env(Environment.DEV, reason)


def prod_only(reason: str | None = None):
    """仅在生产环境运行(装饰器)"""
    return EnvironmentMarker.skip_unless_env(Environment.PROD, reason)


__all__ = [
    "EnvironmentMarker",
    "get_env",
    "is_env",
    "skip_if_prod",
    "skip_if_dev",
    "dev_only",
    "prod_only",
]
