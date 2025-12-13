# v3.5 快速开始指南

> **框架版本**: df-test-framework v3.5.0
> **预计时间**: 5分钟快速上手
> **更新日期**: 2025-11-07

---

## 🎯 5分钟快速上手

跟随以下步骤，5分钟内创建并运行你的第一个测试！

### Step 1: 安装框架（30秒）

```bash
# 使用uv（推荐）
pip install uv
uv pip install df-test-framework

# 或使用pip
pip install df-test-framework
```

---

### Step 2: 创建项目结构（1分钟）

```bash
# 创建项目目录
mkdir my-test-project
cd my-test-project

# 创建标准目录结构
mkdir -p src/my_test/config tests

# 创建配置文件
touch src/my_test/__init__.py
touch src/my_test/config/__init__.py
touch src/my_test/config/settings.py
touch tests/conftest.py
touch tests/test_api.py
touch pytest.ini
touch .env
```

**目录结构**:
```
my-test-project/
├── src/
│   └── my_test/
│       ├── __init__.py
│       └── config/
│           ├── __init__.py
│           └── settings.py  # 配置文件
├── tests/
│   ├── conftest.py          # pytest配置
│   └── test_api.py          # 测试文件
├── pytest.ini               # pytest配置
└── .env                     # 环境变量
```

---

### Step 3: 配置框架（2分钟）

#### 3.1 创建settings.py

```python
# src/my_test/config/settings.py
"""项目配置

v3.5+ 完全声明式配置 - 使用 HTTPSettings 嵌套配置
- ✅ 不需要 load_dotenv() 和 os.getenv()
- ✅ Pydantic 自动加载 .env 文件和环境变量
- ✅ 零代码中间件配置（声明式）
"""

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from df_test_framework import FrameworkSettings
from df_test_framework.infrastructure.config import (
    HTTPSettings,
    SignatureMiddlewareSettings,
)


# 自定义HTTP配置（继承HTTPSettings）
class MyHTTPSettings(HTTPSettings):
    """项目HTTP配置 - 自定义默认值

    v3.5+ 特性:
    - ✅ 嵌套中间件配置
    - ✅ 自动环境变量绑定
    - ✅ 所有配置都可通过环境变量覆盖
    """

    # HTTP基础配置 - 自定义默认值
    base_url: str = Field(
        default="https://jsonplaceholder.typicode.com",
        description="API基础URL"
    )

    # 可选：启用签名中间件
    # 取消下面的注释来启用
    # signature: SignatureMiddlewareSettings = Field(
    #     default_factory=lambda: SignatureMiddlewareSettings(
    #         enabled=True,
    #         priority=10,
    #         algorithm="md5",
    #         secret="your_secret_key",  # ⚠️ 生产环境通过APP_SIGNATURE_SECRET覆盖
    #         header_name="X-Sign",
    #         include_paths=["/api/**"],
    #     )
    # )


class MyTestSettings(FrameworkSettings):
    """测试项目配置

    v3.5+ 特性:
    - ✅ 使用 HTTPSettings 嵌套配置
    - ✅ 完全声明式，零手动代码
    - ✅ Pydantic 自动加载 .env 和环境变量
    """

    # 使用自定义的HTTPSettings
    http_settings: MyHTTPSettings = Field(
        default_factory=MyHTTPSettings,
        description="HTTP配置（包含中间件）"
    )

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_nested_delimiter="__",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
```

#### 3.2 配置pytest.ini

```ini
[pytest]
# Python路径
pythonpath = src

# 测试路径
testpaths = tests

# 框架配置 - 指定settings类
df_settings_class = my_test.config.settings.MyTestSettings

# 命令行选项
addopts =
    -v
    --tb=short
```

#### 3.3 配置.env

```bash
# .env
# API配置
APP_HTTP__BASE_URL=https://jsonplaceholder.typicode.com
APP_HTTP__TIMEOUT=30

# 可观测性
APP_DEBUG=false
APP_LOGGING__LEVEL=INFO
```

#### 3.4 创建conftest.py

```python
# tests/conftest.py
"""Pytest全局配置和Fixtures"""

import pytest

# 启用框架的pytest插件
pytest_plugins = ["df_test_framework.testing.fixtures.core"]

# 框架会自动提供以下fixtures:
# - runtime: RuntimeContext对象
# - http_client: HttpClient对象
# - database: Database对象（如果配置了）
# - redis_client: RedisClient对象（如果配置了）
```

---

### Step 4: 编写第一个测试（1分钟）

```python
# tests/test_api.py
"""API测试示例"""

def test_get_users(http_client):
    """测试获取用户列表"""
    response = http_client.get("/users")

    # 验证状态码
    assert response.status_code == 200

    # 验证响应数据
    users = response.json()
    assert len(users) > 0
    assert "id" in users[0]
    assert "name" in users[0]


def test_get_single_user(http_client):
    """测试获取单个用户"""
    response = http_client.get("/users/1")

    assert response.status_code == 200

    user = response.json()
    assert user["id"] == 1
    assert "name" in user
    assert "email" in user


def test_create_user(http_client):
    """测试创建用户"""
    new_user = {
        "name": "John Doe",
        "username": "johndoe",
        "email": "john@example.com"
    }

    response = http_client.post("/users", json=new_user)

    assert response.status_code == 201
    created_user = response.json()
    assert created_user["name"] == new_user["name"]
```

---

### Step 5: 运行测试（30秒）

```bash
# 运行所有测试
pytest

# 运行带详细日志
pytest -v -s

# 运行特定测试
pytest tests/test_api.py::test_get_users

# 运行并生成Allure报告
pytest --alluredir=./allure-results
allure serve ./allure-results
```

**期望输出**:
```
================================ test session starts ================================
platform linux -- Python 3.12+, pytest-8.4.2, pluggy-1.6.0
collected 3 items

tests/test_api.py::test_get_users PASSED                                      [ 33%]
tests/test_api.py::test_get_single_user PASSED                                [ 66%]
tests/test_api.py::test_create_user PASSED                                    [100%]

================================= 3 passed in 0.50s =================================
```

---

## ✨ v3.5核心特性演示

### 1. 配置化中间件

无需手写拦截逻辑，在settings.py中声明式配置即可。

#### 签名中间件（v3.5+ 声明式配置）

```python
from df_test_framework.infrastructure.config import (
    HTTPSettings,
    SignatureMiddlewareSettings,
)

class MyHTTPSettings(HTTPSettings):
    """HTTP配置 - 启用签名中间件"""

    base_url: str = Field(
        default="https://api.example.com",
        description="API基础URL"
    )

    # 签名中间件配置
    signature: SignatureMiddlewareSettings = Field(
        default_factory=lambda: SignatureMiddlewareSettings(
            enabled=True,
            priority=10,
            algorithm="md5",  # 或 sha256, hmac-sha256
            secret="my_secret",  # ⚠️ 生产环境通过APP_SIGNATURE_SECRET覆盖
            header_name="X-Sign",
            include_paths=["/api/**"],  # 路径匹配
            exclude_paths=["/health"],   # 排除路径
            include_query_params=True,
            include_json_body=True,
        )
    )
```

**环境变量覆盖** (`.env`):
```bash
APP_SIGNATURE_ENABLED=true
APP_SIGNATURE_ALGORITHM=md5
APP_SIGNATURE_SECRET=production_secret_key
```

#### Bearer Token中间件（v3.5+ 声明式配置）

```python
from df_test_framework.infrastructure.config import (
    HTTPSettings,
    BearerTokenMiddlewareSettings,
)

class MyHTTPSettings(HTTPSettings):
    """HTTP配置 - 启用Bearer Token中间件"""

    base_url: str = Field(
        default="https://api.example.com",
        description="API基础URL"
    )

    # Bearer Token中间件配置
    token: BearerTokenMiddlewareSettings = Field(
        default_factory=lambda: BearerTokenMiddlewareSettings(
            enabled=True,
            priority=20,
            token_source="login",  # 自动登录
            login_url="/admin/auth/login",
            username="admin",  # ⚠️ 生产环境通过APP_TOKEN_USERNAME覆盖
            password="admin123",  # ⚠️ 生产环境通过APP_TOKEN_PASSWORD覆盖
            token_field_path="data.token",  # Token在响应中的路径
            header_name="Authorization",
            token_prefix="Bearer",
            include_paths=["/admin/**"],
        )
    )
```

**环境变量覆盖** (`.env`):
```bash
APP_TOKEN_ENABLED=true
APP_TOKEN_USERNAME=prod_admin
APP_TOKEN_PASSWORD=prod_password123
```

---

### 2. Profile环境配置

支持多环境配置文件自动加载。

#### 创建环境配置

```bash
# 创建不同环境的配置文件
.env              # 基础配置
.env.dev          # 开发环境
.env.test         # 测试环境
.env.prod         # 生产环境
```

```bash
# .env.dev
APP_HTTP__BASE_URL=https://dev-api.example.com
APP_DEBUG=true
APP_LOGGING__LEVEL=DEBUG

# .env.test
APP_HTTP__BASE_URL=https://test-api.example.com
APP_DEBUG=false
APP_LOGGING__LEVEL=INFO

# .env.prod
APP_HTTP__BASE_URL=https://api.example.com
APP_DEBUG=false
APP_LOGGING__LEVEL=WARNING
```

#### 切换环境

```bash
# 使用dev环境
ENV=dev pytest

# 使用test环境
ENV=test pytest

# 使用prod环境
ENV=prod pytest
```

---

### 3. 运行时配置覆盖

使用`with_overrides()`实现测试隔离。

```python
def test_with_custom_timeout(runtime_ctx):
    """演示运行时配置覆盖"""

    # 创建临时上下文，修改超时时间为5秒
    test_ctx = runtime_ctx.with_overrides({
        "http.timeout": 5,
        "http.max_retries": 1,
    })

    # 使用临时配置
    client = test_ctx.http_client()
    response = client.get("/api/slow-endpoint")

    # 原始runtime_ctx不受影响（不可变设计）
    assert runtime_ctx.settings.http.timeout == 30  # 仍然是30秒
```

---

### 4. 可观测性集成

v3.5.0自动提供完整的可观测性日志。

```python
# settings.py中启用可观测性
from df_test_framework import LoggingConfig

class MyTestSettings(FrameworkSettings):
    logging: LoggingConfig = Field(
        default_factory=lambda: LoggingConfig(
            level="INFO",
            enable_observability=True,  # 启用可观测性
            enable_http_logging=True,   # HTTP请求日志
            enable_db_logging=True,     # 数据库操作日志
        )
    )
```

**日志输出示例**:
```
[2025-11-07 22:13:47] | INFO | [ObservabilityLogger] → POST /api/users
[2025-11-07 22:13:47] | INFO | [SignatureMiddleware] 已生成签名: abc123...
[2025-11-07 22:13:47] | INFO | [ObservabilityLogger] ← 200 OK (192.3ms)
```

---

## 📚 下一步

恭喜！你已经完成了v3.5快速开始。

### 深入学习

1. **完整用户手册** - [USER_MANUAL.md](USER_MANUAL.md)
   - 详细的API文档
   - 高级特性说明
   - 最佳实践指南

2. **示例代码库** - [examples/](../../examples/)
   - 基础示例
   - 设计模式
   - v3.5新特性示例

3. **最佳实践** - [VERIFIED_BEST_PRACTICES.md](VERIFIED_BEST_PRACTICES.md)
   - 经过验证的最佳实践
   - 常见问题解决方案

### 高级主题

- **配置化中间件** - [INTERCEPTOR_CONFIG_BEST_PRACTICES.md](../INTERCEPTOR_CONFIG_BEST_PRACTICES.md)
- **扩展系统** - [extensions.md](extensions.md)
- **CI/CD集成** - [ci-cd.md](ci-cd.md)
- **性能优化** - [debugging.md](debugging.md)

---

## ❓ 常见问题

### Q: 如何配置数据库？

```python
from df_test_framework import DatabaseConfig

class MyTestSettings(FrameworkSettings):
    db: DatabaseConfig = Field(
        default_factory=lambda: DatabaseConfig(
            host=os.getenv("APP_DB__HOST", "localhost"),
            port=int(os.getenv("APP_DB__PORT", "3306")),
            name=os.getenv("APP_DB__NAME", "test_db"),
            user=os.getenv("APP_DB__USER", "root"),
            password=os.getenv("APP_DB__PASSWORD", "password"),
        )
    )
```

### Q: 如何使用数据库fixture？

```python
def test_database_operations(database):
    """使用database fixture"""
    # 查询
    result = database.query_one("SELECT * FROM users WHERE id = :id", {"id": 1})

    # 插入
    user_id = database.insert("users", {"name": "John", "email": "john@example.com"})

    # 更新
    database.update("users", {"name": "Jane"}, {"id": user_id})

    # 删除
    database.delete("users", {"id": user_id})
```

### Q: 如何生成测试报告？

```bash
# 生成Allure报告
pytest --alluredir=./allure-results
allure serve ./allure-results

# 生成HTML报告
pytest --html=report.html --self-contained-html
```

### Q: 如何调试测试？

```bash
# 显示print输出
pytest -s

# 显示详细日志
pytest -v -s

# 在失败时进入调试器
pytest --pdb

# 启用DEBUG日志
APP_LOGGING__LEVEL=DEBUG pytest -v -s
```

---

## 💡 提示

### 开发建议

1. **使用.env.local** - 本地配置覆盖，不提交git
2. **启用可观测性** - 便于调试和问题排查
3. **使用with_overrides** - 测试隔离，避免测试间干扰
4. **合理使用中间件** - 签名、认证等交给中间件处理

### 性能优化

1. **合理设置超时** - 避免测试挂起
2. **使用连接池** - 数据库和HTTP连接复用
3. **并行执行测试** - 使用pytest-xdist

```bash
# 并行执行（4个worker）
pytest -n 4
```

### 最佳实践

1. **一个测试一个断言** - 测试失败时容易定位
2. **使用有意义的测试名** - test_create_user_should_return_201
3. **清理测试数据** - 使用db_transaction或cleanup fixtures
4. **独立的测试** - 不依赖其他测试的执行顺序

---

## 🎯 总结

你已经学会了：

- ✅ 安装和配置df-test-framework v3.5.0
- ✅ 创建标准项目结构
- ✅ 配置化中间件（签名、Token）
- ✅ Profile环境配置
- ✅ 运行时配置覆盖
- ✅ 编写和运行测试

**下一步**: 查看[完整用户手册](USER_MANUAL.md)深入了解框架能力，或浏览[示例代码](../../examples/)学习最佳实践。

---

**获取帮助**:
- 📖 查阅[文档索引](../DOCUMENTATION_INDEX.md)
- 💬 提交[Issue](https://github.com/yourorg/df-test-framework/issues)
- 📧 联系团队

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
