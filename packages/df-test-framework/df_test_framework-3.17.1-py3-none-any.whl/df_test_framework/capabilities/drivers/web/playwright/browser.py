"""浏览器管理器

提供浏览器实例的创建、配置和管理
基于 Playwright 实现，支持多种浏览器
"""

from enum import Enum
from typing import Any

try:
    from playwright.sync_api import (
        Browser,
        BrowserContext,
        Page,
        Playwright,
        sync_playwright,
    )

    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    Browser = Any
    BrowserContext = Any
    Page = Any
    Playwright = Any


class BrowserType(str, Enum):
    """浏览器类型枚举"""

    CHROMIUM = "chromium"
    FIREFOX = "firefox"
    WEBKIT = "webkit"


class BrowserManager:
    """
    浏览器管理器

    基于Playwright实现，提供：
    - 浏览器启动和关闭
    - 浏览器配置管理
    - 多浏览器支持（Chromium/Firefox/WebKit）
    - 无头模式支持
    - 浏览器上下文管理
    - 页面管理

    示例:
        >>> manager = BrowserManager(browser_type=BrowserType.CHROMIUM, headless=True)
        >>> browser, context, page = manager.start()
        >>> page.goto("https://example.com")
        >>> manager.stop()

        或使用上下文管理器:
        >>> with BrowserManager() as (browser, context, page):
        ...     page.goto("https://example.com")
    """

    def __init__(
        self,
        browser_type: BrowserType = BrowserType.CHROMIUM,
        headless: bool = True,
        slow_mo: int = 0,
        timeout: int = 30000,
        viewport: dict[str, int] | None = None,
        **browser_options: Any,
    ):
        """
        初始化浏览器管理器

        Args:
            browser_type: 浏览器类型（chromium/firefox/webkit）
            headless: 是否使用无头模式
            slow_mo: 每个操作的延迟毫秒数（用于调试）
            timeout: 默认超时时间（毫秒）
            viewport: 视口大小，如 {"width": 1280, "height": 720}
            browser_options: 其他浏览器选项

        Raises:
            ImportError: 如果未安装playwright
        """
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError(
                "Playwright未安装。请运行: pip install playwright && playwright install"
            )

        self.browser_type = browser_type
        self.headless = headless
        self.slow_mo = slow_mo
        self.timeout = timeout
        self.viewport = viewport or {"width": 1280, "height": 720}
        self.browser_options = browser_options

        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None

    def start(self) -> tuple[Browser, BrowserContext, Page]:
        """
        启动浏览器并创建页面

        Returns:
            tuple: (browser, context, page) 三元组

        Raises:
            RuntimeError: 如果浏览器已经启动
        """
        if self._browser is not None:
            raise RuntimeError("浏览器已经启动，请先调用 stop() 关闭")

        # 启动Playwright
        self._playwright = sync_playwright().start()

        # 获取浏览器启动器
        if self.browser_type == BrowserType.CHROMIUM:
            launcher = self._playwright.chromium
        elif self.browser_type == BrowserType.FIREFOX:
            launcher = self._playwright.firefox
        elif self.browser_type == BrowserType.WEBKIT:
            launcher = self._playwright.webkit
        else:
            raise ValueError(f"不支持的浏览器类型: {self.browser_type}")

        # 启动浏览器
        self._browser = launcher.launch(
            headless=self.headless,
            slow_mo=self.slow_mo,
            **self.browser_options,
        )

        # 创建浏览器上下文
        self._context = self._browser.new_context(
            viewport=self.viewport,
        )

        # 设置默认超时
        self._context.set_default_timeout(self.timeout)

        # 创建页面
        self._page = self._context.new_page()

        return self._browser, self._context, self._page

    def stop(self) -> None:
        """
        关闭浏览器并清理资源
        """
        if self._page:
            self._page.close()
            self._page = None

        if self._context:
            self._context.close()
            self._context = None

        if self._browser:
            self._browser.close()
            self._browser = None

        if self._playwright:
            self._playwright.stop()
            self._playwright = None

    def new_page(self) -> Page:
        """
        在当前上下文中创建新页面

        Returns:
            Page: 新创建的页面

        Raises:
            RuntimeError: 如果浏览器未启动
        """
        if not self._context:
            raise RuntimeError("浏览器未启动，请先调用 start()")

        return self._context.new_page()

    def new_context(self, **context_options: Any) -> BrowserContext:
        """
        创建新的浏览器上下文

        Args:
            context_options: 上下文选项

        Returns:
            BrowserContext: 新的浏览器上下文

        Raises:
            RuntimeError: 如果浏览器未启动
        """
        if not self._browser:
            raise RuntimeError("浏览器未启动，请先调用 start()")

        return self._browser.new_context(**context_options)

    @property
    def browser(self) -> Browser:
        """获取浏览器实例"""
        if not self._browser:
            raise RuntimeError("浏览器未启动，请先调用 start()")
        return self._browser

    @property
    def context(self) -> BrowserContext:
        """获取浏览器上下文"""
        if not self._context:
            raise RuntimeError("浏览器上下文不存在，请先调用 start()")
        return self._context

    @property
    def page(self) -> Page:
        """获取当前页面"""
        if not self._page:
            raise RuntimeError("页面不存在，请先调用 start()")
        return self._page

    def __enter__(self):
        """上下文管理器入口"""
        return self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出"""
        self.stop()
        return False


__all__ = ["BrowserManager", "BrowserType"]
