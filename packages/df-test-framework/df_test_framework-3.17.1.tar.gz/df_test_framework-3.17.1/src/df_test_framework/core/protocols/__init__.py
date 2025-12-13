"""
协议定义 - 依赖反转基础

所有协议使用 typing.Protocol 定义，不依赖任何第三方库。
"""

from df_test_framework.core.protocols.client import (
    IDatabaseClient,
    IHttpClient,
    IRedisClient,
)
from df_test_framework.core.protocols.event import (
    IEventBus,
    IEventHandler,
)
from df_test_framework.core.protocols.plugin import (
    IPluginManager,
)
from df_test_framework.core.protocols.repository import (
    IRepository,
    IUnitOfWork,
)
from df_test_framework.core.protocols.telemetry import (
    IMeter,
    ISpan,
    ITelemetry,
    ITracer,
)

__all__ = [
    # 客户端协议
    "IHttpClient",
    "IDatabaseClient",
    "IRedisClient",
    # Repository 协议
    "IRepository",
    "IUnitOfWork",
    # 可观测性协议
    "ITelemetry",
    "ITracer",
    "IMeter",
    "ISpan",
    # 事件协议
    "IEventBus",
    "IEventHandler",
    # 插件协议
    "IPluginManager",
]
