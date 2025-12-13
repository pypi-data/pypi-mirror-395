"""YAML数据加载器

支持从YAML文件加载测试数据

特性:
- 支持多文档YAML
- 支持YAML锚点和引用
- 环境变量替换
- 安全加载（禁用危险标签）

使用示例:
    >>> from df_test_framework.testing.data.loaders import YAMLLoader
    >>>
    >>> # 加载单文档YAML
    >>> config = YAMLLoader.load("config.yaml")
    >>>
    >>> # 加载多文档YAML
    >>> docs = YAMLLoader.load_all("multi.yaml")
    >>>
    >>> # 加载并替换环境变量
    >>> config = YAMLLoader.load("config.yaml", expand_env=True)

v3.10.0 新增 - P2.2 测试数据工具增强
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

from .base import DataLoader

# 检查pyyaml是否可用
try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    yaml = None  # type: ignore


class YAMLLoader(DataLoader):
    """YAML数据加载器

    支持标准YAML格式，需要pyyaml库

    示例:
        >>> # config.yaml:
        >>> # database:
        >>> #   host: localhost
        >>> #   port: 3306
        >>> # redis:
        >>> #   host: localhost

        >>> config = YAMLLoader.load("config.yaml")
        >>> # {'database': {'host': 'localhost', 'port': 3306}, 'redis': {...}}
    """

    # 环境变量模式: ${VAR} 或 ${VAR:default}
    _env_pattern = re.compile(r"\$\{([^}:]+)(?::([^}]*))?\}")

    @classmethod
    def _check_yaml_available(cls):
        """检查YAML库是否可用"""
        if not YAML_AVAILABLE:
            raise ImportError("YAML功能需要pyyaml库，请安装: pip install pyyaml")

    @classmethod
    def load(
        cls,
        file_path: str | Path,
        encoding: str = "utf-8",
        expand_env: bool = False,
        safe: bool = True,
        **kwargs,
    ) -> Any:
        """从YAML文件加载数据

        Args:
            file_path: YAML文件路径
            encoding: 文件编码
            expand_env: 是否展开环境变量
            safe: 是否使用安全加载（推荐）
            **kwargs: yaml.load额外参数

        Returns:
            解析后的Python对象

        Raises:
            FileNotFoundError: 文件不存在
            yaml.YAMLError: YAML格式错误
            ImportError: 未安装pyyaml

        示例:
            >>> config = YAMLLoader.load("config.yaml")
            >>> config = YAMLLoader.load("config.yaml", expand_env=True)
        """
        cls._check_yaml_available()
        path = cls._resolve_path(file_path)

        with open(path, encoding=encoding) as f:
            content = f.read()

        # 环境变量替换
        if expand_env:
            content = cls._expand_env_vars(content)

        loader = yaml.SafeLoader if safe else yaml.FullLoader
        return yaml.load(content, Loader=loader, **kwargs)

    @classmethod
    def loads(cls, content: str, expand_env: bool = False, safe: bool = True, **kwargs) -> Any:
        """从YAML字符串解析数据

        Args:
            content: YAML字符串
            expand_env: 是否展开环境变量
            safe: 是否使用安全加载
            **kwargs: yaml.load额外参数

        Returns:
            解析后的Python对象

        示例:
            >>> data = YAMLLoader.loads("name: Alice\\nage: 25")
            >>> # {'name': 'Alice', 'age': 25}
        """
        cls._check_yaml_available()

        if expand_env:
            content = cls._expand_env_vars(content)

        loader = yaml.SafeLoader if safe else yaml.FullLoader
        return yaml.load(content, Loader=loader, **kwargs)

    @classmethod
    def load_all(
        cls,
        file_path: str | Path,
        encoding: str = "utf-8",
        expand_env: bool = False,
        safe: bool = True,
        **kwargs,
    ) -> list[Any]:
        """加载多文档YAML文件

        YAML支持在一个文件中包含多个文档，用---分隔

        Args:
            file_path: YAML文件路径
            encoding: 文件编码
            expand_env: 是否展开环境变量
            safe: 是否使用安全加载
            **kwargs: yaml.load_all额外参数

        Returns:
            文档列表

        示例:
            >>> # multi.yaml:
            >>> # ---
            >>> # name: doc1
            >>> # ---
            >>> # name: doc2

            >>> docs = YAMLLoader.load_all("multi.yaml")
            >>> # [{'name': 'doc1'}, {'name': 'doc2'}]
        """
        cls._check_yaml_available()
        path = cls._resolve_path(file_path)

        with open(path, encoding=encoding) as f:
            content = f.read()

        if expand_env:
            content = cls._expand_env_vars(content)

        loader = yaml.SafeLoader if safe else yaml.FullLoader
        return list(yaml.load_all(content, Loader=loader, **kwargs))

    @classmethod
    def _expand_env_vars(cls, content: str) -> str:
        """展开环境变量

        支持格式:
            - ${VAR}: 必须存在的环境变量
            - ${VAR:default}: 带默认值的环境变量

        Args:
            content: 原始内容

        Returns:
            替换后的内容

        示例:
            >>> # ${DB_HOST:localhost} -> 环境变量值或 "localhost"
        """

        def replace(match):
            var_name = match.group(1)
            default_value = match.group(2)

            value = os.environ.get(var_name)

            if value is not None:
                return value
            elif default_value is not None:
                return default_value
            else:
                # 环境变量不存在且无默认值，保留原样
                return match.group(0)

        return cls._env_pattern.sub(replace, content)

    @classmethod
    def save(
        cls,
        data: Any,
        file_path: str | Path,
        encoding: str = "utf-8",
        default_flow_style: bool = False,
        allow_unicode: bool = True,
        indent: int = 2,
        **kwargs,
    ) -> None:
        """保存数据到YAML文件

        Args:
            data: 要保存的数据
            file_path: 目标文件路径
            encoding: 文件编码
            default_flow_style: 是否使用流式格式
            allow_unicode: 是否允许Unicode字符
            indent: 缩进空格数
            **kwargs: yaml.dump额外参数

        示例:
            >>> YAMLLoader.save({"name": "测试"}, "output.yaml")
        """
        cls._check_yaml_available()

        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding=encoding) as f:
            yaml.dump(
                data,
                f,
                default_flow_style=default_flow_style,
                allow_unicode=allow_unicode,
                indent=indent,
                **kwargs,
            )

    @classmethod
    def merge(cls, *file_paths: str | Path, expand_env: bool = False) -> dict[str, Any]:
        """合并多个YAML文件

        后面的文件会覆盖前面文件的同名键

        Args:
            *file_paths: YAML文件路径列表
            expand_env: 是否展开环境变量

        Returns:
            合并后的字典

        示例:
            >>> # base.yaml: {a: 1, b: 2}
            >>> # override.yaml: {b: 3, c: 4}
            >>> config = YAMLLoader.merge("base.yaml", "override.yaml")
            >>> # {a: 1, b: 3, c: 4}
        """
        result: dict[str, Any] = {}

        for file_path in file_paths:
            data = cls.load(file_path, expand_env=expand_env)
            if isinstance(data, dict):
                cls._deep_merge(result, data)

        return result

    @classmethod
    def _deep_merge(cls, base: dict, override: dict) -> dict:
        """深度合并字典

        Args:
            base: 基础字典
            override: 覆盖字典

        Returns:
            合并后的字典（修改base）
        """
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                cls._deep_merge(base[key], value)
            else:
                base[key] = value

        return base


__all__ = ["YAMLLoader", "YAML_AVAILABLE"]
