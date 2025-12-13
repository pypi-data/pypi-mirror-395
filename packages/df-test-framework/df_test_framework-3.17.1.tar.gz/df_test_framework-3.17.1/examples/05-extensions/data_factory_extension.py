"""
测试数据工厂扩展示例

演示如何创建测试数据工厂扩展，快速生成测试数据。
与docs/user-guide/extensions.md中的实战示例3对应。
"""

import random
from datetime import datetime, timedelta
from typing import Any

from faker import Faker
from pydantic import Field

from df_test_framework import Bootstrap, FrameworkSettings, hookimpl
from df_test_framework.infrastructure.providers import SingletonProvider


class TestDataFactory:
    """测试数据工厂 - 使用Faker生成各种测试数据"""

    def __init__(self, locale: str = 'zh_CN'):
        """
        初始化数据工厂

        Args:
            locale: 语言环境，默认中文
        """
        self.faker = Faker(locale)
        random.seed(42)  # 固定随机种子，确保数据可重现

    # ========== 用户数据 ==========

    def create_user(self, **overrides) -> dict[str, Any]:
        """
        创建用户数据

        Args:
            **overrides: 覆盖字段

        Returns:
            用户字典
        """
        user = {
            "username": self.faker.user_name(),
            "email": self.faker.email(),
            "phone": self.faker.phone_number(),
            "name": self.faker.name(),
            "age": random.randint(18, 60),
            "gender": random.choice(["male", "female"]),
            "address": self.faker.address(),
            "city": self.faker.city(),
            "created_at": self.faker.date_time_this_year().isoformat(),
        }
        user.update(overrides)
        return user

    def create_batch_users(self, count: int) -> list[dict[str, Any]]:
        """批量创建用户"""
        return [self.create_user() for _ in range(count)]

    # ========== 订单数据 ==========

    def create_order(self, **overrides) -> dict[str, Any]:
        """
        创建订单数据

        Args:
            **overrides: 覆盖字段

        Returns:
            订单字典
        """
        order = {
            "order_no": self.faker.uuid4(),
            "user_id": random.randint(1000, 9999),
            "amount": round(random.uniform(10, 1000), 2),
            "status": random.choice(["pending", "paid", "shipped", "completed", "canceled"]),
            "product_name": self.faker.word().title(),
            "quantity": random.randint(1, 10),
            "created_at": self.faker.date_time_this_month().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
        order.update(overrides)
        return order

    def create_batch_orders(self, count: int, user_id: int = None) -> list[dict[str, Any]]:
        """批量创建订单"""
        orders = []
        for _ in range(count):
            order = self.create_order()
            if user_id:
                order["user_id"] = user_id
            orders.append(order)
        return orders

    # ========== 商品数据 ==========

    def create_product(self, **overrides) -> dict[str, Any]:
        """
        创建商品数据

        Args:
            **overrides: 覆盖字段

        Returns:
            商品字典
        """
        product = {
            "product_id": self.faker.uuid4(),
            "name": self.faker.sentence(nb_words=3),
            "description": self.faker.text(max_nb_chars=200),
            "price": round(random.uniform(9.9, 999.9), 2),
            "stock": random.randint(0, 1000),
            "category": random.choice(["电子产品", "服装", "食品", "图书", "家居"]),
            "brand": self.faker.company(),
            "created_at": self.faker.date_time_this_year().isoformat(),
        }
        product.update(overrides)
        return product

    def create_batch_products(self, count: int) -> list[dict[str, Any]]:
        """批量创建商品"""
        return [self.create_product() for _ in range(count)]

    # ========== 评论数据 ==========

    def create_comment(self, **overrides) -> dict[str, Any]:
        """创建评论数据"""
        comment = {
            "comment_id": self.faker.uuid4(),
            "user_id": random.randint(1000, 9999),
            "product_id": random.randint(1, 100),
            "content": self.faker.text(max_nb_chars=100),
            "rating": random.randint(1, 5),
            "created_at": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat(),
        }
        comment.update(overrides)
        return comment

    # ========== 支付数据 ==========

    def create_payment(self, **overrides) -> dict[str, Any]:
        """创建支付数据"""
        payment = {
            "payment_id": self.faker.uuid4(),
            "order_no": self.faker.uuid4(),
            "amount": round(random.uniform(10, 1000), 2),
            "payment_method": random.choice(["alipay", "wechat", "credit_card"]),
            "status": random.choice(["pending", "success", "failed"]),
            "transaction_id": self.faker.uuid4(),
            "paid_at": datetime.now().isoformat(),
        }
        payment.update(overrides)
        return payment

    # ========== 地址数据 ==========

    def create_address(self, **overrides) -> dict[str, Any]:
        """创建收货地址数据"""
        address = {
            "address_id": self.faker.uuid4(),
            "user_id": random.randint(1000, 9999),
            "name": self.faker.name(),
            "phone": self.faker.phone_number(),
            "province": self.faker.province(),
            "city": self.faker.city(),
            "district": self.faker.district(),
            "detail": self.faker.street_address(),
            "is_default": random.choice([True, False]),
        }
        address.update(overrides)
        return address

    # ========== 完整业务场景数据 ==========

    def create_order_with_details(self) -> dict[str, Any]:
        """
        创建完整的订单场景数据（包含用户、订单、商品、支付）

        Returns:
            完整的业务数据字典
        """
        user = self.create_user()
        products = self.create_batch_products(random.randint(1, 3))
        order = self.create_order(user_id=user.get("user_id", 1001))
        payment = self.create_payment(order_no=order["order_no"])
        address = self.create_address(user_id=user.get("user_id", 1001))

        return {
            "user": user,
            "order": order,
            "products": products,
            "payment": payment,
            "address": address,
        }

    def print_data(self, data: Any, title: str = "数据"):
        """打印数据（格式化）"""
        print(f"\n📦 {title}:")
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    print(f"   {key}: [复杂对象]")
                else:
                    print(f"   {key}: {value}")
        elif isinstance(data, list):
            print(f"   共 {len(data)} 项")
            if data and isinstance(data[0], dict):
                # 只显示第一项的键
                print(f"   字段: {', '.join(data[0].keys())}")
        else:
            print(f"   {data}")


# 数据工厂扩展类
class DataFactoryExtension:
    """数据工厂扩展"""

    @hookimpl
    def df_providers(self, settings, logger):
        """注册数据工厂Provider"""
        logger.info("注册测试数据工厂...")
        return {
            "data_factory": SingletonProvider(lambda ctx: TestDataFactory())
        }

    @hookimpl
    def df_post_bootstrap(self, runtime):
        """Bootstrap完成后打印信息"""
        runtime.logger.info("✅ 测试数据工厂扩展已加载")


# 配置类
class Settings(FrameworkSettings):
    """示例配置"""
    api_base_url: str = Field(default="https://jsonplaceholder.typicode.com")


# ================== 示例代码 ==================

def example_create_single_user():
    """示例1: 创建单个用户"""
    print("\n" + "=" * 70)
    print("示例1: 创建单个用户")
    print("=" * 70)

    extension = DataFactoryExtension()
    app = Bootstrap().with_settings(Settings).with_extensions([extension]).build()
    runtime = app.run()

    factory = runtime.get("data_factory")

    # 创建默认用户
    user1 = factory.create_user()
    factory.print_data(user1, "默认用户")

    # 创建自定义用户
    user2 = factory.create_user(age=25, gender="female", city="北京")
    factory.print_data(user2, "自定义用户")


def example_create_batch_data():
    """示例2: 批量创建数据"""
    print("\n" + "=" * 70)
    print("示例2: 批量创建数据")
    print("=" * 70)

    extension = DataFactoryExtension()
    app = Bootstrap().with_settings(Settings).with_extensions([extension]).build()
    runtime = app.run()

    factory = runtime.get("data_factory")

    # 批量创建用户
    users = factory.create_batch_users(5)
    print(f"\n✅ 创建了 {len(users)} 个用户")
    for i, user in enumerate(users, 1):
        print(f"   {i}. {user['name']} ({user['email']})")

    # 批量创建订单
    orders = factory.create_batch_orders(3, user_id=1001)
    print(f"\n✅ 创建了 {len(orders)} 个订单")
    for i, order in enumerate(orders, 1):
        print(f"   {i}. 订单号: {order['order_no'][:8]}... 金额: ¥{order['amount']}")

    # 批量创建商品
    products = factory.create_batch_products(4)
    print(f"\n✅ 创建了 {len(products)} 个商品")
    for i, product in enumerate(products, 1):
        print(f"   {i}. {product['name']} - ¥{product['price']}")


def example_create_complex_scenario():
    """示例3: 创建复杂业务场景数据"""
    print("\n" + "=" * 70)
    print("示例3: 创建完整订单场景")
    print("=" * 70)

    extension = DataFactoryExtension()
    app = Bootstrap().with_settings(Settings).with_extensions([extension]).build()
    runtime = app.run()

    factory = runtime.get("data_factory")

    # 创建完整场景
    scenario = factory.create_order_with_details()

    print("\n📋 完整订单场景数据:")
    print(f"\n👤 用户: {scenario['user']['name']}")
    print(f"   邮箱: {scenario['user']['email']}")
    print(f"   电话: {scenario['user']['phone']}")

    print(f"\n📦 订单: {scenario['order']['order_no'][:16]}...")
    print(f"   金额: ¥{scenario['order']['amount']}")
    print(f"   状态: {scenario['order']['status']}")
    print(f"   商品数: {len(scenario['products'])}")

    print("\n💳 支付:")
    print(f"   方式: {scenario['payment']['payment_method']}")
    print(f"   状态: {scenario['payment']['status']}")

    print("\n📍 收货地址:")
    print(f"   {scenario['address']['province']} {scenario['address']['city']}")
    print(f"   {scenario['address']['detail']}")


def example_use_in_api_test():
    """示例4: 在API测试中使用"""
    print("\n" + "=" * 70)
    print("示例4: 在API测试中使用数据工厂")
    print("=" * 70)

    extension = DataFactoryExtension()
    app = Bootstrap().with_settings(Settings).with_extensions([extension]).build()
    runtime = app.run()

    factory = runtime.get("data_factory")
    http = runtime.http_client()

    # 创建测试用户数据
    test_user = factory.create_user(
        name="测试用户",
        email="test@example.com",
        username="testuser"
    )

    print("\n📡 使用生成的数据调用API...")
    print(f"   用户数据: {test_user['name']} ({test_user['email']})")

    # 调用API创建用户（这里使用JSONPlaceholder演示）
    try:
        response = http.post("/users", json=test_user)
        print(f"\n✅ API响应: {response.status_code}")
        if response.status_code == 201:
            print(f"   创建成功，ID: {response.json().get('id')}")
    except Exception as e:
        print(f"\n⚠️  API调用失败: {e}")
        print("   (JSONPlaceholder是只读API，POST请求会被模拟)")


def example_custom_data_types():
    """示例5: 创建各种类型的数据"""
    print("\n" + "=" * 70)
    print("示例5: 创建各种业务数据")
    print("=" * 70)

    extension = DataFactoryExtension()
    app = Bootstrap().with_settings(Settings).with_extensions([extension]).build()
    runtime = app.run()

    factory = runtime.get("data_factory")

    # 创建商品
    product = factory.create_product(name="iPhone 15 Pro", price=7999.00)
    factory.print_data(product, "商品数据")

    # 创建评论
    comment = factory.create_comment(rating=5, content="非常好用!")
    factory.print_data(comment, "评论数据")

    # 创建支付
    payment = factory.create_payment(payment_method="alipay", status="success")
    factory.print_data(payment, "支付数据")

    # 创建地址
    address = factory.create_address(is_default=True)
    factory.print_data(address, "收货地址")


if __name__ == "__main__":
    print("\n🏭 测试数据工厂扩展示例")
    print("=" * 70)
    print("演示如何使用数据工厂快速生成各种测试数据")
    print("=" * 70)

    # 运行示例
    example_create_single_user()
    example_create_batch_data()
    example_create_complex_scenario()
    example_use_in_api_test()
    example_custom_data_types()

    print("\n" + "=" * 70)
    print("✅ 所有示例执行完成!")
    print("=" * 70)
    print("\n💡 使用建议:")
    print("  1. 根据业务需求扩展create_*方法")
    print("  2. 使用**overrides灵活覆盖字段")
    print("  3. 结合Repository在测试前准备数据")
    print("  4. 使用固定随机种子确保数据可重现")
    print("  5. 可以创建create_*_with_details方法生成完整场景")
