"""页面对象基类

提供UI自动化测试的页面对象模式(POM)基类
基于 Playwright 实现
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

try:
    from playwright.sync_api import Locator, Page

    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    Page = Any
    Locator = Any


class BasePage(ABC):
    """
    页面对象基类

    提供页面对象模式(POM)的基础功能：
    - 元素定位和操作
    - 页面等待策略
    - 截图功能
    - 日志记录
    - 常用操作封装

    子类应该：
    1. 定义页面URL
    2. 定义页面元素定位器
    3. 实现wait_for_page_load()方法
    4. 提供业务操作方法

    示例:
        >>> class LoginPage(BasePage):
        ...     def __init__(self, page: Page):
        ...         super().__init__(page, url="/login")
        ...         self.username_input = "#username"
        ...         self.password_input = "#password"
        ...         self.login_button = "button[type='submit']"
        ...
        ...     def wait_for_page_load(self):
        ...         self.wait_for_selector(self.login_button)
        ...
        ...     def login(self, username: str, password: str):
        ...         self.fill(self.username_input, username)
        ...         self.fill(self.password_input, password)
        ...         self.click(self.login_button)
    """

    def __init__(self, page: Page, url: str | None = None, base_url: str = ""):
        """
        初始化页面对象

        Args:
            page: Playwright Page实例
            url: 页面相对URL（如 "/login"）
            base_url: 基础URL（如 "https://example.com"）

        Raises:
            ImportError: 如果未安装playwright
        """
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError(
                "Playwright未安装。请运行: pip install playwright && playwright install"
            )

        self.page = page
        self.url = url
        self.base_url = base_url

    @abstractmethod
    def wait_for_page_load(self) -> None:
        """
        等待页面加载完成

        子类必须实现此方法来定义页面加载完成的标志，例如：
        - 等待特定元素出现
        - 等待网络空闲
        - 等待页面标题
        """
        pass

    # ========== 页面导航 ==========

    def goto(self, url: str | None = None, **kwargs: Any) -> None:
        """
        导航到页面

        Args:
            url: 目标URL，如果为None则使用self.url
            kwargs: goto的其他参数

        Raises:
            ValueError: 如果url和self.url都为None
        """
        target_url = url or self.url
        if not target_url:
            raise ValueError("必须提供url参数或在构造函数中设置self.url")

        full_url = f"{self.base_url}{target_url}" if self.base_url else target_url
        self.page.goto(full_url, **kwargs)
        self.wait_for_page_load()

    def reload(self, **kwargs: Any) -> None:
        """刷新页面"""
        self.page.reload(**kwargs)
        self.wait_for_page_load()

    def go_back(self, **kwargs: Any) -> None:
        """返回上一页"""
        self.page.go_back(**kwargs)

    def go_forward(self, **kwargs: Any) -> None:
        """前进到下一页"""
        self.page.go_forward(**kwargs)

    # ========== 元素定位 ==========

    def locator(self, selector: str) -> Locator:
        """
        获取元素定位器

        Args:
            selector: CSS选择器、XPath或文本选择器

        Returns:
            Locator: Playwright定位器对象
        """
        return self.page.locator(selector)

    def get_by_role(self, role: str, **kwargs: Any) -> Locator:
        """通过ARIA role定位元素"""
        return self.page.get_by_role(role, **kwargs)

    def get_by_text(self, text: str, **kwargs: Any) -> Locator:
        """通过文本内容定位元素"""
        return self.page.get_by_text(text, **kwargs)

    def get_by_label(self, label: str, **kwargs: Any) -> Locator:
        """通过label定位元素"""
        return self.page.get_by_label(label, **kwargs)

    def get_by_placeholder(self, placeholder: str, **kwargs: Any) -> Locator:
        """通过placeholder定位元素"""
        return self.page.get_by_placeholder(placeholder, **kwargs)

    def get_by_test_id(self, test_id: str) -> Locator:
        """通过data-testid定位元素"""
        return self.page.get_by_test_id(test_id)

    # ========== 元素操作 ==========

    def click(self, selector: str, **kwargs: Any) -> None:
        """点击元素"""
        self.locator(selector).click(**kwargs)

    def double_click(self, selector: str, **kwargs: Any) -> None:
        """双击元素"""
        self.locator(selector).dblclick(**kwargs)

    def fill(self, selector: str, value: str, **kwargs: Any) -> None:
        """填充输入框"""
        self.locator(selector).fill(value, **kwargs)

    def clear(self, selector: str) -> None:
        """清空输入框"""
        self.locator(selector).clear()

    def type(self, selector: str, text: str, **kwargs: Any) -> None:
        """逐字输入文本（模拟键盘输入）"""
        self.locator(selector).type(text, **kwargs)

    def select_option(self, selector: str, value: str | list[str], **kwargs: Any) -> None:
        """选择下拉框选项"""
        self.locator(selector).select_option(value, **kwargs)

    def check(self, selector: str, **kwargs: Any) -> None:
        """勾选复选框"""
        self.locator(selector).check(**kwargs)

    def uncheck(self, selector: str, **kwargs: Any) -> None:
        """取消勾选复选框"""
        self.locator(selector).uncheck(**kwargs)

    def hover(self, selector: str, **kwargs: Any) -> None:
        """鼠标悬停"""
        self.locator(selector).hover(**kwargs)

    # ========== 元素查询 ==========

    def get_text(self, selector: str) -> str:
        """获取元素文本内容"""
        return self.locator(selector).text_content() or ""

    def get_inner_text(self, selector: str) -> str:
        """获取元素内部文本（不包含HTML标签）"""
        return self.locator(selector).inner_text()

    def get_attribute(self, selector: str, name: str) -> str | None:
        """获取元素属性值"""
        return self.locator(selector).get_attribute(name)

    def get_value(self, selector: str) -> str:
        """获取输入框的值"""
        return self.locator(selector).input_value()

    def is_visible(self, selector: str) -> bool:
        """检查元素是否可见"""
        return self.locator(selector).is_visible()

    def is_enabled(self, selector: str) -> bool:
        """检查元素是否可用"""
        return self.locator(selector).is_enabled()

    def is_checked(self, selector: str) -> bool:
        """检查复选框/单选框是否被选中"""
        return self.locator(selector).is_checked()

    def count(self, selector: str) -> int:
        """获取匹配元素的数量"""
        return self.locator(selector).count()

    # ========== 等待策略 ==========

    def wait_for_selector(
        self, selector: str, state: str = "visible", timeout: int | None = None
    ) -> None:
        """
        等待元素出现

        Args:
            selector: 选择器
            state: 状态 (visible/hidden/attached/detached)
            timeout: 超时时间（毫秒）
        """
        self.page.wait_for_selector(selector, state=state, timeout=timeout)

    def wait_for_url(self, url: str | Any, **kwargs: Any) -> None:
        """等待URL匹配"""
        self.page.wait_for_url(url, **kwargs)

    def wait_for_load_state(self, state: str = "load", **kwargs: Any) -> None:
        """
        等待页面加载状态

        Args:
            state: 状态 (load/domcontentloaded/networkidle)
        """
        self.page.wait_for_load_state(state, **kwargs)

    def wait_for_timeout(self, timeout: int) -> None:
        """等待指定时间（毫秒）"""
        self.page.wait_for_timeout(timeout)

    # ========== 截图 ==========

    def screenshot(self, path: str | Path | None = None, **kwargs: Any) -> bytes:
        """
        页面截图

        Args:
            path: 保存路径，如果为None则返回字节数据
            kwargs: 其他截图参数

        Returns:
            bytes: 截图数据
        """
        return self.page.screenshot(path=path, **kwargs)

    def screenshot_element(
        self, selector: str, path: str | Path | None = None, **kwargs: Any
    ) -> bytes:
        """
        元素截图

        Args:
            selector: 元素选择器
            path: 保存路径
            kwargs: 其他截图参数

        Returns:
            bytes: 截图数据
        """
        return self.locator(selector).screenshot(path=path, **kwargs)

    # ========== 页面信息 ==========

    @property
    def title(self) -> str:
        """获取页面标题"""
        return self.page.title()

    @property
    def current_url(self) -> str:
        """获取当前URL"""
        return self.page.url

    def evaluate(self, expression: str, arg: Any = None) -> Any:
        """
        执行JavaScript代码

        Args:
            expression: JS表达式
            arg: 传递给JS的参数

        Returns:
            Any: JS执行结果
        """
        return self.page.evaluate(expression, arg)

    # ========== 便捷方法 ==========

    def scroll_to_element(self, selector: str) -> None:
        """滚动到元素位置"""
        self.locator(selector).scroll_into_view_if_needed()

    def scroll_to_top(self) -> None:
        """滚动到页面顶部"""
        self.evaluate("window.scrollTo(0, 0)")

    def scroll_to_bottom(self) -> None:
        """滚动到页面底部"""
        self.evaluate("window.scrollTo(0, document.body.scrollHeight)")


__all__ = ["BasePage"]
