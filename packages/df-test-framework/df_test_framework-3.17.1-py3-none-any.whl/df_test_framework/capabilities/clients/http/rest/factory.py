"""REST客户端工厂

提供统一的REST客户端创建接口，支持多种实现
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from df_test_framework.infrastructure.config.schema import HTTPConfig

from .protocols import RestClientProtocol

if TYPE_CHECKING:
    from .httpx.client import HttpClient

ClientType = Literal["httpx", "requests"]


class RestClientFactory:
    """REST客户端工厂

    根据配置创建合适的REST客户端实现

    Examples:
        >>> # 使用默认httpx实现
        >>> client = RestClientFactory.create()
        >>>
        >>> # 使用requests实现（预留）
        >>> client = RestClientFactory.create(client_type="requests")
        >>>
        >>> # 使用自定义配置
        >>> config = HTTPConfig(base_url="https://api.example.com")
        >>> client = RestClientFactory.create(config=config)
    """

    @staticmethod
    def create(
        client_type: ClientType = "httpx",
        config: HTTPConfig | None = None,
    ) -> RestClientProtocol:
        """创建REST客户端

        Args:
            client_type: 客户端类型，默认"httpx"
            config: HTTP配置，如果为None则使用默认配置

        Returns:
            REST客户端实例

        Raises:
            ValueError: 不支持的客户端类型
        """
        if client_type == "httpx":
            from .httpx.client import HttpClient

            # ✅ Bug修复: 正确传递HTTPConfig参数到HttpClient
            if config is None:
                config = HTTPConfig()

            # base_url可能为None，使用默认值
            base_url = config.base_url or "http://localhost"

            return HttpClient(
                base_url=base_url,
                timeout=config.timeout,
                verify_ssl=config.verify_ssl,
                max_retries=config.max_retries,
                max_connections=config.max_connections,
                max_keepalive_connections=config.max_keepalive_connections,
                config=config,  # 传递config用于加载拦截器
            )
        elif client_type == "requests":
            # 预留：未来实现requests客户端
            raise NotImplementedError(
                "requests客户端尚未实现。请使用httpx客户端或提交PR实现requests适配器。"
            )
        else:
            raise ValueError(f"不支持的客户端类型: {client_type}。支持的类型: httpx, requests")

    @staticmethod
    def create_httpx(config: HTTPConfig | None = None) -> HttpClient:
        """创建httpx客户端（便捷方法）

        Args:
            config: HTTP配置

        Returns:
            HttpClient实例
        """
        from .httpx.client import HttpClient

        # ✅ Bug修复: 正确传递HTTPConfig参数到HttpClient
        if config is None:
            config = HTTPConfig()

        # base_url可能为None，使用默认值
        base_url = config.base_url or "http://localhost"

        return HttpClient(
            base_url=base_url,
            timeout=config.timeout,
            verify_ssl=config.verify_ssl,
            max_retries=config.max_retries,
            max_connections=config.max_connections,
            max_keepalive_connections=config.max_keepalive_connections,
            config=config,  # 传递config用于加载拦截器
        )

    @staticmethod
    def create_requests(config: HTTPConfig | None = None):
        """创建requests客户端（预留）

        Args:
            config: HTTP配置

        Returns:
            RequestsClient实例

        Raises:
            NotImplementedError: 功能尚未实现
        """
        raise NotImplementedError(
            "requests客户端尚未实现。请使用create_httpx()或提交PR实现requests适配器。"
        )
