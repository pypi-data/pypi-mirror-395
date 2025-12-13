"""数据库 Mock 工具

提供数据库操作的 Mock 功能，用于单元测试隔离
"""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, Mock

from loguru import logger


class DatabaseMocker:
    """数据库 Mock 工具

    提供数据库操作的 Mock 功能，适用于单元测试

    Examples:
        >>> # 使用上下文管理器
        >>> with DatabaseMocker() as db_mock:
        ...     db_mock.add_query_result("SELECT * FROM users", [{"id": 1, "name": "Alice"}])
        ...     result = db.query("SELECT * FROM users")
        ...     assert result == [{"id": 1, "name": "Alice"}]
        >>>
        >>> # 手动管理
        >>> db_mock = DatabaseMocker()
        >>> db_mock.start()
        >>> db_mock.add_query_result("SELECT * FROM users WHERE id = ?", {"id": 1, "name": "Alice"})
        >>> db_mock.stop()
    """

    def __init__(self) -> None:
        self._mock_results: dict[str, Any] = {}
        self._mock_db: Mock | None = None
        self._call_history: list[tuple[str, tuple, dict]] = []

    def start(self) -> DatabaseMocker:
        """启动 Mock"""
        logger.debug("Starting database mock")
        self._mock_db = MagicMock()
        self._setup_mock_methods()
        return self

    def stop(self) -> None:
        """停止 Mock"""
        logger.debug("Stopping database mock")
        self._mock_db = None
        self._mock_results.clear()
        self._call_history.clear()

    def _setup_mock_methods(self) -> None:
        """设置 Mock 方法"""
        if not self._mock_db:
            return

        # Mock query 方法
        self._mock_db.query.side_effect = self._handle_query
        self._mock_db.query_one.side_effect = self._handle_query_one
        self._mock_db.execute.side_effect = self._handle_execute

    def add_query_result(self, sql: str, result: Any) -> None:
        """添加查询结果

        Args:
            sql: SQL 语句（支持参数占位符）
            result: 查询结果
        """
        normalized_sql = self._normalize_sql(sql)
        self._mock_results[normalized_sql] = result
        logger.debug(f"Added mock result for query: {normalized_sql}")

    def add_execute_result(self, sql: str, affected_rows: int = 1) -> None:
        """添加执行结果

        Args:
            sql: SQL 语句
            affected_rows: 影响的行数
        """
        normalized_sql = self._normalize_sql(sql)
        self._mock_results[normalized_sql] = affected_rows
        logger.debug(f"Added mock result for execute: {normalized_sql}")

    def _normalize_sql(self, sql: str) -> str:
        """标准化 SQL 语句（去除多余空格）"""
        return " ".join(sql.split()).strip()

    def _handle_query(self, sql: str, *args: Any, **kwargs: Any) -> Any:
        """处理 query 调用"""
        self._record_call("query", sql, args, kwargs)
        normalized_sql = self._normalize_sql(sql)

        if normalized_sql in self._mock_results:
            return self._mock_results[normalized_sql]

        logger.warning(f"No mock result for query: {sql}")
        return []

    def _handle_query_one(self, sql: str, *args: Any, **kwargs: Any) -> Any:
        """处理 query_one 调用"""
        self._record_call("query_one", sql, args, kwargs)
        normalized_sql = self._normalize_sql(sql)

        if normalized_sql in self._mock_results:
            result = self._mock_results[normalized_sql]
            # 如果是列表，返回第一个元素
            if isinstance(result, list) and len(result) > 0:
                return result[0]
            return result

        logger.warning(f"No mock result for query_one: {sql}")
        return None

    def _handle_execute(self, sql: str, *args: Any, **kwargs: Any) -> int:
        """处理 execute 调用"""
        self._record_call("execute", sql, args, kwargs)
        normalized_sql = self._normalize_sql(sql)

        if normalized_sql in self._mock_results:
            return self._mock_results[normalized_sql]  # type: ignore

        logger.warning(f"No mock result for execute: {sql}")
        return 0

    def _record_call(self, method: str, sql: str, args: tuple, kwargs: dict) -> None:
        """记录方法调用"""
        self._call_history.append((f"{method}: {sql}", args, kwargs))

    def get_call_history(self) -> list[tuple[str, tuple, dict]]:
        """获取调用历史"""
        return self._call_history

    def assert_called_with(self, sql: str) -> None:
        """断言 SQL 被调用过"""
        normalized_sql = self._normalize_sql(sql)
        for call, _, _ in self._call_history:
            if normalized_sql in call:
                return

        raise AssertionError(
            f"SQL not called: {sql}\nCall history: {[c[0] for c in self._call_history]}"
        )

    def assert_not_called_with(self, sql: str) -> None:
        """断言 SQL 未被调用过"""
        normalized_sql = self._normalize_sql(sql)
        for call, _, _ in self._call_history:
            if normalized_sql in call:
                raise AssertionError(f"SQL was called: {sql}")

    def assert_call_count(self, sql: str, expected_count: int) -> None:
        """断言 SQL 调用次数"""
        normalized_sql = self._normalize_sql(sql)
        actual_count = sum(1 for call, _, _ in self._call_history if normalized_sql in call)

        if actual_count != expected_count:
            raise AssertionError(
                f"Expected {expected_count} calls, got {actual_count} for SQL: {sql}"
            )

    def reset(self) -> None:
        """重置所有 Mock 状态"""
        self._mock_results.clear()
        self._call_history.clear()
        logger.debug("Database mock reset")

    def __enter__(self) -> DatabaseMocker:
        """上下文管理器入口"""
        return self.start()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore
        """上下文管理器退出"""
        self.stop()

    @property
    def mock_db(self) -> Mock:
        """获取 Mock 数据库对象"""
        if not self._mock_db:
            raise RuntimeError("Mock not started. Call start() first.")
        return self._mock_db
