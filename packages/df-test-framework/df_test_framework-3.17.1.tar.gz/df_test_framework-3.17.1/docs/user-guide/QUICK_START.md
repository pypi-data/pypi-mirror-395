# 快速开始指南

> **预计时间**: 5分钟快速上手
> **最近更新**: 2025-12-05
> **框架版本**: v3.17.0

---

## 🎯 5分钟快速上手

跟随以下步骤，5分钟内创建并运行你的第一个测试！

### Step 1: 安装框架（30秒）

```bash
# 使用 uv（推荐）
pip install uv
uv pip install df-test-framework

# 或使用 pip
pip install df-test-framework
```

---

### Step 2: 创建项目结构（1分钟）

```bash
# 使用脚手架初始化项目
df-test init my-test-project
cd my-test-project

# 项目结构
my-test-project/
├── config.py           # 配置类
├── conftest.py         # Pytest配置
├── .env                # 环境变量
├── pytest.ini          # Pytest配置
└── tests/              # 测试目录
```

---

### Step 3: 配置环境（1分钟）

**编辑 `.env` 文件**:

```env
# 环境配置
ENV=test

# HTTP配置
HTTP__BASE_URL=https://api.example.com
HTTP__TIMEOUT=30

# 中间件配置（可选）
HTTP__SIGNATURE__ENABLED=true
HTTP__SIGNATURE__SECRET=your_secret_key
HTTP__SIGNATURE__ALGORITHM=md5

# Repository自动发现（可选）
TEST__REPOSITORY_PACKAGE=my_test_project.repositories
```

---

### Step 4: 编写第一个测试（2分钟）

**创建 `tests/test_example.py`**:

```python
"""示例测试 - 演示框架核心功能"""

import pytest
from df_test_framework import api_class, BaseAPI


# 使用 @api_class 装饰器自动注册 fixture
@api_class("user_api")
class UserAPI(BaseAPI):
    """用户 API 客户端"""

    def get_users(self):
        """获取用户列表"""
        return self.get("/users")

    def create_user(self, data):
        """创建用户"""
        return self.post("/users", json=data)


# 测试函数自动获得 user_api fixture
def test_get_users(user_api):
    """测试获取用户列表"""
    response = user_api.get_users()
    assert response.status_code == 200
    data = response.json()
    assert "users" in data


def test_create_user(user_api, cleanup):
    """测试创建用户（带数据清理）"""
    user_data = {"name": "Alice", "email": "alice@example.com"}
    response = user_api.create_user(user_data)
    assert response.status_code == 201

    # 注册清理（测试结束自动删除）
    user_id = response.json()["id"]
    cleanup.add("users", user_id)
```

---

### Step 5: 运行测试（30秒）

```bash
# 运行所有测试
pytest -v

# 运行并生成 Allure 报告
pytest --alluredir=./allure-results
allure serve ./allure-results
```

**预期输出**:

```
tests/test_example.py::test_get_users PASSED    [50%]
tests/test_example.py::test_create_user PASSED  [100%]

======================== 2 passed in 1.23s ========================
```

---

## 🚀 核心特性速览

### 1. 中间件系统（洋葱模型）

统一的请求/响应处理机制：

```python
from df_test_framework import HttpClient, SignatureMiddleware, RetryMiddleware

client = HttpClient(base_url="https://api.example.com")

# 添加签名中间件
client.use(SignatureMiddleware(secret="xxx", algorithm="md5"))

# 添加重试中间件
client.use(RetryMiddleware(max_retries=3, backoff_factor=0.5))

# 中间件执行顺序：Retry → Signature → 实际请求 → Signature → Retry
```

### 2. 事件总线（EventBus）

事件驱动架构，解耦测试逻辑：

```python
from df_test_framework import EventBus, HttpRequestEndEvent

bus = EventBus()

# 订阅 HTTP 请求结束事件
@bus.on(HttpRequestEndEvent)
async def log_slow_requests(event):
    if event.duration > 5.0:
        print(f"慢请求: {event.url} 耗时 {event.duration:.2f}s")

# HttpClient 自动发布事件
client = HttpClient(base_url="...", event_bus=bus)
response = client.get("/api")  # 自动触发事件
```

### 3. 测试数据清理

自动清理测试数据，保持环境干净：

```python
from df_test_framework import DataGenerator

def test_create_order(http_client, cleanup):
    # 生成测试标识符
    order_no = DataGenerator.test_id("ORD")

    # 创建订单
    response = http_client.post("/orders", json={"order_no": order_no})

    # 注册清理（测试结束自动删除）
    cleanup.add("orders", order_no)

    assert response.status_code == 201
    # 测试结束后自动调用 DELETE /orders/{order_no}
```

### 4. Allure 深度整合

所有 HTTP 请求自动记录到 Allure 报告：

```python
# 无需任何额外代码，所有请求自动记录
def test_api(http_client):
    response = http_client.get("/users")
    # ✅ 自动记录到 Allure:
    #    - 请求方法、URL、Headers
    #    - 请求体、响应体
    #    - OpenTelemetry trace_id/span_id
    #    - 响应时间、状态码
```

### 5. API 自动发现

使用 `@api_class` 装饰器，自动注册 fixture：

```python
from df_test_framework import api_class, BaseAPI

@api_class("order_api", scope="session")
class OrderAPI(BaseAPI):
    def create_order(self, data):
        return self.post("/orders", json=data)

    def get_order(self, order_id):
        return self.get(f"/orders/{order_id}")

# 测试中自动可用
def test_orders(order_api):  # 自动注入 fixture
    response = order_api.create_order({"item": "book"})
    assert response.status_code == 201
```

### 6. OpenTelemetry 追踪整合

自动注入追踪上下文到事件和 Allure 报告：

```python
# 框架自动从当前 Span 提取 trace_id/span_id
# 无需手动配置，开箱即用
def test_with_tracing(http_client):
    response = http_client.get("/users")
    # ✅ 事件自动包含 trace_id/span_id
    # ✅ Allure 报告自动显示追踪链路
```

---

## 📚 下一步

### 深入学习

| 主题 | 文档 | 说明 |
|------|------|------|
| 中间件系统 | [middleware_guide.md](../guides/middleware_guide.md) | 600+行，50+示例 |
| 事件总线 | [event_bus_guide.md](../guides/event_bus_guide.md) | 发布/订阅模式 |
| 数据清理 | [test_data_cleanup.md](../guides/test_data_cleanup.md) | CleanupManager 使用 |
| 异步 HTTP | [async_http_client.md](../guides/async_http_client.md) | 性能提升 40 倍 |
| 代码生成 | [code-generation.md](code-generation.md) | 自动生成测试/Builder |
| 最佳实践 | [BEST_PRACTICES.md](BEST_PRACTICES.md) | 规范和技巧 |
| 完整手册 | [USER_MANUAL.md](USER_MANUAL.md) | 完整功能参考 |

### 常见任务速查

**添加签名中间件**:
```python
from df_test_framework import SignatureMiddleware

client.use(SignatureMiddleware(
    secret="your_secret",
    algorithm="md5",  # 或 "sha256", "hmac-sha256"
    header_name="X-Sign"
))
```

**添加重试中间件**:
```python
from df_test_framework import RetryMiddleware

client.use(RetryMiddleware(
    max_retries=3,
    backoff_factor=0.5,
    retry_on_status=[500, 502, 503, 504]
))
```

**启用 HTTP 调试**:
```python
from df_test_framework.testing.debugging import enable_http_debug

enable_http_debug()  # 显示所有 HTTP 请求详情
```

**订阅数据库慢查询**:
```python
from df_test_framework import EventBus, DatabaseQueryEndEvent

@bus.on(DatabaseQueryEndEvent)
async def log_slow_queries(event):
    if event.duration > 1.0:
        print(f"⚠️ 慢查询: {event.sql} ({event.duration:.2f}s)")
```

**并发请求（异步）**:
```python
import asyncio
from df_test_framework import AsyncHttpClient

async def test_concurrent_requests(async_http_client):
    # 并发发送 100 个请求
    tasks = [
        async_http_client.get(f"/users/{i}")
        for i in range(100)
    ]
    responses = await asyncio.gather(*tasks)
    assert all(r.status_code == 200 for r in responses)
```

---

## 🎓 最佳实践

### 1. 使用中间件处理横切关注点

```python
# ✅ 推荐：使用中间件统一处理
client.use(LoggingMiddleware())      # 日志
client.use(RetryMiddleware())        # 重试
client.use(SignatureMiddleware())    # 签名
client.use(TimeoutMiddleware())      # 超时

# ❌ 不推荐：在业务代码中手动处理
# def api_call():
#     try:
#         response = requests.get(url, timeout=30)
#         if response.status_code == 500:
#             retry()
#         add_signature(response)
#     except Timeout:
#         handle_timeout()
```

### 2. 中间件优先级

```python
# 数字越小越先执行（外层）
client.use(RetryMiddleware(priority=5))       # 最外层
client.use(SignatureMiddleware(priority=10))  # 中间层
client.use(LoggingMiddleware(priority=100))   # 最内层

# 执行顺序：Retry → Signature → Logging → 实际请求 → Logging → Signature → Retry
```

### 3. 使用 @api_class 减少样板代码

```python
# ✅ 推荐：自动注册
@api_class("user_api")
class UserAPI(BaseAPI):
    pass

# ❌ 旧方式：手动创建 fixture
# @pytest.fixture
# def user_api(http_client):
#     return UserAPI(http_client)
```

### 4. 配置化优于硬编码

```python
# ✅ 推荐：从配置读取
# .env: HTTP__SIGNATURE__SECRET=xxx
client = HttpClient(base_url=settings.http.base_url)
if settings.http.signature.enabled:
    client.use(SignatureMiddleware(secret=settings.http.signature.secret))

# ❌ 不推荐：硬编码
# client.use(SignatureMiddleware(secret="hardcoded_secret"))
```

### 5. 使用测试数据清理

```python
# ✅ 推荐：注册清理
def test_create_user(http_client, cleanup):
    user = create_user()
    cleanup.add("users", user.id)  # 自动清理

# ❌ 不推荐：手动清理（容易遗漏）
# def test_create_user(http_client):
#     user = create_user()
#     try:
#         # ... 测试逻辑
#     finally:
#         delete_user(user.id)
```

---

## ❓ 常见问题

### Q: 如何启用 EventBus？

**A**: 将 `event_bus` 参数传递给客户端：

```python
from df_test_framework import EventBus, HttpClient

bus = EventBus()
client = HttpClient(base_url="...", event_bus=bus)

# 订阅事件
@bus.on(HttpRequestEndEvent)
async def handler(event):
    print(f"请求完成: {event.url}")
```

**或使用 fixture**（自动启用 Allure 集成）：

```python
def test_api(allure_observer, http_client):
    response = http_client.get("/users")
    # ✅ 自动记录到 Allure 报告
```

### Q: 如何查看所有 HTTP 请求详情？

**A**: 使用 HTTP 调试器：

```python
from df_test_framework.testing.debugging import enable_http_debug

enable_http_debug()  # 显示所有请求/响应详情

def test_api(http_client):
    response = http_client.get("/users")
    # 终端会显示完整的请求/响应
```

### Q: 如何保留测试数据用于调试？

**A**: 使用 `--keep-test-data` 参数：

```bash
# 保留测试数据，不自动清理
pytest --keep-test-data

# 或设置环境变量
KEEP_TEST_DATA=true pytest
```

### Q: 如何并发执行多个请求？

**A**: 使用 `AsyncHttpClient`：

```python
import asyncio
from df_test_framework import AsyncHttpClient

async def test_concurrent(async_http_client):
    tasks = [
        async_http_client.get(f"/users/{i}")
        for i in range(100)
    ]
    responses = await asyncio.gather(*tasks)
    # 性能提升 40 倍
```

### Q: 事件关联（correlation_id）如何使用？

**A**: 框架自动关联 Start/End 事件：

```python
# 框架自动生成 correlation_id 关联事件对
# 无需手动配置

@bus.on(HttpRequestStartEvent)
def on_start(event):
    print(f"请求开始: {event.correlation_id}")

@bus.on(HttpRequestEndEvent)
def on_end(event):
    print(f"请求结束: {event.correlation_id}")
    # Start 和 End 事件的 correlation_id 相同
```

---

## 📞 获取帮助

- **核心文档导航**: [ESSENTIAL_DOCS.md](../ESSENTIAL_DOCS.md)
- **快速参考**: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- **完整文档**: [docs/](../README.md)
- **示例代码**: [examples/](../../examples/)
- **Issues**: [GitHub Issues](https://github.com/your-org/df-test-framework/issues)

---

## 🎉 恭喜！

你已经完成了快速上手！

**推荐下一步**:
1. 📖 阅读 [核心文档导航](../ESSENTIAL_DOCS.md) - 只看最有价值的文档
2. 🔍 查看 [快速参考](QUICK_REFERENCE.md) - 常用命令速查
3. 🚀 探索 [中间件使用指南](../guides/middleware_guide.md) - 600+行完整示例
4. 📚 学习 [最佳实践](BEST_PRACTICES.md) - 规范和技巧
