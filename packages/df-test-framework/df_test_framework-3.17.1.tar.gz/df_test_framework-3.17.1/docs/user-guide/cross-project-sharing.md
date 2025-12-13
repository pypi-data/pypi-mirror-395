# 跨项目共享最佳实践

如何在多个测试项目之间高效复用框架和通用代码。

---

## 📋 目录

- [概述](#概述)
- [配置共享](#配置共享)
- [通用组件共享](#通用组件共享)
- [扩展共享](#扩展共享)
- [测试数据共享](#测试数据共享)
- [完整示例](#完整示例)
- [最佳实践](#最佳实践)

---

## 概述

### 为什么需要跨项目共享？

在微服务架构下，通常有多个测试项目（如订单测试、用户测试、支付测试等），这些项目需要：

- ✅ **复用通用配置** - 数据库、Redis、日志等配置
- ✅ **复用通用组件** - Repository、Builder、API封装
- ✅ **复用扩展功能** - 监控、性能分析、Allure增强
- ✅ **保持一致性** - 统一的测试风格和代码结构

### 共享架构

```
框架层 (df-test-framework)
  ↓ 提供基础能力
共享层 (共享的Repository、Builder、Extensions)
  ↓ 各项目复用
项目层 (order-test, user-test, payment-test)
  ↓ 业务特定代码
```

---

## 配置共享

### 方式1: 继承FrameworkSettings（推荐）

**场景**: 所有项目共享相同的配置结构

```python
# 项目1: order-test/src/order_test/config/settings.py
from df_test_framework import FrameworkSettings
from pydantic import Field

class OrderTestSettings(FrameworkSettings):
    """订单测试项目配置"""

    # 业务特定配置
    order_api_key: str = Field(default="")
    test_merchant_id: str = Field(default="merchant_001")
```

```python
# 项目2: user-test/src/user_test/config/settings.py
from df_test_framework import FrameworkSettings
from pydantic import Field

class UserTestSettings(FrameworkSettings):
    """用户测试项目配置"""

    # 业务特定配置
    sms_api_key: str = Field(default="")
    test_user_pool: list[str] = Field(default_factory=list)
```

**优势**:
- ✅ 自动继承框架的所有配置（HTTP、Database、Redis等）
- ✅ 只需扩展业务特定配置
- ✅ 环境变量自动加载（使用`APP_`前缀）

---

### 方式2: 共享配置基类

**场景**: 多个项目需要共享额外的通用配置

```python
# 1. 创建共享配置基类 (可以放在框架或独立共享包中)
# shared/config/base.py
from df_test_framework import FrameworkSettings
from pydantic import Field, BaseModel

class MicroserviceConfig(BaseModel):
    """微服务通用配置"""
    service_mesh_url: str = Field(default="http://mesh.example.com")
    trace_enabled: bool = Field(default=True)
    metrics_port: int = Field(default=9090)

class SharedTestSettings(FrameworkSettings):
    """所有测试项目的共享基类"""

    # 共享的微服务配置
    microservice: MicroserviceConfig = Field(
        default_factory=MicroserviceConfig
    )

    # 共享的认证配置
    auth_token: str = Field(default="")
    admin_token: str = Field(default="")
```

```python
# 2. 各项目继承共享基类
# order-test/src/order_test/config/settings.py
from shared.config.base import SharedTestSettings
from pydantic import Field

class OrderTestSettings(SharedTestSettings):
    """订单测试配置（继承共享配置）"""

    # 订单特定配置
    order_api_key: str = Field(default="")
```

```python
# user-test/src/user_test/config/settings.py
from shared.config.base import SharedTestSettings
from pydantic import Field

class UserTestSettings(SharedTestSettings):
    """用户测试配置（继承共享配置）"""

    # 用户特定配置
    sms_api_key: str = Field(default="")
```

**优势**:
- ✅ 所有项目共享通用配置
- ✅ 配置变更一次，所有项目生效
- ✅ 保持配置一致性

---

### 环境变量管理

**共享.env模板**:

```bash
# shared/.env.template - 所有项目共享的环境变量模板

# 框架配置
APP_ENV=test
APP_DEBUG=false

# HTTP配置
APP_HTTP__BASE_URL=https://api-test.example.com
APP_HTTP__TIMEOUT=60

# 数据库配置
APP_DB__HOST=localhost
APP_DB__PORT=3306
APP_DB__USER=root
APP_DB__PASSWORD=secret

# Redis配置
APP_REDIS__HOST=localhost
APP_REDIS__PORT=6379

# 微服务共享配置
APP_MICROSERVICE__SERVICE_MESH_URL=http://mesh.example.com
APP_MICROSERVICE__TRACE_ENABLED=true

# 认证配置
APP_AUTH_TOKEN=shared_auth_token
APP_ADMIN_TOKEN=shared_admin_token
```

**各项目添加特定配置**:

```bash
# order-test/.env
# 引用共享配置
source ../shared/.env.template

# 订单特定配置
APP_ORDER_API_KEY=order_specific_key
APP_TEST_MERCHANT_ID=merchant_001
```

```bash
# user-test/.env
# 引用共享配置
source ../shared/.env.template

# 用户特定配置
APP_SMS_API_KEY=sms_specific_key
```

---

## 通用组件共享

### Repository共享

**场景**: 多个项目需要访问相同的数据库表

#### 方式1: 框架内置通用Repository

```python
# 在框架中定义通用Repository
# df-test-framework/src/df_test_framework/patterns/repositories/common.py
from df_test_framework import BaseRepository
from typing import Optional, List, Dict, Any

class UserRepository(BaseRepository):
    """用户Repository（所有项目共享）"""

    def __init__(self, db):
        super().__init__(db, table_name="users")

    def find_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """根据用户名查找"""
        return self.find_one({"username": username})

    def find_active_users(self) -> List[Dict[str, Any]]:
        """查找活跃用户"""
        return self.find_all(
            {"status": "ACTIVE"},
            order_by="created_at DESC"
        )

class OrderRepository(BaseRepository):
    """订单Repository（所有项目共享）"""

    def __init__(self, db):
        super().__init__(db, table_name="orders")

    def find_by_order_no(self, order_no: str) -> Optional[Dict[str, Any]]:
        """根据订单号查找"""
        return self.find_one({"order_no": order_no})

    def find_by_user_id(self, user_id: str) -> List[Dict[str, Any]]:
        """查找用户的所有订单"""
        return self.find_all({"user_id": user_id})
```

```python
# 在各项目中使用
# order-test/tests/test_order.py
from df_test_framework.patterns.repositories.common import (
    UserRepository,
    OrderRepository
)

def test_create_order(database):
    """测试创建订单"""
    user_repo = UserRepository(database)
    order_repo = OrderRepository(database)

    # 查找测试用户
    user = user_repo.find_by_username("test_user")

    # 创建订单
    order_id = order_repo.create({
        "order_no": "ORD001",
        "user_id": user["id"],
        "amount": 100.0
    })
```

#### 方式2: 共享包中的Repository

```python
# shared-components/src/shared_components/repositories/__init__.py
from df_test_framework import BaseRepository
from typing import Optional, List, Dict, Any

class CommonUserRepository(BaseRepository):
    """共享的用户Repository"""

    def __init__(self, db):
        super().__init__(db, table_name="users")

    # 通用方法...
```

```python
# 安装共享包到各项目
# pyproject.toml
dependencies = [
    "df-test-framework",
    "shared-components @ file:///../shared-components",
]
```

---

### Builder共享

**场景**: 多个项目需要构建相同的测试数据

```python
# df-test-framework或共享包中定义通用Builder
# shared_components/builders/common.py
from df_test_framework import DictBuilder

class UserBuilder(DictBuilder):
    """用户数据Builder（所有项目共享）"""

    def __init__(self):
        super().__init__()
        # 默认值
        self.set("username", "test_user")
        self.set("email", "test@example.com")
        self.set("status", "ACTIVE")
        self.set("age", 25)

    def with_username(self, username: str):
        """设置用户名"""
        self.set("username", username)
        return self

    def with_email(self, email: str):
        """设置邮箱"""
        self.set("email", email)
        return self

    def as_vip(self):
        """设置为VIP用户"""
        self.set("vip_level", 5)
        self.set("vip_expires_at", "2026-12-31")
        return self

    def as_inactive(self):
        """设置为非活跃状态"""
        self.set("status", "INACTIVE")
        return self

class OrderBuilder(DictBuilder):
    """订单数据Builder（所有项目共享）"""

    def __init__(self):
        super().__init__()
        self.set("order_no", "ORD_DEFAULT")
        self.set("user_id", "user_001")
        self.set("amount", 100.0)
        self.set("status", "PENDING")

    def with_order_no(self, order_no: str):
        self.set("order_no", order_no)
        return self

    def with_amount(self, amount: float):
        self.set("amount", amount)
        return self

    def as_paid(self):
        """设置为已支付"""
        self.set("status", "PAID")
        self.set("paid_at", "2025-11-01 10:00:00")
        return self
```

```python
# 在各项目中使用
# order-test/tests/test_order.py
from shared_components.builders.common import UserBuilder, OrderBuilder

def test_order_workflow(order_api, user_repo, order_repo):
    """测试订单流程"""

    # 构建用户数据
    user_data = (
        UserBuilder()
        .with_username("test_user_001")
        .with_email("user001@example.com")
        .as_vip()
        .build()
    )

    # 构建订单数据
    order_data = (
        OrderBuilder()
        .with_order_no("ORD_VIP_001")
        .with_amount(500.0)
        .build()
    )

    # 执行测试...
```

---

## 扩展共享

### 方式1: 框架内置扩展

```python
# 在框架中定义通用扩展
# df-test-framework/src/df_test_framework/extensions/builtin/monitoring.py
from df_test_framework import hookimpl
import time

class APIMonitoringExtension:
    """API监控扩展（所有项目共享）"""

    def __init__(self):
        self.request_count = 0
        self.error_count = 0

    @hookimpl
    def df_post_bootstrap(self, runtime):
        """Bootstrap后初始化监控"""
        logger = runtime.logger
        logger.info("API监控扩展已启动")

        # 包装HTTP客户端
        http = runtime.http_client()
        self._wrap_http(http, logger)

    def _wrap_http(self, http, logger):
        """包装HTTP客户端记录统计"""
        original_request = http.request

        def monitored_request(method, url, **kwargs):
            self.request_count += 1
            start = time.time()
            try:
                response = original_request(method, url, **kwargs)
                duration = time.time() - start
                logger.info(
                    f"API: {method} {url}, "
                    f"耗时: {duration:.3f}s"
                )
                return response
            except Exception as e:
                self.error_count += 1
                logger.error(f"API失败: {method} {url}, {str(e)}")
                raise

        http.request = monitored_request
```

```python
# 各项目使用内置扩展
# order-test/tests/conftest.py
from df_test_framework import Bootstrap
from df_test_framework.extensions.builtin.monitoring import APIMonitoringExtension
from order_test.config.settings import OrderTestSettings

runtime = (
    Bootstrap()
    .with_settings(OrderTestSettings)
    .with_plugin(APIMonitoringExtension())  # 使用框架内置扩展
    .build()
    .run()
)
```

---

### 方式2: 共享扩展包

```python
# shared-extensions/src/shared_extensions/allure_enhancement.py
from df_test_framework import hookimpl
import allure

class AllureEnhancementExtension:
    """Allure报告增强（所有项目共享）"""

    @hookimpl
    def df_post_bootstrap(self, runtime):
        """添加环境信息到Allure"""
        settings = runtime.settings

        # 添加通用环境信息
        allure.environment(
            environment=settings.env,
            api_base_url=settings.http.base_url,
            database_host=settings.db.host,
        )

        # 添加框架版本
        import df_test_framework
        allure.environment(
            framework_version=df_test_framework.__version__
        )
```

```python
# 各项目使用
from shared_extensions.allure_enhancement import AllureEnhancementExtension

runtime = (
    Bootstrap()
    .with_settings(MySettings)
    .with_plugin(AllureEnhancementExtension())
    .build()
    .run()
)
```

---

## 测试数据共享

### Fixture共享

```python
# shared/fixtures/common.py
import pytest
from shared_components.builders.common import UserBuilder, OrderBuilder
from shared_components.repositories.common import UserRepository, OrderRepository

@pytest.fixture
def user_builder():
    """通用用户Builder"""
    return UserBuilder()

@pytest.fixture
def order_builder():
    """通用订单Builder"""
    return OrderBuilder()

@pytest.fixture
def user_repo(database):
    """通用用户Repository"""
    return UserRepository(database)

@pytest.fixture
def order_repo(database):
    """通用订单Repository"""
    return OrderRepository(database)

@pytest.fixture
def test_user(user_repo, user_builder):
    """创建测试用户（自动清理）"""
    user_data = user_builder.with_username("auto_test_user").build()
    user_id = user_repo.create(user_data)

    yield user_repo.find_by_id(user_id)

    # 清理
    user_repo.delete({"id": user_id})
```

```python
# 在各项目中使用共享fixtures
# order-test/tests/conftest.py
pytest_plugins = [
    "df_test_framework.testing.fixtures.core",
    "shared.fixtures.common",  # 导入共享fixtures
]
```

```python
# order-test/tests/test_order.py
def test_create_order(order_api, test_user, order_builder):
    """测试创建订单（使用共享fixtures）"""

    # test_user是共享fixture，自动创建和清理
    order_data = (
        order_builder
        .with_order_no(f"ORD_{test_user['id']}_001")
        .build()
    )

    response = order_api.create(order_data)
    assert response.status_code == 201
```

---

## 完整示例

### 项目结构

```
qa/
├── df-test-framework/          # 框架（Git仓库）
│   └── src/df_test_framework/
│       ├── core/
│       ├── patterns/
│       └── extensions/
│
├── shared-components/          # 共享组件（Git仓库或包）
│   └── src/shared_components/
│       ├── config/
│       │   └── base.py         # SharedTestSettings
│       ├── repositories/
│       │   └── common.py       # UserRepository, OrderRepository
│       ├── builders/
│       │   └── common.py       # UserBuilder, OrderBuilder
│       ├── fixtures/
│       │   └── common.py       # 共享fixtures
│       └── extensions/
│           └── monitoring.py   # 共享扩展
│
├── order-test/                 # 订单测试项目
│   ├── src/order_test/
│   │   ├── config/
│   │   │   └── settings.py     # OrderTestSettings(继承SharedTestSettings)
│   │   ├── apis/
│   │   └── fixtures/
│   └── tests/
│       └── test_order.py
│
└── user-test/                  # 用户测试项目
    ├── src/user_test/
    │   ├── config/
    │   │   └── settings.py     # UserTestSettings(继承SharedTestSettings)
    │   ├── apis/
    │   └── fixtures/
    └── tests/
        └── test_user.py
```

---

### 共享组件配置

```toml
# shared-components/pyproject.toml
[project]
name = "shared-components"
version = "1.0.0"
dependencies = [
    "df-test-framework>=2.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

---

### 项目依赖配置

```toml
# order-test/pyproject.toml
[project]
name = "order-test"
dependencies = [
    "df-test-framework>=2.0.0",
    "shared-components @ file:///../shared-components",  # 本地开发
]

# user-test/pyproject.toml
[project]
name = "user-test"
dependencies = [
    "df-test-framework>=2.0.0",
    "shared-components @ file:///../shared-components",  # 本地开发
]
```

---

### 完整测试示例

```python
# order-test/tests/test_order.py
import pytest
from shared_components.builders.common import UserBuilder, OrderBuilder
from shared_components.repositories.common import OrderRepository

@pytest.mark.smoke
def test_create_order_workflow(
    http_client,
    database,
    test_user,      # 共享fixture
    order_builder,  # 共享fixture
):
    """测试订单创建流程"""

    # 1. 准备订单数据（使用共享Builder）
    order_data = (
        order_builder
        .with_order_no(f"ORD_{test_user['id']}_001")
        .with_amount(299.9)
        .build()
    )

    # 2. 调用API创建订单
    response = http_client.post("/orders", json=order_data)
    assert response.status_code == 201
    order = response.json()

    # 3. 验证数据库（使用共享Repository）
    order_repo = OrderRepository(database)
    db_order = order_repo.find_by_order_no(order["order_no"])

    assert db_order is not None
    assert db_order["amount"] == 299.9
    assert db_order["user_id"] == test_user["id"]
```

---

## 最佳实践

### 1. 共享组件版本管理

✅ **推荐做法**:
```toml
# 使用语义化版本
dependencies = [
    "shared-components>=1.0.0,<2.0.0",
]
```

❌ **避免**:
```toml
# 不要锁定具体版本（除非有特殊原因）
dependencies = [
    "shared-components==1.0.0",
]
```

---

### 2. 共享范围控制

✅ **共享通用逻辑**:
- 通用Repository（用户、订单等）
- 通用Builder（标准数据结构）
- 通用扩展（监控、日志增强）
- 通用配置（数据库、Redis等）

❌ **不要共享业务逻辑**:
- 特定业务的API封装
- 特定业务的测试用例
- 特定业务的验证逻辑

---

### 3. 命名约定

```python
# ✅ 好的命名：明确标识为共享组件
class CommonUserRepository(BaseRepository):
    pass

class SharedAllureExtension:
    pass

# ❌ 避免：容易与项目特定组件混淆
class UserRepository(BaseRepository):  # 哪个项目的？
    pass
```

---

### 4. 文档维护

每个共享组件都应该有清晰的文档：

```python
# shared-components/src/shared_components/repositories/common.py

class UserRepository(BaseRepository):
    """用户Repository（所有项目共享）

    提供通用的用户数据访问方法。

    Usage:
        ```python
        from shared_components.repositories.common import UserRepository

        repo = UserRepository(database)
        user = repo.find_by_username("test_user")
        ```

    Available Methods:
        - find_by_username(username): 根据用户名查找
        - find_active_users(): 查找活跃用户
        - find_vip_users(): 查找VIP用户

    Version: 1.0.0
    Updated: 2025-11-01
    """
```

---

### 5. 依赖管理策略

**本地开发**:
```toml
dependencies = [
    "shared-components @ file:///../shared-components",
]
```

**CI/CD环境**:
```toml
dependencies = [
    "shared-components @ git+https://github.com/org/shared-components.git@v1.0.0",
]
```

**生产环境**:
```toml
dependencies = [
    "shared-components>=1.0.0,<2.0.0",  # 从PyPI安装
]
```

---

### 6. 变更管理

**共享组件变更流程**:

1. **评估影响** - 变更是否影响所有项目？
2. **版本升级** - 破坏性变更升级主版本
3. **通知团队** - 提前通知所有使用项目
4. **文档更新** - 更新变更日志和迁移指南
5. **逐步升级** - 各项目逐步升级，不要强制

---

### 7. 测试策略

**共享组件也需要测试**:

```python
# shared-components/tests/test_user_repository.py
import pytest
from shared_components.repositories.common import UserRepository

def test_find_by_username(database):
    """测试查找用户"""
    repo = UserRepository(database)

    # 创建测试数据
    user_id = repo.create({"username": "test", "email": "test@example.com"})

    # 测试查找
    user = repo.find_by_username("test")
    assert user is not None
    assert user["email"] == "test@example.com"

    # 清理
    repo.delete({"id": user_id})
```

---

## 🔗 相关文档

- [Multi-Repo管理指南](multi-repo.md) - 多仓库Git管理
- [配置管理](configuration.md) - 配置详解
- [扩展系统](extensions.md) - 扩展开发
- [Patterns API](../api-reference/patterns.md) - Builder和Repository
- [Infrastructure API](../api-reference/infrastructure.md) - Bootstrap和配置

---

**返回**: [用户指南首页](README.md) | [文档首页](../README.md)
