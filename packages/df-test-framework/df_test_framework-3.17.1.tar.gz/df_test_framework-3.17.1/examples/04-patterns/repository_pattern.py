"""
Repository模式示例

演示如何使用Repository模式封装数据访问逻辑。
"""


from pydantic import Field

from df_test_framework import BaseRepository, Bootstrap, FrameworkSettings


class Settings(FrameworkSettings):
    """示例配置"""
    database_url: str = Field(default="sqlite:///./example_repo.db")


class UserRepository(BaseRepository):
    """用户Repository"""

    def __init__(self, database):
        super().__init__(database, "users")

    def find_by_email(self, email: str) -> dict | None:
        """通过邮箱查找用户"""
        return self.find_one({"email": email})

    def find_active_users(self) -> list[dict]:
        """查找所有活跃用户"""
        return self.find_all({"active": True})

    def find_by_role(self, role: str) -> list[dict]:
        """通过角色查找用户"""
        return self.find_all({"role": role})


def setup_database(db):
    """设置测试数据库"""
    # 创建表
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            role TEXT,
            active INTEGER
        )
    """)

    # 清空数据
    db.execute("DELETE FROM users")

    # 插入测试数据
    test_users = [
        ("张三", "zhangsan@example.com", "admin", 1),
        ("李四", "lisi@example.com", "user", 1),
        ("王五", "wangwu@example.com", "user", 0),
    ]

    for name, email, role, active in test_users:
        db.execute("""
            INSERT INTO users (name, email, role, active)
            VALUES (?, ?, ?, ?)
        """, (name, email, role, active))


def example_basic_repository():
    """示例1: 基础Repository使用"""
    print("\n" + "="*60)
    print("示例1: 基础Repository操作")
    print("="*60)

    app = Bootstrap().with_settings(Settings).build()
    runtime = app.run()
    db = runtime.database()

    setup_database(db)

    # 创建Repository
    user_repo = UserRepository(db)

    # 查找所有用户
    all_users = user_repo.find_all()
    print(f"所有用户: {len(all_users)}个")
    for user in all_users:
        print(f"  - {user['name']} ({user['email']})")

    # 清理
    db.execute("DROP TABLE users")


def example_find_by_conditions():
    """示例2: 条件查询"""
    print("\n" + "="*60)
    print("示例2: 使用条件查询")
    print("="*60)

    app = Bootstrap().with_settings(Settings).build()
    runtime = app.run()
    db = runtime.database()

    setup_database(db)

    user_repo = UserRepository(db)

    # 通过邮箱查找
    user = user_repo.find_by_email("zhangsan@example.com")
    if user:
        print(f"通过邮箱找到: {user['name']}")

    # 查找活跃用户
    active_users = user_repo.find_active_users()
    print(f"\n活跃用户: {len(active_users)}个")
    for user in active_users:
        print(f"  - {user['name']}")

    # 通过角色查找
    admins = user_repo.find_by_role("admin")
    print(f"\n管理员: {len(admins)}个")
    for admin in admins:
        print(f"  - {admin['name']}")

    # 清理
    db.execute("DROP TABLE users")


class ProductRepository(BaseRepository):
    """产品Repository"""

    def __init__(self, database):
        super().__init__(database, "products")

    def find_in_stock(self) -> list[dict]:
        """查找有库存的产品"""
        sql = "SELECT * FROM products WHERE stock > 0"
        return self.db.execute(sql)

    def find_by_category(self, category: str) -> list[dict]:
        """通过分类查找产品"""
        return self.find_all({"category": category})

    def find_expensive_products(self, min_price: float) -> list[dict]:
        """查找价格高于指定值的产品"""
        sql = "SELECT * FROM products WHERE price >= ?"
        return self.db.execute(sql, (min_price,))


def example_custom_queries():
    """示例3: 自定义查询方法"""
    print("\n" + "="*60)
    print("示例3: 自定义查询方法")
    print("="*60)

    app = Bootstrap().with_settings(Settings).build()
    runtime = app.run()
    db = runtime.database()

    # 创建表
    db.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL,
            stock INTEGER,
            category TEXT
        )
    """)

    # 插入测试数据
    products = [
        ("笔记本电脑", 5999.00, 10, "电子"),
        ("鼠标", 99.00, 0, "电子"),
        ("键盘", 299.00, 5, "电子"),
        ("水杯", 29.00, 20, "生活"),
    ]

    for name, price, stock, category in products:
        db.execute("""
            INSERT INTO products (name, price, stock, category)
            VALUES (?, ?, ?, ?)
        """, (name, price, stock, category))

    # 创建Repository
    product_repo = ProductRepository(db)

    # 查找有库存的产品
    in_stock = product_repo.find_in_stock()
    print(f"有库存的产品: {len(in_stock)}个")

    # 查找电子产品
    electronics = product_repo.find_by_category("电子")
    print(f"\n电子产品: {len(electronics)}个")
    for product in electronics:
        print(f"  - {product['name']}: ¥{product['price']}")

    # 查找价格>=100的产品
    expensive = product_repo.find_expensive_products(100.00)
    print(f"\n价格>=100的产品: {len(expensive)}个")

    # 清理
    db.execute("DROP TABLE products")


def example_repository_pattern_benefits():
    """示例4: Repository模式的优势"""
    print("\n" + "="*60)
    print("示例4: Repository模式的优势")
    print("="*60)

    app = Bootstrap().with_settings(Settings).build()
    runtime = app.run()
    db = runtime.database()

    setup_database(db)

    user_repo = UserRepository(db)

    print("✅ 优势1: 封装数据访问逻辑")
    print("  - 业务代码不需要直接写SQL")
    print("  - 统一的查询接口")

    print("\n✅ 优势2: 代码复用")
    print("  - 相同的查询逻辑只写一次")
    print("  - 多处使用相同的方法")

    # 示例：在多处使用相同的查询
    user_repo.find_by_email("zhangsan@example.com")
    user_repo.find_by_email("zhangsan@example.com")

    print("\n✅ 优势3: 易于测试")
    print("  - Repository可以被Mock")
    print("  - 便于单元测试")

    print("\n✅ 优势4: 易于维护")
    print("  - 数据库结构变更只需修改Repository")
    print("  - 业务代码不受影响")

    # 清理
    db.execute("DROP TABLE users")


if __name__ == "__main__":
    print("\n" + "🗄️ Repository模式示例")
    print("="*60)

    # 运行所有示例
    example_basic_repository()
    example_find_by_conditions()
    example_custom_queries()
    example_repository_pattern_benefits()

    print("\n" + "="*60)
    print("✅ 所有示例执行完成!")
    print("="*60)
    print("\n💡 提示:")
    print("  - Repository模式封装数据访问逻辑")
    print("  - 继承BaseRepository创建自定义Repository")
    print("  - 提供业务相关的查询方法")
