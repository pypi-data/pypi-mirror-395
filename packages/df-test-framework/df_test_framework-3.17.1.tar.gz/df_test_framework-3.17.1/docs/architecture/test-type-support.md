# 测试类型支持架构

本文档详细介绍DF Test Framework如何支持不同类型的测试，包括API测试、UI测试、性能测试等。

## 📋 目录

- [测试类型概览](#测试类型概览)
- [API测试支持](#api测试支持)
- [UI测试支持](#ui测试支持)
- [性能测试支持](#性能测试支持)
- [数据库测试支持](#数据库测试支持)
- [集成测试支持](#集成测试支持)
- [测试数据管理](#测试数据管理)

## 🎯 测试类型概览

### 支持的测试类型矩阵

| 测试类型 | 当前支持 | 核心组件 | 典型场景 |
|---------|---------|----------|----------|
| **API测试** | ✅ 完整支持 | HttpClient | REST API、GraphQL |
| **数据库测试** | ✅ 完整支持 | Database | 数据完整性、SQL逻辑 |
| **缓存测试** | ✅ 完整支持 | RedisClient | 缓存策略、过期时间 |
| **UI测试** | 🔄 扩展支持 | Extension | Web、移动端UI |
| **性能测试** | 🔄 扩展支持 | Extension | 压测、负载测试 |
| **安全测试** | 🔄 扩展支持 | Extension | 认证、授权、注入 |
| **集成测试** | ✅ 完整支持 | 所有组件 | 多服务协作 |

**图例**:
- ✅ 完整支持: 框架核心提供
- 🔄 扩展支持: 通过Extension实现

### 测试分层架构

```
┌─────────────────────────────────────────┐
│     测试层级                             │
├─────────────────────────────────────────┤
│  E2E测试 (UI + API + Database)         │  ← 最接近用户
├─────────────────────────────────────────┤
│  集成测试 (API + Database + Redis)      │
├─────────────────────────────────────────┤
│  接口测试 (API)                         │
├─────────────────────────────────────────┤
│  单元测试 (Repository, Builder)         │  ← 最快速
└─────────────────────────────────────────┘
```

## 🌐 API测试支持

### 核心架构

API测试是DF Test Framework的核心能力，基于以下组件：

```
HttpClient (httpx)
    ├── 自动重试
    ├── 超时控制
    ├── 请求/响应日志
    ├── 数据脱敏
    └── Session管理
```

### 设计特性

#### 1. 自动重试机制

**实现原理**:

```python
# src/df_test_framework/core/http/client.py
class HttpClient:
    def _execute_with_retry(self, method: str, url: str, **kwargs):
        last_exception = None

        for attempt in range(self._max_retries + 1):
            try:
                response = self._client.request(method, url, **kwargs)

                # 只重试5xx服务器错误
                if response.status_code < 500:
                    return response

                if attempt < self._max_retries:
                    self._logger.warning(
                        f"请求失败 ({response.status_code})，"
                        f"将在 {self._retry_delay * (2 ** attempt)}s 后重试..."
                    )
            except (httpx.ConnectError, httpx.TimeoutException) as e:
                last_exception = e
                if attempt < self._max_retries:
                    self._logger.warning(f"连接错误，将重试: {e}")

            if attempt < self._max_retries:
                delay = self._retry_delay * (2 ** attempt)  # 指数退避
                time.sleep(delay)

        raise last_exception or httpx.HTTPError("Max retries exceeded")
```

**配置项**:

```python
class HTTPConfig(BaseModel):
    max_retries: int = 3        # 最大重试次数
    retry_delay: float = 1.0    # 初始重试延迟（秒）
    retry_on_status: List[int] = [500, 502, 503, 504]  # 重试的状态码
```

#### 2. 数据脱敏

**脱敏字段**:

```python
DEFAULT_SANITIZE_PATTERNS = [
    "password",
    "token",
    "secret",
    "api_key",
    "apikey",
    "authorization",
    "auth",
    "credential",
]

def sanitize_data(data: dict, patterns: List[str]) -> dict:
    """递归脱敏敏感数据"""
    result = {}
    for key, value in data.items():
        if any(pattern in key.lower() for pattern in patterns):
            result[key] = "***SANITIZED***"
        elif isinstance(value, dict):
            result[key] = sanitize_data(value, patterns)
        elif isinstance(value, list):
            result[key] = [
                sanitize_data(item, patterns) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            result[key] = value
    return result
```

**使用示例**:

```python
# 请求日志（自动脱敏）
http.post("/api/login", json={
    "username": "john",
    "password": "secret123"  # ← 日志中会被替换为 ***SANITIZED***
})

# 日志输出:
# POST /api/login {"username": "john", "password": "***SANITIZED***"}
```

#### 3. Session管理

**Cookie自动管理**:

```python
http = runtime.http_client()

# 登录（保存cookie）
response = http.post("/api/login", json=credentials)

# 后续请求自动携带cookie
response = http.get("/api/users/me")  # 自动带上登录cookie
```

### API测试模式

#### 模式1: 基础API测试

```python
def test_get_user(http_client):
    """测试获取用户API"""
    response = http_client.get("/api/users/1")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "username" in data
```

#### 模式2: 参数化API测试

```python
@pytest.mark.parametrize("user_id,expected_status", [
    (1, 200),       # 正常用户
    (9999, 404),    # 不存在的用户
    (-1, 400),      # 无效ID
    ("abc", 400),   # 错误类型
])
def test_get_user_various_inputs(http_client, user_id, expected_status):
    response = http_client.get(f"/api/users/{user_id}")
    assert response.status_code == expected_status
```

#### 模式3: 完整CRUD测试

```python
def test_user_crud_flow(http_client, database):
    """完整的用户CRUD测试流程"""

    # 1. Create
    create_data = {"username": "testuser", "email": "test@example.com"}
    response = http_client.post("/api/users", json=create_data)
    assert response.status_code == 201
    user_id = response.json()["id"]

    # 2. Read
    response = http_client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

    # 3. Update
    update_data = {"email": "newemail@example.com"}
    response = http_client.patch(f"/api/users/{user_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["email"] == "newemail@example.com"

    # 4. Delete
    response = http_client.delete(f"/api/users/{user_id}")
    assert response.status_code == 204

    # 5. Verify deletion
    response = http_client.get(f"/api/users/{user_id}")
    assert response.status_code == 404
```

#### 模式4: GraphQL API测试

```python
def test_graphql_query(http_client):
    """测试GraphQL查询"""
    query = """
    query GetUser($id: ID!) {
        user(id: $id) {
            id
            username
            email
            posts {
                title
                content
            }
        }
    }
    """

    response = http_client.post("/graphql", json={
        "query": query,
        "variables": {"id": "1"}
    })

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert data["data"]["user"]["id"] == "1"
```

## 🖥️ UI测试支持

### 架构设计

UI测试通过Extension实现，支持多种UI测试框架：

```
UI测试扩展层
├── SeleniumExtension (Web UI)
├── PlaywrightExtension (Web UI)
├── AppiumExtension (Mobile UI)
└── CustomUIExtension (自定义)
```

### Selenium扩展示例

**扩展实现**:

```python
# extensions/ui/selenium_extension.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from df_test_framework.extensions import hookimpl
from df_test_framework import SingletonProvider

class SeleniumDriver:
    """Selenium驱动封装"""

    def __init__(self, settings, logger):
        self.settings = settings
        self.logger = logger

        # 初始化WebDriver
        options = webdriver.ChromeOptions()
        if settings.ui.headless:
            options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(settings.ui.implicit_wait)
        self.wait = WebDriverWait(
            self.driver,
            settings.ui.explicit_wait
        )

        self.logger.info("Selenium驱动已初始化")

    def get(self, url: str):
        """访问URL"""
        full_url = f"{self.settings.ui.base_url}{url}"
        self.logger.info(f"访问页面: {full_url}")
        self.driver.get(full_url)

    def find_element(self, by: By, value: str):
        """查找元素（带等待）"""
        return self.wait.until(
            EC.presence_of_element_located((by, value))
        )

    def screenshot(self, filename: str):
        """截图"""
        self.driver.save_screenshot(filename)
        self.logger.info(f"截图已保存: {filename}")

    def close(self):
        """关闭浏览器"""
        self.driver.quit()

class SeleniumExtension:
    @hookimpl
    def df_providers(self, settings, logger):
        return {
            "selenium": SingletonProvider(
                lambda rt: SeleniumDriver(rt.settings, rt.logger)
            )
        }
```

**配置**:

```python
class UITestSettings(FrameworkSettings):
    class UIConfig(BaseModel):
        base_url: str = "http://localhost:3000"
        headless: bool = True
        implicit_wait: int = 10
        explicit_wait: int = 20

    ui: UIConfig = Field(default_factory=UIConfig)
```

**使用示例**:

```python
def test_login_ui(runtime):
    """UI登录测试"""
    selenium = runtime.get("selenium")

    # 访问登录页
    selenium.get("/login")

    # 输入用户名
    username_input = selenium.find_element(By.ID, "username")
    username_input.send_keys("testuser")

    # 输入密码
    password_input = selenium.find_element(By.ID, "password")
    password_input.send_keys("password123")

    # 点击登录按钮
    login_button = selenium.find_element(By.ID, "login-btn")
    login_button.click()

    # 验证登录成功
    welcome_msg = selenium.find_element(By.CLASS_NAME, "welcome-message")
    assert "欢迎" in welcome_msg.text

    # 截图
    selenium.screenshot("login_success.png")
```

### Playwright扩展示例

**扩展实现**:

```python
from playwright.sync_api import sync_playwright, Page
from df_test_framework.extensions import hookimpl
from df_test_framework import SingletonProvider

class PlaywrightDriver:
    """Playwright驱动封装"""

    def __init__(self, settings, logger):
        self.settings = settings
        self.logger = logger

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=settings.ui.headless
        )
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

        self.logger.info("Playwright驱动已初始化")

    def goto(self, url: str):
        full_url = f"{self.settings.ui.base_url}{url}"
        self.logger.info(f"访问页面: {full_url}")
        self.page.goto(full_url)

    def screenshot(self, filename: str):
        self.page.screenshot(path=filename)

    def close(self):
        self.browser.close()
        self.playwright.stop()

class PlaywrightExtension:
    @hookimpl
    def df_providers(self, settings, logger):
        return {
            "playwright": SingletonProvider(
                lambda rt: PlaywrightDriver(rt.settings, rt.logger)
            )
        }
```

**使用示例**:

```python
def test_login_ui_playwright(runtime):
    """Playwright UI测试"""
    pw = runtime.get("playwright")

    pw.goto("/login")
    pw.page.fill("#username", "testuser")
    pw.page.fill("#password", "password123")
    pw.page.click("#login-btn")

    # 等待跳转
    pw.page.wait_for_url("**/dashboard")
    assert pw.page.title() == "Dashboard"
```

## ⚡ 性能测试支持

### Locust集成扩展

**扩展实现**:

```python
# extensions/performance/locust_extension.py
from locust import HttpUser, task, between
from df_test_framework.extensions import hookimpl

class APIPerformanceUser(HttpUser):
    """Locust性能测试用户"""

    wait_time = between(1, 3)  # 请求间隔1-3秒

    def on_start(self):
        """测试开始时执行（登录）"""
        response = self.client.post("/api/login", json={
            "username": "testuser",
            "password": "password123"
        })
        self.token = response.json()["token"]

    @task(3)  # 权重3
    def get_users(self):
        """获取用户列表"""
        self.client.get(
            "/api/users",
            headers={"Authorization": f"Bearer {self.token}"}
        )

    @task(2)  # 权重2
    def get_user_detail(self):
        """获取用户详情"""
        user_id = random.randint(1, 100)
        self.client.get(
            f"/api/users/{user_id}",
            headers={"Authorization": f"Bearer {self.token}"}
        )

    @task(1)  # 权重1
    def create_order(self):
        """创建订单"""
        self.client.post(
            "/api/orders",
            json={"product_id": 1, "quantity": 2},
            headers={"Authorization": f"Bearer {self.token}"}
        )

class LocustExtension:
    @hookimpl
    def df_post_bootstrap(self, runtime):
        runtime.logger.info("Locust性能测试扩展已加载")
        # 可以从runtime获取配置
        # 例如: base_url = runtime.settings.http.base_url
```

**运行性能测试**:

```bash
# 启动Locust Web UI
locust -f tests/performance/test_api_performance.py \
    --host=http://localhost:8000 \
    --users=100 \
    --spawn-rate=10

# 无头模式
locust -f tests/performance/test_api_performance.py \
    --host=http://localhost:8000 \
    --users=1000 \
    --spawn-rate=100 \
    --run-time=5m \
    --headless
```

### 自定义性能监控扩展

```python
import time
import statistics
from collections import defaultdict

class PerformanceMonitor:
    """性能监控器"""

    def __init__(self):
        self.metrics = defaultdict(list)

    def record(self, operation: str, duration: float):
        """记录操作耗时"""
        self.metrics[operation].append(duration)

    def get_stats(self, operation: str) -> dict:
        """获取操作统计"""
        durations = self.metrics[operation]
        if not durations:
            return {}

        return {
            "count": len(durations),
            "avg": statistics.mean(durations),
            "median": statistics.median(durations),
            "p95": statistics.quantiles(durations, n=20)[18],  # 95分位
            "p99": statistics.quantiles(durations, n=100)[98],  # 99分位
            "min": min(durations),
            "max": max(durations),
        }

class PerformanceExtension:
    def __init__(self):
        self.monitor = PerformanceMonitor()

    @hookimpl
    def df_providers(self, settings, logger):
        return {
            "performance": SingletonProvider(lambda rt: self.monitor)
        }

    @hookimpl
    def df_post_bootstrap(self, runtime):
        # Hook HttpClient
        http = runtime.http_client()
        original_request = http.request

        def monitored_request(method, url, **kwargs):
            start = time.time()
            response = original_request(method, url, **kwargs)
            duration = time.time() - start

            operation = f"{method} {url}"
            self.monitor.record(operation, duration)

            return response

        http.request = monitored_request
```

**使用示例**:

```python
def test_api_performance(runtime, http_client):
    """API性能测试"""
    perf = runtime.get("performance")

    # 执行100次请求
    for _ in range(100):
        http_client.get("/api/users")

    # 获取统计
    stats = perf.get_stats("GET /api/users")

    # 断言性能要求
    assert stats["avg"] < 0.5, "平均响应时间应小于500ms"
    assert stats["p95"] < 1.0, "95分位响应时间应小于1s"
    assert stats["max"] < 2.0, "最大响应时间应小于2s"
```

## 🗄️ 数据库测试支持

### 核心能力

```
Database组件
├── 事务管理
├── 数据隔离
├── Fixture自动回滚
└── 测试数据清理
```

### 测试数据隔离

#### 模式1: 事务回滚

**Fixture实现**:

```python
# tests/conftest.py
@pytest.fixture
def db_transaction(database):
    """每个测试在独立事务中运行"""
    connection = database.engine.connect()
    transaction = connection.begin()

    # 创建session绑定到这个事务
    from sqlalchemy.orm import sessionmaker, scoped_session
    session_factory = sessionmaker(bind=connection)
    session = scoped_session(session_factory)

    yield session

    # 测试结束后回滚
    session.close()
    transaction.rollback()
    connection.close()
```

**使用示例**:

```python
def test_create_user(db_transaction):
    """测试创建用户（自动回滚）"""
    # 插入测试数据
    db_transaction.execute(
        "INSERT INTO users (username, email) VALUES (:u, :e)",
        {"u": "testuser", "e": "test@example.com"}
    )
    db_transaction.commit()

    # 验证插入
    result = db_transaction.execute(
        "SELECT * FROM users WHERE username = :u",
        {"u": "testuser"}
    ).first()
    assert result is not None

    # 测试结束后自动回滚，数据不会真正保存
```

#### 模式2: 标记清理

**Fixture实现**:

```python
@pytest.fixture
def clean_test_data(database):
    """清理测试数据"""
    yield

    # 测试后清理（删除username以test_开头的数据）
    database.execute("DELETE FROM users WHERE username LIKE 'test_%'")
    database.execute("DELETE FROM orders WHERE order_id LIKE 'TEST%'")
```

### 数据完整性测试

```python
def test_user_email_unique_constraint(database):
    """测试email唯一性约束"""
    email = "duplicate@example.com"

    # 第一次插入成功
    database.execute(
        "INSERT INTO users (username, email) VALUES (:u, :e)",
        {"u": "user1", "e": email}
    )

    # 第二次插入应该失败
    with pytest.raises(IntegrityError):
        database.execute(
            "INSERT INTO users (username, email) VALUES (:u, :e)",
            {"u": "user2", "e": email}
        )
```

### SQL逻辑测试

```python
def test_order_total_calculation(database):
    """测试订单总额计算SQL"""
    # 准备数据
    database.execute(
        "INSERT INTO orders (id, user_id, items) VALUES "
        "(1, 1, '[{\"price\": 100, \"qty\": 2}, {\"price\": 50, \"qty\": 1}]')"
    )

    # 测试SQL逻辑
    result = database.execute("""
        SELECT
            id,
            (SELECT SUM(
                (item->>'price')::numeric * (item->>'qty')::numeric
            ) FROM jsonb_array_elements(items::jsonb) AS item) AS total
        FROM orders
        WHERE id = 1
    """).first()

    assert result.total == 250  # 100*2 + 50*1 = 250
```

## 🔗 集成测试支持

### 多服务集成测试

**场景**: 测试用户注册流程（涉及多个服务和组件）

```python
def test_user_registration_integration(
    http_client,
    database,
    redis,
    runtime
):
    """完整的用户注册集成测试"""

    # 1. 准备：清理缓存
    redis.delete("verification_code:test@example.com")

    # 2. 发送验证码（HTTP API）
    response = http_client.post("/api/auth/send-code", json={
        "email": "test@example.com"
    })
    assert response.status_code == 200

    # 3. 验证：检查验证码已保存到Redis
    code = redis.get("verification_code:test@example.com")
    assert code is not None
    runtime.logger.info(f"验证码: {code}")

    # 4. 注册用户（HTTP API + 验证码）
    response = http_client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "verification_code": code
    })
    assert response.status_code == 201
    user_id = response.json()["user_id"]

    # 5. 验证：用户已保存到数据库
    user = database.execute(
        "SELECT * FROM users WHERE id = :id",
        {"id": user_id}
    ).first()
    assert user is not None
    assert user["username"] == "testuser"
    assert user["email"] == "test@example.com"
    assert user["status"] == "active"

    # 6. 验证：验证码已从Redis删除
    assert redis.get("verification_code:test@example.com") is None

    # 7. 登录测试
    response = http_client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "token" in response.json()
```

## 📊 测试数据管理

### Builder + Repository模式

**完整示例**:

```python
# 1. 定义Builder
class UserBuilder(DictBuilder):
    def __init__(self):
        super().__init__()
        self.with_username(f"user_{uuid.uuid4().hex[:8]}")
        self.with_email(f"user_{uuid.uuid4().hex[:8]}@example.com")
        self.with_status("active")

    def with_username(self, username: str):
        return self.set("username", username)

    def with_email(self, email: str):
        return self.set("email", email)

    def with_status(self, status: str):
        return self.set("status", status)

# 2. 定义Repository
class UserRepository(BaseRepository):
    def __init__(self, database):
        super().__init__(database)
        self.table_name = "users"

    def create_user(self, data: dict) -> int:
        return self.create(data)

# 3. 在测试中使用
def test_with_builder_repo(database):
    repo = UserRepository(database)

    # 构建测试数据
    user_data = (
        UserBuilder()
        .with_username("admin")
        .with_email("admin@example.com")
        .build()
    )

    # 保存到数据库
    user_id = repo.create_user(user_data)

    # 查询验证
    user = repo.find_by_id(user_id)
    assert user["username"] == "admin"
```

### 测试数据工厂

```python
class TestDataFactory:
    """测试数据工厂"""

    def __init__(self, database, redis):
        self.database = database
        self.redis = redis
        self.user_repo = UserRepository(database)
        self.order_repo = OrderRepository(database)

    def create_user(self, **overrides):
        """创建测试用户"""
        data = UserBuilder().merge(overrides).build()
        user_id = self.user_repo.create_user(data)
        return self.user_repo.find_by_id(user_id)

    def create_order(self, user_id: int, **overrides):
        """创建测试订单"""
        data = (
            OrderBuilder()
            .with_user_id(user_id)
            .merge(overrides)
            .build()
        )
        order_id = self.order_repo.create_order(data)
        return self.order_repo.find_by_id(order_id)

    def create_user_with_orders(self, order_count: int = 3):
        """创建用户和多个订单"""
        user = self.create_user()
        orders = [
            self.create_order(user["id"])
            for _ in range(order_count)
        ]
        return user, orders

# Fixture
@pytest.fixture
def test_factory(database, redis):
    return TestDataFactory(database, redis)

# 使用
def test_user_orders(test_factory):
    user, orders = test_factory.create_user_with_orders(5)
    assert len(orders) == 5
    assert all(order["user_id"] == user["id"] for order in orders)
```

## 🔗 相关文档

- [API测试指南](../user-guide/api-testing.md)
- [HttpClient API](../api-reference/core.md#httpclient)
- [Database API](../api-reference/core.md#database)
- [扩展点文档](extension-points.md)

---

**返回**: [架构文档](README.md) | [文档首页](../README.md)
