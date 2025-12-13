"""
UI测试模块

提供基于Playwright的UI自动化测试支持

核心功能:
- BrowserManager: 浏览器管理（支持Chromium/Firefox/WebKit）
- BasePage: 页面对象基类（POM模式）
- ElementLocator: 元素定位器
- WaitHelper: 等待策略助手

支持的浏览器:
- Chromium (推荐)
- Firefox
- WebKit (Safari引擎)

使用前需要安装:
    pip install playwright
    playwright install
"""

from .browser import BrowserManager, BrowserType
from .locator import ElementLocator, LocatorType, WaitHelper
from .page import BasePage

__all__ = [
    # 页面对象基类
    "BasePage",
    # 浏览器管理
    "BrowserManager",
    "BrowserType",
    # 元素定位
    "ElementLocator",
    "LocatorType",
    # 等待助手
    "WaitHelper",
]
