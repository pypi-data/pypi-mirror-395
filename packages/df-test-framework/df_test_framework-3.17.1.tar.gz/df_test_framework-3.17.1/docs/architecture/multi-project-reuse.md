# 多项目复用模式

本文档详细介绍如何在多个测试项目中高效复用DF Test Framework的组件和配置。

## 📋 目录

- [场景概述](#场景概述)
- [复用策略矩阵](#复用策略矩阵)
- [配置复用](#配置复用)
- [Repository复用](#repository复用)
- [Builder复用](#builder复用)
- [Extension复用](#extension复用)
- [Fixture复用](#fixture复用)
- [最佳实践](#最佳实践)

## 🎯 场景概述

### 典型多项目测试架构

```
company/
├── shared-test-lib/              # 共享测试库
│   ├── src/shared_test_lib/
│   │   ├── config.py             # 共享配置基类
│   │   ├── repositories/         # 共享Repository
│   │   ├── builders/             # 共享Builder
│   │   ├── extensions/           # 共享Extension
│   │   └── fixtures/             # 共享Fixtures
│   └── pyproject.toml
│
├── user-service-test/            # 用户服务测试项目
│   ├── tests/
│   │   ├── conftest.py           # 导入共享fixtures
│   │   └── test_users.py
│   ├── src/user_service_test/
│   │   ├── config.py             # 继承共享配置
│   │   └── repositories/         # 用户服务特定Repository
│   └── pyproject.toml            # 依赖shared-test-lib
│
├── order-service-test/           # 订单服务测试项目
│   ├── tests/
│   │   └── test_orders.py
│   ├── src/order_service_test/
│   │   ├── config.py
│   │   └── repositories/
│   └── pyproject.toml
│
└── payment-service-test/         # 支付服务测试项目
    ├── tests/
    │   └── test_payments.py
    └── pyproject.toml
```

### 复用需求

| 组件类型 | 复用需求 | 复用策略 |
|---------|---------|----------|
| **配置** | 统一环境、日志、数据库配置 | 继承FrameworkSettings |
| **Repository** | 跨服务共享数据访问（如UserRepository） | 发布为Python包 |
| **Builder** | 标准化测试数据构建 | 发布为Python包 |
| **Extension** | 统一监控、认证逻辑 | 发布为插件 |
| **Fixtures** | 标准化测试setup/teardown | 共享conftest.py |

## 📊 复用策略矩阵

### 复用程度分类

| 策略级别 | 复用范围 | 实现方式 | 适用场景 |
|---------|---------|----------|----------|
| **L1: 项目内复用** | 单个测试项目内 | 本地模块导入 | 小型单体项目 |
| **L2: 组内复用** | 同团队多个项目 | Monorepo或本地包 | 中型团队（3-5项目） |
| **L3: 跨组复用** | 跨团队多个项目 | PyPI私有仓库 | 大型组织（10+项目） |
| **L4: 开源复用** | 整个公司/社区 | PyPI公共仓库 | 通用测试工具 |

### 技术实现对比

| 方案 | 优点 | 缺点 | 最佳场景 |
|------|------|------|----------|
| **方案1: Git Submodule** | 版本控制、易于开发 | 依赖管理复杂 | 开发阶段 |
| **方案2: 本地包安装** | 简单直接 | 无版本管理 | 原型验证 |
| **方案3: 私有PyPI** | 版本管理、依赖解析 | 需要基础设施 | 生产环境 |
| **方案4: Monorepo** | 统一代码库、原子提交 | 仓库膨胀 | 紧密耦合项目 |

## 🔧 配置复用

### 模式1: 基础配置继承

**shared-test-lib/src/shared_test_lib/config.py**:

```python
from df_test_framework import FrameworkSettings
from pydantic import Field

class SharedTestSettings(FrameworkSettings):
    """所有测试项目的基础配置"""

    # 公司统一配置
    company_domain: str = Field(default="example.com")
    environment: str = Field(default="test")

    # 微服务基础配置
    auth_service_url: str = Field(default="http://auth-service:8000")
    user_service_url: str = Field(default="http://user-service:8000")

    # 统一认证
    api_token: str = Field(default="")
    api_secret: str = Field(default="")

    # 统一数据库（测试数据库）
    test_database_url: str = Field(
        default="postgresql://test:test@localhost:5432/test_db"
    )

    # 统一Redis
    test_redis_host: str = Field(default="localhost")
    test_redis_port: int = Field(default=6379)

    # 日志统一配置
    @property
    def logging_config(self):
        return {
            "level": "DEBUG" if self.environment == "dev" else "INFO",
            "format": "json",  # 统一使用JSON格式
            "output": "stdout",
        }
```

**user-service-test/src/user_service_test/config.py**:

```python
from shared_test_lib.config import SharedTestSettings
from pydantic import Field

class UserServiceTestSettings(SharedTestSettings):
    """用户服务测试项目特定配置"""

    # 覆盖父类配置
    user_service_url: str = Field(default="http://localhost:8001")

    # 新增特定配置
    user_api_version: str = Field(default="v1")
    user_admin_token: str = Field(default="")

    # 功能开关
    enable_user_cache: bool = Field(default=True)
    enable_user_events: bool = Field(default=False)
```

**使用示例**:

```python
# user-service-test/tests/conftest.py
from df_test_framework import Bootstrap
from user_service_test.config import UserServiceTestSettings

@pytest.fixture(scope="session")
def runtime():
    rt = Bootstrap().with_settings(UserServiceTestSettings).build().run()
    yield rt
    rt.close()
```

### 模式2: 多环境配置

**shared-test-lib/src/shared_test_lib/config.py**:

```python
from enum import Enum
from df_test_framework import FrameworkSettings
from pydantic import Field, model_validator

class Environment(str, Enum):
    DEV = "dev"
    TEST = "test"
    STAGING = "staging"
    PROD = "prod"

class MultiEnvSettings(FrameworkSettings):
    environment: Environment = Field(default=Environment.TEST)

    # 环境相关配置
    auth_service_url: str = Field(default="")

    @model_validator(mode="after")
    def set_environment_urls(self):
        """根据环境设置URL"""
        env_urls = {
            Environment.DEV: {
                "auth_service_url": "http://localhost:8000",
                "user_service_url": "http://localhost:8001",
            },
            Environment.TEST: {
                "auth_service_url": "http://test-auth:8000",
                "user_service_url": "http://test-user:8001",
            },
            Environment.STAGING: {
                "auth_service_url": "https://staging-auth.example.com",
                "user_service_url": "https://staging-user.example.com",
            },
        }

        urls = env_urls.get(self.environment, {})
        for key, value in urls.items():
            if not getattr(self, key):  # 只有未设置时才应用默认值
                setattr(self, key, value)

        return self
```

**环境切换**:

```bash
# 通过环境变量切换
export DF_ENVIRONMENT=staging
pytest tests/

# 通过命令行切换
DF_ENVIRONMENT=dev pytest tests/
```

### 模式3: 配置组合

**shared-test-lib/src/shared_test_lib/config.py**:

```python
from pydantic import BaseModel, Field
from df_test_framework import FrameworkSettings

class MicroserviceConfig(BaseModel):
    """微服务配置（可复用）"""
    name: str
    base_url: str
    timeout: int = 30
    max_retries: int = 3
    api_version: str = "v1"

class AuthConfig(BaseModel):
    """认证配置（可复用）"""
    token: str = Field(default="")
    secret: str = Field(default="")
    token_expiry: int = Field(default=3600)
    refresh_enabled: bool = Field(default=True)

class SharedTestSettings(FrameworkSettings):
    # 组合多个配置模型
    user_service: MicroserviceConfig = Field(
        default_factory=lambda: MicroserviceConfig(
            name="user-service",
            base_url="http://localhost:8001"
        )
    )

    order_service: MicroserviceConfig = Field(
        default_factory=lambda: MicroserviceConfig(
            name="order-service",
            base_url="http://localhost:8002"
        )
    )

    auth: AuthConfig = Field(default_factory=AuthConfig)
```

**使用示例**:

```python
def test_user_api(runtime):
    # 访问嵌套配置
    user_url = runtime.settings.user_service.base_url
    timeout = runtime.settings.user_service.timeout
    token = runtime.settings.auth.token
```

## 🗄️ Repository复用

### 模式1: 共享基础Repository

**shared-test-lib/src/shared_test_lib/repositories/user.py**:

```python
from df_test_framework import BaseRepository
from typing import Optional, List, Dict

class UserRepository(BaseRepository):
    """用户Repository - 所有项目共享"""

    def __init__(self, database):
        super().__init__(database)
        self.table_name = "users"

    def find_by_username(self, username: str) -> Optional[Dict]:
        """通过用户名查找"""
        return self.find_one({"username": username})

    def find_by_email(self, email: str) -> Optional[Dict]:
        """通过邮箱查找"""
        return self.find_one({"email": email})

    def find_active_users(self, limit: int = 100) -> List[Dict]:
        """查找活跃用户"""
        return self.find_all({"status": "active"}, limit=limit)

    def create_user(self, username: str, email: str, **kwargs) -> int:
        """创建用户"""
        data = {
            "username": username,
            "email": email,
            "status": "active",
            **kwargs
        }
        return self.create(data)

    def deactivate_user(self, user_id: int) -> bool:
        """停用用户"""
        return self.update(user_id, {"status": "inactive"})
```

**user-service-test/tests/test_users.py**:

```python
from shared_test_lib.repositories.user import UserRepository

def test_create_user(database):
    # 直接使用共享Repository
    user_repo = UserRepository(database)

    user_id = user_repo.create_user(
        username="testuser",
        email="test@example.com"
    )

    user = user_repo.find_by_id(user_id)
    assert user["username"] == "testuser"
```

### 模式2: Repository继承扩展

**user-service-test/src/user_service_test/repositories/user.py**:

```python
from shared_test_lib.repositories.user import UserRepository as BaseUserRepository

class UserRepository(BaseUserRepository):
    """用户服务特定的Repository扩展"""

    def find_premium_users(self) -> List[Dict]:
        """查找高级用户（业务特定）"""
        return self.find_all({"membership_type": "premium"})

    def get_user_statistics(self, user_id: int) -> Dict:
        """获取用户统计（业务特定）"""
        query = """
        SELECT
            u.id,
            u.username,
            COUNT(o.id) as order_count,
            SUM(o.total_amount) as total_spent
        FROM users u
        LEFT JOIN orders o ON u.id = o.user_id
        WHERE u.id = :user_id
        GROUP BY u.id, u.username
        """
        return self.db.execute(query, {"user_id": user_id}).first()
```

### 模式3: Repository工厂

**shared-test-lib/src/shared_test_lib/repositories/factory.py**:

```python
from typing import Dict, Type
from df_test_framework import Database, BaseRepository

class RepositoryFactory:
    """Repository工厂 - 统一创建Repository"""

    def __init__(self, database: Database):
        self.database = database
        self._cache: Dict[str, BaseRepository] = {}

    def get(self, repository_class: Type[BaseRepository]) -> BaseRepository:
        """获取Repository实例（带缓存）"""
        key = repository_class.__name__
        if key not in self._cache:
            self._cache[key] = repository_class(self.database)
        return self._cache[key]

    def user_repo(self):
        from .user import UserRepository
        return self.get(UserRepository)

    def order_repo(self):
        from .order import OrderRepository
        return self.get(OrderRepository)
```

**使用示例**:

```python
# tests/conftest.py
@pytest.fixture
def repo_factory(database):
    return RepositoryFactory(database)

def test_with_factory(repo_factory):
    user_repo = repo_factory.user_repo()
    order_repo = repo_factory.order_repo()
```

## 🏗️ Builder复用

### 模式1: 共享基础Builder

**shared-test-lib/src/shared_test_lib/builders/user.py**:

```python
from df_test_framework import DictBuilder
from datetime import datetime
import uuid

class UserBuilder(DictBuilder):
    """用户Builder - 所有项目共享"""

    def __init__(self):
        super().__init__()
        # 设置默认值
        self.with_id(str(uuid.uuid4()))
        self.with_username(f"user_{uuid.uuid4().hex[:8]}")
        self.with_email(f"user_{uuid.uuid4().hex[:8]}@example.com")
        self.with_status("active")
        self.with_created_at(datetime.now().isoformat())

    def with_id(self, id: str):
        return self.set("id", id)

    def with_username(self, username: str):
        return self.set("username", username)

    def with_email(self, email: str):
        return self.set("email", email)

    def with_status(self, status: str):
        return self.set("status", status)

    def with_created_at(self, created_at: str):
        return self.set("created_at", created_at)

    def as_admin(self):
        """快捷方法：设置为管理员"""
        return self.set("role", "admin").set("permissions", ["*"])

    def as_premium(self):
        """快捷方法：设置为高级用户"""
        return self.set("membership_type", "premium")
```

**使用示例**:

```python
from shared_test_lib.builders.user import UserBuilder

def test_admin_user(database):
    # 构建管理员用户
    admin_data = (
        UserBuilder()
        .with_username("admin")
        .with_email("admin@example.com")
        .as_admin()
        .build()
    )

    user_repo.create(admin_data)
```

### 模式2: Builder链式组合

**shared-test-lib/src/shared_test_lib/builders/order.py**:

```python
from df_test_framework import DictBuilder
from .user import UserBuilder
import uuid

class OrderBuilder(DictBuilder):
    """订单Builder - 支持关联User"""

    def __init__(self):
        super().__init__()
        self.with_id(str(uuid.uuid4()))
        self.with_status("pending")
        self._user_builder = None

    def with_id(self, id: str):
        return self.set("id", id)

    def with_user_id(self, user_id: str):
        return self.set("user_id", user_id)

    def with_user(self, user_builder: UserBuilder):
        """关联UserBuilder"""
        self._user_builder = user_builder
        return self

    def with_status(self, status: str):
        return self.set("status", status)

    def build_with_user(self):
        """构建订单和用户数据"""
        if self._user_builder:
            user_data = self._user_builder.build()
            self.with_user_id(user_data["id"])
            return {
                "user": user_data,
                "order": self.build()
            }
        else:
            return {"order": self.build()}
```

**使用示例**:

```python
from shared_test_lib.builders.user import UserBuilder
from shared_test_lib.builders.order import OrderBuilder

def test_user_order(database):
    # 链式构建用户和订单
    data = (
        OrderBuilder()
        .with_user(
            UserBuilder()
            .with_username("john")
            .as_premium()
        )
        .with_status("paid")
        .build_with_user()
    )

    user_repo.create(data["user"])
    order_repo.create(data["order"])
```

## 🔌 Extension复用

### 模式1: 共享Extension

**shared-test-lib/src/shared_test_lib/extensions/auth.py**:

```python
from df_test_framework.extensions import hookimpl
from df_test_framework import SingletonProvider
import jwt

class AuthProvider:
    """统一认证Provider"""

    def __init__(self, settings, logger):
        self.settings = settings
        self.logger = logger
        self._token = None

    def get_token(self) -> str:
        """获取认证Token"""
        if not self._token:
            self._token = self._generate_token()
        return self._token

    def _generate_token(self) -> str:
        payload = {
            "sub": "test_client",
            "exp": int(time.time()) + 3600
        }
        return jwt.encode(payload, self.settings.auth.secret, algorithm="HS256")

class AuthExtension:
    """认证扩展 - 所有项目共享"""

    @hookimpl
    def df_providers(self, settings, logger):
        return {
            "auth": SingletonProvider(
                lambda rt: AuthProvider(rt.settings, rt.logger)
            )
        }

    @hookimpl
    def df_post_bootstrap(self, runtime):
        runtime.logger.info("认证扩展已加载")
```

**使用示例**:

```python
# user-service-test/tests/conftest.py
from df_test_framework import Bootstrap
from shared_test_lib.extensions.auth import AuthExtension
from user_service_test.config import UserServiceTestSettings

@pytest.fixture(scope="session")
def runtime():
    rt = (
        Bootstrap()
        .with_settings(UserServiceTestSettings)
        .with_plugin(AuthExtension())  # 加载共享扩展
        .build()
        .run()
    )
    yield rt
    rt.close()

def test_with_auth(runtime, http_client):
    # 使用共享认证
    auth = runtime.get("auth")
    token = auth.get_token()

    response = http_client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
```

### 模式2: Extension组合

**shared-test-lib/src/shared_test_lib/extensions/__init__.py**:

```python
from .auth import AuthExtension
from .monitoring import MonitoringExtension
from .data_cleanup import DataCleanupExtension

def get_standard_extensions():
    """获取标准扩展集合"""
    return [
        AuthExtension(),
        MonitoringExtension(),
        DataCleanupExtension(),
    ]
```

**使用示例**:

```python
from shared_test_lib.extensions import get_standard_extensions

runtime = (
    Bootstrap()
    .with_settings(MySettings)
    # 批量加载标准扩展
    *[.with_plugin(ext) for ext in get_standard_extensions()]
    .build()
    .run()
)
```

## 🧪 Fixture复用

### 模式1: 共享Fixtures包

**shared-test-lib/src/shared_test_lib/fixtures.py**:

```python
import pytest
from df_test_framework import Bootstrap
from .config import SharedTestSettings
from .extensions import get_standard_extensions
from .repositories.factory import RepositoryFactory

@pytest.fixture(scope="session")
def shared_runtime():
    """共享Runtime - session级别"""
    rt = Bootstrap().with_settings(SharedTestSettings).build().run()
    for ext in get_standard_extensions():
        rt = Bootstrap().with_plugin(ext).build().run()
    yield rt
    rt.close()

@pytest.fixture
def repo_factory(database):
    """Repository工厂"""
    return RepositoryFactory(database)

@pytest.fixture
def user_repo(repo_factory):
    """用户Repository"""
    return repo_factory.user_repo()

@pytest.fixture
def clean_users(database):
    """清理用户数据"""
    yield
    database.execute("DELETE FROM users WHERE username LIKE 'test_%'")
```

**使用示例**:

```python
# user-service-test/tests/conftest.py
from shared_test_lib.fixtures import *  # 导入所有共享fixtures

# 添加项目特定fixtures
@pytest.fixture
def user_api_client(runtime, http_client):
    """用户API客户端"""
    http_client.base_url = runtime.settings.user_service.base_url
    return http_client
```

### 模式2: Fixture覆盖

```python
# tests/conftest.py
from shared_test_lib.fixtures import *

# 覆盖共享fixture
@pytest.fixture(scope="session")
def shared_runtime():
    """覆盖：使用项目特定配置"""
    from user_service_test.config import UserServiceTestSettings

    rt = Bootstrap().with_settings(UserServiceTestSettings).build().run()
    yield rt
    rt.close()
```

## ✅ 最佳实践

### 1. 版本管理策略

**语义化版本**:

```toml
# shared-test-lib/pyproject.toml
[project]
name = "shared-test-lib"
version = "1.2.3"  # 主版本.次版本.修订版本

# user-service-test/pyproject.toml
[project]
dependencies = [
    "shared-test-lib>=1.2.0,<2.0.0"  # 允许次版本更新
]
```

**版本兼容性**:

- **主版本号**: 不兼容的API变更
- **次版本号**: 向后兼容的功能新增
- **修订版本号**: 向后兼容的bug修复

### 2. 文档规范

**每个共享组件都应有文档**:

```python
# shared-test-lib/src/shared_test_lib/repositories/user.py
class UserRepository(BaseRepository):
    """
    用户Repository - 跨项目共享

    支持的项目:
    - user-service-test
    - order-service-test
    - payment-service-test

    使用示例:
        repo = UserRepository(database)
        user = repo.find_by_username("john")

    版本历史:
    - v1.0.0: 初始版本
    - v1.1.0: 新增find_by_email方法
    - v1.2.0: 新增find_active_users方法
    """
```

### 3. 测试共享组件

**shared-test-lib本身也需要测试**:

```python
# shared-test-lib/tests/test_user_repository.py
def test_user_repository_find_by_username(database):
    """测试UserRepository.find_by_username"""
    repo = UserRepository(database)

    # 准备数据
    user_id = repo.create_user("testuser", "test@example.com")

    # 测试查找
    user = repo.find_by_username("testuser")
    assert user is not None
    assert user["id"] == user_id
```

### 4. 依赖管理

**明确依赖范围**:

```toml
# shared-test-lib/pyproject.toml
[project]
dependencies = [
    "df-test-framework>=2.0.0,<3.0.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
# 可选依赖：只有需要的项目才安装
monitoring = ["prometheus-client>=0.16.0"]
auth = ["pyjwt>=2.8.0"]
```

**项目选择性安装**:

```bash
# 只安装基础功能
pip install shared-test-lib

# 安装监控功能
pip install shared-test-lib[monitoring]

# 安装所有功能
pip install shared-test-lib[monitoring,auth]
```

### 5. 命名规范

**避免命名冲突**:

```python
# ✅ 好：明确的命名空间
from shared_test_lib.repositories import UserRepository as SharedUserRepository
from user_service_test.repositories import UserRepository

# ✅ 好：使用前缀
class SharedUserRepository(BaseRepository):
    ...

class UserServiceUserRepository(SharedUserRepository):
    ...

# ❌ 避免：容易混淆的命名
from shared import UserRepository  # 不清楚来源
```

### 6. 变更管理

**CHANGELOG.md**:

```markdown
# Changelog

## [1.2.0] - 2025-01-15

### Added
- UserRepository新增find_active_users方法
- OrderBuilder支持链式构建用户数据

### Changed
- SharedTestSettings默认timeout从30改为60

### Deprecated
- UserRepository.find_all_users将在v2.0移除，请使用find_active_users

### Fixed
- 修复AuthExtension token过期未刷新的问题
```

### 7. 发布流程

**自动化发布**:

```yaml
# .github/workflows/release.yml
name: Release
on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build package
        run: python -m build
      - name: Publish to PyPI
        run: python -m twine upload dist/*
```

### 8. 迁移指南

**提供版本升级文档**:

```markdown
# 从v1.x迁移到v2.0

## Breaking Changes

### 1. UserRepository.find_all_users已移除
**Before**:
```python
users = repo.find_all_users()
```

**After**:
```python
users = repo.find_active_users()  # 新方法名
```

## 2. SharedTestSettings.api_url重命名
**Before**:
```python
class MySettings(SharedTestSettings):
    api_url: str
```

**After**:
```python
class MySettings(SharedTestSettings):
    user_service_url: str  # 更明确的命名
```
```

## 🔗 相关文档

- [跨项目共享最佳实践](../user-guide/cross-project-sharing.md)
- [v2.0架构详解](v2-architecture.md)
- [扩展点文档](extension-points.md)

---

**返回**: [架构文档](README.md) | [文档首页](../README.md)
