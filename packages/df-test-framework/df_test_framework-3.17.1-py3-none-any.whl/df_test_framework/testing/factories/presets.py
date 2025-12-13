"""预置数据工厂

提供常用的测试数据工厂，开箱即用

核心工厂:
- UserFactory: 用户数据
- OrderFactory: 订单数据
- ProductFactory: 商品数据
- AddressFactory: 地址数据
- PaymentFactory: 支付数据

使用示例:
    >>> from df_test_framework.testing.factories import UserFactory, OrderFactory
    >>>
    >>> # 生成单个用户
    >>> user = UserFactory.build()
    >>> print(user)  # {'id': 1, 'username': 'user_1', 'email': 'user_1@example.com', ...}
    >>>
    >>> # 批量生成
    >>> users = UserFactory.build_batch(10)
    >>>
    >>> # 自定义覆盖
    >>> admin = UserFactory.build(role='admin', is_superuser=True)

v3.10.0 新增 - P2.2 测试数据工具增强
"""

from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any
from uuid import uuid4

from .base import FAKER_AVAILABLE, Factory, FakerAttribute, LazyAttribute, Sequence

# 尝试导入 Faker
if FAKER_AVAILABLE:
    from faker import Faker

    _faker = Faker(locale="zh_CN")
else:
    _faker = None


def _random_choice(choices: list[Any]) -> Any:
    """随机选择（不依赖faker）"""
    import random

    return random.choice(choices)


def _random_decimal(min_val: float = 0.01, max_val: float = 9999.99, decimals: int = 2) -> Decimal:
    """生成随机金额"""
    import random

    value = random.uniform(min_val, max_val)
    return Decimal(str(round(value, decimals)))


def _random_date(start_days: int = -365, end_days: int = 0) -> datetime:
    """生成随机日期"""
    import random

    days = random.randint(start_days, end_days)
    return datetime.now() + timedelta(days=days)


class UserFactory(Factory):
    """用户数据工厂

    生成用户相关测试数据

    字段说明:
        id: 自增ID
        user_id: UUID格式用户ID
        username: 用户名 (user_1, user_2, ...)
        email: 邮箱 (基于username生成)
        phone: 手机号 (Faker生成)
        name: 真实姓名 (Faker生成)
        password: 密码哈希
        avatar: 头像URL
        gender: 性别 (male/female/unknown)
        age: 年龄 (18-60)
        status: 状态 (active/inactive/banned)
        role: 角色 (user/admin/vip)
        is_verified: 是否验证
        created_at: 创建时间
        updated_at: 更新时间

    示例:
        >>> user = UserFactory.build()
        >>> admin = UserFactory.build(role='admin', is_superuser=True)
        >>> users = UserFactory.build_batch(100)
    """

    id = Sequence()
    user_id = LazyAttribute(lambda _: str(uuid4()))
    username = Sequence(lambda n: f"user_{n}")
    email = LazyAttribute(lambda obj: f"{obj.username}@example.com")

    # Faker字段（如果可用）
    if FAKER_AVAILABLE:
        phone = FakerAttribute("phone_number")
        name = FakerAttribute("name")
    else:
        phone = Sequence(lambda n: f"138{str(n).zfill(8)}")
        name = Sequence(lambda n: f"测试用户{n}")

    password = "hashed_password_placeholder"
    avatar = LazyAttribute(lambda obj: f"https://avatar.example.com/{obj.username}.png")
    gender = LazyAttribute(lambda _: _random_choice(["male", "female", "unknown"]))
    age = LazyAttribute(lambda _: _random_choice(range(18, 61)))
    status = "active"
    role = "user"
    is_verified = True
    is_superuser = False
    created_at = LazyAttribute(lambda _: datetime.now())
    updated_at = LazyAttribute(lambda obj: obj.created_at)


class OrderFactory(Factory):
    """订单数据工厂

    生成订单相关测试数据

    字段说明:
        id: 自增ID
        order_no: 订单号 (ORD-20251125-000001)
        user_id: 用户ID
        status: 订单状态 (pending/paid/shipped/completed/cancelled)
        total_amount: 订单总金额
        discount_amount: 折扣金额
        payment_amount: 实付金额
        quantity: 商品数量
        shipping_fee: 运费
        payment_method: 支付方式
        shipping_address: 收货地址
        remark: 备注
        created_at: 创建时间
        paid_at: 支付时间
        shipped_at: 发货时间
        completed_at: 完成时间

    示例:
        >>> order = OrderFactory.build()
        >>> paid_order = OrderFactory.build(status='paid', paid_at=datetime.now())
        >>> orders = OrderFactory.build_batch(50)
    """

    id = Sequence()
    order_no = Sequence(lambda n: f"ORD-{datetime.now().strftime('%Y%m%d')}-{str(n).zfill(6)}")
    user_id = LazyAttribute(lambda _: str(uuid4()))
    status = "pending"
    total_amount = LazyAttribute(lambda _: _random_decimal(10.00, 5000.00))
    discount_amount = LazyAttribute(lambda _: _random_decimal(0, 100.00))
    payment_amount = LazyAttribute(lambda obj: obj.total_amount - obj.discount_amount)
    quantity = LazyAttribute(lambda _: _random_choice(range(1, 11)))
    shipping_fee = LazyAttribute(lambda _: _random_decimal(0, 20.00))
    payment_method = LazyAttribute(lambda _: _random_choice(["alipay", "wechat", "card", "cash"]))

    if FAKER_AVAILABLE:
        shipping_address = FakerAttribute("address")
    else:
        shipping_address = Sequence(lambda n: f"测试地址{n}")

    remark = ""
    created_at = LazyAttribute(lambda _: datetime.now())
    paid_at = None
    shipped_at = None
    completed_at = None


class ProductFactory(Factory):
    """商品数据工厂

    生成商品相关测试数据

    字段说明:
        id: 自增ID
        product_id: 商品ID (UUID)
        sku: SKU编码
        name: 商品名称
        description: 商品描述
        category: 商品分类
        price: 原价
        sale_price: 售价
        cost_price: 成本价
        stock: 库存
        sold_count: 销量
        status: 状态 (on_sale/off_sale/sold_out)
        weight: 重量(克)
        images: 图片列表
        tags: 标签列表
        created_at: 创建时间

    示例:
        >>> product = ProductFactory.build()
        >>> expensive = ProductFactory.build(price=Decimal('9999.00'))
    """

    id = Sequence()
    product_id = LazyAttribute(lambda _: str(uuid4()))
    sku = Sequence(lambda n: f"SKU-{str(n).zfill(8)}")

    if FAKER_AVAILABLE:
        name = FakerAttribute("word")
        description = FakerAttribute("sentence")
    else:
        name = Sequence(lambda n: f"商品{n}")
        description = Sequence(lambda n: f"这是商品{n}的描述")

    category = LazyAttribute(
        lambda _: _random_choice(["electronics", "clothing", "food", "books", "home"])
    )
    price = LazyAttribute(lambda _: _random_decimal(10.00, 2000.00))
    sale_price = LazyAttribute(lambda obj: obj.price * Decimal("0.9"))
    cost_price = LazyAttribute(lambda obj: obj.price * Decimal("0.5"))
    stock = LazyAttribute(lambda _: _random_choice(range(0, 1001)))
    sold_count = LazyAttribute(lambda _: _random_choice(range(0, 10001)))
    status = "on_sale"
    weight = LazyAttribute(lambda _: _random_choice(range(100, 5001)))
    images = LazyAttribute(
        lambda obj: [f"https://img.example.com/{obj.sku}/{i}.jpg" for i in range(3)]
    )
    tags = LazyAttribute(
        lambda _: _random_choice([["热销", "推荐"], ["新品"], ["特价", "限时"], []])
    )
    created_at = LazyAttribute(lambda _: datetime.now())


class AddressFactory(Factory):
    """地址数据工厂

    生成收货地址相关测试数据

    字段说明:
        id: 自增ID
        user_id: 用户ID
        name: 收货人姓名
        phone: 收货人电话
        province: 省份
        city: 城市
        district: 区县
        street: 街道地址
        postal_code: 邮编
        is_default: 是否默认地址
        tag: 标签 (家/公司/学校)

    示例:
        >>> addr = AddressFactory.build()
        >>> default_addr = AddressFactory.build(is_default=True)
    """

    id = Sequence()
    user_id = LazyAttribute(lambda _: str(uuid4()))

    if FAKER_AVAILABLE:
        name = FakerAttribute("name")
        phone = FakerAttribute("phone_number")
        province = FakerAttribute("province")
        city = FakerAttribute("city")
        district = FakerAttribute("district")
        street = FakerAttribute("street_address")
        postal_code = FakerAttribute("postcode")
    else:
        name = Sequence(lambda n: f"收货人{n}")
        phone = Sequence(lambda n: f"139{str(n).zfill(8)}")
        province = "广东省"
        city = "深圳市"
        district = "南山区"
        street = Sequence(lambda n: f"科技园{n}号")
        postal_code = "518000"

    is_default = False
    tag = LazyAttribute(lambda _: _random_choice(["家", "公司", "学校", ""]))


class PaymentFactory(Factory):
    """支付数据工厂

    生成支付相关测试数据

    字段说明:
        id: 自增ID
        payment_no: 支付单号
        order_no: 关联订单号
        user_id: 用户ID
        amount: 支付金额
        method: 支付方式
        status: 支付状态 (pending/success/failed/refunded)
        channel: 支付渠道
        transaction_id: 第三方交易号
        paid_at: 支付时间
        created_at: 创建时间
        metadata: 扩展数据

    示例:
        >>> payment = PaymentFactory.build()
        >>> success_payment = PaymentFactory.build(status='success', paid_at=datetime.now())
    """

    id = Sequence()
    payment_no = Sequence(lambda n: f"PAY-{datetime.now().strftime('%Y%m%d')}-{str(n).zfill(6)}")
    order_no = Sequence(lambda n: f"ORD-{datetime.now().strftime('%Y%m%d')}-{str(n).zfill(6)}")
    user_id = LazyAttribute(lambda _: str(uuid4()))
    amount = LazyAttribute(lambda _: _random_decimal(1.00, 10000.00))
    method = LazyAttribute(lambda _: _random_choice(["alipay", "wechat", "unionpay", "card"]))
    status = "pending"
    channel = LazyAttribute(lambda obj: f"{obj.method}_app")
    transaction_id = LazyAttribute(lambda _: f"TXN{uuid4().hex[:16].upper()}")
    paid_at = None
    created_at = LazyAttribute(lambda _: datetime.now())
    metadata = LazyAttribute(lambda _: {})


class CardFactory(Factory):
    """卡券数据工厂

    生成卡券相关测试数据（礼品卡、优惠券等）

    字段说明:
        id: 自增ID
        card_no: 卡号
        card_type: 卡类型 (gift_card/coupon/voucher)
        face_value: 面值
        balance: 余额
        status: 状态 (inactive/active/used/expired)
        user_id: 绑定用户
        expire_at: 过期时间
        created_at: 创建时间
        activated_at: 激活时间
        used_at: 使用时间

    示例:
        >>> card = CardFactory.build()
        >>> gift_card = CardFactory.build(card_type='gift_card', face_value=Decimal('100.00'))
    """

    id = Sequence()
    card_no = Sequence(lambda n: f"CARD{str(n).zfill(12)}")
    card_type = "gift_card"
    face_value = LazyAttribute(
        lambda _: _random_choice(
            [Decimal("50.00"), Decimal("100.00"), Decimal("200.00"), Decimal("500.00")]
        )
    )
    balance = LazyAttribute(lambda obj: obj.face_value)
    status = "inactive"
    user_id = None
    expire_at = LazyAttribute(lambda _: datetime.now() + timedelta(days=365))
    created_at = LazyAttribute(lambda _: datetime.now())
    activated_at = None
    used_at = None


class ApiResponseFactory(Factory):
    """API响应数据工厂

    生成标准API响应格式测试数据

    字段说明:
        code: 业务码
        message: 消息
        data: 数据体
        timestamp: 时间戳
        request_id: 请求ID

    示例:
        >>> resp = ApiResponseFactory.build()
        >>> error_resp = ApiResponseFactory.build(code=400, message='参数错误', data=None)
    """

    code = 0
    message = "success"
    data = LazyAttribute(lambda _: {})
    timestamp = LazyAttribute(lambda _: int(datetime.now().timestamp() * 1000))
    request_id = LazyAttribute(lambda _: str(uuid4()))


class PaginationFactory(Factory):
    """分页数据工厂

    生成分页响应测试数据

    字段说明:
        items: 数据列表
        total: 总条数
        page: 当前页
        page_size: 每页条数
        total_pages: 总页数
        has_next: 是否有下一页
        has_prev: 是否有上一页

    示例:
        >>> page = PaginationFactory.build(total=100, page=1, page_size=10)
    """

    items = LazyAttribute(lambda _: [])
    total = 0
    page = 1
    page_size = 20
    total_pages = LazyAttribute(
        lambda obj: (obj.total + obj.page_size - 1) // obj.page_size if obj.page_size > 0 else 0
    )
    has_next = LazyAttribute(lambda obj: obj.page < obj.total_pages)
    has_prev = LazyAttribute(lambda obj: obj.page > 1)


__all__ = [
    "UserFactory",
    "OrderFactory",
    "ProductFactory",
    "AddressFactory",
    "PaymentFactory",
    "CardFactory",
    "ApiResponseFactory",
    "PaginationFactory",
]
