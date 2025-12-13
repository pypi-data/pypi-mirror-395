"""DBDebugger 单元测试"""

import time

import pytest

from df_test_framework.testing.debugging import (
    DBDebugger,
    disable_db_debug,
    enable_db_debug,
    get_global_db_debugger,
)


class TestDBDebugger:
    """DBDebugger 基本功能测试"""

    def test_init_default(self):
        """测试默认初始化"""
        debugger = DBDebugger()
        assert debugger.enabled is True
        assert debugger.slow_query_threshold_ms == 100
        assert debugger.max_sql_length == 500
        assert debugger.queries == []

    def test_init_custom(self):
        """测试自定义初始化"""
        debugger = DBDebugger(
            enabled=False,
            slow_query_threshold_ms=50,
            max_sql_length=200,
        )
        assert debugger.enabled is False
        assert debugger.slow_query_threshold_ms == 50
        assert debugger.max_sql_length == 200

    def test_start_stop(self):
        """测试启动和停止"""
        debugger = DBDebugger(enabled=False)
        assert debugger.enabled is False

        debugger.start()
        assert debugger.enabled is True

        debugger.stop()
        assert debugger.enabled is False

    def test_clear(self):
        """测试清空记录"""
        debugger = DBDebugger()
        debugger.log_query_start("SELECT * FROM users")
        debugger.log_query_end(result_count=10)

        assert len(debugger.queries) == 1

        debugger.clear()
        assert len(debugger.queries) == 0
        assert debugger._current_query is None


class TestDBDebuggerLogging:
    """DBDebugger 日志记录测试"""

    def test_log_query_basic(self, capsys):
        """测试基本查询日志"""
        debugger = DBDebugger()
        debugger.log_query_start("SELECT * FROM users WHERE id = 1")
        debugger.log_query_end(result_count=1)

        captured = capsys.readouterr()
        assert "[DB DEBUG] SQL:" in captured.out
        assert "SELECT * FROM users" in captured.out
        assert "Result: 1 row(s)" in captured.out

    def test_log_query_with_params(self, capsys):
        """测试带参数的查询日志"""
        debugger = DBDebugger()
        debugger.log_query_start(
            "SELECT * FROM users WHERE id = %s",
            params=(1,),
        )
        debugger.log_query_end(result_count=1)

        captured = capsys.readouterr()
        assert "[DB DEBUG] Params:" in captured.out

    def test_log_query_error(self):
        """测试查询错误日志"""
        debugger = DBDebugger()
        debugger.log_query_start("SELECT * FROM nonexistent")
        debugger.log_query_error(Exception("Table not found"))

        assert len(debugger.queries) == 1
        assert "error" in debugger.queries[0]
        assert debugger.queries[0]["error_type"] == "Exception"

    def test_disabled_logging(self):
        """测试禁用状态不记录日志"""
        debugger = DBDebugger(enabled=False)
        debugger.log_query_start("SELECT 1")
        debugger.log_query_end(result_count=1)

        assert len(debugger.queries) == 0


class TestDBDebuggerSlowQuery:
    """DBDebugger 慢查询测试"""

    def test_slow_query_detection(self):
        """测试慢查询检测"""
        debugger = DBDebugger(slow_query_threshold_ms=10)

        debugger.log_query_start("SELECT * FROM large_table")
        time.sleep(0.02)  # 20ms
        debugger.log_query_end(result_count=1000)

        assert len(debugger.queries) == 1
        assert debugger.queries[0]["is_slow"] is True

    def test_fast_query(self):
        """测试快速查询"""
        debugger = DBDebugger(slow_query_threshold_ms=1000)

        debugger.log_query_start("SELECT 1")
        debugger.log_query_end(result_count=1)

        assert len(debugger.queries) == 1
        assert debugger.queries[0]["is_slow"] is False


class TestDBDebuggerQueries:
    """DBDebugger 查询功能测试"""

    @pytest.fixture
    def debugger_with_data(self):
        """创建带数据的调试器"""
        debugger = DBDebugger(slow_query_threshold_ms=10)

        # 快速查询
        debugger.log_query_start("SELECT 1")
        debugger.log_query_end(result_count=1)

        # 慢查询
        debugger.log_query_start("SELECT * FROM large_table")
        time.sleep(0.02)  # 20ms
        debugger.log_query_end(result_count=1000)

        # 失败查询
        debugger.log_query_start("SELECT * FROM nonexistent")
        debugger.log_query_error(Exception("Table not found"))

        return debugger

    def test_get_queries(self, debugger_with_data):
        """测试获取所有查询"""
        queries = debugger_with_data.get_queries()
        assert len(queries) == 3

    def test_get_slow_queries(self, debugger_with_data):
        """测试获取慢查询"""
        slow = debugger_with_data.get_slow_queries()
        assert len(slow) == 1
        assert "large_table" in slow[0]["sql"]

    def test_get_failed_queries(self, debugger_with_data):
        """测试获取失败查询"""
        failed = debugger_with_data.get_failed_queries()
        assert len(failed) == 1
        assert "nonexistent" in failed[0]["sql"]

    def test_get_statistics(self, debugger_with_data):
        """测试获取统计信息"""
        stats = debugger_with_data.get_statistics()

        assert stats["total_queries"] == 3
        assert stats["slow_queries"] == 1
        assert stats["failed_queries"] == 1
        assert stats["avg_duration_ms"] > 0
        assert stats["max_duration_ms"] >= stats["min_duration_ms"]

    def test_get_statistics_empty(self):
        """测试空统计"""
        debugger = DBDebugger()
        stats = debugger.get_statistics()
        assert stats == {}

    def test_print_summary(self, debugger_with_data, capsys):
        """测试打印摘要"""
        debugger_with_data.print_summary()

        captured = capsys.readouterr()
        assert "数据库查询摘要" in captured.out
        assert "总查询数: 3" in captured.out
        assert "慢查询: 1" in captured.out
        assert "失败: 1" in captured.out
        assert "慢查询详情" in captured.out
        assert "失败查询详情" in captured.out

    def test_print_summary_empty(self, capsys):
        """测试空摘要"""
        debugger = DBDebugger()
        debugger.print_summary()

        captured = capsys.readouterr()
        assert "无查询记录" in captured.out


class TestDBDebuggerTruncation:
    """DBDebugger 截断功能测试"""

    def test_truncate_long_sql(self):
        """测试截断长 SQL"""
        debugger = DBDebugger(max_sql_length=50)
        long_sql = "SELECT " + ", ".join([f"col{i}" for i in range(100)]) + " FROM table"

        debugger.log_query_start(long_sql)
        debugger.log_query_end(result_count=1)

        assert debugger.queries[0]["sql"].endswith("...")

    def test_truncate_with_custom_length(self):
        """测试自定义截断长度"""
        debugger = DBDebugger()
        long_sql = "x" * 200

        truncated = debugger._truncate_sql(long_sql, max_length=50)
        assert len(truncated) == 53  # 50 + "..."


class TestGlobalDBDebugger:
    """全局数据库调试器测试"""

    def setup_method(self):
        """每个测试前重置全局调试器"""
        import df_test_framework.testing.debugging.database as db_module

        db_module._global_db_debugger = None

    def test_enable_disable(self):
        """测试启用和禁用全局调试器"""
        debugger = enable_db_debug()
        assert debugger is not None
        assert debugger.enabled is True

        disable_db_debug()
        assert debugger.enabled is False

    def test_get_global_debugger(self):
        """测试获取全局调试器"""
        enable_db_debug()
        debugger = get_global_db_debugger()
        assert debugger is not None

    def test_enable_with_custom_threshold(self):
        """测试自定义慢查询阈值"""
        debugger = enable_db_debug(slow_query_threshold_ms=50)
        assert debugger.slow_query_threshold_ms == 50
