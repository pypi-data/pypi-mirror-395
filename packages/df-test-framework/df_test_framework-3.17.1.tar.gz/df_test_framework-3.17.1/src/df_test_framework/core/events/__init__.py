"""
事件类型定义

定义框架中使用的各种事件类型。

注意: 事件总线的具体实现在 infrastructure/events/ 中。
"""

from df_test_framework.core.events.types import (
    # Cache 事件
    CacheOperationEndEvent,
    CacheOperationErrorEvent,
    CacheOperationStartEvent,
    DatabaseQueryEndEvent,
    DatabaseQueryErrorEvent,
    # Database 事件
    DatabaseQueryStartEvent,
    Event,
    HttpRequestEndEvent,
    HttpRequestErrorEvent,
    # HTTP 事件
    HttpRequestStartEvent,
    MessageConsumeEvent,
    # MQ 事件
    MessagePublishEvent,
    # 中间件事件
    MiddlewareExecuteEvent,
    # Storage 事件
    StorageOperationEndEvent,
    StorageOperationErrorEvent,
    StorageOperationStartEvent,
    TestEndEvent,
    # 测试事件
    TestStartEvent,
    # 事务事件
    TransactionCommitEvent,
    TransactionRollbackEvent,
)

__all__ = [
    "Event",
    # HTTP
    "HttpRequestStartEvent",
    "HttpRequestEndEvent",
    "HttpRequestErrorEvent",
    # 中间件
    "MiddlewareExecuteEvent",
    # Database
    "DatabaseQueryStartEvent",
    "DatabaseQueryEndEvent",
    "DatabaseQueryErrorEvent",
    # Cache
    "CacheOperationStartEvent",
    "CacheOperationEndEvent",
    "CacheOperationErrorEvent",
    # MQ
    "MessagePublishEvent",
    "MessageConsumeEvent",
    # Storage
    "StorageOperationStartEvent",
    "StorageOperationEndEvent",
    "StorageOperationErrorEvent",
    # 测试
    "TestStartEvent",
    "TestEndEvent",
    # 事务
    "TransactionCommitEvent",
    "TransactionRollbackEvent",
]
