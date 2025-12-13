"""基础设施层 (Layer 1) - Config、Logging、Telemetry、Events、Plugins

v3.16.0 架构重构:
- Bootstrap、Providers、Runtime 已迁移到 bootstrap/ (Layer 4)
- 请从 df_test_framework.bootstrap 导入这些模块
"""

from .config import (
    DatabaseConfig,
    FrameworkSettings,
    HTTPConfig,
    LoggingConfig,
    RedisConfig,
    SignatureConfig,
    TestExecutionConfig,
    clear_settings,
    configure_settings,
    create_settings,
    get_settings,
)
from .logging import LoggerStrategy, LoguruStructuredStrategy, NoOpStrategy

__all__ = [
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
]
