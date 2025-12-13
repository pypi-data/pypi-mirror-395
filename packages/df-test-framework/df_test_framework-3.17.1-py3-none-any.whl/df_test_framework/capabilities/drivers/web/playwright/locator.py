"""元素定位器和等待策略

提供便捷的元素定位和等待工具
基于 Playwright 实现
"""

from enum import Enum
from typing import Any

try:
    from playwright.sync_api import Locator, Page, expect

    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    Page = Any
    Locator = Any


class LocatorType(str, Enum):
    """定位器类型枚举"""

    CSS = "css"
    XPATH = "xpath"
    ID = "id"
    TEXT = "text"
    ROLE = "role"
    LABEL = "label"
    PLACEHOLDER = "placeholder"
    TEST_ID = "testid"


class ElementLocator:
    """
    元素定位器

    提供便捷的元素定位方法，支持：
    - 多种定位策略（CSS、XPath、文本等）
    - 链式调用
    - 预定义常用定位器

    示例:
        >>> # 使用CSS定位器
        >>> locator = ElementLocator.css("#username")
        >>>
        >>> # 使用文本定位器
        >>> locator = ElementLocator.text("登录")
        >>>
        >>> # 使用test-id定位器
        >>> locator = ElementLocator.test_id("submit-button")
    """

    def __init__(self, selector: str, locator_type: LocatorType = LocatorType.CSS):
        """
        初始化元素定位器

        Args:
            selector: 选择器表达式
            locator_type: 定位器类型
        """
        self.selector = selector
        self.locator_type = locator_type

    def get_locator(self, page: Page) -> Locator:
        """
        获取Playwright Locator对象

        Args:
            page: Playwright Page对象

        Returns:
            Locator: Playwright Locator对象
        """
        if self.locator_type == LocatorType.CSS:
            return page.locator(self.selector)
        elif self.locator_type == LocatorType.XPATH:
            return page.locator(f"xpath={self.selector}")
        elif self.locator_type == LocatorType.ID:
            return page.locator(f"#{self.selector}")
        elif self.locator_type == LocatorType.TEXT:
            return page.get_by_text(self.selector)
        elif self.locator_type == LocatorType.ROLE:
            return page.get_by_role(self.selector)
        elif self.locator_type == LocatorType.LABEL:
            return page.get_by_label(self.selector)
        elif self.locator_type == LocatorType.PLACEHOLDER:
            return page.get_by_placeholder(self.selector)
        elif self.locator_type == LocatorType.TEST_ID:
            return page.get_by_test_id(self.selector)
        else:
            return page.locator(self.selector)

    # ========== 便捷构造方法 ==========

    @classmethod
    def css(cls, selector: str) -> "ElementLocator":
        """通过CSS选择器定位"""
        return cls(selector, LocatorType.CSS)

    @classmethod
    def xpath(cls, expression: str) -> "ElementLocator":
        """通过XPath表达式定位"""
        return cls(expression, LocatorType.XPATH)

    @classmethod
    def id(cls, element_id: str) -> "ElementLocator":
        """通过ID定位"""
        return cls(element_id, LocatorType.ID)

    @classmethod
    def text(cls, text: str) -> "ElementLocator":
        """通过文本内容定位"""
        return cls(text, LocatorType.TEXT)

    @classmethod
    def role(cls, role: str) -> "ElementLocator":
        """通过ARIA role定位"""
        return cls(role, LocatorType.ROLE)

    @classmethod
    def label(cls, label: str) -> "ElementLocator":
        """通过label定位"""
        return cls(label, LocatorType.LABEL)

    @classmethod
    def placeholder(cls, placeholder: str) -> "ElementLocator":
        """通过placeholder定位"""
        return cls(placeholder, LocatorType.PLACEHOLDER)

    @classmethod
    def test_id(cls, test_id: str) -> "ElementLocator":
        """通过data-testid定位"""
        return cls(test_id, LocatorType.TEST_ID)

    def __str__(self) -> str:
        return f"{self.locator_type.value}: {self.selector}"

    def __repr__(self) -> str:
        return f"ElementLocator({self.locator_type.value}={self.selector!r})"


class WaitHelper:
    """
    等待助手

    提供常用的等待策略和工具方法

    示例:
        >>> from df_test_framework.ui import WaitHelper
        >>> wait = WaitHelper(page)
        >>> wait.for_visible("#submit-button")
        >>> wait.for_url_contains("/dashboard")
    """

    def __init__(self, page: Page, default_timeout: int = 30000):
        """
        初始化等待助手

        Args:
            page: Playwright Page对象
            default_timeout: 默认超时时间（毫秒）
        """
        self.page = page
        self.default_timeout = default_timeout

    def for_selector(
        self, selector: str, state: str = "visible", timeout: int | None = None
    ) -> None:
        """
        等待选择器

        Args:
            selector: CSS选择器
            state: 状态 (visible/hidden/attached/detached)
            timeout: 超时时间（毫秒）
        """
        self.page.wait_for_selector(selector, state=state, timeout=timeout or self.default_timeout)

    def for_visible(self, selector: str, timeout: int | None = None) -> None:
        """等待元素可见"""
        self.for_selector(selector, state="visible", timeout=timeout)

    def for_hidden(self, selector: str, timeout: int | None = None) -> None:
        """等待元素隐藏"""
        self.for_selector(selector, state="hidden", timeout=timeout)

    def for_url(self, url: str | Any, timeout: int | None = None) -> None:
        """
        等待URL匹配

        Args:
            url: URL字符串或正则表达式
            timeout: 超时时间（毫秒）
        """
        self.page.wait_for_url(url, timeout=timeout or self.default_timeout)

    def for_url_contains(self, substring: str, timeout: int | None = None) -> None:
        """等待URL包含指定字符串"""
        self.for_url(f"**/*{substring}*", timeout=timeout)

    def for_title(self, title: str, timeout: int | None = None) -> None:
        """
        等待页面标题

        Args:
            title: 期望的标题
            timeout: 超时时间（毫秒）
        """
        timeout_ms = timeout or self.default_timeout
        expect(self.page).to_have_title(title, timeout=timeout_ms)

    def for_title_contains(self, substring: str, timeout: int | None = None) -> None:
        """等待页面标题包含指定字符串"""
        timeout_ms = timeout or self.default_timeout
        # 使用正则表达式匹配
        import re

        pattern = re.compile(f".*{re.escape(substring)}.*")
        expect(self.page).to_have_title(pattern, timeout=timeout_ms)

    def for_load_state(self, state: str = "load", timeout: int | None = None) -> None:
        """
        等待页面加载状态

        Args:
            state: 状态 (load/domcontentloaded/networkidle)
            timeout: 超时时间（毫秒）
        """
        self.page.wait_for_load_state(state, timeout=timeout or self.default_timeout)

    def for_network_idle(self, timeout: int | None = None) -> None:
        """等待网络空闲"""
        self.for_load_state("networkidle", timeout=timeout)

    def for_dom_loaded(self, timeout: int | None = None) -> None:
        """等待DOM加载完成"""
        self.for_load_state("domcontentloaded", timeout=timeout)

    def for_condition(
        self, condition: callable, timeout: int | None = None, interval: int = 100
    ) -> Any:
        """
        等待自定义条件

        Args:
            condition: 条件函数，返回True时停止等待
            timeout: 超时时间（毫秒）
            interval: 检查间隔（毫秒）

        Returns:
            Any: condition函数的返回值

        Raises:
            TimeoutError: 超时
        """
        import time

        timeout_ms = timeout or self.default_timeout
        start_time = time.time() * 1000
        last_exception = None

        while (time.time() * 1000 - start_time) < timeout_ms:
            try:
                result = condition()
                if result:
                    return result
            except Exception as e:
                last_exception = e

            time.sleep(interval / 1000)

        raise TimeoutError(
            f"等待条件超时 ({timeout_ms}ms)" + (f": {last_exception}" if last_exception else "")
        )

    def for_text_visible(self, text: str, timeout: int | None = None) -> None:
        """等待包含指定文本的元素可见"""
        locator = self.page.get_by_text(text)
        expect(locator).to_be_visible(timeout=timeout or self.default_timeout)

    def for_count(self, selector: str, count: int, timeout: int | None = None) -> None:
        """等待元素数量达到指定值"""
        locator = self.page.locator(selector)
        expect(locator).to_have_count(count, timeout=timeout or self.default_timeout)


__all__ = ["ElementLocator", "LocatorType", "WaitHelper"]
