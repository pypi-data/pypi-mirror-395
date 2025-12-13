"""UI交互能力层 - Layer 1

提供多种UI驱动的实现
"""

from .web.playwright.browser import BrowserManager, BrowserType
from .web.playwright.locator import ElementLocator, LocatorType
from .web.playwright.page import BasePage

__all__ = [
    "BasePage",
    "BrowserManager",
    "BrowserType",
    "ElementLocator",
    "LocatorType",
]
