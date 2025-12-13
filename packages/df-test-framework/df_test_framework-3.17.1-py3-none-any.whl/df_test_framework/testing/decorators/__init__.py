"""测试装饰器

提供用于测试的装饰器，如 API 类自动注册等。
"""

from .api_class import api_class, get_api_registry, load_api_fixtures

__all__ = [
    "api_class",
    "get_api_registry",
    "load_api_fixtures",
]
