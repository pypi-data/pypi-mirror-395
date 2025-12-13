# 分布式追踪指南

> **版本**: v3.17.0 | **更新**: 2025-12-05
>
> - v3.10.0 新增 - OpenTelemetry 分布式追踪
> - v3.12.0 更新 - gRPC 追踪拦截器
> - **v3.17.0 更新** - EventBus 自动注入 trace_id/span_id ⚡

本指南介绍如何使用 DF Test Framework 的分布式追踪功能，基于 OpenTelemetry 标准实现。

## 目录

- [概述](#概述)
- [快速开始](#快速开始)
- [核心组件](#核心组件)
- [HTTP请求追踪](#http请求追踪)
- [gRPC请求追踪](#grpc请求追踪)
- [数据库查询追踪](#数据库查询追踪)
- [装饰器使用](#装饰器使用)
- [上下文传播](#上下文传播)
- [导出器配置](#导出器配置)
- [最佳实践](#最佳实践)

## 概述

分布式追踪帮助你：

- **可视化请求流程**：跟踪请求在各服务间的传递路径
- **性能分析**：识别慢查询和性能瓶颈
- **问题定位**：快速定位分布式系统中的错误
- **依赖分析**：了解服务间的调用关系

### 核心概念

| 概念 | 说明 |
|------|------|
| Trace | 一次完整的请求链路，包含多个 Span |
| Span | 一个操作单元（如 HTTP 请求、数据库查询） |
| Context | 追踪上下文，在服务间传递 |
| Baggage | 随追踪传播的自定义键值对 |

## 快速开始

### 安装依赖

```bash
# 基础追踪
pip install opentelemetry-sdk opentelemetry-api

# 可选导出器
pip install opentelemetry-exporter-otlp      # OTLP (推荐)
pip install opentelemetry-exporter-jaeger    # Jaeger
pip install opentelemetry-exporter-zipkin    # Zipkin
```

### 基础用法

```python
from df_test_framework.infrastructure.tracing import (
    TracingManager,
    TracingConfig,
    ExporterType,
    trace_span
)

# 1. 配置追踪
config = TracingConfig(
    service_name="my-test-service",
    exporter_type=ExporterType.CONSOLE,  # 开发环境用控制台
    batch_export=False
)

# 2. 初始化
tracing = TracingManager(config=config)
tracing.init()

# 3. 使用装饰器追踪函数
@trace_span("process_user")
def process_user(user_id: int):
    return {"id": user_id, "name": "Alice"}

# 4. 手动创建 Span
with tracing.start_span("custom_operation") as span:
    span.set_attribute("custom.key", "value")
    # 业务逻辑
    result = do_something()

# 5. 清理
tracing.shutdown()
```

## 核心组件

### TracingManager

追踪管理器，负责初始化和配置：

```python
from df_test_framework.infrastructure.tracing import TracingManager, TracingConfig

# 使用配置对象
config = TracingConfig(
    service_name="my-service",
    exporter_type=ExporterType.OTLP,
    endpoint="http://localhost:4317",
    batch_export=True,           # 生产环境推荐
    sample_rate=1.0,             # 全采样
    extra_attributes={"env": "test", "version": "1.0.0"}
)

manager = TracingManager(config=config)
manager.init()

# 简化用法
manager = TracingManager(service_name="my-service")
manager.init()
```

### TracingConfig

配置选项：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| service_name | str | "df-test-framework" | 服务名称 |
| exporter_type | ExporterType | CONSOLE | 导出器类型 |
| endpoint | str | None | 导出端点 URL |
| batch_export | bool | True | 是否批量导出 |
| sample_rate | float | 1.0 | 采样率 (0.0-1.0) |
| enabled | bool | True | 是否启用追踪 |
| extra_attributes | dict | {} | 额外资源属性 |

## HTTP请求追踪

### 使用 TracingInterceptor

为 HTTP 客户端添加自动追踪：

```python
from df_test_framework.clients.http.rest.httpx import AsyncHttpClient
from df_test_framework.infrastructure.tracing.interceptors import TracingInterceptor

# 创建追踪拦截器
tracing_interceptor = TracingInterceptor(
    record_headers=True,      # 记录请求/响应头
    record_body=False,        # 不记录请求体（避免敏感数据）
    propagate_context=True,   # 传播追踪上下文
    sensitive_headers=["authorization", "x-api-key"]  # 敏感头脱敏
)

# 添加到客户端
async with AsyncHttpClient("https://api.example.com") as client:
    client.interceptor_chain.add(tracing_interceptor)

    # 所有请求自动追踪
    response = await client.get("/users/1")
```

### 追踪属性

TracingInterceptor 自动记录：

- `http.method`: HTTP 方法
- `http.url`: 请求 URL
- `http.status_code`: 响应状态码
- `http.response_content_length`: 响应体长度
- `http.request.duration_ms`: 请求耗时

## gRPC请求追踪

> v3.12.0 新增

### 使用 GrpcTracingInterceptor

为 gRPC 客户端添加自动追踪：

```python
from df_test_framework.clients.grpc import GrpcClient
from df_test_framework.infrastructure.tracing.interceptors import GrpcTracingInterceptor

# 创建 gRPC 追踪拦截器
grpc_tracing = GrpcTracingInterceptor(
    record_metadata=True,       # 记录请求/响应元数据
    propagate_context=True,     # 传播追踪上下文
    sensitive_keys=["authorization", "x-api-key"]  # 敏感键脱敏
)

# 添加到 gRPC 客户端
client = GrpcClient("localhost:50051")
client.add_interceptor(grpc_tracing)

# 所有 gRPC 调用自动追踪
response = client.call(
    service="UserService",
    method="GetUser",
    request={"user_id": 123}
)
```

### gRPC 追踪属性

GrpcTracingInterceptor 自动记录：

| 属性 | 说明 |
|------|------|
| `rpc.system` | "grpc" |
| `rpc.service` | 服务名称（如 "UserService"） |
| `rpc.method` | 方法名称（如 "GetUser"） |
| `rpc.grpc.full_method` | 完整方法路径（如 "/package.UserService/GetUser"） |
| `rpc.grpc.status_code` | gRPC 状态码（0=OK） |
| `rpc.request.duration_ms` | 调用耗时 |
| `rpc.request.metadata.*` | 请求元数据（可选） |
| `rpc.response.metadata.*` | 响应元数据（可选） |

### 配置选项

```python
GrpcTracingInterceptor(
    record_metadata=False,      # 是否记录元数据（默认 False）
    propagate_context=True,     # 是否传播追踪上下文（默认 True）
    sensitive_keys=[            # 敏感键列表（自动脱敏）
        "authorization",
        "x-api-key",
        "x-auth-token",
        "cookie",
    ]
)
```

### 与 HTTP 追踪配合使用

同时追踪 HTTP 和 gRPC 请求：

```python
from df_test_framework.infrastructure.tracing.interceptors import (
    TracingInterceptor,       # HTTP 追踪
    GrpcTracingInterceptor,   # gRPC 追踪
)

# HTTP 客户端
http_client.interceptor_chain.add(TracingInterceptor())

# gRPC 客户端
grpc_client.add_interceptor(GrpcTracingInterceptor())

# 在同一个测试中，两种协议的调用都会被追踪
# 并且共享相同的 trace context
```

## 数据库查询追踪

### 使用 TracedDatabase

包装现有数据库实例：

```python
from df_test_framework.databases import Database
from df_test_framework.infrastructure.tracing.integrations import TracedDatabase

# 原始数据库
db = Database("mysql+pymysql://user:pass@localhost/testdb")

# 包装为追踪数据库
traced_db = TracedDatabase(
    db,
    record_statement=True,    # 记录 SQL 语句
)

# 所有操作自动追踪
result = traced_db.query_one("SELECT * FROM users WHERE id = 1")
traced_db.insert("users", {"name": "Bob"})
```

### 使用 DatabaseTracer

更细粒度的控制：

```python
from df_test_framework.infrastructure.tracing.integrations import DatabaseTracer

tracer = DatabaseTracer(
    db_system="mysql",
    db_name="testdb",
    server_address="localhost",
    server_port=3306
)

# 追踪单个查询
with tracer.trace_query("SELECT", "users", "SELECT * FROM users") as span:
    result = db.query_all("SELECT * FROM users")
    tracer.record_row_count(span, len(result))

# 追踪事务
with tracer.trace_transaction("create_order"):
    db.insert("orders", {"user_id": 1, "amount": 100})
    db.insert("order_items", {"order_id": 1, "product_id": 10})
```

### SQLAlchemy 自动仪表化

无需修改代码即可追踪 SQLAlchemy：

```python
from sqlalchemy import create_engine
from df_test_framework.infrastructure.tracing.integrations import instrument_sqlalchemy

engine = create_engine("mysql+pymysql://user:pass@localhost/db")

# 仪表化引擎
instrument_sqlalchemy(
    engine,
    record_statement=True,
    max_statement_length=1000
)

# 后续所有查询自动追踪
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM users"))
```

## 装饰器使用

### @trace_span - 同步函数

```python
from df_test_framework.infrastructure.tracing import trace_span

@trace_span("get_user")
def get_user(user_id: int):
    return {"id": user_id}

# 带属性
@trace_span("process_order", attributes={"component": "order_service"})
def process_order(order_id: int):
    return order_id

# 记录参数和返回值
@trace_span(record_args=True, record_result=True)
def calculate(a: int, b: int) -> int:
    return a + b
```

### @trace_async_span - 异步函数

```python
from df_test_framework.infrastructure.tracing import trace_async_span

@trace_async_span("fetch_user")
async def fetch_user(user_id: int):
    await asyncio.sleep(0.1)
    return {"id": user_id}

@trace_async_span(record_args=True)
async def async_calculate(a: int, b: int) -> int:
    return a + b
```

### @TraceClass - 类方法追踪

```python
from df_test_framework.infrastructure.tracing import TraceClass

@TraceClass(prefix="UserService", record_args=True)
class UserService:
    def get_user(self, user_id: int):
        return {"id": user_id}

    async def update_user(self, user_id: int, data: dict):
        return {"updated": True}

    def _helper(self):  # 私有方法不追踪
        pass

# 所有公共方法自动追踪：
# - UserService.get_user
# - UserService.update_user
```

## 上下文传播

### 注入追踪上下文

在发送请求时注入追踪信息：

```python
from df_test_framework.infrastructure.tracing import TracingContext

# 注入到 HTTP 请求头
headers = {"Content-Type": "application/json"}
TracingContext.inject(headers)
# headers 现在包含 traceparent 和 tracestate

response = requests.post(url, headers=headers, json=data)
```

### 提取追踪上下文

在接收请求时提取追踪信息：

```python
from df_test_framework.infrastructure.tracing import TracingContext

# 从 HTTP 请求头提取
ctx = TracingContext.extract(request.headers)

# 在提取的上下文中创建 Span
with TracingContext.use(ctx):
    with tracing.start_span("handle_request"):
        process_request()
```

### 使用 Baggage

传递自定义数据：

```python
from df_test_framework.infrastructure.tracing import Baggage

# 设置 Baggage
Baggage.set("user_id", "12345")
Baggage.set("tenant", "acme")

# 获取 Baggage
user_id = Baggage.get("user_id")
all_baggage = Baggage.get_all()

# 清理
Baggage.remove("user_id")
Baggage.clear()
```

### 获取追踪 ID

```python
from df_test_framework.infrastructure.tracing import TracingContext

# 获取当前追踪 ID
trace_id = TracingContext.get_trace_id()
span_id = TracingContext.get_span_id()
traceparent = TracingContext.get_trace_parent()

# 用于日志关联
logger.info(f"处理请求", extra={"trace_id": trace_id})
```

## 导出器配置

### Console（开发调试）

```python
config = TracingConfig(
    service_name="my-service",
    exporter_type=ExporterType.CONSOLE,
    batch_export=False  # 立即输出
)
```

### OTLP（推荐生产环境）

```python
config = TracingConfig(
    service_name="my-service",
    exporter_type=ExporterType.OTLP,
    endpoint="http://localhost:4317",  # gRPC 端点
    batch_export=True
)
```

### Jaeger

```python
config = TracingConfig(
    service_name="my-service",
    exporter_type=ExporterType.JAEGER,
    # 使用默认端点 localhost:6831
)
```

### Zipkin

```python
config = TracingConfig(
    service_name="my-service",
    exporter_type=ExporterType.ZIPKIN,
    endpoint="http://localhost:9411/api/v2/spans"
)
```

## 最佳实践

### 1. 服务命名规范

```python
# 好的命名
config = TracingConfig(
    service_name="order-service",
    extra_attributes={
        "service.namespace": "ecommerce",
        "service.version": "1.2.0",
        "deployment.environment": "production"
    }
)

# 避免
config = TracingConfig(service_name="my_app")  # 不具体
```

### 2. Span 命名约定

```python
# HTTP 请求：HTTP {METHOD} {PATH}
@trace_span("HTTP GET /users")

# gRPC 调用：gRPC {SERVICE}/{METHOD}
@trace_span("gRPC UserService/GetUser")

# 数据库操作：{OPERATION} {TABLE}
@trace_span("SELECT users")

# 业务操作：{动词} {名词}
@trace_span("process_order")
@trace_span("validate_payment")
```

### 3. 属性使用

```python
with tracing.start_span("process_order") as span:
    # 设置语义化属性
    span.set_attribute("order.id", order_id)
    span.set_attribute("order.amount", amount)
    span.set_attribute("customer.id", customer_id)

    # 记录事件
    span.add_event("payment_validated", {"gateway": "stripe"})

    # 避免敏感数据
    # span.set_attribute("credit_card", "1234...")  # 禁止！
```

### 4. 错误处理

```python
from opentelemetry import trace

with tracing.start_span("risky_operation") as span:
    try:
        result = do_something_risky()
    except Exception as e:
        span.record_exception(e)
        span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
        raise
```

### 5. 采样策略

```python
# 开发环境：全采样
config = TracingConfig(sample_rate=1.0)

# 生产高流量：降低采样率
config = TracingConfig(sample_rate=0.1)  # 10% 采样
```

### 6. 与日志集成

```python
import logging
from df_test_framework.infrastructure.tracing import TracingContext

class TracingLogFilter(logging.Filter):
    def filter(self, record):
        record.trace_id = TracingContext.get_trace_id() or "N/A"
        record.span_id = TracingContext.get_span_id() or "N/A"
        return True

# 日志格式
formatter = logging.Formatter(
    '%(asctime)s [%(trace_id)s] %(levelname)s - %(message)s'
)
```

## 故障排除

### OpenTelemetry 未安装

```
ImportError: OpenTelemetry追踪需要安装: pip install opentelemetry-sdk opentelemetry-api
```

解决：安装必要的包。

### 导出器未安装

```
ImportError: OTLP导出器需要安装: pip install opentelemetry-exporter-otlp
```

解决：根据需要安装对应的导出器包。

### 追踪数据未显示

1. 检查 `enabled=True`
2. 检查导出端点是否可达
3. 检查采样率 `sample_rate > 0`
4. 确保调用了 `manager.init()`

## v3.17.0 新特性：EventBus 自动集成

> ⚡ **v3.17.0** 引入了 EventBus 与 OpenTelemetry 的深度整合

### 自动注入 trace_id 和 span_id

从 v3.17.0 开始，所有 HTTP 请求事件会自动包含当前 Span 的追踪上下文：

```python
from opentelemetry import trace
from df_test_framework import EventBus, HttpRequestEndEvent

def test_auto_trace_injection():
    """v3.17.0: 事件自动包含追踪上下文"""
    bus = EventBus()
    tracer = trace.get_tracer(__name__)

    captured_events = []

    @bus.on(HttpRequestEndEvent)
    def capture_event(event):
        captured_events.append({
            "url": event.url,
            "trace_id": event.trace_id,  # ✅ 自动注入
            "span_id": event.span_id,    # ✅ 自动注入
            "correlation_id": event.correlation_id
        })

    # 在 Span 上下文中发起请求
    with tracer.start_as_current_span("test-request") as span:
        client = HttpClient(base_url="https://api.example.com", event_bus=bus)
        response = client.get("/users")

    # 验证追踪信息
    event_data = captured_events[0]
    assert event_data["trace_id"] is not None  # 32 字符十六进制
    assert event_data["span_id"] is not None   # 16 字符十六进制
    assert len(event_data["trace_id"]) == 32
    assert len(event_data["span_id"]) == 16
```

### W3C TraceContext 标准格式

v3.17.0 遵循 W3C TraceContext 规范：

```python
def test_w3c_trace_format():
    """验证 W3C TraceContext 格式"""
    bus = EventBus()
    tracer = trace.get_tracer(__name__)

    @bus.on(HttpRequestEndEvent)
    def verify_format(event):
        # trace_id: 32 字符十六进制 (128-bit)
        # 示例: 4bf92f3577b34da6a3ce929d0e0e4736
        assert event.trace_id
        assert len(event.trace_id) == 32
        assert all(c in "0123456789abcdef" for c in event.trace_id.lower())

        # span_id: 16 字符十六进制 (64-bit)
        # 示例: 00f067aa0ba902b7
        assert event.span_id
        assert len(event.span_id) == 16
        assert all(c in "0123456789abcdef" for c in event.span_id.lower())

    with tracer.start_as_current_span("w3c-test"):
        client = HttpClient(base_url="https://api.example.com", event_bus=bus)
        client.get("/users")
```

### 与 Allure 集成（v3.17.0）

结合 `allure_observer`，追踪信息会自动记录到 Allure 报告：

```python
def test_tracing_with_allure(allure_observer, http_client):
    """v3.17.0: 追踪信息自动记录到 Allure"""
    from opentelemetry import trace

    tracer = trace.get_tracer(__name__)

    with tracer.start_as_current_span("allure-traced-request") as span:
        response = http_client.get("/users")

        # ✅ Allure 报告自动包含:
        # - trace_id: 4bf92f3577b34da6a3ce929d0e0e4736
        # - span_id: 00f067aa0ba902b7
        # - 请求/响应完整详情
        # - 响应时间

    assert response.status_code == 200
```

### 分布式追踪完整示例

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from df_test_framework import EventBus, HttpClient, HttpRequestEndEvent

def test_distributed_tracing_complete():
    """v3.17.0: 完整的分布式追踪示例"""
    # 1. 配置 OpenTelemetry
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer(__name__)

    # 2. 配置 EventBus
    bus = EventBus()

    @bus.on(HttpRequestEndEvent)
    def log_trace(event):
        print(f"[{event.trace_id}:{event.span_id}] {event.method} {event.url}")
        print(f"  Correlation ID: {event.correlation_id}")
        print(f"  Status: {event.status_code}")
        print(f"  Duration: {event.duration}s")

    # 3. 在 Span 中发起请求
    with tracer.start_as_current_span("user-api-test") as parent_span:
        client = HttpClient(base_url="https://api.example.com", event_bus=bus)

        with tracer.start_as_current_span("get-users"):
            response1 = client.get("/users")

        with tracer.start_as_current_span("get-user-detail"):
            response2 = client.get("/users/1")

    # ✅ 所有请求共享同一个 trace_id
    # ✅ 每个请求有独立的 span_id
    # ✅ 完整的调用链路可在 Jaeger/Zipkin 中查看
```

### 相关文档

- [EventBus 指南](event_bus_guide.md) - 事件系统完整文档
- [最佳实践 - 事件系统](../user-guide/BEST_PRACTICES.md#11-事件系统与可观测性最佳实践)
- [调试指南 - 事件调试](../troubleshooting/debugging-guide.md#-事件系统调试)

---

## 参考资料

- [OpenTelemetry Python 文档](https://opentelemetry.io/docs/languages/python/)
- [W3C Trace Context 规范](https://www.w3.org/TR/trace-context/)
- [Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/)
- [DF Test Framework - EventBus 指南](event_bus_guide.md) (v3.17+)
