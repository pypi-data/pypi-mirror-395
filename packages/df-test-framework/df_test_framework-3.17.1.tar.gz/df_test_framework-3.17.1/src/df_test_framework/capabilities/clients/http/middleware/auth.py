"""
认证中间件

提供 Bearer Token 等认证方式。

v3.17.0+:
- 支持静态 Token (STATIC)
- 支持动态登录获取 Token (LOGIN)
- 支持环境变量读取 Token (ENV)
"""

import asyncio
import os
from collections.abc import Awaitable, Callable
from typing import Any

from loguru import logger

from df_test_framework.capabilities.clients.http.core.request import Request
from df_test_framework.capabilities.clients.http.core.response import Response
from df_test_framework.core.middleware import BaseMiddleware


class LoginTokenProvider:
    """登录 Token 提供器

    通过调用登录接口动态获取 Token，并缓存以避免重复登录。

    v3.17.0+: 支持配置驱动的动态登录获取 Token。

    示例:
        provider = LoginTokenProvider(
            login_url="/admin/login",
            credentials={"username": "admin", "password": "pass"},
            token_path="data.token",  # 从响应 JSON 中提取 token 的路径
        )

        token = await provider.get_token(http_client)
    """

    def __init__(
        self,
        login_url: str,
        credentials: dict[str, Any],
        token_path: str = "data.token",
        cache_token: bool = True,
    ):
        """初始化登录 Token 提供器

        Args:
            login_url: 登录接口 URL（相对路径）
            credentials: 登录凭据（如 {"username": "admin", "password": "pass"}）
            token_path: Token 在响应 JSON 中的路径（如 "data.token"）
            cache_token: 是否缓存 Token（默认 True）
        """
        self.login_url = login_url
        self.credentials = credentials
        self.token_path = token_path
        self.cache_token = cache_token
        self._cached_token: str | None = None
        self._lock = asyncio.Lock()

    async def get_token(self, http_client: Any) -> str:
        """获取 Token

        如果已缓存且有效，返回缓存的 Token；否则调用登录接口获取新 Token。

        Args:
            http_client: HTTP 客户端实例（用于调用登录接口）

        Returns:
            JWT Token 字符串

        Raises:
            ValueError: 登录失败或无法提取 Token
        """
        # 如果有缓存且启用缓存，直接返回
        if self.cache_token and self._cached_token:
            logger.debug("[LoginTokenProvider] 使用缓存的 Token")
            return self._cached_token

        async with self._lock:
            # 双重检查锁定
            if self.cache_token and self._cached_token:
                return self._cached_token

            logger.info(f"[LoginTokenProvider] 调用登录接口: {self.login_url}")

            # 调用登录接口
            # 注意：这里需要绕过中间件，直接调用底层 HTTP 客户端
            response = await self._do_login(http_client)

            # 从响应中提取 Token
            token = self._extract_token(response)

            if self.cache_token:
                self._cached_token = token
                logger.info("[LoginTokenProvider] Token 已缓存")

            return token

    async def _do_login(self, http_client: Any) -> dict[str, Any]:
        """执行登录请求

        Args:
            http_client: HTTP 客户端

        Returns:
            登录响应 JSON
        """
        # 获取底层的 httpx 客户端
        raw_client = getattr(http_client, "_client", http_client)

        # 构建完整 URL
        base_url = str(getattr(http_client, "base_url", ""))
        full_url = f"{base_url.rstrip('/')}{self.login_url}"

        logger.debug(f"[LoginTokenProvider] POST {full_url}")

        # 直接调用 httpx 客户端（绕过中间件）
        if hasattr(raw_client, "post"):
            # httpx.AsyncClient
            response = await raw_client.post(full_url, json=self.credentials)
        else:
            # 降级：使用 http_client 的方法
            response = await http_client.post(self.login_url, json=self.credentials)

        # 解析响应
        if hasattr(response, "json"):
            if asyncio.iscoroutinefunction(response.json):
                return await response.json()
            return response.json()

        raise ValueError(f"登录失败: 无法解析响应 {response}")

    def _extract_token(self, response: dict[str, Any]) -> str:
        """从响应中提取 Token

        Args:
            response: 登录响应 JSON

        Returns:
            Token 字符串

        Raises:
            ValueError: 无法提取 Token
        """
        # 按路径提取（如 "data.token" -> response["data"]["token"]）
        parts = self.token_path.split(".")
        value = response

        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                raise ValueError(
                    f"无法从响应中提取 Token: 路径 '{self.token_path}' 不存在。响应: {response}"
                )

        if not isinstance(value, str) or not value:
            raise ValueError(f"Token 值无效: {value}")

        logger.debug(f"[LoginTokenProvider] 成功提取 Token: {value[:20]}...")
        return value

    def clear_cache(self) -> None:
        """清除缓存的 Token"""
        self._cached_token = None
        logger.debug("[LoginTokenProvider] Token 缓存已清除")


class BearerTokenMiddleware(BaseMiddleware[Request, Response]):
    """Bearer Token 认证中间件

    自动为请求添加 Authorization: Bearer <token> 头。

    v3.17.0+ 支持三种模式:
    1. 静态 Token (STATIC): 直接提供 token
    2. 动态 Token Provider: 提供获取 token 的回调函数
    3. 登录获取 Token (LOGIN): 通过配置自动登录获取 Token
    4. 环境变量 (ENV): 从环境变量读取 Token

    示例:
        # 方式1: 静态 Token
        middleware = BearerTokenMiddleware(token="my_token")

        # 方式2: 动态 Token Provider
        async def get_token():
            return await auth_service.get_token()
        middleware = BearerTokenMiddleware(token_provider=get_token)

        # 方式3: 登录获取 Token（需要 http_client）
        middleware = BearerTokenMiddleware(
            login_token_provider=LoginTokenProvider(
                login_url="/admin/login",
                credentials={"username": "admin", "password": "pass"},
            )
        )
    """

    def __init__(
        self,
        token: str | None = None,
        token_provider: Callable[[], Awaitable[str]] | None = None,
        login_token_provider: LoginTokenProvider | None = None,
        header_name: str = "Authorization",
        header_prefix: str = "Bearer",
        priority: int = 20,
    ):
        """初始化认证中间件

        Args:
            token: 静态 Token
            token_provider: Token 提供函数（异步）
            login_token_provider: 登录 Token 提供器
            header_name: Header 名称
            header_prefix: Header 前缀
            priority: 优先级
        """
        super().__init__(name="BearerTokenMiddleware", priority=priority)
        self._token = token
        self._token_provider = token_provider
        self._login_token_provider = login_token_provider
        self.header_name = header_name
        self.header_prefix = header_prefix
        self._http_client: Any = None  # 延迟注入的 HTTP 客户端

        if not token and not token_provider and not login_token_provider:
            raise ValueError("必须提供 token、token_provider 或 login_token_provider 之一")

    def set_http_client(self, http_client: Any) -> None:
        """设置 HTTP 客户端（用于登录模式）

        Args:
            http_client: HTTP 客户端实例
        """
        self._http_client = http_client

    async def __call__(
        self,
        request: Request,
        call_next,
    ) -> Response:
        """添加认证头"""
        # 获取 Token
        token = await self._get_token()

        # 添加 Authorization 头
        auth_value = f"{self.header_prefix} {token}" if self.header_prefix else token
        request = request.with_header(self.header_name, auth_value)

        return await call_next(request)

    async def _get_token(self) -> str:
        """获取 Token

        按优先级尝试：token_provider > login_token_provider > static token
        """
        if self._token_provider:
            return await self._token_provider()

        if self._login_token_provider:
            if not self._http_client:
                raise ValueError(
                    "使用 login_token_provider 时必须先调用 set_http_client() 注入 HTTP 客户端"
                )
            return await self._login_token_provider.get_token(self._http_client)

        if self._token:
            return self._token

        raise ValueError("无法获取 Token: 未配置任何 Token 来源")


def create_env_token_provider(env_var: str = "API_TOKEN") -> Callable[[], Awaitable[str]]:
    """创建环境变量 Token 提供器

    从环境变量读取 Token。

    Args:
        env_var: 环境变量名称（默认 API_TOKEN）

    Returns:
        异步 Token 提供函数

    示例:
        middleware = BearerTokenMiddleware(
            token_provider=create_env_token_provider("MY_API_TOKEN")
        )
    """

    async def get_token_from_env() -> str:
        token = os.environ.get(env_var)
        if not token:
            raise ValueError(f"环境变量 '{env_var}' 未设置或为空")
        return token

    return get_token_from_env


class ApiKeyMiddleware(BaseMiddleware[Request, Response]):
    """API Key 认证中间件

    将 API Key 添加到请求头或查询参数中。

    示例:
        # Header 方式
        middleware = ApiKeyMiddleware(
            api_key="my_key",
            header_name="X-API-Key",
        )

        # 查询参数方式
        middleware = ApiKeyMiddleware(
            api_key="my_key",
            param_name="api_key",
            in_header=False,
        )
    """

    def __init__(
        self,
        api_key: str,
        header_name: str = "X-API-Key",
        param_name: str = "api_key",
        in_header: bool = True,
        priority: int = 20,
    ):
        """初始化 API Key 中间件

        Args:
            api_key: API Key
            header_name: Header 名称（当 in_header=True 时使用）
            param_name: 参数名称（当 in_header=False 时使用）
            in_header: 是否放在 Header 中
            priority: 优先级
        """
        super().__init__(name="ApiKeyMiddleware", priority=priority)
        self.api_key = api_key
        self.header_name = header_name
        self.param_name = param_name
        self.in_header = in_header

    async def __call__(
        self,
        request: Request,
        call_next,
    ) -> Response:
        """添加 API Key"""
        if self.in_header:
            request = request.with_header(self.header_name, self.api_key)
        else:
            request = request.with_param(self.param_name, self.api_key)

        return await call_next(request)
