# v3.14.0 快速开始指南

> **框架版本**: df-test-framework v3.14.0
> **预计时间**: 5分钟快速上手
> **更新日期**: 2025-12-04

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

# v3.14.0: 中间件配置（可选）
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
"""示例测试 - 演示 v3.14.0 新特性"""

import pytest
from df_test_framework import api_class, BaseAPI


# v3.14.0: 使用 @api_class 装饰器自动注册 fixture
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


def test_create_user(user_api):
    """测试创建用户"""
    user_data = {"name": "Alice", "email": "alice@example.com"}
    response = user_api.create_user(user_data)
    assert response.status_code == 201
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

## 🆕 v3.14.0 新特性速览

### 1. 中间件系统（洋葱模型）

**旧版（v3.13）**:
```python
# ❌ 旧的 Middleware 系统
from df_test_framework.clients.http.middlewares import SignatureMiddleware

client = HttpClient(
    base_url="https://api.example.com",
    middlewares=[SignatureMiddleware(secret="xxx")]
)
```

**新版（v3.14）**:
```python
# ✅ 新的 Middleware 系统
from df_test_framework import HttpClient, SignatureMiddleware

client = HttpClient(base_url="https://api.example.com")
client.use(SignatureMiddleware(secret="xxx", algorithm="md5"))

# 或在构造时传入
client = HttpClient(
    base_url="https://api.example.com",
    middlewares=[SignatureMiddleware(secret="xxx")]
)
```

### 2. 事件总线（EventBus）

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

### 3. 可观测性集成（Telemetry）

```python
from df_test_framework import Telemetry

telemetry = Telemetry(logger=logger)

# 自动记录 Trace + Metrics + Logs
async with telemetry.span("api.call") as span:
    response = await client.get("/api")
    span.set_attribute("status_code", response.status_code)

# 一行代码，三种可观测性数据：
# - Trace Span（包含 duration、attributes）
# - Metrics（histogram、counter）
# - Logs（structured logging）
```

### 4. API 自动发现（@api_class）

```python
from df_test_framework import api_class, BaseAPI

@api_class("order_api", scope="session")
class OrderAPI(BaseAPI):
    def create_order(self, data):
        return self.post("/orders", json=data)

# 测试中自动可用
def test_orders(order_api):  # 自动注入 fixture
    response = order_api.create_order({"item": "book"})
    assert response.status_code == 201
```

### 5. Repository 自动发现

**配置（`.env`）**:
```env
TEST__REPOSITORY_PACKAGE=my_project.repositories
```

**使用**:
```python
def test_database(uow):
    # uow.users, uow.orders 自动可用（无需手动注册）
    user = uow.users.create({"name": "Alice"})
    order = uow.orders.create({"user_id": user.id})
    uow.commit()
```

---

## 📚 下一步

### 深入学习

| 主题 | 文档 |
|------|------|
| 中间件系统 | [middleware_guide.md](../guides/middleware_guide.md) |
| 事件总线 | [event_bus_guide.md](../guides/event_bus_guide.md) |
| 可观测性 | [telemetry_guide.md](../guides/telemetry_guide.md) |
| 迁移指南 | [v3.13-to-v3.14.md](../migration/v3.13-to-v3.14.md) |
| 完整手册 | [USER_MANUAL.md](USER_MANUAL.md) |

### 常见任务

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
    backoff_factor=0.5
))
```

**启用 Allure 自动记录**:
```python
# pytest.ini
[pytest]
df_plugins = df_test_framework.plugins.builtin.reporting.allure_plugin.AllurePlugin

# 所有 HTTP 请求和数据库查询自动记录到 Allure 报告
```

**数据库事件订阅**:
```python
from df_test_framework import EventBus, DatabaseQueryEndEvent

@bus.on(DatabaseQueryEndEvent)
async def log_slow_queries(event):
    if event.duration > 1.0:
        logger.warning(f"慢查询: {event.sql} ({event.duration:.2f}s)")
```

---

## 🎓 最佳实践

### 1. 使用中间件而非中间件

```python
# ✅ 推荐：新的 Middleware 系统
client.use(LoggingMiddleware())
client.use(RetryMiddleware())
client.use(SignatureMiddleware(secret="xxx"))

# ❌ 废弃：旧的 Middleware（v3.16.0 将移除）
# client.add_middleware(LoggingMiddleware())
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

---

## ❓ 常见问题

### Q: v3.14.0 与 v3.13 兼容吗？

**A**: 完全向后兼容。旧 API 仍可使用，但会触发 DeprecationWarning。

```python
# ✅ 旧代码仍能运行
from df_test_framework.clients.http.middlewares import SignatureMiddleware
# ⚠️ 但会看到：DeprecationWarning: middlewares 模块已废弃
```

### Q: 如何从 v3.13 迁移？

**A**: 查看迁移指南 [v3.13-to-v3.14.md](../migration/v3.13-to-v3.14.md)

**快速迁移**:
1. 导入路径：`middlewares` → `middleware`
2. 类重命名：`Middleware` → `Middleware`
3. 优先级反转：`priority=100`（先执行） → `priority=10`（先执行）

### Q: Middleware 和 Middleware 有什么区别？

**A**:
- **Middleware**: before/after 分离，状态共享困难
- **Middleware**: 洋葱模型，before/after 在同一作用域，自然共享状态

```python
# Middleware：自然共享 start_time
class TimingMiddleware(BaseMiddleware):
    async def __call__(self, request, call_next):
        start = time.time()  # before
        response = await call_next(request)
        duration = time.time() - start  # after，直接访问 start
        print(f"耗时: {duration}s")
        return response
```

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

---

## 📞 获取帮助

- **文档**: [docs/](../README.md)
- **示例**: [examples/](../examples.md)
- **Issues**: [GitHub Issues](https://github.com/your-org/df-test-framework/issues)
- **迁移指南**: [v3.13-to-v3.14.md](../migration/v3.13-to-v3.14.md)

---

## 🎉 恭喜！

你已经完成了 v3.14.0 的快速上手！

**推荐下一步**:
1. 📖 阅读 [中间件使用指南](../guides/middleware_guide.md)
2. 🔍 探索 [最佳实践](BEST_PRACTICES.md)
3. 🚀 尝试 [高级功能](USER_MANUAL.md)
