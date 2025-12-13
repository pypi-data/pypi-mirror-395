# 中间件使用指南

> **版本要求**: df-test-framework >= 3.14.0
> **更新日期**: 2025-12-05
> **最新版本**: v3.17.0

---

## 概述

v3.14.0 引入了全新的**中间件系统**（Middleware），采用**洋葱模型**架构，取代旧的 Interceptor 系统。

**v3.17.0 增强** ⚡:
- ✅ 中间件与 EventBus 深度整合
- ✅ 自动记录中间件处理过程到 Allure（通过 `allure_observer`）
- ✅ 支持 OpenTelemetry 追踪上下文传播

### 为什么选择中间件？

**洋葱模型**的优势：
- ✅ before 和 after 在同一作用域，自然共享状态
- ✅ 代码更简洁，逻辑更清晰
- ✅ 符合业界标准（Starlette、FastAPI、Koa 等）

**对比示例**：

```python
# ❌ 旧的 Interceptor（before/after 分离，状态共享困难）
class TimingInterceptor(BaseInterceptor):
    def before_request(self, request):
        self._start_time = time.time()  # 需要实例变量
        return request

    def after_response(self, response):
        duration = time.time() - self._start_time  # 访问实例变量
        return response

# ✅ 新的 Middleware（洋葱模型，自然共享局部变量）
class TimingMiddleware(BaseMiddleware):
    async def __call__(self, request, call_next):
        start = time.time()  # before - 局部变量
        response = await call_next(request)
        duration = time.time() - start  # after - 直接访问
        print(f"耗时: {duration}s")
        return response
```

---

## 快速开始

### 1. 使用内置中间件

```python
from df_test_framework import (
    HttpClient,
    SignatureMiddleware,
    RetryMiddleware,
    LoggingMiddleware
)

# 创建客户端
client = HttpClient(base_url="https://api.example.com")

# 链式添加中间件
client.use(LoggingMiddleware())
client.use(RetryMiddleware(max_retries=3))
client.use(SignatureMiddleware(secret="my_secret", algorithm="md5"))

# 发送请求（中间件自动生效）
response = client.request_with_middleware("GET", "/users")
```

### 2. 或在构造时传入

```python
client = HttpClient(
    base_url="https://api.example.com",
    middlewares=[
        RetryMiddleware(max_retries=3, priority=5),
        SignatureMiddleware(secret="my_secret", priority=10),
        LoggingMiddleware(priority=100),
    ]
)

response = client.request_with_middleware("GET", "/users")
```

---

## 内置中间件

### SignatureMiddleware - 请求签名

自动为请求添加签名，支持多种算法。

```python
from df_test_framework import SignatureMiddleware

# MD5 签名
middleware = SignatureMiddleware(
    secret="your_secret_key",
    algorithm="md5",           # 默认
    header_name="X-Sign",      # 签名 Header 名称
    timestamp_header="X-Timestamp",  # 时间戳 Header
    include_params=True,       # 包含 URL 参数
    include_body=True,         # 包含请求体
)

client.use(middleware)

# 发送请求
response = client.request_with_middleware("POST", "/api/orders", json={
    "order_no": "ORDER001",
    "amount": 100.0
})

# 自动添加的 Headers:
# X-Sign: 计算的签名值
# X-Timestamp: 当前时间戳
```

**支持的算法**：
- `md5` - MD5 签名（默认）
- `sha256` - SHA256 签名
- `hmac-sha256` - HMAC-SHA256 签名

**签名计算方式**：
```python
# 1. 收集参数和请求体
data = {**url_params, **request_body, "timestamp": timestamp}

# 2. 按键名排序
sorted_items = sorted(data.items())

# 3. 拼接并计算哈希
sign_string = "&".join(f"{k}={v}" for k, v in sorted_items) + secret
signature = hashlib.md5(sign_string.encode()).hexdigest()
```

### RetryMiddleware - 自动重试

失败时自动重试请求。

```python
from df_test_framework import RetryMiddleware

middleware = RetryMiddleware(
    max_retries=3,          # 最大重试次数
    backoff_factor=0.5,     # 退避因子（每次重试等待时间）
    retry_on_status=[500, 502, 503, 504],  # 哪些状态码触发重试
    priority=5,             # 优先级（建议设为最外层）
)

client.use(middleware)

# 如果返回 500，会自动重试最多 3 次
# 重试等待时间：0.5s、1s、2s（指数退避）
response = client.request_with_middleware("GET", "/api/unstable")
```

### LoggingMiddleware - 请求日志

自动记录请求和响应详情。

```python
from df_test_framework import LoggingMiddleware

middleware = LoggingMiddleware(
    log_request=True,       # 记录请求
    log_response=True,      # 记录响应
    log_headers=False,      # 是否记录 Headers
    max_body_length=1000,   # 最大 body 长度（截断）
)

client.use(middleware)

# 自动打印请求和响应日志
response = client.request_with_middleware("POST", "/api/users", json={...})

# 输出示例：
# [HTTP Request] POST https://api.example.com/api/users
# [HTTP Response] 201 Created (0.234s)
```

### BearerTokenMiddleware - Token 认证

自动添加 Bearer Token。

```python
from df_test_framework import BearerTokenMiddleware

middleware = BearerTokenMiddleware(
    token="your_access_token",
    header_name="Authorization",  # 默认
    token_prefix="Bearer",         # 默认
)

client.use(middleware)

# 自动添加: Authorization: Bearer your_access_token
response = client.request_with_middleware("GET", "/api/protected")
```

### HttpTelemetryMiddleware - 可观测性

集成 Telemetry，自动记录 Trace、Metrics、Logs。

```python
from df_test_framework import HttpTelemetryMiddleware, Telemetry

telemetry = Telemetry(logger=logger)

middleware = HttpTelemetryMiddleware(
    telemetry=telemetry,
    span_name_template="http.{method}",  # Span 名称模板
)

client.use(middleware)

# 每个请求自动记录：
# - Trace Span（包含 method、url、status_code）
# - Metrics（http.request.duration、http.request.count）
# - Logs（Starting/Completed HTTP request）
response = client.request_with_middleware("GET", "/api/users")
```

---

## 自定义中间件

### 基本结构

```python
from df_test_framework.core.middleware import BaseMiddleware
from df_test_framework.capabilities.clients.http.core import Request, Response

class CustomMiddleware(BaseMiddleware[Request, Response]):
    """自定义中间件"""

    def __init__(self, config: str, priority: int = 50):
        super().__init__(name="CustomMiddleware", priority=priority)
        self.config = config

    async def __call__(self, request: Request, call_next):
        # Before: 请求发送前的逻辑
        print(f"发送请求: {request.method} {request.url}")

        # 修改请求（如果需要）
        request = request.with_header("X-Custom", self.config)

        # 调用下一个中间件（或发送实际请求）
        response = await call_next(request)

        # After: 响应返回后的逻辑
        print(f"收到响应: {response.status_code}")

        # 修改响应（如果需要）
        # response.custom_data = {...}

        return response
```

### 示例 1: 请求计时中间件

```python
import time
from df_test_framework.core.middleware import BaseMiddleware

class TimingMiddleware(BaseMiddleware):
    """请求计时中间件"""

    async def __call__(self, request, call_next):
        start = time.monotonic()

        response = await call_next(request)

        duration = time.monotonic() - start
        print(f"⏱️ {request.method} {request.url} - {duration:.3f}s")

        # 将耗时附加到响应对象
        response.duration = duration

        return response

# 使用
client.use(TimingMiddleware())
response = client.request_with_middleware("GET", "/api/slow")
print(f"请求耗时: {response.duration:.3f}s")
```

### 示例 2: 自动添加请求 ID

```python
import uuid
from df_test_framework.core.middleware import BaseMiddleware

class RequestIDMiddleware(BaseMiddleware):
    """为每个请求添加唯一 ID"""

    async def __call__(self, request, call_next):
        # 生成请求 ID
        request_id = str(uuid.uuid4())

        # 添加到请求头
        request = request.with_header("X-Request-ID", request_id)

        print(f"📋 Request ID: {request_id}")

        response = await call_next(request)

        # 将 request_id 附加到响应
        response.request_id = request_id

        return response
```

### 示例 3: 慢请求告警

```python
import time
from df_test_framework.core.middleware import BaseMiddleware

class SlowRequestAlertMiddleware(BaseMiddleware):
    """慢请求告警中间件"""

    def __init__(self, threshold: float = 3.0, priority: int = 1):
        super().__init__(name="SlowRequestAlert", priority=priority)
        self.threshold = threshold

    async def __call__(self, request, call_next):
        start = time.monotonic()

        response = await call_next(request)

        duration = time.monotonic() - start

        if duration > self.threshold:
            print(f"⚠️ 慢请求告警: {request.method} {request.url}")
            print(f"   耗时: {duration:.2f}s (阈值: {self.threshold}s)")
            # 可以发送告警通知、记录日志等

        return response

# 使用
client.use(SlowRequestAlertMiddleware(threshold=2.0))
```

### 示例 4: 请求/响应拦截修改

```python
from df_test_framework.core.middleware import BaseMiddleware

class ModifyRequestResponseMiddleware(BaseMiddleware):
    """修改请求和响应"""

    async def __call__(self, request, call_next):
        # 修改请求：添加公共参数
        if request.method == "POST":
            if request.json:
                # 添加公共字段
                request.json["app_version"] = "1.0.0"
                request.json["device_id"] = "test_device"

        response = await call_next(request)

        # 修改响应：提取嵌套数据
        if response.status_code == 200:
            data = response.json()
            if "data" in data:
                # 展开嵌套的 data 字段
                response._json_data = data["data"]

        return response
```

---

## 中间件优先级

### 优先级规则

- **数字越小，优先级越高（越先执行，在更外层）**
- 执行顺序：`优先级低 → 高 → 实际请求 → 高 → 低`

```python
client.use(RetryMiddleware(priority=5))       # 最外层（最先/最后执行）
client.use(SignatureMiddleware(priority=10))  # 中间层
client.use(LoggingMiddleware(priority=100))   # 最内层（最后/最先执行）

# 执行流程：
# Retry(before) → Signature(before) → Logging(before)
#     → 实际请求
# Retry(after) ← Signature(after) ← Logging(after)
```

### 推荐优先级

| 中间件 | 推荐优先级 | 原因 |
|--------|-----------|------|
| RetryMiddleware | 1-5 | 最外层，可以重试整个请求链 |
| SignatureMiddleware | 10-20 | 签名应在重试之后、日志之前 |
| BearerTokenMiddleware | 10-20 | 认证应在业务逻辑之前 |
| HttpTelemetryMiddleware | 1-10 | 记录完整的请求周期 |
| LoggingMiddleware | 80-100 | 最内层，记录最接近实际请求的日志 |
| 自定义业务中间件 | 30-70 | 根据业务逻辑调整 |

---

## 高级用法

### 1. 条件中间件

```python
class ConditionalMiddleware(BaseMiddleware):
    """条件中间件 - 仅对特定请求生效"""

    async def __call__(self, request, call_next):
        # 仅对 POST 请求生效
        if request.method == "POST":
            print("处理 POST 请求")
            # ... 特殊逻辑

        return await call_next(request)
```

### 2. 中间件中止请求

```python
from df_test_framework.core import MiddlewareAbort

class RateLimitMiddleware(BaseMiddleware):
    """限流中间件"""

    def __init__(self, max_requests: int = 100):
        super().__init__(name="RateLimit")
        self.count = 0
        self.max_requests = max_requests

    async def __call__(self, request, call_next):
        self.count += 1

        if self.count > self.max_requests:
            # 中止请求，返回自定义响应
            raise MiddlewareAbort(
                status_code=429,
                message="请求过多，已触发限流"
            )

        return await call_next(request)
```

### 3. 中间件之间传递数据

```python
class DataPassingMiddleware(BaseMiddleware):
    """中间件间传递数据"""

    async def __call__(self, request, call_next):
        # 在 request 上附加数据
        request.custom_data = {"user_id": 123}

        response = await call_next(request)

        # 在 response 上附加数据
        response.custom_flag = True

        return response

class ConsumerMiddleware(BaseMiddleware):
    """消费数据的中间件"""

    async def __call__(self, request, call_next):
        # 读取上游中间件附加的数据
        if hasattr(request, "custom_data"):
            print(f"用户 ID: {request.custom_data['user_id']}")

        return await call_next(request)
```

---

## 最佳实践

### 1. 使用配置化中间件

```python
# ✅ 推荐：从配置读取
class Config:
    signature_enabled: bool = True
    signature_secret: str = "xxx"

if Config.signature_enabled:
    client.use(SignatureMiddleware(secret=Config.signature_secret))

# ❌ 不推荐：硬编码
# client.use(SignatureMiddleware(secret="hardcoded_secret"))
```

### 2. 中间件保持单一职责

```python
# ✅ 好：每个中间件只做一件事
client.use(LoggingMiddleware())
client.use(TimingMiddleware())
client.use(RetryMiddleware())

# ❌ 差：一个中间件做所有事情
# client.use(GodMiddleware())  # 日志+计时+重试+...
```

### 3. 合理设置优先级

```python
# ✅ 好：明确指定优先级
client.use(RetryMiddleware(priority=5))
client.use(SignatureMiddleware(priority=10))
client.use(LoggingMiddleware(priority=100))

# ⚠️ 注意：优先级相同时，按添加顺序执行
```

### 4. 使用类型注解

```python
from df_test_framework.core.middleware import BaseMiddleware
from df_test_framework.capabilities.clients.http.core import Request, Response

class MyMiddleware(BaseMiddleware[Request, Response]):
    async def __call__(
        self,
        request: Request,
        call_next
    ) -> Response:
        # 类型安全，IDE 有提示
        return await call_next(request)
```

---

## 常见问题

### Q: Middleware 和 Interceptor 有什么区别？

**A**: 核心区别是**状态共享**：

| 特性 | Interceptor | Middleware |
|------|-------------|------------|
| 架构 | before/after 分离 | 洋葱模型（嵌套） |
| 状态共享 | 需要实例变量 | 自然共享局部变量 |
| 代码复杂度 | 较高 | 较低 |
| 业界标准 | 否 | 是（Starlette/FastAPI/Koa） |

### Q: 如何从 Interceptor 迁移到 Middleware？

**A**: 查看 [迁移指南](../migration/v3.13-to-v3.14.md)。

**快速对照**：

```python
# Interceptor → Middleware
before_request() → __call__() 的前半部分
after_response() → __call__() 的后半部分

# 优先级反转
priority=100（先执行） → priority=10（先执行）
```

### Q: 可以同时使用旧的 Interceptor 吗？

**A**: 可以，但会触发 DeprecationWarning。建议尽快迁移到 Middleware。

### Q: 如何调试中间件执行顺序？

**A**: 使用 LoggingMiddleware 或自定义日志：

```python
class DebugMiddleware(BaseMiddleware):
    async def __call__(self, request, call_next):
        print(f"[{self.name}] Before")
        response = await call_next(request)
        print(f"[{self.name}] After")
        return response

client.use(DebugMiddleware(name="Outer", priority=5))
client.use(DebugMiddleware(name="Inner", priority=10))

# 输出:
# [Outer] Before
# [Inner] Before
# [Inner] After
# [Outer] After
```

---

## v3.17.0 整合示例

### 与 EventBus 和 Allure 整合

中间件处理的所有请求会自动发布事件，并可被 `AllureObserver` 记录。

```python
from df_test_framework import HttpClient, RetryMiddleware, SignatureMiddleware

# 测试中使用 allure_observer fixture
def test_with_middleware(allure_observer, http_client):
    # 添加中间件
    http_client.use(RetryMiddleware(max_retries=3))
    http_client.use(SignatureMiddleware(secret="xxx", algorithm="md5"))

    # 发送请求
    response = http_client.get("/users")

    # ✅ Allure 报告自动包含:
    #    - 中间件处理的完整请求/响应
    #    - 重试次数（如果发生）
    #    - 签名信息
    #    - OpenTelemetry trace_id/span_id
    #    - 响应时间
```

### 自定义中间件与事件

```python
from df_test_framework import BaseMiddleware, EventBus
from df_test_framework.core.events import HttpRequestStartEvent, HttpRequestEndEvent

class MonitoringMiddleware(BaseMiddleware):
    """监控中间件 - 与 EventBus 集成"""

    async def __call__(self, request, call_next):
        # 中间件可以访问 EventBus（如果 HttpClient 配置了）
        response = await call_next(request)

        # HttpClient 会自动发布 HttpRequestEndEvent
        # 订阅者可以监听该事件

        return response

# 使用
bus = EventBus()

@bus.on(HttpRequestEndEvent)
def monitor(event):
    if event.duration > 1.0:
        print(f"⚠️ 慢请求: {event.url}")

client = HttpClient(base_url="...", event_bus=bus)
client.use(MonitoringMiddleware())
```

### OpenTelemetry 追踪传播

中间件自动支持 OpenTelemetry 上下文传播：

```python
from opentelemetry import trace
from df_test_framework import HttpClient, LoggingMiddleware

tracer = trace.get_tracer(__name__)

def test_with_tracing(http_client):
    http_client.use(LoggingMiddleware())

    with tracer.start_as_current_span("api-call") as span:
        response = http_client.get("/users")
        # ✅ 请求事件自动包含:
        #    - trace_id: 当前 Span 的 Trace ID
        #    - span_id: 当前 Span 的 Span ID
        # ✅ 可用于分布式追踪链路分析
```

---

## 参考资料

- [快速开始](../user-guide/QUICK_START.md)
- [快速参考](../user-guide/QUICK_REFERENCE.md)
- [EventBus 使用指南](event_bus_guide.md)
- [Telemetry 使用指南](telemetry_guide.md)
- [v3.17.0 发布说明](../releases/v3.17.0.md)
- [v3.13 → v3.14 迁移指南](../migration/v3.13-to-v3.14.md)
- [API 参考文档](../api-reference/)
