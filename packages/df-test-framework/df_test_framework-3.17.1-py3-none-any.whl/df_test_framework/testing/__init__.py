"""测试支持层 - Fixtures、Plugins、Debug工具、Reporting"""

from .debugging import (
    DBDebugger,
    HTTPDebugger,
    disable_db_debug,
    disable_http_debug,
    enable_db_debug,
    enable_http_debug,
)
from .fixtures import database, http_client, redis_client, runtime
from .plugins import EnvironmentMarker
from .reporting.allure import AllureHelper, attach_json, attach_log, step

__all__ = [
    # Fixtures
    "runtime",
    "http_client",
    "database",
    "redis_client",
    # Reporting
    "AllureHelper",
    "attach_json",
    "attach_log",
    "step",
    # Plugins
    "EnvironmentMarker",
    # Debug工具
    "HTTPDebugger",
    "DBDebugger",
    "enable_http_debug",
    "disable_http_debug",
    "enable_db_debug",
    "disable_db_debug",
]
