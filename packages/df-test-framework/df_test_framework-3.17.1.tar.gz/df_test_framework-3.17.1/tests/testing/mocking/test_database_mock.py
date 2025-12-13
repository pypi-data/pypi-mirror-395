"""测试数据库 Mock"""

from df_test_framework.testing.mocking import DatabaseMocker


class TestDatabaseMocker:
    """测试 DatabaseMocker"""

    def test_context_manager(self) -> None:
        """测试上下文管理器"""
        with DatabaseMocker() as db_mock:
            assert db_mock.mock_db is not None

    def test_add_query_result(self) -> None:
        """测试添加查询结果"""
        with DatabaseMocker() as db_mock:
            db_mock.add_query_result("SELECT * FROM users", [{"id": 1, "name": "Alice"}])

            result = db_mock.mock_db.query("SELECT * FROM users")
            assert result == [{"id": 1, "name": "Alice"}]

    def test_add_execute_result(self) -> None:
        """测试添加执行结果"""
        with DatabaseMocker() as db_mock:
            db_mock.add_execute_result("DELETE FROM users WHERE id = 1", 1)

            affected_rows = db_mock.mock_db.execute("DELETE FROM users WHERE id = 1")
            assert affected_rows == 1

    def test_query_one(self) -> None:
        """测试 query_one"""
        with DatabaseMocker() as db_mock:
            db_mock.add_query_result(
                "SELECT * FROM users WHERE id = 1", [{"id": 1, "name": "Alice"}]
            )

            result = db_mock.mock_db.query_one("SELECT * FROM users WHERE id = 1")
            assert result == {"id": 1, "name": "Alice"}

    def test_normalize_sql(self) -> None:
        """测试 SQL 标准化"""
        db_mock = DatabaseMocker()

        sql1 = "SELECT  *  FROM   users"
        sql2 = "SELECT * FROM users"

        assert db_mock._normalize_sql(sql1) == db_mock._normalize_sql(sql2)

    def test_call_history(self) -> None:
        """测试调用历史"""
        with DatabaseMocker() as db_mock:
            db_mock.add_query_result("SELECT * FROM users", [])

            db_mock.mock_db.query("SELECT * FROM users")
            db_mock.mock_db.execute("INSERT INTO users VALUES (?)")

            history = db_mock.get_call_history()
            assert len(history) == 2
            assert "SELECT * FROM users" in history[0][0]
            assert "INSERT INTO users VALUES (?)" in history[1][0]

    def test_assert_called_with(self) -> None:
        """测试断言被调用"""
        with DatabaseMocker() as db_mock:
            db_mock.add_query_result("SELECT * FROM users", [])
            db_mock.mock_db.query("SELECT * FROM users")

            db_mock.assert_called_with("SELECT * FROM users")

    def test_assert_not_called_with(self) -> None:
        """测试断言未被调用"""
        with DatabaseMocker() as db_mock:
            db_mock.assert_not_called_with("DELETE FROM users")

    def test_assert_call_count(self) -> None:
        """测试断言调用次数"""
        with DatabaseMocker() as db_mock:
            db_mock.add_query_result("SELECT * FROM users", [])

            db_mock.mock_db.query("SELECT * FROM users")
            db_mock.mock_db.query("SELECT * FROM users")

            db_mock.assert_call_count("SELECT * FROM users", 2)

    def test_reset(self) -> None:
        """测试重置"""
        with DatabaseMocker() as db_mock:
            db_mock.add_query_result("SELECT * FROM users", [])
            db_mock.mock_db.query("SELECT * FROM users")

            db_mock.reset()

            assert len(db_mock.get_call_history()) == 0
