"""
DF 测试自动化框架 v3.17.1

企业级测试平台架构升级，基于五层架构 + 事件驱动 + 可观测性。

v3.17.1 核心特性:
- 🔧 能力层 Allure 集成优化 - 纯 EventBus 驱动模式
- 🐛 EventBus 同步/异步处理器兼容性修复
- 💾 UoW 事务事件集成 - commit/rollback 自动记录到 Allure
- 📊 回滚原因追踪 - auto/exception/manual 分类
- 🔌 AllurePlugin 标记为 DEPRECATED - 推荐使用 allure fixture

架构层级:
- Layer 0 (core/): 纯抽象，无第三方依赖
- Layer 1 (infrastructure/): 基础设施，配置/插件/遥测/事件
- Layer 2 (capabilities/): 能力层，HTTP/DB/MQ/Storage
- Layer 3 (testing/ + cli/): 门面层
- Layer 4 (bootstrap/): 引导层，框架组装和初始化
- 横切 (plugins/): 插件实现

历史版本特性:
- 🔄 事件系统重构 - EventBus 与 Allure 深度整合（v3.17）
- 🔗 OpenTelemetry 整合 - trace_id/span_id 自动注入（v3.17）
- 🧪 测试隔离 - 每个测试独立的 EventBus（v3.17）
- 🏗️ 五层架构 - Layer 4 Bootstrap 引导层（v3.16）
- 🧅 统一中间件系统（v3.14）
- 📡 可观测性融合（v3.14）
- 🔗 上下文传播（v3.14）
- 📢 事件驱动（v3.14）
- 🏗️ Testing 模块架构重构（v3.12）
- 🌐 协议扩展 - GraphQL/gRPC 客户端（v3.11）
- 🎭 Mock 增强 - DatabaseMocker/RedisMocker（v3.11）
- 📊 可观测性增强 - OpenTelemetry/Prometheus（v3.10）
- 💾 存储客户端 - LocalFile/S3/OSS（v3.10）
- 🚀 异步HTTP客户端 - 性能提升40倍（v3.8）
- 🔄 Unit of Work 模式支持（v3.7）
"""

__version__ = "3.17.1"
__author__ = "DF QA Team"

# ============= 异常体系 =============
# HTTP核心对象
# GraphQL客户端
# ============= 引导层 (Layer 4) =============
from .bootstrap import (
    # Bootstrap
    Bootstrap,
    BootstrapApp,
    # Providers
    Provider,
    ProviderRegistry,
    # Runtime
    RuntimeBuilder,
    RuntimeContext,
    SingletonProvider,
    default_providers,
)
from .capabilities.clients.graphql import (
    GraphQLClient,
    GraphQLError,
    GraphQLRequest,
    GraphQLResponse,
    QueryBuilder,
)

# gRPC客户端
from .capabilities.clients.grpc import (
    GrpcClient,
    GrpcError,
    GrpcResponse,
)
from .capabilities.clients.http.core import Request, Response

# v3.16.0: HTTP拦截器已完全移除，请使用中间件系统
# Capabilities 层 - HTTP 中间件
from .capabilities.clients.http.middleware import (
    BearerTokenMiddleware,
    HttpTelemetryMiddleware,
    LoggingMiddleware,
    RetryMiddleware,
    SignatureMiddleware,
)

# ============= 核心功能层 =============
# HTTP客户端
from .capabilities.clients.http.rest.httpx import (
    AsyncHttpClient,
    BaseAPI,
    BusinessError,
    HttpClient,
)

# 数据库
from .capabilities.databases.database import Database
from .capabilities.databases.redis.redis_client import RedisClient

# Repository模式
from .capabilities.databases.repositories.base import BaseRepository
from .capabilities.databases.repositories.query_spec import QuerySpec

# Unit of Work 模式
from .capabilities.databases.uow import UnitOfWork

# ============= UI模块 =============
from .capabilities.drivers.web import (
    BasePage,
    BrowserManager,
    BrowserType,
    ElementLocator,
    LocatorType,
    WaitHelper,
)

# ============= 异常体系 (v3.14.0 统一到 core) =============
from .core import (
    ConfigurationError,
    DatabaseError,
    ExtensionError,
    FrameworkError,
    HttpError,
    MiddlewareAbort,
    MiddlewareError,
    ProviderError,
    RedisError,
    ResourceError,
    TestError,
    ValidationError,
)
from .core.context import (
    ExecutionContext,
    get_current_context,
    get_or_create_context,
    with_context,
    with_context_async,
)
from .core.events import (
    DatabaseQueryEndEvent,
    DatabaseQueryStartEvent,
    Event,
    HttpRequestEndEvent,
    HttpRequestErrorEvent,
    HttpRequestStartEvent,
    TestEndEvent,
    TestStartEvent,
)
from .core.middleware import (
    BaseMiddleware,
    Middleware,
    MiddlewareChain,
    SyncMiddleware,
    middleware,
)

# 类型和枚举
from .core.types import (
    DatabaseOperation,
    Environment,
    HttpMethod,
    HttpStatus,
    HttpStatusGroup,
    LogLevel,
    TestPriority,
    TestType,
)

# ============= 扩展系统 (向后兼容，已废弃) =============
# 注意：extensions 模块已废弃，推荐使用 infrastructure.plugins
# ============= 基础设施层 (Layer 1) =============
from .infrastructure import (
    # Config
    DatabaseConfig,
    FrameworkSettings,
    HTTPConfig,
    # Logging
    LoggerStrategy,
    LoggingConfig,
    LoguruStructuredStrategy,
    NoOpStrategy,
    RedisConfig,
    SignatureConfig,
    TestExecutionConfig,
    clear_settings,
    configure_settings,
    create_settings,
    get_settings,
)
from .infrastructure.context import (
    GrpcContextCarrier,
    HttpContextCarrier,
    MqContextCarrier,
)
from .infrastructure.events import (
    EventBus,
    get_event_bus,
    set_event_bus,
)

# Infrastructure 层 - 插件系统 (v3.14.0 推荐)
from .infrastructure.plugins import (
    HookSpecs,
    PluggyPluginManager,
    hookimpl,  # v3.14.0 统一使用 infrastructure.plugins.hookimpl
)
from .infrastructure.telemetry import (
    NoopTelemetry,
    SpanContext,
    Telemetry,
)

# ============= 数据模型 =============
# Pydantic 基础模型
from .models import (
    BaseRequest,
    BaseResponse,
    PageResponse,
)

# Plugins - 横切关注点
from .plugins.builtin.monitoring import MonitoringPlugin
from .plugins.builtin.reporting import AllurePlugin

# ============= 设计模式层 =============
# Builder模式
from .testing.data.builders.base import BaseBuilder, DictBuilder
from .testing.debugging import (
    DBDebugger,
    HTTPDebugger,
    disable_db_debug,
    disable_http_debug,
    enable_db_debug,
    enable_http_debug,
)

# ============= 测试支持层 =============
# API 自动发现装饰器
from .testing.decorators import api_class, load_api_fixtures
from .testing.fixtures import (
    CleanupManager,
    ListCleanup,
    SimpleCleanupManager,
    database,
    http_client,
    redis_client,
    runtime,
    should_keep_test_data,
)
from .testing.plugins import (
    EnvironmentMarker,
    dev_only,
    get_env,
    is_env,
    prod_only,
    skip_if_dev,
    skip_if_prod,
)
from .testing.reporting.allure import (
    AllureHelper,
    attach_json,
    attach_log,
    attach_screenshot,
    step,
)
from .utils.assertion import assert_that
from .utils.data_generator import DataGenerator

# ============= 工具函数 =============
from .utils.decorator import (
    cache_result,
    deprecated,
    log_execution,
    retry_on_failure,
)
from .utils.performance import (
    PerformanceCollector,
    PerformanceTimer,
    track_performance,
)

# ============= 类型工具 (v3.6新增) =============
from .utils.types import Decimal, DecimalAsCurrency, DecimalAsFloat

# ============= 全部导出 =============
__all__ = [
    # 版本信息
    "__version__",
    "__author__",
    # ===== 异常体系 =====
    "FrameworkError",
    "ConfigurationError",
    "ResourceError",
    "DatabaseError",
    "RedisError",
    "HttpError",
    "ValidationError",
    "ExtensionError",
    "ProviderError",
    "TestError",
    # ===== 基础设施层 =====
    # Bootstrap
    "Bootstrap",
    "BootstrapApp",
    # Runtime
    "RuntimeContext",
    "RuntimeBuilder",
    # Config
    "FrameworkSettings",
    "HTTPConfig",
    "DatabaseConfig",
    "RedisConfig",
    "LoggingConfig",
    "TestExecutionConfig",
    "SignatureConfig",
    "configure_settings",
    "get_settings",
    "clear_settings",
    "create_settings",
    # Logging
    "LoggerStrategy",
    "LoguruStructuredStrategy",
    "NoOpStrategy",
    # Providers
    "ProviderRegistry",
    "Provider",
    "SingletonProvider",
    "default_providers",
    # ===== 核心功能层 =====
    # HTTP客户端
    "HttpClient",
    "AsyncHttpClient",
    "BaseAPI",
    "BusinessError",
    # HTTP核心对象
    "Request",
    "Response",
    # v3.16.0: HTTP拦截器已移除
    # GraphQL客户端 (v3.11)
    "GraphQLClient",
    "GraphQLRequest",
    "GraphQLResponse",
    "GraphQLError",
    "QueryBuilder",
    # gRPC客户端 (v3.11)
    "GrpcClient",
    "GrpcResponse",
    "GrpcError",
    # 数据库
    "Database",
    "RedisClient",
    # ===== 设计模式层 =====
    "BaseBuilder",
    "DictBuilder",
    "BaseRepository",
    "QuerySpec",
    # Unit of Work
    "UnitOfWork",
    # ===== 测试支持层 =====
    # Fixtures
    "runtime",
    "http_client",
    "database",
    "redis_client",
    # 数据清理 (v3.11.1)
    "should_keep_test_data",
    "CleanupManager",
    "SimpleCleanupManager",
    "ListCleanup",
    # Plugins
    "AllureHelper",
    "EnvironmentMarker",
    "attach_json",
    "attach_log",
    "attach_screenshot",
    "step",
    "get_env",
    "is_env",
    "skip_if_prod",
    "skip_if_dev",
    "dev_only",
    "prod_only",
    # Debug工具
    "HTTPDebugger",
    "DBDebugger",
    "enable_http_debug",
    "disable_http_debug",
    "enable_db_debug",
    "disable_db_debug",
    # ===== 数据模型 =====
    "BaseRequest",
    "BaseResponse",
    "PageResponse",
    "HttpMethod",
    "Environment",
    "LogLevel",
    "HttpStatus",
    "HttpStatusGroup",
    "DatabaseOperation",
    "TestPriority",
    "TestType",
    # ===== 工具函数 =====
    "cache_result",
    "deprecated",
    "log_execution",
    "retry_on_failure",
    "track_performance",
    "PerformanceTimer",
    "PerformanceCollector",
    "DataGenerator",
    "assert_that",
    # ===== 类型工具 (v3.6) =====
    "Decimal",
    "DecimalAsFloat",
    "DecimalAsCurrency",
    # ===== UI模块 =====
    "BasePage",
    "BrowserManager",
    "BrowserType",
    "ElementLocator",
    "LocatorType",
    "WaitHelper",
    # ===== v3.14.0 新增 =====
    # Core 层 - 中间件
    "Middleware",
    "BaseMiddleware",
    "SyncMiddleware",
    "MiddlewareChain",
    "middleware",
    "MiddlewareAbort",
    "MiddlewareError",
    # Core 层 - 上下文
    "ExecutionContext",
    "get_current_context",
    "get_or_create_context",
    "with_context",
    "with_context_async",
    # Core 层 - 事件
    "Event",
    "HttpRequestStartEvent",
    "HttpRequestEndEvent",
    "HttpRequestErrorEvent",
    "DatabaseQueryStartEvent",
    "DatabaseQueryEndEvent",
    "TestStartEvent",
    "TestEndEvent",
    # Infrastructure - 插件系统
    "HookSpecs",
    "PluggyPluginManager",
    "hookimpl",
    # Infrastructure - 遥测
    "Telemetry",
    "NoopTelemetry",
    "SpanContext",
    # Infrastructure - 事件总线
    "EventBus",
    "get_event_bus",
    "set_event_bus",
    # Infrastructure - 上下文载体
    "HttpContextCarrier",
    "GrpcContextCarrier",
    "MqContextCarrier",
    # Capabilities - HTTP 中间件
    "SignatureMiddleware",
    "BearerTokenMiddleware",
    "RetryMiddleware",
    "LoggingMiddleware",
    "HttpTelemetryMiddleware",
    # Plugins
    "MonitoringPlugin",
    "AllurePlugin",
    # Testing - API 自动发现
    "api_class",
    "load_api_fixtures",
]
