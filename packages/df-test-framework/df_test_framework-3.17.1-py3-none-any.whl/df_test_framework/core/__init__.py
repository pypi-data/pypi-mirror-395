"""
DF Test Framework - Core Layer (Layer 0)

纯抽象层，无第三方依赖。

包含:
- protocols/: 协议定义（依赖反转基础）
- middleware/: 统一中间件系统
- context/: 上下文传播系统
- events/: 事件类型定义
- exceptions: 异常体系
- types: 类型定义
"""

from df_test_framework.core.exceptions import (
    ConfigurationError,
    DatabaseError,
    ExtensionError,
    FrameworkError,
    HttpError,
    MessengerError,
    MiddlewareAbort,
    MiddlewareError,
    PluginError,
    ProviderError,
    RedisError,
    ResourceError,
    StorageError,
    TelemetryError,
    TestError,
    ValidationError,
)
from df_test_framework.core.types import (
    DatabaseDialect,
    DatabaseOperation,
    Environment,
    Headers,
    HttpMethod,
    HttpStatus,
    HttpStatusGroup,
    JsonDict,
    LogLevel,
    MessageQueueType,
    QueryParams,
    StorageType,
    TestPriority,
    TestType,
    TRequest,
    TResponse,
)

__all__ = [
    # 异常
    "FrameworkError",
    "ConfigurationError",
    "HttpError",
    "DatabaseError",
    "MessengerError",
    "StorageError",
    "MiddlewareError",
    "MiddlewareAbort",
    "PluginError",
    "TelemetryError",
    "ResourceError",
    "RedisError",
    "ValidationError",
    "ExtensionError",
    "ProviderError",
    "TestError",
    # 类型
    "Environment",
    "LogLevel",
    "HttpMethod",
    "HttpStatus",
    "HttpStatusGroup",
    "DatabaseDialect",
    "DatabaseOperation",
    "MessageQueueType",
    "StorageType",
    "TestPriority",
    "TestType",
    "TRequest",
    "TResponse",
    "JsonDict",
    "Headers",
    "QueryParams",
]
