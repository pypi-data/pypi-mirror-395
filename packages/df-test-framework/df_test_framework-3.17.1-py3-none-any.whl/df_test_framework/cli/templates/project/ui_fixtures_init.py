"""UI Fixtures模块导出模板"""

UI_FIXTURES_INIT_TEMPLATE = """\"\"\"Fixtures模块

导出框架提供的fixtures供测试使用。
\"\"\"

# UI测试fixtures
from df_test_framework.testing.fixtures import (
    browser_manager,
    browser,
    context,
    page,
    ui_manager,
    goto,
    screenshot,
)


__all__ = [
    # UI测试fixtures
    "browser_manager",
    "browser",
    "context",
    "page",
    "ui_manager",
    "goto",
    "screenshot",
]
"""

__all__ = ["UI_FIXTURES_INIT_TEMPLATE"]
