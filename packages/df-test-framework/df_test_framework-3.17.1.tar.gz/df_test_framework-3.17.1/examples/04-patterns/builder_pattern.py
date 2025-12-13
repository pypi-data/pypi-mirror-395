"""
Builder模式示例

演示如何使用Builder模式构建测试数据。
"""

from decimal import Decimal

from df_test_framework import BaseBuilder, DictBuilder


def example_dict_builder():
    """示例1: 使用DictBuilder"""
    print("\n" + "="*60)
    print("示例1: 使用DictBuilder构建字典")
    print("="*60)

    # 使用链式调用构建字典
    user = (
        DictBuilder()
        .set("id", 1)
        .set("name", "张三")
        .set("age", 30)
        .set("email", "zhangsan@example.com")
        .set("active", True)
        .build()
    )

    print(f"构建的用户: {user}")
    print(f"类型: {type(user)}")


def example_nested_builder():
    """示例2: 构建嵌套结构"""
    print("\n" + "="*60)
    print("示例2: 构建嵌套数据结构")
    print("="*60)

    # 构建地址
    address = (
        DictBuilder()
        .set("street", "中山路100号")
        .set("city", "上海")
        .set("zipcode", "200000")
        .build()
    )

    # 构建包含地址的用户
    user = (
        DictBuilder()
        .set("id", 1)
        .set("name", "张三")
        .set("address", address)  # 嵌套对象
        .build()
    )

    print("用户信息:")
    print(f"  姓名: {user['name']}")
    print(f"  地址: {user['address']['city']} {user['address']['street']}")


def example_list_builder():
    """示例3: 构建列表数据"""
    print("\n" + "="*60)
    print("示例3: 构建包含列表的数据")
    print("="*60)

    # 构建带标签的文章
    article = (
        DictBuilder()
        .set("title", "测试文章")
        .set("content", "这是文章内容")
        .set("tags", ["Python", "测试", "框架"])  # 列表
        .set("views", 0)
        .build()
    )

    print(f"文章标题: {article['title']}")
    print(f"标签: {', '.join(article['tags'])}")


class UserBuilder(BaseBuilder[dict]):
    """自定义用户Builder"""

    def __init__(self):
        super().__init__()
        self._data = {
            "active": True,  # 默认值
            "role": "user"   # 默认角色
        }

    def with_id(self, user_id: int):
        """设置用户ID"""
        self._data["id"] = user_id
        return self

    def with_name(self, name: str):
        """设置用户名"""
        self._data["name"] = name
        return self

    def with_email(self, email: str):
        """设置邮箱"""
        self._data["email"] = email
        return self

    def with_age(self, age: int):
        """设置年龄"""
        self._data["age"] = age
        return self

    def as_admin(self):
        """设置为管理员"""
        self._data["role"] = "admin"
        return self

    def inactive(self):
        """设置为不活跃"""
        self._data["active"] = False
        return self

    def build(self) -> dict:
        """构建用户字典"""
        return self._data.copy()


def example_custom_builder():
    """示例4: 自定义Builder"""
    print("\n" + "="*60)
    print("示例4: 使用自定义Builder")
    print("="*60)

    # 构建普通用户
    user = (
        UserBuilder()
        .with_id(1)
        .with_name("张三")
        .with_email("zhangsan@example.com")
        .with_age(30)
        .build()
    )

    print(f"普通用户: {user}")
    print(f"  角色: {user['role']}")
    print(f"  活跃: {user['active']}")

    # 构建管理员
    admin = (
        UserBuilder()
        .with_id(2)
        .with_name("李四")
        .with_email("lisi@example.com")
        .as_admin()
        .build()
    )

    print(f"\n管理员: {admin}")
    print(f"  角色: {admin['role']}")


class OrderBuilder(BaseBuilder[dict]):
    """订单Builder"""

    def __init__(self):
        super().__init__()
        self._data = {
            "items": [],
            "status": "pending",
            "total": Decimal("0.00")
        }

    def with_order_no(self, order_no: str):
        """设置订单号"""
        self._data["order_no"] = order_no
        return self

    def with_customer(self, customer_id: int):
        """设置客户ID"""
        self._data["customer_id"] = customer_id
        return self

    def add_item(self, product: str, quantity: int, price: Decimal):
        """添加订单项"""
        self._data["items"].append({
            "product": product,
            "quantity": quantity,
            "price": price
        })
        # 更新总价
        self._data["total"] += price * quantity
        return self

    def mark_paid(self):
        """标记为已支付"""
        self._data["status"] = "paid"
        return self

    def build(self) -> dict:
        """构建订单"""
        return self._data.copy()


def example_complex_builder():
    """示例5: 复杂Builder"""
    print("\n" + "="*60)
    print("示例5: 复杂的订单Builder")
    print("="*60)

    # 构建订单
    order = (
        OrderBuilder()
        .with_order_no("ORD001")
        .with_customer(1)
        .add_item("笔记本电脑", 1, Decimal("5999.00"))
        .add_item("鼠标", 2, Decimal("99.00"))
        .add_item("键盘", 1, Decimal("299.00"))
        .mark_paid()
        .build()
    )

    print(f"订单号: {order['order_no']}")
    print(f"状态: {order['status']}")
    print("订单项:")
    for item in order["items"]:
        print(f"  - {item['product']}: {item['quantity']}个 x ¥{item['price']}")
    print(f"总价: ¥{order['total']}")


def example_builder_with_defaults():
    """示例6: 带默认值的Builder"""
    print("\n" + "="*60)
    print("示例6: 使用默认值简化构建")
    print("="*60)

    # 只设置必要字段，其他使用默认值
    user1 = (
        UserBuilder()
        .with_id(1)
        .with_name("张三")
        .with_email("zhangsan@example.com")
        .build()
    )

    print("用户1 (使用默认值):")
    print(f"  姓名: {user1['name']}")
    print(f"  角色: {user1['role']} (默认)")
    print(f"  活跃: {user1['active']} (默认)")

    # 覆盖默认值
    user2 = (
        UserBuilder()
        .with_id(2)
        .with_name("李四")
        .with_email("lisi@example.com")
        .as_admin()
        .inactive()
        .build()
    )

    print("\n用户2 (覆盖默认值):")
    print(f"  姓名: {user2['name']}")
    print(f"  角色: {user2['role']} (已修改)")
    print(f"  活跃: {user2['active']} (已修改)")


if __name__ == "__main__":
    print("\n" + "🏗️ Builder模式示例")
    print("="*60)

    # 运行所有示例
    example_dict_builder()
    example_nested_builder()
    example_list_builder()
    example_custom_builder()
    example_complex_builder()
    example_builder_with_defaults()

    print("\n" + "="*60)
    print("✅ 所有示例执行完成!")
    print("="*60)
    print("\n💡 提示:")
    print("  - Builder模式适合构建复杂对象")
    print("  - 链式调用提高代码可读性")
    print("  - 可以设置默认值简化使用")
