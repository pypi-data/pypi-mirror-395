"""数据库指标集成

为数据库操作提供 Prometheus 指标收集

v3.10.0 新增 - P2.3 Prometheus监控
"""

from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Any

from ..manager import get_metrics_manager
from ..types import Counter, Gauge, Histogram


class DatabaseMetrics:
    """数据库指标收集器

    提供标准的数据库操作指标

    使用示例:
        >>> db_metrics = DatabaseMetrics(db_name="mydb")
        >>>
        >>> # 手动记录
        >>> db_metrics.record_query("SELECT", "users", 0.05, 100)
        >>>
        >>> # 使用上下文管理器
        >>> with db_metrics.observe_query("SELECT", "users"):
        ...     result = db.query("SELECT * FROM users")

    收集的指标:
        - db_queries_total: 查询总数（按操作、表）
        - db_query_duration_seconds: 查询耗时（按操作、表）
        - db_query_rows_affected: 影响/返回的行数
        - db_connections_active: 活跃连接数
        - db_connections_idle: 空闲连接数
        - db_errors_total: 错误总数
    """

    def __init__(self, db_name: str = "default", db_type: str = "unknown", prefix: str = "db"):
        """初始化数据库指标收集器

        Args:
            db_name: 数据库名称
            db_type: 数据库类型（mysql/postgresql/sqlite等）
            prefix: 指标名称前缀
        """
        self.db_name = db_name
        self.db_type = db_type
        self.prefix = prefix

        self._metrics_initialized = False
        self._queries_total: Counter | None = None
        self._query_duration: Histogram | None = None
        self._query_rows: Histogram | None = None
        self._connections_active: Gauge | None = None
        self._connections_idle: Gauge | None = None
        self._errors_total: Counter | None = None

    def _init_metrics(self) -> None:
        """初始化指标"""
        if self._metrics_initialized:
            return

        manager = get_metrics_manager()
        if not manager.is_initialized:
            manager.init()

        # 查询总数
        self._queries_total = manager.counter(
            f"{self.prefix}_queries_total",
            "Total database queries",
            labels=["db_name", "db_type", "operation", "table"],
        )

        # 查询耗时
        self._query_duration = manager.histogram(
            f"{self.prefix}_query_duration_seconds",
            "Database query duration in seconds",
            labels=["db_name", "operation", "table"],
            buckets=(0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5),
        )

        # 影响行数
        self._query_rows = manager.histogram(
            f"{self.prefix}_query_rows_affected",
            "Number of rows affected/returned by query",
            labels=["db_name", "operation"],
            buckets=(1, 10, 50, 100, 500, 1000, 5000, 10000),
        )

        # 活跃连接
        self._connections_active = manager.gauge(
            f"{self.prefix}_connections_active",
            "Number of active database connections",
            labels=["db_name"],
        )

        # 空闲连接
        self._connections_idle = manager.gauge(
            f"{self.prefix}_connections_idle",
            "Number of idle database connections",
            labels=["db_name"],
        )

        # 错误总数
        self._errors_total = manager.counter(
            f"{self.prefix}_errors_total",
            "Total database errors",
            labels=["db_name", "operation", "error_type"],
        )

        self._metrics_initialized = True

    def record_query(self, operation: str, table: str, duration: float, rows: int = 0) -> None:
        """记录查询指标

        Args:
            operation: 操作类型（SELECT/INSERT/UPDATE/DELETE）
            table: 表名
            duration: 查询耗时（秒）
            rows: 影响/返回的行数
        """
        self._init_metrics()

        # 查询计数
        self._queries_total.labels(
            db_name=self.db_name, db_type=self.db_type, operation=operation.upper(), table=table
        ).inc()

        # 查询耗时
        self._query_duration.labels(
            db_name=self.db_name, operation=operation.upper(), table=table
        ).observe(duration)

        # 影响行数
        if rows > 0:
            self._query_rows.labels(db_name=self.db_name, operation=operation.upper()).observe(rows)

    def record_error(self, operation: str, error_type: str) -> None:
        """记录错误

        Args:
            operation: 操作类型
            error_type: 错误类型
        """
        self._init_metrics()

        self._errors_total.labels(
            db_name=self.db_name, operation=operation.upper(), error_type=error_type
        ).inc()

    def set_connection_counts(self, active: int, idle: int) -> None:
        """设置连接数

        Args:
            active: 活跃连接数
            idle: 空闲连接数
        """
        self._init_metrics()

        self._connections_active.labels(db_name=self.db_name).set(active)
        self._connections_idle.labels(db_name=self.db_name).set(idle)

    @contextmanager
    def observe_query(self, operation: str, table: str):
        """查询观察上下文管理器

        Args:
            operation: 操作类型
            table: 表名

        Yields:
            None
        """
        start_time = time.perf_counter()
        try:
            yield
        except Exception as e:
            duration = time.perf_counter() - start_time
            self.record_query(operation, table, duration, 0)
            self.record_error(operation, type(e).__name__)
            raise
        else:
            duration = time.perf_counter() - start_time
            self.record_query(operation, table, duration)


class MetricsTracedDatabase:
    """带指标收集的数据库包装器

    包装 Database 类，自动收集指标

    使用示例:
        >>> from df_test_framework.capabilities.databases import Database
        >>> from df_test_framework.infrastructure.metrics.integrations import MetricsTracedDatabase
        >>>
        >>> db = Database(connection_string)
        >>> metrics_db = MetricsTracedDatabase(db)
        >>>
        >>> # 所有操作自动收集指标
        >>> result = metrics_db.query_one("SELECT * FROM users WHERE id = 1")
    """

    def __init__(self, database: Any, db_name: str | None = None, db_type: str | None = None):
        """初始化指标包装器

        Args:
            database: Database 实例
            db_name: 数据库名称（自动推断）
            db_type: 数据库类型（自动推断）
        """
        self._database = database

        # 推断数据库信息
        conn_str = getattr(database, "connection_string", "")
        self._db_type = db_type or self._infer_db_type(conn_str)
        self._db_name = db_name or self._infer_db_name(conn_str)

        self._metrics = DatabaseMetrics(db_name=self._db_name, db_type=self._db_type)

    def _infer_db_type(self, conn_str: str) -> str:
        """推断数据库类型"""
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
        """推断数据库名称"""
        if "/" in conn_str:
            parts = conn_str.split("/")
            if parts:
                db_part = parts[-1].split("?")[0]
                if db_part:
                    return db_part
        return "unknown"

    def _parse_operation(self, sql: str) -> str:
        """解析 SQL 操作类型"""
        sql_upper = sql.strip().upper()
        for op in ["SELECT", "INSERT", "UPDATE", "DELETE"]:
            if sql_upper.startswith(op):
                return op
        return "EXECUTE"

    def _parse_table(self, sql: str, operation: str) -> str:
        """解析表名"""
        sql_upper = sql.strip().upper()

        try:
            if operation == "SELECT" and "FROM" in sql_upper:
                parts = sql_upper.split("FROM")[1].split()
                if parts:
                    return parts[0].strip().rstrip(",")
            elif operation == "INSERT" and "INTO" in sql_upper:
                parts = sql_upper.split("INTO")[1].split()
                if parts:
                    return parts[0].strip().rstrip("(")
            elif operation == "UPDATE":
                parts = sql_upper.split("UPDATE")[1].split()
                if parts:
                    return parts[0].strip()
            elif operation == "DELETE" and "FROM" in sql_upper:
                parts = sql_upper.split("FROM")[1].split()
                if parts:
                    return parts[0].strip()
        except (IndexError, ValueError):
            pass

        return "unknown"

    def execute(self, sql: str, params: dict[str, Any] | None = None) -> int:
        """执行 SQL（带指标）"""
        operation = self._parse_operation(sql)
        table = self._parse_table(sql, operation)

        start_time = time.perf_counter()
        try:
            result = self._database.execute(sql, params)
            duration = time.perf_counter() - start_time
            self._metrics.record_query(operation, table, duration, result)
            return result
        except Exception as e:
            duration = time.perf_counter() - start_time
            self._metrics.record_query(operation, table, duration, 0)
            self._metrics.record_error(operation, type(e).__name__)
            raise

    def query_one(self, sql: str, params: dict[str, Any] | None = None) -> dict[str, Any] | None:
        """查询单条记录（带指标）"""
        table = self._parse_table(sql, "SELECT")

        start_time = time.perf_counter()
        try:
            result = self._database.query_one(sql, params)
            duration = time.perf_counter() - start_time
            self._metrics.record_query("SELECT", table, duration, 1 if result else 0)
            return result
        except Exception as e:
            duration = time.perf_counter() - start_time
            self._metrics.record_query("SELECT", table, duration, 0)
            self._metrics.record_error("SELECT", type(e).__name__)
            raise

    def query_all(self, sql: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """查询多条记录（带指标）"""
        table = self._parse_table(sql, "SELECT")

        start_time = time.perf_counter()
        try:
            result = self._database.query_all(sql, params)
            duration = time.perf_counter() - start_time
            self._metrics.record_query("SELECT", table, duration, len(result))
            return result
        except Exception as e:
            duration = time.perf_counter() - start_time
            self._metrics.record_query("SELECT", table, duration, 0)
            self._metrics.record_error("SELECT", type(e).__name__)
            raise

    def insert(self, table: str, data: dict[str, Any]) -> int:
        """插入记录（带指标）"""
        start_time = time.perf_counter()
        try:
            result = self._database.insert(table, data)
            duration = time.perf_counter() - start_time
            self._metrics.record_query("INSERT", table, duration, 1)
            return result
        except Exception as e:
            duration = time.perf_counter() - start_time
            self._metrics.record_query("INSERT", table, duration, 0)
            self._metrics.record_error("INSERT", type(e).__name__)
            raise

    def update(
        self,
        table: str,
        data: dict[str, Any],
        where: str,
        where_params: dict[str, Any] | None = None,
    ) -> int:
        """更新记录（带指标）"""
        start_time = time.perf_counter()
        try:
            result = self._database.update(table, data, where, where_params)
            duration = time.perf_counter() - start_time
            self._metrics.record_query("UPDATE", table, duration, result)
            return result
        except Exception as e:
            duration = time.perf_counter() - start_time
            self._metrics.record_query("UPDATE", table, duration, 0)
            self._metrics.record_error("UPDATE", type(e).__name__)
            raise

    def delete(self, table: str, where: str, where_params: dict[str, Any] | None = None) -> int:
        """删除记录（带指标）"""
        start_time = time.perf_counter()
        try:
            result = self._database.delete(table, where, where_params)
            duration = time.perf_counter() - start_time
            self._metrics.record_query("DELETE", table, duration, result)
            return result
        except Exception as e:
            duration = time.perf_counter() - start_time
            self._metrics.record_query("DELETE", table, duration, 0)
            self._metrics.record_error("DELETE", type(e).__name__)
            raise

    @property
    def metrics(self) -> DatabaseMetrics:
        """获取指标收集器"""
        return self._metrics

    def __getattr__(self, name: str) -> Any:
        """代理其他方法到原始数据库"""
        return getattr(self._database, name)


__all__ = [
    "DatabaseMetrics",
    "MetricsTracedDatabase",
]
