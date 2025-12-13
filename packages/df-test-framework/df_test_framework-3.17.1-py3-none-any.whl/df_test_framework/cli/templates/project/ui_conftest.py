"""UI项目pytest配置模板"""

UI_CONFTEST_TEMPLATE = """\"\"\"Pytest全局配置 - UI测试

UI测试专用的pytest配置和fixtures。
\"\"\"

import pytest
from pathlib import Path

from df_test_framework.capabilities.drivers.web import BrowserType

# ========== 启用UI测试fixtures ==========
pytest_plugins = ["df_test_framework.testing.fixtures.ui"]

# ========== 导入框架fixtures ==========
from {project_name}.fixtures import (
    # UI测试fixtures
    browser_manager,
    browser,
    context,
    page,
)


# ========== 配置fixtures ==========

@pytest.fixture(scope="session")
def settings():
    \"\"\"配置对象（session级别）

    Returns:
        {ProjectName}Settings: 项目配置对象
    \"\"\"
    from {project_name}.config import {ProjectName}Settings
    return {ProjectName}Settings()


@pytest.fixture(scope="session")
def browser_headless(pytestconfig, settings):
    \"\"\"浏览器无头模式配置，支持 --headed 覆盖\"\"\"
    if pytestconfig.getoption("--headed"):
        return False
    return settings.headless


@pytest.fixture(scope="session")
def browser_type(pytestconfig, settings):
    \"\"\"浏览器类型配置，支持 --browser 覆盖\"\"\"
    selected = pytestconfig.getoption("--browser") or settings.browser_type
    browser_map = {
        "chromium": BrowserType.CHROMIUM,
        "firefox": BrowserType.FIREFOX,
        "webkit": BrowserType.WEBKIT,
    }
    return browser_map.get(str(selected).lower(), BrowserType.CHROMIUM)


@pytest.fixture(scope="session")
def browser_timeout(settings):
    \"\"\"浏览器超时配置\"\"\"
    return settings.browser_timeout


@pytest.fixture(scope="session")
def browser_viewport(settings):
    \"\"\"浏览器视口配置\"\"\"
    return {{
        "width": settings.viewport_width,
        "height": settings.viewport_height,
    }}


@pytest.fixture(scope="session")
def base_url(settings):
    \"\"\"基础URL\"\"\"
    return settings.base_url


# ========== 测试钩子 ==========

def pytest_addoption(parser):
    \"\"\"添加命令行选项\"\"\"
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="显示浏览器窗口（非无头模式）"
    )
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        help="浏览器类型: chromium, firefox, webkit"
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    \"\"\"测试失败时自动截图\"\"\"
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        if "page" in item.funcargs:
            page = item.funcargs["page"]
            screenshots_dir = Path("reports/screenshots")
            screenshots_dir.mkdir(parents=True, exist_ok=True)
            screenshot_path = screenshots_dir / f"{{item.name}}_failure.png"

            try:
                page.screenshot(path=str(screenshot_path))
                print(f"\\n📸 失败截图: {{screenshot_path}}")
            except Exception as e:
                print(f"\\n⚠️  截图失败: {{e}}")


def pytest_configure(config):
    \"\"\"Pytest配置钩子\"\"\"
    # 注册自定义标记
    config.addinivalue_line("markers", "ui: mark test as ui test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
"""

__all__ = ["UI_CONFTEST_TEMPLATE"]
