"""Web浏览器驱动协议定义

定义Web驱动的标准接口，支持多种实现（Playwright、Selenium等）
"""

from typing import Any, Protocol, Self


class WebDriverProtocol(Protocol):
    """Web浏览器驱动协议

    定义所有Web驱动实现必须遵循的接口
    """

    def __enter__(self) -> Self:
        """进入上下文管理器"""
        ...

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """退出上下文管理器"""
        ...

    def start(self) -> None:
        """启动浏览器"""
        ...

    def stop(self) -> None:
        """停止浏览器"""
        ...

    def navigate(self, url: str) -> None:
        """导航到URL"""
        ...

    def find_element(self, locator: str, locator_type: str = "css") -> Any:
        """查找单个元素"""
        ...

    def find_elements(self, locator: str, locator_type: str = "css") -> list[Any]:
        """查找多个元素"""
        ...

    def click(self, locator: str, locator_type: str = "css") -> None:
        """点击元素"""
        ...

    def input_text(self, locator: str, text: str, locator_type: str = "css") -> None:
        """输入文本"""
        ...

    def get_text(self, locator: str, locator_type: str = "css") -> str:
        """获取元素文本"""
        ...

    def screenshot(self, path: str | None = None) -> bytes:
        """截图"""
        ...


class PageProtocol(Protocol):
    """页面对象协议

    定义页面对象的标准接口
    """

    def __init__(self, driver: WebDriverProtocol):
        """初始化页面对象

        Args:
            driver: Web驱动实例
        """
        ...

    def goto(self, url: str | None = None) -> None:
        """访问页面

        Args:
            url: 页面URL，如果为None则使用默认URL
        """
        ...

    def wait_for_load(self, timeout: float = 30.0) -> None:
        """等待页面加载完成

        Args:
            timeout: 超时时间（秒）
        """
        ...
