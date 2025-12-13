"""HTTP Mock支持

基于 Middleware 的 HTTP 请求 Mock 功能，用于测试隔离

核心特性:
- 完全 Mock HTTP 请求，无需真实服务
- 支持请求匹配（URL、Method、Headers、Body）
- 支持响应定制（状态码、Headers、JSON/Text）
- 支持多次请求和序列响应
- 与框架的中间件系统完全兼容

v3.16.0: 迁移到 Middleware 系统，移除 Interceptor 依赖

使用场景:
- 单元测试：隔离外部API依赖
- 集成测试：Mock部分上游服务
- 性能测试：避免真实请求开销
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from re import Pattern
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from df_test_framework.capabilities.clients.http.rest.httpx.client import HttpClient

try:
    from pytest_httpx import HTTPXMock

    HTTPX_MOCK_AVAILABLE = True
except ImportError:
    HTTPXMock = None
    HTTPX_MOCK_AVAILABLE = False

from df_test_framework.capabilities.clients.http.core import Request, Response
from df_test_framework.core.middleware import BaseMiddleware


class MockResponseException(Exception):
    """携带 Mock 响应的特殊异常

    MockMiddleware 抛出此异常来终止真实请求并返回 Mock 响应

    Attributes:
        response: Mock 响应对象
        request: 原始请求对象
    """

    def __init__(self, response: Response, request: Request):
        self.response = response
        self.request = request
        super().__init__(f"Mock response for {request.method} {request.url}")


# 保持向后兼容
MockResponse = MockResponseException


@dataclass
class MockRule:
    """Mock规则定义

    定义一个HTTP请求的Mock规则，包括匹配条件和响应内容

    Attributes:
        url: URL匹配（支持字符串、正则、通配符）
        method: HTTP方法匹配（GET/POST等，None表示匹配所有）
        status_code: Mock响应状态码
        json_data: Mock响应JSON数据
        text_data: Mock响应Text数据
        headers: Mock响应Headers
        match_headers: 请求Headers匹配条件
        match_json: 请求JSON Body匹配条件
        times: 此规则可匹配的次数（None表示无限次）

    Example:
        >>> # 简单Mock
        >>> rule = MockRule(
        ...     url="/api/users",
        ...     method="GET",
        ...     status_code=200,
        ...     json_data={"users": []}
        ... )

        >>> # 带请求匹配
        >>> rule = MockRule(
        ...     url=re.compile(r"/api/users/\\d+"),
        ...     method="POST",
        ...     match_json={"name": "Alice"},
        ...     status_code=201,
        ...     json_data={"id": 1, "name": "Alice"}
        ... )
    """

    url: str | Pattern
    method: str | None = None
    status_code: int = 200
    json_data: dict[str, Any] | None = None
    text_data: str | None = None
    headers: dict[str, str] = field(default_factory=dict)
    match_headers: dict[str, str] | None = None
    match_json: dict[str, Any] | None = None
    times: int | None = None  # None表示无限次


class MockMiddleware(BaseMiddleware[Request, Response]):
    """HTTP Mock 中间件

    在请求发送前拦截并返回 Mock 响应，实现完全的请求隔离

    v3.16.0: 从 MockInterceptor 迁移到 MockMiddleware

    工作原理:
    1. 在中间件链中检查是否有匹配的 Mock 规则
    2. 如果匹配，直接返回 Mock 响应，不调用 call_next
    3. 如果无匹配，继续调用下一个中间件

    特点:
    - 与中间件链完全兼容
    - 支持多规则和优先级
    - 支持请求验证

    Example:
        >>> # 方式1: 直接使用中间件
        >>> mock_middleware = MockMiddleware()
        >>> mock_middleware.add_rule(MockRule(
        ...     url="/api/users",
        ...     method="GET",
        ...     json_data={"users": [{"id": 1, "name": "Alice"}]}
        ... ))
        >>> http_client.use(mock_middleware)

        >>> # 方式2: 使用 http_mock fixture（推荐）
        >>> def test_get_users(http_mock):
        ...     http_mock.add_rule(
        ...         url="/api/users",
        ...         method="GET",
        ...         json_data={"users": []}
        ...     )
        ...     # 测试代码...
    """

    def __init__(self, priority: int = 1):
        """初始化 Mock 中间件

        Args:
            priority: 优先级（默认1，确保在其他中间件之前执行）
        """
        super().__init__(name="MockMiddleware", priority=priority)
        self.rules: list[MockRule] = []
        self.matched_requests: list[Request] = []  # 用于验证

    def add_rule(
        self,
        url: str | Pattern,
        method: str | None = None,
        status_code: int = 200,
        json_data: dict[str, Any] | None = None,
        text_data: str | None = None,
        headers: dict[str, str] | None = None,
        match_headers: dict[str, str] | None = None,
        match_json: dict[str, Any] | None = None,
        times: int | None = None,
    ) -> MockMiddleware:
        """添加 Mock 规则（链式调用）

        Args:
            url: URL匹配模式（字符串或正则）
            method: HTTP方法（None表示匹配所有）
            status_code: Mock响应状态码
            json_data: Mock响应JSON
            text_data: Mock响应Text
            headers: Mock响应Headers
            match_headers: 请求Headers匹配
            match_json: 请求JSON匹配
            times: 匹配次数限制

        Returns:
            self，支持链式调用

        Example:
            >>> mock.add_rule("/api/users", "GET", json_data={"users": []})
            ...     .add_rule("/api/login", "POST", status_code=201)
        """
        rule = MockRule(
            url=url,
            method=method,
            status_code=status_code,
            json_data=json_data,
            text_data=text_data,
            headers=headers or {},
            match_headers=match_headers,
            match_json=match_json,
            times=times,
        )
        self.rules.append(rule)
        return self

    async def __call__(self, request: Request, call_next) -> Response:
        """中间件调用

        检查是否有匹配的 Mock 规则，如果有则返回 Mock 响应，
        否则继续调用下一个中间件。

        Args:
            request: 请求对象
            call_next: 调用下一个中间件的函数

        Returns:
            响应对象（Mock 响应或真实响应）
        """
        for i, rule in enumerate(self.rules):
            if self._match_rule(rule, request):
                # 记录匹配的请求（用于验证）
                self.matched_requests.append(request)

                # 创建 Mock 响应
                mock_response = self._create_mock_response(rule, request)

                # 检查 times 限制
                if rule.times is not None:
                    rule.times -= 1
                    if rule.times <= 0:
                        # 移除已达上限的规则
                        self.rules.pop(i)

                # 直接返回 Mock 响应，不调用 call_next
                return mock_response

        # 无匹配规则，继续正常请求
        return await call_next(request)

    def _match_rule(self, rule: MockRule, request: Request) -> bool:
        """检查请求是否匹配规则

        Args:
            rule: Mock规则
            request: 请求对象

        Returns:
            是否匹配
        """
        # 1. 检查URL
        request_url = request.url if hasattr(request, "url") else request.path
        if isinstance(rule.url, Pattern):
            if not rule.url.match(request_url):
                return False
        else:
            # 字符串匹配（支持通配符*）
            url_pattern = rule.url.replace("*", ".*")
            if not re.match(f"^{url_pattern}$", request_url):
                return False

        # 2. 检查Method
        if rule.method and request.method.upper() != rule.method.upper():
            return False

        # 3. 检查Headers
        if rule.match_headers:
            for key, value in rule.match_headers.items():
                if request.headers.get(key) != value:
                    return False

        # 4. 检查JSON Body
        if rule.match_json:
            if request.json != rule.match_json:
                return False

        return True

    def _create_mock_response(self, rule: MockRule, request: Request) -> Response:
        """根据规则创建 Mock 响应

        Args:
            rule: Mock规则
            request: 请求对象

        Returns:
            Mock响应对象
        """
        # 构造响应Body
        body = None
        json_data = None

        if rule.json_data is not None:
            import json

            json_data = rule.json_data
            body = json.dumps(json_data, ensure_ascii=False)
        elif rule.text_data is not None:
            body = rule.text_data
        else:
            body = ""

        # 构造响应Headers
        headers = dict(rule.headers)
        if json_data is not None and "content-type" not in {k.lower() for k in headers}:
            headers["Content-Type"] = "application/json; charset=utf-8"

        return Response(
            status_code=rule.status_code,
            headers=headers,
            body=body,
            json_data=json_data,
        )

    def clear_rules(self) -> None:
        """清空所有 Mock 规则"""
        self.rules.clear()
        self.matched_requests.clear()

    def assert_called(self, url: str, method: str | None = None, times: int | None = None) -> None:
        """断言某个请求被调用

        Args:
            url: 请求URL
            method: 请求方法（None表示不限）
            times: 期望调用次数（None表示至少1次）

        Raises:
            AssertionError: 断言失败

        Example:
            >>> mock.assert_called("/api/users", "GET", times=1)
        """
        matched = [
            r
            for r in self.matched_requests
            if (r.url if hasattr(r, "url") else r.path) == url
            and (method is None or r.method.upper() == method.upper())
        ]

        if times is None:
            assert len(matched) >= 1, (
                f"Expected request to {method or 'ANY'} {url} but never called"
            )
        else:
            assert len(matched) == times, (
                f"Expected request to {method or 'ANY'} {url} called {times} times, "
                f"but called {len(matched)} times"
            )


# 保持向后兼容别名
MockInterceptor = MockMiddleware


class HttpMocker:
    """HTTP Mock工具类

    提供便捷的HTTP Mock API，用于测试

    Features:
    - 简化的Mock规则添加
    - 自动管理 MockMiddleware 生命周期
    - 支持请求验证

    Example:
        >>> @pytest.fixture
        ... def http_mock(http_client):
        ...     mocker = HttpMocker(http_client)
        ...     yield mocker
        ...     mocker.reset()

        >>> def test_api(http_mock, http_client):
        ...     http_mock.get("/api/users", json={"users": []})
        ...     response = http_client.get("/api/users")
        ...     assert response.json() == {"users": []}
    """

    def __init__(self, http_client: HttpClient):
        """初始化HTTP Mocker

        Args:
            http_client: HttpClient实例
        """
        self.http_client = http_client
        self.middleware = MockMiddleware(priority=1)

        # 将 MockMiddleware 添加到中间件链（最高优先级）
        if hasattr(http_client, "use"):
            http_client.use(self.middleware)
        elif hasattr(http_client, "middleware_chain"):
            http_client.middleware_chain.use(self.middleware)

    def add_rule(self, *args, **kwargs) -> HttpMocker:
        """添加Mock规则（代理到MockMiddleware）"""
        self.middleware.add_rule(*args, **kwargs)
        return self

    def get(
        self,
        url: str,
        status_code: int = 200,
        json: dict | None = None,
        text: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpMocker:
        """快捷方法：Mock GET请求"""
        return self.add_rule(
            url=url,
            method="GET",
            status_code=status_code,
            json_data=json,
            text_data=text,
            headers=headers,
        )

    def post(
        self,
        url: str,
        status_code: int = 201,
        json: dict | None = None,
        text: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpMocker:
        """快捷方法：Mock POST请求"""
        return self.add_rule(
            url=url,
            method="POST",
            status_code=status_code,
            json_data=json,
            text_data=text,
            headers=headers,
        )

    def put(
        self,
        url: str,
        status_code: int = 200,
        json: dict | None = None,
        text: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpMocker:
        """快捷方法：Mock PUT请求"""
        return self.add_rule(
            url=url,
            method="PUT",
            status_code=status_code,
            json_data=json,
            text_data=text,
            headers=headers,
        )

    def delete(
        self,
        url: str,
        status_code: int = 204,
        json: dict | None = None,
        text: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpMocker:
        """快捷方法：Mock DELETE请求"""
        return self.add_rule(
            url=url,
            method="DELETE",
            status_code=status_code,
            json_data=json,
            text_data=text,
            headers=headers,
        )

    def assert_called(self, url: str, method: str | None = None, times: int | None = None) -> None:
        """断言请求被调用（代理到MockMiddleware）"""
        self.middleware.assert_called(url, method, times)

    def reset(self) -> None:
        """重置所有Mock规则"""
        self.middleware.clear_rules()


__all__ = [
    "MockRule",
    "MockMiddleware",
    "MockInterceptor",  # 向后兼容别名
    "MockResponse",
    "MockResponseException",
    "HttpMocker",
    "HTTPX_MOCK_AVAILABLE",
]
