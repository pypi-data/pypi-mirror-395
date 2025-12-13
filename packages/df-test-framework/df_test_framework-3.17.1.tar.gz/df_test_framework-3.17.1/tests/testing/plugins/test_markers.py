"""环境标记插件单元测试"""

import os
from unittest import mock

from df_test_framework.core.types import Environment
from df_test_framework.testing.plugins.markers import (
    EnvironmentMarker,
    dev_only,
    get_env,
    is_env,
    prod_only,
    skip_if_dev,
    skip_if_prod,
)


class TestEnvironmentMarker:
    """EnvironmentMarker 类测试"""

    def test_get_current_env_default(self):
        """测试获取默认环境"""
        with mock.patch.dict(os.environ, {}, clear=True):
            env = EnvironmentMarker.get_current_env()
            assert env == Environment.TEST

    def test_get_current_env_from_env_var(self):
        """测试从环境变量获取环境"""
        with mock.patch.dict(os.environ, {"ENV": "dev"}):
            env = EnvironmentMarker.get_current_env()
            assert env == Environment.DEV

    def test_get_current_env_invalid_fallback(self):
        """测试无效环境变量回退到 TEST"""
        with mock.patch.dict(os.environ, {"ENV": "invalid"}):
            env = EnvironmentMarker.get_current_env()
            assert env == Environment.TEST

    def test_is_env_string(self):
        """测试字符串环境比较"""
        with mock.patch.dict(os.environ, {"ENV": "dev"}):
            assert EnvironmentMarker.is_env("dev") is True
            assert EnvironmentMarker.is_env("DEV") is True
            assert EnvironmentMarker.is_env("prod") is False

    def test_is_env_enum(self):
        """测试枚举环境比较"""
        with mock.patch.dict(os.environ, {"ENV": "prod"}):
            assert EnvironmentMarker.is_env(Environment.PROD) is True
            assert EnvironmentMarker.is_env(Environment.DEV) is False


class TestEnvironmentMarkerDecorators:
    """EnvironmentMarker 装饰器测试"""

    def test_skip_if_env_matches(self):
        """测试 skip_if_env 匹配时跳过"""
        with mock.patch.dict(os.environ, {"ENV": "prod"}):
            marker = EnvironmentMarker.skip_if_env("prod")
            # 检查 marker 已创建
            assert marker is not None

    def test_skip_if_env_custom_reason(self):
        """测试 skip_if_env 自定义原因"""
        with mock.patch.dict(os.environ, {"ENV": "prod"}):
            marker = EnvironmentMarker.skip_if_env("prod", reason="生产环境禁止")
            assert marker is not None

    def test_skip_unless_env(self):
        """测试 skip_unless_env"""
        with mock.patch.dict(os.environ, {"ENV": "test"}):
            marker = EnvironmentMarker.skip_unless_env("dev")
            assert marker is not None

    def test_require_any_env_match(self):
        """测试 require_any_env 匹配"""
        with mock.patch.dict(os.environ, {"ENV": "dev"}):
            marker = EnvironmentMarker.require_any_env("dev", "test")
            assert marker is not None

    def test_require_any_env_no_match(self):
        """测试 require_any_env 不匹配"""
        with mock.patch.dict(os.environ, {"ENV": "prod"}):
            marker = EnvironmentMarker.require_any_env("dev", "test")
            assert marker is not None


class TestConvenienceFunctions:
    """便捷函数测试"""

    def test_get_env(self):
        """测试 get_env 函数"""
        with mock.patch.dict(os.environ, {"ENV": "staging"}):
            env = get_env()
            assert env == Environment.STAGING

    def test_is_env_function(self):
        """测试 is_env 函数"""
        with mock.patch.dict(os.environ, {"ENV": "test"}):
            assert is_env("test") is True
            assert is_env("prod") is False

    def test_skip_if_prod(self):
        """测试 skip_if_prod 装饰器"""
        with mock.patch.dict(os.environ, {"ENV": "prod"}):
            marker = skip_if_prod()
            assert marker is not None

    def test_skip_if_prod_custom_reason(self):
        """测试 skip_if_prod 自定义原因"""
        with mock.patch.dict(os.environ, {"ENV": "prod"}):
            marker = skip_if_prod(reason="生产环境禁止测试")
            assert marker is not None

    def test_skip_if_dev(self):
        """测试 skip_if_dev 装饰器"""
        with mock.patch.dict(os.environ, {"ENV": "dev"}):
            marker = skip_if_dev()
            assert marker is not None

    def test_dev_only(self):
        """测试 dev_only 装饰器"""
        with mock.patch.dict(os.environ, {"ENV": "dev"}):
            marker = dev_only()
            assert marker is not None

    def test_prod_only(self):
        """测试 prod_only 装饰器"""
        with mock.patch.dict(os.environ, {"ENV": "prod"}):
            marker = prod_only()
            assert marker is not None


class TestEnvironmentTypes:
    """环境类型测试"""

    def test_all_environment_values(self):
        """测试所有环境值"""
        envs = ["dev", "test", "staging", "prod"]
        for env_name in envs:
            with mock.patch.dict(os.environ, {"ENV": env_name}):
                env = get_env()
                assert env.value == env_name

    def test_case_insensitive(self):
        """测试大小写不敏感"""
        with mock.patch.dict(os.environ, {"ENV": "DEV"}):
            env = get_env()
            assert env == Environment.DEV

        with mock.patch.dict(os.environ, {"ENV": "Dev"}):
            env = get_env()
            assert env == Environment.DEV
