"""数据加载器

支持从多种格式文件加载测试数据

支持格式:
- JSON: 标准JSON文件
- CSV: 逗号分隔值文件
- YAML: YAML配置文件
- Excel: Excel电子表格 (需要openpyxl)

使用示例:
    >>> from df_test_framework.testing.data.loaders import JSONLoader, CSVLoader, YAMLLoader
    >>>
    >>> # 加载JSON数据
    >>> users = JSONLoader.load("tests/data/users.json")
    >>>
    >>> # 加载CSV数据
    >>> products = CSVLoader.load("tests/data/products.csv")
    >>>
    >>> # 加载YAML数据
    >>> config = YAMLLoader.load("tests/data/config.yaml")

v3.10.0 新增 - P2.2 测试数据工具增强
"""

from .base import DataLoader
from .csv_loader import CSVLoader
from .json_loader import JSONLoader
from .yaml_loader import YAMLLoader

__all__ = [
    "DataLoader",
    "JSONLoader",
    "CSVLoader",
    "YAMLLoader",
]
