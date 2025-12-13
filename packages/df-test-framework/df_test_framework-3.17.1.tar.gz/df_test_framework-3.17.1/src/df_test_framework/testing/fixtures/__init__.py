"""
df-test-framework fixture entry points.

The primary pytest plugin lives in `df_test_framework.fixtures.core`.
"""

# Allure fixture（薄包装层，依赖 reporting.allure 的核心实现）
from .allure import _auto_allure_observer  # noqa: F401
from .cleanup import (  # noqa: F401
    CleanupManager,
    ListCleanup,
    SimpleCleanupManager,
    should_keep_test_data,
)
from .core import database, http_client, redis_client, runtime  # noqa: F401
from .ui import (  # noqa: F401
    browser,
    browser_manager,
    context,
    goto,
    page,
    screenshot,
    ui_manager,
)

__all__ = [
    # API测试fixtures
    "runtime",
    "http_client",
    "database",
    "redis_client",
    # 数据清理
    "should_keep_test_data",
    "CleanupManager",
    "SimpleCleanupManager",
    "ListCleanup",
    # UI测试fixtures
    "browser_manager",
    "browser",
    "context",
    "page",
    "ui_manager",
    "goto",
    "screenshot",
]
