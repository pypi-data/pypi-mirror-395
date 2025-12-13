"""
Configuration subsystem for df-test-framework.

Projects should subclass `FrameworkSettings` to extend business-specific fields,
then register the subclass via `configure_settings`.
"""

# v3.16.0: HTTPSettings 和 InterceptorSettings 已移除
# 请使用 middleware_schema 中的配置和 FrameworkSettings
from .manager import (
    SettingsAlreadyConfiguredError,
    SettingsNamespace,
    SettingsNotConfiguredError,
    clear_settings,
    configure_settings,
    create_settings,
    get_settings,
)

# v3.16.0: 新的中间件配置系统
from .middleware_schema import (
    BearerTokenMiddlewareConfig,
    LoggingMiddlewareConfig,
    MiddlewareConfig,
    MiddlewareType,
    RetryMiddlewareConfig,
    RetryStrategy,
    SignatureAlgorithm,
    SignatureMiddlewareConfig,
    TokenSource,
)
from .pipeline import ConfigPipeline
from .schema import (
    BearerTokenInterceptorConfig,
    CustomInterceptorConfig,
    DatabaseConfig,
    FrameworkSettings,
    HTTPConfig,
    # Interceptor配置
    InterceptorConfig,
    LoggingConfig,
    RedisConfig,
    SignatureConfig,
    SignatureInterceptorConfig,
    StorageConfig,
    TestExecutionConfig,
    TokenInterceptorConfig,
)
from .sources import (
    ConfigSource,
    DictSource,
    DotenvSource,
    EnvVarSource,
)

__all__ = [
    # schema
    "FrameworkSettings",
    "HTTPConfig",
    "DatabaseConfig",
    "RedisConfig",
    "StorageConfig",
    "TestExecutionConfig",
    "LoggingConfig",
    "SignatureConfig",
    # Interceptor配置（已废弃，保留向后兼容）
    "InterceptorConfig",
    "SignatureInterceptorConfig",
    "BearerTokenInterceptorConfig",
    "TokenInterceptorConfig",
    "CustomInterceptorConfig",
    # v3.16.0: Middleware配置（推荐）
    "MiddlewareConfig",
    "MiddlewareType",
    "SignatureMiddlewareConfig",
    "SignatureAlgorithm",
    "BearerTokenMiddlewareConfig",
    "TokenSource",
    "RetryMiddlewareConfig",
    "RetryStrategy",
    "LoggingMiddlewareConfig",
    # v3.16.0: HTTPSettings/InterceptorSettings 已移除
    # manager
    "configure_settings",
    "get_settings",
    "create_settings",
    "clear_settings",
    "SettingsNamespace",
    "SettingsAlreadyConfiguredError",
    "SettingsNotConfiguredError",
    # sources
    "ConfigSource",
    "DictSource",
    "EnvVarSource",
    "DotenvSource",
    # pipeline
    "ConfigPipeline",
]

# 修复 Pydantic 前向引用问题
# 在所有模块加载完成后调用 model_rebuild()
# 参考: https://docs.pydantic.dev/latest/concepts/postponed_annotations/
FrameworkSettings.model_rebuild()
