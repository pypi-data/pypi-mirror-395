"""数据工厂模块

提供强大的测试数据构建能力

v3.5新增:
- Factory: 数据工厂基类
- LazyAttribute: 延迟计算属性
- Sequence: 序列生成器
- FakerAttribute: 假数据生成

v3.10.0新增 (P2.2):
- 预置工厂: UserFactory, OrderFactory, ProductFactory等
- 开箱即用的常用数据生成器

使用示例:
    >>> from df_test_framework.testing.factories import UserFactory, OrderFactory
    >>>
    >>> user = UserFactory.build()
    >>> users = UserFactory.build_batch(100)
    >>> admin = UserFactory.build(role='admin', is_superuser=True)
"""

from .base import (
    FAKER_AVAILABLE,
    Factory,
    FakerAttribute,
    LazyAttribute,
    Sequence,
    fake,
)
from .presets import (
    AddressFactory,
    ApiResponseFactory,
    CardFactory,
    OrderFactory,
    PaginationFactory,
    PaymentFactory,
    ProductFactory,
    UserFactory,
)

__all__ = [
    # 基础类
    "Factory",
    "LazyAttribute",
    "Sequence",
    "FakerAttribute",
    "fake",
    "FAKER_AVAILABLE",
    # 预置工厂 (v3.10.0)
    "UserFactory",
    "OrderFactory",
    "ProductFactory",
    "AddressFactory",
    "PaymentFactory",
    "CardFactory",
    "ApiResponseFactory",
    "PaginationFactory",
]
