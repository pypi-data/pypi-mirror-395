"""追踪集成单元测试

测试 HTTP 拦截器和数据库追踪集成
"""

from unittest.mock import MagicMock

import pytest


def _otel_available() -> bool:
    """检查OpenTelemetry是否可用"""
    try:
        from df_test_framework.infrastructure.tracing.manager import OTEL_AVAILABLE

        return OTEL_AVAILABLE
    except ImportError:
        return False


class TestTracingInterceptor:
    """TracingInterceptor 测试"""

    def test_interceptor_initialization(self):
        """测试拦截器初始化"""
        from df_test_framework.infrastructure.tracing.interceptors import TracingInterceptor

        interceptor = TracingInterceptor()
        assert interceptor.name == "TracingInterceptor"
        assert interceptor.priority == 10
        assert interceptor.propagate_context is True
        assert interceptor.record_headers is False

    def test_interceptor_custom_config(self):
        """测试自定义配置"""
        from df_test_framework.infrastructure.tracing.interceptors import TracingInterceptor

        interceptor = TracingInterceptor(
            name="CustomTracer",
            priority=5,
            record_headers=True,
            record_body=True,
            propagate_context=False,
            sensitive_headers=["x-secret"],
        )

        assert interceptor.name == "CustomTracer"
        assert interceptor.priority == 5
        assert interceptor.record_headers is True
        assert interceptor.record_body is True
        assert interceptor.propagate_context is False
        assert "x-secret" in interceptor.sensitive_headers

    @pytest.mark.asyncio
    async def test_middleware_without_otel(self):
        """测试无OTEL时中间件直接透传请求

        v3.16.0: TracingInterceptor 迁移到 Middleware API
        """
        from df_test_framework.capabilities.clients.http.core import Request, Response
        from df_test_framework.infrastructure.tracing.interceptors import TracingInterceptor
        from df_test_framework.infrastructure.tracing.manager import OTEL_AVAILABLE

        if not OTEL_AVAILABLE:
            interceptor = TracingInterceptor()
            request = Request(method="GET", url="/api/users")

            # Mock call_next
            async def mock_call_next(req):
                return Response(status_code=200, headers={}, body="")

            # 调用中间件
            response = await interceptor(request, mock_call_next)
            assert response.status_code == 200


class TestDatabaseTracer:
    """DatabaseTracer 测试"""

    def test_tracer_initialization(self):
        """测试数据库追踪器初始化"""
        from df_test_framework.infrastructure.tracing.integrations.database import DatabaseTracer

        tracer = DatabaseTracer(
            db_system="mysql",
            db_name="test_db",
            db_user="root",
            server_address="localhost",
            server_port=3306,
        )

        assert tracer.db_system == "mysql"
        assert tracer.db_name == "test_db"
        assert tracer.db_user == "root"
        assert tracer.server_address == "localhost"
        assert tracer.server_port == 3306

    def test_trace_query_context_manager(self):
        """测试查询追踪上下文管理器"""
        from df_test_framework.infrastructure.tracing.integrations.database import DatabaseTracer

        tracer = DatabaseTracer(db_system="mysql", db_name="test_db")

        # 即使没有OTEL也应该工作
        with tracer.trace_query("SELECT", "users", "SELECT * FROM users"):
            # span可能为None（无OTEL时）
            pass

    def test_trace_transaction_context_manager(self):
        """测试事务追踪上下文管理器"""
        from df_test_framework.infrastructure.tracing.integrations.database import DatabaseTracer

        tracer = DatabaseTracer(db_system="mysql", db_name="test_db")

        with tracer.trace_transaction("my_transaction"):
            pass


class TestTracedDatabase:
    """TracedDatabase 包装器测试"""

    def test_infer_db_system_mysql(self):
        """测试推断MySQL数据库系统"""
        from df_test_framework.infrastructure.tracing.integrations.database import TracedDatabase

        mock_db = MagicMock()
        mock_db.connection_string = "mysql+pymysql://user:pass@localhost/testdb"

        traced_db = TracedDatabase(mock_db)
        assert traced_db._db_system == "mysql"

    def test_infer_db_system_postgresql(self):
        """测试推断PostgreSQL数据库系统"""
        from df_test_framework.infrastructure.tracing.integrations.database import TracedDatabase

        mock_db = MagicMock()
        mock_db.connection_string = "postgresql://user:pass@localhost/testdb"

        traced_db = TracedDatabase(mock_db)
        assert traced_db._db_system == "postgresql"

    def test_infer_db_system_sqlite(self):
        """测试推断SQLite数据库系统"""
        from df_test_framework.infrastructure.tracing.integrations.database import TracedDatabase

        mock_db = MagicMock()
        mock_db.connection_string = "sqlite:///test.db"

        traced_db = TracedDatabase(mock_db)
        assert traced_db._db_system == "sqlite"

    def test_infer_db_name(self):
        """测试推断数据库名称"""
        from df_test_framework.infrastructure.tracing.integrations.database import TracedDatabase

        mock_db = MagicMock()
        mock_db.connection_string = "mysql+pymysql://user:pass@localhost/my_database"

        traced_db = TracedDatabase(mock_db)
        assert traced_db._db_name == "my_database"

    def test_parse_operation(self):
        """测试解析SQL操作类型"""
        from df_test_framework.infrastructure.tracing.integrations.database import TracedDatabase

        mock_db = MagicMock()
        mock_db.connection_string = "mysql://localhost/test"

        traced_db = TracedDatabase(mock_db)

        assert traced_db._parse_operation("SELECT * FROM users") == "SELECT"
        assert traced_db._parse_operation("INSERT INTO users VALUES (1)") == "INSERT"
        assert traced_db._parse_operation("UPDATE users SET name='test'") == "UPDATE"
        assert traced_db._parse_operation("DELETE FROM users WHERE id=1") == "DELETE"
        assert traced_db._parse_operation("TRUNCATE TABLE users") == "EXECUTE"

    def test_parse_table(self):
        """测试解析表名"""
        from df_test_framework.infrastructure.tracing.integrations.database import TracedDatabase

        mock_db = MagicMock()
        mock_db.connection_string = "mysql://localhost/test"

        traced_db = TracedDatabase(mock_db)

        assert traced_db._parse_table("SELECT * FROM users WHERE id=1", "SELECT") == "USERS"
        assert traced_db._parse_table("INSERT INTO orders (id) VALUES (1)", "INSERT") == "ORDERS"
        assert traced_db._parse_table("UPDATE products SET price=100", "UPDATE") == "PRODUCTS"
        assert traced_db._parse_table("DELETE FROM logs WHERE id=1", "DELETE") == "LOGS"

    def test_query_one_delegates_to_database(self):
        """测试query_one委托给原始数据库"""
        from df_test_framework.infrastructure.tracing.integrations.database import TracedDatabase

        mock_db = MagicMock()
        mock_db.connection_string = "mysql://localhost/test"
        mock_db.query_one.return_value = {"id": 1, "name": "Alice"}

        traced_db = TracedDatabase(mock_db)
        result = traced_db.query_one("SELECT * FROM users WHERE id = 1")

        mock_db.query_one.assert_called_once()
        assert result == {"id": 1, "name": "Alice"}

    def test_insert_delegates_to_database(self):
        """测试insert委托给原始数据库"""
        from df_test_framework.infrastructure.tracing.integrations.database import TracedDatabase

        mock_db = MagicMock()
        mock_db.connection_string = "mysql://localhost/test"
        mock_db.insert.return_value = 1

        traced_db = TracedDatabase(mock_db)
        result = traced_db.insert("users", {"name": "Bob"})

        mock_db.insert.assert_called_once_with("users", {"name": "Bob"})
        assert result == 1

    def test_getattr_proxies_to_database(self):
        """测试__getattr__代理到原始数据库"""
        from df_test_framework.infrastructure.tracing.integrations.database import TracedDatabase

        mock_db = MagicMock()
        mock_db.connection_string = "mysql://localhost/test"
        mock_db.custom_method.return_value = "custom_result"

        traced_db = TracedDatabase(mock_db)
        result = traced_db.custom_method()

        assert result == "custom_result"


class TestTraceDbOperationDecorator:
    """trace_db_operation 装饰器测试"""

    def test_decorator_wraps_function(self):
        """测试装饰器包装函数"""
        from df_test_framework.infrastructure.tracing.integrations.database import (
            trace_db_operation,
        )

        @trace_db_operation("SELECT", "users", db_system="mysql")
        def get_user(user_id: int):
            return {"id": user_id, "name": "Test"}

        result = get_user(1)
        assert result == {"id": 1, "name": "Test"}

    def test_decorator_preserves_metadata(self):
        """测试装饰器保留函数元数据"""
        from df_test_framework.infrastructure.tracing.integrations.database import (
            trace_db_operation,
        )

        @trace_db_operation("SELECT", "users")
        def documented_function():
            """This is the docstring."""
            return "result"

        assert documented_function.__name__ == "documented_function"
        assert documented_function.__doc__ == "This is the docstring."


class TestSqlalchemyInstrumentation:
    """SQLAlchemy 仪表化测试"""

    def test_infer_db_system(self):
        """测试推断数据库系统"""
        from df_test_framework.infrastructure.tracing.integrations.sqlalchemy_instrumentation import (
            _infer_db_system,
        )

        assert _infer_db_system("mysql+pymysql://localhost/db") == "mysql"
        assert _infer_db_system("postgresql://localhost/db") == "postgresql"
        assert _infer_db_system("sqlite:///test.db") == "sqlite"
        assert _infer_db_system("oracle://localhost/db") == "oracle"
        assert _infer_db_system("mssql://localhost/db") == "mssql"
        assert _infer_db_system("unknown://localhost/db") == "unknown"

    def test_infer_db_name(self):
        """测试推断数据库名"""
        from df_test_framework.infrastructure.tracing.integrations.sqlalchemy_instrumentation import (
            _infer_db_name,
        )

        assert _infer_db_name("mysql://user:pass@localhost/my_db") == "my_db"
        assert _infer_db_name("mysql://user:pass@localhost/my_db?charset=utf8") == "my_db"

    def test_parse_operation(self):
        """测试解析操作类型"""
        from df_test_framework.infrastructure.tracing.integrations.sqlalchemy_instrumentation import (
            _parse_operation,
        )

        assert _parse_operation("SELECT * FROM users") == "SELECT"
        assert _parse_operation("  INSERT INTO users") == "INSERT"
        assert _parse_operation("UPDATE users SET") == "UPDATE"
        assert _parse_operation("DELETE FROM users") == "DELETE"
        assert _parse_operation("CREATE TABLE users") == "CREATE"
        assert _parse_operation("DROP TABLE users") == "DROP"
        assert _parse_operation("ALTER TABLE users") == "ALTER"
        assert _parse_operation("TRUNCATE users") == "EXECUTE"

    def test_parse_table(self):
        """测试解析表名"""
        from df_test_framework.infrastructure.tracing.integrations.sqlalchemy_instrumentation import (
            _parse_table,
        )

        assert _parse_table("SELECT * FROM users WHERE id=1", "SELECT") == "USERS"
        assert _parse_table("INSERT INTO orders (id) VALUES (1)", "INSERT") == "ORDERS"
        assert _parse_table("CREATE TABLE products (id INT)", "CREATE") == "PRODUCTS"
