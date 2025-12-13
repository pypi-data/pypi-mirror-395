# DF Test Framework - 使用手册

> **版本**: v3.17.0
> **更新日期**: 2025-12-05
> **目标读者**: QA工程师、测试开发工程师

---

## 📚 目录

1. [快速开始](#1-快速开始)
2. [核心概念](#2-核心概念)
3. [配置管理](#3-配置管理)
4. [HTTP客户端](#4-http客户端)
5. [数据库操作](#5-数据库操作)
6. [Redis操作](#6-redis操作)
7. [测试数据管理](#7-测试数据管理)
8. [事件系统与可观测性](#8-事件系统与可观测性) ⚡ v3.17+
9. [Fixtures使用](#9-fixtures使用)
10. [设计模式](#10-设计模式)
11. [调试和日志](#11-调试和日志)
12. [Allure报告](#12-allure报告)
13. [常见问题](#13-常见问题)

---

## 1. 快速开始

### 1.1 创建项目

使用脚手架工具快速创建项目：

```bash
# 创建API测试项目
df-test init my-test-project

# 创建UI测试项目
df-test init my-ui-project --type ui

# 创建完整项目（API + UI）
df-test init my-full-project --type full
```

### 1.2 配置环境

```bash
cd my-test-project

# 复制环境变量模板
cp .env.example .env

# 编辑环境变量
vim .env
```

**.env 示例**:

```bash
# HTTP配置
MYPROJECT_HTTP_BASE_URL=http://localhost:8000/api
MYPROJECT_HTTP_TIMEOUT=30

# 数据库配置
MYPROJECT_DB_CONNECTION_STRING=mysql+pymysql://user:pass@localhost:3306/testdb

# Redis配置
MYPROJECT_REDIS_HOST=localhost
MYPROJECT_REDIS_PORT=6379
```

### 1.3 运行测试

```bash
# 运行所有测试
pytest

# 运行冒烟测试
pytest -m smoke

# 运行指定文件
pytest tests/api/test_user.py

# 运行并生成Allure报告
pytest --alluredir=allure-results
allure serve allure-results
```

---

## 2. 核心概念

### 2.1 v3架构分层

DF Test Framework v3.0采用按交互模式分类的5层架构：

```
Layer 0: common/              # 基础层（异常、协议）
         └── exceptions.py

Layer 1: 能力层（按交互模式分类）
         ├── clients/         # 请求-响应模式（HTTP、gRPC等）
         ├── drivers/         # 会话式交互模式（Web、App等）
         ├── databases/       # 数据访问模式（MySQL、Redis等）
         ├── messengers/      # 消息传递模式（Kafka、RabbitMQ等）
         ├── storages/        # 文件存储模式（S3、OSS等）
         └── engines/         # 计算引擎模式（Spark、Flink等）

Layer 2: infrastructure/      # 基础设施层
         ├── bootstrap/       # 启动流程
         ├── runtime/         # 运行时管理
         ├── config/          # 配置管理
         ├── logging/         # 日志管理
         └── providers/       # 依赖注入

Layer 3: testing/             # 测试支持层
         ├── fixtures/        # Pytest fixtures
         ├── data/            # 测试数据（builders等）
         ├── plugins/         # Pytest插件
         └── debug/           # 调试工具

Layer 4: 扩展工具层
         ├── extensions/      # 扩展系统
         ├── cli/             # 命令行工具
         ├── models/          # 数据模型
         └── utils/           # 工具函数
```

### 2.2 核心组件

| 组件 | 说明 | 文件路径 |
|------|------|---------|
| **Bootstrap** | 框架启动器 | `infrastructure/bootstrap/` |
| **RuntimeContext** | 运行时上下文 | `infrastructure/runtime/` |
| **HttpClient** | HTTP客户端 | `clients/http/rest/httpx/` |
| **Database** | 数据库客户端 | `databases/database.py` |
| **RedisClient** | Redis客户端 | `databases/redis/` |
| **BaseAPI** | API基类 | `clients/http/rest/httpx/base_api.py` |
| **BaseRepository** | Repository基类 | `databases/repositories/` |
| **BaseBuilder** | Builder基类 | `testing/data/builders/` |

### 2.3 启动流程

```python
from df_test_framework import Bootstrap

# 1. 创建Bootstrap
app = Bootstrap().with_settings(MySettings).build()

# 2. 运行并获取RuntimeContext
runtime = app.run()

# 3. 获取客户端
http_client = runtime.http_client()
database = runtime.database()
redis = runtime.redis()
```

在pytest中，这个流程由框架自动完成，你只需使用fixtures：

```python
def test_example(http_client, database):
    """框架自动注入http_client和database"""
    response = http_client.get("/users/1")
    user = database.query_one("SELECT * FROM users WHERE id = :id", {"id": 1})
```

---

## 3. 配置管理

### 3.1 定义配置类

**config/settings.py**:

```python
from pydantic import Field
from df_test_framework import (
    FrameworkSettings,
    HTTPConfig,
    DatabaseConfig,
    RedisConfig,
)


class MyProjectSettings(FrameworkSettings):
    """项目配置类

    继承FrameworkSettings，添加项目特定配置。
    支持从环境变量自动加载。
    """

    # HTTP配置（v3.5+ 使用HTTPSettings）
    http_settings: HTTPSettings = Field(
        default_factory=lambda: HTTPSettings(
            base_url="http://localhost:8000/api",
            timeout=30,
            max_retries=3,
        ),
        description="HTTP配置（自动转换为HTTPConfig）"
    )

    # 数据库配置
    db: DatabaseConfig = Field(
        default_factory=lambda: DatabaseConfig(
            connection_string="mysql+pymysql://user:pass@localhost:3306/testdb",
            pool_size=5,
            echo=False,
        )
    )

    # 项目特定配置
    test_user_id: str = Field(default="test_user_001", env="TEST_USER_ID")
    admin_token: str = Field(default="", env="ADMIN_TOKEN")

    class Config:
        env_prefix = "MYPROJECT_"  # 环境变量前缀
        env_nested_delimiter = "_"
```

### 3.2 配置pytest

**pytest.ini**:

```ini
[pytest]
# 指定Settings类
df_settings_class = config.settings.MyProjectSettings

# pytest配置
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers

# 标记
markers =
    smoke: 冒烟测试
    p0: P0优先级
    p1: P1优先级
    p2: P2优先级
```

### 3.3 在测试中使用配置

**方法1：使用settings fixture**

```python
@pytest.fixture(scope="session")
def settings():
    """配置对象"""
    from config import MyProjectSettings
    return MyProjectSettings()

def test_with_settings(settings):
    """使用配置"""
    assert settings.http.base_url.startswith("http")
    user_id = settings.test_user_id
```

**方法2：通过runtime获取**

```python
def test_with_runtime(runtime):
    """通过runtime获取配置"""
    settings = runtime.settings
    assert settings.http.timeout == 30
```

---

## 4. HTTP客户端

### 4.1 使用框架提供的HttpClient

**基础用法**:

```python
def test_http_basic(http_client):
    """HTTP客户端基础用法"""

    # GET请求
    response = http_client.get("/users/1")
    assert response.status_code == 200
    user = response.json()

    # POST请求
    response = http_client.post("/users", json={
        "username": "test_user",
        "email": "test@example.com"
    })

    # PUT请求
    response = http_client.put("/users/1", json={
        "username": "updated_user"
    })

    # DELETE请求
    response = http_client.delete("/users/1")
```

**带请求头**:

```python
def test_http_with_headers(http_client):
    """带自定义请求头"""
    headers = {
        "Authorization": "Bearer token123",
        "X-Request-ID": "req-001"
    }
    response = http_client.get("/users/1", headers=headers)
```

**带查询参数**:

```python
def test_http_with_params(http_client):
    """带查询参数"""
    params = {
        "page": 1,
        "size": 10,
        "status": "ACTIVE"
    }
    response = http_client.get("/users", params=params)
```

### 4.2 封装API客户端

**apis/user_api.py**:

```python
from df_test_framework import BaseAPI, HttpClient
from df_test_framework.clients.http.rest.httpx import BusinessError
from typing import Dict, Any, List


class UserAPI(BaseAPI):
    """用户API客户端"""

    def __init__(self, http_client: HttpClient):
        super().__init__(http_client)
        self.base_path = "/users"

    def _check_business_error(self, response_data: dict) -> None:
        """检查业务错误"""
        code = response_data.get("code")
        if code != 200:
            message = response_data.get("message", "未知错误")
            raise BusinessError(f"[{code}] {message}", code=code)

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """获取用户"""
        response = self.http_client.get(f"{self.base_path}/{user_id}")
        data = response.json()
        self._check_business_error(data)
        return data.get("data")

    def create_user(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建用户"""
        response = self.http_client.post(self.base_path, json=request_data)
        data = response.json()
        self._check_business_error(data)
        return data.get("data")
```

**在conftest.py中提供fixture**:

```python
@pytest.fixture
def user_api(http_client):
    """用户API客户端fixture"""
    from apis import UserAPI
    return UserAPI(http_client)
```

**在测试中使用**:

```python
def test_create_user(user_api):
    """使用封装的API客户端"""
    result = user_api.create_user({
        "username": "test_user",
        "email": "test@example.com"
    })

    assert result["username"] == "test_user"
    assert "user_id" in result
```

### 4.3 使用认证中间件

**Bearer Token认证**:

```python
from df_test_framework import BearerTokenMiddleware

@pytest.fixture
def authenticated_http_client(http_client, settings):
    """带认证的HTTP客户端"""
    token = settings.admin_token
    middleware = BearerTokenMiddleware(token)
    http_client.add_request_middleware(middleware)
    return http_client
```

**签名认证**:

```python
# ⚠️ v3.5+ 推荐使用声明式配置（在settings.py中配置SignatureMiddlewareSettings）
# 以下是高级用法示例 - 手动添加中间件

from df_test_framework import (
    SignatureMiddleware,
    MD5SortedValuesStrategy,
    SignatureConfig,
)

@pytest.fixture
def signed_http_client(http_client):
    """带签名的HTTP客户端（高级用法 - 手动添加中间件）

    v3.5+ 推荐方式：在 settings.py 中使用 SignatureMiddlewareSettings 配置
    详见：docs/user-guide/configuration.md
    """
    config = SignatureConfig(
        app_id="your_app_id",
        app_secret="your_app_secret",
        sign_param_name="sign",
        timestamp_param_name="timestamp",
    )

    strategy = MD5SortedValuesStrategy(config)
    middleware = SignatureMiddleware(strategy, config)
    http_client.add_request_middleware(middleware)

    return http_client
```

---

## 5. 数据库操作

### 5.1 直接使用Database

**基础查询**:

```python
def test_database_query(database):
    """数据库查询"""

    # 查询单条
    user = database.query_one(
        "SELECT * FROM users WHERE id = :id",
        {"id": 1}
    )
    assert user is not None

    # 查询多条
    users = database.query_all(
        "SELECT * FROM users WHERE status = :status",
        {"status": "ACTIVE"}
    )
    assert len(users) > 0
```

**执行操作**:

```python
def test_database_execute(database):
    """数据库执行"""

    # INSERT
    user_id = database.insert("users", {
        "username": "test_user",
        "email": "test@example.com",
        "status": "ACTIVE"
    })

    # UPDATE
    affected = database.update(user_id, {
        "status": "INACTIVE"
    })
    assert affected == 1

    # DELETE
    affected = database.delete("users", {"id": user_id})
    assert affected == 1
```

### 5.2 使用Repository模式

**repositories/user_repo.py**:

```python
from df_test_framework import BaseRepository
from typing import Optional, List, Dict, Any


class UserRepository(BaseRepository):
    """用户Repository"""

    def __init__(self, db):
        super().__init__(db, table_name="users")

    def find_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """根据用户名查找"""
        return self.find_one({"username": username})

    def find_active_users(self) -> List[Dict[str, Any]]:
        """查找激活用户"""
        return self.find_all(
            conditions={"status": "ACTIVE"},
            order_by="created_at DESC"
        )

    def count_by_status(self, status: str) -> int:
        """统计指定状态的用户"""
        return self.count({"status": status})
```

**在conftest.py中提供fixture**:

```python
@pytest.fixture
def user_repo(database):
    """用户Repository fixture"""
    from repositories import UserRepository
    return UserRepository(database)
```

**在测试中使用**:

```python
def test_user_repository(user_repo):
    """使用Repository"""

    # 查找用户
    user = user_repo.find_by_username("test_user")
    assert user is not None

    # 统计
    count = user_repo.count_by_status("ACTIVE")
    assert count > 0
```

### 5.3 使用事务

**手动事务**:

```python
def test_transaction(database):
    """使用事务"""

    with database.transaction():
        # 插入用户
        user_id = database.insert("users", {
            "username": "test_user"
        })

        # 插入配置
        database.insert("user_settings", {
            "user_id": user_id,
            "theme": "dark"
        })

        # 如果发生异常，自动回滚
        # 如果成功，自动提交
```

**Unit of Work 模式（v3.7推荐）**:

```python
# 1. 定义项目的 UoW（在 your_project/uow.py）
from df_test_framework.databases import UnitOfWork

class ProjectUoW(UnitOfWork):
    """项目的 Unit of Work

    统一管理事务和所有 Repository
    """

    @property
    def users(self):
        """用户 Repository"""
        from .repositories import UserRepository
        return self.repository(UserRepository)

    @property
    def orders(self):
        """订单 Repository"""
        from .repositories import OrderRepository
        return self.repository(OrderRepository)

# 2. 在 conftest.py 中定义 fixture
@pytest.fixture
def uow(session_factory):
    """Unit of Work fixture"""
    from your_project.uow import ProjectUoW
    with ProjectUoW(session_factory) as uow:
        yield uow
        # 默认自动回滚，调用 uow.commit() 持久化

# 3. 在测试中使用
def test_with_uow(uow):
    """使用 UoW 模式"""
    # 使用 Repository 查询
    user = uow.users.find_by_username("test_user")

    # 执行 SQL 查询
    from sqlalchemy import text
    result = uow.session.execute(
        text("SELECT * FROM users WHERE id = :id"),
        {"id": 1}
    )

    # ✅ 测试结束后自动回滚，数据不会保留
    # 如需持久化：uow.commit()
```

---

## 6. Redis操作

### 6.1 基础操作

```python
def test_redis_basic(redis_client):
    """Redis基础操作"""

    # 字符串操作
    redis_client.set("key1", "value1")
    value = redis_client.get("key1")
    assert value == "value1"

    # 带过期时间
    redis_client.set("key2", "value2", ex=60)  # 60秒后过期

    # 删除
    redis_client.delete("key1")
    assert redis_client.get("key1") is None
```

### 6.2 哈希操作

```python
def test_redis_hash(redis_client):
    """Redis哈希操作"""

    # 设置哈希字段
    redis_client.hset("user:1", "name", "张三")
    redis_client.hset("user:1", "age", "30")

    # 获取哈希字段
    name = redis_client.hget("user:1", "name")
    assert name == "张三"

    # 获取所有字段
    user_data = redis_client.hgetall("user:1")
    assert user_data["name"] == "张三"
    assert user_data["age"] == "30"
```

### 6.3 列表操作

```python
def test_redis_list(redis_client):
    """Redis列表操作"""

    # 左推
    redis_client.lpush("queue", "item1")
    redis_client.lpush("queue", "item2")

    # 右推
    redis_client.rpush("queue", "item3")

    # 范围获取
    items = redis_client.lrange("queue", 0, -1)
    assert len(items) == 3
```

---

## 7. 测试数据管理

### 7.1 使用 Unit of Work 模式（⭐v3.7推荐）

**uow.py**:

```python
from df_test_framework.databases import UnitOfWork

class ProjectUoW(UnitOfWork):
    """项目的 Unit of Work

    统一管理事务和所有 Repository，确保同一个 Session
    """

    @property
    def users(self):
        from .repositories import UserRepository
        return self.repository(UserRepository)

    @property
    def orders(self):
        from .repositories import OrderRepository
        return self.repository(OrderRepository)
```

**conftest.py**:

```python
@pytest.fixture
def uow(session_factory):
    """Unit of Work fixture

    默认自动回滚，调用 uow.commit() 持久化数据
    """
    from your_project.uow import ProjectUoW
    with ProjectUoW(session_factory) as uow:
        yield uow
        # 默认自动回滚
```

**使用**:

```python
def test_create_user(user_api, uow):
    """测试创建用户（自动回滚）"""

    # 创建用户
    result = user_api.create_user({
        "username": "test_user"
    })
    user_id = result["user_id"]

    # 验证数据库 - 使用 UoW 的 Repository
    user = uow.users.find_by_id(user_id)
    assert user is not None
    assert user["username"] == "test_user"

    # ✅ 测试结束后自动回滚
```

### 7.2 使用Builder构建测试数据

**builders/user_builder.py**:

```python
from df_test_framework import DictBuilder


class UserRequestBuilder:
    """用户请求Builder"""

    def __init__(self):
        self._builder = DictBuilder({
            "username": "default_user",
            "email": "default@example.com",
            "password": "Default123!",
            "status": "ACTIVE"
        })

    def with_username(self, username: str):
        self._builder.set("username", username)
        return self

    def with_email(self, email: str):
        self._builder.set("email", email)
        return self

    def as_inactive(self):
        self._builder.set("status", "INACTIVE")
        return self

    def build(self):
        return self._builder.build()
```

**使用**:

```python
from builders import UserRequestBuilder

def test_create_user_with_builder(user_api):
    """使用Builder构建数据"""

    user_data = (
        UserRequestBuilder()
        .with_username("test_user_001")
        .with_email("test001@example.com")
        .build()
    )

    result = user_api.create_user(user_data)
    assert result["username"] == "test_user_001"
```

---

## 8. 事件系统与可观测性

> ⚡ **v3.17.0 新特性**: 事件关联、OpenTelemetry 整合、AllureObserver 自动集成

### 8.1 事件系统概述

DF Test Framework v3.14+ 引入了 EventBus 事件总线，v3.17.0 进一步增强了可观测性：

**核心特性**：
- ✅ 发布-订阅模式（Pub/Sub）
- ✅ 事件关联（correlation_id）- v3.17+
- ✅ OpenTelemetry 整合（trace_id/span_id）- v3.17+
- ✅ 测试隔离机制 - v3.17+
- ✅ AllureObserver 自动集成 - v3.17+

### 8.2 AllureObserver 自动记录（v3.17+，⭐推荐）

最简单的使用方式 - 只需注入 `allure_observer` fixture：

```python
def test_api_with_allure(allure_observer, http_client):
    """自动记录 HTTP 请求到 Allure 报告

    只需注入 allure_observer，所有 HTTP 请求会自动记录：
    - 请求方法、URL、Headers、Body
    - 响应状态码、Headers、Body
    - OpenTelemetry trace_id/span_id
    - 响应时间
    """
    response = http_client.get("/users/123")
    assert response.status_code == 200
    # ✅ 请求已自动记录到 Allure
```

**支持的协议**：
- HTTP/REST
- GraphQL
- gRPC

### 8.3 事件关联（correlation_id）

v3.17.0 引入事件关联机制，可以追踪完整的请求生命周期：

```python
from df_test_framework import EventBus, HttpRequestStartEvent, HttpRequestEndEvent

bus = EventBus()
requests = {}

@bus.on(HttpRequestStartEvent)
def on_start(event):
    """记录请求开始"""
    requests[event.correlation_id] = {
        "start_time": event.timestamp,
        "url": event.url,
    }

@bus.on(HttpRequestEndEvent)
def on_end(event):
    """计算请求耗时"""
    if event.correlation_id in requests:
        start = requests[event.correlation_id]["start_time"]
        duration = (event.timestamp - start).total_seconds()
        print(f"请求 {event.url} 耗时: {duration}s")

# HttpClient 使用 EventBus
client = HttpClient(base_url="https://api.example.com", event_bus=bus)
response = client.get("/users")
```

**关键概念**：
- `event_id`: 每个事件的唯一标识（evt-{12hex}）
- `correlation_id`: 关联 Start/End 事件对（cor-{12hex}）
- `trace_id`/`span_id`: OpenTelemetry 追踪上下文

### 8.4 测试隔离

v3.17.0 确保每个测试使用独立的 EventBus，避免事件跨测试泄漏：

```python
from df_test_framework.infrastructure.events import set_test_event_bus, EventBus

def test_with_isolated_events():
    """每个测试使用独立的 EventBus"""
    # 创建测试专用的 EventBus
    test_bus = EventBus()
    set_test_event_bus(test_bus)

    # 订阅测试事件
    @test_bus.on(HttpRequestEndEvent)
    def on_request(event):
        print(f"请求完成: {event.url}")

    # HttpClient 自动使用测试 EventBus
    # ✅ 事件只在当前测试中生效
```

### 8.5 OpenTelemetry 整合

v3.17.0 自动注入 OpenTelemetry 追踪上下文到事件：

```python
from opentelemetry import trace
from df_test_framework import EventBus, HttpRequestEndEvent

tracer = trace.get_tracer(__name__)
bus = EventBus()

@bus.on(HttpRequestEndEvent)
def log_with_trace(event):
    """记录请求时包含追踪信息"""
    print(f"[{event.trace_id}] {event.method} {event.url} - {event.status_code}")

# HttpClient 自动注入 trace_id/span_id 到事件
with tracer.start_as_current_span("test-api-call"):
    client = HttpClient(base_url="https://api.example.com", event_bus=bus)
    response = client.get("/users")
    # ✅ 事件自动包含当前 Span 的 trace_id 和 span_id
```

**追踪格式**: 符合 W3C TraceContext 标准
- `trace_id`: 32 字符十六进制（如: `4bf92f3577b34da6a3ce929d0e0e4736`）
- `span_id`: 16 字符十六进制（如: `00f067aa0ba902b7`）

### 8.6 详细文档

完整的事件系统使用说明，请参考：
- [EventBus 指南](../guides/event_bus_guide.md) - 600+ 行完整示例
- [最佳实践 - 事件系统](BEST_PRACTICES.md#11-事件系统与可观测性最佳实践)

---

## 9. Fixtures使用

### 9.1 框架提供的Fixtures

| Fixture | 作用域 | 说明 | 版本 |
|---------|--------|------|------|
| `runtime` | session | RuntimeContext实例 | v3.0+ |
| `http_client` | session | HTTP客户端 | v3.0+ |
| `database` | session | 数据库客户端 | v3.0+ |
| `redis_client` | session | Redis客户端 | v3.0+ |
| `event_bus` | session | 事件总线 | v3.14+ |
| `allure_observer` | function | Allure观察器（自动记录HTTP请求）| v3.17+ |
| `cleanup` | function | 测试数据清理管理器 | v3.11+ |

### 9.2 自定义Fixtures

**conftest.py**:

```python
import pytest

# Session级别 - 整个测试会话共享
@pytest.fixture(scope="session")
def test_config():
    """测试配置"""
    return {
        "test_user_id": "test_user_001",
        "admin_token": "admin_token_123"
    }

# Function级别 - 每个测试独立
@pytest.fixture
def test_user_data():
    """测试用户数据"""
    return {
        "username": "test_user",
        "email": "test@example.com"
    }

# 带清理的Fixture
@pytest.fixture
def temp_file():
    """临时文件"""
    import tempfile

    # Setup
    f = tempfile.NamedTemporaryFile(delete=False)

    yield f.name

    # Teardown
    import os
    os.unlink(f.name)
```

---

## 10. 设计模式

### 10.1 Repository模式

用于封装数据访问逻辑：

```python
from df_test_framework import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, table_name="users")

    def find_by_username(self, username: str):
        return self.find_one({"username": username})
```

### 9.2 Builder模式

用于构建测试数据：

```python
from df_test_framework import DictBuilder

class UserRequestBuilder:
    def __init__(self):
        self._builder = DictBuilder({"username": "default"})

    def with_username(self, username: str):
        self._builder.set("username", username)
        return self

    def build(self):
        return self._builder.build()
```

### 9.3 Page Object模式（UI测试）

```python
from df_test_framework import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login")

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
```

---

## 11. 调试和日志

### 11.1 启用HTTP调试

```python
from df_test_framework.testing.debug import enable_http_debug

def test_with_http_debug(http_client):
    """启用HTTP调试"""
    enable_http_debug()

    response = http_client.get("/users/1")

    # 会打印详细的请求和响应日志
```

### 10.2 启用数据库调试

```python
from df_test_framework.testing.debug import enable_db_debug

def test_with_db_debug(database):
    """启用数据库调试"""
    enable_db_debug()

    user = database.query_one("SELECT * FROM users WHERE id = :id", {"id": 1})

    # 会打印SQL语句和参数
```

### 10.3 使用loguru日志

```python
from loguru import logger

def test_with_logging():
    """使用日志"""
    logger.info("测试开始")
    logger.debug("调试信息")
    logger.warning("警告信息")
    logger.error("错误信息")
```

---

## 12. Allure报告

### 12.1 基础用法

```python
import allure

@allure.feature("用户管理")
@allure.story("用户创建")
class TestUserCreation:

    @allure.title("测试创建用户成功")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_success(self, user_api):
        """测试创建用户成功"""
        result = user_api.create_user({"username": "test_user"})
        assert result["username"] == "test_user"
```

### 11.2 使用步骤

```python
from df_test_framework.testing.plugins import step, attach_json

def test_with_steps(user_api):
    """使用Allure步骤"""

    with step("准备测试数据"):
        user_data = {"username": "test_user"}
        attach_json(user_data, name="用户数据")

    with step("调用创建API"):
        result = user_api.create_user(user_data)
        attach_json(result, name="API响应")

    with step("验证结果"):
        assert result["username"] == "test_user"
```

### 11.3 附加信息

```python
from df_test_framework.testing.plugins import (
    attach_json,
    attach_log,
    attach_screenshot,
)

def test_with_attachments(user_api):
    """附加信息到报告"""

    # 附加JSON
    attach_json({"key": "value"}, name="数据")

    # 附加日志
    attach_log("这是日志内容", name="日志")

    # 附加截图（UI测试）
    # attach_screenshot(page.screenshot(), name="截图")
```

---

## 13. 常见问题

### 13.1 如何配置数据库连接？

在`config/settings.py`中配置：

```python
from df_test_framework import FrameworkSettings, DatabaseConfig
from pydantic import Field

class MySettings(FrameworkSettings):
    db: DatabaseConfig = Field(
        default_factory=lambda: DatabaseConfig(
            connection_string="mysql+pymysql://user:pass@localhost:3306/testdb"
        )
    )
```

### 12.2 如何避免测试数据污染？

使用 Unit of Work 模式自动回滚（v3.7推荐）：

```python
# conftest.py
@pytest.fixture
def uow(database):
    from your_project.uow import ProjectUoW
    with ProjectUoW(database.engine) as uow:
        yield uow
        # 默认自动回滚

def test_example(uow):
    # 所有数据操作都会回滚
    user = uow.users.create({"username": "test"})
    # 测试结束后自动回滚，数据不会保留
```

### 12.3 如何添加认证token？

使用中间件：

```python
from df_test_framework import BearerTokenMiddleware

@pytest.fixture
def authenticated_client(http_client):
    middleware = BearerTokenMiddleware("your_token")
    http_client.add_request_middleware(middleware)
    return http_client
```

### 12.4 如何运行特定标记的测试？

```bash
# 运行冒烟测试
pytest -m smoke

# 运行P0测试
pytest -m p0

# 运行P0或P1测试
pytest -m "p0 or p1"

# 排除慢速测试
pytest -m "not slow"
```

### 12.5 如何生成测试报告？

```bash
# Allure报告
pytest --alluredir=allure-results
allure serve allure-results

# HTML报告
pytest --html=report.html --self-contained-html

# JUnit XML报告
pytest --junitxml=junit.xml
```

---

## 📝 下一步

- [最佳实践指南](BEST_PRACTICES.md) - 学习最佳实践
- [API参考文档](../api-reference/README.md) - 查阅完整API
- [示例代码](../../examples/) - 查看示例代码

---

**版本历史**:
- v1.0 (2025-11-04) - 初始版本
