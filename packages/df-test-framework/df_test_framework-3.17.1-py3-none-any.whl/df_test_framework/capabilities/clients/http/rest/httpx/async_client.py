"""异步HTTP客户端封装

v3.8.0 新增:
- AsyncHttpClient: 基于 httpx.AsyncClient 的异步HTTP客户端
- 支持并发请求，性能提升10-50倍
- 完整的拦截器支持（异步适配）
- 上下文管理器（async with）

v3.14.0 重构:
- 集成 MiddlewareChain（洋葱模型）
- 支持 middlewares=[] 构造参数
- 支持 .use(middleware) 链式调用
- 集成 EventBus 发布 HTTP 事件
- 保持向后兼容：interceptors 参数仍可用（已废弃）

v3.16.0 重构:
- 完全移除 InterceptorChain，统一使用 MiddlewareChain
- 支持从 HTTPConfig.middlewares 自动加载
- 移除 config.interceptors 兼容代码

v3.17.0 重构:
- 使用新事件系统（带 correlation_id 的事件关联）
- 使用事件工厂方法创建事件

典型使用场景:
- 并发API测试（同时发送多个请求）
- 压力测试（高QPS场景）
- 批量数据处理

示例:
    基础使用::

        async with AsyncHttpClient("https://api.example.com") as client:
            response = await client.get("/users/1")
            assert response.status == 200

    并发请求::

        async with AsyncHttpClient("https://api.example.com") as client:
            # 并发100个请求
            tasks = [client.get(f"/users/{i}") for i in range(100)]
            responses = await asyncio.gather(*tasks)
            assert len(responses) == 100

    使用中间件 (v3.16.0)::

        async with AsyncHttpClient(
            "https://api.example.com",
            middlewares=[
                RetryMiddleware(max_attempts=3),
                SignatureMiddleware(secret="xxx"),
            ]
        ) as client:
            response = await client.post("/users", json={"name": "Alice"})
"""

from __future__ import annotations

import re
import time
from typing import TYPE_CHECKING, Any

import httpx
from loguru import logger
from pydantic import BaseModel

from df_test_framework.capabilities.clients.http.core import (
    Request,
    Response,
)
from df_test_framework.capabilities.clients.http.middleware import (
    MiddlewareFactory,
    PathFilteredMiddleware,
)
from df_test_framework.core.events import (
    HttpRequestEndEvent,
    HttpRequestErrorEvent,
    HttpRequestStartEvent,
)
from df_test_framework.core.middleware import (
    Middleware,
    MiddlewareChain,
)

if TYPE_CHECKING:
    from df_test_framework.infrastructure.config.schema import HTTPConfig
    from df_test_framework.infrastructure.events import EventBus


def sanitize_url_async(url: str) -> str:
    """
    异步版本的URL脱敏（实际上是同步的，但保持命名一致）

    将敏感参数值替换为****:
    - token, access_token, refresh_token
    - key, api_key, secret, secret_key
    - password
    - authorization

    Args:
        url: 原始URL

    Returns:
        脱敏后的URL
    """
    sensitive_params = [
        "token",
        "access_token",
        "refresh_token",
        "key",
        "api_key",
        "secret",
        "secret_key",
        "password",
        "passwd",
        "authorization",
        "auth",
    ]

    for param in sensitive_params:
        pattern = rf"([?&]{param}=)[^&]*"
        url = re.sub(pattern, r"\1****", url, flags=re.IGNORECASE)

    return url


class AsyncHttpClient:
    """
    异步HTTP客户端封装

    基于 httpx.AsyncClient，提供:
    - 🆕 v3.16.0: 纯中间件系统（完全移除 InterceptorChain）
    - 🆕 v3.16.0: 支持从 HTTPConfig.middlewares 自动加载
    - 🆕 v3.14.0: 统一中间件系统（洋葱模型）
    - 🆕 v3.14.0: 集成 EventBus 发布 HTTP 事件
    - 异步HTTP请求（get/post/put/delete/patch）
    - 上下文管理器
    - 连接池管理
    - HTTP/2 支持

    性能优势:
    - 并发100个请求: 从30秒降至1秒（30倍提升）
    - 非阻塞IO: CPU利用率更高
    - 连接复用: 减少TCP握手开销

    Note:
        异步客户端必须在异步上下文中使用:
        - 使用 async with 确保资源正确释放
        - 所有方法都是 async def，需要 await 调用
    """

    def __init__(
        self,
        base_url: str | None = None,
        timeout: int | None = None,
        headers: dict[str, str] | None = None,
        verify_ssl: bool | None = None,
        max_connections: int | None = None,
        max_keepalive_connections: int | None = None,
        http2: bool = True,  # 默认启用HTTP/2
        config: HTTPConfig | None = None,
        middlewares: list[Middleware[Request, Response]] | None = None,
        event_bus: EventBus | None = None,
    ):
        """
        初始化异步HTTP客户端

        配置优先级: 显式参数 > HTTPConfig > 默认值

        Args:
            base_url: API基础URL (优先使用，其次config.base_url)
            timeout: 请求超时时间(秒) (优先使用，其次config.timeout，默认30)
            headers: 默认请求头
            verify_ssl: 是否验证SSL证书 (优先使用，其次config.verify_ssl，默认True)
            max_connections: 最大并发连接数 (优先使用，其次config.max_connections，默认100)
            max_keepalive_connections: Keep-Alive连接数 (优先使用，其次config.max_keepalive_connections，默认20)
            http2: 是否启用HTTP/2，默认True
            config: 🆕 v3.16.0 HTTPConfig配置对象（用于自动加载中间件）
            middlewares: 🆕 v3.16.0 中间件列表（如果为空，从 config.middlewares 加载）
            event_bus: 🆕 v3.14.0 事件总线（可选，用于发布 HTTP 事件）

        Example::

            # 基础初始化
            client = AsyncHttpClient("https://api.example.com")

            # 自定义配置
            client = AsyncHttpClient(
                base_url="https://api.example.com",
                timeout=60,
                headers={"X-API-Key": "xxx"},
                max_connections=200,
                http2=True
            )

            # v3.16.0: 使用HTTPConfig (推荐)
            config = HTTPConfig(base_url="https://api.example.com", timeout=60, middlewares=[...])
            client = AsyncHttpClient(config=config)

            # 混合使用: 显式参数覆盖config
            config = HTTPConfig(timeout=30, verify_ssl=True)
            client = AsyncHttpClient("https://api.example.com", timeout=60, config=config)
            # 结果: timeout=60 (显式参数优先)
        """
        # 配置优先级: 显式参数 > HTTPConfig > 默认值
        effective_base_url = (
            base_url or (config.base_url if config else None) or "http://localhost:8000"
        )
        effective_timeout = timeout if timeout is not None else (config.timeout if config else 30)
        effective_verify_ssl = (
            verify_ssl if verify_ssl is not None else (config.verify_ssl if config else True)
        )
        effective_max_connections = (
            max_connections
            if max_connections is not None
            else (config.max_connections if config else 100)
        )
        effective_max_keepalive = (
            max_keepalive_connections
            if max_keepalive_connections is not None
            else (config.max_keepalive_connections if config else 20)
        )

        self.base_url = effective_base_url
        self.timeout = effective_timeout
        self.default_headers = headers or {}
        self.verify_ssl = effective_verify_ssl
        self.http2 = http2
        self._event_bus = event_bus

        # v3.16.0: 纯中间件系统
        self._middleware_chain: MiddlewareChain[Request, Response] | None = None
        self._middlewares: list[Middleware[Request, Response]] = []

        # 配置连接限制
        limits = httpx.Limits(
            max_connections=effective_max_connections,
            max_keepalive_connections=effective_max_keepalive,
        )

        # 创建异步客户端
        self.client = httpx.AsyncClient(
            base_url=effective_base_url,
            timeout=effective_timeout,
            headers=self.default_headers,
            limits=limits,
            verify=effective_verify_ssl,
            http2=http2,
            follow_redirects=True,
        )

        logger.debug(
            f"异步HTTP客户端已初始化: base_url={effective_base_url}, "
            f"timeout={effective_timeout}s, max_connections={effective_max_connections}, http2={http2}"
        )

        # v3.16.0: 加载中间件
        if middlewares:
            # 方式1: 手动传入中间件列表
            for mw in middlewares:
                self.use(mw)
        elif config and config.middlewares:
            # 方式2: 从 HTTPConfig.middlewares 自动加载
            self._load_middlewares_from_config(config.middlewares)

    def set_auth_token(self, token: str, token_type: str = "Bearer") -> None:
        """
        设置认证token

        Args:
            token: 认证令牌
            token_type: 令牌类型（Bearer, Basic等）

        Example::

            client.set_auth_token("abc123", "Bearer")
            # 后续请求会自动添加: Authorization: Bearer abc123
        """
        self.client.headers["Authorization"] = f"{token_type} {token}"
        logger.debug(f"已设置认证token: {token_type} {token[:10]}...")

    def use(self, middleware: Middleware[Request, Response]) -> AsyncHttpClient:
        """添加中间件（链式调用）

        v3.14.0 新增

        Args:
            middleware: 要添加的中间件

        Returns:
            self，支持链式调用

        Example:
            client.use(RetryMiddleware()).use(LoggingMiddleware())
        """
        self._middlewares.append(middleware)
        # 重置链，下次执行时重新构建
        self._middleware_chain = None
        logger.debug(f"添加中间件: {middleware.name} (priority={middleware.priority})")
        return self

    # ==================== v3.14.0: 中间件执行 ====================

    def _build_middleware_chain(self) -> MiddlewareChain[Request, Response]:
        """构建中间件链（懒加载）"""
        if self._middleware_chain is not None:
            return self._middleware_chain

        # 创建最终处理器（发送实际 HTTP 请求）
        async def send_request(request: Request) -> Response:
            return await self._send_request_async(request)

        chain = MiddlewareChain[Request, Response](send_request)
        for mw in self._middlewares:
            chain.use(mw)

        self._middleware_chain = chain
        return chain

    async def _send_request_async(self, request: Request) -> Response:
        """异步发送 HTTP 请求（中间件链的最终处理器）"""
        params: dict[str, Any] = {}
        if request.headers:
            params["headers"] = dict(request.headers)
        if request.params:
            params["params"] = dict(request.params)
        if request.json is not None:
            params["json"] = request.json
        if request.data is not None:
            params["data"] = request.data

        httpx_response = await self.client.request(request.method, request.url, **params)
        return self._parse_response(httpx_response)

    async def _publish_event(self, event: Any) -> None:
        """发布事件到 EventBus

        v3.17.0: 动态获取 EventBus（支持测试隔离，每个测试使用独立的 EventBus）。
        """
        # 动态获取 EventBus（优先使用测试上下文的 EventBus）
        event_bus = self._event_bus
        if event_bus is None:
            from df_test_framework.infrastructure.events import get_event_bus

            event_bus = get_event_bus()

        if event_bus:
            await event_bus.publish(event)

    # ==================== 核心请求方法 ====================

    async def get(self, url: str, **kwargs) -> Response:
        """
        异步GET请求

        Args:
            url: 请求路径
            **kwargs: httpx支持的参数（params, headers等）

        Returns:
            Response对象

        Example::

            response = await client.get("/users")
            response = await client.get("/users/1")
            response = await client.get("/search", params={"q": "python"})
        """
        return await self.request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs) -> Response:
        """
        异步POST请求

        Args:
            url: 请求路径
            **kwargs: httpx支持的参数（json, data, headers等）

        Returns:
            Response对象

        Example::

            response = await client.post("/users", json={"name": "Alice"})
            response = await client.post("/login", data={"user": "admin"})
        """
        return await self.request("POST", url, **kwargs)

    async def put(self, url: str, **kwargs) -> Response:
        """
        异步PUT请求

        Args:
            url: 请求路径
            **kwargs: httpx支持的参数

        Returns:
            Response对象

        Example::

            response = await client.put("/users/1", json={"name": "Bob"})
        """
        return await self.request("PUT", url, **kwargs)

    async def delete(self, url: str, **kwargs) -> Response:
        """
        异步DELETE请求

        Args:
            url: 请求路径
            **kwargs: httpx支持的参数

        Returns:
            Response对象

        Example::

            response = await client.delete("/users/1")
        """
        return await self.request("DELETE", url, **kwargs)

    async def patch(self, url: str, **kwargs) -> Response:
        """
        异步PATCH请求

        Args:
            url: 请求路径
            **kwargs: httpx支持的参数

        Returns:
            Response对象

        Example::

            response = await client.patch("/users/1", json={"age": 30})
        """
        return await self.request("PATCH", url, **kwargs)

    async def request(self, method: str, url: str, **kwargs) -> Response:
        """
        通用异步请求方法

        ✅ v3.16.0: 纯中间件系统（移除 InterceptorChain）
        ✅ v3.14.0: 优先使用中间件系统
        ✅ v3.17.0: 使用新事件系统（带 correlation_id 的事件关联）

        Args:
            method: HTTP方法（GET/POST/PUT/DELETE/PATCH）
            url: 请求路径
            **kwargs: httpx支持的参数

        Returns:
            Response对象

        Raises:
            httpx.HTTPError: HTTP请求错误
            Exception: 其他异常

        执行流程:
            1. 准备Request对象
            2. 执行中间件链（如果已配置）
            3. 发送异步HTTP请求
            4. 解析响应
            5. 返回Response对象
        """
        # 准备请求对象
        request_obj = self._prepare_request_object(method, url, **kwargs)

        # v3.17.0: 使用事件工厂方法创建 Start 事件，获取 correlation_id
        start_time = time.time()
        start_event, correlation_id = HttpRequestStartEvent.create(method=method, url=url)
        await self._publish_event(start_event)

        try:
            # v3.16.0: 如果配置了中间件，使用中间件系统
            if self._middlewares:
                chain = self._build_middleware_chain()
                response = await chain.execute(request_obj)
            else:
                # 没有中间件，直接执行
                httpx_response = await self.client.request(
                    method=request_obj.method,
                    url=request_obj.url,
                    headers=dict(request_obj.headers) if request_obj.headers else None,
                    params=dict(request_obj.params) if request_obj.params else None,
                    json=request_obj.json,
                    data=request_obj.data,
                )
                response = self._parse_response(httpx_response)

            # v3.17.0: 使用事件工厂方法创建 End 事件，复用 correlation_id
            duration = time.time() - start_time
            end_event = HttpRequestEndEvent.create(
                correlation_id=correlation_id,
                method=method,
                url=url,
                status_code=response.status_code,
                duration=duration,
            )
            await self._publish_event(end_event)
            return response

        except Exception as e:
            # v3.17.0: 使用事件工厂方法创建 Error 事件，复用 correlation_id
            duration = time.time() - start_time
            error_event = HttpRequestErrorEvent.create(
                correlation_id=correlation_id,
                method=method,
                url=url,
                error=e,
                duration=duration,
            )
            await self._publish_event(error_event)
            raise

    # ==================== 辅助方法 ====================

    def _prepare_request_object(self, method: str, url: str, **kwargs) -> Request:
        """
        准备Request对象

        支持 Pydantic 模型自动序列化
        """
        # 处理 Pydantic 模型
        if "json" in kwargs and isinstance(kwargs["json"], BaseModel):
            kwargs["json"] = kwargs["json"].model_dump()

        return Request(
            method=method,
            url=url,
            headers=kwargs.get("headers", {}),
            params=kwargs.get("params", {}),
            json=kwargs.get("json"),
            data=kwargs.get("data"),
        )

    def _parse_response(self, httpx_response: httpx.Response) -> Response:
        """
        解析httpx.Response为框架Response对象
        """
        json_data = None
        try:
            # 只有JSON响应才解析
            content_type = (
                httpx_response.headers.get("content-type")
                or httpx_response.headers.get("Content-Type")
                or ""
            )
            if content_type.startswith("application/json"):
                json_data = httpx_response.json()
        except Exception:
            pass

        return Response(
            status_code=httpx_response.status_code,
            headers=dict(httpx_response.headers),
            body=httpx_response.text,
            json_data=json_data,
        )

    def _load_middlewares_from_config(self, middleware_configs: list[Any]) -> None:
        """从配置自动加载中间件（v3.16.0 新增）

        从 HTTPConfig.middlewares 加载中间件配置并创建实例。

        Args:
            middleware_configs: 中间件配置列表（MiddlewareConfig 对象）
        """
        from df_test_framework.infrastructure.config.middleware_schema import MiddlewareConfig

        logger.debug(f"[AsyncHttpClient] 开始加载中间件: count={len(middleware_configs)}")

        # 按优先级排序
        sorted_configs = sorted(middleware_configs, key=lambda c: c.priority)

        for config in sorted_configs:
            try:
                if not isinstance(config, MiddlewareConfig):
                    logger.warning(f"[AsyncHttpClient] 跳过无效配置: {type(config)}")
                    continue

                # 使用 MiddlewareFactory 创建中间件实例
                middleware = MiddlewareFactory.create(config)
                if not middleware:
                    continue

                # 检查是否需要路径过滤
                has_path_rules = (hasattr(config, "include_paths") and config.include_paths) or (
                    hasattr(config, "exclude_paths") and config.exclude_paths
                )

                if has_path_rules:
                    # 包装为路径过滤中间件
                    middleware = PathFilteredMiddleware(
                        middleware=middleware,
                        include_paths=getattr(config, "include_paths", None),
                        exclude_paths=getattr(config, "exclude_paths", None),
                    )
                    logger.debug(
                        f"[AsyncHttpClient] 中间件已包装路径过滤: "
                        f"include={getattr(config, 'include_paths', [])}, "
                        f"exclude={getattr(config, 'exclude_paths', [])}"
                    )

                # 添加到中间件列表
                self.use(middleware)
                logger.debug(
                    f"[AsyncHttpClient] 已加载中间件: "
                    f"type={config.type}, priority={config.priority}, name={middleware.name}"
                )

            except Exception as e:
                logger.error(f"[AsyncHttpClient] 加载中间件失败: type={config.type}, error={e}")
                raise

        logger.debug(f"[AsyncHttpClient] 中间件加载完成: total={len(self._middlewares)}")

    # ==================== 上下文管理器 ====================

    async def __aenter__(self):
        """
        异步上下文管理器入口

        Example::

            async with AsyncHttpClient("https://api.example.com") as client:
                response = await client.get("/users")
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        异步上下文管理器退出，自动关闭客户端
        """
        await self.close()

    async def close(self):
        """
        关闭客户端，释放连接池资源

        Note:
            使用 async with 时会自动调用，无需手动调用

        Example::

            client = AsyncHttpClient("https://api.example.com")
            try:
                response = await client.get("/users")
            finally:
                await client.close()
        """
        await self.client.aclose()
        logger.debug("异步HTTP客户端已关闭")


__all__ = ["AsyncHttpClient"]
