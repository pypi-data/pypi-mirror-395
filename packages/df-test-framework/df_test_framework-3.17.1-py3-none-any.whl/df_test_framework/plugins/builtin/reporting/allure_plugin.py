"""Allure 报告插件

⚠️ **DEPRECATED (v3.18.0)** ⚠️

此插件已被标记为废弃，将在 v4.0.0 移除。

废弃原因：
- 框架的 Allure 集成已通过 testing/fixtures/allure.py 的 pytest fixture 完整实现
- Fixture 方式提供更好的测试隔离（每个测试独立 EventBus）
- 符合能力层优化计划的设计意图（纯 EventBus 驱动 + Fixture 集成）
- 两套并行机制导致架构混乱和维护成本增加

推荐使用方式：
- ✅ 默认使用 Pytest Fixture 集成（无需任何配置，自动生效）
- ✅ 所有能力层事件自动记录到 Allure 报告
- ✅ 测试级 EventBus 确保测试隔离，无状态污染

如果你之前配置了此插件：
    # pyproject.toml
    df_plugins = "df_test_framework.plugins.builtin.reporting.allure_plugin"  # 可以安全移除

迁移指南：
1. 移除 pyproject.toml 中的 df_plugins 配置
2. 无需任何代码修改，Fixture 方式自动生效
3. 如有非 pytest 场景需求，请参考：
   docs/architecture/future_allure_plugin_plans.md（方案 B）

版本历史：
- v3.14.0: 基于新的插件系统和事件总线重构
- v3.17.1: 完善所有能力层事件支持
- v3.18.0: 标记为 DEPRECATED，推荐使用 Fixture 方式
- v4.0.0: 计划移除（未来）

参考文档：
- docs/architecture/allure_integration_modes.md - 架构分析与方案对比
- docs/architecture/capability_plan_vs_current.md - 优化计划对比分析
- docs/architecture/future_allure_plugin_plans.md - 未来演进方案
"""

import json
from typing import Any

from df_test_framework.core.events import (
    CacheOperationEndEvent,
    CacheOperationErrorEvent,
    CacheOperationStartEvent,
    DatabaseQueryEndEvent,
    DatabaseQueryErrorEvent,
    DatabaseQueryStartEvent,
    HttpRequestEndEvent,
    HttpRequestErrorEvent,
    HttpRequestStartEvent,
    MessageConsumeEvent,
    MessagePublishEvent,
    MiddlewareExecuteEvent,
    StorageOperationEndEvent,
    StorageOperationErrorEvent,
    StorageOperationStartEvent,
)
from df_test_framework.infrastructure.events import EventBus
from df_test_framework.infrastructure.plugins import hookimpl


class AllurePlugin:
    """Allure 报告插件（Plugin 模式）

    ⚠️ **DEPRECATED (v3.18.0)** - 将在 v4.0.0 移除

    此类已被标记为废弃。请使用框架内置的 Pytest Fixture 集成方式。

    废弃说明：
    - 框架通过 testing/fixtures/allure.py 提供完整的 Allure 集成
    - Fixture 方式提供更好的测试隔离和自动化
    - 无需任何配置，自动生效

    如果你必须使用此插件（不推荐）：
    1. 明确你的使用场景（非 pytest 场景？）
    2. 参考未来演进方案：docs/architecture/future_allure_plugin_plans.md
    3. 考虑在 v4.0.0 前迁移到 Fixture 方式

    功能（保留用于文档目的）：
    - ✅ HTTP Client (请求/响应/错误/中间件)
    - ✅ Database (查询开始/结束/错误)
    - ✅ Redis/Cache (操作开始/结束/错误)
    - ✅ Message Queue (发布/消费)
    - ✅ Storage (操作开始/结束/错误)
    """

    def __init__(self, enabled: bool = True):
        """初始化插件

        ⚠️ DEPRECATED: 不推荐使用此类，请使用 Pytest Fixture 集成

        Args:
            enabled: 是否启用插件
        """
        import warnings

        warnings.warn(
            "AllurePlugin is deprecated since v3.18.0 and will be removed in v4.0.0. "
            "The framework now uses Pytest Fixture integration automatically. "
            "Please remove 'df_plugins' configuration from pyproject.toml. "
            "See docs/architecture/allure_integration_modes.md for details.",
            DeprecationWarning,
            stacklevel=2,
        )

        self._enabled = enabled
        self._allure_available = self._check_allure()
        self._event_bus = None  # 可选：外部传入的 EventBus

    def _check_allure(self) -> bool:
        """检查 Allure 是否可用"""
        try:
            import allure  # noqa: F401

            return True
        except ImportError:
            return False

    def attach_to_event_bus(self, event_bus: EventBus) -> None:
        """附加到外部 EventBus（用于测试隔离）

        Args:
            event_bus: 外部 EventBus 实例（通常是测试级 EventBus）
        """
        if not self._allure_available or not self._enabled:
            return

        self._event_bus = event_bus
        handlers = self._create_handlers(event_bus)

        # 手动订阅所有处理器
        for handler in handlers:
            # handlers 已经通过 @event_bus.on() 装饰器注册
            pass

    @hookimpl
    def df_event_handlers(self, event_bus: EventBus) -> list[Any]:
        """注册事件处理器（Pluggy Hook）

        Args:
            event_bus: 框架的全局 EventBus

        Returns:
            事件处理器列表
        """
        if not self._allure_available or not self._enabled:
            return []

        return self._create_handlers(event_bus)

    def _create_handlers(self, event_bus: EventBus) -> list[Any]:
        """创建所有事件处理器

        Args:
            event_bus: EventBus 实例

        Returns:
            处理器函数列表
        """
        handlers = []

        # ========== HTTP Client 事件 ==========

        @event_bus.on(HttpRequestStartEvent)
        def record_http_start(event: HttpRequestStartEvent) -> None:
            """记录 HTTP 请求开始"""
            # 简化版本：仅在结束时记录
            pass

        handlers.append(record_http_start)

        @event_bus.on(HttpRequestEndEvent)
        def record_http_end(event: HttpRequestEndEvent) -> None:
            """记录 HTTP 请求结束"""
            import allure

            status_emoji = "✓" if 200 <= event.status_code < 300 else "✗"
            step_name = f"{event.method} {event.url} {status_emoji} {event.status_code}"

            with allure.step(step_name):
                details = {
                    "method": event.method,
                    "url": event.url,
                    "status_code": event.status_code,
                    "duration": f"{event.duration:.3f}s",
                    "timestamp": event.timestamp.isoformat(),
                }
                if hasattr(event, "trace_id") and event.trace_id:
                    details["trace_id"] = event.trace_id
                if hasattr(event, "span_id") and event.span_id:
                    details["span_id"] = event.span_id

                allure.attach(
                    json.dumps(details, indent=2, ensure_ascii=False),
                    name="Response Info",
                    attachment_type=allure.attachment_type.JSON,
                )

        handlers.append(record_http_end)

        @event_bus.on(HttpRequestErrorEvent)
        def record_http_error(event: HttpRequestErrorEvent) -> None:
            """记录 HTTP 请求错误"""
            import allure

            step_name = f"❌ {event.method} {event.url} - Error"

            with allure.step(step_name):
                error_details = {
                    "method": event.method,
                    "url": event.url,
                    "error_type": event.error_type,
                    "error_message": event.error_message,
                    "duration": f"{event.duration:.3f}s",
                }
                allure.attach(
                    json.dumps(error_details, indent=2, ensure_ascii=False),
                    name="Error Info",
                    attachment_type=allure.attachment_type.JSON,
                )

        handlers.append(record_http_error)

        @event_bus.on(MiddlewareExecuteEvent)
        def record_middleware(event: MiddlewareExecuteEvent) -> None:
            """记录中间件执行（可选，避免报告过于冗长）"""
            # 简化版本：不记录中间件详情，避免报告噪音
            pass

        handlers.append(record_middleware)

        # ========== Database 事件 ==========

        @event_bus.on(DatabaseQueryStartEvent)
        def record_db_start(event: DatabaseQueryStartEvent) -> None:
            """记录数据库查询开始"""
            # 简化版本：仅在结束时记录
            pass

        handlers.append(record_db_start)

        @event_bus.on(DatabaseQueryEndEvent)
        def record_db_end(event: DatabaseQueryEndEvent) -> None:
            """记录数据库查询结束"""
            import allure

            operation = getattr(event, "operation", "QUERY")
            table = getattr(event, "table", "unknown")
            duration_ms = getattr(event, "duration_ms", 0)
            row_count = getattr(event, "row_count", 0)

            step_name = f"🗄️ {operation} {table} ({duration_ms:.2f}ms, {row_count} rows)"

            with allure.step(step_name):
                details = {
                    "operation": operation,
                    "table": table,
                    "sql": getattr(event, "sql", ""),
                    "duration_ms": duration_ms,
                    "row_count": row_count,
                }
                if hasattr(event, "trace_id") and event.trace_id:
                    details["trace_id"] = event.trace_id

                allure.attach(
                    json.dumps(details, indent=2, ensure_ascii=False),
                    name="Query Info",
                    attachment_type=allure.attachment_type.JSON,
                )

        handlers.append(record_db_end)

        @event_bus.on(DatabaseQueryErrorEvent)
        def record_db_error(event: DatabaseQueryErrorEvent) -> None:
            """记录数据库查询错误"""
            import allure

            operation = getattr(event, "operation", "QUERY")
            table = getattr(event, "table", "unknown")

            step_name = f"❌ {operation} {table} - Error"

            with allure.step(step_name):
                error_details = {
                    "operation": operation,
                    "table": table,
                    "error_type": getattr(event, "error_type", "UnknownError"),
                    "error_message": getattr(event, "error_message", ""),
                    "sql": getattr(event, "sql", ""),
                }
                allure.attach(
                    json.dumps(error_details, indent=2, ensure_ascii=False),
                    name="Error Info",
                    attachment_type=allure.attachment_type.JSON,
                )

        handlers.append(record_db_error)

        # ========== Redis/Cache 事件 ==========

        @event_bus.on(CacheOperationStartEvent)
        def record_cache_start(event: CacheOperationStartEvent) -> None:
            """记录缓存操作开始"""
            pass

        handlers.append(record_cache_start)

        @event_bus.on(CacheOperationEndEvent)
        def record_cache_end(event: CacheOperationEndEvent) -> None:
            """记录缓存操作结束"""
            import allure

            operation = getattr(event, "operation", "UNKNOWN")
            key = getattr(event, "key", "")
            duration_ms = getattr(event, "duration_ms", 0)

            step_name = f"💾 Redis {operation} {key} ({duration_ms:.2f}ms)"

            with allure.step(step_name):
                details = {
                    "operation": operation,
                    "key": key,
                    "duration_ms": duration_ms,
                    "hit": getattr(event, "hit", None),
                }
                allure.attach(
                    json.dumps(details, indent=2, ensure_ascii=False),
                    name="Cache Info",
                    attachment_type=allure.attachment_type.JSON,
                )

        handlers.append(record_cache_end)

        @event_bus.on(CacheOperationErrorEvent)
        def record_cache_error(event: CacheOperationErrorEvent) -> None:
            """记录缓存操作错误"""
            import allure

            operation = getattr(event, "operation", "UNKNOWN")
            key = getattr(event, "key", "")

            step_name = f"❌ Redis {operation} {key} - Error"

            with allure.step(step_name):
                error_details = {
                    "operation": operation,
                    "key": key,
                    "error_type": getattr(event, "error_type", "UnknownError"),
                    "error_message": getattr(event, "error_message", ""),
                }
                allure.attach(
                    json.dumps(error_details, indent=2, ensure_ascii=False),
                    name="Error Info",
                    attachment_type=allure.attachment_type.JSON,
                )

        handlers.append(record_cache_error)

        # ========== Message Queue 事件 ==========

        @event_bus.on(MessagePublishEvent)
        def record_mq_publish(event: MessagePublishEvent) -> None:
            """记录消息发布"""
            import allure

            topic = getattr(event, "topic", "unknown")
            message_id = getattr(event, "message_id", "")

            step_name = f"📤 Publish to {topic}"

            with allure.step(step_name):
                details = {
                    "topic": topic,
                    "message_id": message_id,
                    "payload": str(getattr(event, "payload", ""))[:200],  # 截断
                }
                allure.attach(
                    json.dumps(details, indent=2, ensure_ascii=False),
                    name="Publish Info",
                    attachment_type=allure.attachment_type.JSON,
                )

        handlers.append(record_mq_publish)

        @event_bus.on(MessageConsumeEvent)
        def record_mq_consume(event: MessageConsumeEvent) -> None:
            """记录消息消费"""
            import allure

            topic = getattr(event, "topic", "unknown")
            message_id = getattr(event, "message_id", "")

            step_name = f"📥 Consume from {topic}"

            with allure.step(step_name):
                details = {
                    "topic": topic,
                    "message_id": message_id,
                    "payload": str(getattr(event, "payload", ""))[:200],
                }
                allure.attach(
                    json.dumps(details, indent=2, ensure_ascii=False),
                    name="Consume Info",
                    attachment_type=allure.attachment_type.JSON,
                )

        handlers.append(record_mq_consume)

        # ========== Storage 事件 ==========

        @event_bus.on(StorageOperationStartEvent)
        def record_storage_start(event: StorageOperationStartEvent) -> None:
            """记录存储操作开始"""
            pass

        handlers.append(record_storage_start)

        @event_bus.on(StorageOperationEndEvent)
        def record_storage_end(event: StorageOperationEndEvent) -> None:
            """记录存储操作结束"""
            import allure

            operation = getattr(event, "operation", "UNKNOWN")
            path = getattr(event, "path", "")
            duration_ms = getattr(event, "duration_ms", 0)

            step_name = f"📁 Storage {operation} {path} ({duration_ms:.2f}ms)"

            with allure.step(step_name):
                details = {
                    "operation": operation,
                    "path": path,
                    "duration_ms": duration_ms,
                    "size": getattr(event, "size", None),
                }
                allure.attach(
                    json.dumps(details, indent=2, ensure_ascii=False),
                    name="Storage Info",
                    attachment_type=allure.attachment_type.JSON,
                )

        handlers.append(record_storage_end)

        @event_bus.on(StorageOperationErrorEvent)
        def record_storage_error(event: StorageOperationErrorEvent) -> None:
            """记录存储操作错误"""
            import allure

            operation = getattr(event, "operation", "UNKNOWN")
            path = getattr(event, "path", "")

            step_name = f"❌ Storage {operation} {path} - Error"

            with allure.step(step_name):
                error_details = {
                    "operation": operation,
                    "path": path,
                    "error_type": getattr(event, "error_type", "UnknownError"),
                    "error_message": getattr(event, "error_message", ""),
                }
                allure.attach(
                    json.dumps(error_details, indent=2, ensure_ascii=False),
                    name="Error Info",
                    attachment_type=allure.attachment_type.JSON,
                )

        handlers.append(record_storage_error)

        return handlers

    @hookimpl
    def df_test_setup(self, request: Any, runtime: Any) -> None:
        """测试开始前添加元数据"""
        if not self._allure_available or not self._enabled:
            return

        import allure

        # 添加测试标签
        for marker in request.node.iter_markers():
            allure.dynamic.tag(marker.name)

    @hookimpl
    def df_test_teardown(self, request: Any, runtime: Any, outcome: Any) -> None:
        """测试结束后记录结果"""
        if not self._allure_available or not self._enabled:
            return

        # 可以在这里添加测试结束后的额外记录
        pass
