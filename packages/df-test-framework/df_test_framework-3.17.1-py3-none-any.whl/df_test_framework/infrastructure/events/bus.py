"""
事件总线实现

v3.17.0 重构:
- 添加 publish_sync() 同步发布方法
- 添加测试隔离支持（set_test_event_bus）
- 按注册顺序执行处理器（保证顺序）
"""

import asyncio
import logging
from collections.abc import Awaitable, Callable
from contextvars import ContextVar
from typing import TypeVar

from df_test_framework.core.events.types import Event
from df_test_framework.core.protocols.event import IEventBus

T = TypeVar("T", bound=Event)

EventHandler = Callable[[Event], Awaitable[None]]


class EventBus(IEventBus):
    """事件总线

    发布/订阅模式，解耦组件通信。

    特性：
    - 异步处理
    - 同步发布模式（v3.17.0）
    - 事件处理异常不影响主流程
    - 支持通配符订阅（subscribe_all）
    - 支持装饰器语法
    - 测试隔离（v3.17.0）

    示例:
        bus = EventBus()

        # 装饰器语法
        @bus.on(HttpRequestEndEvent)
        async def log_request(event: HttpRequestEndEvent):
            print(f"{event.method} {event.url} -> {event.status_code}")

        # 异步发布
        await bus.publish(event)

        # 同步发布（v3.17.0，推荐用于测试）
        bus.publish_sync(event)
    """

    def __init__(self, logger: logging.Logger | None = None):
        """初始化事件总线

        Args:
            logger: 日志对象
        """
        self._handlers: dict[type[Event], list[EventHandler]] = {}
        self._global_handlers: list[EventHandler] = []
        self._logger = logger or logging.getLogger(__name__)

    def subscribe(
        self,
        event_type: type[T],
        handler: Callable[[T], Awaitable[None]],
    ) -> None:
        """订阅特定类型事件

        Args:
            event_type: 事件类型
            handler: 事件处理器

        示例:
            async def handle_http(event: HttpRequestEndEvent):
                print(event.status_code)

            bus.subscribe(HttpRequestEndEvent, handle_http)
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)  # type: ignore
        self._logger.debug(f"Subscribed {handler.__name__} to {event_type.__name__}")

    def subscribe_all(self, handler: EventHandler) -> None:
        """订阅所有事件

        Args:
            handler: 事件处理器

        示例:
            async def log_all(event: Event):
                print(f"Event: {type(event).__name__}")

            bus.subscribe_all(log_all)
        """
        self._global_handlers.append(handler)
        self._logger.debug(f"Subscribed {handler.__name__} to all events")

    def unsubscribe(
        self,
        event_type: type[T],
        handler: Callable[[T], Awaitable[None]],
    ) -> None:
        """取消订阅

        Args:
            event_type: 事件类型
            handler: 事件处理器
        """
        if event_type in self._handlers:
            try:
                self._handlers[event_type].remove(handler)  # type: ignore
                self._logger.debug(f"Unsubscribed {handler.__name__} from {event_type.__name__}")
            except ValueError:
                pass

    def unsubscribe_all(self, handler: EventHandler) -> None:
        """取消订阅所有事件

        Args:
            handler: 事件处理器
        """
        try:
            self._global_handlers.remove(handler)
        except ValueError:
            pass

    async def publish(self, event: Event) -> None:
        """异步发布事件

        按注册顺序依次执行处理器（v3.17.0 改为顺序执行，保证处理顺序）。

        Args:
            event: 要发布的事件

        示例:
            await bus.publish(HttpRequestEndEvent(
                method="GET",
                url="/api",
                status_code=200,
                duration=0.5
            ))
        """
        handlers = self._handlers.get(type(event), []) + self._global_handlers

        if not handlers:
            return

        # v3.17.0: 按注册顺序依次执行（保证顺序，便于调试）
        for handler in handlers:
            await self._safe_call(handler, event)

    def publish_sync(self, event: Event) -> None:
        """同步发布事件（阻塞等待所有处理器完成）

        v3.17.0 新增：适用于测试场景，确保事件处理完成后再继续。

        Args:
            event: 要发布的事件

        示例:
            # 同步发布，等待所有处理器执行完成
            bus.publish_sync(HttpRequestStartEvent(...))

            # 执行操作...

            bus.publish_sync(HttpRequestEndEvent(...))
        """
        try:
            loop = asyncio.get_running_loop()
            # 如果已在事件循环中，需要使用 run_until_complete
            # 但这会导致嵌套事件循环错误，所以创建新协程
            future = asyncio.ensure_future(self.publish(event), loop=loop)
            loop.run_until_complete(future)
        except RuntimeError:
            # 没有运行中的事件循环，创建新的并执行
            asyncio.run(self.publish(event))

    async def _safe_call(self, handler: EventHandler, event: Event) -> None:
        """安全调用处理器（异常不传播）

        v3.18.0: 支持同步和异步两种处理器

        Args:
            handler: 事件处理器（可以是同步或异步函数）
            event: 事件
        """
        try:
            result = handler(event)
            # 检查是否为协程（异步函数的返回值）
            if asyncio.iscoroutine(result):
                await result
            # 如果是同步函数，result 为 None，无需 await
        except Exception as e:
            self._logger.warning(
                f"Event handler error: {handler.__name__} failed with {e}",
                exc_info=True,
            )

    def on(
        self,
        event_type: type[T],
    ) -> Callable[[Callable[[T], Awaitable[None]]], Callable[[T], Awaitable[None]]]:
        """装饰器：订阅事件

        Args:
            event_type: 事件类型

        Returns:
            装饰器函数

        示例:
            @bus.on(HttpRequestEndEvent)
            async def handle(event: HttpRequestEndEvent):
                print(event.status_code)
        """

        def decorator(
            handler: Callable[[T], Awaitable[None]],
        ) -> Callable[[T], Awaitable[None]]:
            self.subscribe(event_type, handler)
            return handler

        return decorator

    def clear(self) -> None:
        """清空所有订阅"""
        self._handlers.clear()
        self._global_handlers.clear()

    def get_handlers(self, event_type: type[Event]) -> list[EventHandler]:
        """获取特定事件类型的处理器列表

        Args:
            event_type: 事件类型

        Returns:
            处理器列表
        """
        return self._handlers.get(event_type, []).copy()

    def handler_count(self) -> int:
        """获取处理器总数"""
        count = sum(len(handlers) for handlers in self._handlers.values())
        return count + len(self._global_handlers)


# =============================================================================
# 全局事件总线管理
# =============================================================================

# 测试隔离：每个测试可以有独立的 EventBus（v3.17.0）
_test_event_bus: ContextVar[EventBus | None] = ContextVar("test_event_bus", default=None)

# 全局事件总线（应用级别共享）
_global_event_bus: EventBus | None = None


def get_event_bus() -> EventBus:
    """获取事件总线

    v3.17.0: 优先返回测试上下文的 EventBus（测试隔离），否则返回全局实例。

    Returns:
        事件总线实例
    """
    # 优先使用测试上下文的 EventBus（测试隔离）
    test_bus = _test_event_bus.get()
    if test_bus is not None:
        return test_bus

    # 全局单例
    global _global_event_bus
    if _global_event_bus is None:
        _global_event_bus = EventBus()
    return _global_event_bus


def set_event_bus(bus: EventBus) -> None:
    """设置全局事件总线

    Args:
        bus: 事件总线实例
    """
    global _global_event_bus
    _global_event_bus = bus


def set_test_event_bus(bus: EventBus | None) -> None:
    """设置测试上下文的 EventBus

    v3.17.0 新增：用于测试隔离，每个测试使用独立的 EventBus。

    Args:
        bus: 事件总线实例，或 None 清除测试上下文

    示例:
        @pytest.fixture(autouse=True)
        def isolated_event_bus():
            # 创建测试专用的 EventBus
            test_bus = EventBus()
            set_test_event_bus(test_bus)

            yield test_bus

            # 清理
            test_bus.clear()
            set_test_event_bus(None)
    """
    _test_event_bus.set(bus)
