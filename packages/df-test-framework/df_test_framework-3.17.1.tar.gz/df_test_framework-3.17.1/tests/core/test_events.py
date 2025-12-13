"""
测试 infrastructure.events - 事件总线系统

v3.14.0 新增：
- EventBus 发布/订阅模式
- 事件类型定义
- 异步事件处理
"""

import asyncio

import pytest

from df_test_framework.core.events import (
    DatabaseQueryEndEvent,
    Event,
    HttpRequestEndEvent,
    HttpRequestStartEvent,
)
from df_test_framework.infrastructure.events import EventBus


# ==================== 自定义测试事件 ====================
class CustomTestEvent(Event):
    """自定义测试事件"""

    def __init__(self, message: str, value: int):
        super().__init__()
        self.message = message
        self.value = value


class AnotherTestEvent(Event):
    """另一个测试事件"""

    def __init__(self, data: str):
        super().__init__()
        self.data = data


# ==================== 测试 EventBus 基本功能 ====================
class TestEventBusBasics:
    """测试 EventBus 基本功能"""

    @pytest.mark.asyncio
    async def test_create_event_bus(self):
        """测试创建事件总线"""
        bus = EventBus()
        assert bus is not None

    @pytest.mark.asyncio
    async def test_subscribe_and_publish(self):
        """测试订阅和发布事件"""
        bus = EventBus()
        received_events = []

        async def handler(event: CustomTestEvent):
            received_events.append(event)

        bus.subscribe(CustomTestEvent, handler)

        # 发布事件
        event = CustomTestEvent(message="test", value=42)
        await bus.publish(event)

        # 验证处理器被调用
        assert len(received_events) == 1
        assert received_events[0].message == "test"
        assert received_events[0].value == 42

    @pytest.mark.asyncio
    async def test_multiple_handlers_for_same_event(self):
        """测试同一事件的多个处理器"""
        bus = EventBus()
        call_order = []

        async def handler1(event: CustomTestEvent):
            call_order.append("handler1")

        async def handler2(event: CustomTestEvent):
            call_order.append("handler2")

        async def handler3(event: CustomTestEvent):
            call_order.append("handler3")

        bus.subscribe(CustomTestEvent, handler1)
        bus.subscribe(CustomTestEvent, handler2)
        bus.subscribe(CustomTestEvent, handler3)

        event = CustomTestEvent(message="test", value=1)
        await bus.publish(event)

        # 验证所有处理器都被调用（并发执行，顺序不保证）
        assert set(call_order) == {"handler1", "handler2", "handler3"}
        assert len(call_order) == 3

    @pytest.mark.asyncio
    async def test_different_event_types(self):
        """测试不同类型的事件"""
        bus = EventBus()
        custom_events = []
        another_events = []

        async def custom_handler(event: CustomTestEvent):
            custom_events.append(event)

        async def another_handler(event: AnotherTestEvent):
            another_events.append(event)

        bus.subscribe(CustomTestEvent, custom_handler)
        bus.subscribe(AnotherTestEvent, another_handler)

        # 发布不同类型的事件
        await bus.publish(CustomTestEvent(message="custom", value=1))
        await bus.publish(AnotherTestEvent(data="another"))
        await bus.publish(CustomTestEvent(message="custom2", value=2))

        # 验证处理器只接收对应类型的事件
        assert len(custom_events) == 2
        assert len(another_events) == 1
        assert custom_events[0].message == "custom"
        assert another_events[0].data == "another"

    @pytest.mark.asyncio
    async def test_publish_without_handlers(self):
        """测试发布没有处理器的事件"""
        bus = EventBus()

        # 不应该抛出异常
        await bus.publish(CustomTestEvent(message="no handler", value=0))


# ==================== 测试装饰器语法 ====================
class TestEventBusDecorator:
    """测试装饰器语法"""

    @pytest.mark.asyncio
    async def test_on_decorator(self):
        """测试 @bus.on() 装饰器"""
        bus = EventBus()
        received = []

        @bus.on(CustomTestEvent)
        async def handle_event(event: CustomTestEvent):
            received.append(event.message)

        await bus.publish(CustomTestEvent(message="decorated", value=1))

        assert len(received) == 1
        assert received[0] == "decorated"

    @pytest.mark.asyncio
    async def test_multiple_decorated_handlers(self):
        """测试多个装饰器处理器"""
        bus = EventBus()
        results = []

        @bus.on(CustomTestEvent)
        async def handler1(event: CustomTestEvent):
            results.append(f"h1:{event.value}")

        @bus.on(CustomTestEvent)
        async def handler2(event: CustomTestEvent):
            results.append(f"h2:{event.value}")

        await bus.publish(CustomTestEvent(message="test", value=42))

        assert len(results) == 2
        assert "h1:42" in results
        assert "h2:42" in results


# ==================== 测试全局订阅 ====================
class TestEventBusGlobalSubscribe:
    """测试全局订阅功能"""

    @pytest.mark.asyncio
    async def test_subscribe_all(self):
        """测试订阅所有事件"""
        bus = EventBus()
        all_events = []

        async def global_handler(event: Event):
            all_events.append(type(event).__name__)

        bus.subscribe_all(global_handler)

        # 发布不同类型的事件
        await bus.publish(CustomTestEvent(message="test1", value=1))
        await bus.publish(AnotherTestEvent(data="test2"))
        await bus.publish(
            HttpRequestEndEvent(method="GET", url="/api", status_code=200, duration=0.5)
        )

        # 验证全局处理器接收所有事件
        assert len(all_events) == 3
        assert "CustomTestEvent" in all_events
        assert "AnotherTestEvent" in all_events
        assert "HttpRequestEndEvent" in all_events

    @pytest.mark.asyncio
    async def test_subscribe_all_and_specific(self):
        """测试全局订阅和特定订阅同时存在"""
        bus = EventBus()
        global_events = []
        custom_events = []

        async def global_handler(event: Event):
            global_events.append(event)

        async def custom_handler(event: CustomTestEvent):
            custom_events.append(event)

        bus.subscribe_all(global_handler)
        bus.subscribe(CustomTestEvent, custom_handler)

        event = CustomTestEvent(message="test", value=1)
        await bus.publish(event)

        # 验证两个处理器都被调用
        assert len(global_events) == 1
        assert len(custom_events) == 1


# ==================== 测试取消订阅 ====================
class TestEventBusUnsubscribe:
    """测试取消订阅"""

    @pytest.mark.asyncio
    async def test_unsubscribe(self):
        """测试取消订阅"""
        bus = EventBus()
        received = []

        async def handler(event: CustomTestEvent):
            received.append(event)

        bus.subscribe(CustomTestEvent, handler)

        # 发布第一个事件
        await bus.publish(CustomTestEvent(message="before", value=1))
        assert len(received) == 1

        # 取消订阅
        bus.unsubscribe(CustomTestEvent, handler)

        # 发布第二个事件
        await bus.publish(CustomTestEvent(message="after", value=2))

        # 验证取消订阅后不再接收事件
        assert len(received) == 1

    @pytest.mark.asyncio
    async def test_unsubscribe_all(self):
        """测试取消全局订阅"""
        bus = EventBus()
        received = []

        async def handler(event: Event):
            received.append(event)

        bus.subscribe_all(handler)

        await bus.publish(CustomTestEvent(message="before", value=1))
        assert len(received) == 1

        # 取消全局订阅
        bus.unsubscribe_all(handler)

        await bus.publish(CustomTestEvent(message="after", value=2))

        # 验证取消订阅后不再接收事件
        assert len(received) == 1

    @pytest.mark.asyncio
    async def test_unsubscribe_nonexistent_handler(self):
        """测试取消不存在的处理器"""
        bus = EventBus()

        async def handler(event: CustomTestEvent):
            pass

        # 不应该抛出异常
        bus.unsubscribe(CustomTestEvent, handler)
        bus.unsubscribe_all(handler)


# ==================== 测试异常处理 ====================
class TestEventBusErrorHandling:
    """测试异常处理"""

    @pytest.mark.asyncio
    async def test_handler_exception_does_not_affect_other_handlers(self):
        """测试处理器异常不影响其他处理器"""
        bus = EventBus()
        results = []

        async def failing_handler(event: CustomTestEvent):
            raise ValueError("Handler failed")

        async def success_handler1(event: CustomTestEvent):
            results.append("success1")

        async def success_handler2(event: CustomTestEvent):
            results.append("success2")

        bus.subscribe(CustomTestEvent, success_handler1)
        bus.subscribe(CustomTestEvent, failing_handler)
        bus.subscribe(CustomTestEvent, success_handler2)

        # 发布事件
        await bus.publish(CustomTestEvent(message="test", value=1))

        # 验证成功的处理器仍然执行
        assert len(results) == 2
        assert "success1" in results
        assert "success2" in results

    @pytest.mark.asyncio
    async def test_all_handlers_fail(self):
        """测试所有处理器都失败"""
        bus = EventBus()

        async def failing_handler1(event: CustomTestEvent):
            raise ValueError("Handler 1 failed")

        async def failing_handler2(event: CustomTestEvent):
            raise RuntimeError("Handler 2 failed")

        bus.subscribe(CustomTestEvent, failing_handler1)
        bus.subscribe(CustomTestEvent, failing_handler2)

        # 不应该抛出异常到调用者
        await bus.publish(CustomTestEvent(message="test", value=1))


# ==================== 测试异步并发 ====================
class TestEventBusAsyncConcurrency:
    """测试异步并发处理"""

    @pytest.mark.asyncio
    async def test_concurrent_handler_execution(self):
        """测试处理器并发执行"""
        bus = EventBus()
        execution_order = []

        async def slow_handler(event: CustomTestEvent):
            await asyncio.sleep(0.1)
            execution_order.append("slow")

        async def fast_handler(event: CustomTestEvent):
            await asyncio.sleep(0.01)
            execution_order.append("fast")

        bus.subscribe(CustomTestEvent, slow_handler)
        bus.subscribe(CustomTestEvent, fast_handler)

        start = asyncio.get_event_loop().time()
        await bus.publish(CustomTestEvent(message="test", value=1))
        duration = asyncio.get_event_loop().time() - start

        # 验证并发执行（总时间应该接近最慢的处理器）
        assert duration < 0.15  # 并发执行，不是 0.11 秒
        assert len(execution_order) == 2

    @pytest.mark.asyncio
    async def test_handler_can_be_async(self):
        """测试处理器必须是异步的"""
        bus = EventBus()
        received = []

        async def async_handler(event: CustomTestEvent):
            await asyncio.sleep(0.01)
            received.append(event.message)

        bus.subscribe(CustomTestEvent, async_handler)
        await bus.publish(CustomTestEvent(message="async_test", value=1))

        assert len(received) == 1
        assert received[0] == "async_test"


# ==================== 测试框架内置事件 ====================
class TestFrameworkEvents:
    """测试框架内置事件类型"""

    @pytest.mark.asyncio
    async def test_http_request_end_event(self):
        """测试 HttpRequestEndEvent"""
        bus = EventBus()
        received = []

        async def handler(event: HttpRequestEndEvent):
            received.append(
                {
                    "method": event.method,
                    "url": event.url,
                    "status": event.status_code,
                    "duration": event.duration,
                }
            )

        bus.subscribe(HttpRequestEndEvent, handler)

        await bus.publish(
            HttpRequestEndEvent(method="POST", url="/api/users", status_code=201, duration=0.35)
        )

        assert len(received) == 1
        assert received[0]["method"] == "POST"
        assert received[0]["url"] == "/api/users"
        assert received[0]["status"] == 201
        assert received[0]["duration"] == 0.35

    @pytest.mark.asyncio
    async def test_database_query_end_event(self):
        """测试 DatabaseQueryEndEvent

        v3.18.0: 更新字段名 duration -> duration_ms，添加 operation/table 字段
        """
        bus = EventBus()
        received = []

        async def handler(event: DatabaseQueryEndEvent):
            received.append(
                {
                    "sql": event.sql,
                    "operation": event.operation,
                    "table": event.table,
                    "duration_ms": event.duration_ms,
                    "rows": event.row_count,
                }
            )

        bus.subscribe(DatabaseQueryEndEvent, handler)

        await bus.publish(
            DatabaseQueryEndEvent(
                operation="SELECT",
                table="users",
                sql="SELECT * FROM users WHERE id = ?",
                params={"id": 1},
                duration_ms=50.0,
                row_count=1,
            )
        )

        assert len(received) == 1
        assert "SELECT * FROM users" in received[0]["sql"]
        assert received[0]["operation"] == "SELECT"
        assert received[0]["table"] == "users"
        assert received[0]["duration_ms"] == 50.0
        assert received[0]["rows"] == 1


# ==================== 测试实际使用场景 ====================
class TestEventBusRealWorldScenarios:
    """测试实际使用场景"""

    @pytest.mark.asyncio
    async def test_http_request_logging_scenario(self):
        """测试 HTTP 请求日志场景"""
        bus = EventBus()
        log_entries = []

        @bus.on(HttpRequestStartEvent)
        async def log_request_start(event: HttpRequestStartEvent):
            log_entries.append(f"[START] {event.method} {event.url}")

        @bus.on(HttpRequestEndEvent)
        async def log_request_end(event: HttpRequestEndEvent):
            log_entries.append(
                f"[END] {event.method} {event.url} -> {event.status_code} ({event.duration:.2f}s)"
            )

        # 模拟 HTTP 请求
        await bus.publish(HttpRequestStartEvent(method="GET", url="/api/users"))
        await bus.publish(
            HttpRequestEndEvent(method="GET", url="/api/users", status_code=200, duration=0.123)
        )

        assert len(log_entries) == 2
        assert "[START] GET /api/users" in log_entries[0]
        assert "[END] GET /api/users -> 200 (0.12s)" in log_entries[1]

    @pytest.mark.asyncio
    async def test_metrics_collection_scenario(self):
        """测试指标收集场景"""
        bus = EventBus()
        metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_duration": 0.0,
        }

        @bus.on(HttpRequestEndEvent)
        async def collect_metrics(event: HttpRequestEndEvent):
            metrics["total_requests"] += 1
            metrics["total_duration"] += event.duration
            if 200 <= event.status_code < 400:
                metrics["successful_requests"] += 1
            else:
                metrics["failed_requests"] += 1

        # 模拟多个请求
        await bus.publish(
            HttpRequestEndEvent(method="GET", url="/api/users", status_code=200, duration=0.1)
        )
        await bus.publish(
            HttpRequestEndEvent(method="POST", url="/api/users", status_code=201, duration=0.2)
        )
        await bus.publish(
            HttpRequestEndEvent(method="GET", url="/api/orders", status_code=404, duration=0.05)
        )
        await bus.publish(
            HttpRequestEndEvent(method="GET", url="/api/products", status_code=500, duration=0.15)
        )

        # 验证指标
        assert metrics["total_requests"] == 4
        assert metrics["successful_requests"] == 2
        assert metrics["failed_requests"] == 2
        assert metrics["total_duration"] == 0.5
