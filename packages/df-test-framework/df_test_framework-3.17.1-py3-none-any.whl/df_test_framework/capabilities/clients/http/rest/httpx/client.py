"""HTTP客户端封装

v3.0.0 新增:
- 集成HTTPDebugger调试支持

v3.5.0 重构:
- 使用InterceptorChain替代List[Callable]
- 支持完整的before/after/on_error拦截器生命周期

v3.14.0 重构:
- 集成 MiddlewareChain（洋葱模型）
- 支持 middlewares=[] 构造参数
- 支持 .use(middleware) 链式调用
- 集成 EventBus 发布 HTTP 事件

v3.16.0 重构:
- 完全移除 InterceptorChain，统一使用 MiddlewareChain
- 支持从 HTTPConfig.middlewares 自动加载
- 移除 config.interceptors 兼容代码

v3.17.0 重构:
- 使用新事件系统（带 correlation_id 的事件关联）
- 使用 publish_sync() 同步发布事件
- 使用事件工厂方法创建事件
"""

from __future__ import annotations

import asyncio
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


def sanitize_url(url: str) -> str:
    """
    脱敏URL中的敏感参数

    将以下敏感参数值替换为****:
    - token, access_token, refresh_token
    - key, api_key, secret, secret_key
    - password
    - authorization

    Args:
        url: 原始URL

    Returns:
        脱敏后的URL

    Examples:
        >>> sanitize_url("/api/users?token=abc123&id=1")
        '/api/users?token=****&id=1'

        >>> sanitize_url("/api/pay?amount=100&key=xyz789")
        '/api/pay?amount=100&key=****'
    """
    # 敏感参数列表
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
        # 匹配 ?param=value 或 &param=value，替换为 ?param=**** 或 &param=****
        # 使用(?<![a-zA-Z_]) 和 (?![a-zA-Z_]) 确保参数名准确匹配
        pattern = rf"([?&]{param}=)[^&]*"
        url = re.sub(pattern, r"\1****", url, flags=re.IGNORECASE)

    return url


class HttpClient:
    """
    统一的HTTP客户端封装

    功能:
    - 🆕 v3.16.0: 纯中间件系统（完全移除 InterceptorChain）
    - 🆕 v3.16.0: 支持从 HTTPConfig.middlewares 自动加载
    - 统一中间件系统（洋葱模型）
    - 集成 EventBus 发布 HTTP 事件
    - 自动添加认证token
    - 请求/响应日志记录
    - 自动重试机制
    - 上下文管理器支持

    v3.16.0 用法:
        # 方式1: 手动传入中间件
        client = HttpClient(
            "https://api.example.com",
            middlewares=[
                RetryMiddleware(max_attempts=3),
                SignatureMiddleware(secret="xxx"),
                BearerTokenMiddleware(token="yyy"),
            ]
        )

        # 方式2: 从配置自动加载
        client = HttpClient(
            "https://api.example.com",
            config=http_config,  # 自动从 config.middlewares 加载
        )

        # 方式3: 链式添加
        client = HttpClient("https://api.example.com")
        client.use(RetryMiddleware()).use(LoggingMiddleware())
    """

    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        headers: dict[str, str] | None = None,
        verify_ssl: bool = True,
        max_retries: int = 3,
        max_connections: int = 50,
        max_keepalive_connections: int = 20,
        config: HTTPConfig | None = None,
        middlewares: list[Middleware[Request, Response]] | None = None,
        event_bus: EventBus | None = None,
    ):
        """
        初始化HTTP客户端

        Args:
            base_url: API基础URL
            timeout: 请求超时时间(秒) (默认30)
            headers: 默认请求头
            verify_ssl: 是否验证SSL证书 (默认True)
            max_retries: 最大重试次数 (默认3)
            max_connections: 最大连接数 (默认50)
            max_keepalive_connections: Keep-Alive连接数 (默认20)
            config: 🆕 v3.16.0 HTTPConfig配置对象（用于自动加载中间件）
            middlewares: 🆕 v3.16.0 中间件列表（如果为空，从 config.middlewares 加载）
            event_bus: 🆕 v3.14.0 事件总线（可选，用于发布 HTTP 事件）
        """
        self.base_url = base_url
        self.timeout = timeout
        self.default_headers = headers or {}
        self.verify_ssl = verify_ssl
        self.max_retries = max_retries

        # v3.17.0 修复: 延迟获取 EventBus（支持测试隔离）
        # 如果显式传入 EventBus，则使用传入的实例
        # 否则每次发布事件时动态获取（支持测试隔离，每个测试使用独立的 EventBus）
        self._event_bus: EventBus | None = event_bus

        # v3.16.0: 纯中间件系统
        self._middleware_chain: MiddlewareChain[Request, Response] | None = None
        self._middlewares: list[Middleware[Request, Response]] = []

        # 配置传输层 (注意: httpx.HTTPTransport没有retries参数)
        transport = httpx.HTTPTransport(
            verify=verify_ssl,
        )

        # 配置连接限制
        limits = httpx.Limits(
            max_connections=max_connections,
            max_keepalive_connections=max_keepalive_connections,
        )

        # 创建httpx客户端
        self.client = httpx.Client(
            base_url=base_url,
            timeout=timeout,
            headers=self.default_headers,
            transport=transport,
            limits=limits,
            follow_redirects=True,
        )

        logger.debug(
            f"HTTP客户端已初始化: base_url={base_url}, "
            f"timeout={timeout}s, max_retries={max_retries}"
        )

        # v3.16.0: 加载中间件
        if middlewares:
            # 方式1: 手动传入中间件列表
            for mw in middlewares:
                self.use(mw)
        elif config and config.middlewares:
            # 方式2: 从 HTTPConfig.middlewares 自动加载
            self._load_middlewares_from_config(config.middlewares)

    def use(self, middleware: Middleware[Request, Response]) -> HttpClient:
        """添加中间件（链式调用）

        v3.14.0 新增
        v3.17.0 增强: 自动为 BearerTokenMiddleware (LOGIN 模式) 注入 http_client

        Args:
            middleware: 要添加的中间件

        Returns:
            self，支持链式调用

        Example:
            client.use(RetryMiddleware()).use(LoggingMiddleware())
        """
        # v3.17.0: 自动注入 http_client 给需要的中间件（如 BearerTokenMiddleware LOGIN 模式）
        if hasattr(middleware, "set_http_client") and hasattr(middleware, "_login_token_provider"):
            if middleware._login_token_provider is not None:
                middleware.set_http_client(self)
                logger.debug(f"已为中间件 {middleware.name} 注入 http_client (LOGIN 模式)")

        self._middlewares.append(middleware)
        # 重置链，下次执行时重新构建
        self._middleware_chain = None
        logger.debug(f"添加中间件: {middleware.name} (priority={middleware.priority})")
        return self

    def set_auth_token(self, token: str, token_type: str = "Bearer") -> None:
        """
        设置认证token

        Args:
            token: 认证令牌
            token_type: 令牌类型 (Bearer, Basic等)
        """
        self.client.headers["Authorization"] = f"{token_type} {token}"
        logger.debug(f"已设置认证token: {token_type} {token[:10]}...")

    # ==================== v3.14.0: 中间件执行 ====================

    def _build_middleware_chain(self) -> MiddlewareChain[Request, Response]:
        """构建中间件链（懒加载）

        Returns:
            MiddlewareChain 实例
        """
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
        """异步发送 HTTP 请求（中间件链的最终处理器）

        Args:
            request: Request 对象

        Returns:
            Response 对象
        """
        # 转换 Request 为 httpx 参数
        params: dict[str, Any] = {}
        if request.headers:
            params["headers"] = dict(request.headers)
        if request.params:
            params["params"] = dict(request.params)
        if request.json is not None:
            params["json"] = request.json
        if request.data is not None:
            params["data"] = request.data

        # 使用线程池执行同步请求（保持与现有同步客户端兼容）
        loop = asyncio.get_event_loop()
        httpx_response = await loop.run_in_executor(
            None,
            lambda: self.client.request(request.method, request.url, **params),
        )

        return self._create_response_object(httpx_response)

    def _publish_event(self, event: Any) -> None:
        """发布事件到 EventBus（同步模式）

        v3.17.0: 统一使用 publish_sync，确保事件处理完成后再继续。
        v3.17.0: 动态获取 EventBus（支持测试隔离，每个测试使用独立的 EventBus）。

        Args:
            event: 要发布的事件
        """
        # 动态获取 EventBus（优先使用测试上下文的 EventBus）
        event_bus = self._event_bus
        if event_bus is None:
            from df_test_framework.infrastructure.events import get_event_bus

            event_bus = get_event_bus()

        if event_bus:
            event_bus.publish_sync(event)

    def request_with_middleware(
        self,
        method: str,
        url: str,
        **kwargs,
    ) -> Response:
        """使用新中间件系统发送请求

        v3.14.0 新增
        v3.17.0 重构: 使用新事件系统（带 correlation_id 的事件关联）

        Args:
            method: HTTP 方法
            url: 请求路径
            **kwargs: 请求参数

        Returns:
            Response 对象（框架对象，非 httpx.Response）
        """
        # 准备请求
        request_obj = self._prepare_request_object(method, url, **kwargs)

        # 在事件循环中执行
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # v3.17.0: 使用事件工厂方法创建 Start 事件，获取 correlation_id
        start_time = time.time()
        start_event, correlation_id = HttpRequestStartEvent.create(
            method=method,
            url=url,
            headers=dict(request_obj.headers) if request_obj.headers else None,
            body=str(request_obj.json or request_obj.data)
            if (request_obj.json or request_obj.data)
            else None,
        )
        self._publish_event(start_event)

        try:
            # 构建并执行中间件链
            chain = self._build_middleware_chain()

            response = loop.run_until_complete(chain.execute(request_obj))

            # v3.17.0: 使用事件工厂方法创建 End 事件，复用 correlation_id
            duration = time.time() - start_time
            end_event = HttpRequestEndEvent.create(
                correlation_id=correlation_id,
                method=method,
                url=url,
                status_code=response.status_code,
                duration=duration,
                headers=dict(response.headers) if response.headers else None,
                body=response.body,  # v3.17.0: 包含响应体
            )
            self._publish_event(end_event)

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
            self._publish_event(error_event)
            raise

    # ==================== ✅ 重构: 辅助方法（降低request()复杂度） ====================

    def _prepare_request_object(
        self,
        method: str,
        url: str,
        **kwargs,
    ) -> Request:
        """准备Request对象

        ✅ v3.6新增: 支持 Pydantic 模型自动序列化

        Args:
            method: 请求方法
            url: 请求URL
            **kwargs: 请求参数
                - json: 可以是 Pydantic 模型或字典
                  如果是 Pydantic 模型，会自动使用 model_dump_json() 序列化
                  自动处理 Decimal/datetime/UUID 等类型

        Returns:
            Request对象
        """
        # ✅ v3.6: 自动处理 Pydantic 模型序列化
        json_param = kwargs.get("json")
        if json_param is not None:
            # 检查是否为 Pydantic 模型
            from pydantic import BaseModel

            if isinstance(json_param, BaseModel):
                # 使用 Pydantic 的 model_dump_json() 序列化
                # 优点：
                # 1. 自动处理 Decimal → 字符串
                # 2. 自动处理 datetime → ISO 8601
                # 3. 自动处理 UUID → 字符串
                # 4. 性能优化（Rust 核心）
                json_str = json_param.model_dump_json()

                # 将序列化后的 JSON 字符串设置为 data
                # 同时设置 Content-Type 头
                kwargs["data"] = json_str
                headers = kwargs.get("headers", {})
                if "Content-Type" not in headers and "content-type" not in headers:
                    headers["Content-Type"] = "application/json"
                    kwargs["headers"] = headers

                # 清空 json 参数，避免 httpx 重复处理
                kwargs["json"] = None

        return Request(
            method=method,
            url=url,
            headers=kwargs.get("headers", {}),
            params=kwargs.get("params"),
            json=kwargs.get("json"),
            data=kwargs.get("data"),
            context={"base_url": self.base_url},
        )

    def _load_middlewares_from_config(self, middleware_configs: list[Any]) -> None:
        """从配置自动加载中间件（v3.16.0 新增）

        从 HTTPConfig.middlewares 加载中间件配置并创建实例。

        Args:
            middleware_configs: 中间件配置列表（MiddlewareConfig 对象）
        """
        from df_test_framework.infrastructure.config.middleware_schema import MiddlewareConfig

        logger.debug(f"[HttpClient] 开始加载中间件: count={len(middleware_configs)}")

        # 按优先级排序
        sorted_configs = sorted(middleware_configs, key=lambda c: c.priority)

        for config in sorted_configs:
            try:
                if not isinstance(config, MiddlewareConfig):
                    logger.warning(f"[HttpClient] 跳过无效配置: {type(config)}")
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
                        f"[HttpClient] 中间件已包装路径过滤: "
                        f"include={getattr(config, 'include_paths', [])}, "
                        f"exclude={getattr(config, 'exclude_paths', [])}"
                    )

                # 添加到中间件列表
                self.use(middleware)
                logger.debug(
                    f"[HttpClient] 已加载中间件: "
                    f"type={config.type}, priority={config.priority}, name={middleware.name}"
                )

            except Exception as e:
                logger.error(f"[HttpClient] 加载中间件失败: type={config.type}, error={e}")
                raise

        logger.debug(f"[HttpClient] 中间件加载完成: total={len(self._middlewares)}")

    def _create_response_object(self, httpx_response: httpx.Response) -> Response:
        """创建Response对象

        Args:
            httpx_response: httpx响应

        Returns:
            Response对象
        """
        json_data = None
        try:
            if httpx_response.headers.get("content-type", "").startswith("application/json"):
                json_data = httpx_response.json()
        except Exception:
            pass

        return Response(
            status_code=httpx_response.status_code,
            headers=dict(httpx_response.headers),
            body=httpx_response.text,
            json_data=json_data,
        )

    # ==================== 主请求方法 ====================

    def request(
        self,
        method: str,
        url: str,
        **kwargs,
    ) -> httpx.Response:
        """
        发送HTTP请求 (支持自动重试)

        ✅ v3.16.0: 纯中间件系统（移除 InterceptorChain）
        ✅ v3.14.0: 优先使用中间件系统
        ✅ v3.5重构: 拆分为多个辅助方法,降低复杂度

        重试策略:
        - 自动重试: 超时异常(TimeoutException)和5xx服务器错误
        - 不重试: 4xx客户端错误
        - 重试次数: max_retries (初始化时指定)
        - 退避策略: 指数退避 (1s, 2s, 4s, 8s...)

        Args:
            method: 请求方法 (GET, POST, PUT, DELETE等)
            url: 请求路径
            **kwargs: 其他请求参数 (params, json, data, headers等)

        Returns:
            httpx.Response对象

        Raises:
            httpx.TimeoutException: 请求超时 (重试max_retries次后仍失败)
            httpx.HTTPStatusError: HTTP状态错误
            httpx.RequestError: 请求错误
        """
        # v3.16.0: 如果配置了中间件，使用中间件系统
        if self._middlewares:
            response = self.request_with_middleware(method, url, **kwargs)
            # 将 Response 转换为 httpx.Response 以保持向后兼容
            request_obj = self._prepare_request_object(method, url, **kwargs)
            return self._convert_to_httpx_response(response, request_obj)

        # 没有中间件，使用基础请求逻辑
        return self._send_without_middleware(method, url, **kwargs)

    def _convert_to_httpx_response(self, response: Response, request: Request) -> httpx.Response:
        """将框架Response对象转换为httpx.Response对象

        用于Mock响应的转换

        Args:
            response: 框架的Response对象
            request: 原始请求对象

        Returns:
            httpx.Response对象
        """
        # 构造httpx.Request对象
        httpx_request = httpx.Request(
            method=request.method,
            url=f"{self.base_url}{request.url}",
            headers=request.headers,
        )

        # 移除压缩相关的响应头，因为 response.body 已经是解压后的文本
        # httpx.Response 会根据 Content-Encoding 头自动解压，但我们的内容已经解压了
        clean_headers = dict(response.headers)
        clean_headers.pop("Content-Encoding", None)
        clean_headers.pop("content-encoding", None)

        # 构造httpx.Response对象
        return httpx.Response(
            status_code=response.status_code,
            headers=clean_headers,
            content=response.body.encode("utf-8") if response.body else b"",
            request=httpx_request,
        )

    def _send_without_middleware(self, method: str, url: str, **kwargs) -> httpx.Response:
        """不使用中间件的基础请求发送

        v3.16.0 简化版
        v3.17.0 重构: 使用新事件系统（带 correlation_id 的事件关联）

        用于没有配置中间件时的快速请求路径。

        Args:
            method: 请求方法
            url: 请求URL
            **kwargs: 请求参数

        Returns:
            httpx.Response对象
        """
        start_time = time.time()

        # v3.17.0: 使用事件工厂方法创建 Start 事件，获取 correlation_id
        start_event, correlation_id = HttpRequestStartEvent.create(method=method, url=url)
        self._publish_event(start_event)

        try:
            # 准备请求对象（处理 Pydantic 模型序列化）
            request_obj = self._prepare_request_object(method, url, **kwargs)

            # 将 Request 对象转换回 kwargs
            kwargs = {}
            if request_obj.headers:
                kwargs["headers"] = dict(request_obj.headers)
            if request_obj.params:
                kwargs["params"] = dict(request_obj.params)
            if request_obj.json:
                kwargs["json"] = request_obj.json
            if request_obj.data:
                kwargs["data"] = request_obj.data

            # 直接发送 HTTP 请求（包含重试逻辑）
            last_exception = None

            for attempt in range(self.max_retries + 1):
                try:
                    httpx_response = self.client.request(method, url, **kwargs)

                    logger.info(f"Response Status: {httpx_response.status_code}")
                    logger.debug(f"Response Body: {httpx_response.text[:500]}")

                    # 检查是否需要重试 (5xx错误)
                    if httpx_response.status_code >= 500 and attempt < self.max_retries:
                        logger.warning(
                            f"服务器错误 {httpx_response.status_code}, 重试 {attempt + 1}/{self.max_retries}"
                        )
                        time.sleep(2**attempt)
                        continue

                    # v3.17.0: 使用事件工厂方法创建 End 事件，复用 correlation_id
                    duration = time.time() - start_time
                    end_event = HttpRequestEndEvent.create(
                        correlation_id=correlation_id,
                        method=method,
                        url=url,
                        status_code=httpx_response.status_code,
                        duration=duration,
                        headers=dict(httpx_response.headers),
                        body=httpx_response.text,  # v3.17.0: 包含响应体
                    )
                    self._publish_event(end_event)

                    return httpx_response

                except httpx.TimeoutException as e:
                    last_exception = e
                    if attempt < self.max_retries:
                        time.sleep(2**attempt)
                        continue
                    else:
                        # v3.17.0: 使用事件工厂方法创建 Error 事件
                        error_event = HttpRequestErrorEvent.create(
                            correlation_id=correlation_id,
                            method=method,
                            url=url,
                            error=e,
                            duration=(time.time() - start_time),
                        )
                        self._publish_event(error_event)
                        raise

                except httpx.RequestError as e:
                    last_exception = e
                    if attempt < self.max_retries:
                        time.sleep(2**attempt)
                        continue
                    else:
                        # v3.17.0: 使用事件工厂方法创建 Error 事件
                        error_event = HttpRequestErrorEvent.create(
                            correlation_id=correlation_id,
                            method=method,
                            url=url,
                            error=e,
                            duration=(time.time() - start_time),
                        )
                        self._publish_event(error_event)
                        raise

            # 所有重试失败
            if last_exception:
                raise last_exception

            # 不应该到达这里
            raise RuntimeError("Unexpected state in _send_without_middleware")

        except Exception as e:
            # 捕获其他异常并发布事件
            if not isinstance(e, (httpx.TimeoutException, httpx.RequestError)):
                # v3.17.0: 使用事件工厂方法创建 Error 事件
                error_event = HttpRequestErrorEvent.create(
                    correlation_id=correlation_id,
                    method=method,
                    url=url,
                    error=e,
                    duration=(time.time() - start_time),
                )
                self._publish_event(error_event)
            raise

    def get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        **kwargs,
    ) -> httpx.Response:
        """GET请求"""
        return self.request("GET", url, params=params, **kwargs)

    def post(
        self,
        url: str,
        json: dict[str, Any] | BaseModel | None = None,
        data: dict[str, Any] | None = None,
        **kwargs,
    ) -> httpx.Response:
        """POST请求

        ✅ v3.6新增: 支持直接传入 Pydantic 模型

        Args:
            url: 请求路径
            json: 请求体，支持：
                - Python 字典
                - Pydantic 模型（推荐）- 自动序列化，支持 Decimal/datetime/UUID 等
            data: 表单数据
            **kwargs: 其他请求参数

        Returns:
            httpx.Response对象

        Example:
            >>> # 方式 1: 使用字典（传统方式）
            >>> response = client.post("/api/users", json={"name": "Alice"})
            >>>
            >>> # 方式 2: 使用 Pydantic 模型（推荐）
            >>> from pydantic import BaseModel
            >>> from decimal import Decimal
            >>>
            >>> class PaymentRequest(BaseModel):
            ...     amount: Decimal  # 自动序列化为字符串
            ...
            >>> request = PaymentRequest(amount=Decimal("123.45"))
            >>> response = client.post("/api/payment", json=request)
            >>> # 发送: {"amount":"123.45"}
        """
        return self.request("POST", url, json=json, data=data, **kwargs)

    def put(
        self,
        url: str,
        json: dict[str, Any] | BaseModel | None = None,
        **kwargs,
    ) -> httpx.Response:
        """PUT请求

        ✅ v3.6新增: 支持直接传入 Pydantic 模型

        Args:
            url: 请求路径
            json: 请求体，支持字典或 Pydantic 模型
            **kwargs: 其他请求参数

        Returns:
            httpx.Response对象
        """
        return self.request("PUT", url, json=json, **kwargs)

    def patch(
        self,
        url: str,
        json: dict[str, Any] | BaseModel | None = None,
        **kwargs,
    ) -> httpx.Response:
        """PATCH请求

        ✅ v3.6新增: 支持直接传入 Pydantic 模型

        Args:
            url: 请求路径
            json: 请求体，支持字典或 Pydantic 模型
            **kwargs: 其他请求参数

        Returns:
            httpx.Response对象
        """
        return self.request("PATCH", url, json=json, **kwargs)

    def delete(
        self,
        url: str,
        **kwargs,
    ) -> httpx.Response:
        """DELETE请求"""
        return self.request("DELETE", url, **kwargs)

    def close(self) -> None:
        """关闭客户端连接"""
        self.client.close()
        logger.debug("HTTP客户端已关闭")

    def __enter__(self):
        """上下文管理器入口"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()


__all__ = ["HttpClient"]
