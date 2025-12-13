"""SQLAlchemy 仪表化

提供SQLAlchemy引擎的自动追踪仪表化

v3.10.0 新增 - P2.1 OpenTelemetry分布式追踪
"""

from __future__ import annotations

import time
from typing import Any

from ..manager import OTEL_AVAILABLE, get_tracing_manager

if OTEL_AVAILABLE:
    from opentelemetry import trace

# 存储已仪表化的引擎
_instrumented_engines: set[int] = set()


def instrument_sqlalchemy(
    engine: Any,
    db_system: str | None = None,
    db_name: str | None = None,
    record_statement: bool = True,
    max_statement_length: int = 1000,
) -> None:
    """仪表化SQLAlchemy引擎

    为SQLAlchemy引擎添加自动追踪，无需修改现有代码

    Args:
        engine: SQLAlchemy Engine实例
        db_system: 数据库系统（自动推断）
        db_name: 数据库名称（自动推断）
        record_statement: 是否记录SQL语句
        max_statement_length: SQL语句最大长度

    使用示例:
        >>> from sqlalchemy import create_engine
        >>> from df_test_framework.infrastructure.tracing.integrations import instrument_sqlalchemy
        >>>
        >>> engine = create_engine("mysql+pymysql://user:pass@localhost/db")
        >>> instrument_sqlalchemy(engine)
        >>>
        >>> # 后续所有查询自动追踪
        >>> with engine.connect() as conn:
        ...     result = conn.execute(text("SELECT * FROM users"))
    """
    if not OTEL_AVAILABLE:
        return

    engine_id = id(engine)
    if engine_id in _instrumented_engines:
        return  # 避免重复仪表化

    from sqlalchemy import event

    # 推断数据库信息
    url = str(engine.url)
    inferred_db_system = db_system or _infer_db_system(url)
    inferred_db_name = db_name or _infer_db_name(url)

    # 存储span的字典（通过connection id）
    connection_spans: dict[int, tuple[Any, float]] = {}

    @event.listens_for(engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        """SQL执行前：创建span"""
        manager = get_tracing_manager()

        # 解析操作类型和表名
        operation = _parse_operation(statement)
        table = _parse_table(statement, operation)

        span_name = f"{operation} {table}"

        # 构建属性
        attributes: dict[str, Any] = {
            "db.system": inferred_db_system,
            "db.name": inferred_db_name,
            "db.operation": operation,
            "db.sql.table": table,
        }

        if record_statement:
            stmt = statement
            if len(stmt) > max_statement_length:
                stmt = stmt[:max_statement_length] + "..."
            attributes["db.statement"] = stmt

        if executemany:
            attributes["db.execute_many"] = True

        # 创建span
        span = manager.start_span_no_context(span_name, attributes=attributes)
        start_time = time.perf_counter()

        # 存储span供after使用
        connection_spans[id(cursor)] = (span, start_time)

    @event.listens_for(engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        """SQL执行后：结束span"""
        cursor_id = id(cursor)
        if cursor_id not in connection_spans:
            return

        span, start_time = connection_spans.pop(cursor_id)

        if span and span.is_recording():
            duration_ms = (time.perf_counter() - start_time) * 1000
            span.set_attribute("db.query.duration_ms", duration_ms)

            # 记录行数
            if hasattr(cursor, "rowcount"):
                span.set_attribute("db.row_count", cursor.rowcount)

            span.end()

    @event.listens_for(engine, "handle_error")
    def handle_error(exception_context):
        """处理错误：记录异常到span"""
        cursor = getattr(exception_context, "cursor", None)
        if cursor is None:
            return

        cursor_id = id(cursor)
        if cursor_id not in connection_spans:
            return

        span, start_time = connection_spans.pop(cursor_id)

        if span and span.is_recording():
            duration_ms = (time.perf_counter() - start_time) * 1000
            span.set_attribute("db.query.duration_ms", duration_ms)

            # 记录异常
            error = exception_context.original_exception
            span.record_exception(error)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(error)))
            span.end()

    _instrumented_engines.add(engine_id)


def uninstrument_sqlalchemy(engine: Any) -> None:
    """移除SQLAlchemy引擎的仪表化

    Args:
        engine: SQLAlchemy Engine实例
    """
    engine_id = id(engine)
    if engine_id in _instrumented_engines:
        _instrumented_engines.discard(engine_id)

        # 注意：SQLAlchemy不支持移除事件监听器
        # 这里只是从跟踪集合中移除


def _infer_db_system(url: str) -> str:
    """从URL推断数据库系统"""
    url_lower = url.lower()
    if "mysql" in url_lower:
        return "mysql"
    elif "postgresql" in url_lower or "postgres" in url_lower:
        return "postgresql"
    elif "sqlite" in url_lower:
        return "sqlite"
    elif "oracle" in url_lower:
        return "oracle"
    elif "mssql" in url_lower or "sqlserver" in url_lower:
        return "mssql"
    return "unknown"


def _infer_db_name(url: str) -> str:
    """从URL推断数据库名"""
    if "/" in url:
        parts = url.split("/")
        if parts:
            db_part = parts[-1].split("?")[0]
            if db_part:
                return db_part
    return "unknown"


def _parse_operation(statement: str) -> str:
    """解析SQL操作类型"""
    stmt_upper = statement.strip().upper()
    for op in ["SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "ALTER"]:
        if stmt_upper.startswith(op):
            return op
    return "EXECUTE"


def _parse_table(statement: str, operation: str) -> str:
    """解析表名"""
    stmt_upper = statement.strip().upper()

    try:
        if operation == "SELECT" and "FROM" in stmt_upper:
            parts = stmt_upper.split("FROM")[1].split()
            if parts:
                return parts[0].strip().rstrip(",")

        elif operation == "INSERT" and "INTO" in stmt_upper:
            parts = stmt_upper.split("INTO")[1].split()
            if parts:
                return parts[0].strip().rstrip("(")

        elif operation == "UPDATE":
            parts = stmt_upper.split("UPDATE")[1].split()
            if parts:
                return parts[0].strip()

        elif operation == "DELETE" and "FROM" in stmt_upper:
            parts = stmt_upper.split("FROM")[1].split()
            if parts:
                return parts[0].strip()

        elif operation in ["CREATE", "DROP", "ALTER"]:
            # CREATE TABLE xxx / DROP TABLE xxx
            if "TABLE" in stmt_upper:
                parts = stmt_upper.split("TABLE")[1].split()
                if parts:
                    return parts[0].strip().rstrip("(")
    except (IndexError, ValueError):
        pass

    return "unknown"


__all__ = [
    "instrument_sqlalchemy",
    "uninstrument_sqlalchemy",
]
