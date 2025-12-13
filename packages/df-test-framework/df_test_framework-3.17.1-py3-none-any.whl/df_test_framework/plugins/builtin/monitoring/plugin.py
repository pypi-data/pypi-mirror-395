"""
监控插件实现

v3.14.0: 基于新的插件系统重构。
"""

from typing import Any

from df_test_framework.core.events import DatabaseQueryEndEvent, HttpRequestEndEvent
from df_test_framework.infrastructure.events import EventBus
from df_test_framework.infrastructure.plugins import hookimpl


class MonitoringPlugin:
    """监控插件

    提供：
    - API 调用统计
    - 数据库查询监控
    - 性能指标收集

    通过事件订阅实现监控，与 v3.x 的 Tracker 类似。
    """

    def __init__(self):
        self._api_calls: list[dict[str, Any]] = []
        self._db_queries: list[dict[str, Any]] = []
        self._enabled = True

    @hookimpl
    def df_event_handlers(self, event_bus: EventBus) -> list[Any]:
        """注册事件处理器"""
        handlers = []

        @event_bus.on(HttpRequestEndEvent)
        async def track_http(event: HttpRequestEndEvent) -> None:
            if self._enabled:
                self._api_calls.append(
                    {
                        "method": event.method,
                        "url": event.url,
                        "status_code": event.status_code,
                        "duration": event.duration,
                        "timestamp": event.timestamp.isoformat(),
                    }
                )

        handlers.append(track_http)

        @event_bus.on(DatabaseQueryEndEvent)
        async def track_db(event: DatabaseQueryEndEvent) -> None:
            if self._enabled:
                self._db_queries.append(
                    {
                        "sql": event.sql,
                        "duration": event.duration,
                        "row_count": event.row_count,
                        "timestamp": event.timestamp.isoformat(),
                    }
                )

        handlers.append(track_db)

        return handlers

    @property
    def api_calls(self) -> list[dict[str, Any]]:
        """获取 API 调用记录"""
        return self._api_calls.copy()

    @property
    def db_queries(self) -> list[dict[str, Any]]:
        """获取数据库查询记录"""
        return self._db_queries.copy()

    def clear(self) -> None:
        """清空所有记录"""
        self._api_calls.clear()
        self._db_queries.clear()

    def enable(self) -> None:
        """启用监控"""
        self._enabled = True

    def disable(self) -> None:
        """禁用监控"""
        self._enabled = False

    def get_summary(self) -> dict[str, Any]:
        """获取监控摘要"""
        api_count = len(self._api_calls)
        db_count = len(self._db_queries)

        api_total_duration = sum(c["duration"] for c in self._api_calls)
        db_total_duration = sum(q["duration"] for q in self._db_queries)

        return {
            "api_calls": {
                "count": api_count,
                "total_duration": api_total_duration,
                "avg_duration": api_total_duration / api_count if api_count else 0,
            },
            "db_queries": {
                "count": db_count,
                "total_duration": db_total_duration,
                "avg_duration": db_total_duration / db_count if db_count else 0,
            },
        }
