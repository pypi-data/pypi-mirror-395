"""Web浏览器驱动工厂

提供统一的Web驱动创建接口，支持多种实现
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from .protocols import WebDriverProtocol

if TYPE_CHECKING:
    from .playwright.manager import BrowserManager

DriverType = Literal["playwright", "selenium"]
BrowserType = Literal["chromium", "firefox", "webkit", "chrome", "edge"]


class WebDriverFactory:
    """Web驱动工厂

    根据配置创建合适的Web驱动实现

    Examples:
        >>> # 使用默认playwright实现
        >>> driver = WebDriverFactory.create()
        >>>
        >>> # 使用selenium实现（预留）
        >>> driver = WebDriverFactory.create(driver_type="selenium")
        >>>
        >>> # 使用指定浏览器
        >>> driver = WebDriverFactory.create(browser="firefox")
    """

    @staticmethod
    def create(
        driver_type: DriverType = "playwright",
        browser: BrowserType = "chromium",
        headless: bool = True,
        **kwargs,
    ) -> WebDriverProtocol:
        """创建Web驱动

        Args:
            driver_type: 驱动类型，默认"playwright"
            browser: 浏览器类型
            headless: 是否无头模式
            **kwargs: 其他驱动配置

        Returns:
            Web驱动实例

        Raises:
            ValueError: 不支持的驱动类型
        """
        if driver_type == "playwright":
            from .playwright.browser_manager import BrowserManager

            return BrowserManager(browser_type=browser, headless=headless, **kwargs)
        elif driver_type == "selenium":
            # 预留：未来实现selenium驱动
            raise NotImplementedError(
                "selenium驱动尚未实现。请使用playwright驱动或提交PR实现selenium适配器。"
            )
        else:
            raise ValueError(f"不支持的驱动类型: {driver_type}。支持的类型: playwright, selenium")

    @staticmethod
    def create_playwright(
        browser: BrowserType = "chromium",
        headless: bool = True,
        **kwargs,
    ) -> BrowserManager:
        """创建Playwright驱动（便捷方法）

        Args:
            browser: 浏览器类型
            headless: 是否无头模式
            **kwargs: 其他配置

        Returns:
            BrowserManager实例
        """
        from .playwright.browser_manager import BrowserManager

        return BrowserManager(browser_type=browser, headless=headless, **kwargs)

    @staticmethod
    def create_selenium(
        browser: BrowserType = "chrome",
        headless: bool = True,
        **kwargs,
    ):
        """创建Selenium驱动（预留）

        Args:
            browser: 浏览器类型
            headless: 是否无头模式
            **kwargs: 其他配置

        Returns:
            SeleniumDriver实例

        Raises:
            NotImplementedError: 功能尚未实现
        """
        raise NotImplementedError(
            "selenium驱动尚未实现。请使用create_playwright()或提交PR实现selenium适配器。"
        )
