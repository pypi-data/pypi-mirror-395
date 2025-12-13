"""数据库查询调试工具

记录SQL查询并提供慢查询分析。
"""

from __future__ import annotations

import logging
import time
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


class DBDebugger:
    """数据库调试器

    记录所有SQL查询，分析慢查询，提供统计信息。

    Example:
        >>> debugger = DBDebugger(slow_query_threshold_ms=100)
        >>> debugger.start()
        >>> debugger.log_query_start("SELECT * FROM users WHERE id = %s", (1,))
        >>> debugger.log_query_end(result_count=1)
        >>> debugger.print_summary()
    """

    def __init__(
        self,
        enabled: bool = True,
        slow_query_threshold_ms: int = 100,
        max_sql_length: int = 500,
    ):
        """初始化数据库调试器

        Args:
            enabled: 是否启用调试
            slow_query_threshold_ms: 慢查询阈值（毫秒）
            max_sql_length: 最大记录的SQL长度
        """
        self.enabled = enabled
        self.slow_query_threshold_ms = slow_query_threshold_ms
        self.max_sql_length = max_sql_length
        self.queries: list[dict[str, Any]] = []
        self._query_start_time: float | None = None
        self._current_query: dict[str, Any] | None = None

    def start(self):
        """启动调试"""
        self.enabled = True
        logger.info(f"🔍 数据库调试已启用（慢查询阈值: {self.slow_query_threshold_ms}ms）")

    def stop(self):
        """停止调试"""
        self.enabled = False
        logger.info("⏹️  数据库调试已停止")

    def clear(self):
        """清空调试记录"""
        self.queries.clear()
        self._query_start_time = None
        self._current_query = None

    def log_query_start(self, sql: str, params: tuple | None = None):
        """记录查询开始

        Args:
            sql: SQL语句
            params: 查询参数
        """
        if not self.enabled:
            return

        self._query_start_time = time.time()
        self._current_query = {
            "timestamp": datetime.now().isoformat(),
            "sql": self._truncate_sql(sql),
            "params": params,
            "duration_ms": None,
            "result_count": None,
            "is_slow": False,
        }

        # v3: 同时输出到stdout (pytest -s可见) 和logger
        print(f"[DB DEBUG] SQL: {self._truncate_sql(sql)}")
        if params:
            print(f"[DB DEBUG] Params: {params}")
        logger.debug(f"🔍 查询: {self._truncate_sql(sql, 100)}")

    def log_query_end(self, result_count: int | None = None):
        """记录查询结束

        Args:
            result_count: 结果数量
        """
        if not self.enabled or not self._current_query:
            return

        duration_ms = (time.time() - self._query_start_time) * 1000

        self._current_query["duration_ms"] = duration_ms
        self._current_query["result_count"] = result_count
        self._current_query["is_slow"] = duration_ms > self.slow_query_threshold_ms

        self.queries.append(self._current_query.copy())

        # v3: 同时输出到stdout (pytest -s可见) 和logger
        print(f"[DB DEBUG] Result: {result_count} row(s) in {duration_ms:.2f}ms")

        # 根据查询时间使用不同的日志级别
        if self._current_query["is_slow"]:
            logger.warning(f"🐌 慢查询: {duration_ms:.2f}ms (阈值{self.slow_query_threshold_ms}ms)")
        else:
            logger.debug(f"✅ 查询完成: {duration_ms:.2f}ms")

        self._current_query = None
        self._query_start_time = None

    def log_query_error(self, error: Exception):
        """记录查询错误

        Args:
            error: 异常对象
        """
        if not self.enabled or not self._current_query:
            return

        duration_ms = (time.time() - self._query_start_time) * 1000

        self._current_query["duration_ms"] = duration_ms
        self._current_query["error"] = str(error)
        self._current_query["error_type"] = type(error).__name__

        self.queries.append(self._current_query.copy())
        logger.error(f"❌ 查询错误: {error} ({duration_ms:.2f}ms)")

        self._current_query = None
        self._query_start_time = None

    def get_queries(self) -> list[dict[str, Any]]:
        """获取所有查询记录

        Returns:
            List[Dict]: 查询记录列表
        """
        return self.queries.copy()

    def get_slow_queries(self) -> list[dict[str, Any]]:
        """获取慢查询列表

        Returns:
            List[Dict]: 慢查询列表
        """
        return [q for q in self.queries if q.get("is_slow", False)]

    def get_failed_queries(self) -> list[dict[str, Any]]:
        """获取失败的查询

        Returns:
            List[Dict]: 失败的查询列表
        """
        return [q for q in self.queries if "error" in q]

    def get_statistics(self) -> dict[str, Any]:
        """获取查询统计

        Returns:
            Dict: 统计信息
        """
        if not self.queries:
            return {}

        durations = [q["duration_ms"] for q in self.queries if q["duration_ms"]]

        return {
            "total_queries": len(self.queries),
            "slow_queries": len(self.get_slow_queries()),
            "failed_queries": len(self.get_failed_queries()),
            "avg_duration_ms": sum(durations) / len(durations) if durations else 0,
            "max_duration_ms": max(durations) if durations else 0,
            "min_duration_ms": min(durations) if durations else 0,
            "total_duration_ms": sum(durations) if durations else 0,
        }

    def print_summary(self):
        """打印调试摘要"""
        if not self.queries:
            print("\n📊 数据库调试摘要: 无查询记录")
            return

        stats = self.get_statistics()

        print("\n" + "=" * 80)
        print("📊 数据库查询摘要")
        print("=" * 80)

        print(f"\n总查询数: {stats['total_queries']}")
        print(f"  慢查询: {stats['slow_queries']} ⚠️")
        print(f"  失败: {stats['failed_queries']} ❌")

        print("\n查询耗时:")
        print(f"  平均: {stats['avg_duration_ms']:.2f}ms")
        print(f"  最快: {stats['min_duration_ms']:.2f}ms")
        print(f"  最慢: {stats['max_duration_ms']:.2f}ms")
        print(f"  总计: {stats['total_duration_ms']:.2f}ms")

        # 慢查询详情
        slow_queries = self.get_slow_queries()
        if slow_queries:
            print("\n" + "=" * 80)
            print(f"🐌 慢查询详情 (阈值: {self.slow_query_threshold_ms}ms):")
            print("=" * 80)

            for i, query in enumerate(slow_queries, 1):
                self._print_query_detail(i, query)

        # 失败查询详情
        failed_queries = self.get_failed_queries()
        if failed_queries:
            print("\n" + "=" * 80)
            print("❌ 失败查询详情:")
            print("=" * 80)

            for i, query in enumerate(failed_queries, 1):
                self._print_query_detail(i, query)

        print("=" * 80)

    def _print_query_detail(self, index: int, query: dict[str, Any]):
        """打印单个查询详情"""
        print(f"\n{index}. {query['sql'][:100]}...")
        print(f"   时间: {query['timestamp']}")
        print(f"   耗时: {query.get('duration_ms', 0):.2f}ms")

        if query.get("params"):
            print(f"   参数: {query['params']}")

        if query.get("result_count") is not None:
            print(f"   结果数: {query['result_count']}")

        if "error" in query:
            print(f"   错误: {query['error']}")

    def _truncate_sql(self, sql: str, max_length: int | None = None) -> str:
        """截断SQL（如果太长）"""
        max_len = max_length or self.max_sql_length
        if len(sql) > max_len:
            return sql[:max_len] + "..."
        return sql


# 全局调试器实例
_global_db_debugger: DBDebugger | None = None


def enable_db_debug(slow_query_threshold_ms: int = 100) -> DBDebugger:
    """启用全局数据库调试

    Args:
        slow_query_threshold_ms: 慢查询阈值（毫秒）

    Returns:
        DBDebugger: 调试器实例

    Example:
        >>> debugger = enable_db_debug(threshold=50)
        >>> # 执行数据库操作
        >>> debugger.print_summary()
    """
    global _global_db_debugger
    if _global_db_debugger is None:
        _global_db_debugger = DBDebugger(
            enabled=True, slow_query_threshold_ms=slow_query_threshold_ms
        )
    else:
        _global_db_debugger.start()
    return _global_db_debugger


def disable_db_debug():
    """禁用全局数据库调试"""
    global _global_db_debugger
    if _global_db_debugger:
        _global_db_debugger.stop()


def get_global_db_debugger() -> DBDebugger | None:
    """获取全局数据库调试器实例"""
    return _global_db_debugger


__all__ = [
    "DBDebugger",
    "enable_db_debug",
    "disable_db_debug",
    "get_global_db_debugger",
]
