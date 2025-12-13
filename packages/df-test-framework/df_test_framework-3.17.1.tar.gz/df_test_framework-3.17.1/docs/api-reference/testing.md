# Testing API 参考

> 📖 **测试支持层** - v3架构新增调试工具和数据构建器
>
> v3新增: Debug Tools（HTTP/DB调试）、Data Builders（测试数据构建）

> ⭐ **推荐阅读**: 本文档包含API参考。如果你需要**经过实际项目验证**的测试用例编写最佳实践（包含完整示例），请查看 [已验证最佳实践](../user-guide/VERIFIED_BEST_PRACTICES.md#6-测试用例编写最佳实践)，该文档基于真实生产项目（gift-card-test）验证，置信度100%。

测试支持层的完整API参考，包含Pytest Fixtures和测试辅助工具。

---

## 📦 模块导入

```python
# Fixtures（通常在conftest.py中自动可用）
from df_test_framework.testing.fixtures.core import (
    runtime,
    http_client,
    database,
    redis_client,
)

# Plugins（测试中使用）
from df_test_framework.testing.plugins import (
    AllureHelper,
    attach_json,
    attach_log,
    attach_screenshot,
    step,
    EnvironmentMarker,
    get_env,
    is_env,
)

# 🆕 v3新增: Data Builders（测试数据构建）
from df_test_framework import BaseBuilder, DictBuilder
# 或完整路径
from df_test_framework.testing.data.builders import BaseBuilder, DictBuilder

# 🆕 v3新增: Debug Tools（调试工具）
from df_test_framework import (
    HTTPDebugger,
    DBDebugger,
    enable_http_debug,
    disable_http_debug,
    enable_db_debug,
    disable_db_debug,
)
# 或完整路径
from df_test_framework.testing.debug import HTTPDebugger, DBDebugger
```

---

## 🎯 Pytest Fixtures

框架提供的核心fixtures，通过pytest插件自动注册。

### 配置pytest插件

在`conftest.py`中启用框架插件：

```python
# tests/conftest.py
import pytest

# 方式1: 使用pytest_plugins（推荐）
pytest_plugins = ["df_test_framework.testing.fixtures.core"]

# 方式2: 在pytest.ini中配置
# [pytest]
# df_settings_class = your_project.config.settings.YourSettings
```

---

### runtime

**类型**: `pytest.fixture(scope="session")`

**返回**: `RuntimeContext`

**说明**: 运行时上下文对象，提供对所有核心服务的访问。

#### 使用示例

```python
def test_runtime_access(runtime):
    """访问运行时上下文"""

    # 获取配置
    settings = runtime.settings
    assert settings.environment == "test"

    # 获取HTTP客户端
    http = runtime.http_client()

    # 获取数据库
    db = runtime.database()

    # 获取Redis客户端
    redis = runtime.redis()
```

#### API方法

| 方法 | 返回类型 | 说明 |
|-----|---------|------|
| `runtime.settings` | `FrameworkSettings` | 配置对象 |
| `runtime.http_client()` | `HttpClient` | HTTP客户端实例 |
| `runtime.database()` | `Database` | 数据库实例 |
| `runtime.redis()` | `RedisClient` | Redis客户端实例 |
| `runtime.close()` | `None` | 关闭所有资源 |

---

### http_client

**类型**: `pytest.fixture(scope="session")`

**返回**: `HttpClient`

**说明**: HTTP客户端fixture，用于发送API请求。

#### 基本用法

```python
def test_api_request(http_client):
    """发送HTTP请求"""

    # GET请求
    response = http_client.get("/api/users/1")
    assert response.status_code == 200

    # POST请求
    response = http_client.post("/api/users", json={
        "name": "张三",
        "email": "zhangsan@example.com"
    })
    assert response.status_code == 201

    # 带请求头
    response = http_client.get("/api/profile", headers={
        "Authorization": "Bearer token123"
    })
```

#### 高级用法

```python
import allure
from df_test_framework.testing.plugins import step

def test_api_with_steps(http_client):
    """使用步骤记录API测试"""

    with step("创建用户"):
        response = http_client.post("/api/users", json={
            "name": "测试用户"
        })
        user_id = response.json()["id"]

    with step("查询用户"):
        response = http_client.get(f"/api/users/{user_id}")
        assert response.json()["name"] == "测试用户"

    with step("删除用户"):
        response = http_client.delete(f"/api/users/{user_id}")
        assert response.status_code == 204
```

#### API方法

| 方法 | 说明 |
|-----|------|
| `get(url, **kwargs)` | 发送GET请求 |
| `post(url, **kwargs)` | 发送POST请求 |
| `put(url, **kwargs)` | 发送PUT请求 |
| `patch(url, **kwargs)` | 发送PATCH请求 |
| `delete(url, **kwargs)` | 发送DELETE请求 |
| `request(method, url, **kwargs)` | 发送自定义请求 |

---

### database

**类型**: `pytest.fixture(scope="session")`

**返回**: `Database`

**说明**: 数据库fixture，用于执行SQL查询。

#### 基本用法

```python
def test_database_query(database):
    """执行数据库查询"""

    # 执行查询
    result = database.execute(
        "SELECT * FROM users WHERE id = :id",
        {"id": 1}
    )

    assert len(result) > 0
    assert result[0]["id"] == 1
```

#### 使用Repository模式

```python
from your_project.repositories import UserRepository

def test_with_repository(database):
    """使用Repository访问数据"""

    repo = UserRepository(database)

    # 查询用户
    user = repo.find_by_id(1)
    assert user is not None

    # 查询所有用户
    users = repo.find_all()
    assert len(users) > 0
```

#### API方法

| 方法 | 说明 |
|-----|------|
| `execute(sql, params=None)` | 执行SQL并返回结果 |
| `execute_many(sql, params_list)` | 批量执行SQL |
| `transaction()` | 开启事务上下文 |
| `close()` | 关闭数据库连接 |

---

### redis_client

**类型**: `pytest.fixture(scope="session")`

**返回**: `RedisClient`

**说明**: Redis客户端fixture，用于缓存和数据存储。

#### 使用示例

```python
def test_redis_operations(redis_client):
    """Redis基本操作"""

    # 设置值
    redis_client.set("test_key", "test_value", ex=60)

    # 获取值
    value = redis_client.get("test_key")
    assert value == "test_value"

    # 删除键
    redis_client.delete("test_key")

    # 验证删除
    assert redis_client.get("test_key") is None
```

#### API方法

| 方法 | 说明 |
|-----|------|
| `get(key)` | 获取值 |
| `set(key, value, ex=None)` | 设置值（可选过期时间） |
| `delete(*keys)` | 删除键 |
| `exists(*keys)` | 检查键是否存在 |
| `expire(key, seconds)` | 设置过期时间 |
| `hget(name, key)` | 获取哈希值 |
| `hset(name, key, value)` | 设置哈希值 |
| `lpush(key, *values)` | 列表左侧推入 |
| `rpush(key, *values)` | 列表右侧推入 |

---

## ⭐ 数据清理Fixture（核心特性）

### db_transaction

**类型**: `pytest.fixture(scope="function")`

**返回**: `Database`

**说明**: 数据库事务自动回滚fixture - **框架最强大的特性之一**！

#### 为什么重要？

- ❌ **传统方式**：测试后需手动清理数据，容易遗漏导致数据污染
- ✅ **db_transaction**：测试结束自动回滚，数据库始终干净
- 🚀 **提升效率**：节省80%数据清理代码

#### 实现方式

在项目的`fixtures/data_cleaners.py`中定义：

```python
import pytest
from typing import Generator
from df_test_framework import Database

@pytest.fixture
def db_transaction(database: Database) -> Generator[Database, None, None]:
    """数据库事务回滚清理（⭐推荐）

    测试开始前开启事务，测试结束后自动回滚，数据不会保留。
    """
    with database.transaction() as session:
        yield database
        # 测试结束后自动回滚
```

#### 使用示例

```python
from your_project.repositories import UserRepository

def test_create_and_verify_user(http_client, db_transaction):
    """测试创建用户并验证数据库

    ✨ 使用db_transaction后，测试结束会自动回滚，无需手动清理！
    """

    # 1. 调用API创建用户
    response = http_client.post("/api/users", json={
        "name": "测试用户",
        "email": "test@example.com"
    })
    assert response.status_code == 201
    user_id = response.json()["id"]

    # 2. 验证数据库中的数据
    repo = UserRepository(db_transaction)
    user = repo.find_by_id(user_id)
    assert user is not None
    assert user["name"] == "测试用户"

    # ✅ 测试结束后，数据自动回滚，数据库保持干净！
    # 无需手动删除，无需担心数据污染！
```

#### 对比：有无db_transaction

**❌ 不使用db_transaction（传统方式）：**

```python
def test_create_user(http_client, database):
    # 创建用户
    response = http_client.post("/api/users", json={"name": "测试"})
    user_id = response.json()["id"]

    # 验证
    assert user_id is not None

    # ⚠️ 必须手动清理
    database.execute("DELETE FROM users WHERE id = :id", {"id": user_id})
    database.execute("DELETE FROM user_profiles WHERE user_id = :id", {"id": user_id})
    database.execute("DELETE FROM user_settings WHERE user_id = :id", {"id": user_id})
    # ...还有更多关联表需要清理
```

**✅ 使用db_transaction（推荐方式）：**

```python
def test_create_user(http_client, db_transaction):
    # 创建用户
    response = http_client.post("/api/users", json={"name": "测试"})
    user_id = response.json()["id"]

    # 验证
    assert user_id is not None

    # ✅ 无需任何清理代码！测试结束自动回滚！
```

#### 最佳实践

1. **API + 数据库验证场景**（最常用）
   ```python
   def test_api_with_db_check(http_client, db_transaction):
       # API操作
       response = http_client.post("/api/orders", json={...})

       # 数据库验证
       repo = OrderRepository(db_transaction)
       order = repo.find_by_id(response.json()["order_id"])
       assert order["status"] == "PENDING"

       # 自动回滚，无需清理
   ```

2. **复杂业务流程测试**
   ```python
   def test_order_workflow(http_client, db_transaction):
       # 创建订单 -> 支付 -> 发货 -> 完成
       # 每一步都验证数据库状态
       # 测试结束所有数据自动回滚
   ```

3. **数据隔离测试**
   ```python
   @pytest.mark.parametrize("user_data", [
       {"name": "用户A"},
       {"name": "用户B"},
       {"name": "用户C"},
   ])
   def test_multiple_users(http_client, db_transaction, user_data):
       # 每次参数化执行都独立事务
       # 互不影响，自动清理
   ```

---

## 🎨 Allure报告辅助工具

### AllureHelper

完整的Allure报告增强类。

#### attach_json()

附加JSON数据到报告。

```python
from df_test_framework.testing.plugins import attach_json

def test_api_response(http_client):
    response = http_client.get("/api/users/1")

    # 附加响应数据到报告
    attach_json(response.json(), name="用户响应数据")

    assert response.status_code == 200
```

#### attach_log()

附加日志文件到报告。

```python
from df_test_framework.testing.plugins import attach_log

def test_with_log():
    # 执行操作...

    # 附加日志文件
    attach_log("logs/test.log", name="测试日志")
```

#### attach_screenshot()

附加截图到报告（UI测试）。

```python
from df_test_framework.testing.plugins import attach_screenshot

def test_ui_screenshot(driver):
    # 执行UI操作...

    # 保存截图
    screenshot_bytes = driver.get_screenshot_as_png()
    attach_screenshot(screenshot_bytes, name="页面截图")
```

#### step()

添加测试步骤（上下文管理器）。

```python
from df_test_framework.testing.plugins import step

def test_multi_step_api(http_client):
    """多步骤API测试"""

    with step("步骤1: 创建用户"):
        response = http_client.post("/api/users", json={"name": "测试"})
        user_id = response.json()["id"]

    with step("步骤2: 查询用户"):
        response = http_client.get(f"/api/users/{user_id}")
        assert response.json()["name"] == "测试"

    with step("步骤3: 更新用户"):
        response = http_client.put(f"/api/users/{user_id}", json={
            "name": "新名称"
        })
        assert response.status_code == 200

    with step("步骤4: 删除用户"):
        response = http_client.delete(f"/api/users/{user_id}")
        assert response.status_code == 204
```

#### add_environment_info()

添加环境信息到报告。

```python
from df_test_framework.testing.plugins import AllureHelper

def pytest_sessionstart(session):
    """在测试开始时添加环境信息"""
    AllureHelper.add_environment_info({
        "环境": "test",
        "Python版本": "3.12",
        "操作系统": "Windows 11",
        "API地址": "https://api.test.example.com"
    })
```

#### add_categories()

自定义错误分类。

```python
from df_test_framework.testing.plugins import AllureHelper

def pytest_sessionstart(session):
    """配置错误分类"""
    AllureHelper.add_categories([
        {
            "name": "API错误",
            "matchedStatuses": ["failed"],
            "messageRegex": ".*API.*"
        },
        {
            "name": "数据库错误",
            "matchedStatuses": ["broken"],
            "messageRegex": ".*(Database|SQL).*"
        },
        {
            "name": "超时错误",
            "matchedStatuses": ["broken"],
            "messageRegex": ".*timeout.*"
        }
    ])
```

---

## 🏷️ 环境标记

根据环境条件跳过或执行测试。

### get_env()

获取当前环境。

```python
from df_test_framework.testing.plugins import get_env

def test_check_environment():
    env = get_env()
    print(f"当前环境: {env}")  # test / dev / prod
```

### is_env()

检查是否为指定环境。

```python
from df_test_framework.testing.plugins import is_env

def test_environment_specific():
    if is_env("prod"):
        # 生产环境特殊处理
        pass
```

### skip_if_prod()

生产环境跳过测试。

```python
import pytest
from df_test_framework.testing.plugins import skip_if_prod

@skip_if_prod()
def test_dangerous_operation():
    """此测试在生产环境会被跳过"""
    # 危险操作，仅在测试环境执行
    pass
```

### skip_if_dev()

开发环境跳过测试。

```python
from df_test_framework.testing.plugins import skip_if_dev

@skip_if_dev()
def test_production_only():
    """此测试仅在生产环境执行"""
    pass
```

### dev_only() / prod_only()

限定环境执行。

```python
from df_test_framework.testing.plugins import dev_only, prod_only

@dev_only()
def test_dev_feature():
    """仅开发环境"""
    pass

@prod_only()
def test_prod_validation():
    """仅生产环境"""
    pass
```

---

## 📝 完整测试示例

### 综合示例：API + 数据库 + Allure

```python
import pytest
import allure
from df_test_framework.testing.plugins import step, attach_json

@allure.feature("用户管理")
@allure.story("用户CRUD操作")
class TestUserCRUD:
    """用户完整生命周期测试"""

    @allure.title("测试用户完整生命周期")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_user_lifecycle(self, http_client, db_transaction):
        """测试创建、查询、更新、删除用户"""

        user_id = None

        with step("创建用户"):
            response = http_client.post("/api/users", json={
                "name": "张三",
                "email": "zhangsan@example.com",
                "age": 30
            })
            assert response.status_code == 201

            user_data = response.json()
            user_id = user_data["id"]
            attach_json(user_data, name="创建的用户数据")

        with step("验证数据库中的用户"):
            from your_project.repositories import UserRepository
            repo = UserRepository(db_transaction)

            user = repo.find_by_id(user_id)
            assert user is not None
            assert user["name"] == "张三"
            attach_json(user, name="数据库中的用户")

        with step("查询用户API"):
            response = http_client.get(f"/api/users/{user_id}")
            assert response.status_code == 200
            assert response.json()["email"] == "zhangsan@example.com"

        with step("更新用户"):
            response = http_client.put(f"/api/users/{user_id}", json={
                "name": "李四",
                "age": 31
            })
            assert response.status_code == 200

            # 验证数据库已更新
            user = repo.find_by_id(user_id)
            assert user["name"] == "李四"
            assert user["age"] == 31

        with step("删除用户"):
            response = http_client.delete(f"/api/users/{user_id}")
            assert response.status_code == 204

            # 验证数据库已删除
            user = repo.find_by_id(user_id)
            assert user is None

        # ✅ 测试结束，所有数据库操作自动回滚！
```

---

## 🆕 v3新增: Data Builders（测试数据构建）

> ⚠️ **v3架构变更**: Builder模式已从`patterns/`迁移至`testing/data/builders/`
>
> 详见: [databases.md](databases.md) 和 [patterns.md](patterns.md)

### BaseBuilder - Builder基类

用于构建测试数据的抽象基类，提供流畅的链式API。

#### 快速开始

```python
from df_test_framework import BaseBuilder
from pydantic import BaseModel

# 定义数据模型
class UserRequest(BaseModel):
    name: str
    email: str
    age: int = 18

# 实现Builder
class UserRequestBuilder(BaseBuilder[UserRequest]):
    """用户请求Builder"""

    def __init__(self):
        self._name = "默认用户"
        self._email = "default@example.com"
        self._age = 18

    def with_name(self, name: str) -> "UserRequestBuilder":
        self._name = name
        return self

    def with_email(self, email: str) -> "UserRequestBuilder":
        self._email = email
        return self

    def with_age(self, age: int) -> "UserRequestBuilder":
        self._age = age
        return self

    def build(self) -> UserRequest:
        return UserRequest(
            name=self._name,
            email=self._email,
            age=self._age
        )

# 使用Builder
builder = UserRequestBuilder()
user = builder.with_name("张三").with_email("zhangsan@example.com").build()

# 重置Builder
builder.reset()
user2 = builder.with_name("李四").build()
```

### DictBuilder - 字典Builder

快速构建字典类型的测试数据。

```python
from df_test_framework import DictBuilder

# 基本使用
builder = DictBuilder()
data = (builder
    .add("name", "张三")
    .add("age", 25)
    .add("email", "zhangsan@example.com")
    .build())

# 条件添加
builder = DictBuilder()
data = (builder
    .add("name", "张三")
    .add_if(True, "vip", True)  # 条件为True才添加
    .add_if(False, "admin", True)  # 不添加
    .build())

# 嵌套结构
builder = DictBuilder()
data = (builder
    .add("user", {
        "name": "张三",
        "profile": {
            "age": 25,
            "city": "北京"
        }
    })
    .build())
```

### 完整文档

详细API文档请参考: [patterns.md#Builder](patterns.md#builder)

---

## 🆕 v3新增: Debug Tools（调试工具）

v3新增的调试工具，帮助开发者追踪HTTP请求和数据库查询。

### HTTPDebugger - HTTP调试器

追踪和记录所有HTTP请求/响应。

#### 基本用法

```python
from df_test_framework import enable_http_debug, disable_http_debug

def test_with_http_debug(http_client):
    """启用HTTP调试"""

    # 启用调试
    enable_http_debug()

    try:
        # 所有请求会自动打印到控制台
        response = http_client.get("/api/users/1")
        # 输出:
        # [HTTP DEBUG] GET /api/users/1
        # [HTTP DEBUG] Response: 200 OK
        # [HTTP DEBUG] Body: {"id": 1, "name": "张三"}

        response = http_client.post("/api/users", json={"name": "李四"})
        # 输出:
        # [HTTP DEBUG] POST /api/users
        # [HTTP DEBUG] Request Body: {"name": "李四"}
        # [HTTP DEBUG] Response: 201 Created

    finally:
        # 禁用调试
        disable_http_debug()
```

#### 高级用法

```python
from df_test_framework import HTTPDebugger

def test_custom_http_debug(http_client):
    """自定义HTTP调试"""

    debugger = HTTPDebugger()

    # 开始记录
    debugger.start()

    # 执行请求
    http_client.get("/api/users")
    http_client.post("/api/users", json={"name": "测试"})

    # 停止记录
    debugger.stop()

    # 获取记录的请求
    requests = debugger.get_requests()
    assert len(requests) == 2

    # 检查第一个请求
    assert requests[0]["method"] == "GET"
    assert requests[0]["url"] == "/api/users"
    assert requests[0]["status_code"] == 200
```

### DBDebugger - 数据库调试器

追踪和记录所有数据库查询。

#### 基本用法

```python
from df_test_framework import enable_db_debug, disable_db_debug

def test_with_db_debug(database):
    """启用数据库调试"""

    # 启用调试
    enable_db_debug()

    try:
        # 所有SQL会自动打印到控制台
        database.query_one("SELECT * FROM users WHERE id = :id", {"id": 1})
        # 输出:
        # [DB DEBUG] SELECT * FROM users WHERE id = :id
        # [DB DEBUG] Params: {'id': 1}
        # [DB DEBUG] Execution time: 0.015s

        database.insert("users", {"name": "张三", "age": 25})
        # 输出:
        # [DB DEBUG] INSERT INTO users (name, age) VALUES (:name, :age)
        # [DB DEBUG] Params: {'name': '张三', 'age': 25}
        # [DB DEBUG] Rows affected: 1

    finally:
        # 禁用调试
        disable_db_debug()
```

#### 高级用法

```python
from df_test_framework import DBDebugger

def test_custom_db_debug(database):
    """自定义数据库调试"""

    debugger = DBDebugger()

    # 开始记录
    debugger.start()

    # 执行查询
    database.query_all("SELECT * FROM users")
    database.insert("users", {"name": "测试"})

    # 停止记录
    debugger.stop()

    # 获取记录的查询
    queries = debugger.get_queries()
    assert len(queries) == 2

    # 检查慢查询
    slow_queries = debugger.get_slow_queries(threshold=0.1)  # 超过100ms
    for query in slow_queries:
        print(f"慢查询: {query['sql']} (耗时: {query['duration']}s)")
```

### Pytest Fixture集成

```python
# conftest.py
import pytest
from df_test_framework import enable_http_debug, enable_db_debug
from df_test_framework import disable_http_debug, disable_db_debug

@pytest.fixture(scope="function")
def debug_mode():
    """自动启用调试模式"""
    enable_http_debug()
    enable_db_debug()
    yield
    disable_http_debug()
    disable_db_debug()

# 使用
def test_with_debug(debug_mode, http_client, database):
    """测试中自动启用调试"""
    http_client.get("/api/users")  # 自动打印调试信息
    database.query_all("SELECT * FROM users")  # 自动打印调试信息
```

---

## ✅ 测试用例编写最佳实践（已验证）

### 完整测试用例模板

以下是经过gift-card-test项目验证的完整测试用例：

```python
# 来自: gift-card-test/tests/api/test_admin_system/test_templates.py

import pytest
import allure
from df_test_framework.testing.plugins import attach_json, step


@allure.feature("Admin管理端")
@allure.story("卡模板管理")
class TestAdminTemplates:
    """Admin管理端卡模板管理测试类

    ✅ 已验证特性:
    - 使用step分步骤
    - 使用attach_json附加数据
    - API调用 + Repository验证双重保障
    - db_transaction自动回滚
    """

    @allure.title("查询卡模板-分页查询")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_query_templates_pagination(
        self,
        admin_template_api,      # API客户端
        template_repository,     # Repository
        db_transaction,          # 自动回滚
        settings                 # 配置对象
    ):
        """测试Admin分页查询卡模板

        测试步骤:
        1. 使用Admin API分页查询模板
        2. 验证分页信息正确
        3. 验证模板信息完整
        4. 使用Repository验证数据库数据

        验证点:
        - 响应成功
        - 分页信息正确(current/size/total/pages)
        - 模板字段完整
        - 数据库数据一致
        """
        with step("分页查询卡模板"):
            request = AdminTemplateQueryRequest(current=1, size=20)
            response = admin_template_api.query_templates(request)
            attach_json(response.model_dump(), name="查询响应")

        with step("验证响应成功"):
            assert response.success, f"查询失败: {response.message}"
            assert response.data is not None

        with step("验证分页信息"):
            assert response.data.current == 1
            assert response.data.size == 20
            assert response.data.total >= 0
            assert response.data.pages >= 0

        with step("验证模板信息完整"):
            if len(response.data.records) > 0:
                for template in response.data.records:
                    assert template.id is not None
                    assert template.template_id is not None
                    assert template.name is not None
                    assert template.face_value is not None
                    assert template.status in [0, 1]

        with step("使用Repository验证数据一致性"):
            if len(response.data.records) > 0:
                first_template = response.data.records[0]
                db_template = template_repository.find_by_template_id(
                    first_template.template_id
                )
                assert db_template is not None
                assert db_template["name"] == first_template.name
```

### 关键特性说明

#### 1. Allure增强标注

```python
@allure.feature("系统名称")     # Feature级别分类
@allure.story("功能模块")       # Story级别分类
class TestFeatureName:
    @allure.title("测试场景描述")  # 测试标题
    @allure.severity(allure.severity_level.CRITICAL)  # 优先级
    @pytest.mark.smoke           # pytest标记
    def test_case(self):
        pass
```

#### 2. Fixtures使用

**必需Fixtures**:
- `api_fixture` - API客户端（必需）
- `repository_fixture` - Repository（推荐，用于验证）
- `db_transaction` - 自动回滚（写入数据库时必需）
- `settings` - 配置对象（按需）

#### 3. 测试步骤组织

```python
with step("步骤1: 准备数据"):
    # 准备测试数据
    pass

with step("步骤2: 调用API"):
    response = api.some_method(request)
    attach_json(response.model_dump(), name="API响应")

with step("步骤3: 验证响应"):
    assert response.success
    assert response.data is not None

with step("步骤4: 验证数据库"):
    db_data = repository.find_by_id(response.data.id)
    assert db_data is not None
```

#### 4. 双重验证模式（推荐）⭐

```python
def test_create_card(
    master_card_api,
    card_repository,
    db_transaction,
):
    """测试创建卡片（双重验证）"""

    # 步骤1: API调用
    request = MasterCardCreateRequest(...)
    response = master_card_api.create_cards(request)

    # 验证1: API响应
    assert response.success
    assert len(response.data.card_nos) == 1

    # 验证2: 数据库数据
    card = card_repository.find_by_card_no(response.data.card_nos[0])
    assert card is not None
    assert card["status"] == 1
    assert card["user_id"] == settings.test_user_id
```

**为什么需要Repository验证？**
1. API可能不返回完整数据
2. 验证数据真实写入数据库
3. 验证所有字段值正确
4. 增强测试可靠性

### 完整文档

- **测试用例模板**: [已验证最佳实践](../user-guide/VERIFIED_BEST_PRACTICES.md#6-测试用例编写最佳实践)
- **三层架构**: [已验证最佳实践](../user-guide/VERIFIED_BEST_PRACTICES.md#5-三层架构最佳实践)
- **Fixtures管理**: [已验证最佳实践](../user-guide/VERIFIED_BEST_PRACTICES.md#4-fixtures和事务管理最佳实践)

---

## 🔗 相关文档

### v3架构文档
- [Clients API](clients.md) - HTTP客户端详细API（含BaseAPI最佳实践）
- [Databases API](databases.md) - Database、Redis详细API（含Repository最佳实践）
- [Patterns API](patterns.md) - Builder模式（v2兼容）

### 已验证最佳实践
- [VERIFIED_BEST_PRACTICES.md](../user-guide/VERIFIED_BEST_PRACTICES.md) - 完整的已验证最佳实践（推荐阅读）⭐

### v2兼容文档
- [Core API参考](core.md) - v2版HttpClient、Database

### 其他资源
- [配置管理](../user-guide/configuration.md) - pytest配置说明
- [快速入门](../getting-started/quickstart.md) - 实战示例
- [v2→v3迁移](../migration/v2-to-v3.md) - Builder路径迁移

---

**返回**: [API参考首页](README.md) | [文档首页](../README.md)
