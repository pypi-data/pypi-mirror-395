"""
事件总线实现

发布/订阅模式，解耦组件通信。

v3.17.0:
- 添加 publish_sync() 同步发布方法
- 添加 set_test_event_bus() 测试隔离支持
"""

from df_test_framework.infrastructure.events.bus import (
    EventBus,
    get_event_bus,
    set_event_bus,
    set_test_event_bus,
)

__all__ = [
    "EventBus",
    "get_event_bus",
    "set_event_bus",
    "set_test_event_bus",
]
