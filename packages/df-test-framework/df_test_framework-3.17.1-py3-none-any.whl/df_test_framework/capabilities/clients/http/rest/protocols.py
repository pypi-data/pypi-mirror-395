"""REST客户端协议定义

定义REST客户端的标准接口，支持多种实现（httpx、requests等）
"""

from typing import Any, Protocol, Self


class RestClientProtocol(Protocol):
    """REST客户端协议

    定义所有REST客户端实现必须遵循的接口
    """

    def __enter__(self) -> Self:
        """进入上下文管理器"""
        ...

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """退出上下文管理器"""
        ...

    def request(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> Any:
        """发送HTTP请求

        Args:
            method: HTTP方法（GET、POST等）
            url: 请求URL
            **kwargs: 其他请求参数

        Returns:
            响应对象
        """
        ...

    def get(self, url: str, **kwargs: Any) -> Any:
        """发送GET请求"""
        ...

    def post(self, url: str, **kwargs: Any) -> Any:
        """发送POST请求"""
        ...

    def put(self, url: str, **kwargs: Any) -> Any:
        """发送PUT请求"""
        ...

    def patch(self, url: str, **kwargs: Any) -> Any:
        """发送PATCH请求"""
        ...

    def delete(self, url: str, **kwargs: Any) -> Any:
        """发送DELETE请求"""
        ...

    def close(self) -> None:
        """关闭客户端"""
        ...


class BaseAPIProtocol(Protocol):
    """业务API基类协议

    定义业务API的标准接口
    """

    def __init__(self, client: RestClientProtocol, base_url: str | None = None):
        """初始化API

        Args:
            client: REST客户端实例
            base_url: 基础URL（可选）
        """
        ...

    def request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any,
    ) -> Any:
        """发送API请求

        Args:
            method: HTTP方法
            endpoint: API端点
            **kwargs: 其他请求参数

        Returns:
            响应数据
        """
        ...
