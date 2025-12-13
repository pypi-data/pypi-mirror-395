# Infrastructure API 参考

基础设施层的完整API参考，包含Bootstrap启动器、RuntimeContext运行时上下文、配置管理和Provider系统。

---

## 📦 模块导入

```python
# Bootstrap启动器
from df_test_framework import Bootstrap

# RuntimeContext
from df_test_framework import RuntimeContext

# 配置类
from df_test_framework import FrameworkSettings
from df_test_framework.infrastructure.config import (
    HTTPConfig,
    DatabaseConfig,
    RedisConfig,
    LoggingConfig,
    TestExecutionConfig,
)

# Provider系统
from df_test_framework.infrastructure.providers import ProviderRegistry

# 或者从具体模块导入
from df_test_framework.infrastructure.bootstrap import Bootstrap
from df_test_framework.infrastructure.runtime import RuntimeContext
from df_test_framework.infrastructure.config.schema import FrameworkSettings
```

---

## 🚀 Bootstrap - 启动器

**说明**: Bootstrap负责编排配置加载、日志设置和运行时初始化。项目可以流畅地自定义每个阶段。

### 核心设计

Bootstrap采用**Builder模式**，通过链式调用配置各个组件，最后构建并运行应用。

```
Bootstrap → with_*() → build() → BootstrapApp → run() → RuntimeContext
```

---

### 初始化

```python
bootstrap = Bootstrap()
```

**默认配置**:
- `settings_cls`: `FrameworkSettings`
- `namespace`: `"default"`
- `sources`: `None`（自动加载.env文件）
- `cache_enabled`: `True`
- `logger_strategy`: `LoguruStructuredStrategy()`
- `provider_factory`: `None`（使用默认providers）
- `plugins`: `[]`

---

### 链式配置方法

#### with_settings()

**功能**: 配置Settings类

**签名**:
```python
def with_settings(
    settings_cls: Type[FrameworkSettings],
    *,
    namespace: str = "default",
    sources: Optional[Iterable[ConfigSource]] = None,
    cache_enabled: bool = True,
) -> Bootstrap
```

**参数**:
- `settings_cls`: Settings类（需继承`FrameworkSettings`）
- `namespace`: 配置命名空间（默认`"default"`）
- `sources`: 配置源列表（默认`None`，自动加载.env）
- `cache_enabled`: 是否缓存配置（默认`True`）

**示例**:
```python
from df_test_framework import Bootstrap, FrameworkSettings
from pydantic import Field

# 1. 定义自定义Settings
class MySettings(FrameworkSettings):
    api_key: str = Field(default="")
    business_config: str = Field(default="default")

# 2. 使用自定义Settings
bootstrap = Bootstrap().with_settings(MySettings)
```

---

#### with_logging()

**功能**: 配置日志策略

**签名**:
```python
def with_logging(strategy: LoggerStrategy) -> Bootstrap
```

**参数**:
- `strategy`: 日志策略对象

**示例**:
```python
from df_test_framework.infrastructure.logging import LoguruStructuredStrategy

strategy = LoguruStructuredStrategy()
bootstrap = Bootstrap().with_logging(strategy)
```

---

#### with_provider_factory()

**功能**: 配置Provider工厂

**签名**:
```python
def with_provider_factory(factory: ProviderFactory) -> Bootstrap
```

**参数**:
- `factory`: Provider工厂函数

**示例**:
```python
from df_test_framework.infrastructure.providers import ProviderRegistry

def my_provider_factory() -> ProviderRegistry:
    registry = ProviderRegistry()
    # 自定义provider注册
    return registry

bootstrap = Bootstrap().with_provider_factory(my_provider_factory)
```

---

#### with_plugin()

**功能**: 添加插件（扩展）

**签名**:
```python
def with_plugin(plugin: Union[str, object]) -> Bootstrap
```

**参数**:
- `plugin`: 插件对象或模块路径

**示例**:
```python
class MyPlugin:
    @hookimpl
    def df_post_bootstrap(self, runtime):
        print("Bootstrap完成后执行")

bootstrap = Bootstrap().with_plugin(MyPlugin())
```

---

#### build()

**功能**: 构建BootstrapApp

**签名**:
```python
def build() -> BootstrapApp
```

**返回**: `BootstrapApp`对象

---

### BootstrapApp - 启动应用

**说明**: 由`Bootstrap.build()`创建，负责执行启动流程。

#### run()

**功能**: 执行Bootstrap流程并返回RuntimeContext

**签名**:
```python
def run(*, force_reload: bool = False) -> RuntimeContext
```

**参数**:
- `force_reload`: 是否强制重新加载配置（默认`False`）

**返回**: `RuntimeContext`对象

**执行流程**:
1. 加载配置（从.env、环境变量等）
2. 初始化日志系统
3. 注册Providers
4. 执行插件Hooks
5. 构建RuntimeContext

**示例**:
```python
app = Bootstrap().with_settings(MySettings).build()
runtime = app.run()
```

---

### 完整使用示例

```python
from df_test_framework import Bootstrap, FrameworkSettings
from pydantic import Field

# 1. 定义项目Settings
class MyProjectSettings(FrameworkSettings):
    """项目配置"""
    api_key: str = Field(default="")
    test_user_id: str = Field(default="test_001")

# 2. 使用Bootstrap链式配置
runtime = (
    Bootstrap()
    .with_settings(MyProjectSettings)
    .build()
    .run()
)

# 3. 使用RuntimeContext
try:
    # 获取配置
    settings = runtime.settings
    print(f"环境: {settings.env}")
    print(f"API Key: {settings.api_key}")

    # 获取HTTP客户端
    http = runtime.http_client()
    response = http.get("/api/users")

    # 获取数据库
    db = runtime.database()
    users = db.query_all("SELECT * FROM users")

    # 获取Redis
    redis = runtime.redis()
    redis.set("key", "value")

finally:
    # 4. 关闭资源
    runtime.close()
```

---

## 🎯 RuntimeContext - 运行时上下文

**说明**: 运行时上下文保存运行时单例，如配置、日志、资源Providers。是测试、fixtures和扩展代码中的主要依赖访问器。

### 属性

| 属性 | 类型 | 说明 |
|-----|------|------|
| `settings` | `FrameworkSettings` | 配置对象 |
| `logger` | `Logger` | 日志对象（loguru） |
| `providers` | `ProviderRegistry` | Provider注册表 |
| `extensions` | `ExtensionManager` | 扩展管理器 |

---

### 核心方法

#### get()

**功能**: 从Provider注册表获取资源

**签名**:
```python
def get(key: str) -> Any
```

**参数**:
- `key`: 资源键名

**示例**:
```python
http_client = runtime.get("http_client")
database = runtime.get("database")
redis = runtime.get("redis")
```

---

#### http_client()

**功能**: 获取HTTP客户端（快捷方法）

**签名**:
```python
def http_client() -> HttpClient
```

**示例**:
```python
http = runtime.http_client()
response = http.get("/api/users")
```

---

#### database()

**功能**: 获取数据库实例（快捷方法）

**签名**:
```python
def database() -> Database
```

**示例**:
```python
db = runtime.database()
users = db.query_all("SELECT * FROM users")
```

---

#### redis()

**功能**: 获取Redis客户端（快捷方法）

**签名**:
```python
def redis() -> RedisClient
```

**示例**:
```python
redis = runtime.redis()
redis.set("session:123", "token_data")
```

---

#### close()

**功能**: 关闭所有资源

**签名**:
```python
def close() -> None
```

**说明**: 调用所有Providers的`shutdown()`方法，释放资源。

**示例**:
```python
try:
    runtime = Bootstrap().build().run()
    # 使用runtime...
finally:
    runtime.close()
```

---

### 使用模式

#### 模式1: 直接使用

```python
# 创建运行时
runtime = Bootstrap().with_settings(MySettings).build().run()

try:
    # 使用
    http = runtime.http_client()
    response = http.get("/api/data")
finally:
    # 清理
    runtime.close()
```

---

#### 模式2: 在Pytest中使用（推荐）

```python
# conftest.py
import pytest
from df_test_framework import Bootstrap
from my_project.config import MySettings

@pytest.fixture(scope="session")
def runtime():
    """运行时上下文fixture"""
    rt = Bootstrap().with_settings(MySettings).build().run()
    yield rt
    rt.close()

# test_example.py
def test_api(runtime):
    """测试中自动注入runtime"""
    http = runtime.http_client()
    response = http.get("/api/users")
    assert response.status_code == 200
```

---

## ⚙️ FrameworkSettings - 配置基类

**说明**: 框架配置基类，基于Pydantic BaseSettings实现。项目应继承此类并扩展业务配置。

### 内置配置字段

| 字段 | 类型 | 默认值 | 说明 |
|-----|------|--------|------|
| `env` | `Literal["dev", "test", "staging", "prod"]` | `"test"` | 运行环境 |
| `debug` | `bool` | `False` | 调试模式 |
| `http` | `HTTPConfig` | `HTTPConfig()` | HTTP客户端配置 |
| `db` | `DatabaseConfig` | `DatabaseConfig()` | 数据库配置 |
| `redis` | `RedisConfig` | `RedisConfig()` | Redis配置 |
| `test` | `TestExecutionConfig` | `TestExecutionConfig()` | 测试执行配置 |
| `logging` | `LoggingConfig` | `LoggingConfig()` | 日志配置 |
| `extras` | `dict` | `{}` | 任意扩展配置 |

---

### 环境检查属性

| 属性 | 返回类型 | 说明 |
|-----|---------|------|
| `is_dev` | `bool` | 是否为开发环境 |
| `is_test` | `bool` | 是否为测试环境 |
| `is_staging` | `bool` | 是否为预发布环境 |
| `is_prod` | `bool` | 是否为生产环境 |

**示例**:
```python
settings = runtime.settings

if settings.is_prod:
    print("生产环境，禁用调试模式")
elif settings.is_test:
    print("测试环境")
```

---

### 环境变量加载

FrameworkSettings基于Pydantic BaseSettings，支持自动从环境变量加载配置。

**前缀**: `APP_`

**嵌套分隔符**: `__`

**示例**:
```bash
# .env文件
APP_ENV=test
APP_DEBUG=false
APP_HTTP__BASE_URL=https://api.example.com
APP_HTTP__TIMEOUT=60
APP_DB__HOST=localhost
APP_DB__PORT=3306
APP_DB__NAME=testdb
APP_DB__USER=root
APP_DB__PASSWORD=secret
APP_REDIS__HOST=localhost
APP_REDIS__PORT=6379
```

```python
# Python代码
settings = MySettings()
print(settings.env)  # "test"
print(settings.http.base_url)  # "https://api.example.com"
print(settings.http.timeout)  # 60
print(settings.db.host)  # "localhost"
```

---

### 自定义Settings

```python
from df_test_framework import FrameworkSettings
from pydantic import Field

class MyProjectSettings(FrameworkSettings):
    """项目配置"""

    # 添加项目特定配置
    api_key: str = Field(default="", description="API密钥")
    test_user_id: str = Field(default="test_001", description="测试用户ID")
    business_timeout: int = Field(default=300, description="业务超时时间（秒）")

    # 嵌套配置
    class FeatureFlags(BaseModel):
        enable_new_feature: bool = Field(default=False)
        enable_cache: bool = Field(default=True)

    features: FeatureFlags = Field(default_factory=FeatureFlags)
```

**环境变量**:
```bash
APP_API_KEY=my_secret_key
APP_TEST_USER_ID=user_001
APP_BUSINESS_TIMEOUT=600
APP_FEATURES__ENABLE_NEW_FEATURE=true
APP_FEATURES__ENABLE_CACHE=false
```

---

## 🔧 配置类详解

### HTTPConfig - HTTP客户端配置

| 字段 | 类型 | 默认值 | 约束 | 说明 |
|-----|------|--------|------|------|
| `base_url` | `Optional[str]` | `None` | - | API基础URL |
| `timeout` | `int` | `30` | 1-300 | 请求超时时间（秒） |
| `max_retries` | `int` | `3` | 0-10 | 重试次数 |
| `verify_ssl` | `bool` | `True` | - | 是否验证SSL证书 |
| `max_connections` | `int` | `50` | 1-500 | 最大连接数 |
| `max_keepalive_connections` | `int` | `20` | 1-200 | Keep-Alive连接数 |

**验证规则**:
- `timeout` ≥ 5秒（警告：不应低于5秒）

**环境变量**:
```bash
APP_HTTP__BASE_URL=https://api.example.com
APP_HTTP__TIMEOUT=60
APP_HTTP__MAX_RETRIES=5
APP_HTTP__VERIFY_SSL=false
```

---

### DatabaseConfig - 数据库配置

| 字段 | 类型 | 默认值 | 约束 | 说明 |
|-----|------|--------|------|------|
| `connection_string` | `Optional[str]` | `None` | - | 数据库连接字符串 |
| `host` | `Optional[str]` | `None` | - | 数据库主机 |
| `port` | `Optional[int]` | `None` | 1-65535 | 数据库端口 |
| `name` | `Optional[str]` | `None` | - | 数据库名/Schema |
| `user` | `Optional[str]` | `None` | - | 用户名 |
| `password` | `Optional[SecretStr]` | `None` | - | 密码（加密） |
| `charset` | `str` | `"utf8mb4"` | - | 连接字符集 |
| `pool_size` | `int` | `10` | 1-100 | 连接池大小 |
| `max_overflow` | `int` | `20` | 0-100 | 额外溢出连接数 |
| `pool_timeout` | `int` | `30` | 1-300 | 连接池超时（秒） |
| `pool_recycle` | `int` | `3600` | ≥60 | 连接回收时间（秒） |
| `pool_pre_ping` | `bool` | `True` | - | 启用连接预检 |
| `echo` | `bool` | `False` | - | 启用SQL日志（调试用） |

**验证规则**:
- `pool_size` ≥ 5（警告：不应低于5）

**方法**:
```python
def resolved_connection_string() -> str
```
**功能**: 解析并返回完整的数据库连接字符串

**示例**:
```python
# 方式1: 使用connection_string
db_config = DatabaseConfig(
    connection_string="mysql+pymysql://user:pass@localhost:3306/testdb?charset=utf8mb4"
)

# 方式2: 使用独立字段（自动构建connection_string）
db_config = DatabaseConfig(
    host="localhost",
    port=3306,
    name="testdb",
    user="root",
    password="secret",
    charset="utf8mb4"
)

connection_str = db_config.resolved_connection_string()
# "mysql+pymysql://root:secret@localhost:3306/testdb?charset=utf8mb4"
```

**环境变量**:
```bash
# 方式1: 直接设置连接字符串
APP_DB__CONNECTION_STRING=mysql+pymysql://user:pass@localhost:3306/db

# 方式2: 独立字段
APP_DB__HOST=localhost
APP_DB__PORT=3306
APP_DB__NAME=testdb
APP_DB__USER=root
APP_DB__PASSWORD=secret
APP_DB__POOL_SIZE=20
```

---

### RedisConfig - Redis配置

| 字段 | 类型 | 默认值 | 约束 | 说明 |
|-----|------|--------|------|------|
| `host` | `str` | `"localhost"` | - | Redis主机 |
| `port` | `int` | `6379` | 1-65535 | Redis端口 |
| `db` | `int` | `0` | 0-15 | Redis数据库索引 |
| `password` | `Optional[SecretStr]` | `None` | - | 密码（加密） |
| `decode_responses` | `bool` | `True` | - | 自动解码为字符串 |
| `socket_timeout` | `int` | `5` | 1-60 | Socket超时（秒） |
| `socket_connect_timeout` | `int` | `5` | 1-60 | 连接超时（秒） |
| `max_connections` | `int` | `50` | 1-1000 | 连接池大小 |
| `retry_on_timeout` | `bool` | `True` | - | 超时时重试 |

**环境变量**:
```bash
APP_REDIS__HOST=redis.example.com
APP_REDIS__PORT=6379
APP_REDIS__DB=1
APP_REDIS__PASSWORD=redis_secret
APP_REDIS__MAX_CONNECTIONS=100
```

---

### TestExecutionConfig - 测试执行配置

| 字段 | 类型 | 默认值 | 约束 | 说明 |
|-----|------|--------|------|------|
| `parallel_workers` | `int` | `4` | 1-64 | 并行Worker数量 |
| `retry_times` | `int` | `0` | 0-5 | 失败重试次数 |
| `default_timeout` | `int` | `300` | 10-3600 | 默认超时时间（秒） |

**验证规则**:
- `parallel_workers` ≤ CPU核心数 × 2

**环境变量**:
```bash
APP_TEST__PARALLEL_WORKERS=8
APP_TEST__RETRY_TIMES=2
APP_TEST__DEFAULT_TIMEOUT=600
```

---

### LoggingConfig - 日志配置

| 字段 | 类型 | 默认值 | 说明 |
|-----|------|--------|------|
| `level` | `Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]` | `"INFO"` | 日志级别 |
| `format` | `Literal["text", "json"]` | `"text"` | 日志格式 |
| `file` | `Optional[str]` | `None` | 日志文件路径 |
| `rotation` | `str` | `"100 MB"` | 日志轮转策略 |
| `retention` | `str` | `"7 days"` | 日志保留策略 |
| `enable_console` | `bool` | `True` | 启用控制台输出 |
| `sanitize` | `bool` | `True` | 自动脱敏敏感字段 |

**环境变量**:
```bash
APP_LOGGING__LEVEL=DEBUG
APP_LOGGING__FORMAT=json
APP_LOGGING__FILE=logs/test.log
APP_LOGGING__ENABLE_CONSOLE=true
```

---

## 📚 完整配置示例

### 项目Settings定义

```python
# src/my_project/config/settings.py
from df_test_framework import FrameworkSettings
from pydantic import Field, BaseModel

class BusinessConfig(BaseModel):
    """业务配置"""
    test_user_id: str = Field(default="test_001")
    admin_user_id: str = Field(default="admin_001")
    default_card_template: str = Field(default="TPL_001")

class MyProjectSettings(FrameworkSettings):
    """项目配置"""

    # 项目特定配置
    api_key: str = Field(default="", description="API密钥")
    business: BusinessConfig = Field(
        default_factory=BusinessConfig,
        description="业务配置"
    )

    # 覆盖默认值（可选）
    class Config:
        env_prefix = "MY_APP_"  # 自定义前缀
```

---

### .env配置文件

```bash
# .env

# 框架配置
MY_APP_ENV=test
MY_APP_DEBUG=false

# HTTP配置
MY_APP_HTTP__BASE_URL=https://api-test.example.com
MY_APP_HTTP__TIMEOUT=60
MY_APP_HTTP__MAX_RETRIES=5

# 数据库配置
MY_APP_DB__CONNECTION_STRING=mysql+pymysql://root:secret@localhost:3306/testdb?charset=utf8mb4
MY_APP_DB__POOL_SIZE=20

# Redis配置
MY_APP_REDIS__HOST=localhost
MY_APP_REDIS__PORT=6379
MY_APP_REDIS__DB=1

# 日志配置
MY_APP_LOGGING__LEVEL=DEBUG
MY_APP_LOGGING__FORMAT=json
MY_APP_LOGGING__FILE=logs/test.log

# 业务配置
MY_APP_API_KEY=my_secret_api_key
MY_APP_BUSINESS__TEST_USER_ID=user_test_001
MY_APP_BUSINESS__ADMIN_USER_ID=admin_001
MY_APP_BUSINESS__DEFAULT_CARD_TEMPLATE=TPL_DEFAULT
```

---

### 在测试中使用

```python
# tests/conftest.py
import pytest
from df_test_framework import Bootstrap
from my_project.config.settings import MyProjectSettings

pytest_plugins = ["df_test_framework.testing.fixtures.core"]

@pytest.fixture(scope="session")
def runtime():
    """运行时上下文"""
    rt = (
        Bootstrap()
        .with_settings(MyProjectSettings)
        .build()
        .run()
    )
    yield rt
    rt.close()

# tests/test_example.py
def test_with_config(runtime):
    """测试中使用配置"""

    # 访问配置
    settings = runtime.settings
    assert settings.env == "test"
    assert settings.api_key != ""

    # 访问业务配置
    assert settings.business.test_user_id == "user_test_001"

    # 使用HTTP客户端（自动使用配置中的base_url）
    http = runtime.http_client()
    response = http.get("/api/health")
    assert response.status_code == 200

    # 使用数据库（自动使用配置中的连接字符串）
    db = runtime.database()
    result = db.query_one("SELECT 1 as num")
    assert result["num"] == 1
```

---

## 🔗 相关文档

### v3架构文档
- [Clients API](clients.md) - HTTP客户端
- [Databases API](databases.md) - 数据访问（Database、Redis、Repository）
- [Drivers API](drivers.md) - Web自动化
- [Testing API](testing.md) - Pytest Fixtures和测试辅助工具
- [Extensions API](extensions.md) - 扩展系统和Hooks

### v2兼容文档
- [Core API](core.md) - v2版核心功能（已迁移）
- [Patterns API](patterns.md) - v2版设计模式（已迁移）

### 其他资源
- [配置管理指南](../user-guide/configuration.md) - 配置详解
- [快速入门](../getting-started/quickstart.md) - 5分钟上手指南
- [v2→v3迁移](../migration/v2-to-v3.md) - 迁移指南

---

**返回**: [API参考首页](README.md) | [文档首页](../README.md)
