# 中间件架构 设计方案

> **状态**: 📝 设计草案（待讨论）
> **作者**: Claude Code
> **日期**: 2025-12-03
> **目标版本**: v3.14.0

---

## 📋 目录

1. [背景分析](#1-背景分析)
2. [设计目标](#2-设计目标)
3. [核心设计](#3-核心设计)
4. [详细实现](#4-详细实现)
5. [使用示例](#5-使用示例)
6. [跨能力层统一](#6-跨能力层统一)
7. [配置化支持](#7-配置化支持)
8. [目录结构](#8-目录结构)
9. [与现有设计对比](#9-与现有设计对比)
10. [待讨论问题](#10-待讨论问题)

---

## 1. 背景分析

### 1.1 当前设计 (v3.3)

当前拦截器采用 **分离式执行模型**：

```python
class Interceptor(ABC):
    def before_request(self, request: Request) -> Request | None:
        """请求前处理"""
        ...

    def after_response(self, response: Response) -> Response | None:
        """响应后处理"""
        ...

    def on_error(self, error: Exception, request: Request) -> None:
        """错误处理"""
        ...
```

### 1.2 现有设计的优点

| 优点 | 说明 |
|------|------|
| ✅ 概念简单 | before/after 分离，职责清晰 |
| ✅ 配置完善 | 支持声明式、编程式配置 |
| ✅ 路径匹配 | 支持通配符和正则表达式 |
| ✅ 测试覆盖 | 已有完整测试用例 |

### 1.3 现有设计的问题

#### 问题 1: 状态共享困难

`before_request` 和 `after_response` 是分离的两个方法，无法在同一作用域共享状态：

```python
class TimingInterceptor(BaseInterceptor):
    def before_request(self, request):
        # 如何把 start_time 传递给 after_response？

        # 方案1: 实例变量（多线程不安全）
        self._start_time = time.monotonic()  # ❌ 危险

        # 方案2: context 传递（繁琐）
        return request.with_context("start_time", time.monotonic())  # ✅ 但繁琐

    def after_response(self, response):
        start = response.context.get("start_time")  # 需要从 context 取回
        duration = time.monotonic() - start
        ...
```

#### 问题 2: 异步支持不完善

当前设计以同步为主，异步客户端需要在 async 方法中调用同步拦截器：

```python
class AsyncHttpClient:
    async def request(self, ...):
        # 在 async 方法中调用同步拦截器
        request = self.chain.execute_before_request(request)  # 同步
        response = await self._client.request(...)  # 异步
        response = self.chain.execute_after_response(response)  # 同步
```

#### 问题 3: 协议不统一

存在两套拦截器协议：

| 协议 | 位置 | 状态 |
|------|------|------|
| 通用协议 | `common/protocols/interceptor.py` | ⚠️ 定义了但未使用 |
| HTTP 协议 | `clients/http/core/interceptor.py` | ✅ 实际使用 |

gRPC 拦截器有独立设计，与 HTTP 不统一。

#### 问题 4: 定义方式单一

只支持类定义，不支持函数式或装饰器定义：

```python
# 当前：必须定义类
class MyInterceptor(BaseInterceptor):
    def before_request(self, request):
        return request.with_header("X-Custom", "value")

# 期望：也能用函数
@interceptor
async def my_interceptor(request, call_next):
    return await call_next(request.with_header("X-Custom", "value"))
```

---

## 2. 设计目标

### 2.1 核心原则

| 原则 | 说明 |
|------|------|
| **洋葱模型** | `call_next` 模式，before/after 在同一作用域 |
| **异步原生** | 所有中间件都是 async，同步是特例 |
| **泛型统一** | 一套协议适配 HTTP/gRPC/DB/MQ |
| **多态定义** | 支持类、函数、装饰器三种方式 |
| **配置即代码** | 配置和代码使用同一套类型系统 |

### 2.2 使用场景

```python
# 场景1: 配置文件（80% 用户）
middlewares=[
    SignatureConfig(secret="xxx", algorithm="md5"),
    BearerTokenConfig(login_url="/auth/login"),
]

# 场景2: 链式调用（15% 用户）
client = (
    HttpClient("https://api.example.com")
    .use(SignatureMiddleware(secret="xxx"))
    .use(LoggingMiddleware())
)

# 场景3: 函数式定义（5% 用户）
@middleware(priority=50)
async def custom_middleware(request, call_next):
    response = await call_next(request)
    return response
```

---

## 3. 核心设计

### 3.1 执行模型：洋葱模型

```
Request
    ↓
┌─────────────────────────────────────────────┐
│  Middleware 1 (priority=10)                 │
│    ┌─────────────────────────────────────┐  │
│    │  Middleware 2 (priority=20)         │  │
│    │    ┌─────────────────────────────┐  │  │
│    │    │  Middleware 3 (priority=30) │  │  │
│    │    │    ┌─────────────────────┐  │  │  │
│    │    │    │  Core Handler       │  │  │  │
│    │    │    │  (HTTP Request)     │  │  │  │
│    │    │    └─────────────────────┘  │  │  │
│    │    │  ← after                    │  │  │
│    │    └─────────────────────────────┘  │  │
│    │  ← after                            │  │
│    └─────────────────────────────────────┘  │
│  ← after                                    │
└─────────────────────────────────────────────┘
    ↓
Response
```

**关键点**：每个中间件控制整个请求-响应周期，before 和 after 在同一个函数作用域内。

### 3.2 核心接口

```python
# Python 3.12 类型别名语法
type Next[T, R] = Callable[[T], Awaitable[R]]
type MiddlewareFunc[T, R] = Callable[[T, Next[T, R]], Awaitable[R]]


class Middleware[TRequest, TResponse](ABC):
    """统一中间件协议

    泛型实例化:
    - Middleware[Request, Response]          # HTTP
    - Middleware[GrpcRequest, GrpcResponse]  # gRPC
    - Middleware[Query, QueryResult]         # Database
    - Middleware[Message, PublishResult]     # MQ
    """

    name: str = ""
    priority: int = 100

    @abstractmethod
    async def __call__(
        self,
        request: TRequest,
        call_next: Next[TRequest, TResponse]
    ) -> TResponse:
        """洋葱模型核心方法"""
        ...
```

### 3.3 对比：分离式 vs 洋葱模型

#### 分离式（当前设计）

```python
class TimingInterceptor(BaseInterceptor):
    def before_request(self, request):
        return request.with_context("start", time.monotonic())

    def after_response(self, response):
        start = response.context.get("start")
        print(f"Duration: {time.monotonic() - start:.3f}s")
        return response
```

#### 洋葱模型（新设计）

```python
class TimingMiddleware(BaseMiddleware[Request, Response]):
    async def __call__(self, request, call_next):
        start = time.monotonic()  # 直接在作用域内

        response = await call_next(request)

        print(f"Duration: {time.monotonic() - start:.3f}s")  # 直接访问
        return response
```

---

## 4. 详细实现

### 4.1 核心协议层

```python
# common/middleware/protocol.py
from abc import ABC, abstractmethod
from typing import Callable, Awaitable, Any
from dataclasses import dataclass

type Next[T, R] = Callable[[T], Awaitable[R]]
type MiddlewareFunc[T, R] = Callable[[T, Next[T, R]], Awaitable[R]]


class Middleware[TRequest, TResponse](ABC):
    """统一中间件协议（洋葱模型）"""

    name: str = ""
    priority: int = 100

    @abstractmethod
    async def __call__(
        self,
        request: TRequest,
        call_next: Next[TRequest, TResponse]
    ) -> TResponse:
        ...


class MiddlewareAbort(Exception):
    """中间件主动终止"""

    def __init__(self, message: str = "", response: Any = None):
        super().__init__(message)
        self.response = response
```

### 4.2 中间件链

```python
# common/middleware/chain.py
from typing import Self


class MiddlewareChain[TRequest, TResponse]:
    """中间件执行链"""

    def __init__(self, handler: Next[TRequest, TResponse]):
        self._handler = handler
        self._middlewares: list[Middleware[TRequest, TResponse]] = []

    def use(self, middleware: Middleware[TRequest, TResponse]) -> Self:
        """添加中间件（链式调用）"""
        self._middlewares.append(middleware)
        self._middlewares.sort(key=lambda m: m.priority)
        return self

    async def execute(self, request: TRequest) -> TResponse:
        """执行中间件链"""
        chain = self._handler
        for middleware in reversed(self._middlewares):
            chain = self._wrap(middleware, chain)
        return await chain(request)

    def _wrap(
        self,
        middleware: Middleware[TRequest, TResponse],
        next_handler: Next[TRequest, TResponse]
    ) -> Next[TRequest, TResponse]:
        async def wrapped(request: TRequest) -> TResponse:
            return await middleware(request, next_handler)
        return wrapped
```

### 4.3 便捷基类

```python
# common/middleware/base.py

class BaseMiddleware[TRequest, TResponse](Middleware[TRequest, TResponse]):
    """中间件便捷基类"""

    def __init__(self, name: str | None = None, priority: int = 100):
        self.name = name or self.__class__.__name__
        self.priority = priority

    async def __call__(
        self,
        request: TRequest,
        call_next: Next[TRequest, TResponse]
    ) -> TResponse:
        return await call_next(request)


class SyncMiddleware[TRequest, TResponse](BaseMiddleware[TRequest, TResponse]):
    """同步中间件基类（简化同步逻辑）"""

    def before(self, request: TRequest) -> TRequest:
        """前置处理（同步）"""
        return request

    def after(self, response: TResponse) -> TResponse:
        """后置处理（同步）"""
        return response

    async def __call__(
        self,
        request: TRequest,
        call_next: Next[TRequest, TResponse]
    ) -> TResponse:
        request = self.before(request)
        response = await call_next(request)
        response = self.after(response)
        return response


def middleware[T, R](
    priority: int = 100,
    name: str | None = None
) -> Callable[[MiddlewareFunc[T, R]], Middleware[T, R]]:
    """装饰器：将函数转换为中间件"""

    def decorator(func: MiddlewareFunc[T, R]) -> Middleware[T, R]:
        class FuncMiddleware(Middleware[T, R]):
            def __init__(self):
                self.name = name or func.__name__
                self.priority = priority

            async def __call__(self, request: T, call_next: Next[T, R]) -> R:
                return await func(request, call_next)

        return FuncMiddleware()

    return decorator
```

### 4.4 HTTP 特化层

```python
# clients/http/middleware/types.py
from dataclasses import dataclass, field, replace
from typing import Any


@dataclass(frozen=True, slots=True)
class Request:
    """HTTP 请求对象（不可变）"""
    method: str
    path: str
    headers: dict[str, str] = field(default_factory=dict)
    params: dict[str, Any] = field(default_factory=dict)
    json: dict[str, Any] | None = None
    data: bytes | None = None
    context: dict[str, Any] = field(default_factory=dict)

    def with_header(self, key: str, value: str) -> "Request":
        return replace(self, headers={**self.headers, key: value})

    def with_headers(self, headers: dict[str, str]) -> "Request":
        return replace(self, headers={**self.headers, **headers})

    def with_param(self, key: str, value: Any) -> "Request":
        return replace(self, params={**self.params, key: value})

    def with_context(self, key: str, value: Any) -> "Request":
        return replace(self, context={**self.context, key: value})


@dataclass(frozen=True, slots=True)
class Response:
    """HTTP 响应对象（不可变）"""
    status_code: int
    headers: dict[str, str] = field(default_factory=dict)
    body: bytes = b""
    json_data: dict[str, Any] | None = None
    context: dict[str, Any] = field(default_factory=dict)

    @property
    def text(self) -> str:
        return self.body.decode("utf-8")

    @property
    def is_success(self) -> bool:
        return 200 <= self.status_code < 300

    def with_context(self, key: str, value: Any) -> "Response":
        return replace(self, context={**self.context, key: value})


# 类型别名
type HttpMiddleware = Middleware[Request, Response]
type HttpNext = Next[Request, Response]
```

### 4.5 内置中间件

```python
# clients/http/middleware/builtins.py

class SignatureMiddleware(BaseMiddleware[Request, Response]):
    """签名中间件"""

    def __init__(
        self,
        secret: str,
        algorithm: Literal["md5", "sha256", "hmac-sha256", "hmac-sha512"] = "md5",
        header_name: str = "X-Sign",
        include_params: bool = True,
        include_body: bool = True,
        priority: int = 10,
    ):
        super().__init__(name="SignatureMiddleware", priority=priority)
        self.secret = secret
        self.algorithm = algorithm
        self.header_name = header_name
        self.include_params = include_params
        self.include_body = include_body

    async def __call__(self, request: Request, call_next: HttpNext) -> Response:
        # 收集签名数据
        data = {}
        if self.include_params:
            data.update(request.params)
        if self.include_body and request.json:
            data.update(request.json)

        # 生成签名
        signature = self._sign(data)

        # 添加到请求头并继续
        request = request.with_header(self.header_name, signature)
        return await call_next(request)

    def _sign(self, data: dict) -> str:
        sorted_items = sorted(data.items(), key=lambda x: x[0])
        values = "&".join(str(v) for k, v in sorted_items if v)
        sign_string = f"{values}{self.secret}"

        match self.algorithm:
            case "md5":
                return hashlib.md5(sign_string.encode()).hexdigest()
            case "sha256":
                return hashlib.sha256(sign_string.encode()).hexdigest()
            case "hmac-sha256":
                return hmac.new(self.secret.encode(), values.encode(), "sha256").hexdigest()
            case "hmac-sha512":
                return hmac.new(self.secret.encode(), values.encode(), "sha512").hexdigest()


class BearerTokenMiddleware(BaseMiddleware[Request, Response]):
    """Bearer Token 认证中间件"""

    _token_cache: dict[str, str] = {}

    def __init__(
        self,
        token: str | None = None,
        token_factory: Callable[[], str] | None = None,
        login_url: str | None = None,
        login_body: dict | None = None,
        token_path: str = "data.token",
        header_name: str = "Authorization",
        prefix: str = "Bearer",
        priority: int = 20,
    ):
        super().__init__(name="BearerTokenMiddleware", priority=priority)
        self.token = token
        self.token_factory = token_factory
        self.login_url = login_url
        self.login_body = login_body
        self.token_path = token_path
        self.header_name = header_name
        self.prefix = prefix

    async def __call__(self, request: Request, call_next: HttpNext) -> Response:
        token = await self._get_token(request)
        value = f"{self.prefix} {token}" if self.prefix else token
        request = request.with_header(self.header_name, value)
        return await call_next(request)

    async def _get_token(self, request: Request) -> str:
        if self.token:
            return self.token
        if self.token_factory:
            return self.token_factory()
        if self.login_url:
            # 登录获取（带缓存）
            ...
        raise ValueError("No token source configured")


class LoggingMiddleware(BaseMiddleware[Request, Response]):
    """日志中间件"""

    def __init__(
        self,
        level: str = "INFO",
        log_body: bool = True,
        max_body_length: int = 500,
        priority: int = 100,
    ):
        super().__init__(name="LoggingMiddleware", priority=priority)
        self.level = getattr(logging, level.upper())
        self.log_body = log_body
        self.max_body_length = max_body_length

    async def __call__(self, request: Request, call_next: HttpNext) -> Response:
        start = time.monotonic()
        logger.log(self.level, f"→ {request.method} {request.path}")

        response = await call_next(request)

        duration = time.monotonic() - start
        logger.log(self.level, f"← {response.status_code} ({duration:.3f}s)")

        return response


class RetryMiddleware(BaseMiddleware[Request, Response]):
    """重试中间件"""

    def __init__(
        self,
        max_attempts: int = 3,
        backoff: float = 1.0,
        retry_on_status: list[int] | None = None,
        priority: int = 5,
    ):
        super().__init__(name="RetryMiddleware", priority=priority)
        self.max_attempts = max_attempts
        self.backoff = backoff
        self.retry_on_status = retry_on_status or [500, 502, 503, 504]

    async def __call__(self, request: Request, call_next: HttpNext) -> Response:
        import asyncio

        last_response = None
        for attempt in range(self.max_attempts):
            response = await call_next(request)

            if response.status_code not in self.retry_on_status:
                return response

            last_response = response
            await asyncio.sleep(self.backoff * (2 ** attempt))

        return last_response
```

### 4.6 路径过滤

```python
# clients/http/middleware/path_filter.py

class PathFilteredMiddleware(BaseMiddleware[Request, Response]):
    """路径过滤中间件包装器"""

    def __init__(
        self,
        inner: HttpMiddleware,
        include: list[str] | None = None,
        exclude: list[str] | None = None
    ):
        super().__init__(
            name=f"PathFiltered({inner.name})",
            priority=inner.priority
        )
        self._inner = inner
        self._include = include or ["/**"]
        self._exclude = exclude or []

    async def __call__(self, request: Request, call_next: HttpNext) -> Response:
        if not self._should_apply(request.path):
            return await call_next(request)
        return await self._inner(request, call_next)

    def _should_apply(self, path: str) -> bool:
        import fnmatch

        for pattern in self._exclude:
            if self._match(path, pattern):
                return False

        for pattern in self._include:
            if self._match(path, pattern):
                return True

        return False

    def _match(self, path: str, pattern: str) -> bool:
        # 支持 ** 多级匹配
        pattern = pattern.replace("**", "*")
        return fnmatch.fnmatch(path, pattern)
```

### 4.7 HTTP 客户端

```python
# clients/http/client.py
import httpx
from typing import Any, Self


class HttpClient:
    """HTTP 客户端"""

    def __init__(
        self,
        base_url: str = "",
        timeout: float = 30.0,
        middlewares: list[HttpMiddleware] | None = None,
    ):
        self.base_url = base_url
        self._client = httpx.AsyncClient(base_url=base_url, timeout=timeout)
        self._chain = MiddlewareChain(self._send)

        if middlewares:
            for m in middlewares:
                self._chain.use(m)

    def use(self, middleware: HttpMiddleware) -> Self:
        """添加中间件"""
        self._chain.use(middleware)
        return self

    def use_for_paths(
        self,
        middleware: HttpMiddleware,
        include: list[str] | None = None,
        exclude: list[str] | None = None
    ) -> Self:
        """添加带路径过滤的中间件"""
        if include or exclude:
            middleware = PathFilteredMiddleware(middleware, include, exclude)
        self._chain.use(middleware)
        return self

    async def _send(self, request: Request) -> Response:
        """核心发送方法"""
        httpx_response = await self._client.request(
            method=request.method,
            url=request.path,
            headers=request.headers,
            params=request.params,
            json=request.json,
            content=request.data,
        )

        json_data = None
        if "application/json" in httpx_response.headers.get("content-type", ""):
            try:
                json_data = httpx_response.json()
            except Exception:
                pass

        return Response(
            status_code=httpx_response.status_code,
            headers=dict(httpx_response.headers),
            body=httpx_response.content,
            json_data=json_data,
            context=request.context,
        )

    async def request(self, method: str, path: str, **kwargs: Any) -> Response:
        """发送请求"""
        request = Request(
            method=method,
            path=path,
            headers=kwargs.get("headers", {}),
            params=kwargs.get("params", {}),
            json=kwargs.get("json"),
            data=kwargs.get("data"),
            context={"base_url": self.base_url},
        )
        return await self._chain.execute(request)

    async def get(self, path: str, **kwargs) -> Response:
        return await self.request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs) -> Response:
        return await self.request("POST", path, **kwargs)

    async def put(self, path: str, **kwargs) -> Response:
        return await self.request("PUT", path, **kwargs)

    async def delete(self, path: str, **kwargs) -> Response:
        return await self.request("DELETE", path, **kwargs)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *args) -> None:
        await self._client.aclose()
```

---

## 5. 使用示例

### 5.1 链式配置

```python
async def main():
    client = (
        HttpClient("https://api.example.com")
        .use(RetryMiddleware(max_attempts=3))
        .use(SignatureMiddleware(secret="xxx", algorithm="md5"))
        .use(BearerTokenMiddleware(token="my_token"))
        .use(LoggingMiddleware(level="DEBUG"))
    )

    async with client:
        response = await client.post("/orders", json={"amount": 100})
        print(response.json_data)
```

### 5.2 函数式中间件

```python
from common.middleware import middleware

@middleware(priority=50)
async def timing_middleware(request: Request, call_next) -> Response:
    """计时中间件"""
    start = time.monotonic()
    response = await call_next(request)
    print(f"Request took {time.monotonic() - start:.3f}s")
    return response

client = HttpClient("https://api.example.com").use(timing_middleware)
```

### 5.3 同步中间件

```python
class AddHeaderMiddleware(SyncMiddleware[Request, Response]):
    """添加固定请求头（同步）"""

    def __init__(self, headers: dict[str, str]):
        super().__init__(name="AddHeaderMiddleware")
        self.headers = headers

    def before(self, request: Request) -> Request:
        return request.with_headers(self.headers)

client = HttpClient("https://api.example.com").use(
    AddHeaderMiddleware({"X-App-Version": "1.0.0"})
)
```

### 5.4 路径过滤

```python
client = (
    HttpClient("https://api.example.com")
    .use_for_paths(
        SignatureMiddleware(secret="xxx"),
        include=["/api/**"],
        exclude=["/api/health", "/api/login"]
    )
    .use_for_paths(
        BearerTokenMiddleware(token="xxx"),
        include=["/admin/**"]
    )
)
```

### 5.5 自定义中间件

```python
class RateLimitMiddleware(BaseMiddleware[Request, Response]):
    """限流中间件"""

    def __init__(self, requests_per_second: float = 10.0, priority: int = 1):
        super().__init__(name="RateLimitMiddleware", priority=priority)
        self.interval = 1.0 / requests_per_second
        self._last_request = 0.0

    async def __call__(self, request: Request, call_next: HttpNext) -> Response:
        import asyncio

        now = time.monotonic()
        wait_time = self._last_request + self.interval - now

        if wait_time > 0:
            await asyncio.sleep(wait_time)

        self._last_request = time.monotonic()
        return await call_next(request)
```

---

## 6. 跨能力层统一

### 6.1 gRPC 中间件

```python
# clients/grpc/middleware.py
from common.middleware import Middleware, BaseMiddleware

@dataclass(frozen=True)
class GrpcRequest:
    method: str
    metadata: dict[str, str]
    message: Any

@dataclass(frozen=True)
class GrpcResponse:
    status: int
    metadata: dict[str, str]
    message: Any

type GrpcMiddleware = Middleware[GrpcRequest, GrpcResponse]


class GrpcLoggingMiddleware(BaseMiddleware[GrpcRequest, GrpcResponse]):
    async def __call__(self, request, call_next):
        logger.info(f"→ gRPC {request.method}")
        response = await call_next(request)
        logger.info(f"← gRPC status={response.status}")
        return response
```

### 6.2 数据库中间件

```python
# databases/middleware.py
from common.middleware import Middleware, BaseMiddleware

@dataclass
class Query:
    sql: str
    params: dict[str, Any]

@dataclass
class QueryResult:
    rows: list[dict]
    row_count: int

type DbMiddleware = Middleware[Query, QueryResult]


class SlowQueryMiddleware(BaseMiddleware[Query, QueryResult]):
    def __init__(self, threshold: float = 1.0):
        super().__init__(name="SlowQueryMiddleware")
        self.threshold = threshold

    async def __call__(self, query, call_next):
        start = time.monotonic()
        result = await call_next(query)
        duration = time.monotonic() - start

        if duration > self.threshold:
            logger.warning(f"Slow query ({duration:.3f}s): {query.sql}")

        return result
```

### 6.3 消息队列中间件

```python
# messengers/middleware.py
from common.middleware import Middleware, BaseMiddleware

@dataclass
class Message:
    topic: str
    body: bytes
    headers: dict[str, str]

@dataclass
class PublishResult:
    message_id: str
    success: bool

type MqMiddleware = Middleware[Message, PublishResult]


class TracingMiddleware(BaseMiddleware[Message, PublishResult]):
    async def __call__(self, message, call_next):
        with tracer.start_span("mq.publish") as span:
            span.set_attribute("topic", message.topic)
            return await call_next(message)
```

---

## 7. 配置化支持

### 7.1 配置类

```python
# infrastructure/config/middleware.py
from pydantic import BaseModel, Field
from typing import Literal, Any


class MiddlewareConfig(BaseModel):
    """中间件配置基类"""
    type: str
    enabled: bool = True
    priority: int = 100
    include_paths: list[str] = Field(default=["/**"])
    exclude_paths: list[str] = Field(default=[])


class SignatureConfig(MiddlewareConfig):
    type: Literal["signature"] = "signature"
    secret: str
    algorithm: Literal["md5", "sha256", "hmac-sha256", "hmac-sha512"] = "md5"
    header_name: str = "X-Sign"


class BearerTokenConfig(MiddlewareConfig):
    type: Literal["bearer_token"] = "bearer_token"
    token: str | None = None
    login_url: str | None = None
    login_body: dict[str, Any] | None = None
    token_path: str = "data.token"


class LoggingConfig(MiddlewareConfig):
    type: Literal["logging"] = "logging"
    level: str = "INFO"
    log_body: bool = True


class RetryConfig(MiddlewareConfig):
    type: Literal["retry"] = "retry"
    max_attempts: int = 3
    backoff: float = 1.0


class CustomConfig(MiddlewareConfig):
    type: Literal["custom"] = "custom"
    class_path: str
    params: dict[str, Any] = Field(default={})
```

### 7.2 工厂

```python
class MiddlewareFactory:
    """中间件工厂"""

    _registry: dict[str, type] = {}

    @classmethod
    def register(cls, type_name: str):
        """装饰器：注册中间件类型"""
        def decorator(middleware_cls: type):
            cls._registry[type_name] = middleware_cls
            return middleware_cls
        return decorator

    @classmethod
    def create(cls, config: MiddlewareConfig) -> HttpMiddleware | None:
        """从配置创建中间件"""
        if not config.enabled:
            return None

        match config.type:
            case "signature":
                return SignatureMiddleware(...)
            case "bearer_token":
                return BearerTokenMiddleware(...)
            case "logging":
                return LoggingMiddleware(...)
            case "retry":
                return RetryMiddleware(...)
            case "custom":
                return cls._create_custom(config)
            case _:
                if config.type in cls._registry:
                    return cls._registry[config.type](**config.model_dump())
                raise ValueError(f"Unknown middleware type: {config.type}")
```

---

## 8. 目录结构

```
src/df_test_framework/
├── common/
│   └── middleware/                  # 通用中间件协议
│       ├── __init__.py              # 导出核心类型
│       ├── protocol.py              # Middleware 协议定义
│       ├── chain.py                 # MiddlewareChain 实现
│       └── base.py                  # BaseMiddleware, @middleware
│
├── clients/
│   ├── http/
│   │   ├── middleware/              # HTTP 中间件
│   │   │   ├── __init__.py          # Request, Response, 类型别名
│   │   │   ├── types.py             # Request, Response 定义
│   │   │   ├── builtins.py          # 内置中间件
│   │   │   ├── path_filter.py       # 路径过滤
│   │   │   └── factory.py           # MiddlewareFactory
│   │   └── client.py                # HttpClient
│   │
│   └── grpc/
│       └── middleware/              # gRPC 中间件
│           ├── __init__.py
│           └── types.py
│
├── databases/
│   └── middleware/                  # 数据库中间件
│       ├── __init__.py
│       └── slow_query.py
│
├── messengers/
│   └── middleware/                  # MQ 中间件
│       ├── __init__.py
│       └── tracing.py
│
└── infrastructure/
    └── config/
        └── middleware.py            # 配置类定义
```

---

## 9. 与现有设计对比

| 维度 | v3.3 (现有) | v3.14.0 (新设计) | 改进 |
|------|------------|--------------|------|
| **执行模型** | `before`/`after` 分离 | 洋葱模型 `call_next` | ✅ 状态共享更自然 |
| **状态共享** | 需要 context 传递 | 函数作用域共享 | ✅ 更简洁 |
| **异步支持** | 同步为主 | async 原生 | ✅ 更现代 |
| **定义方式** | 仅类 | 类 + 函数 + 装饰器 | ✅ 更灵活 |
| **类型系统** | `Generic[T]` | Python 3.12 `type` | ✅ 更简洁 |
| **跨能力层** | HTTP/gRPC 独立 | 统一协议 | ✅ 更一致 |
| **重试** | HttpClient 内置 | 中间件实现 | ✅ 更灵活 |
| **配置化** | 完善 | 保持完善 | = 保持 |
| **路径过滤** | 完善 | 保持完善 | = 保持 |

---

## 10. 待讨论问题

### 10.1 命名：Interceptor vs Middleware

| 选项 | 优点 | 缺点 |
|------|------|------|
| **Middleware** | 业界通用（Starlette/FastAPI/Express） | 与现有代码不兼容 |
| **Interceptor** | 与现有代码一致 | 不够现代 |

**建议**: 使用 `Middleware`，更符合现代 Web 框架惯例。

### 10.2 是否保留 `before`/`after` 便捷方法

`SyncMiddleware` 提供了 `before`/`after` 便捷方法：

```python
class AddHeaderMiddleware(SyncMiddleware):
    def before(self, request):
        return request.with_header("X-Custom", "value")
```

**问题**: 是否需要保留这种简化方式？

**建议**: 保留 `SyncMiddleware`，方便简单场景。

### 10.3 同步客户端支持

新设计以 async 为主，是否需要同步客户端？

**方案 A**: 只提供 async 客户端，用户自行 `asyncio.run()`

**方案 B**: 提供 `SyncHttpClient` 包装层

**建议**: 方案 A，简化设计。测试框架中 pytest-asyncio 已经很成熟。

### 10.4 与现有 Allure 集成

现有 `InterceptorChain` 支持 Allure 集成，新设计如何保持？

**方案**: 在 `MiddlewareChain.execute()` 中添加可观测性钩子。

### 10.5 实施计划

如果决定采用新设计，建议的实施步骤：

1. **Phase 1**: 实现 `common/middleware/` 核心协议
2. **Phase 2**: 实现 HTTP 客户端和内置中间件
3. **Phase 3**: 迁移配置系统
4. **Phase 4**: 更新测试和文档
5. **Phase 5**: 扩展到 gRPC/DB/MQ

---

## 📚 参考资料

- [Starlette Middleware](https://www.starlette.io/middleware/)
- [Koa.js Middleware](https://koajs.com/)
- [gRPC Interceptors](https://grpc.io/docs/guides/interceptors/)
- [Python 3.12 Type Parameter Syntax](https://docs.python.org/3.12/whatsnew/3.12.html#pep-695-type-parameter-syntax)

---

> **下一步**: 请审阅此设计方案，如有问题或建议，可以进一步讨论。
