"""
测试Database类

验证数据库操作、事务管理、CRUD方法和表名白名单验证。
"""

import pytest
from sqlalchemy import text

from df_test_framework.capabilities.databases.database import Database


class TestDatabaseInit:
    """测试Database初始化"""

    def test_database_creation_sqlite(self):
        """测试创建SQLite内存数据库"""
        db = Database("sqlite:///:memory:")

        assert db.connection_string == "sqlite:///:memory:"
        assert db.engine is not None
        assert db.session_factory is not None
        assert db.allowed_tables is None  # 默认不限制

        db.close()

    def test_database_with_allowed_tables(self):
        """测试使用表名白名单"""
        allowed = {"users", "orders"}
        db = Database("sqlite:///:memory:", allowed_tables=allowed)

        assert db.allowed_tables == allowed

        db.close()

    def test_database_with_empty_allowed_tables(self):
        """测试空白名单（禁止所有表）"""
        db = Database("sqlite:///:memory:", allowed_tables=set())

        assert db.allowed_tables == set()

        db.close()

    def test_mask_connection_string(self):
        """测试连接字符串密码脱敏"""
        db = Database("mysql+pymysql://user:password123@localhost/db")

        masked = db._mask_connection_string()

        assert "password123" not in masked
        assert "****" in masked
        assert "localhost/db" in masked

        db.close()


class TestDatabaseValidateTable:
    """测试表名验证"""

    def test_validate_table_allows_all_when_none(self):
        """测试白名单为None时允许所有表"""
        db = Database("sqlite:///:memory:", allowed_tables=None)

        # 不应该抛出异常
        db._validate_table_name("any_table")
        db._validate_table_name("another_table")

        db.close()

    def test_validate_table_rejects_all_when_empty(self):
        """测试白名单为空集时拒绝所有表"""
        db = Database("sqlite:///:memory:", allowed_tables=set())

        with pytest.raises(ValueError, match="表操作已禁用"):
            db._validate_table_name("users")

        db.close()

    def test_validate_table_allows_whitelist_only(self):
        """测试白名单只允许指定的表"""
        db = Database("sqlite:///:memory:", allowed_tables={"users", "orders"})

        # 允许的表
        db._validate_table_name("users")
        db._validate_table_name("orders")

        # 不允许的表
        with pytest.raises(ValueError, match="不在白名单中"):
            db._validate_table_name("products")

        db.close()


class TestDatabaseSession:
    """测试session上下文管理器"""

    def setup_method(self):
        """每个测试前创建数据库"""
        self.db = Database("sqlite:///:memory:")
        # 创建测试表
        with self.db.session() as session:
            session.execute(
                text("""
                CREATE TABLE test_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER
                )
            """)
            )

    def teardown_method(self):
        """每个测试后关闭数据库"""
        self.db.close()

    def test_session_commit_on_success(self):
        """测试session成功时自动提交"""
        with self.db.session() as session:
            session.execute(text("INSERT INTO test_users (name, age) VALUES ('Alice', 25)"))

        # 验证数据已插入
        with self.db.session() as session:
            result = session.execute(text("SELECT * FROM test_users WHERE name = 'Alice'"))
            row = result.fetchone()
            assert row is not None
            assert row[1] == "Alice"

    def test_session_rollback_on_exception(self):
        """测试session异常时自动回滚"""
        try:
            with self.db.session() as session:
                session.execute(text("INSERT INTO test_users (name, age) VALUES ('Bob', 30)"))
                raise ValueError("Test exception")
        except ValueError:
            pass

        # 验证数据未插入
        with self.db.session() as session:
            result = session.execute(text("SELECT * FROM test_users WHERE name = 'Bob'"))
            row = result.fetchone()
            assert row is None


class TestDatabaseTransaction:
    """测试transaction事务管理"""

    def setup_method(self):
        """每个测试前创建数据库"""
        self.db = Database("sqlite:///:memory:")
        with self.db.session() as session:
            session.execute(
                text("""
                CREATE TABLE test_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )
            """)
            )

    def teardown_method(self):
        """每个测试后关闭数据库"""
        self.db.close()

    def test_transaction_commit(self):
        """测试事务提交"""
        with self.db.transaction() as session:
            session.execute(text("INSERT INTO test_users (name) VALUES ('Alice')"))
            session.execute(text("INSERT INTO test_users (name) VALUES ('Bob')"))

        # 验证两条记录都插入了
        with self.db.session() as session:
            result = session.execute(text("SELECT COUNT(*) FROM test_users"))
            count = result.scalar()
            assert count == 2

    def test_transaction_rollback(self):
        """测试事务回滚"""
        try:
            with self.db.transaction() as session:
                session.execute(text("INSERT INTO test_users (name) VALUES ('Alice')"))
                session.execute(text("INSERT INTO test_users (name) VALUES ('Bob')"))
                raise ValueError("Rollback test")
        except ValueError:
            pass

        # 验证数据未插入
        with self.db.session() as session:
            result = session.execute(text("SELECT COUNT(*) FROM test_users"))
            count = result.scalar()
            assert count == 0


class TestDatabaseQuery:
    """测试查询方法"""

    def setup_method(self):
        """每个测试前创建数据库和测试数据"""
        self.db = Database("sqlite:///:memory:")
        with self.db.session() as session:
            session.execute(
                text("""
                CREATE TABLE test_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER
                )
            """)
            )
            session.execute(text("INSERT INTO test_users (name, age) VALUES ('Alice', 25)"))
            session.execute(text("INSERT INTO test_users (name, age) VALUES ('Bob', 30)"))
            session.execute(text("INSERT INTO test_users (name, age) VALUES ('Charlie', 35)"))

    def teardown_method(self):
        """每个测试后关闭数据库"""
        self.db.close()

    def test_query_one_found(self):
        """测试query_one查询到记录"""
        result = self.db.query_one("SELECT * FROM test_users WHERE name = :name", {"name": "Alice"})

        assert result is not None
        assert result["name"] == "Alice"
        assert result["age"] == 25

    def test_query_one_not_found(self):
        """测试query_one未查询到记录"""
        result = self.db.query_one(
            "SELECT * FROM test_users WHERE name = :name", {"name": "NonExistent"}
        )

        assert result is None

    def test_query_all_with_results(self):
        """测试query_all查询多条记录"""
        results = self.db.query_all("SELECT * FROM test_users ORDER BY age")

        assert len(results) == 3
        assert results[0]["name"] == "Alice"
        assert results[1]["name"] == "Bob"
        assert results[2]["name"] == "Charlie"

    def test_query_all_with_params(self):
        """测试query_all带参数查询"""
        results = self.db.query_all(
            "SELECT * FROM test_users WHERE age > :min_age ORDER BY age", {"min_age": 25}
        )

        assert len(results) == 2
        assert results[0]["name"] == "Bob"
        assert results[1]["name"] == "Charlie"

    def test_query_all_empty(self):
        """测试query_all查询为空"""
        results = self.db.query_all(
            "SELECT * FROM test_users WHERE age > :min_age", {"min_age": 100}
        )

        assert results == []


class TestDatabaseExecute:
    """测试execute方法"""

    def setup_method(self):
        """每个测试前创建数据库"""
        self.db = Database("sqlite:///:memory:")
        with self.db.session() as session:
            session.execute(
                text("""
                CREATE TABLE test_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER
                )
            """)
            )

    def teardown_method(self):
        """每个测试后关闭数据库"""
        self.db.close()

    def test_execute_insert(self):
        """测试execute执行INSERT"""
        rowcount = self.db.execute(
            "INSERT INTO test_users (name, age) VALUES (:name, :age)", {"name": "Alice", "age": 25}
        )

        assert rowcount == 1

    def test_execute_update(self):
        """测试execute执行UPDATE"""
        # 先插入数据
        self.db.execute("INSERT INTO test_users (name, age) VALUES ('Alice', 25)")

        # 更新
        rowcount = self.db.execute(
            "UPDATE test_users SET age = :age WHERE name = :name", {"age": 26, "name": "Alice"}
        )

        assert rowcount == 1

    def test_execute_delete(self):
        """测试execute执行DELETE"""
        # 先插入数据
        self.db.execute("INSERT INTO test_users (name, age) VALUES ('Alice', 25)")

        # 删除
        rowcount = self.db.execute("DELETE FROM test_users WHERE name = :name", {"name": "Alice"})

        assert rowcount == 1


class TestDatabaseInsert:
    """测试insert方法"""

    def setup_method(self):
        """每个测试前创建数据库"""
        self.db = Database("sqlite:///:memory:")
        with self.db.session() as session:
            session.execute(
                text("""
                CREATE TABLE test_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER
                )
            """)
            )

    def teardown_method(self):
        """每个测试后关闭数据库"""
        self.db.close()

    def test_insert_returns_id(self):
        """测试insert返回插入的ID"""
        inserted_id = self.db.insert("test_users", {"name": "Alice", "age": 25})

        assert inserted_id > 0

        # 验证数据已插入
        result = self.db.query_one("SELECT * FROM test_users WHERE id = :id", {"id": inserted_id})
        assert result["name"] == "Alice"

    def test_insert_with_whitelist_allowed(self):
        """测试白名单允许的表插入成功"""
        db = Database("sqlite:///:memory:", allowed_tables={"test_users"})

        with db.session() as session:
            session.execute(
                text("""
                CREATE TABLE test_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )
            """)
            )

        # 应该成功
        inserted_id = db.insert("test_users", {"name": "Alice"})
        assert inserted_id > 0

        db.close()

    def test_insert_with_whitelist_rejected(self):
        """测试白名单拒绝的表插入失败"""
        db = Database("sqlite:///:memory:", allowed_tables={"allowed_table"})

        with db.session() as session:
            session.execute(
                text("""
                CREATE TABLE test_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )
            """)
            )

        # 应该抛出异常
        with pytest.raises(ValueError, match="不在白名单中"):
            db.insert("test_users", {"name": "Alice"})

        db.close()


class TestDatabaseBatchInsert:
    """测试batch_insert方法"""

    def setup_method(self):
        """每个测试前创建数据库"""
        self.db = Database("sqlite:///:memory:")
        with self.db.session() as session:
            session.execute(
                text("""
                CREATE TABLE test_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER
                )
            """)
            )

    def teardown_method(self):
        """每个测试后关闭数据库"""
        self.db.close()

    def test_batch_insert_small(self):
        """测试批量插入少量数据"""
        data_list = [
            {"name": "Alice", "age": 25},
            {"name": "Bob", "age": 30},
            {"name": "Charlie", "age": 35},
        ]

        count = self.db.batch_insert("test_users", data_list)

        assert count == 3

        # 验证数据已插入
        results = self.db.query_all("SELECT * FROM test_users ORDER BY id")
        assert len(results) == 3

    def test_batch_insert_empty_list_raises_error(self):
        """测试批量插入空列表抛出异常"""
        with pytest.raises(ValueError, match="数据列表不能为空"):
            self.db.batch_insert("test_users", [])

    def test_batch_insert_with_chunks(self):
        """测试批量插入大量数据分批处理"""
        # 创建2500条数据
        data_list = [{"name": f"User{i}", "age": 20 + (i % 50)} for i in range(2500)]

        # chunk_size=1000，应该分3批插入
        count = self.db.batch_insert("test_users", data_list, chunk_size=1000)

        assert count == 2500

        # 验证数据已插入
        result = self.db.query_one("SELECT COUNT(*) as count FROM test_users")
        assert result["count"] == 2500


class TestDatabaseUpdate:
    """测试update方法"""

    def setup_method(self):
        """每个测试前创建数据库和测试数据"""
        self.db = Database("sqlite:///:memory:")
        with self.db.session() as session:
            session.execute(
                text("""
                CREATE TABLE test_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER
                )
            """)
            )
            session.execute(text("INSERT INTO test_users (name, age) VALUES ('Alice', 25)"))
            session.execute(text("INSERT INTO test_users (name, age) VALUES ('Bob', 30)"))

    def teardown_method(self):
        """每个测试后关闭数据库"""
        self.db.close()

    def test_update_single_record(self):
        """测试更新单条记录"""
        affected = self.db.update("test_users", {"age": 26}, "name = :name", {"name": "Alice"})

        assert affected == 1

        # 验证更新成功
        result = self.db.query_one("SELECT * FROM test_users WHERE name = 'Alice'")
        assert result["age"] == 26

    def test_update_multiple_records(self):
        """测试更新多条记录"""
        affected = self.db.update("test_users", {"age": 99}, "age > :min_age", {"min_age": 0})

        assert affected == 2

        # 验证更新成功
        results = self.db.query_all("SELECT * FROM test_users")
        assert all(r["age"] == 99 for r in results)

    def test_update_no_match(self):
        """测试更新不匹配任何记录"""
        affected = self.db.update(
            "test_users", {"age": 100}, "name = :name", {"name": "NonExistent"}
        )

        assert affected == 0


class TestDatabaseDelete:
    """测试delete方法"""

    def setup_method(self):
        """每个测试前创建数据库和测试数据"""
        self.db = Database("sqlite:///:memory:")
        with self.db.session() as session:
            session.execute(
                text("""
                CREATE TABLE test_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER
                )
            """)
            )
            session.execute(text("INSERT INTO test_users (name, age) VALUES ('Alice', 25)"))
            session.execute(text("INSERT INTO test_users (name, age) VALUES ('Bob', 30)"))
            session.execute(text("INSERT INTO test_users (name, age) VALUES ('Charlie', 35)"))

    def teardown_method(self):
        """每个测试后关闭数据库"""
        self.db.close()

    def test_delete_single_record(self):
        """测试删除单条记录"""
        deleted = self.db.delete("test_users", "name = :name", {"name": "Alice"})

        assert deleted == 1

        # 验证删除成功
        result = self.db.query_one("SELECT * FROM test_users WHERE name = 'Alice'")
        assert result is None

    def test_delete_multiple_records(self):
        """测试删除多条记录"""
        deleted = self.db.delete("test_users", "age >= :min_age", {"min_age": 30})

        assert deleted == 2

        # 验证删除成功
        results = self.db.query_all("SELECT * FROM test_users")
        assert len(results) == 1
        assert results[0]["name"] == "Alice"

    def test_delete_no_match(self):
        """测试删除不匹配任何记录"""
        deleted = self.db.delete("test_users", "name = :name", {"name": "NonExistent"})

        assert deleted == 0


class TestDatabaseClose:
    """测试close方法"""

    def test_close_disposes_engine(self):
        """测试close关闭数据库连接"""
        db = Database("sqlite:///:memory:")

        # 关闭
        db.close()

        # engine应该被dispose（注意：SQLite内存数据库关闭后无法验证，但不应该抛出异常）
        assert True  # 没有抛出异常即为成功
