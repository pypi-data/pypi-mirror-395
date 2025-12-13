"""
事件协议定义
"""

from collections.abc import Awaitable, Callable
from typing import Any, Protocol, TypeVar

T = TypeVar("T")


class IEventHandler(Protocol[T]):
    """事件处理器协议"""

    async def __call__(self, event: T) -> None:
        """处理事件"""
        ...


class IEventBus(Protocol):
    """事件总线协议

    发布/订阅模式，解耦组件通信
    """

    def subscribe(
        self,
        event_type: type[T],
        handler: Callable[[T], Awaitable[None]],
    ) -> None:
        """订阅特定类型事件"""
        ...

    def subscribe_all(
        self,
        handler: Callable[[Any], Awaitable[None]],
    ) -> None:
        """订阅所有事件"""
        ...

    def unsubscribe(
        self,
        event_type: type[T],
        handler: Callable[[T], Awaitable[None]],
    ) -> None:
        """取消订阅"""
        ...

    async def publish(self, event: Any) -> None:
        """发布事件"""
        ...

    def on(
        self,
        event_type: type[T],
    ) -> Callable[[Callable[[T], Awaitable[None]]], Callable[[T], Awaitable[None]]]:
        """装饰器：订阅事件"""
        ...
