"""调试工具模块

提供测试调试功能（不依赖 pytest）：
- HTTPDebugger - HTTP 请求/响应调试
- DBDebugger - 数据库查询调试

注意：DebugPlugin（pytest 插件）位于 testing/plugins/debug.py

使用方式：
    # 启用 HTTP 调试
    from df_test_framework.testing.debugging import enable_http_debug

    debugger = enable_http_debug()
    # ... 执行测试 ...
    debugger.print_summary()

    # 启用数据库调试
    from df_test_framework.testing.debugging import enable_db_debug

    db_debugger = enable_db_debug(slow_query_threshold_ms=100)
    # ... 执行数据库操作 ...
    db_debugger.print_summary()
"""

from .database import (
    DBDebugger,
    disable_db_debug,
    enable_db_debug,
    get_global_db_debugger,
)
from .http import (
    HTTPDebugger,
    disable_http_debug,
    enable_http_debug,
    get_global_debugger,
)

__all__ = [
    # HTTP Debugger
    "HTTPDebugger",
    "enable_http_debug",
    "disable_http_debug",
    "get_global_debugger",
    # DB Debugger
    "DBDebugger",
    "enable_db_debug",
    "disable_db_debug",
    "get_global_db_debugger",
]
