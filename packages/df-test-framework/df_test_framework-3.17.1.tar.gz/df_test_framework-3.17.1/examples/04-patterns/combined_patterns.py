"""
组合模式示例

演示如何组合使用Builder和Repository模式。
"""

from decimal import Decimal

from pydantic import Field

from df_test_framework import BaseBuilder, BaseRepository, Bootstrap, FrameworkSettings


class Settings(FrameworkSettings):
    """示例配置"""
    database_url: str = Field(default="sqlite:///./combined.db")


# ============= Builder层 =============

class ProductBuilder(BaseBuilder[dict]):
    """产品Builder"""

    def __init__(self):
        super().__init__()
        self._data = {
            "stock": 0,
            "active": True
        }

    def with_name(self, name: str):
        self._data["name"] = name
        return self

    def with_price(self, price: Decimal):
        self._data["price"] = float(price)
        return self

    def with_stock(self, stock: int):
        self._data["stock"] = stock
        return self

    def with_category(self, category: str):
        self._data["category"] = category
        return self

    def inactive(self):
        self._data["active"] = False
        return self

    def build(self) -> dict:
        return self._data.copy()


class OrderBuilder(BaseBuilder[dict]):
    """订单Builder"""

    def __init__(self):
        super().__init__()
        self._data = {
            "items": [],
            "status": "pending",
            "total": 0.00
        }

    def with_order_no(self, order_no: str):
        self._data["order_no"] = order_no
        return self

    def with_customer_id(self, customer_id: int):
        self._data["customer_id"] = customer_id
        return self

    def add_item(self, product_id: int, quantity: int, price: float):
        self._data["items"].append({
            "product_id": product_id,
            "quantity": quantity,
            "price": price
        })
        self._data["total"] += price * quantity
        return self

    def mark_paid(self):
        self._data["status"] = "paid"
        return self

    def build(self) -> dict:
        return self._data.copy()


# ============= Repository层 =============

class ProductRepository(BaseRepository):
    """产品Repository"""

    def __init__(self, database):
        super().__init__(database, "products")

    def find_active_products(self) -> list[dict]:
        """查找活跃产品"""
        return self.find_all({"active": 1})

    def find_by_category(self, category: str) -> list[dict]:
        """查找指定分类的产品"""
        return self.find_all({"category": category})

    def create(self, product_data: dict) -> int:
        """创建产品并返回ID"""
        sql = """
            INSERT INTO products (name, price, stock, category, active)
            VALUES (?, ?, ?, ?, ?)
        """
        self.db.execute(sql, (
            product_data["name"],
            product_data["price"],
            product_data["stock"],
            product_data["category"],
            1 if product_data.get("active", True) else 0
        ))

        # 获取最后插入的ID
        result = self.db.execute("SELECT last_insert_rowid() as id")
        return result[0]["id"]


class OrderRepository(BaseRepository):
    """订单Repository"""

    def __init__(self, database):
        super().__init__(database, "orders")

    def find_by_customer(self, customer_id: int) -> list[dict]:
        """查找客户的所有订单"""
        return self.find_all({"customer_id": customer_id})

    def find_paid_orders(self) -> list[dict]:
        """查找已支付的订单"""
        return self.find_all({"status": "paid"})

    def create(self, order_data: dict) -> int:
        """创建订单"""
        sql = """
            INSERT INTO orders (order_no, customer_id, total, status)
            VALUES (?, ?, ?, ?)
        """
        self.db.execute(sql, (
            order_data["order_no"],
            order_data["customer_id"],
            order_data["total"],
            order_data["status"]
        ))

        result = self.db.execute("SELECT last_insert_rowid() as id")
        return result[0]["id"]


# ============= 业务场景 =============

def setup_database(db):
    """设置数据库"""
    # 创建产品表
    db.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL,
            stock INTEGER,
            category TEXT,
            active INTEGER
        )
    """)

    # 创建订单表
    db.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_no TEXT UNIQUE,
            customer_id INTEGER,
            total REAL,
            status TEXT
        )
    """)

    # 清空数据
    db.execute("DELETE FROM products")
    db.execute("DELETE FROM orders")


def example_builder_with_repository():
    """示例1: Builder + Repository组合使用"""
    print("\n" + "="*60)
    print("示例1: Builder构建数据 + Repository保存")
    print("="*60)

    app = Bootstrap().with_settings(Settings).build()
    runtime = app.run()
    db = runtime.database()

    setup_database(db)

    # 创建Repository
    product_repo = ProductRepository(db)

    # 使用Builder构建产品数据
    product1 = (
        ProductBuilder()
        .with_name("笔记本电脑")
        .with_price(Decimal("5999.00"))
        .with_stock(10)
        .with_category("电子")
        .build()
    )

    product2 = (
        ProductBuilder()
        .with_name("鼠标")
        .with_price(Decimal("99.00"))
        .with_stock(50)
        .with_category("电子")
        .build()
    )

    # 使用Repository保存
    id1 = product_repo.create(product1)
    id2 = product_repo.create(product2)

    print(f"✅ 创建产品1: ID={id1}, {product1['name']}")
    print(f"✅ 创建产品2: ID={id2}, {product2['name']}")

    # 查询验证
    all_products = product_repo.find_all()
    print(f"\n数据库中的产品: {len(all_products)}个")

    # 清理
    db.execute("DROP TABLE products")
    db.execute("DROP TABLE orders")


def example_complete_workflow():
    """示例2: 完整的业务流程"""
    print("\n" + "="*60)
    print("示例2: 完整的电商业务流程")
    print("="*60)

    app = Bootstrap().with_settings(Settings).build()
    runtime = app.run()
    db = runtime.database()

    setup_database(db)

    product_repo = ProductRepository(db)
    order_repo = OrderRepository(db)

    # 步骤1: 创建产品
    print("\n步骤1: 创建产品")
    products = [
        ProductBuilder()
        .with_name("笔记本电脑")
        .with_price(Decimal("5999.00"))
        .with_stock(10)
        .with_category("电子")
        .build(),

        ProductBuilder()
        .with_name("鼠标")
        .with_price(Decimal("99.00"))
        .with_stock(50)
        .with_category("电子")
        .build(),
    ]

    product_ids = {}
    for product in products:
        pid = product_repo.create(product)
        product_ids[product["name"]] = pid
        print(f"  ✅ 创建产品: {product['name']}")

    # 步骤2: 查询产品
    print("\n步骤2: 查询电子产品")
    electronics = product_repo.find_by_category("电子")
    print(f"  找到 {len(electronics)} 个电子产品")

    # 步骤3: 创建订单
    print("\n步骤3: 创建订单")
    order = (
        OrderBuilder()
        .with_order_no("ORD001")
        .with_customer_id(1)
        .add_item(product_ids["笔记本电脑"], 1, 5999.00)
        .add_item(product_ids["鼠标"], 2, 99.00)
        .mark_paid()
        .build()
    )

    order_repo.create(order)
    print(f"  ✅ 创建订单: {order['order_no']}, 总金额: ¥{order['total']}")

    # 步骤4: 查询订单
    print("\n步骤4: 查询客户订单")
    customer_orders = order_repo.find_by_customer(1)
    print(f"  客户1的订单: {len(customer_orders)}个")

    # 清理
    db.execute("DROP TABLE products")
    db.execute("DROP TABLE orders")


def example_pattern_benefits():
    """示例3: 模式组合的优势"""
    print("\n" + "="*60)
    print("示例3: 模式组合的优势")
    print("="*60)

    print("\n✅ Builder模式优势:")
    print("  - 链式调用，代码清晰")
    print("  - 灵活构建复杂对象")
    print("  - 提供默认值")

    print("\n✅ Repository模式优势:")
    print("  - 封装数据访问")
    print("  - 统一查询接口")
    print("  - 易于测试和维护")

    print("\n✅ 组合使用优势:")
    print("  - Builder负责数据构建")
    print("  - Repository负责数据持久化")
    print("  - 职责清晰，易于扩展")

    # 示例代码
    print("\n示例代码:")
    print("""
    # 使用Builder构建
    product = (
        ProductBuilder()
        .with_name("产品名称")
        .with_price(Decimal("99.00"))
        .build()
    )

    # 使用Repository保存
    product_id = product_repo.create(product)

    # 使用Repository查询
    all_products = product_repo.find_all()
    """)


if __name__ == "__main__":
    print("\n" + "🔄 组合模式示例")
    print("="*60)

    # 运行所有示例
    example_builder_with_repository()
    example_complete_workflow()
    example_pattern_benefits()

    print("\n" + "="*60)
    print("✅ 所有示例执行完成!")
    print("="*60)
    print("\n💡 提示:")
    print("  - Builder模式构建数据，Repository模式访问数据")
    print("  - 职责分离，代码更清晰")
    print("  - 易于测试和维护")
