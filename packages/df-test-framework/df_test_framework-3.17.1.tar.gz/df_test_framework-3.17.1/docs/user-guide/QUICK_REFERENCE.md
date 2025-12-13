# DF Test Framework - 快速参考

> **版本**: v3.17.0 | **更新**: 2025-12-05

---

## 🚀 快速开始

```bash
# 创建项目
df-test init my-project

# 配置环境
cp .env.example .env && vim .env

# 运行测试
pytest -v
```

---

## 📦 核心导入

```python
# HTTP 客户端
from df_test_framework import (
    HttpClient,             # 同步 HTTP 客户端
    AsyncHttpClient,        # 异步 HTTP 客户端（v3.8+）
    BaseAPI,                # API 基类
    api_class,              # API 装饰器（v3.14+）
)

# 中间件（v3.14+）
from df_test_framework import (
    SignatureMiddleware,    # 签名认证
    RetryMiddleware,        # 重试
    TimeoutMiddleware,      # 超时
    LoggingMiddleware,      # 日志
    BearerTokenMiddleware,  # Bearer Token
)

# 事件系统（v3.14+）
from df_test_framework import (
    EventBus,               # 事件总线
    HttpRequestStartEvent,  # HTTP 请求开始事件
    HttpRequestEndEvent,    # HTTP 请求结束事件
)

# 数据库
from df_test_framework import (
    Database,               # 数据库客户端
    BaseRepository,         # Repository 基类
    UnitOfWork,             # UoW 模式（v3.7+）
    RedisClient,            # Redis 客户端
)

# 测试数据
from df_test_framework import (
    DataGenerator,          # 数据生成器
    CleanupManager,         # 清理管理器（v3.11+）
)

# 设计模式
from df_test_framework import (
    BaseBuilder,            # Builder 基类
    DictBuilder,            # 字典 Builder
)

# 测试支持
from df_test_framework.testing.plugins import (
    step,                   # Allure 步骤
    attach_json,            # 附加 JSON
    attach_log,             # 附加日志
)

# 调试工具
from df_test_framework.testing.debugging import (
    enable_http_debug,      # HTTP 调试
    enable_db_debug,        # 数据库调试
)
```

---

## 🌐 HTTP 客户端

### 基础用法

```python
def test_http(http_client):
    # GET
    response = http_client.get("/users/1")

    # POST
    response = http_client.post("/users", json={"name": "张三"})

    # PUT
    response = http_client.put("/users/1", json={"name": "李四"})

    # DELETE
    response = http_client.delete("/users/1")

    # 带参数和请求头
    response = http_client.get(
        "/users",
        params={"page": 1, "size": 10},
        headers={"Authorization": "Bearer token"}
    )
```

### 使用中间件（v3.14+）

```python
from df_test_framework import SignatureMiddleware, RetryMiddleware

client = HttpClient(base_url="https://api.example.com")

# 添加签名中间件
client.use(SignatureMiddleware(
    secret="your_secret",
    algorithm="md5",
    header_name="X-Sign"
))

# 添加重试中间件
client.use(RetryMiddleware(
    max_retries=3,
    backoff_factor=0.5
))
```

### 封装 API 客户端（v3.14+）

```python
from df_test_framework import api_class, BaseAPI

@api_class("user_api", scope="session")
class UserAPI(BaseAPI):
    """用户 API 客户端

    @api_class 装饰器自动注册为 pytest fixture
    """

    def get_user(self, user_id: str):
        return self.get(f"/users/{user_id}")

    def create_user(self, data: dict):
        return self.post("/users", json=data)

# 测试中自动注入
def test_user(user_api):
    response = user_api.get_user("1")
    assert response.status_code == 200
```

### 异步 HTTP（v3.8+）

```python
import asyncio
from df_test_framework import AsyncHttpClient

async def test_async_http(async_http_client):
    # 并发请求（性能提升 40 倍）
    tasks = [
        async_http_client.get(f"/users/{i}")
        for i in range(100)
    ]
    responses = await asyncio.gather(*tasks)
    assert all(r.status_code == 200 for r in responses)
```

---

## 💾 数据库操作

### 直接使用 Database

```python
def test_db(database):
    # 查询单条
    user = database.query_one(
        "SELECT * FROM users WHERE id = :id",
        {"id": 1}
    )

    # 查询多条
    users = database.query_all(
        "SELECT * FROM users WHERE status = :status",
        {"status": "ACTIVE"}
    )

    # 插入
    user_id = database.insert("users", {
        "username": "test_user",
        "email": "test@example.com"
    })

    # 更新
    database.update("users", user_id, {"status": "INACTIVE"})

    # 删除
    database.delete("users", {"id": user_id})
```

### Unit of Work 模式（v3.7+，推荐）

```python
# uow.py - 定义 UoW
from df_test_framework import UnitOfWork

class ProjectUoW(UnitOfWork):
    @property
    def users(self):
        return UserRepository(self._session)

    @property
    def orders(self):
        return OrderRepository(self._session)

# conftest.py - 注册 fixture
@pytest.fixture
def uow(database):
    with ProjectUoW(database.engine) as uow:
        yield uow
        # 测试结束后自动回滚

# 测试中使用
def test_with_uow(user_api, uow):
    # 调用 API 创建用户
    result = user_api.create_user({"username": "test"})

    # 使用 UoW 验证数据库
    user = uow.users.find_by_id(result["user_id"])
    assert user is not None

    # ✅ 测试结束后自动回滚
```

---

## 🧹 测试数据清理（v3.11+）

### 使用 CleanupManager

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

### 保留数据调试

```bash
# 保留测试数据，不自动清理
pytest --keep-test-data

# 或设置环境变量
KEEP_TEST_DATA=true pytest
```

---

## 🎲 Redis 操作

```python
def test_redis(redis_client):
    # 字符串
    redis_client.set("key", "value", ex=60)
    value = redis_client.get("key")

    # 哈希
    redis_client.hset("user:1", "name", "张三")
    name = redis_client.hget("user:1", "name")
    user = redis_client.hgetall("user:1")

    # 列表
    redis_client.lpush("queue", "item1")
    items = redis_client.lrange("queue", 0, -1)

    # 集合
    redis_client.sadd("tags", "python", "testing")
    tags = redis_client.smembers("tags")
```

---

## 📡 事件系统（v3.14+）

### 订阅 HTTP 事件

```python
from df_test_framework import EventBus, HttpRequestEndEvent

bus = EventBus()

# 订阅请求结束事件
@bus.on(HttpRequestEndEvent)
def log_slow_requests(event):
    if event.duration > 1.0:
        print(f"⚠️ 慢请求: {event.url} - {event.duration}s")

# HttpClient 自动发布事件
client = HttpClient(base_url="...", event_bus=bus)
response = client.get("/users")
```

### Allure 自动集成（v3.17+）

```python
# 使用 allure_observer fixture，自动记录所有 HTTP 请求
def test_api(allure_observer, http_client):
    response = http_client.get("/users")
    # ✅ 自动记录到 Allure 报告:
    #    - 请求方法、URL、Headers、Body
    #    - 响应状态码、Headers、Body
    #    - OpenTelemetry trace_id/span_id
    #    - 响应时间
```

---

## 🧪 Pytest Fixtures

### 框架提供

| Fixture | 说明 | 作用域 | 版本 |
|---------|------|--------|------|
| `http_client` | HTTP 客户端 | session | v3.0+ |
| `async_http_client` | 异步 HTTP 客户端 | session | v3.8+ |
| `database` | 数据库客户端 | session | v3.0+ |
| `redis_client` | Redis 客户端 | session | v3.0+ |
| `cleanup` | 数据清理管理器 | function | v3.11+ |
| `allure_observer` | Allure 观察器 | function | v3.17+ |
| `event_bus` | 事件总线 | session | v3.14+ |

### 自定义 Fixtures

```python
# conftest.py

# API 客户端（使用 @api_class 更简单）
@pytest.fixture
def user_api(http_client):
    from apis import UserAPI
    return UserAPI(http_client)

# UoW
@pytest.fixture
def uow(database):
    from your_project.uow import ProjectUoW
    with ProjectUoW(database.engine) as uow:
        yield uow

# 测试数据
@pytest.fixture
def test_user_data():
    return {"username": "test", "email": "test@example.com"}
```

---

## 📊 Allure 报告

```python
import allure
from df_test_framework.testing.plugins import step, attach_json

@allure.feature("用户管理")
@allure.story("用户创建")
class TestUserCreation:

    @allure.title("测试创建用户成功")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_create_user(self, user_api):
        """测试创建用户"""

        with step("准备测试数据"):
            user_data = {"username": "test"}
            attach_json(user_data, name="请求数据")

        with step("调用 API"):
            result = user_api.create_user(user_data)
            attach_json(result, name="响应数据")

        with step("验证结果"):
            assert result["username"] == "test"
```

---

## 🔍 调试

```python
# HTTP 调试（显示所有请求/响应详情）
from df_test_framework.testing.debugging import enable_http_debug

def test_debug(http_client):
    enable_http_debug()
    response = http_client.get("/users/1")
    # 终端会显示完整的请求/响应详情

# 数据库调试（显示所有 SQL 查询）
from df_test_framework.testing.debugging import enable_db_debug

def test_db_debug(database):
    enable_db_debug()
    user = database.query_one("SELECT * FROM users WHERE id = 1")
    # 终端会显示 SQL 和执行时间

# 日志
from loguru import logger

logger.info("信息日志")
logger.debug("调试日志")
logger.warning("警告日志")
logger.error("错误日志")
```

---

## ⚡ 常用命令

```bash
# 运行所有测试
pytest -v

# 运行指定文件
pytest tests/api/test_user.py

# 运行指定测试
pytest tests/api/test_user.py::TestUser::test_create_user

# 运行标记
pytest -m smoke

# 并行运行
pytest -n auto

# 显示打印
pytest -s

# 失败时停止
pytest -x

# 重新运行失败的测试
pytest --lf

# 生成 Allure 报告
pytest --alluredir=allure-results
allure serve allure-results

# 生成 HTML 报告
pytest --html=report.html --self-contained-html

# 覆盖率
pytest --cov=src --cov-report=html

# 保留测试数据（不自动清理）
pytest --keep-test-data
```

---

## 🏷️ Pytest 标记

```python
# 定义标记（pytest.ini 或 conftest.py）
def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: 冒烟测试")
    config.addinivalue_line("markers", "p0: P0 优先级")
    config.addinivalue_line("markers", "slow: 慢速测试")

# 使用标记
@pytest.mark.smoke
@pytest.mark.p0
def test_critical():
    pass

# 运行特定标记
# pytest -m smoke
# pytest -m "p0 or p1"
# pytest -m "smoke and not slow"
```

---

## ⚙️ 环境配置

**.env**:

```env
# 环境
ENV=test

# HTTP 配置
HTTP__BASE_URL=https://api.example.com
HTTP__TIMEOUT=30

# 中间件配置
HTTP__SIGNATURE__ENABLED=true
HTTP__SIGNATURE__SECRET=your_secret_key
HTTP__SIGNATURE__ALGORITHM=md5

# 数据库配置
DATABASE__URL=mysql+pymysql://user:pass@localhost:3306/testdb

# Redis 配置
REDIS__HOST=localhost
REDIS__PORT=6379

# 测试配置
TEST__REPOSITORY_PACKAGE=my_project.repositories
TEST__KEEP_DATA=false
```

---

## 📂 推荐项目结构

```
my-project/
├── apis/
│   ├── base.py              # API 基类
│   └── user_api.py          # 用户 API
├── repositories/
│   └── user_repo.py         # 用户 Repository
├── builders/
│   └── user_builder.py      # 用户 Builder
├── uow.py                   # Unit of Work
├── tests/
│   ├── conftest.py          # Pytest 配置
│   ├── api/
│   │   └── test_user.py     # API 测试
│   └── integration/
│       └── test_workflow.py # 集成测试
├── .env                     # 环境变量
├── pytest.ini               # Pytest 配置
└── pyproject.toml           # 项目配置
```

---

## 🆕 版本特性速查

| 版本 | 核心特性 |
|------|---------|
| **v3.17.0** | 事件关联（correlation_id）、OpenTelemetry 整合、Allure 深度集成 |
| **v3.16.0** | Layer 4 Bootstrap 架构、五层架构完善 |
| **v3.14.0** | 中间件系统、EventBus、可观测性融合 |
| **v3.11.0** | 测试数据清理模块（CleanupManager） |
| **v3.8.0** | AsyncHttpClient（性能提升 40 倍） |
| **v3.7.0** | Unit of Work 模式 |

---

## 🔗 相关链接

- [快速开始](QUICK_START.md) - 5 分钟上手
- [核心文档导航](../ESSENTIAL_DOCS.md) - 最有价值的文档
- [中间件指南](../guides/middleware_guide.md) - 600+行完整示例
- [EventBus 指南](../guides/event_bus_guide.md) - 事件驱动架构
- [最佳实践](BEST_PRACTICES.md) - 规范和技巧
- [完整手册](USER_MANUAL.md) - 全面的功能参考

---

**快速查询完毕！开始编写测试吧 🚀**
