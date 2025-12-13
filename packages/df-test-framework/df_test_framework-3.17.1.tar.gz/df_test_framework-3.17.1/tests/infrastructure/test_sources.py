"""
测试Config Sources

验证DictSource、EnvVarSource、DotenvSource和ArgSource的配置加载功能。
"""

import tempfile
from pathlib import Path

from df_test_framework.infrastructure.config.sources import (
    ArgSource,
    DictSource,
    DotenvSource,
    EnvVarSource,
    _normalise_key,
    _to_nested,
    merge_dicts,
)


class TestMergeDicts:
    """测试merge_dicts深度合并功能"""

    def test_merge_empty_dicts(self):
        """测试合并空字典"""
        result = merge_dicts({}, {})
        assert result == {}

    def test_merge_non_overlapping_keys(self):
        """测试合并无重叠键的字典"""
        base = {"a": 1, "b": 2}
        update = {"c": 3, "d": 4}

        result = merge_dicts(base, update)

        assert result == {"a": 1, "b": 2, "c": 3, "d": 4}

    def test_merge_overlapping_keys_simple(self):
        """测试合并有重叠键的简单字典"""
        base = {"a": 1, "b": 2}
        update = {"b": 99, "c": 3}

        result = merge_dicts(base, update)

        assert result == {"a": 1, "b": 99, "c": 3}

    def test_merge_nested_dicts(self):
        """测试深度合并嵌套字典"""
        base = {"app": {"name": "OldApp", "port": 8000}}
        update = {"app": {"name": "NewApp", "env": "prod"}}

        result = merge_dicts(base, update)

        assert result == {
            "app": {
                "name": "NewApp",  # 被覆盖
                "port": 8000,  # 保留
                "env": "prod",  # 新增
            }
        }

    def test_merge_deeply_nested(self):
        """测试多层嵌套字典合并"""
        base = {
            "app": {
                "database": {
                    "host": "localhost",
                    "port": 5432,
                }
            }
        }
        update = {
            "app": {
                "database": {
                    "port": 3306,  # 覆盖
                    "user": "admin",  # 新增
                }
            }
        }

        result = merge_dicts(base, update)

        assert result == {
            "app": {
                "database": {
                    "host": "localhost",
                    "port": 3306,
                    "user": "admin",
                }
            }
        }

    def test_merge_does_not_mutate_inputs(self):
        """测试merge不会修改输入字典"""
        base = {"a": 1}
        update = {"b": 2}

        merge_dicts(base, update)

        assert base == {"a": 1}
        assert update == {"b": 2}


class TestToNested:
    """测试_to_nested扁平key转嵌套字典"""

    def test_single_level_key(self):
        """测试单层key"""
        result = _to_nested("NAME", "TestApp")
        assert result == {"name": "TestApp"}

    def test_two_level_key(self):
        """测试两层key"""
        result = _to_nested("APP__NAME", "TestApp")
        assert result == {"app": {"name": "TestApp"}}

    def test_three_level_key(self):
        """测试三层key"""
        result = _to_nested("APP__DATABASE__HOST", "localhost")
        assert result == {"app": {"database": {"host": "localhost"}}}

    def test_custom_delimiter(self):
        """测试自定义分隔符"""
        result = _to_nested("APP::NAME", "TestApp", delimiter="::")
        assert result == {"app": {"name": "TestApp"}}

    def test_key_is_lowercased(self):
        """测试key会被转为小写"""
        result = _to_nested("APP__NAME__VALUE", "test")
        assert result == {"app": {"name": {"value": "test"}}}


class TestNormaliseKey:
    """测试_normalise_key标准化"""

    def test_lowercase_conversion(self):
        """测试转换为小写"""
        assert _normalise_key("NAME") == "name"
        assert _normalise_key("App_Name") == "app_name"

    def test_strip_whitespace(self):
        """测试移除空白"""
        assert _normalise_key("  name  ") == "name"
        assert _normalise_key("\tkey\n") == "key"


class TestDictSource:
    """测试DictSource"""

    def test_load_simple_dict(self):
        """测试加载简单字典"""
        source = DictSource({"app_name": "TestApp", "app_env": "test"})

        result = source.load()

        assert result == {"app_name": "TestApp", "app_env": "test"}

    def test_load_nested_dict(self):
        """测试加载嵌套字典"""
        source = DictSource(
            {
                "app": {
                    "name": "TestApp",
                    "settings": {
                        "debug": True,
                    },
                }
            }
        )

        result = source.load()

        assert result["app"]["name"] == "TestApp"
        assert result["app"]["settings"]["debug"] is True

    def test_load_returns_copy(self):
        """测试load返回副本而非原字典"""
        data = {"key": "value"}
        source = DictSource(data)

        result = source.load()
        result["key"] = "modified"

        # 原数据不应被修改
        assert data["key"] == "value"


class TestEnvVarSource:
    """测试EnvVarSource"""

    def test_load_with_prefix(self):
        """测试加载带前缀的环境变量"""
        environ = {
            "APP_NAME": "TestApp",
            "APP_ENV": "test",
            "OTHER_VAR": "ignored",  # 无APP_前缀，被忽略
        }

        source = EnvVarSource(prefix="APP_", environ=environ)
        result = source.load()

        assert result == {
            "name": "TestApp",
            "env": "test",
        }

    def test_load_nested_keys(self):
        """测试加载嵌套键（双下划线分隔）"""
        environ = {
            "APP_DATABASE__HOST": "localhost",
            "APP_DATABASE__PORT": "5432",
            "APP_CACHE__TTL": "3600",
        }

        source = EnvVarSource(prefix="APP_", environ=environ)
        result = source.load()

        assert result == {
            "database": {
                "host": "localhost",
                "port": "5432",
            },
            "cache": {
                "ttl": "3600",
            },
        }

    def test_load_with_custom_prefix(self):
        """测试自定义前缀"""
        environ = {
            "MYAPP_NAME": "TestApp",
            "APP_NAME": "ignored",  # 不同前缀
        }

        source = EnvVarSource(prefix="MYAPP_", environ=environ)
        result = source.load()

        assert result == {"name": "TestApp"}

    def test_load_respects_env_variable(self):
        """测试ENV环境变量特殊处理"""
        environ = {
            "APP_NAME": "TestApp",
            "ENV": "production",  # 特殊变量
        }

        source = EnvVarSource(prefix="APP_", environ=environ)
        result = source.load()

        assert result["name"] == "TestApp"
        assert result["env"] == "production"

    def test_load_empty_environ(self):
        """测试空环境变量"""
        source = EnvVarSource(prefix="APP_", environ={})
        result = source.load()

        assert result == {}


class TestDotenvSource:
    """测试DotenvSource"""

    def test_load_single_env_file(self):
        """测试加载单个.env文件"""
        with tempfile.TemporaryDirectory() as tmpdir:
            env_file = Path(tmpdir) / ".env"
            env_file.write_text("APP__NAME=TestApp\nAPP__ENV=test\n")

            source = DotenvSource(files=[env_file])
            result = source.load()

            assert result == {
                "app": {
                    "name": "TestApp",
                    "env": "test",
                }
            }

    def test_load_multiple_env_files(self):
        """测试加载多个.env文件（默认override=False，前面的文件优先）"""
        with tempfile.TemporaryDirectory() as tmpdir:
            env1 = Path(tmpdir) / ".env"
            env2 = Path(tmpdir) / ".env.local"

            env1.write_text("APP__NAME=BaseApp\nAPP__PORT=8000\n")
            env2.write_text("APP__NAME=LocalApp\nAPP__DEBUG=true\n")

            source = DotenvSource(files=[env1, env2])
            result = source.load()

            # override=False（默认）时，前面的文件优先
            assert result["app"]["name"] == "BaseApp"  # 保留（不被覆盖）
            assert result["app"]["port"] == "8000"  # 保留
            assert result["app"]["debug"] == "true"  # 新增

    def test_load_nonexistent_file(self):
        """测试加载不存在的文件不报错"""
        source = DotenvSource(files=[Path("/nonexistent/.env")])

        result = source.load()

        assert result == {}

    def test_load_with_nested_keys(self):
        """测试.env文件中的嵌套键"""
        with tempfile.TemporaryDirectory() as tmpdir:
            env_file = Path(tmpdir) / ".env"
            env_file.write_text("DATABASE__HOST=localhost\nDATABASE__PORT=5432\n")

            source = DotenvSource(files=[env_file])
            result = source.load()

            assert result == {
                "database": {
                    "host": "localhost",
                    "port": "5432",
                }
            }

    def test_load_skips_none_values(self):
        """测试跳过None值"""
        with tempfile.TemporaryDirectory() as tmpdir:
            env_file = Path(tmpdir) / ".env"
            # dotenv_values会将空值解析为None
            env_file.write_text("APP__NAME=TestApp\nEMPTY_KEY=\n")

            source = DotenvSource(files=[env_file])
            result = source.load()

            # EMPTY_KEY应该被跳过
            assert "empty" not in result
            assert result["app"]["name"] == "TestApp"

    def test_load_with_override_true(self):
        """测试override=True时后面的文件覆盖前面的"""
        with tempfile.TemporaryDirectory() as tmpdir:
            env1 = Path(tmpdir) / ".env"
            env2 = Path(tmpdir) / ".env.local"

            env1.write_text("APP__NAME=First\n")
            env2.write_text("APP__NAME=Second\n")

            source = DotenvSource(files=[env1, env2], override=True)
            result = source.load()

            assert result["app"]["name"] == "Second"

    def test_load_with_override_false(self):
        """测试override=False时前面的文件不被覆盖"""
        with tempfile.TemporaryDirectory() as tmpdir:
            env1 = Path(tmpdir) / ".env"
            env2 = Path(tmpdir) / ".env.local"

            env1.write_text("APP__NAME=First\n")
            env2.write_text("APP__NAME=Second\n")

            source = DotenvSource(files=[env1, env2], override=False)
            result = source.load()

            # override=False时，前面的值不被覆盖
            assert result["app"]["name"] == "First"


class TestArgSource:
    """测试ArgSource"""

    def test_load_simple_args(self):
        """测试加载简单参数"""
        argv = ["--APP_NAME=TestApp", "--APP_ENV=test"]

        source = ArgSource(argv=argv, prefix="APP_")
        result = source.load()

        assert result == {
            "name": "TestApp",
            "env": "test",
        }

    def test_load_nested_args(self):
        """测试加载嵌套参数"""
        argv = [
            "--APP_DATABASE__HOST=localhost",
            "--APP_DATABASE__PORT=5432",
        ]

        source = ArgSource(argv=argv, prefix="APP_")
        result = source.load()

        assert result == {
            "database": {
                "host": "localhost",
                "port": "5432",
            }
        }

    def test_load_ignores_non_prefixed_args(self):
        """测试忽略无前缀参数"""
        argv = [
            "--APP_NAME=TestApp",
            "--OTHER_VAR=ignored",  # 无APP_前缀
        ]

        source = ArgSource(argv=argv, prefix="APP_")
        result = source.load()

        assert result == {"name": "TestApp"}

    def test_load_ignores_args_without_double_dash(self):
        """测试忽略不以--开头的参数"""
        argv = [
            "--APP_NAME=TestApp",
            "-APP_SHORT=ignored",  # 只有单破折号
            "APP_NO_DASH=ignored",  # 无破折号
        ]

        source = ArgSource(argv=argv, prefix="APP_")
        result = source.load()

        assert result == {"name": "TestApp"}

    def test_load_ignores_args_without_equals(self):
        """测试忽略不含=的参数"""
        argv = [
            "--APP_NAME=TestApp",
            "--APP_FLAG",  # 无=号
        ]

        source = ArgSource(argv=argv, prefix="APP_")
        result = source.load()

        assert result == {"name": "TestApp"}

    def test_load_with_value_containing_equals(self):
        """测试值中包含=号"""
        argv = ["--APP_FORMULA=a=b+c"]

        source = ArgSource(argv=argv, prefix="APP_")
        result = source.load()

        # 应该只分割第一个=号
        assert result == {"formula": "a=b+c"}

    def test_load_with_custom_prefix(self):
        """测试自定义前缀"""
        argv = [
            "--MYAPP_NAME=TestApp",
            "--APP_NAME=ignored",  # 不同前缀
        ]

        source = ArgSource(argv=argv, prefix="MYAPP_")
        result = source.load()

        assert result == {"name": "TestApp"}

    def test_load_empty_argv(self):
        """测试空参数列表"""
        source = ArgSource(argv=[], prefix="APP_")
        result = source.load()

        assert result == {}


class TestSourcesIntegration:
    """集成测试：测试多个源的协作"""

    def test_merge_dict_and_env_sources(self):
        """测试合并DictSource和EnvVarSource"""
        dict_source = DictSource({"app_name": "DictApp", "app_port": 8000})

        environ = {"APP_NAME": "EnvApp", "APP_ENV": "test"}
        env_source = EnvVarSource(prefix="APP_", environ=environ)

        # DictSource
        dict_data = dict_source.load()

        # EnvVarSource (应该覆盖app_name)
        env_data = env_source.load()

        # 合并
        merged = merge_dicts(dict_data, env_data)

        assert merged["app_name"] == "DictApp"  # dict保留
        assert merged["app_port"] == 8000  # dict保留
        assert merged["name"] == "EnvApp"  # env新增
        assert merged["env"] == "test"  # env新增
