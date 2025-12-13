# 拦截器理想架构设计（从零开始）

> **设计目标**: 抛开现有实现，从第一性原理出发，设计一个完美的拦截器架构
> **设计时间**: 2025-11-06
> **设计原则**: 简单、直观、强大

---

## 🤔 第一性原理思考

### 问题本质

**拦截器是什么？**
- 在请求/响应的生命周期中，插入自定义逻辑的钩子
- 类似AOP（面向切面编程）的概念

**拦截器要解决什么问题？**
1. **横切关注点分离** - 签名、认证、日志、重试等逻辑不应该耦合在业务代码中
2. **可复用性** - 同样的签名逻辑可以复用到多个API
3. **可配置性** - 不同环境、不同API可能需要不同的拦截器
4. **可组合性** - 多个拦截器可以组合使用

**谁需要拦截器？**
1. **测试框架开发者** - 内置通用拦截器（签名、Token等）
2. **测试项目开发者** - 自定义业务拦截器
3. **测试用例编写者** - 简单配置，无需关心实现细节

---

## 🎯 设计目标

### 目标1: 简单直观

**对于80%的用户（测试用例编写者）**:
```python
# 配置文件就能搞定，不需要写代码
# settings.yaml
http:
  interceptors:
    - type: signature
      algorithm: md5
      secret: xxx
    - type: admin_auth
      login_url: /admin/login
      username: admin
```

**对于15%的用户（测试项目开发者）**:
```python
# 可以灵活自定义
@pytest.fixture
def my_custom_api(http_client):
    api = MyAPI(http_client)
    api.use(my_custom_interceptor)  # 链式调用，直观
    return api
```

**对于5%的用户（框架开发者）**:
```python
# 可以深度定制
class MyCustomInterceptor(BaseInterceptor):
    def before_request(self, request):
        # 自定义逻辑
        pass
```

---

### 目标2: 单一职责

**每个组件只做一件事**:
- `HttpClient` - 发送HTTP请求
- `Interceptor` - 处理请求/响应
- `InterceptorChain` - 管理拦截器执行顺序
- `InterceptorRegistry` - 注册和查找拦截器
- `InterceptorFactory` - 从配置创建拦截器

---

### 目标3: 灵活但不复杂

**支持三种配置方式，但内部实现统一**:
1. 声明式配置（settings.yaml/settings.py）
2. 编程式配置（fixture中显式创建）
3. 装饰器配置（类似Flask的@app.route）

---

## 🏗️ 核心架构设计

### 1. 概念模型

```
Request
    ↓
┌─────────────────────────────────────┐
│   InterceptorChain                  │
│   ┌─────────────────────────────┐   │
│   │ Interceptor 1 (priority=10) │   │
│   │   - before_request()        │   │
│   └─────────────────────────────┘   │
│             ↓                       │
│   ┌─────────────────────────────┐   │
│   │ Interceptor 2 (priority=20) │   │
│   │   - before_request()        │   │
│   └─────────────────────────────┘   │
│             ↓                       │
│   ┌─────────────────────────────┐   │
│   │ Interceptor 3 (priority=30) │   │
│   │   - before_request()        │   │
│   └─────────────────────────────┘   │
└─────────────────────────────────────┘
    ↓
HttpClient.send(request)
    ↓
Response
    ↓
┌─────────────────────────────────────┐
│   InterceptorChain                  │
│   ┌─────────────────────────────┐   │
│   │ Interceptor 3               │   │
│   │   - after_response()        │   │
│   └─────────────────────────────┘   │
│             ↓                       │
│   ┌─────────────────────────────┐   │
│   │ Interceptor 2               │   │
│   │   - after_response()        │   │
│   └─────────────────────────────┘   │
│             ↓                       │
│   ┌─────────────────────────────┐   │
│   │ Interceptor 1               │   │
│   │   - after_response()        │   │
│   └─────────────────────────────┘   │
└─────────────────────────────────────┘
    ↓
Return Response
```

---

### 2. 核心抽象

#### 2.1 Request 对象

```python
@dataclass
class Request:
    """HTTP请求对象（不可变）

    设计理念：
    - 不可变对象，拦截器通过返回新对象来修改
    - 包含所有请求信息
    - 类型安全
    """
    method: str
    url: str
    headers: Dict[str, str] = field(default_factory=dict)
    params: Dict[str, Any] = field(default_factory=dict)
    json: Optional[Dict[str, Any]] = None
    data: Optional[Any] = None

    # 上下文信息（用于拦截器间传递数据）
    context: Dict[str, Any] = field(default_factory=dict)

    def with_header(self, key: str, value: str) -> "Request":
        """返回添加了新header的新Request对象"""
        new_headers = {**self.headers, key: value}
        return replace(self, headers=new_headers)

    def with_context(self, key: str, value: Any) -> "Request":
        """在context中设置值"""
        new_context = {**self.context, key: value}
        return replace(self, context=new_context)
```

**为什么不可变？**
- 避免拦截器互相影响
- 更容易调试（每个拦截器的输入输出都清晰）
- 支持并发（未来）

---

#### 2.2 Response 对象

```python
@dataclass
class Response:
    """HTTP响应对象（不可变）"""
    status_code: int
    headers: Dict[str, str]
    body: str
    json_data: Optional[Dict[str, Any]] = None

    # 携带request的context
    context: Dict[str, Any] = field(default_factory=dict)

    def with_context(self, key: str, value: Any) -> "Response":
        """在context中设置值"""
        new_context = {**self.context, key: value}
        return replace(self, context=new_context)
```

---

#### 2.3 Interceptor 接口

```python
from abc import ABC, abstractmethod
from typing import Optional

class Interceptor(ABC):
    """拦截器接口

    设计理念：
    - 简单的生命周期钩子
    - 返回None表示不修改（性能优化）
    - 返回新对象表示修改
    """

    # 拦截器元数据
    name: str = ""
    priority: int = 100  # 数字越小越先执行

    def before_request(self, request: Request) -> Optional[Request]:
        """请求前处理

        Args:
            request: 原始请求对象

        Returns:
            - None: 不修改请求
            - Request: 修改后的新请求对象
        """
        return None

    def after_response(self, response: Response) -> Optional[Response]:
        """响应后处理

        Args:
            response: 原始响应对象

        Returns:
            - None: 不修改响应
            - Response: 修改后的新响应对象
        """
        return None

    def on_error(self, error: Exception, request: Request) -> None:
        """错误处理（可选）

        Args:
            error: 异常对象
            request: 请求对象
        """
        pass


# 便捷基类（提供默认实现）
class BaseInterceptor(Interceptor):
    """拦截器基类

    提供默认的name和priority
    子类只需要覆盖需要的钩子
    """

    def __init__(self, name: Optional[str] = None, priority: int = 100):
        self.name = name or self.__class__.__name__
        self.priority = priority
```

**为什么这样设计？**
- `before_request` + `after_response` 覆盖95%的场景
- 返回`Optional[Request/Response]`比修改原对象更安全
- `on_error` 钩子用于日志、告警等

---

#### 2.4 InterceptorChain（拦截器链）

```python
class InterceptorChain:
    """拦截器执行链

    设计理念：
    - 责任链模式
    - 自动排序（按priority）
    - 短路机制（interceptor可以终止请求）
    """

    def __init__(self, interceptors: List[Interceptor]):
        # 按priority排序
        self.interceptors = sorted(interceptors, key=lambda i: i.priority)

    def execute_before_request(self, request: Request) -> Request:
        """执行所有before_request钩子"""
        current_request = request

        for interceptor in self.interceptors:
            try:
                modified_request = interceptor.before_request(current_request)
                if modified_request is not None:
                    current_request = modified_request

            except InterceptorAbort as e:
                # 拦截器可以主动终止请求
                logger.warning(f"请求被拦截器终止: {interceptor.name}, 原因: {e}")
                raise

            except Exception as e:
                logger.error(
                    f"拦截器执行失败: {interceptor.name}, 错误: {e}",
                    exc_info=True
                )
                # 默认继续执行下一个拦截器（容错）
                # 如果需要严格模式，可以配置抛出异常

        return current_request

    def execute_after_response(self, response: Response) -> Response:
        """执行所有after_response钩子（逆序）"""
        current_response = response

        # 响应拦截器逆序执行（像洋葱模型）
        for interceptor in reversed(self.interceptors):
            try:
                modified_response = interceptor.after_response(current_response)
                if modified_response is not None:
                    current_response = modified_response
            except Exception as e:
                logger.error(
                    f"响应拦截器执行失败: {interceptor.name}, 错误: {e}"
                )

        return current_response


class InterceptorAbort(Exception):
    """拦截器主动终止请求的异常"""
    pass
```

**为什么逆序执行响应拦截器？**
```
Request:
  Interceptor A (加密)
    → Interceptor B (签名)
      → HTTP请求
      → HTTP响应
    ← Interceptor B (验签)
  ← Interceptor A (解密)
Response
```
这是洋葱模型，符合直觉。

---

#### 2.5 HttpClient（简化版）

```python
class HttpClient:
    """HTTP客户端

    设计理念：
    - 职责单一：发送HTTP请求
    - 拦截器通过InterceptorChain管理
    - 支持多种方式添加拦截器
    """

    def __init__(
        self,
        base_url: str,
        interceptors: Optional[List[Interceptor]] = None,
    ):
        self.base_url = base_url
        self.client = httpx.Client(base_url=base_url)

        # 拦截器链
        self.chain = InterceptorChain(interceptors or [])

    def use(self, interceptor: Interceptor) -> "HttpClient":
        """添加拦截器（链式调用）

        Example:
            >>> client = HttpClient("http://api.example.com")
            >>> client.use(SignatureInterceptor(secret="xxx"))
            >>> client.use(LogInterceptor())
        """
        self.chain.interceptors.append(interceptor)
        self.chain.interceptors.sort(key=lambda i: i.priority)
        return self

    def request(
        self,
        method: str,
        url: str,
        **kwargs
    ) -> Response:
        """发送HTTP请求

        执行流程:
        1. 创建Request对象
        2. 执行before_request拦截器链
        3. 发送HTTP请求
        4. 执行after_response拦截器链
        5. 返回Response对象
        """
        # 1. 创建Request对象
        request = Request(
            method=method,
            url=url,
            headers=kwargs.get("headers", {}),
            params=kwargs.get("params", {}),
            json=kwargs.get("json"),
            data=kwargs.get("data"),
        )

        # 2. 执行before_request拦截器链
        request = self.chain.execute_before_request(request)

        # 3. 发送HTTP请求
        http_response = self.client.request(
            method=request.method,
            url=request.url,
            headers=request.headers,
            params=request.params,
            json=request.json,
            data=request.data,
        )

        # 4. 创建Response对象
        response = Response(
            status_code=http_response.status_code,
            headers=dict(http_response.headers),
            body=http_response.text,
            json_data=http_response.json() if http_response.headers.get("content-type", "").startswith("application/json") else None,
            context=request.context,  # 继承request的context
        )

        # 5. 执行after_response拦截器链
        response = self.chain.execute_after_response(response)

        return response
```

---

### 3. 配置系统设计

#### 3.1 声明式配置（推荐）

```yaml
# settings.yaml
http:
  base_url: http://api.example.com
  interceptors:
    # 签名拦截器
    - type: signature
      priority: 10
      enabled: true
      algorithm: md5
      secret: ${BUSINESS_APP_SECRET}  # 支持环境变量
      header_name: X-Sign

    # Admin认证拦截器
    - type: admin_auth
      priority: 20
      enabled: true
      login_url: /admin/auth/login
      username: ${ADMIN_USERNAME}
      password: ${ADMIN_PASSWORD}
      token_cache: true  # 启用Token缓存

    # 自定义拦截器
    - type: custom
      priority: 30
      class: my_project.interceptors.MyCustomInterceptor
      params:
        foo: bar
```

**对应的Python配置**:
```python
# settings.py
from pydantic import Field
from df_test_framework import FrameworkSettings, HTTPConfig

class MySettings(FrameworkSettings):
    http: HTTPConfig = Field(
        default_factory=lambda: HTTPConfig(
            base_url=os.getenv("API_BASE_URL", "http://api.example.com"),
            interceptors=[
                SignatureInterceptorConfig(
                    type="signature",
                    priority=10,
                    algorithm="md5",
                    secret=os.getenv("BUSINESS_APP_SECRET"),
                ),
                AdminAuthInterceptorConfig(
                    type="admin_auth",
                    priority=20,
                    login_url="/admin/auth/login",
                    username=os.getenv("ADMIN_USERNAME"),
                    password=os.getenv("ADMIN_PASSWORD"),
                ),
            ],
        )
    )
```

---

#### 3.2 编程式配置

```python
# fixtures/http_client.py
from df_test_framework import HttpClient
from df_test_framework.interceptors import SignatureInterceptor, LogInterceptor

@pytest.fixture(scope="session")
def http_client(settings):
    client = HttpClient(base_url=settings.http.base_url)

    # 链式调用添加拦截器
    client.use(SignatureInterceptor(
        algorithm="md5",
        secret=settings.business.app_secret,
        priority=10
    ))

    client.use(LogInterceptor(
        level="DEBUG",
        priority=100
    ))

    return client
```

---

#### 3.3 装饰器配置（API级别）

```python
from df_test_framework import BaseAPI
from df_test_framework.interceptors import retry, rate_limit

class MyAPI(BaseAPI):

    @retry(max_attempts=3, backoff=2)  # 装饰器配置重试
    @rate_limit(requests_per_second=10)  # 装饰器配置限流
    def get_users(self, page: int = 1) -> List[User]:
        """获取用户列表"""
        response = self.get("/users", params={"page": page})
        return [User(**u) for u in response.json_data["users"]]
```

---

### 4. 内置拦截器设计

#### 4.1 SignatureInterceptor（签名拦截器）

```python
class SignatureInterceptor(BaseInterceptor):
    """签名拦截器

    自动为请求添加签名Header
    """

    def __init__(
        self,
        algorithm: str = "md5",  # md5, sha256, hmac-sha256
        secret: str = "",
        header_name: str = "X-Sign",
        include_query: bool = True,
        include_body: bool = True,
        priority: int = 10,
    ):
        super().__init__(name="SignatureInterceptor", priority=priority)
        self.algorithm = algorithm
        self.secret = secret
        self.header_name = header_name
        self.include_query = include_query
        self.include_body = include_body

        # 策略模式：根据算法选择签名策略
        self.strategy = self._create_strategy(algorithm)

    def _create_strategy(self, algorithm: str):
        strategies = {
            "md5": MD5SignatureStrategy(),
            "sha256": SHA256SignatureStrategy(),
            "hmac-sha256": HMACSignatureStrategy(algorithm="sha256"),
        }
        return strategies.get(algorithm)

    def before_request(self, request: Request) -> Request:
        """添加签名"""
        # 1. 提取参数
        params = {}
        if self.include_query:
            params.update(request.params)
        if self.include_body and request.json:
            params.update(request.json)

        # 2. 生成签名
        signature = self.strategy.generate(params, self.secret)

        # 3. 添加到header
        return request.with_header(self.header_name, signature)
```

---

#### 4.2 AdminAuthInterceptor（Admin认证）

```python
class AdminAuthInterceptor(BaseInterceptor):
    """Admin认证拦截器

    自动登录获取Token并添加到请求头
    """

    def __init__(
        self,
        login_url: str,
        username: str,
        password: str,
        token_field: str = "data.token",
        header_name: str = "Authorization",
        token_prefix: str = "Bearer",
        cache_enabled: bool = True,
        priority: int = 20,
    ):
        super().__init__(name="AdminAuthInterceptor", priority=priority)
        self.login_url = login_url
        self.username = username
        self.password = password
        self.token_field = token_field
        self.header_name = header_name
        self.token_prefix = token_prefix

        # Token缓存
        self._token_cache = None if cache_enabled else None

    def before_request(self, request: Request) -> Request:
        """添加Token"""
        # 1. 获取Token（带缓存）
        token = self._get_token(request.context.get("base_url"))

        # 2. 添加到header
        token_value = f"{self.token_prefix} {token}" if self.token_prefix else token
        return request.with_header(self.header_name, token_value)

    def _get_token(self, base_url: str) -> str:
        """获取Token（带缓存）"""
        if self._token_cache:
            return self._token_cache

        # 调用登录接口
        import httpx
        response = httpx.post(
            f"{base_url}{self.login_url}",
            json={"username": self.username, "password": self.password}
        )

        # 提取Token
        data = response.json()
        for field in self.token_field.split("."):
            data = data[field]

        self._token_cache = data
        return data
```

---

#### 4.3 LogInterceptor（日志拦截器）

```python
class LogInterceptor(BaseInterceptor):
    """日志拦截器

    记录请求和响应
    """

    def __init__(
        self,
        level: str = "INFO",
        log_request_body: bool = True,
        log_response_body: bool = True,
        max_body_length: int = 500,
        priority: int = 100,
    ):
        super().__init__(name="LogInterceptor", priority=priority)
        self.level = level
        self.log_request_body = log_request_body
        self.log_response_body = log_response_body
        self.max_body_length = max_body_length

    def before_request(self, request: Request) -> None:
        """记录请求"""
        logger.log(
            self.level,
            f"→ {request.method} {request.url}",
            extra={
                "headers": request.headers,
                "params": request.params,
                "body": str(request.json)[:self.max_body_length] if self.log_request_body else None,
            }
        )
        return None  # 不修改请求

    def after_response(self, response: Response) -> None:
        """记录响应"""
        logger.log(
            self.level,
            f"← {response.status_code}",
            extra={
                "headers": response.headers,
                "body": response.body[:self.max_body_length] if self.log_response_body else None,
            }
        )
        return None  # 不修改响应
```

---

#### 4.4 RetryInterceptor（重试拦截器）

```python
class RetryInterceptor(BaseInterceptor):
    """重试拦截器

    支持自定义重试策略
    """

    def __init__(
        self,
        max_attempts: int = 3,
        backoff_factor: float = 2.0,
        retry_on_status: List[int] = None,  # [500, 502, 503, 504]
        retry_on_exception: List[Type[Exception]] = None,
        priority: int = 5,  # 优先级很高，最先执行
    ):
        super().__init__(name="RetryInterceptor", priority=priority)
        self.max_attempts = max_attempts
        self.backoff_factor = backoff_factor
        self.retry_on_status = retry_on_status or [500, 502, 503, 504]
        self.retry_on_exception = retry_on_exception or [httpx.TimeoutException]

    # 重试逻辑需要在HttpClient层面实现
    # 这里只是示例，实际需要特殊处理
```

---

### 5. 拦截器工厂

```python
class InterceptorFactory:
    """拦截器工厂

    从配置创建拦截器实例
    """

    # 内置拦截器映射
    _builtin_interceptors = {
        "signature": SignatureInterceptor,
        "admin_auth": AdminAuthInterceptor,
        "log": LogInterceptor,
        "retry": RetryInterceptor,
    }

    @classmethod
    def create(cls, config: InterceptorConfig) -> Interceptor:
        """从配置创建拦截器

        Args:
            config: 拦截器配置对象

        Returns:
            拦截器实例
        """
        # 1. 内置拦截器
        if config.type in cls._builtin_interceptors:
            interceptor_class = cls._builtin_interceptors[config.type]
            return interceptor_class(**config.dict(exclude={"type", "enabled"}))

        # 2. 自定义拦截器（通过class路径）
        if config.type == "custom" and hasattr(config, "class_path"):
            interceptor_class = cls._import_class(config.class_path)
            return interceptor_class(**config.params)

        raise ValueError(f"未知的拦截器类型: {config.type}")

    @classmethod
    def register(cls, name: str, interceptor_class: Type[Interceptor]):
        """注册自定义拦截器

        Example:
            >>> InterceptorFactory.register("my_interceptor", MyInterceptor)
        """
        cls._builtin_interceptors[name] = interceptor_class
```

---

## 🎨 使用示例

### 示例1: 最简单的场景（零代码）

```yaml
# settings.yaml
http:
  base_url: http://api.example.com
  interceptors:
    - type: signature
      algorithm: md5
      secret: my_secret
```

```python
# test_api.py
def test_create_card(http_client):
    # 自动应用签名拦截器
    response = http_client.post("/cards", json={"amount": 100})
    assert response.status_code == 200
```

---

### 示例2: 灵活的手工配置

```python
# fixtures/http_client.py
@pytest.fixture(scope="session")
def http_client(settings):
    client = HttpClient(base_url=settings.http.base_url)

    # 链式添加拦截器
    client.use(SignatureInterceptor(
        algorithm="md5",
        secret=settings.business.app_secret,
        priority=10
    )).use(LogInterceptor(
        level="DEBUG",
        priority=100
    ))

    return client
```

---

### 示例3: 不同API不同拦截器

```python
# fixtures/http_clients.py
@pytest.fixture(scope="session")
def master_http_client(settings):
    """Master系统专用客户端 - MD5签名"""
    client = HttpClient(base_url=settings.http.base_url)
    client.use(SignatureInterceptor(algorithm="md5", secret=settings.business.app_secret))
    return client

@pytest.fixture(scope="session")
def h5_http_client(settings):
    """H5系统专用客户端 - SHA256签名"""
    client = HttpClient(base_url=settings.http.base_url)
    client.use(SignatureInterceptor(algorithm="sha256", secret=settings.business.app_secret))
    return client

@pytest.fixture(scope="session")
def admin_http_client(settings):
    """Admin系统专用客户端 - Token认证"""
    client = HttpClient(base_url=settings.http.base_url)
    client.use(AdminAuthInterceptor(
        login_url="/admin/auth/login",
        username=settings.business.admin_username,
        password=settings.business.admin_password,
    ))
    return client

# 使用
@pytest.fixture
def master_card_api(master_http_client):
    return MasterCardAPI(master_http_client)

@pytest.fixture
def h5_card_api(h5_http_client):
    return H5CardAPI(h5_http_client)

@pytest.fixture
def admin_order_api(admin_http_client):
    return AdminOrderAPI(admin_http_client)
```

---

### 示例4: 自定义拦截器

```python
# my_project/interceptors.py
from df_test_framework import BaseInterceptor, Request

class TimestampInterceptor(BaseInterceptor):
    """添加时间戳"""

    def before_request(self, request: Request) -> Request:
        import time
        timestamp = str(int(time.time() * 1000))
        return request.with_header("X-Timestamp", timestamp)


# 使用
@pytest.fixture
def http_client_with_timestamp(settings):
    client = HttpClient(base_url=settings.http.base_url)
    client.use(TimestampInterceptor(priority=5))
    return client
```

---

## ✅ 设计优势

### 1. 概念简单清晰 ✅

```
Request → Interceptor Chain → HTTP → Response
```
一条线，没有分支，容易理解。

---

### 2. 职责明确 ✅

| 组件 | 职责 |
|------|------|
| `HttpClient` | 发送HTTP请求 |
| `Interceptor` | 处理请求/响应（单一职责） |
| `InterceptorChain` | 管理执行顺序 |
| `InterceptorFactory` | 创建拦截器实例 |
| `Request/Response` | 不可变数据对象 |

---

### 3. 易于扩展 ✅

**添加新拦截器**:
```python
class MyInterceptor(BaseInterceptor):
    def before_request(self, request: Request) -> Request:
        # 自定义逻辑
        return request.with_header("X-Custom", "value")

# 注册
InterceptorFactory.register("my_interceptor", MyInterceptor)
```

**配置使用**:
```yaml
interceptors:
  - type: my_interceptor
```

---

### 4. 不可变对象保证安全 ✅

```python
# 拦截器A
def before_request(self, request: Request) -> Request:
    return request.with_header("X-A", "a")

# 拦截器B
def before_request(self, request: Request) -> Request:
    # request是新对象，不会受A的影响（除非A返回了修改后的对象）
    return request.with_header("X-B", "b")
```

---

### 5. 洋葱模型符合直觉 ✅

```
Request:
  Interceptor A (before)
    → Interceptor B (before)
      → HTTP请求
      → HTTP响应
    ← Interceptor B (after)
  ← Interceptor A (after)
Response
```

---

### 6. 支持多种配置方式 ✅

- ✅ 声明式配置（settings.yaml） - 适合80%场景
- ✅ 编程式配置（链式调用） - 适合15%复杂场景
- ✅ 装饰器配置（@retry） - 适合API级别配置

---

### 7. 没有重复执行问题 ✅

**原因**: 只有一个执行入口 - `HttpClient.request()`

```python
def request(self, method, url, **kwargs) -> Response:
    request = Request(...)
    request = self.chain.execute_before_request(request)  # 执行1次
    http_response = self.client.request(...)
    response = Response(...)
    response = self.chain.execute_after_response(response)  # 执行1次
    return response
```

---

### 8. 性能优化 ✅

**优化点**:
1. 拦截器返回`None`表示不修改 - 避免创建新对象
2. 不可变对象 - 支持未来的并发优化
3. 惰性求值 - `json_data`只在需要时解析

---

## 🔄 与现有实现对比

### 当前实现的问题

| 问题 | 现有实现 | 理想设计 |
|------|---------|---------|
| **重复执行** | HttpClient + BaseAPI两层 | 只在HttpClient一层 |
| **难以理解** | kwargs字典传递 | Request/Response对象 |
| **拦截器互相影响** | 可变对象 | 不可变对象 |
| **配置混乱** | 自动配置vs手工配置冲突 | 统一的配置方式 |
| **调试困难** | 不知道拦截器执行顺序 | 明确的priority和日志 |

---

### 迁移成本

**破坏性变更**:
1. `HttpClient.request()`的参数从`**kwargs`改为`Request`对象
2. `Interceptor`接口从`__call__(**kwargs)`改为`before_request(request)`
3. BaseAPI不再有`request_interceptors`参数

**兼容层**（可选）:
```python
# 提供v3兼容适配器
class V3InterceptorAdapter(BaseInterceptor):
    """适配v3的拦截器"""

    def __init__(self, v3_interceptor: Callable):
        self.v3_interceptor = v3_interceptor

    def before_request(self, request: Request) -> Request:
        kwargs = {
            "headers": request.headers,
            "params": request.params,
            "json": request.json,
        }
        new_kwargs = self.v3_interceptor(request.method, request.url, **kwargs)

        return Request(
            method=request.method,
            url=request.url,
            headers=new_kwargs.get("headers", request.headers),
            params=new_kwargs.get("params", request.params),
            json=new_kwargs.get("json", request.json),
        )
```

---

## 📝 总结

### 核心设计理念

1. **单一职责** - 每个组件只做一件事
2. **不可变对象** - Request/Response不可变，拦截器返回新对象
3. **洋葱模型** - before → HTTP → after（逆序）
4. **单一入口** - 所有拦截器在HttpClient.request()执行
5. **简单直观** - 80%场景零代码配置

### 关键创新

- ✅ `Request/Response`对象（不可变）
- ✅ `Interceptor`接口（生命周期钩子）
- ✅ `InterceptorChain`（责任链模式）
- ✅ 链式调用`client.use(interceptor)`
- ✅ 统一的配置系统

### 解决的问题

- ❌ 重复执行 → ✅ 单一入口
- ❌ 混用冲突 → ✅ 统一配置
- ❌ 难以理解 → ✅ 简单清晰
- ❌ 难以调试 → ✅ 明确的执行顺序
- ❌ 不易扩展 → ✅ 简单的Interceptor接口

---

**这是一个从第一性原理出发的设计，完全抛开现有实现的约束。**

你觉得这个设计怎么样？有哪些地方需要调整？
