# EventBus 使用指南

> **版本要求**: df-test-framework >= 3.14.0
> **更新日期**: 2025-12-05
> **最新版本**: v3.17.0

---

## 概述

EventBus 是 v3.14.0 引入的**发布/订阅**事件系统，用于解耦组件间的通信。

**核心优势**:
- ✅ 解耦：组件间无需直接依赖
- ✅ 可扩展：新增订阅者不影响发布者
- ✅ 异步：支持异步事件处理
- ✅ 类型安全：基于事件类的订阅

**v3.17.0 新特性** ⚡:
- ✨ 事件关联（correlation_id）- 关联 Start/End 事件对
- ✨ OpenTelemetry 整合 - 自动注入 trace_id/span_id
- ✨ 测试隔离 - 每个测试独立的 EventBus 实例
- ✨ Allure 深度整合 - AllureObserver 自动记录所有请求

---

## 快速开始

### 1. 基本用法

```python
from df_test_framework import EventBus, HttpRequestEndEvent

# 创建事件总线
bus = EventBus()

# 订阅事件
@bus.on(HttpRequestEndEvent)
async def log_request(event: HttpRequestEndEvent):
    print(f"请求完成: {event.method} {event.url} - {event.status_code}")

# 集成到 HttpClient
from df_test_framework import HttpClient

client = HttpClient(
    base_url="https://api.example.com",
    event_bus=bus  # 传入 event_bus
)

# 发送请求（自动触发事件）
response = client.request_with_middleware("GET", "/users")
# 输出: 请求完成: GET https://api.example.com/users - 200
```

### 2. 订阅多个事件

```python
from df_test_framework import (
    EventBus,
    HttpRequestEndEvent,
    DatabaseQueryEndEvent
)

bus = EventBus()

# HTTP 事件
@bus.on(HttpRequestEndEvent)
async def log_http(event):
    print(f"HTTP: {event.url} - {event.duration:.2f}s")

# 数据库事件
@bus.on(DatabaseQueryEndEvent)
async def log_db(event):
    print(f"SQL: {event.sql} ({event.row_count} rows, {event.duration:.2f}s)")

# 集成到多个客户端
from df_test_framework import Database

http_client = HttpClient(base_url="...", event_bus=bus)
database = Database(config, event_bus=bus)

# 所有操作自动触发事件
http_client.request_with_middleware("GET", "/api")
database.execute("SELECT * FROM users")
```

---

## 框架内置事件

### HTTP 事件

```python
from df_test_framework.core.events import (
    HttpRequestStartEvent,  # 请求开始
    HttpRequestEndEvent,    # 请求结束
    HttpRequestErrorEvent,  # 请求错误
)

@bus.on(HttpRequestEndEvent)
async def on_http_end(event):
    print(f"Method: {event.method}")
    print(f"URL: {event.url}")
    print(f"Status: {event.status_code}")
    print(f"Duration: {event.duration}s")
    print(f"Timestamp: {event.timestamp}")
```

### 数据库事件

```python
from df_test_framework.core.events import (
    DatabaseQueryStartEvent,  # 查询开始
    DatabaseQueryEndEvent,    # 查询结束
)

@bus.on(DatabaseQueryEndEvent)
async def on_query_end(event):
    print(f"SQL: {event.sql}")
    print(f"Params: {event.params}")
    print(f"Row Count: {event.row_count}")
    print(f"Duration: {event.duration}s")
```

### 消息队列事件

```python
from df_test_framework.core.events import (
    MessagePublishEvent,  # 消息发布
    MessageConsumeEvent,  # 消息消费
)

@bus.on(MessagePublishEvent)
async def on_message_publish(event):
    print(f"Topic: {event.topic}")
    print(f"Message: {event.message}")
    print(f"Queue Type: {event.queue_type}")  # kafka/rabbitmq/rocketmq
```

---

## 实用场景

### 场景 1: 慢请求告警

```python
@bus.on(HttpRequestEndEvent)
async def alert_slow_requests(event):
    if event.duration > 5.0:
        # 发送告警
        print(f"⚠️ 慢请求: {event.url} 耗时 {event.duration:.2f}s")
        # 可以调用告警接口、发送邮件等
```

### 场景 2: 请求统计

```python
from collections import defaultdict

stats = defaultdict(int)

@bus.on(HttpRequestEndEvent)
async def collect_stats(event):
    stats[event.method] += 1
    stats["total"] += 1

    if stats["total"] % 10 == 0:
        print(f"统计: {dict(stats)}")
```

### 场景 3: 自动重试记录

```python
@bus.on(HttpRequestErrorEvent)
async def log_errors(event):
    print(f"❌ 请求失败: {event.url}")
    print(f"   错误: {event.error}")
    print(f"   重试次数: {event.retry_count}")
```

### 场景 4: 慢 SQL 优化提示

```python
@bus.on(DatabaseQueryEndEvent)
async def optimize_slow_queries(event):
    if event.duration > 1.0:
        print(f"🐌 慢查询: {event.sql}")
        print(f"   耗时: {event.duration:.2f}s")
        print(f"   建议: 添加索引或优化查询")
```

### 场景 5: Allure 自动记录

```python
import allure

@bus.on(HttpRequestEndEvent)
async def record_to_allure(event):
    status_emoji = "✓" if 200 <= event.status_code < 300 else "✗"
    step_name = f"{event.method} {event.url} {status_emoji} {event.status_code}"

    with allure.step(step_name):
        allure.attach(
            f"Duration: {event.duration:.3f}s\nStatus: {event.status_code}",
            name="Response Info",
            attachment_type=allure.attachment_type.TEXT
        )
```

---

## 自定义事件

### 1. 定义事件类

```python
from df_test_framework.core.events import Event
from datetime import datetime

class OrderCreatedEvent(Event):
    """订单创建事件"""

    def __init__(self, order_id: str, amount: float, user_id: int):
        super().__init__()
        self.order_id = order_id
        self.amount = amount
        self.user_id = user_id
```

### 2. 发布自定义事件

```python
# 创建并发布事件
event = OrderCreatedEvent(
    order_id="ORDER001",
    amount=100.0,
    user_id=123
)

await bus.publish(event)
```

### 3. 订阅自定义事件

```python
@bus.on(OrderCreatedEvent)
async def send_notification(event):
    print(f"新订单: {event.order_id}")
    print(f"金额: {event.amount}")
    # 发送通知...
```

---

## 高级用法

### 全局订阅（所有事件）

```python
@bus.on_all()
async def log_all_events(event):
    print(f"事件: {type(event).__name__}")
```

### 取消订阅

```python
# 订阅
handler = bus.on(HttpRequestEndEvent)(my_handler)

# 取消订阅
bus.off(HttpRequestEndEvent, my_handler)
```

### 一次性订阅

```python
@bus.once(HttpRequestEndEvent)
async def run_once(event):
    print("只执行一次")
```

---

## 最佳实践

### 1. 事件处理器保持轻量

```python
# ✅ 好：快速处理
@bus.on(HttpRequestEndEvent)
async def quick_handler(event):
    logger.info(f"Request: {event.url}")

# ❌ 差：耗时操作阻塞
# @bus.on(HttpRequestEndEvent)
# async def slow_handler(event):
#     time.sleep(10)  # 阻塞其他事件处理
```

### 2. 异常处理

```python
@bus.on(HttpRequestEndEvent)
async def safe_handler(event):
    try:
        # 处理逻辑
        process(event)
    except Exception as e:
        logger.error(f"事件处理失败: {e}")
        # 不要让异常传播，影响其他订阅者
```

### 3. 使用类型注解

```python
from df_test_framework.core.events import HttpRequestEndEvent

@bus.on(HttpRequestEndEvent)
async def typed_handler(event: HttpRequestEndEvent):
    # IDE 有类型提示
    print(event.url)  # ✅ 有提示
```

---

## v3.17.0 新特性详解

### 1. 事件关联（Event Correlation）

**问题**: 如何关联同一个请求的 Start 和 End 事件？

**解决方案**: v3.17.0 引入 `correlation_id`，自动关联事件对。

```python
from df_test_framework import EventBus, HttpRequestStartEvent, HttpRequestEndEvent

bus = EventBus()

# 记录所有请求
requests = {}

@bus.on(HttpRequestStartEvent)
def on_start(event):
    # Start 事件包含 correlation_id
    requests[event.correlation_id] = {
        "start_time": event.timestamp,
        "url": event.url
    }
    print(f"请求开始: {event.url} [cor:{event.correlation_id}]")

@bus.on(HttpRequestEndEvent)
def on_end(event):
    # End 事件的 correlation_id 与 Start 相同
    if event.correlation_id in requests:
        start_info = requests[event.correlation_id]
        duration = event.duration
        print(f"请求完成: {event.url} [cor:{event.correlation_id}]")
        print(f"  实际耗时: {duration}s")
        del requests[event.correlation_id]

# HttpClient 自动生成 correlation_id
client = HttpClient(base_url="...", event_bus=bus)
response = client.get("/users")
# 输出:
# 请求开始: /users [cor:cor-a1b2c3d4e5f6]
# 请求完成: /users [cor:cor-a1b2c3d4e5f6]
```

**工作原理**:
1. HttpClient 创建 Start 事件时生成 `correlation_id`
2. End 事件复用相同的 `correlation_id`
3. 订阅者通过 `correlation_id` 匹配事件对

### 2. OpenTelemetry 整合

**v3.17.0 自动注入追踪上下文到事件**，无需手动配置。

```python
from opentelemetry import trace
from df_test_framework import EventBus, HttpRequestEndEvent

bus = EventBus()

@bus.on(HttpRequestEndEvent)
def on_request(event):
    # v3.17.0: 事件自动包含 trace_id 和 span_id
    print(f"Trace ID: {event.trace_id}")     # 32 字符十六进制
    print(f"Span ID: {event.span_id}")       # 16 字符十六进制
    print(f"Correlation: {event.correlation_id}")  # cor-{12hex}

# 在 Span 上下文中发送请求
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("test-api-call") as span:
    client = HttpClient(base_url="...", event_bus=bus)
    response = client.get("/users")
    # 事件自动包含当前 Span 的 trace_id 和 span_id
```

**与 Allure 集成**:

```python
# v3.17.0: AllureObserver 自动提取追踪信息
def test_with_tracing(allure_observer, http_client):
    response = http_client.get("/users")
    # ✅ Allure 报告自动显示:
    #    - Trace ID: 1234567890abcdef1234567890abcdef
    #    - Span ID: 1234567890abcdef
    #    - Correlation ID: cor-a1b2c3d4e5f6
```

### 3. 测试隔离（Test Isolation）

**问题**: 并发测试时事件互相干扰。

**v3.17.0 解决方案**: 每个测试独立的 EventBus 实例。

```python
from df_test_framework.infrastructure.events import set_test_event_bus, get_event_bus

def test_isolated_events_1():
    # 创建测试专用 EventBus
    test_bus = EventBus()
    set_test_event_bus(test_bus)

    events = []

    @test_bus.on(HttpRequestEndEvent)
    def collect(event):
        events.append(event)

    # HttpClient 自动使用测试 EventBus
    client = HttpClient(base_url="...")
    client.get("/users")

    assert len(events) == 1  # ✅ 只有本测试的事件

def test_isolated_events_2():
    # 另一个测试有自己的 EventBus
    test_bus = EventBus()
    set_test_event_bus(test_bus)

    events = []

    @test_bus.on(HttpRequestEndEvent)
    def collect(event):
        events.append(event)

    client = HttpClient(base_url="...")
    client.get("/orders")

    assert len(events) == 1  # ✅ 不受其他测试影响
```

**自动清理**: 测试结束后自动清理 EventBus。

### 4. Allure 深度整合（v3.17.0）

**AllureObserver**: 自动记录所有 HTTP 请求到 Allure 报告。

```python
# 使用 allure_observer fixture（推荐）
def test_with_allure(allure_observer, http_client):
    response = http_client.get("/users")
    # ✅ 自动记录到 Allure:
    #    - 完整请求体和响应体
    #    - OpenTelemetry trace_id/span_id
    #    - 响应时间
    #    - 事件关联 ID

# 手动创建 AllureObserver
from df_test_framework.testing.reporting.allure import AllureObserver

def test_manual_observer():
    test_bus = EventBus()
    observer = AllureObserver(test_bus)

    client = HttpClient(base_url="...", event_bus=test_bus)
    response = client.get("/users")
    # 所有请求自动记录
```

**支持的协议**:
- ✅ HTTP/REST
- ✅ GraphQL（v3.11+）
- ✅ gRPC（v3.11+）

**记录内容**:
- 请求方法、URL、Headers、Body
- 响应状态码、Headers、Body（支持 gzip/deflate 解压）
- OpenTelemetry 追踪信息（trace_id, span_id）
- 事件关联 ID（correlation_id）
- 响应时间
- 错误信息（如有）

---

## 事件参考

### v3.17.0 事件字段

所有事件都包含以下字段：

```python
class Event:
    event_id: str           # v3.17.0: 事件唯一 ID (evt-{12hex})
    timestamp: datetime     # 事件时间
    trace_id: str | None    # v3.17.0: OpenTelemetry Trace ID
    span_id: str | None     # v3.17.0: OpenTelemetry Span ID
```

**可关联事件**（Start/End 配对）:

```python
class CorrelatedEvent(Event):
    correlation_id: str     # v3.17.0: 关联 ID (cor-{12hex})
```

### HTTP 事件字段

#### HttpRequestStartEvent

```python
event_id: str              # evt-a1b2c3d4e5f6
correlation_id: str        # cor-x7y8z9a1b2c3
method: str                # GET/POST/PUT/DELETE
url: str                   # https://api.example.com/users
headers: dict              # 请求头
body: Any | None           # 请求体
timestamp: datetime
trace_id: str | None       # OpenTelemetry Trace ID
span_id: str | None        # OpenTelemetry Span ID
```

#### HttpRequestEndEvent

```python
event_id: str              # evt-b2c3d4e5f6a1
correlation_id: str        # cor-x7y8z9a1b2c3 (与 Start 相同)
method: str
url: str
status_code: int
headers: dict              # 响应头
body: Any | None           # v3.17.0: 响应体
duration: float            # 耗时（秒）
timestamp: datetime
trace_id: str | None
span_id: str | None
```

---

## 版本特性对比

| 特性 | v3.14.0 | v3.17.0 |
|------|---------|---------|
| 基础发布/订阅 | ✅ | ✅ |
| 异步事件处理 | ✅ | ✅ |
| 内置事件（HTTP/DB/MQ） | ✅ | ✅ |
| 事件唯一 ID（event_id） | ❌ | ✅ |
| 事件关联（correlation_id） | ❌ | ✅ |
| OpenTelemetry 整合 | ❌ | ✅ |
| 测试隔离 | ❌ | ✅ |
| AllureObserver | ❌ | ✅ |
| 响应体记录 | ❌ | ✅ |

---

## 参考资料

- [快速开始](../user-guide/QUICK_START.md)
- [快速参考](../user-guide/QUICK_REFERENCE.md)
- [中间件使用指南](middleware_guide.md)
- [v3.17.0 发布说明](../releases/v3.17.0.md)
- [v3.17.0 架构设计](../architecture/V3.17_EVENT_SYSTEM_REDESIGN.md)
