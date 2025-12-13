"""Web浏览器驱动

支持多种Web驱动实现（Playwright、Selenium等）
通过Factory模式提供统一接口
"""

# 协议定义
# 工厂类
from .factory import WebDriverFactory
from .playwright.browser import BrowserManager, BrowserType
from .playwright.locator import ElementLocator, LocatorType, WaitHelper

# 默认实现（Playwright）
from .playwright.page import BasePage
from .protocols import PageProtocol, WebDriverProtocol

__all__ = [
    # 协议
    "WebDriverProtocol",
    "PageProtocol",
    # 工厂
    "WebDriverFactory",
    # 默认实现
    "BasePage",
    "BrowserManager",
    "BrowserType",
    "ElementLocator",
    "LocatorType",
    "WaitHelper",
]
