"""测试数据管理

提供测试数据的构建和加载能力

模块:
- builders: 数据构建器 (Builder模式)
- loaders: 数据加载器 (JSON/CSV/YAML)

使用示例:
    >>> from df_test_framework.testing.data import DictBuilder, JSONLoader, CSVLoader
    >>>
    >>> # 构建数据
    >>> data = DictBuilder().set("name", "Alice").set("age", 25).build()
    >>>
    >>> # 加载数据
    >>> users = JSONLoader.load("tests/data/users.json")
    >>> products = CSVLoader.load("tests/data/products.csv")

v3.10.0新增 (P2.2):
- 数据加载器: JSONLoader, CSVLoader, YAMLLoader
"""

from .builders.base import BaseBuilder, DictBuilder
from .loaders import CSVLoader, DataLoader, JSONLoader, YAMLLoader

__all__ = [
    # 构建器
    "BaseBuilder",
    "DictBuilder",
    # 加载器 (v3.10.0)
    "DataLoader",
    "JSONLoader",
    "CSVLoader",
    "YAMLLoader",
]
