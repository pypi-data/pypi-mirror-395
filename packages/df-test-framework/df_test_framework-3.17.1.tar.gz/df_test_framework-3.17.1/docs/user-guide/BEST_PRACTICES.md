# DF Test Framework - 最佳实践指南

> **版本**: v3.17.0
> **更新日期**: 2025-12-05
> **适用范围**: API测试、数据库测试、集成测试

> ⭐ **推荐阅读**: 本文档包含通用最佳实践。如果你需要**经过实际项目验证**的最佳实践（包含完整示例和实现细节），请查看 [VERIFIED_BEST_PRACTICES.md](VERIFIED_BEST_PRACTICES.md)，该文档基于真实生产项目（gift-card-test）验证，置信度100%。

---

## 📚 目录

1. [项目结构最佳实践](#1-项目结构最佳实践)
2. [配置管理最佳实践](#2-配置管理最佳实践)
3. [HTTP客户端使用最佳实践](#3-http客户端使用最佳实践)
4. [数据库操作最佳实践](#4-数据库操作最佳实践)
5. [测试数据管理最佳实践](#5-测试数据管理最佳实践)
6. [Fixtures使用最佳实践](#6-fixtures使用最佳实践)
7. [断言和验证最佳实践](#7-断言和验证最佳实践)
8. [错误处理最佳实践](#8-错误处理最佳实践)
9. [测试用例组织最佳实践](#9-测试用例组织最佳实践)
10. [性能优化最佳实践](#10-性能优化最佳实践)
11. [事件系统与可观测性最佳实践](#11-事件系统与可观测性最佳实践) ⚡ v3.17+

---

## 1. 项目结构最佳实践

### ✅ 推荐的目录结构

使用脚手架工具生成标准结构：

```bash
df-test init my-test-project
```

生成的项目结构：

```
my-test-project/
├── config/                      # 配置管理
│   ├── __init__.py
│   └── settings.py             # 项目配置
├── apis/                        # API客户端封装
│   ├── __init__.py
│   ├── base.py                 # 基础API类
│   ├── admin/                  # Admin系统API
│   ├── h5/                     # H5系统API
│   └── master/                 # Master系统API
├── models/                      # 数据模型
│   ├── __init__.py
│   ├── requests/               # 请求模型
│   └── responses/              # 响应模型
├── repositories/                # 数据库Repository
│   ├── __init__.py
│   └── user_repo.py
├── builders/                    # 测试数据Builder
│   ├── __init__.py
│   └── user_builder.py
├── fixtures/                    # Pytest Fixtures
│   ├── __init__.py
│   └── data_cleaners.py        # 数据清理
├── utils/                       # 工具函数
│   ├── __init__.py
│   ├── validators.py           # 验证函数
│   └── converters.py           # 转换函数
├── constants/                   # 常量定义
│   ├── __init__.py
│   └── error_codes.py
├── data/                        # 测试数据
│   ├── fixtures/               # JSON/YAML fixture数据
│   └── files/                  # 测试文件（图片、文档等）
├── tests/                       # 测试用例
│   ├── conftest.py             # Pytest配置
│   ├── api/                    # API测试
│   ├── integration/            # 集成测试
│   └── smoke/                  # 冒烟测试
├── scripts/                     # 脚本
│   └── run_tests.sh
├── docs/                        # 文档
│   └── api.md
├── .env.example                 # 环境变量示例
├── .env                         # 环境变量（gitignore）
├── pytest.ini                   # Pytest配置
├── pyproject.toml              # 项目配置
└── README.md
```

### ✅ 模块命名规范

| 类型 | 命名规范 | 示例 |
|------|---------|------|
| API客户端 | `{模块名}_api.py` | `user_api.py`, `card_api.py` |
| Repository | `{模块名}_repo.py` | `user_repo.py`, `card_repo.py` |
| Builder | `{模块名}_builder.py` | `user_builder.py` |
| 测试用例 | `test_{功能}.py` | `test_user_creation.py` |
| Fixture | `{功能}_fixtures.py` | `user_fixtures.py` |

---

## 2. 配置管理最佳实践

### ✅ 推荐：使用Pydantic Settings + 环境变量

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
    """项目测试配置

    支持从环境变量自动加载配置。
    环境变量命名规则：{PREFIX}_{SECTION}_{KEY}
    例如：MYPROJECT_HTTP_BASE_URL
    """

    # HTTP配置（v3.5+ 使用HTTPSettings）
    http_settings: HTTPSettings = Field(
        default_factory=lambda: HTTPSettings(
            base_url="http://localhost:8000/api",  # 默认值
            timeout=30,
            max_retries=3,
        ),
        description="HTTP配置"
    )

    # 数据库配置（可选）
    db: DatabaseConfig = Field(
        default_factory=lambda: DatabaseConfig(
            connection_string="mysql+pymysql://user:pass@localhost:3306/testdb",
            pool_size=5,
            echo=False,
        )
    )

    # Redis配置（可选）
    redis: RedisConfig = Field(
        default_factory=lambda: RedisConfig(
            host="localhost",
            port=6379,
            db=0,
        )
    )

    # 项目特定配置
    test_user_id: str = Field(default="test_user_001", env="TEST_USER_ID")
    test_admin_token: str = Field(default="", env="ADMIN_TOKEN")

    class Config:
        env_prefix = "MYPROJECT_"  # 环境变量前缀
        env_nested_delimiter = "_"  # 嵌套配置分隔符
```

**.env 文件**:

```bash
# HTTP配置
MYPROJECT_HTTP_BASE_URL=https://api.example.com
MYPROJECT_HTTP_TIMEOUT=30

# 数据库配置
MYPROJECT_DB_CONNECTION_STRING=mysql+pymysql://user:pass@localhost:3306/testdb

# Redis配置
MYPROJECT_REDIS_HOST=redis.example.com
MYPROJECT_REDIS_PORT=6379

# 项目特定配置
TEST_USER_ID=test_user_001
ADMIN_TOKEN=your_admin_token_here
```

**pytest.ini**:

```ini
[pytest]
# 指定框架使用的Settings类
df_settings_class = config.settings.MyProjectSettings

# 其他pytest配置
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

### ✅ 多环境配置

**方法1：使用不同的.env文件**

```bash
# 开发环境
cp .env.dev .env

# 测试环境
cp .env.test .env

# 生产环境
cp .env.prod .env
```

**方法2：使用环境变量控制**

```python
class MyProjectSettings(FrameworkSettings):
    env: str = Field(default="test", env="ENVIRONMENT")

    @property
    def is_production(self) -> bool:
        return self.env == "production"

    @property
    def is_test(self) -> bool:
        return self.env == "test"
```

---

## 3. HTTP客户端使用最佳实践

### ✅ 推荐方法1：使用 @api_class 装饰器（v3.14+，⭐最简单）

```python
"""用户API客户端 - 使用 @api_class 自动注册"""

from df_test_framework import api_class, BaseAPI


@api_class("user_api", scope="session")
class UserAPI(BaseAPI):
    """用户API客户端

    @api_class 装饰器自动注册为 pytest fixture，
    测试中可直接使用 user_api 参数。
    """

    def get_user(self, user_id: str) -> dict:
        """获取用户信息"""
        response = self.get(f"/users/{user_id}")
        return response.json()

    def create_user(self, data: dict) -> dict:
        """创建用户"""
        response = self.post("/users", json=data)
        return response.json()


# 测试中自动注入
def test_user(user_api):
    """测试获取用户 - user_api 自动注入"""
    result = user_api.get_user("123")
    assert result["code"] == 200
```

**优势**：
- ✅ 无需手动编写 fixture
- ✅ 自动注册到 pytest
- ✅ 支持所有 fixture 作用域
- ✅ 减少样板代码

### ✅ 推荐方法2：手动封装API客户端类（灵活）

**apis/base.py**:

```python
"""API基类 - 统一的业务错误处理"""

from df_test_framework import BaseAPI, HttpClient
from df_test_framework.clients.http.rest.httpx import BusinessError
from typing import Dict, Any


class MyProjectBaseAPI(BaseAPI):
    """项目API基类

    提供统一的业务错误检查和通用功能。
    """

    def __init__(self, http_client: HttpClient):
        super().__init__(http_client)

    def _check_business_error(self, response_data: dict) -> None:
        """检查业务错误

        Args:
            response_data: 响应数据字典

        Raises:
            BusinessError: 业务错误（code != 200）
        """
        code = response_data.get("code")
        if code != 200:
            message = response_data.get("message", "未知错误")
            data = response_data.get("data")
            raise BusinessError(
                message=f"[{code}] {message}",
                code=code,
                data=data
            )

    def _extract_data(self, response_data: dict) -> Any:
        """提取响应数据

        Args:
            response_data: 完整响应

        Returns:
            响应中的data字段
        """
        self._check_business_error(response_data)
        return response_data.get("data")
```

**apis/user_api.py**:

```python
"""用户API客户端"""

from typing import Dict, Any, List
from .base import MyProjectBaseAPI


class UserAPI(MyProjectBaseAPI):
    """用户API客户端

    封装用户相关的所有API调用。
    """

    def __init__(self, http_client):
        super().__init__(http_client)
        self.base_path = "/users"

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """获取用户信息

        Args:
            user_id: 用户ID

        Returns:
            用户数据字典

        Raises:
            BusinessError: 业务错误
        """
        response = self.http_client.get(f"{self.base_path}/{user_id}")
        data = response.json()
        return self._extract_data(data)

    def list_users(self, page: int = 1, size: int = 10) -> List[Dict[str, Any]]:
        """获取用户列表

        Args:
            page: 页码
            size: 每页数量

        Returns:
            用户列表
        """
        response = self.http_client.get(
            self.base_path,
            params={"page": page, "size": size}
        )
        data = response.json()
        return self._extract_data(data)

    def create_user(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建用户

        Args:
            request_data: 用户创建请求

        Returns:
            创建的用户数据
        """
        response = self.http_client.post(self.base_path, json=request_data)
        data = response.json()
        return self._extract_data(data)

    def update_user(self, user_id: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新用户

        Args:
            user_id: 用户ID
            request_data: 更新数据

        Returns:
            更新后的用户数据
        """
        response = self.http_client.put(
            f"{self.base_path}/{user_id}",
            json=request_data
        )
        data = response.json()
        return self._extract_data(data)

    def delete_user(self, user_id: str) -> None:
        """删除用户

        Args:
            user_id: 用户ID
        """
        response = self.http_client.delete(f"{self.base_path}/{user_id}")
        data = response.json()
        self._check_business_error(data)
```

### ✅ 使用中间件添加认证（v3.14+）

```python
from df_test_framework import BearerTokenMiddleware

# 在conftest.py中配置
@pytest.fixture
def authenticated_http_client(http_client):
    """带认证的HTTP客户端（v3.14+ 中间件系统）"""
    token = "your_auth_token_here"
    middleware = BearerTokenMiddleware(token)

    # v3.14+ 统一使用 .use() 方法
    http_client.use(middleware)

    return http_client
```

### ⭐ BaseAPI 双模式支持（重要）

> ⚠️ **核心设计**: BaseAPI 的所有 HTTP 方法都支持 **Pydantic 模型** 和 **Dict** 两种返回模式！

#### 设计说明

框架通过 **可选的 `model` 参数** 提供了灵活的返回类型：

```python
# 模式1：返回 Pydantic 模型（推荐用于生产项目）
response: UserResponse = self.get("/users/1", model=UserResponse)

# 模式2：返回 Dict（用于快速原型）
response: Dict[str, Any] = self.get("/users/1")
```

**Pydantic 模型模式的优势**：
- ✅ 类型安全和 IDE 自动补全
- ✅ 自动数据验证
- ✅ 字段别名支持（snake_case ↔ camelCase）
- ✅ 清晰的数据结构定义
- ✅ 重构友好

**Dict 模式的适用场景**：
- 快速原型和探索性测试
- 简单的数据结构
- 不需要严格类型检查

#### 示例：Pydantic 模型模式（推荐）

```python
from pydantic import BaseModel, Field
from typing import Optional

# 1. 定义响应模型
class UserVO(BaseModel):
    id: int
    username: str
    email: str
    created_at: str = Field(alias="createdAt")

    model_config = {"populate_by_name": True}

class UserResponse(BaseResponse[UserVO]):
    pass

# 2. API 客户端中使用
class UserAPI(MyProjectBaseAPI):
    def get_user(self, user_id: int) -> UserResponse:
        """获取用户信息（类型安全）"""
        return self.get(
            endpoint=f"/users/{user_id}",
            model=UserResponse  # ← 指定模型类
        )

# 3. 测试中使用
def test_get_user(user_api):
    response = user_api.get_user(123)

    # ✅ 类型安全，IDE 自动补全
    assert response.data.username == "张三"
    assert response.data.email == "test@example.com"
```

#### 示例：Dict 模式（快速原型）

```python
class UserAPI(MyProjectBaseAPI):
    def get_user_dict(self, user_id: int) -> Dict[str, Any]:
        """获取用户信息（Dict 模式）"""
        return self.get(f"/users/{user_id}")  # ← 不指定 model

def test_get_user_dict(user_api):
    response = user_api.get_user_dict(123)

    # ⚠️ 无类型检查
    assert response["data"]["username"] == "张三"
```

> 💡 **最佳实践**: 生产项目优先使用 Pydantic 模型模式，快速原型可以使用 Dict 模式。
>
> 详细说明请参考 [VERIFIED_BEST_PRACTICES.md - 1.3 BaseAPI 双模式支持](VERIFIED_BEST_PRACTICES.md#13-baseapi-双模式支持---核心设计说明)

---

### ✅ 使用中间件添加签名（v3.14+）

```python
from df_test_framework import SignatureMiddleware

# 在conftest.py中配置
@pytest.fixture
def signed_http_client(http_client):
    """带签名的HTTP客户端（v3.14+ 中间件系统）"""
    middleware = SignatureMiddleware(
        secret="your_app_secret",
        algorithm="md5",  # 支持: md5, sha1, sha256
        header_name="X-Sign",
    )

    # v3.14+ 统一使用 .use() 方法
    http_client.use(middleware)

    return http_client
```

---

## 4. 数据库操作最佳实践

### ✅ 推荐：使用Repository模式

**repositories/user_repo.py**:

```python
"""用户Repository"""

from df_test_framework import BaseRepository
from typing import Optional, List, Dict, Any


class UserRepository(BaseRepository):
    """用户数据访问层

    封装用户表的所有数据库操作。
    """

    def __init__(self, db):
        super().__init__(db, table_name="users")

    def find_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """根据用户名查找用户

        Args:
            username: 用户名

        Returns:
            用户数据字典，不存在返回None
        """
        return self.find_one({"username": username})

    def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """根据邮箱查找用户"""
        return self.find_one({"email": email})

    def find_active_users(self) -> List[Dict[str, Any]]:
        """查找所有激活的用户"""
        return self.find_all(
            conditions={"status": "ACTIVE"},
            order_by="created_at DESC"
        )

    def count_users_by_status(self, status: str) -> int:
        """统计指定状态的用户数"""
        return self.count({"status": status})

    def soft_delete(self, user_id: str) -> bool:
        """软删除用户

        Args:
            user_id: 用户ID

        Returns:
            是否删除成功
        """
        return self.update(user_id, {"is_deleted": True}) > 0
```

### ✅ 使用事务确保数据一致性

```python
def test_user_transaction(database):
    """测试用户创建事务"""

    # 开启事务
    with database.transaction():
        # 插入用户
        user_id = database.insert("users", {
            "username": "test_user",
            "email": "test@example.com",
            "status": "ACTIVE"
        })

        # 插入用户配置
        database.insert("user_settings", {
            "user_id": user_id,
            "theme": "dark",
            "language": "zh_CN"
        })

        # 如果发生异常，自动回滚
        # 如果成功，自动提交
```

---

## 5. 测试数据管理最佳实践

### ✅ 方法1：使用 Unit of Work 模式（⭐v3.7推荐）

**uow.py**:

```python
"""Unit of Work 实现"""

from df_test_framework.infrastructure.database import UnitOfWork

class ProjectUoW(UnitOfWork):
    """项目的 Unit of Work

    统一管理事务和所有 Repository，确保同一个 Session。
    """
    def __init__(self, engine):
        super().__init__(engine)

    @property
    def users(self):
        """用户 Repository"""
        from .repositories import UserRepository
        return UserRepository(self._session)

    @property
    def orders(self):
        """订单 Repository"""
        from .repositories import OrderRepository
        return OrderRepository(self._session)
```

**conftest.py**:

```python
@pytest.fixture
def uow(database):
    """Unit of Work fixture（⭐推荐）

    测试开始前开启事务，测试结束后自动回滚，数据不会保留。

    使用示例:
        ```python
        def test_create_user(api, uow):
            # 创建用户
            response = api.create_user(request)

            # 验证数据库 - 使用 UoW 的 Repository
            user = uow.users.find_by_id(response.data.user_id)
            assert user is not None

            # ✅ 测试结束后自动回滚，无需手动清理
        ```
    """
    from your_project.uow import ProjectUoW
    with ProjectUoW(database.engine) as uow:
        yield uow
        # 默认自动回滚
```

**测试用例**:

```python
def test_create_user(user_api, uow):
    """测试创建用户（自动回滚）"""

    # 创建用户
    user_data = {
        "username": "test_user",
        "email": "test@example.com"
    }
    result = user_api.create_user(user_data)
    user_id = result["user_id"]

    # 验证数据库 - 使用 UoW 的 Repository
    user = uow.users.find_by_id(user_id)

    assert user is not None
    assert user["username"] == "test_user"

    # ✅ 测试结束后，数据自动回滚，不会污染数据库
```

### ✅ 方法2：使用Builder构建测试数据

**builders/user_builder.py**:

```python
"""用户数据Builder"""

from df_test_framework import DictBuilder
from typing import Dict, Any


class UserRequestBuilder:
    """用户创建请求Builder

    提供流畅的API构建用户创建请求。
    """

    def __init__(self):
        self._builder = DictBuilder({
            "username": "default_user",
            "email": "default@example.com",
            "password": "default_password",
            "status": "ACTIVE"
        })

    def with_username(self, username: str) -> "UserRequestBuilder":
        """设置用户名"""
        self._builder.set("username", username)
        return self

    def with_email(self, email: str) -> "UserRequestBuilder":
        """设置邮箱"""
        self._builder.set("email", email)
        return self

    def with_password(self, password: str) -> "UserRequestBuilder":
        """设置密码"""
        self._builder.set("password", password)
        return self

    def as_inactive(self) -> "UserRequestBuilder":
        """设置为未激活状态"""
        self._builder.set("status", "INACTIVE")
        return self

    def build(self) -> Dict[str, Any]:
        """构建最终的请求数据"""
        return self._builder.build()
```

**使用Builder**:

```python
from builders import UserRequestBuilder

def test_create_user_with_builder(user_api, uow):
    """使用Builder构建测试数据"""

    # 构建用户数据
    user_data = (
        UserRequestBuilder()
        .with_username("test_user_001")
        .with_email("test001@example.com")
        .with_password("SecureP@ss123")
        .build()
    )

    # 创建用户
    result = user_api.create_user(user_data)

    assert result["username"] == "test_user_001"
```

### ✅ 方法3：使用Fixture提供测试数据

```python
# conftest.py
@pytest.fixture
def test_user_data():
    """测试用户数据"""
    return {
        "username": "test_user",
        "email": "test@example.com",
        "password": "Test123!",
        "status": "ACTIVE"
    }

@pytest.fixture
def inactive_user_data():
    """未激活用户数据"""
    return {
        "username": "inactive_user",
        "email": "inactive@example.com",
        "password": "Test123!",
        "status": "INACTIVE"
    }

# 测试用例
def test_create_user(user_api, test_user_data):
    """使用Fixture提供的测试数据"""
    result = user_api.create_user(test_user_data)
    assert result["username"] == test_user_data["username"]
```

---

## 6. Fixtures使用最佳实践

### ✅ Fixture作用域选择

| Scope | 说明 | 使用场景 |
|-------|------|---------|
| `function` | 每个测试函数执行一次 | 测试数据、数据清理 |
| `class` | 每个测试类执行一次 | 共享数据准备 |
| `module` | 每个模块执行一次 | 模块级别的数据准备 |
| `session` | 整个测试会话执行一次 | Runtime、HttpClient、Database |

**示例**:

```python
# Session级别 - 整个测试会话共享
@pytest.fixture(scope="session")
def runtime():
    """Runtime实例（session级别）"""
    app = Bootstrap().build()
    runtime = app.run()
    yield runtime
    runtime.close()

# Function级别 - 每个测试独立
@pytest.fixture
def uow(database):
    """Unit of Work（function级别）"""
    from your_project.uow import ProjectUoW
    with ProjectUoW(database.engine) as uow:
        yield uow
        # 每个测试结束后回滚
```

### ✅ Fixture依赖链

```python
# 基础fixture
@pytest.fixture(scope="session")
def runtime():
    """Runtime实例"""
    app = Bootstrap().build()
    return app.run()

# 依赖runtime的fixture
@pytest.fixture(scope="session")
def http_client(runtime):
    """HTTP客户端"""
    return runtime.http_client()

@pytest.fixture(scope="session")
def database(runtime):
    """数据库客户端"""
    return runtime.database()

# 依赖http_client的fixture
@pytest.fixture
def user_api(http_client):
    """用户API客户端"""
    from apis import UserAPI
    return UserAPI(http_client)

# 依赖database的fixture
@pytest.fixture
def user_repo(database):
    """用户Repository"""
    from repositories import UserRepository
    return UserRepository(database)
```

### ✅ Fixture自动使用（autouse）

```python
@pytest.fixture(autouse=True, scope="session")
def setup_test_environment():
    """自动执行的环境准备"""
    print("\n=== 测试环境准备 ===")
    # 准备工作...
    yield
    print("\n=== 测试环境清理 ===")
    # 清理工作...
```

---

## 7. 断言和验证最佳实践

### ✅ 使用明确的断言消息

```python
# ❌ 不推荐
assert response.status_code == 200

# ✅ 推荐
assert response.status_code == 200, f"期望状态码200，实际{response.status_code}"
```

### ✅ 使用Allure步骤

```python
import allure
from df_test_framework.testing.plugins import step, attach_json

@allure.feature("用户管理")
@allure.story("用户创建")
class TestUserCreation:

    @allure.title("测试创建用户成功")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_success(self, user_api, uow):
        """测试创建用户成功"""

        with step("准备测试数据"):
            user_data = {
                "username": "test_user",
                "email": "test@example.com"
            }
            attach_json(user_data, name="用户数据")

        with step("调用创建用户API"):
            result = user_api.create_user(user_data)
            attach_json(result, name="API响应")

        with step("验证API响应"):
            assert result["username"] == user_data["username"]
            assert "user_id" in result

        with step("验证数据库"):
            # 使用 UoW 的 Repository
            user = uow.users.find_by_id(result["user_id"])

            assert user is not None
            assert user["username"] == user_data["username"]
```

### ✅ 分离验证逻辑

**utils/validators.py**:

```python
"""验证工具函数"""

from typing import Dict, Any


def validate_user_response(user_data: Dict[str, Any]) -> None:
    """验证用户响应数据格式

    Args:
        user_data: 用户数据字典

    Raises:
        AssertionError: 验证失败
    """
    assert "user_id" in user_data, "缺少user_id字段"
    assert "username" in user_data, "缺少username字段"
    assert "email" in user_data, "缺少email字段"
    assert "status" in user_data, "缺少status字段"

    # 验证格式
    assert isinstance(user_data["user_id"], str), "user_id应为字符串"
    assert "@" in user_data["email"], "邮箱格式不正确"


def validate_pagination_response(response: Dict[str, Any]) -> None:
    """验证分页响应格式"""
    assert "total" in response, "缺少total字段"
    assert "page" in response, "缺少page字段"
    assert "size" in response, "缺少size字段"
    assert "items" in response, "缺少items字段"
    assert isinstance(response["items"], list), "items应为列表"
```

**使用**:

```python
from utils.validators import validate_user_response

def test_get_user(user_api):
    """测试获取用户"""
    user = user_api.get_user("user_001")

    # 使用验证函数
    validate_user_response(user)

    # 业务验证
    assert user["username"] == "expected_username"
```

---

## 8. 错误处理最佳实践

### ✅ 捕获并验证业务错误

```python
import pytest
from df_test_framework.clients.http.rest.httpx import BusinessError

def test_create_duplicate_user(user_api):
    """测试创建重复用户应抛出错误"""

    user_data = {"username": "existing_user"}

    # 验证抛出BusinessError
    with pytest.raises(BusinessError) as exc_info:
        user_api.create_user(user_data)

    # 验证错误信息
    error = exc_info.value
    assert error.code == 40001  # 用户已存在错误码
    assert "用户名已存在" in error.message
```

### ✅ 使用try-except进行容错

```python
def test_delete_user_idempotent(user_api):
    """测试删除用户幂等性"""

    user_id = "user_to_delete"

    # 第一次删除
    user_api.delete_user(user_id)

    # 第二次删除（幂等）
    try:
        user_api.delete_user(user_id)
    except BusinessError as e:
        # 允许"用户不存在"错误
        assert e.code == 40004
```

---

## 9. 测试用例组织最佳实践

### ✅ 使用测试类组织相关测试

```python
import pytest
import allure


@allure.feature("用户管理")
@allure.story("用户CRUD")
class TestUserCRUD:
    """用户CRUD测试"""

    @pytest.mark.smoke
    @pytest.mark.p0
    def test_create_user(self, user_api):
        """测试创建用户"""
        pass

    @pytest.mark.smoke
    @pytest.mark.p0
    def test_get_user(self, user_api):
        """测试获取用户"""
        pass

    @pytest.mark.p1
    def test_update_user(self, user_api):
        """测试更新用户"""
        pass

    @pytest.mark.p1
    def test_delete_user(self, user_api):
        """测试删除用户"""
        pass


@allure.feature("用户管理")
@allure.story("用户查询")
class TestUserQuery:
    """用户查询测试"""

    @pytest.mark.p1
    def test_list_users(self, user_api):
        """测试获取用户列表"""
        pass

    @pytest.mark.p2
    def test_search_users(self, user_api):
        """测试搜索用户"""
        pass
```

### ✅ 使用pytest.mark标记

```python
# conftest.py - 注册自定义标记
def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: 冒烟测试")
    config.addinivalue_line("markers", "p0: P0优先级")
    config.addinivalue_line("markers", "p1: P1优先级")
    config.addinivalue_line("markers", "p2: P2优先级")
    config.addinivalue_line("markers", "slow: 慢速测试")

# 测试用例
@pytest.mark.smoke
@pytest.mark.p0
def test_critical_feature(user_api):
    """关键功能测试"""
    pass

# 运行特定标记的测试
# pytest -m "smoke"
# pytest -m "p0 or p1"
# pytest -m "smoke and not slow"
```

### ✅ 使用参数化测试

```python
@pytest.mark.parametrize("username,email,expected_status", [
    ("user1", "user1@example.com", "ACTIVE"),
    ("user2", "user2@example.com", "ACTIVE"),
    ("user3", "user3@example.com", "INACTIVE"),
])
def test_create_users_parametrized(user_api, uow,
                                   username, email, expected_status):
    """参数化测试创建多个用户"""
    user_data = {
        "username": username,
        "email": email,
        "status": expected_status
    }

    result = user_api.create_user(user_data)

    assert result["username"] == username
    assert result["status"] == expected_status
```

---

## 10. 性能优化最佳实践

### ✅ 使用Session级别的Fixture

```python
# ✅ 推荐 - Session级别，只创建一次
@pytest.fixture(scope="session")
def http_client(runtime):
    """HTTP客户端（session级别）"""
    return runtime.http_client()

# ❌ 不推荐 - Function级别，每个测试都创建
@pytest.fixture
def http_client(runtime):
    """HTTP客户端（function级别）"""
    return runtime.http_client()
```

### ✅ 使用数据库连接池

```python
class MyProjectSettings(FrameworkSettings):
    db: DatabaseConfig = Field(
        default_factory=lambda: DatabaseConfig(
            connection_string="mysql+pymysql://...",
            pool_size=10,  # 连接池大小
            max_overflow=20,  # 最大溢出连接
            pool_timeout=30,  # 超时时间
            pool_recycle=3600,  # 连接回收时间
        )
    )
```

### ✅ 批量操作

```python
def test_batch_create_users(user_api, uow):
    """批量创建用户"""

    # ❌ 不推荐 - 逐个创建
    for i in range(100):
        user_api.create_user({"username": f"user_{i}"})

    # ✅ 推荐 - 批量创建
    users_data = [
        {"username": f"user_{i}", "email": f"user{i}@example.com"}
        for i in range(100)
    ]
    user_api.batch_create_users(users_data)
```

### ✅ 使用并行测试

```bash
# 安装pytest-xdist
pip install pytest-xdist

# 并行运行测试（自动检测CPU核心数）
pytest -n auto

# 指定并行数量
pytest -n 4
```

---

## 11. 事件系统与可观测性最佳实践

### ✅ 使用 allure_observer 自动记录 HTTP 请求（v3.17+，⭐推荐）

```python
def test_api_with_allure(allure_observer, http_client):
    """使用 allure_observer 自动记录 HTTP 请求到 Allure 报告

    v3.17.0 新特性：只需注入 allure_observer fixture，
    所有 HTTP 请求会自动记录到 Allure 报告，包括：
    - 请求方法、URL、Headers、Body
    - 响应状态码、Headers、Body
    - OpenTelemetry trace_id/span_id
    - 响应时间
    """
    response = http_client.get("/users/123")
    assert response.status_code == 200
    # ✅ 请求已自动记录到 Allure，无需手动附加
```

**最佳实践**：
- ✅ 在需要详细记录的测试中注入 `allure_observer`
- ✅ 自动关联 OpenTelemetry 追踪信息
- ✅ 支持 HTTP/GraphQL/gRPC 多种协议

### ✅ 使用测试隔离的 EventBus（v3.17+）

```python
from df_test_framework.infrastructure.events import set_test_event_bus, EventBus

def test_with_isolated_event_bus():
    """每个测试使用独立的 EventBus

    v3.17.0 新特性：测试隔离机制确保事件不会跨测试泄漏。
    """
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

### ✅ 使用事件关联追踪请求（v3.17+）

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
client = HttpClient(base_url="...", event_bus=bus)
```

**关键概念**：
- `event_id`: 每个事件的唯一标识（evt-{12hex}）
- `correlation_id`: 关联 Start/End 事件对（cor-{12hex}）
- `trace_id`/`span_id`: OpenTelemetry 追踪上下文

### ✅ 集成 OpenTelemetry 追踪（v3.17+）

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
    client = HttpClient(base_url="...", event_bus=bus)
    response = client.get("/users")
    # ✅ 事件自动包含当前 Span 的 trace_id 和 span_id
```

### ✅ 使用 CleanupManager 自动清理测试数据（v3.11+）

```python
from df_test_framework import DataGenerator

def test_create_order(http_client, cleanup):
    """测试创建订单 - 自动清理数据

    v3.11.0 新特性：CleanupManager 自动清理测试数据。
    """
    # 生成测试标识符
    order_no = DataGenerator.test_id("TEST_ORD")

    # 创建订单
    response = http_client.post("/orders", json={
        "order_no": order_no,
        "amount": 100.00
    })

    # 注册清理
    cleanup.add("orders", order_no)

    assert response.status_code == 201
    # ✅ 测试结束后自动调用 DELETE /orders/{order_no}
```

**调试技巧**：
```bash
# 保留测试数据不清理（用于调试）
pytest --keep-test-data

# 或设置环境变量
KEEP_TEST_DATA=true pytest
```

---

## 📝 总结

### 核心原则

1. **配置集中管理** - 使用Pydantic Settings + 环境变量
2. **API客户端封装** - 使用 @api_class 装饰器或继承 BaseAPI
3. **Repository模式** - 数据库操作封装
4. **Builder模式** - 测试数据构建
5. **Unit of Work模式** - 统一管理事务和Repository，自动回滚
6. **Fixture合理作用域** - Session级别共享资源
7. **明确的断言** - 带清晰的错误消息
8. **Allure步骤** - 测试步骤可视化
9. **测试分类标记** - 使用pytest.mark
10. **性能优化** - Session级别fixture、连接池、并行测试
11. **事件驱动** - 使用 EventBus 和 AllureObserver 增强可观测性（v3.17+）
12. **自动清理** - 使用 CleanupManager 自动清理测试数据（v3.11+）

### v3.17.0 新特性速查

| 特性 | 说明 | 使用场景 |
|------|------|---------|
| **allure_observer** | 自动记录 HTTP 请求到 Allure | 需要详细请求/响应日志的测试 |
| **事件关联** | correlation_id 关联 Start/End 事件 | 追踪完整请求生命周期 |
| **测试隔离** | 每个测试独立的 EventBus | 避免事件跨测试泄漏 |
| **OpenTelemetry 整合** | 自动注入 trace_id/span_id | 分布式追踪 |
| **CleanupManager** | 自动清理测试数据 | 避免数据污染 |

### 下一步

- [快速开始](QUICK_START.md) - 5分钟快速上手
- [快速参考](QUICK_REFERENCE.md) - API 速查表
- [EventBus 指南](../guides/event_bus_guide.md) - 事件系统详解
- [中间件指南](../guides/middleware_guide.md) - 中间件系统详解
- [完整手册](USER_MANUAL.md) - 全面的功能参考

---

**版本历史**:
- v3.17.0 (2025-12-05) - 添加事件系统与可观测性最佳实践
- v1.0 (2025-11-04) - 初始版本
