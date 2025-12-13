# DF Test Framework 架构总览 (v3.17.0)

**版本**: v3.17.0
**更新日期**: 2025-12-05
**架构代号**: 五层架构 + 事件驱动 + 可观测性

---

## 📋 目录

- [设计目标](#设计目标)
- [五层架构](#五层架构)
- [核心设计原则](#核心设计原则)
- [层级详解](#层级详解)
- [关键特性](#关键特性)
- [架构演进](#架构演进)

---

## 🎯 设计目标

### 核心理念

DF Test Framework v3.17.0 基于以下核心理念构建：

1. **清晰的层级分离** - 五层架构，职责明确，依赖单向
2. **事件驱动** - EventBus 发布/订阅模式，组件解耦
3. **可观测性融合** - OpenTelemetry 追踪、Metrics、结构化日志
4. **类型安全** - Pydantic v2 配置验证，Python 3.12+ 类型注解
5. **可扩展性** - Pluggy Hook 系统，灵活的扩展点

### 设计原则

```
1. 单向依赖  - 高层依赖低层，低层不感知高层
2. 职责单一  - 每层只关注自己的职责
3. 开放封闭  - 对扩展开放，对修改封闭
4. 依赖注入  - 通过 Provider/Runtime 管理依赖
5. 事件驱动  - 通过 EventBus 实现组件间通信
```

---

## 🏗️ 五层架构

### 架构图

```
┌─────────────────────────────────────────────────────────────┐
│                    Layer 4 - Bootstrap                      │
│              框架组装与初始化（可依赖所有层）                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Bootstrap   │  │  Providers   │  │   Runtime    │      │
│  │  (启动入口)   │  │  (服务工厂)   │  │ (运行时上下文)│      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└───────────────────────────┬─────────────────────────────────┘
                            │ 可依赖所有层
        ┌───────────────────┴───────────────────┐
        │                                       │
┌───────▼─────────────────┐          ┌────────▼───────────────┐
│  Layer 3 - Testing/CLI  │          │  Plugins (横切关注点)  │
│      测试工具 + CLI      │          │      插件实现           │
│  ┌────────┐  ┌────────┐ │          │  ┌──────────────────┐ │
│  │Fixtures│  │  CLI   │ │          │  │ MonitoringPlugin │ │
│  │Debugging│ │Scaffold│ │          │  │  AllurePlugin    │ │
│  └────────┘  └────────┘ │          │  └──────────────────┘ │
└───────┬─────────────────┘          └────────────────────────┘
        │ 可依赖 Layer 0-2
┌───────▼─────────────────────────────────────────────────────┐
│                 Layer 2 - Capabilities                      │
│           能力层（HTTP/DB/MQ/Storage/Drivers）                │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐           │
│  │  HTTP  │  │   DB   │  │   MQ   │  │Storage │           │
│  │ Client │  │Database│  │ Kafka  │  │  S3    │           │
│  │GraphQL │  │  Redis │  │RabbitMQ│  │  OSS   │           │
│  │  gRPC  │  │  UoW   │  │RocketMQ│  │LocalFile│          │
│  └────────┘  └────────┘  └────────┘  └────────┘           │
│  ┌────────────────────────────────────────────┐            │
│  │           Web Drivers (Playwright)         │            │
│  └────────────────────────────────────────────┘            │
└───────┬─────────────────────────────────────────────────────┘
        │ 可依赖 Layer 0-1
┌───────▼─────────────────────────────────────────────────────┐
│              Layer 1 - Infrastructure                       │
│           基础设施（Config/Events/Telemetry/Plugins）         │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐           │
│  │ Config │  │EventBus│  │Telemetry│ │ Plugins│           │
│  │Settings│  │ Pub/Sub│  │ Tracing│  │ Pluggy │           │
│  │ Logging│  │TestIso │  │ Metrics│  │  Hooks │           │
│  └────────┘  └────────┘  └────────┘  └────────┘           │
└───────┬─────────────────────────────────────────────────────┘
        │ 只能依赖 Layer 0
┌───────▼─────────────────────────────────────────────────────┐
│                    Layer 0 - Core                           │
│              核心抽象（无第三方依赖）                           │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐           │
│  │Middleware│ │ Events │ │ Context│  │ Types  │           │
│  │  Chain  │  │  Base  │  │Execution│ │Exception│          │
│  │ Protocol│  │Correlated│ │Propagation│ │Enums│          │
│  └────────┘  └────────┘  └────────┘  └────────┘           │
└─────────────────────────────────────────────────────────────┘
```

### 依赖规则

```
Layer 4 (bootstrap/)       ──► 可依赖 Layer 0-3 全部（引导层特权）
Layer 3 (testing/ + cli/)  ──► 可依赖 Layer 0-2（门面层，并行）
Layer 2 (capabilities/)    ──► 可依赖 Layer 0-1
Layer 1 (infrastructure/)  ──► 只能依赖 Layer 0
Layer 0 (core/)            ──► 无依赖（最底层）
plugins/ (横切关注点)       ──► 可依赖任意层级
```

---

## 📐 核心设计原则

### 1. 单向依赖

```
✅ 正确：Layer 2 导入 Layer 1
from df_test_framework.infrastructure.events import EventBus

✅ 正确：Layer 3 导入 Layer 2
from df_test_framework.capabilities.clients.http import HttpClient

❌ 错误：Layer 1 导入 Layer 2
from df_test_framework.capabilities.clients.http import HttpClient  # 违规！
```

### 2. 职责单一

每层只关注自己的核心职责：

| 层级 | 职责 | 不应包含 |
|------|------|----------|
| Layer 0 | 定义抽象和协议 | 具体实现、第三方依赖 |
| Layer 1 | 提供基础设施服务 | 业务逻辑、测试工具 |
| Layer 2 | 封装技术能力 | 测试逻辑、框架组装 |
| Layer 3 | 提供测试工具 | 框架初始化 |
| Layer 4 | 组装框架 | 业务逻辑 |

### 3. 事件驱动

组件间通过 EventBus 通信，避免直接耦合：

```python
# ✅ 好：通过事件通信
class HttpClient:
    def request(self, ...):
        event, correlation_id = HttpRequestStartEvent.create(...)
        self._event_bus.publish_sync(event)
        # ... 执行请求 ...
        end_event = HttpRequestEndEvent.create(correlation_id=correlation_id, ...)
        self._event_bus.publish_sync(end_event)

# AllureObserver 订阅事件，无需耦合
@pytest.fixture
def allure_observer():
    observer = AllureObserver()
    event_bus.subscribe(HttpRequestStartEvent, observer.handle_start)
    event_bus.subscribe(HttpRequestEndEvent, observer.handle_end)
```

---

## 📚 层级详解

### Layer 0 - Core (核心抽象层)

**目录**: `src/df_test_framework/core/`

**职责**: 定义纯抽象、协议和类型，无第三方依赖。

**核心模块**:

```
core/
├── middleware/           # 中间件系统
│   ├── base.py          # Middleware 协议
│   ├── chain.py         # MiddlewareChain
│   └── decorators.py    # @middleware
├── events/              # 事件系统
│   ├── types.py         # Event、CorrelatedEvent、工厂方法
│   └── __init__.py
├── context/             # 上下文传播
│   ├── execution.py     # ExecutionContext
│   └── __init__.py
├── exceptions.py        # 异常体系
└── types.py            # 枚举和类型定义
```

**关键设计**:

1. **中间件协议** - 定义洋葱模型接口
2. **事件基类** - Event、CorrelatedEvent（v3.17.0 新增）
3. **上下文传播** - ExecutionContext 跨层传递
4. **类型安全** - 类型注解、枚举

**示例**:
```python
# 事件定义
@dataclass(frozen=True)
class Event:
    event_id: str = field(default_factory=generate_event_id)
    timestamp: datetime = field(default_factory=datetime.now)
    trace_id: str | None = None  # v3.17.0: OpenTelemetry 追踪
    span_id: str | None = None

@dataclass(frozen=True)
class CorrelatedEvent(Event):
    correlation_id: str = ""  # v3.17.0: 事件关联

# 工厂方法
event, correlation_id = HttpRequestStartEvent.create(method="GET", url="...")
```

### Layer 1 - Infrastructure (基础设施层)

**目录**: `src/df_test_framework/infrastructure/`

**职责**: 提供配置、日志、事件总线、遥测、插件等基础设施。

**核心模块**:

```
infrastructure/
├── config/              # 配置系统
│   ├── settings.py      # FrameworkSettings (Pydantic)
│   ├── sources.py       # 配置源（Env/Dotenv/Dict）
│   └── logging.py       # LoggingConfig、LoggerStrategy
├── events/              # 事件总线
│   ├── bus.py          # EventBus、测试隔离
│   └── __init__.py
├── telemetry/           # 可观测性
│   ├── telemetry.py     # Telemetry 抽象
│   └── noop.py         # NoopTelemetry
├── tracing/             # 分布式追踪
│   ├── manager.py       # TracingManager
│   └── interceptors/    # TracingInterceptor
├── plugins/             # 插件系统
│   ├── manager.py       # PluggyPluginManager
│   └── hooks.py        # HookSpecs
└── context/             # 上下文载体
    └── carriers/        # HttpContextCarrier、GrpcContextCarrier
```

**关键设计**:

1. **EventBus 测试隔离** (v3.17.0)
   ```python
   # 每个测试独立的 EventBus
   _test_event_bus: ContextVar[EventBus | None] = ContextVar("test_event_bus")

   def get_event_bus() -> EventBus:
       test_bus = _test_event_bus.get()
       if test_bus is not None:
           return test_bus
       return _global_event_bus
   ```

2. **配置分层**
   ```python
   class FrameworkSettings(BaseSettings):
       http: HTTPConfig
       db: DatabaseConfig
       redis: RedisConfig
       test: TestExecutionConfig
       logging: LoggingConfig
       # v3.14.0: 可扩展命名空间
       extras: dict[str, Any] = {}
   ```

3. **Pluggy Hook 系统**
   ```python
   class HookSpecs:
       @hookspec
       def df_providers(self, registry: ProviderRegistry) -> dict: ...

       @hookspec
       def df_post_bootstrap(self, runtime: RuntimeContext) -> None: ...
   ```

### Layer 2 - Capabilities (能力层)

**目录**: `src/df_test_framework/capabilities/`

**职责**: 封装技术能力（HTTP、数据库、消息队列、存储、驱动）。

**核心模块**:

```
capabilities/
├── clients/             # 客户端
│   ├── http/           # HTTP 客户端
│   │   ├── core/       # Request、Response
│   │   ├── middleware/ # 中间件实现
│   │   └── rest/httpx/ # HttpClient、AsyncHttpClient
│   ├── graphql/        # GraphQL 客户端
│   └── grpc/          # gRPC 客户端
├── databases/          # 数据库
│   ├── database.py     # Database (SQLAlchemy)
│   ├── redis/         # RedisClient
│   ├── repositories/  # Repository 模式
│   └── uow.py        # Unit of Work
├── messengers/         # 消息队列
│   ├── kafka/         # KafkaClient
│   ├── rabbitmq/      # RabbitMQClient
│   └── rocketmq/      # RocketMQClient
├── storages/          # 存储
│   ├── local_file/    # LocalFileClient
│   ├── s3/           # S3Client
│   └── oss/          # OSSClient
└── drivers/           # 驱动
    └── web/          # Playwright、Selenium
```

**关键设计**:

1. **HTTP 中间件** (v3.14.0)
   ```python
   client = HttpClient()
   client.use(SignatureMiddleware())
   client.use(RetryMiddleware(max_retries=3))
   client.use(LoggingMiddleware())

   response = client.get("/api/users")
   ```

2. **事件发布** (v3.17.0)
   ```python
   class HttpClient:
       def request(self, method: str, url: str, **kwargs) -> Response:
           # 动态获取 EventBus（支持测试隔离）
           event_bus = self._event_bus or get_event_bus()

           # 使用工厂方法创建事件
           start_event, correlation_id = HttpRequestStartEvent.create(
               method=method, url=url, headers=headers, body=body
           )
           event_bus.publish_sync(start_event)

           # ... 执行请求 ...

           end_event = HttpRequestEndEvent.create(
               correlation_id=correlation_id,
               status_code=response.status_code,
               duration=duration,
               body=response.body  # v3.17.0: 包含响应体
           )
           event_bus.publish_sync(end_event)
   ```

3. **Repository + UoW 模式**
   ```python
   with UnitOfWork() as uow:
       user = uow.users.find_by_id(123)
       user.name = "Updated"
       uow.commit()  # 自动提交所有 Repository 变更
   ```

### Layer 3 - Testing / CLI (门面层)

**目录**: `src/df_test_framework/testing/` + `src/df_test_framework/cli/`

**职责**: 提供测试工具（Fixtures、调试器、数据构建）和 CLI 脚手架。

**核心模块**:

```
testing/
├── fixtures/            # Pytest Fixtures
│   ├── core.py         # runtime、http_client、database、redis_client
│   ├── allure.py       # _auto_allure_observer (v3.17.0 测试隔离)
│   ├── cleanup.py      # CleanupManager、ListCleanup
│   └── ui.py          # browser_manager、page
├── reporting/          # 报告系统
│   └── allure/        # AllureObserver、AllureHelper
├── debugging/          # 调试工具
│   ├── http.py        # HTTPDebugger
│   └── database.py    # DBDebugger
├── data/              # 数据工具
│   ├── builders/      # Builder 模式
│   └── loaders/       # JSONLoader、CSVLoader
└── plugins/           # pytest 插件
    └── markers.py     # dev_only、prod_only

cli/
├── commands/          # CLI 命令
│   ├── init.py       # df-test init
│   └── gen.py        # df-test gen
└── templates/        # 脚手架模板
```

**关键设计**:

1. **Allure 测试隔离** (v3.17.0)
   ```python
   @pytest.fixture(scope="function", autouse=True)
   def _auto_allure_observer(request):
       observer = AllureObserver(test_name=request.node.name)
       set_current_observer(observer)

       # v3.17.0: 每个测试独立的 EventBus
       test_event_bus = EventBus()
       set_test_event_bus(test_event_bus)

       # 订阅事件
       test_event_bus.subscribe(HttpRequestStartEvent, observer.handle_http_request_start_event)
       test_event_bus.subscribe(HttpRequestEndEvent, observer.handle_http_request_end_event)
       test_event_bus.subscribe(HttpRequestErrorEvent, observer.handle_http_request_error_event)

       try:
           yield observer
       finally:
           observer.cleanup()
           set_current_observer(None)
           test_event_bus.clear()
           set_test_event_bus(None)  # 清理上下文
   ```

2. **调试工具自动注入**
   ```python
   # HTTPDebugger 自动记录所有请求/响应
   with HTTPDebugger():
       response = http_client.get("/api/users")
   # 自动打印请求详情、响应状态、耗时
   ```

### Layer 4 - Bootstrap (引导层)

**目录**: `src/df_test_framework/bootstrap/`

**职责**: 框架组装、初始化、服务注册（可依赖所有层）。

**核心模块**:

```
bootstrap/
├── bootstrap.py        # Bootstrap、BootstrapApp
├── providers.py        # ProviderRegistry、Provider、SingletonProvider
└── runtime.py         # RuntimeContext、RuntimeBuilder
```

**关键设计**:

1. **Bootstrap 启动流程**
   ```python
   from df_test_framework import Bootstrap

   runtime = (
       Bootstrap()
       .with_settings(MySettings, namespace="myapp")
       .with_plugin("myapp.plugins")
       .build()
       .run()
   )

   # 获取服务
   http = runtime.http_client()
   db = runtime.database()
   ```

2. **Provider 注册**
   ```python
   class ProviderRegistry:
       def register(self, name: str, provider: Provider):
           self._providers[name] = provider

       def get(self, name: str) -> Any:
           provider = self._providers.get(name)
           if not provider:
               raise ProviderError(f"Provider '{name}' not found")
           return provider.create(self._context)
   ```

3. **SingletonProvider**
   ```python
   class SingletonProvider:
       def __init__(self, factory: Callable):
           self._factory = factory
           self._instance = None
           self._lock = threading.Lock()

       def create(self, context: RuntimeContext) -> Any:
           if self._instance is None:
               with self._lock:
                   if self._instance is None:  # 双重检查锁
                       self._instance = self._factory(context)
           return self._instance
   ```

---

## ⚡ 关键特性

### 1. 事件驱动架构 (v3.14.0+)

**EventBus 发布/订阅模式**:
```python
# 发布事件
event_bus.publish_sync(HttpRequestStartEvent(...))

# 订阅事件
event_bus.subscribe(HttpRequestEndEvent, handler)

# 装饰器订阅
@event_bus.on(HttpRequestEndEvent)
async def handle_request_end(event):
    print(f"Request completed: {event.status_code}")
```

### 2. 事件关联系统 (v3.17.0)

**correlation_id 关联 Start/End 事件**:
```python
# 发布 Start 事件，获取 correlation_id
event, correlation_id = HttpRequestStartEvent.create(method="GET", url="...")
event_bus.publish_sync(event)

# End 事件复用 correlation_id
end_event = HttpRequestEndEvent.create(
    correlation_id=correlation_id,  # 关联 Start 事件
    status_code=200,
    duration=0.5
)
event_bus.publish_sync(end_event)

# AllureObserver 通过 correlation_id 匹配 Start/End 事件
```

### 3. OpenTelemetry 追踪整合 (v3.17.0)

**自动注入 trace_id/span_id**:
```python
# 工厂方法自动从当前 Span 提取追踪上下文
def _get_current_trace_context() -> tuple[str | None, str | None]:
    span = trace.get_current_span()
    if span and span.is_recording():
        ctx = span.get_span_context()
        trace_id = format(ctx.trace_id, "032x")
        span_id = format(ctx.span_id, "016x")
        return trace_id, span_id
    return None, None

# 事件自动包含追踪信息
event = HttpRequestStartEvent.create(...)
# event.trace_id = "a1b2c3d4e5f6..."
# event.span_id = "1234567890abcdef"
```

### 4. 测试隔离 (v3.17.0)

**每个测试独立的 EventBus**:
```python
# ContextVar 实现
_test_event_bus: ContextVar[EventBus | None] = ContextVar("test_event_bus")

def test_a():
    # 自动获取测试级 EventBus
    bus = get_event_bus()  # 返回 test_a 的独立 EventBus

def test_b():
    # 不会收到 test_a 的事件
    bus = get_event_bus()  # 返回 test_b 的独立 EventBus
```

### 5. 中间件系统 (v3.14.0)

**洋葱模型**:
```python
class LoggingMiddleware(Middleware):
    async def process(self, request: Request, next: Callable) -> Response:
        print(f"→ Request: {request.method} {request.url}")
        response = await next(request)
        print(f"← Response: {response.status_code}")
        return response

client = HttpClient()
client.use(SignatureMiddleware())  # 最外层
client.use(RetryMiddleware())      # 中间层
client.use(LoggingMiddleware())    # 最内层
```

---

## 📈 架构演进

### v3.0 → v3.14.0

- **问题**: 目录按技术栈组织（clients/databases/drivers），职责不清
- **改进**: 引入四层架构，按职责分层

### v3.14.0 → v3.16.0

- **问题**: infrastructure/ 依赖 capabilities/，违反架构规则
- **改进**: 引入 Layer 4 Bootstrap 引导层，解决依赖违规

**v3.14.0 (旧)**:
```
Layer 0: common/
Layer 1: clients/databases/drivers/
Layer 2: infrastructure/
Layer 3: testing/
Layer 4: extensions/
```

**v3.16.0 (新)**:
```
Layer 0: core/
Layer 1: infrastructure/
Layer 2: capabilities/
Layer 3: testing/ + cli/
Layer 4: bootstrap/
```

### v3.16.0 → v3.17.0

- **问题**: Allure 报告无法记录 HTTP 请求/响应（EventBus 未集成）
- **改进**:
  - 事件关联系统（correlation_id）
  - OpenTelemetry 追踪整合（trace_id/span_id）
  - 测试隔离（独立 EventBus）
  - 动态 EventBus 解析

---

## 📝 使用示例

### 完整示例

```python
from df_test_framework import Bootstrap

# 1. 初始化框架
runtime = Bootstrap().build().run()

# 2. 获取服务
http_client = runtime.http_client()
database = runtime.database()

# 3. 使用中间件
http_client.use(SignatureMiddleware())
http_client.use(RetryMiddleware(max_retries=3))

# 4. 发送请求（自动发布事件）
response = http_client.get("/api/users")

# 5. Allure 自动记录（通过 EventBus 订阅）
# - HTTP 请求详情（method、url、headers、body）
# - HTTP 响应详情（status_code、headers、body）
# - event_id、correlation_id
# - trace_id、span_id（如果启用 OpenTelemetry）

# 6. 数据库操作
with database.transaction():
    result = database.execute("SELECT * FROM users WHERE id = ?", [123])
```

---

## 🔗 相关文档

- [v3.17.0 发布说明](../releases/v3.17.0.md) - 事件系统重构详情
- [v3.16.0 发布说明](../releases/v3.16.0.md) - Layer 4 Bootstrap 架构
- [v3.14.0 发布说明](../releases/v3.14.0.md) - 企业级平台架构升级
- [中间件使用指南](../guides/middleware_guide.md) - 中间件完整指南
- [EventBus 使用指南](../guides/event_bus_guide.md) - 事件驱动完整指南
- [架构演进历史](./archive/ARCHITECTURE_HISTORY.md) - 历史架构版本

---

**最后更新**: 2025-12-05
**下一次更新**: v3.18.0 发布后
