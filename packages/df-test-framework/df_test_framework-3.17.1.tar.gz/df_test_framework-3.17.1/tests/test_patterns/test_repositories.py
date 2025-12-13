"""
测试Repository模式和QuerySpec

验证BaseRepository和QuerySpec查询构建器的功能。

v3.7.0+ 更新: Repository现在接收Session而非Database
"""

from typing import Any

import pytest

from df_test_framework.capabilities.databases.repositories import (
    BaseRepository,
    QuerySpec,
)

# ========== Mock Session for v3.7+ ==========


class MockResult:
    """模拟SQLAlchemy Result对象"""

    def __init__(
        self, data: dict[str, Any] | None = None, data_list: list[dict[str, Any]] | None = None
    ):
        self._data = data
        self._data_list = data_list or []
        self._rowcount = 1 if data or data_list else 0
        self._lastrowid = 1

    def mappings(self):
        """返回self以支持链式调用"""
        return self

    def first(self):
        """返回第一条记录"""
        return self._data

    def all(self):
        """返回所有记录"""
        return self._data_list

    @property
    def rowcount(self):
        return self._rowcount

    @property
    def lastrowid(self):
        return self._lastrowid


class MockSession:
    """模拟SQLAlchemy Session用于测试"""

    def __init__(self):
        self.query_one_result: dict[str, Any] | None = None
        self.query_all_result: list[dict[str, Any]] = []
        self.execute_result: int = 0  # 用于UPDATE/DELETE的rowcount
        self.insert_result: int = 0  # 用于INSERT的lastrowid
        self.batch_insert_result: int = 0  # 用于批量插入的rowcount

        # 用于记录调用
        self.last_sql: str = ""
        self.last_params: dict[str, Any] = {}

    def execute(self, sql, params: dict[str, Any] | None = None):
        """模拟execute方法"""
        self.last_sql = str(sql)
        self.last_params = params or {}

        # 判断SQL类型
        sql_str = str(sql).upper()
        if "SELECT" in sql_str:
            # 查询操作
            if "LIMIT 1" in sql_str or self.query_one_result is not None:
                return MockResult(data=self.query_one_result)
            else:
                return MockResult(data_list=self.query_all_result)
        elif "INSERT" in sql_str:
            result = MockResult()
            result._rowcount = 1
            result._lastrowid = self.insert_result
            return result
        elif "UPDATE" in sql_str or "DELETE" in sql_str:
            result = MockResult()
            result._rowcount = self.execute_result
            return result
        else:
            return MockResult()


# ========== 测试用的Repository ==========


class UserRepository(BaseRepository):
    """测试用的UserRepository"""

    def __init__(self, session: MockSession):
        super().__init__(session, table_name="users")

    def find_by_username(self, username: str) -> dict[str, Any] | None:
        """根据用户名查找用户"""
        return self.find_one({"username": username})


class TestBaseRepository:
    """测试BaseRepository"""

    def setup_method(self):
        """每个测试前创建mock session"""
        self.session = MockSession()
        self.repo = BaseRepository(self.session, table_name="test_table")

    def test_repository_creation(self):
        """测试创建Repository"""
        assert self.repo.session is self.session
        assert self.repo.table_name == "test_table"

    def test_find_by_id(self):
        """测试find_by_id"""
        self.session.query_one_result = {"id": 1, "name": "Alice"}

        result = self.repo.find_by_id(1)

        assert result == {"id": 1, "name": "Alice"}
        assert "WHERE id = :id_value" in self.session.last_sql
        assert self.session.last_params == {"id_value": 1}

    def test_find_by_id_custom_column(self):
        """测试find_by_id使用自定义ID列"""
        self.session.query_one_result = {"user_id": "user_001", "name": "Alice"}

        result = self.repo.find_by_id("user_001", id_column="user_id")

        assert result["user_id"] == "user_001"
        assert "WHERE user_id = :id_value" in self.session.last_sql

    def test_find_one(self):
        """测试find_one"""
        self.session.query_one_result = {"id": 1, "name": "Alice", "status": "ACTIVE"}

        result = self.repo.find_one({"name": "Alice", "status": "ACTIVE"})

        assert result == {"id": 1, "name": "Alice", "status": "ACTIVE"}
        assert "WHERE" in self.session.last_sql
        assert "name = :name" in self.session.last_sql
        assert "status = :status" in self.session.last_sql

    def test_find_all_no_conditions(self):
        """测试find_all不带条件"""
        self.session.query_all_result = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
        ]

        result = self.repo.find_all()

        assert len(result) == 2
        assert "SELECT * FROM test_table" in self.session.last_sql
        assert "WHERE" not in self.session.last_sql

    def test_find_all_with_conditions(self):
        """测试find_all带条件"""
        self.session.query_all_result = [{"id": 1, "name": "Alice", "status": "ACTIVE"}]

        result = self.repo.find_all(conditions={"status": "ACTIVE"})

        assert len(result) == 1
        assert "WHERE status = :status" in self.session.last_sql

    def test_find_all_with_order_by(self):
        """测试find_all带排序"""
        self.session.query_all_result = []

        self.repo.find_all(order_by="created_at DESC")

        assert "ORDER BY created_at DESC" in self.session.last_sql

    def test_find_all_with_limit(self):
        """测试find_all带限制"""
        self.session.query_all_result = []

        self.repo.find_all(limit=10)

        assert "LIMIT 10" in self.session.last_sql

    def test_find_by_ids(self):
        """测试find_by_ids批量查询"""
        self.session.query_all_result = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
        ]

        result = self.repo.find_by_ids([1, 2])

        assert len(result) == 2
        assert "WHERE id IN" in self.session.last_sql

    def test_find_by_ids_empty_list(self):
        """测试find_by_ids空列表"""
        result = self.repo.find_by_ids([])

        assert result == []

    def test_count_all(self):
        """测试count统计所有记录"""
        self.session.query_one_result = {"count": 100}

        result = self.repo.count()

        assert result == 100
        assert "SELECT COUNT(*)" in self.session.last_sql

    def test_count_with_conditions(self):
        """测试count带条件"""
        self.session.query_one_result = {"count": 50}

        result = self.repo.count({"status": "ACTIVE"})

        assert result == 50
        assert "WHERE status = :status" in self.session.last_sql

    def test_exists_true(self):
        """测试exists返回True"""
        self.session.query_one_result = {"count": 1}

        result = self.repo.exists({"name": "Alice"})

        assert result is True

    def test_exists_false(self):
        """测试exists返回False"""
        self.session.query_one_result = {"count": 0}

        result = self.repo.exists({"name": "NonExistent"})

        assert result is False

    def test_create(self):
        """测试create创建记录"""
        self.session.insert_result = 123

        result = self.repo.create({"name": "Alice", "age": 25})

        assert result == 123
        assert self.session.last_params == {"name": "Alice", "age": 25}

    def test_batch_create(self):
        """测试batch_create批量创建"""
        self.session.batch_insert_result = 3

        data_list = [
            {"name": "Alice", "age": 25},
            {"name": "Bob", "age": 30},
            {"name": "Charlie", "age": 35},
        ]

        result = self.repo.batch_create(data_list)

        assert result == 3

    def test_update(self):
        """测试update更新记录"""
        self.session.execute_result = 1

        result = self.repo.update(
            conditions={"id": 1},
            data={"name": "Alice Updated", "age": 26},
        )

        assert result == 1
        assert "UPDATE test_table SET" in self.session.last_sql
        assert "WHERE" in self.session.last_sql

    def test_delete(self):
        """测试delete删除记录"""
        self.session.execute_result = 1

        result = self.repo.delete({"id": 1})

        assert result == 1
        assert "DELETE FROM test_table WHERE id = :id" in self.session.last_sql

    def test_delete_by_ids(self):
        """测试delete_by_ids批量删除"""
        self.session.execute_result = 2

        result = self.repo.delete_by_ids([1, 2])

        assert result == 2
        assert "DELETE FROM test_table WHERE id IN" in self.session.last_sql

    def test_delete_by_ids_empty_list(self):
        """测试delete_by_ids空列表"""
        result = self.repo.delete_by_ids([])

        assert result == 0


class TestQuerySpec:
    """测试QuerySpec查询构建器"""

    def test_equal_operator(self):
        """测试等于操作符"""
        spec = QuerySpec("status") == "ACTIVE"

        sql, params = spec.get_where_sql_and_params()

        assert sql == "status = :param"
        assert params == {"param": "ACTIVE"}

    def test_not_equal_operator(self):
        """测试不等于操作符"""
        spec = QuerySpec("status") != "DELETED"

        sql, params = spec.get_where_sql_and_params()

        assert sql == "status != :param"
        assert params == {"param": "DELETED"}

    def test_greater_than_operator(self):
        """测试大于操作符"""
        spec = QuerySpec("age") > 18

        sql, params = spec.get_where_sql_and_params()

        assert sql == "age > :param"
        assert params == {"param": 18}

    def test_greater_equal_operator(self):
        """测试大于等于操作符"""
        spec = QuerySpec("age") >= 18

        sql, params = spec.get_where_sql_and_params()

        assert sql == "age >= :param"

    def test_less_than_operator(self):
        """测试小于操作符"""
        spec = QuerySpec("age") < 65

        sql, params = spec.get_where_sql_and_params()

        assert sql == "age < :param"

    def test_less_equal_operator(self):
        """测试小于等于操作符"""
        spec = QuerySpec("age") <= 65

        sql, params = spec.get_where_sql_and_params()

        assert sql == "age <= :param"

    def test_like_operator(self):
        """测试LIKE模糊查询"""
        spec = QuerySpec("name").like("%Alice%")

        sql, params = spec.get_where_sql_and_params()

        assert sql == "name LIKE :param"
        assert params == {"param": "%Alice%"}

    def test_in_list_operator(self):
        """测试IN列表查询"""
        spec = QuerySpec("status").in_list(["ACTIVE", "PENDING", "PROCESSING"])

        sql, params = spec.get_where_sql_and_params()

        assert "status IN" in sql
        assert len(params) == 3

    def test_between_operator(self):
        """测试BETWEEN范围查询"""
        spec = QuerySpec("amount").between(100, 500)

        sql, params = spec.get_where_sql_and_params()

        assert "amount BETWEEN" in sql
        assert "param_start" in params
        assert "param_end" in params
        assert params["param_start"] == 100
        assert params["param_end"] == 500

    def test_is_null_operator(self):
        """测试IS NULL"""
        spec = QuerySpec("deleted_at").is_null()

        sql, params = spec.get_where_sql_and_params()

        assert sql == "deleted_at IS NULL"
        assert params == {}

    def test_is_not_null_operator(self):
        """测试IS NOT NULL"""
        spec = QuerySpec("deleted_at").is_not_null()

        sql, params = spec.get_where_sql_and_params()

        assert sql == "deleted_at IS NOT NULL"
        assert params == {}

    def test_and_combination(self):
        """测试AND逻辑组合"""
        spec = (QuerySpec("status") == "ACTIVE") & (QuerySpec("age") > 18)

        sql, params = spec.get_where_sql_and_params()

        assert "AND" in sql
        assert "status = " in sql
        assert "age > " in sql

    def test_or_combination(self):
        """测试OR逻辑组合"""
        spec = (QuerySpec("status") == "DELETED") | (QuerySpec("status") == "ARCHIVED")

        sql, params = spec.get_where_sql_and_params()

        assert "OR" in sql
        assert "status = " in sql

    def test_complex_combination(self):
        """测试复杂逻辑组合"""
        spec = ((QuerySpec("status") == "ACTIVE") & (QuerySpec("age") > 18)) | (
            QuerySpec("is_vip") == True  # noqa: E712
        )

        sql, params = spec.get_where_sql_and_params()

        assert "AND" in sql
        assert "OR" in sql

    def test_uninitialized_spec_raises_error(self):
        """测试未初始化的QuerySpec抛出错误"""
        spec = QuerySpec("status")

        with pytest.raises(ValueError, match="QuerySpec未初始化"):
            spec.get_where_sql_and_params()

    def test_and_uninitialized_raises_error(self):
        """测试对未初始化的QuerySpec进行AND操作抛出错误"""
        spec1 = QuerySpec("status")
        spec2 = QuerySpec("age") > 18

        with pytest.raises(ValueError, match="不能对未初始化的QuerySpec进行AND操作"):
            spec1 & spec2

    def test_or_uninitialized_raises_error(self):
        """测试对未初始化的QuerySpec进行OR操作抛出错误"""
        spec1 = QuerySpec("status") == "ACTIVE"
        spec2 = QuerySpec("age")

        with pytest.raises(ValueError, match="不能对未初始化的QuerySpec进行OR操作"):
            spec1 | spec2


class TestQuerySpecIntegration:
    """QuerySpec集成测试"""

    def test_real_world_query_1(self):
        """真实场景：查找活跃且年龄在18-65之间的用户"""
        spec = (QuerySpec("status") == "ACTIVE") & (QuerySpec("age").between(18, 65))

        sql, params = spec.get_where_sql_and_params()

        assert "status = " in sql
        assert "age BETWEEN" in sql
        assert "AND" in sql

    def test_real_world_query_2(self):
        """真实场景：查找已删除或已归档的记录"""
        spec = (QuerySpec("status") == "DELETED") | (QuerySpec("status") == "ARCHIVED")

        sql, params = spec.get_where_sql_and_params()

        assert "OR" in sql

    def test_real_world_query_3(self):
        """真实场景：查找特定状态且金额大于100的订单"""
        spec = (QuerySpec("status").in_list(["PENDING", "PROCESSING"])) & (
            QuerySpec("amount") > 100
        )

        sql, params = spec.get_where_sql_and_params()

        assert "IN" in sql
        assert "AND" in sql
        assert "amount > " in sql

    def test_real_world_query_4(self):
        """真实场景：查找VIP用户或订单金额大于1000的用户"""
        spec = (QuerySpec("is_vip") == True) | (  # noqa: E712
            QuerySpec("total_amount") > 1000
        )

        sql, params = spec.get_where_sql_and_params()

        assert "OR" in sql
