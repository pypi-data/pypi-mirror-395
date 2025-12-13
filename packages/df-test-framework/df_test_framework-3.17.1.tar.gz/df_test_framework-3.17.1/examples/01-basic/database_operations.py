"""
数据库操作示例

演示如何使用DF Test Framework的Database进行数据库操作。
"""

from pydantic import Field

from df_test_framework import Bootstrap, FrameworkSettings


class Settings(FrameworkSettings):
    """示例配置"""

    # 注意：实际使用时需要配置真实的数据库URL
    database_url: str = Field(
        default="sqlite:///./example.db",
        description="数据库连接URL"
    )


def example_execute_query():
    """示例1: 执行SQL查询"""
    print("\n" + "="*60)
    print("示例1: 执行SQL查询")
    print("="*60)

    app = Bootstrap().with_settings(Settings).build()
    runtime = app.run()
    db = runtime.database()

    # 创建测试表
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE
        )
    """)

    # 插入测试数据
    db.execute("""
        INSERT OR IGNORE INTO users (id, name, email)
        VALUES (1, '张三', 'zhangsan@example.com')
    """)

    # 查询数据
    result = db.execute("SELECT * FROM users WHERE id = 1")

    print(f"查询结果: {result}")

    # 清理
    db.execute("DROP TABLE users")


def example_parameterized_query():
    """示例2: 参数化查询（防SQL注入）"""
    print("\n" + "="*60)
    print("示例2: 参数化查询")
    print("="*60)

    app = Bootstrap().with_settings(Settings).build()
    runtime = app.run()
    db = runtime.database()

    # 创建表
    db.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            price REAL
        )
    """)

    # 使用参数化插入
    db.execute(
        "INSERT INTO products (name, price) VALUES (:name, :price)",
        {"name": "笔记本电脑", "price": 5999.00}
    )

    # 使用参数化查询
    result = db.execute(
        "SELECT * FROM products WHERE price > :min_price",
        {"min_price": 1000.00}
    )

    print(f"价格大于1000的产品: {result}")

    # 清理
    db.execute("DROP TABLE products")


def example_transaction():
    """示例3: 事务管理"""
    print("\n" + "="*60)
    print("示例3: 事务管理")
    print("="*60)

    app = Bootstrap().with_settings(Settings).build()
    runtime = app.run()
    db = runtime.database()

    # 创建表
    db.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY,
            name TEXT,
            balance REAL
        )
    """)

    try:
        # 开始事务
        db.execute("BEGIN TRANSACTION")

        # 插入账户
        db.execute(
            "INSERT INTO accounts (name, balance) VALUES (?, ?)",
            ("账户A", 1000.00)
        )

        db.execute(
            "INSERT INTO accounts (name, balance) VALUES (?, ?)",
            ("账户B", 2000.00)
        )

        # 提交事务
        db.execute("COMMIT")

        print("✅ 事务提交成功")

        # 查询结果
        result = db.execute("SELECT * FROM accounts")
        print(f"账户列表: {result}")

    except Exception as e:
        # 回滚事务
        db.execute("ROLLBACK")
        print(f"❌ 事务回滚: {e}")

    finally:
        # 清理
        db.execute("DROP TABLE accounts")


def example_batch_operations():
    """示例4: 批量操作"""
    print("\n" + "="*60)
    print("示例4: 批量操作")
    print("="*60)

    app = Bootstrap().with_settings(Settings).build()
    runtime = app.run()
    db = runtime.database()

    # 创建表
    db.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_no TEXT,
            amount REAL
        )
    """)

    # 批量插入
    orders = [
        ("ORD001", 100.00),
        ("ORD002", 200.00),
        ("ORD003", 300.00),
    ]

    for order_no, amount in orders:
        db.execute(
            "INSERT INTO orders (order_no, amount) VALUES (?, ?)",
            (order_no, amount)
        )

    # 查询统计
    result = db.execute("SELECT COUNT(*), SUM(amount) FROM orders")
    count, total = result[0]['COUNT(*)'], result[0]['SUM(amount)']

    print(f"订单数量: {count}")
    print(f"总金额: {total}")

    # 清理
    db.execute("DROP TABLE orders")


if __name__ == "__main__":
    print("\n" + "🗄️ 数据库操作示例")
    print("="*60)

    # 运行所有示例
    example_execute_query()
    example_parameterized_query()
    example_transaction()
    example_batch_operations()

    print("\n" + "="*60)
    print("✅ 所有示例执行完成!")
    print("="*60)
    print("\n💡 提示: 实际使用时请配置真实的数据库URL")
