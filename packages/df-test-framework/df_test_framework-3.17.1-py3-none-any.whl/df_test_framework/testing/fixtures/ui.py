"""UI测试fixtures

提供UI自动化测试的pytest fixtures
"""

from collections.abc import Generator

import pytest

try:
    from playwright.sync_api import Browser, BrowserContext, Page

    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    Browser = None
    BrowserContext = None
    Page = None

from df_test_framework.capabilities.drivers.web import BrowserManager, BrowserType


@pytest.fixture(scope="session")
def browser_type() -> BrowserType:
    """
    浏览器类型配置

    默认使用Chromium，可以在conftest.py中重写此fixture来更改浏览器类型

    示例:
        >>> # 在conftest.py中
        >>> @pytest.fixture(scope="session")
        >>> def browser_type():
        ...     return BrowserType.FIREFOX
    """
    return BrowserType.CHROMIUM


@pytest.fixture(scope="session")
def browser_headless() -> bool:
    """
    浏览器无头模式配置

    默认为True（无头模式），可以在conftest.py中重写此fixture

    示例:
        >>> # 在conftest.py中显示浏览器
        >>> @pytest.fixture(scope="session")
        >>> def browser_headless():
        ...     return False
    """
    return True


@pytest.fixture(scope="session")
def browser_timeout() -> int:
    """
    浏览器超时配置（毫秒）

    默认30秒，可以在conftest.py中重写此fixture
    """
    return 30000


@pytest.fixture(scope="session")
def browser_viewport() -> dict:
    """
    浏览器视口大小配置

    默认1280x720，可以在conftest.py中重写此fixture

    示例:
        >>> # 在conftest.py中设置1920x1080
        >>> @pytest.fixture(scope="session")
        >>> def browser_viewport():
        ...     return {"width": 1920, "height": 1080}
    """
    return {"width": 1280, "height": 720}


@pytest.fixture(scope="session")
def browser_manager(
    browser_type: BrowserType,
    browser_headless: bool,
    browser_timeout: int,
    browser_viewport: dict,
) -> Generator[BrowserManager, None, None]:
    """
    浏览器管理器（会话级）

    在整个测试会话中共享同一个浏览器实例

    Yields:
        BrowserManager: 浏览器管理器实例
    """
    if not PLAYWRIGHT_AVAILABLE:
        pytest.skip("Playwright未安装，跳过UI测试")

    manager = BrowserManager(
        browser_type=browser_type,
        headless=browser_headless,
        timeout=browser_timeout,
        viewport=browser_viewport,
    )

    manager.start()

    yield manager

    manager.stop()


@pytest.fixture(scope="function")
def browser(browser_manager: BrowserManager) -> Browser:
    """
    浏览器实例（函数级）

    每个测试函数获取共享的浏览器实例

    Args:
        browser_manager: 浏览器管理器

    Returns:
        Browser: Playwright浏览器实例
    """
    return browser_manager.browser


@pytest.fixture(scope="function")
def context(browser: Browser, browser_viewport: dict) -> Generator[BrowserContext, None, None]:
    """
    浏览器上下文（函数级）

    每个测试函数创建独立的浏览器上下文，测试间相互隔离

    Args:
        browser: 浏览器实例
        browser_viewport: 视口大小

    Yields:
        BrowserContext: Playwright浏览器上下文
    """
    ctx = browser.new_context(viewport=browser_viewport)
    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """
    页面实例（函数级）

    每个测试函数获取独立的页面实例

    Args:
        context: 浏览器上下文

    Yields:
        Page: Playwright页面实例

    示例:
        >>> def test_example(page):
        ...     page.goto("https://example.com")
        ...     assert page.title() == "Example Domain"
    """
    p = context.new_page()
    yield p
    p.close()


@pytest.fixture(scope="function")
def ui_manager(browser_manager: BrowserManager):
    """
    UI管理器（函数级）

    提供完整的浏览器管理器，包含browser、context、page

    Args:
        browser_manager: 浏览器管理器

    Returns:
        BrowserManager: 浏览器管理器实例

    示例:
        >>> def test_with_manager(ui_manager):
        ...     page = ui_manager.page
        ...     page.goto("https://example.com")
        ...     assert page.title() == "Example Domain"
    """
    return browser_manager


# ========== 便捷 fixtures ==========


@pytest.fixture
def goto(page: Page):
    """
    页面导航助手

    提供简化的页面导航方法

    Args:
        page: 页面实例

    Returns:
        callable: 导航函数

    示例:
        >>> def test_navigation(goto):
        ...     goto("/login")  # 导航到登录页
    """

    def _goto(url: str, **kwargs):
        """导航到指定URL"""
        page.goto(url, **kwargs)
        return page

    return _goto


@pytest.fixture
def screenshot(page: Page):
    """
    截图助手

    提供便捷的截图功能

    Args:
        page: 页面实例

    Returns:
        callable: 截图函数

    示例:
        >>> def test_with_screenshot(page, screenshot):
        ...     page.goto("https://example.com")
        ...     screenshot("example.png")
    """

    def _screenshot(path: str = None, **kwargs):
        """
        页面截图

        Args:
            path: 保存路径
            kwargs: 其他参数
        """
        return page.screenshot(path=path, **kwargs)

    return _screenshot


__all__ = [
    # 配置fixtures
    "browser_type",
    "browser_headless",
    "browser_timeout",
    "browser_viewport",
    # 核心fixtures
    "browser_manager",
    "browser",
    "context",
    "page",
    "ui_manager",
    # 便捷fixtures
    "goto",
    "screenshot",
]
