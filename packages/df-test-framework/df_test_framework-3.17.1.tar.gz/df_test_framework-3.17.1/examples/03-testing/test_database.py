"""
数据库测试示例

演示如何使用框架进行数据库测试。
"""

import pytest


@pytest.fixture(scope="module")
def test_table(database):
    """创建测试表"""
    # 创建表
    database.execute("""
        CREATE TABLE IF NOT EXISTS test_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            age INTEGER
        )
    """)

    yield

    # 清理表
    database.execute("DROP TABLE IF EXISTS test_users")


class TestDatabaseCRUD:
    """数据库CRUD操作测试"""

    def test_insert_user(self, database, test_table):
        """测试插入用户"""
        database.execute("""
            INSERT INTO test_users (name, email, age)
            VALUES (?, ?, ?)
        """, ("张三", "zhangsan@example.com", 30))

        # 验证插入
        result = database.execute(
            "SELECT * FROM test_users WHERE email = ?",
            ("zhangsan@example.com",)
        )

        assert len(result) == 1
        assert result[0]["name"] == "张三"
        assert result[0]["age"] == 30

        # 清理
        database.execute("DELETE FROM test_users WHERE email = ?", ("zhangsan@example.com",))

    def test_update_user(self, database, test_table):
        """测试更新用户"""
        # 插入测试数据
        database.execute("""
            INSERT INTO test_users (name, email, age)
            VALUES (?, ?, ?)
        """, ("李四", "lisi@example.com", 25))

        # 更新
        database.execute("""
            UPDATE test_users
            SET age = ?
            WHERE email = ?
        """, (26, "lisi@example.com"))

        # 验证更新
        result = database.execute(
            "SELECT * FROM test_users WHERE email = ?",
            ("lisi@example.com",)
        )

        assert result[0]["age"] == 26

        # 清理
        database.execute("DELETE FROM test_users WHERE email = ?", ("lisi@example.com",))

    def test_delete_user(self, database, test_table):
        """测试删除用户"""
        # 插入测试数据
        database.execute("""
            INSERT INTO test_users (name, email, age)
            VALUES (?, ?, ?)
        """, ("王五", "wangwu@example.com", 28))

        # 删除
        database.execute(
            "DELETE FROM test_users WHERE email = ?",
            ("wangwu@example.com",)
        )

        # 验证删除
        result = database.execute(
            "SELECT * FROM test_users WHERE email = ?",
            ("wangwu@example.com",)
        )

        assert len(result) == 0

    def test_query_users(self, database, test_table):
        """测试查询用户"""
        # 插入多个用户
        users = [
            ("用户1", "user1@example.com", 20),
            ("用户2", "user2@example.com", 30),
            ("用户3", "user3@example.com", 40),
        ]

        for name, email, age in users:
            database.execute("""
                INSERT INTO test_users (name, email, age)
                VALUES (?, ?, ?)
            """, (name, email, age))

        # 查询年龄大于25的用户
        result = database.execute(
            "SELECT * FROM test_users WHERE age > ?",
            (25,)
        )

        assert len(result) == 2
        assert all(user["age"] > 25 for user in result)

        # 清理
        database.execute("DELETE FROM test_users")


class TestTransaction:
    """事务测试"""

    def test_transaction_commit(self, database, test_table):
        """测试事务提交"""
        try:
            database.execute("BEGIN TRANSACTION")

            database.execute("""
                INSERT INTO test_users (name, email, age)
                VALUES (?, ?, ?)
            """, ("事务用户1", "trans1@example.com", 30))

            database.execute("COMMIT")

            # 验证提交成功
            result = database.execute(
                "SELECT * FROM test_users WHERE email = ?",
                ("trans1@example.com",)
            )

            assert len(result) == 1

        finally:
            # 清理
            database.execute("DELETE FROM test_users")

    def test_transaction_rollback(self, database, test_table):
        """测试事务回滚"""
        try:
            database.execute("BEGIN TRANSACTION")

            database.execute("""
                INSERT INTO test_users (name, email, age)
                VALUES (?, ?, ?)
            """, ("事务用户2", "trans2@example.com", 30))

            # 回滚
            database.execute("ROLLBACK")

            # 验证回滚成功
            result = database.execute(
                "SELECT * FROM test_users WHERE email = ?",
                ("trans2@example.com",)
            )

            assert len(result) == 0

        finally:
            pass


class TestParameterizedQuery:
    """参数化查询测试"""

    @pytest.mark.parametrize("name,email,age", [
        ("测试1", "test1@example.com", 20),
        ("测试2", "test2@example.com", 30),
        ("测试3", "test3@example.com", 40),
    ])
    def test_insert_multiple_users(self, database, test_table, name, email, age):
        """参数化测试：插入多个用户"""
        database.execute("""
            INSERT INTO test_users (name, email, age)
            VALUES (?, ?, ?)
        """, (name, email, age))

        result = database.execute(
            "SELECT * FROM test_users WHERE email = ?",
            (email,)
        )

        assert len(result) == 1
        assert result[0]["name"] == name
        assert result[0]["age"] == age

        # 清理
        database.execute("DELETE FROM test_users WHERE email = ?", (email,))
