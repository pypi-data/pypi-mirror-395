"""数据库追踪集成

为数据库操作提供OpenTelemetry追踪支持

v3.10.0 新增 - P2.1 OpenTelemetry分布式追踪
"""

from __future__ import annotations

import functools
import time
from collections.abc import Callable
from contextlib import contextmanager
from typing import Any, TypeVar

from ..manager import OTEL_AVAILABLE, get_tracing_manager

if OTEL_AVAILABLE:
    from opentelemetry import trace

F = TypeVar("F", bound=Callable[..., Any])


class DatabaseTracer:
    """数据库追踪器

    为数据库操作创建追踪span

    使用示例:
        >>> tracer = DatabaseTracer(db_system="mysql", db_name="test_db")
        >>>
        >>> # 追踪查询
        >>> with tracer.trace_query("SELECT", "users", "SELECT * FROM users"):
        ...     result = db.query("SELECT * FROM users")
        >>>
        >>> # 追踪事务
        >>> with tracer.trace_transaction():
        ...     db.insert("users", {"name": "Alice"})
        ...     db.insert("orders", {"user_id": 1})

    追踪属性:
        - db.system: 数据库系统（mysql/postgresql/sqlite等）
        - db.name: 数据库名称
        - db.statement: SQL语句（可选）
        - db.operation: 操作类型（SELECT/INSERT/UPDATE/DELETE）
        - db.sql.table: 表名
        - db.row_count: 影响/返回的行数
    """

    def __init__(
        self,
        db_system: str = "unknown",
        db_name: str = "unknown",
        db_user: str | None = None,
        server_address: str | None = None,
        server_port: int | None = None,
        record_statement: bool = True,
        max_statement_length: int = 1000,
    ):
        """初始化数据库追踪器

        Args:
            db_system: 数据库系统类型（mysql/postgresql/sqlite等）
            db_name: 数据库名称
            db_user: 数据库用户（可选）
            server_address: 服务器地址（可选）
            server_port: 服务器端口（可选）
            record_statement: 是否记录SQL语句
            max_statement_length: SQL语句最大长度（超出截断）
        """
        self.db_system = db_system
        self.db_name = db_name
        self.db_user = db_user
        self.server_address = server_address
        self.server_port = server_port
        self.record_statement = record_statement
        self.max_statement_length = max_statement_length

    @contextmanager
    def trace_query(
        self,
        operation: str,
        table: str,
        statement: str | None = None,
        params: dict[str, Any] | None = None,
    ):
        """追踪单个查询

        Args:
            operation: 操作类型（SELECT/INSERT/UPDATE/DELETE）
            table: 表名
            statement: SQL语句（可选）
            params: 查询参数（可选，不记录到span）

        Yields:
            Span对象
        """
        if not OTEL_AVAILABLE:
            yield None
            return

        manager = get_tracing_manager()
        span_name = f"{operation} {table}"

        attributes = self._build_base_attributes()
        attributes["db.operation"] = operation
        attributes["db.sql.table"] = table

        if self.record_statement and statement:
            # 截断过长的SQL语句
            if len(statement) > self.max_statement_length:
                statement = statement[: self.max_statement_length] + "..."
            attributes["db.statement"] = statement

        start_time = time.perf_counter()

        with manager.start_span(span_name, attributes=attributes) as span:
            try:
                yield span
            except Exception as e:
                # 记录异常
                if span and span.is_recording():
                    duration_ms = (time.perf_counter() - start_time) * 1000
                    span.set_attribute("db.query.duration_ms", duration_ms)
                    span.record_exception(e)
                    span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                raise
            else:
                # 记录成功
                if span and span.is_recording():
                    duration_ms = (time.perf_counter() - start_time) * 1000
                    span.set_attribute("db.query.duration_ms", duration_ms)

    @contextmanager
    def trace_transaction(self, name: str = "transaction"):
        """追踪数据库事务

        Args:
            name: 事务名称

        Yields:
            Span对象
        """
        if not OTEL_AVAILABLE:
            yield None
            return

        manager = get_tracing_manager()
        span_name = f"DB Transaction: {name}"

        attributes = self._build_base_attributes()
        attributes["db.operation"] = "TRANSACTION"

        start_time = time.perf_counter()

        with manager.start_span(span_name, attributes=attributes) as span:
            try:
                yield span
            except Exception as e:
                if span and span.is_recording():
                    duration_ms = (time.perf_counter() - start_time) * 1000
                    span.set_attribute("db.transaction.duration_ms", duration_ms)
                    span.set_attribute("db.transaction.status", "rollback")
                    span.record_exception(e)
                    span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                raise
            else:
                if span and span.is_recording():
                    duration_ms = (time.perf_counter() - start_time) * 1000
                    span.set_attribute("db.transaction.duration_ms", duration_ms)
                    span.set_attribute("db.transaction.status", "commit")

    def record_row_count(self, span: Any, row_count: int) -> None:
        """记录行数到span

        Args:
            span: Span对象
            row_count: 行数
        """
        if OTEL_AVAILABLE and span and span.is_recording():
            span.set_attribute("db.row_count", row_count)

    def _build_base_attributes(self) -> dict[str, Any]:
        """构建基础属性

        Returns:
            属性字典
        """
        attrs: dict[str, Any] = {
            "db.system": self.db_system,
            "db.name": self.db_name,
        }

        if self.db_user:
            attrs["db.user"] = self.db_user

        if self.server_address:
            attrs["server.address"] = self.server_address

        if self.server_port:
            attrs["server.port"] = self.server_port

        return attrs


def trace_db_operation(
    operation: str,
    table: str,
    db_system: str = "unknown",
    db_name: str = "unknown",
    record_statement: bool = False,
) -> Callable[[F], F]:
    """数据库操作追踪装饰器

    Args:
        operation: 操作类型
        table: 表名
        db_system: 数据库系统
        db_name: 数据库名
        record_statement: 是否记录SQL语句

    Returns:
        装饰器函数

    示例:
        >>> @trace_db_operation("SELECT", "users", db_system="mysql")
        >>> def get_user(user_id: int):
        ...     return db.query_one("SELECT * FROM users WHERE id = :id", {"id": user_id})
    """

    def decorator(func: F) -> F:
        tracer = DatabaseTracer(
            db_system=db_system, db_name=db_name, record_statement=record_statement
        )

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with tracer.trace_query(operation, table):
                return func(*args, **kwargs)

        return wrapper  # type: ignore

    return decorator


class TracedDatabase:
    """带追踪功能的数据库包装器

    包装Database类，自动添加追踪功能

    使用示例:
        >>> from df_test_framework.capabilities.databases import Database
        >>> from df_test_framework.infrastructure.tracing.integrations import TracedDatabase
        >>>
        >>> # 包装现有数据库实例
        >>> db = Database(connection_string)
        >>> traced_db = TracedDatabase(db)
        >>>
        >>> # 所有操作自动追踪
        >>> result = traced_db.query_one("SELECT * FROM users WHERE id = 1")
        >>> traced_db.insert("users", {"name": "Alice"})
    """

    def __init__(
        self,
        database: Any,
        db_system: str | None = None,
        db_name: str | None = None,
        record_statement: bool = True,
    ):
        """初始化追踪包装器

        Args:
            database: Database实例
            db_system: 数据库系统（自动从连接字符串推断）
            db_name: 数据库名称（自动从连接字符串推断）
            record_statement: 是否记录SQL语句
        """
        self._database = database
        self._record_statement = record_statement

        # 自动推断数据库系统和名称
        conn_str = getattr(database, "connection_string", "")
        self._db_system = db_system or self._infer_db_system(conn_str)
        self._db_name = db_name or self._infer_db_name(conn_str)

        self._tracer = DatabaseTracer(
            db_system=self._db_system, db_name=self._db_name, record_statement=record_statement
        )

    def _infer_db_system(self, conn_str: str) -> str:
        """从连接字符串推断数据库系统

        Args:
            conn_str: 连接字符串

        Returns:
            数据库系统名称
        """
        conn_str = conn_str.lower()
        if "mysql" in conn_str:
            return "mysql"
        elif "postgresql" in conn_str or "postgres" in conn_str:
            return "postgresql"
        elif "sqlite" in conn_str:
            return "sqlite"
        elif "oracle" in conn_str:
            return "oracle"
        elif "mssql" in conn_str or "sqlserver" in conn_str:
            return "mssql"
        return "unknown"

    def _infer_db_name(self, conn_str: str) -> str:
        """从连接字符串推断数据库名称

        Args:
            conn_str: 连接字符串

        Returns:
            数据库名称
        """
        # 尝试从URL中提取数据库名
        # 格式: driver://user:pass@host:port/database
        if "/" in conn_str:
            parts = conn_str.split("/")
            if parts:
                db_part = parts[-1].split("?")[0]  # 去除查询参数
                if db_part:
                    return db_part
        return "unknown"

    def execute(self, sql: str, params: dict[str, Any] | None = None) -> int:
        """执行SQL语句（带追踪）"""
        operation = self._parse_operation(sql)
        table = self._parse_table(sql, operation)

        with self._tracer.trace_query(
            operation, table, sql if self._record_statement else None
        ) as span:
            result = self._database.execute(sql, params)
            self._tracer.record_row_count(span, result)
            return result

    def query_one(self, sql: str, params: dict[str, Any] | None = None) -> dict[str, Any] | None:
        """查询单条记录（带追踪）"""
        table = self._parse_table(sql, "SELECT")

        with self._tracer.trace_query(
            "SELECT", table, sql if self._record_statement else None
        ) as span:
            result = self._database.query_one(sql, params)
            self._tracer.record_row_count(span, 1 if result else 0)
            return result

    def query_all(self, sql: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """查询多条记录（带追踪）"""
        table = self._parse_table(sql, "SELECT")

        with self._tracer.trace_query(
            "SELECT", table, sql if self._record_statement else None
        ) as span:
            result = self._database.query_all(sql, params)
            self._tracer.record_row_count(span, len(result))
            return result

    def insert(self, table: str, data: dict[str, Any]) -> int:
        """插入记录（带追踪）"""
        with self._tracer.trace_query("INSERT", table) as span:
            result = self._database.insert(table, data)
            self._tracer.record_row_count(span, 1)
            return result

    def batch_insert(
        self, table: str, data_list: list[dict[str, Any]], chunk_size: int = 1000
    ) -> int:
        """批量插入（带追踪）"""
        with self._tracer.trace_query("INSERT", table) as span:
            result = self._database.batch_insert(table, data_list, chunk_size)
            self._tracer.record_row_count(span, result)
            return result

    def update(
        self,
        table: str,
        data: dict[str, Any],
        where: str,
        where_params: dict[str, Any] | None = None,
    ) -> int:
        """更新记录（带追踪）"""
        with self._tracer.trace_query("UPDATE", table) as span:
            result = self._database.update(table, data, where, where_params)
            self._tracer.record_row_count(span, result)
            return result

    def delete(self, table: str, where: str, where_params: dict[str, Any] | None = None) -> int:
        """删除记录（带追踪）"""
        with self._tracer.trace_query("DELETE", table) as span:
            result = self._database.delete(table, where, where_params)
            self._tracer.record_row_count(span, result)
            return result

    def transaction(self):
        """事务上下文管理器（带追踪）"""
        return _TracedTransactionContext(self._database, self._tracer)

    def session(self):
        """会话上下文管理器（代理）"""
        return self._database.session()

    def _parse_operation(self, sql: str) -> str:
        """解析SQL操作类型"""
        sql_upper = sql.strip().upper()
        for op in ["SELECT", "INSERT", "UPDATE", "DELETE"]:
            if sql_upper.startswith(op):
                return op
        return "EXECUTE"

    def _parse_table(self, sql: str, operation: str) -> str:
        """解析表名"""
        sql_upper = sql.strip().upper()

        if operation == "SELECT" and "FROM" in sql_upper:
            parts = sql_upper.split("FROM")[1].split()
            if parts:
                return parts[0].strip()

        elif operation == "INSERT" and "INTO" in sql_upper:
            parts = sql_upper.split("INTO")[1].split()
            if parts:
                return parts[0].strip()

        elif operation == "UPDATE":
            parts = sql_upper.split("UPDATE")[1].split()
            if parts:
                return parts[0].strip()

        elif operation == "DELETE" and "FROM" in sql_upper:
            parts = sql_upper.split("FROM")[1].split()
            if parts:
                return parts[0].strip()

        return "unknown"

    def __getattr__(self, name: str) -> Any:
        """代理其他方法到原始数据库"""
        return getattr(self._database, name)


class _TracedTransactionContext:
    """追踪事务上下文管理器"""

    def __init__(self, database: Any, tracer: DatabaseTracer):
        self._database = database
        self._tracer = tracer
        self._span_context = None
        self._transaction_context = None

    def __enter__(self):
        self._span_context = self._tracer.trace_transaction()
        self._span_context.__enter__()
        self._transaction_context = self._database.transaction()
        return self._transaction_context.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            result = self._transaction_context.__exit__(exc_type, exc_val, exc_tb)
        finally:
            self._span_context.__exit__(exc_type, exc_val, exc_tb)
        return result


__all__ = [
    "DatabaseTracer",
    "TracedDatabase",
    "trace_db_operation",
]
