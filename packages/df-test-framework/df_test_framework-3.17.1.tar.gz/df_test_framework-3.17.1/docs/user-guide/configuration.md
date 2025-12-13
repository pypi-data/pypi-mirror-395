# 配置管理最佳实践 (2025现代化方案)

## 📋 目录

1. [为什么选择pydantic-settings](#为什么选择pydantic-settings)
2. [核心概念](#核心概念)
3. [完整实现示例](#完整实现示例)
4. [配置文件组织](#配置文件组织)
5. [使用方式](#使用方式)
6. [最佳实践](#最佳实践)
7. [常见问题](#常见问题)

---

## 为什么选择pydantic-settings

### 方案对比

| 配置方式 | 类型安全 | 自动验证 | 环境变量 | 学习曲线 | 推荐度 |
|---------|---------|---------|---------|---------|--------|
| **pydantic-settings 2.0+** | ✅ | ✅ | ✅ | 中等 | ⭐⭐⭐⭐⭐ |
| **Dynaconf** | ⚠️ 部分 | ⚠️ 需配置 | ✅ | 较陡 | ⭐⭐⭐⭐ |
| **python-decouple** | ❌ | ❌ | ✅ | 简单 | ⭐⭐⭐ |
| **YAML/JSON** | ❌ | ❌ | ❌ | 简单 | ⭐⭐ |

### pydantic-settings 2.0+ 的核心优势

#### 1. ✅ 类型安全和自动验证
```python
class Settings(BaseSettings):
    port: int = 8080  # 自动验证必须是整数
    timeout: int = Field(ge=1, le=300)  # 必须在1-300之间
```

**效果**: 配置错误在启动时立即发现,不会等到运行时才报错

#### 2. ✅ 嵌套配置和复杂结构
```python
class DatabaseConfig(BaseModel):
    host: str = "localhost"
    port: int = 3306

class Settings(BaseSettings):
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)

# 访问: settings.db.host
# 环境变量: APP_DB__HOST=localhost
```

#### 3. ✅ 密钥保护 (SecretStr)
```python
password: SecretStr = Field(default=SecretStr("secret"))

# 打印时自动隐藏
print(settings.password)  # **********

# 需要显式获取
actual_pwd = settings.password.get_secret_value()
```

#### 4. ✅ 配置优先级清晰
```
1. CLI参数 (可选,通过cli_parse_args=True启用)
   ↓
2. 环境变量 (生产环境推荐)
   ↓
3. .env.{ENV} 文件 (环境特定配置)
   ↓
4. .env 文件 (基础配置)
   ↓
5. 默认值 (代码中定义)
```

#### 5. ✅ 云原生支持
- AWS Secrets Manager
- Azure Key Vault
- Google Secret Manager
- Docker/K8s Secrets挂载

---

## 核心概念

### 1. 环境变量命名规则

**前缀**: 使用 `APP_` 避免冲突
```bash
APP_ENV=test
APP_LOG_LEVEL=DEBUG
```

**嵌套**: 使用 `__` (双下划线) 表示层级
```bash
APP_DB__HOST=localhost          # → settings.db.host
APP_DB__PORT=3306              # → settings.db.port
APP_API__TIMEOUT=30            # → settings.api.timeout
```

**不区分大小写**: (通过 `case_sensitive=False`)
```bash
APP_LOG_LEVEL=INFO
app_log_level=info  # 等效
```

### 2. 配置文件加载顺序

```python
model_config = SettingsConfigDict(
    env_file=(
        ".env",                                # 1. 基础配置 (提交git)
        f".env.{os.getenv('ENV', 'test')}",   # 2. 环境特定 (提交git)
        ".env.local",                          # 3. 本地覆盖 (不提交)
    )
)
```

**实际加载**:
```bash
ENV=test pytest
# 加载顺序: .env → .env.test → .env.local
# 后面的文件覆盖前面的配置
```

### 3. 配置验证

```python
from pydantic import Field, field_validator

class Settings(BaseSettings):
    port: int = Field(ge=1, le=65535)  # 范围验证

    @field_validator('port')
    @classmethod
    def validate_port(cls, v: int) -> int:
        if v < 1024:
            raise ValueError('端口应大于1024避免需要root权限')
        return v
```

---

## 完整实现示例

### gift-card-test 项目的完整配置

```python
"""config/settings.py - 现代化配置管理"""

import os
from typing import Literal, Optional
from pydantic import BaseModel, Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


# ========== 嵌套配置模型 ==========

class APIConfig(BaseModel):
    """API配置"""
    base_url: str = "http://47.94.57.99:8088/api"
    timeout: int = Field(default=30, ge=1, le=300)
    max_retries: int = Field(default=3, ge=0, le=10)
    verify_ssl: bool = True

    @field_validator('timeout')
    @classmethod
    def validate_timeout(cls, v: int) -> int:
        if v < 5:
            raise ValueError('超时时间不应小于5秒')
        return v


class DatabaseConfig(BaseModel):
    """数据库配置"""
    host: str = "localhost"
    port: int = Field(default=3306, ge=1, le=65535)
    name: str = "test_db"
    user: str = "root"
    password: SecretStr = Field(default=SecretStr("password"))
    charset: str = "utf8mb4"
    pool_size: int = Field(default=10, ge=1, le=100)

    @property
    def connection_string(self) -> str:
        """构建数据库连接字符串"""
        pwd = self.password.get_secret_value()
        return f"mysql+pymysql://{self.user}:{pwd}@{self.host}:{self.port}/{self.name}"


class RedisConfig(BaseModel):
    """Redis配置"""
    host: str = "localhost"
    port: int = 6379
    db: int = Field(default=0, ge=0, le=15)
    password: Optional[SecretStr] = None


class TestConfig(BaseModel):
    """测试配置"""
    parallel_workers: int = Field(default=4, ge=1, le=32)
    retry_times: int = Field(default=2, ge=0, le=5)

    @field_validator('parallel_workers')
    @classmethod
    def validate_workers(cls, v: int) -> int:
        import os
        cpu_count = os.cpu_count() or 4
        if v > cpu_count * 2:
            raise ValueError(f'worker数量({v})不应超过CPU核心数的2倍({cpu_count * 2})')
        return v


class BusinessConfig(BaseSettings):
    """业务配置（v3.5+ 推荐使用 BaseSettings + 独立前缀）

    注意：
    - ✅ 继承 BaseSettings 而不是 BaseModel
    - ✅ 使用独立的 env_prefix="BUSINESS_"
    - ✅ 环境变量使用 BUSINESS_* 而不是 APP_BUSINESS__*

    详细说明请参考：docs/user-guide/nested-settings-guide.md
    """
    default_card_amount: str = Field(default="100.00", description="默认卡面额")
    test_user_id: str = Field(default="test_user_001", description="测试用户ID")

    model_config = SettingsConfigDict(
        env_prefix="BUSINESS_",  # 独立的环境变量前缀
        env_file=".env",
        extra="ignore",
    )


# ========== 主配置类 ==========

class Settings(BaseSettings):
    """
    应用配置管理类

    配置加载优先级(从高到低):
    1. 环境变量 (APP_API__BASE_URL)
    2. .env.{ENV} 文件 (环境特定配置)
    3. .env 文件 (基础配置)
    4. 默认值 (代码中定义)
    """

    # ========== 环境配置 ==========
    env: Literal["dev", "test", "staging", "prod"] = "test"
    debug: bool = False

    # ========== 日志配置 ==========
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    log_format: Literal["json", "text"] = "text"

    # ========== 嵌套配置 ==========
    api: APIConfig = Field(default_factory=APIConfig)
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    test: TestConfig = Field(default_factory=TestConfig)
    business: BusinessConfig = Field(default_factory=BusinessConfig)

    # ========== pydantic-settings配置 ==========
    model_config = SettingsConfigDict(
        env_prefix="APP_",                              # 环境变量前缀
        env_nested_delimiter="__",                       # 嵌套分隔符
        case_sensitive=False,                            # 不区分大小写
        env_ignore_empty=True,                           # 忽略空环境变量
        extra="ignore",                                  # 忽略额外字段
        env_file=(
            ".env",                                      # 基础配置
            f".env.{os.getenv('ENV', 'test')}",         # 环境特定
            ".env.local",                                # 本地覆盖
        ),
        env_file_encoding="utf-8",
        validate_default=True,                           # 验证默认值
    )

    # ========== 计算属性 ==========

    @property
    def is_production(self) -> bool:
        return self.env == "prod"

    @property
    def is_debug_enabled(self) -> bool:
        return self.debug or self.env == "dev"

    # ========== 自定义验证 ==========

    @field_validator('env')
    @classmethod
    def validate_env(cls, v: str) -> str:
        """禁止在CI环境使用生产配置"""
        if v == "prod" and os.getenv("CI") == "true":
            raise ValueError("禁止在CI环境使用生产配置")
        return v

    def model_post_init(self, __context) -> None:
        """配置加载后的安全检查"""
        if self.is_production:
            # 生产环境不能使用默认密码
            if self.db.password.get_secret_value() == "password":
                raise ValueError("生产环境必须设置真实的数据库密码")


# ========== 单例模式 ==========

_settings_instance: Optional[Settings] = None

def get_settings(force_reload: bool = False) -> Settings:
    """获取全局配置实例(单例)"""
    global _settings_instance
    if _settings_instance is None or force_reload:
        _settings_instance = Settings()
    return _settings_instance


def create_settings(**overrides) -> Settings:
    """
    创建配置实例,支持覆盖(用于测试)

    示例:
        test_settings = create_settings(
            env="test",
            api__base_url="http://test-api.com",
            db__host="test-db",
        )
    """
    # 处理双下划线嵌套配置
    processed = {}
    nested_configs = {}

    for key, value in overrides.items():
        if '__' in key:
            parent, child = key.split('__', 1)
            if parent not in nested_configs:
                nested_configs[parent] = {}
            nested_configs[parent][child] = value
        else:
            processed[key] = value

    # 合并嵌套配置
    for parent, children in nested_configs.items():
        if parent in processed and isinstance(processed[parent], dict):
            processed[parent].update(children)
        else:
            processed[parent] = children

    return Settings(**processed)


# ========== 全局实例 ==========
settings = get_settings()

__all__ = ["settings", "get_settings", "create_settings", "Settings"]
```

---

## HTTP配置和中间件（v3.5+ 声明式配置）

### 为什么要用HTTPSettings？

v3.5+引入了`HTTPSettings`类，实现了**完全声明式的HTTP和中间件配置**：

**优势**：
- ✅ **零手动代码**：不需要手动创建`HTTPConfig`和中间件对象
- ✅ **嵌套配置**：`HTTPSettings` → `SignatureMiddlewareSettings` + `BearerTokenMiddlewareSettings`
- ✅ **自动加载**：中间件根据配置自动启用/禁用
- ✅ **类型安全**：完整的Pydantic类型验证
- ✅ **环境变量绑定**：所有配置都可通过环境变量覆盖

### HTTPSettings 类结构

```python
from df_test_framework.infrastructure.config import (
    HTTPSettings,
    SignatureMiddlewareSettings,
    BearerTokenMiddlewareSettings,
)

# ========== 中间件Settings类 ==========

class SignatureMiddlewareSettings(BaseSettings):
    """签名中间件配置 - 完全声明式

    环境变量（使用APP_SIGNATURE_前缀）:
        APP_SIGNATURE_ENABLED - 是否启用签名中间件
        APP_SIGNATURE_ALGORITHM - 签名算法（md5/sha256/hmac-sha256）
        APP_SIGNATURE_SECRET - 签名密钥
        APP_SIGNATURE_HEADER_NAME - 签名Header名称
        APP_SIGNATURE_INCLUDE_PATHS - 包含的路径模式
        APP_SIGNATURE_EXCLUDE_PATHS - 排除的路径模式
    """
    enabled: bool = Field(default=False, description="是否启用")
    priority: int = Field(default=10, description="中间件优先级")
    algorithm: str = Field(default="md5", description="签名算法")
    secret: str = Field(default="change_me", description="签名密钥")
    header_name: str = Field(default="X-Sign", description="签名Header")
    include_paths: list[str] = Field(default_factory=lambda: ["/**"])
    exclude_paths: list[str] = Field(default_factory=list)
    # ... 更多配置字段

    model_config = SettingsConfigDict(
        env_prefix="APP_SIGNATURE_",  # 独立前缀
        env_file=".env",
    )

class BearerTokenMiddlewareSettings(BaseSettings):
    """Bearer Token中间件配置

    环境变量（使用APP_TOKEN_前缀）:
        APP_TOKEN_ENABLED - 是否启用Token中间件
        APP_TOKEN_TOKEN_SOURCE - Token来源（login/env/file）
        APP_TOKEN_USERNAME - 登录用户名（token_source=login时）
        APP_TOKEN_PASSWORD - 登录密码
        APP_TOKEN_LOGIN_URL - 登录接口URL
    """
    enabled: bool = Field(default=False)
    priority: int = Field(default=20)
    token_source: str = Field(default="login")
    username: str = Field(default="admin")
    password: str = Field(default="password")
    login_url: str = Field(default="/auth/login")
    # ... 更多配置字段

    model_config = SettingsConfigDict(
        env_prefix="APP_TOKEN_",
        env_file=".env",
    )

# ========== HTTPSettings主类 ==========

class HTTPSettings(BaseSettings):
    """HTTP配置 - 嵌套中间件配置

    完全声明式，包含HTTP基础配置和中间件配置。

    环境变量:
        # HTTP基础配置
        APP_HTTP_BASE_URL - API基础URL
        APP_HTTP_TIMEOUT - 请求超时时间（秒）
        APP_HTTP_MAX_RETRIES - 最大重试次数

        # 签名中间件（通过APP_SIGNATURE_前缀）
        APP_SIGNATURE_ENABLED - 是否启用
        APP_SIGNATURE_SECRET - 签名密钥

        # Token中间件（通过APP_TOKEN_前缀）
        APP_TOKEN_ENABLED - 是否启用
        APP_TOKEN_USERNAME - 登录用户名
    """

    # HTTP基础配置
    base_url: str = Field(default="http://localhost:8000")
    timeout: int = Field(default=30)
    max_retries: int = Field(default=3)
    verify_ssl: bool = Field(default=True)

    # 嵌套中间件配置
    signature: SignatureMiddlewareSettings = Field(
        default_factory=SignatureMiddlewareSettings
    )
    token: BearerTokenMiddlewareSettings = Field(
        default_factory=BearerTokenMiddlewareSettings
    )

    model_config = SettingsConfigDict(
        env_prefix="APP_HTTP_",
        env_nested_delimiter="__",
        env_file=".env",
    )

    @property
    def http_config(self) -> HTTPConfig:
        """自动构建HTTPConfig对象

        根据Settings配置自动构建HTTPConfig，包括：
        1. HTTP基础配置（base_url, timeout等）
        2. 启用的中间件配置

        Returns:
            HTTPConfig对象，包含所有配置和启用的中间件
        """
        from .schema import HTTPConfig

        # 收集所有启用的中间件
        middlewares = []
        if sig_config := self.signature.to_config():
            middlewares.append(sig_config)
        if token_config := self.token.to_config():
            middlewares.append(token_config)

        # 按优先级排序
        middlewares.sort(key=lambda x: x.priority)

        return HTTPConfig(
            base_url=self.base_url,
            timeout=self.timeout,
            max_retries=self.max_retries,
            verify_ssl=self.verify_ssl,
            middlewares=middlewares,
        )
```

### 在项目中使用HTTPSettings

#### 方式1：继承并自定义默认值（推荐）

```python
"""config/settings.py"""

from pydantic import Field
from pydantic_settings import SettingsConfigDict
from df_test_framework import FrameworkSettings
from df_test_framework.infrastructure.config import (
    HTTPSettings,
    SignatureMiddlewareSettings,
    BearerTokenMiddlewareSettings,
)

# 自定义HTTP配置（继承HTTPSettings）
class ProjectHTTPSettings(HTTPSettings):
    """项目HTTP配置 - 自定义默认值"""

    # 覆盖HTTP基础配置的默认值
    base_url: str = Field(
        default="https://api.example.com",
        description="API基础URL"
    )

    # 覆盖签名中间件的默认值
    signature: SignatureMiddlewareSettings = Field(
        default_factory=lambda: SignatureMiddlewareSettings(
            enabled=True,  # 默认启用
            algorithm="md5",
            secret="your_secret_key",
            include_paths=["/api/**"],
            exclude_paths=["/health", "/metrics"],
        )
    )

    # 覆盖Token中间件的默认值
    token: BearerTokenMiddlewareSettings = Field(
        default_factory=lambda: BearerTokenMiddlewareSettings(
            enabled=True,  # 默认启用
            token_source="login",
            login_url="/auth/login",
            username="admin",
            password="admin123",
            include_paths=["/admin/**"],
        )
    )

# 项目主配置
class ProjectSettings(FrameworkSettings):
    """项目配置"""

    # 使用自定义的HTTPSettings
    http_settings: ProjectHTTPSettings = Field(
        default_factory=ProjectHTTPSettings,
        description="HTTP配置（包含中间件）"
    )

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
    )
```

**环境变量配置（`.env`）**：

```bash
# HTTP基础配置
APP_HTTP_BASE_URL=https://api.prod.com
APP_HTTP_TIMEOUT=60

# 签名中间件配置
APP_SIGNATURE_ENABLED=true
APP_SIGNATURE_ALGORITHM=hmac-sha256
APP_SIGNATURE_SECRET=prod_secret_key

# Token中间件配置
APP_TOKEN_ENABLED=true
APP_TOKEN_USERNAME=prod_user
APP_TOKEN_PASSWORD=prod_password
```

#### 方式2：直接使用HTTPSettings（简单项目）

```python
"""config/settings.py"""

from pydantic import Field
from df_test_framework import FrameworkSettings
from df_test_framework.infrastructure.config import HTTPSettings

class ProjectSettings(FrameworkSettings):
    """项目配置 - 使用默认HTTPSettings"""

    http_settings: HTTPSettings = Field(
        default_factory=HTTPSettings,
        description="HTTP配置"
    )
```

**环境变量配置（`.env`）**：

```bash
# 所有配置都通过环境变量提供
APP_HTTP_BASE_URL=https://api.example.com
APP_HTTP_TIMEOUT=30

APP_SIGNATURE_ENABLED=true
APP_SIGNATURE_SECRET=my_secret

APP_TOKEN_ENABLED=true
APP_TOKEN_USERNAME=admin
APP_TOKEN_PASSWORD=admin123
```

### 环境变量命名规则

**HTTPSettings 配置分层**：

```
ProjectSettings
└── http_settings: HTTPSettings
    ├── base_url          → APP_HTTP_BASE_URL
    ├── timeout           → APP_HTTP_TIMEOUT
    ├── signature: SignatureMiddlewareSettings
    │   ├── enabled       → APP_SIGNATURE_ENABLED
    │   ├── algorithm     → APP_SIGNATURE_ALGORITHM
    │   └── secret        → APP_SIGNATURE_SECRET
    └── token: BearerTokenMiddlewareSettings
        ├── enabled       → APP_TOKEN_ENABLED
        ├── username      → APP_TOKEN_USERNAME
        └── password      → APP_TOKEN_PASSWORD
```

**关键规则**：

1. **HTTP基础配置**：使用`APP_HTTP_`前缀
   - `APP_HTTP_BASE_URL`
   - `APP_HTTP_TIMEOUT`
   - `APP_HTTP_MAX_RETRIES`

2. **签名中间件**：使用`APP_SIGNATURE_`前缀（独立）
   - `APP_SIGNATURE_ENABLED`
   - `APP_SIGNATURE_ALGORITHM`
   - `APP_SIGNATURE_SECRET`

3. **Token中间件**：使用`APP_TOKEN_`前缀（独立）
   - `APP_TOKEN_ENABLED`
   - `APP_TOKEN_USERNAME`
   - `APP_TOKEN_PASSWORD`

### 使用示例

```python
from config.settings import ProjectSettings
from df_test_framework import Bootstrap

# 创建运行时
runtime = Bootstrap().with_settings(ProjectSettings).build().run()

# 获取HTTP客户端（中间件自动生效）
http_client = runtime.http_client()

# 发送请求（签名和Token中间件自动应用）
response = http_client.get("/api/users")

# 查看配置
settings = runtime.settings
print(f"Base URL: {settings.http.base_url}")
print(f"中间件数量: {len(settings.http.middlewares)}")
for middleware in settings.http.middlewares:
    print(f"  - {middleware.type} (priority={middleware.priority})")
```

**输出**：

```
Base URL: https://api.example.com
中间件数量: 2
  - signature (priority=10)
  - bearer_token (priority=20)
```

### 优势总结

使用HTTPSettings的声明式配置方式：

1. ✅ **零手动代码**：不需要手动创建HTTPConfig和中间件
2. ✅ **类型安全**：Pydantic自动验证所有配置
3. ✅ **环境变量绑定**：所有配置都可通过环境变量覆盖
4. ✅ **独立前缀**：中间件使用独立的`APP_SIGNATURE_`和`APP_TOKEN_`前缀
5. ✅ **自动启用/禁用**：通过`enabled`字段控制中间件
6. ✅ **按优先级排序**：中间件自动按priority排序

---

## 配置文件组织

### 目录结构

```
project_root/
├── .env                    # 基础配置 (可以提交)
├── .env.dev                # 开发环境 (可以提交)
├── .env.test               # 测试环境 (可以提交)
├── .env.prod               # 生产环境 (❌ 不提交)
├── .env.local              # 本地覆盖 (❌ 不提交)
├── .env.example            # 配置模板 (✅ 必须提交)
├── .env.local.example      # 本地覆盖模板
├── .gitignore
└── config/
    └── settings.py
```

### .env (基础配置)

```bash
# ========== .env ==========
# 基础配置,可以提交到git (不包含真实密码)

APP_ENV=test
APP_DEBUG=false

# API配置
APP_API__BASE_URL=http://47.94.57.99:8088/api
APP_API__TIMEOUT=30
APP_API__MAX_RETRIES=3

# 数据库配置
APP_DB__HOST=localhost
APP_DB__PORT=3306
APP_DB__NAME=test_db
APP_DB__USER=root
APP_DB__PASSWORD=default_password  # ⚠️ 生产环境必须覆盖

# Redis配置
APP_REDIS__HOST=localhost
APP_REDIS__PORT=6379
APP_REDIS__DB=0

# 测试配置
APP_TEST__PARALLEL_WORKERS=4
APP_TEST__RETRY_TIMES=2

# 业务配置（v3.5+ 使用独立的 BUSINESS_ 前缀）
# 注意：不是 APP_BUSINESS__* 而是 BUSINESS_*
BUSINESS_DEFAULT_CARD_AMOUNT=100.00
BUSINESS_TEST_USER_ID=test_user_001
```

### .env.dev (开发环境)

```bash
# ========== .env.dev ==========
# 开发环境特定配置

APP_ENV=dev
APP_DEBUG=true
APP_LOG_LEVEL=DEBUG

# API (本地开发服务器)
APP_API__BASE_URL=http://localhost:8080/api
APP_API__TIMEOUT=60
APP_API__VERIFY_SSL=false

# 数据库 (本地Docker)
APP_DB__HOST=localhost
APP_DB__PORT=3307
APP_DB__NAME=gift_card_dev
APP_DB__PASSWORD=dev_password

# 测试 (减少并发)
APP_TEST__PARALLEL_WORKERS=2
```

### .env.test (测试环境)

```bash
# ========== .env.test ==========
# 测试环境配置

APP_ENV=test
APP_DEBUG=false
APP_LOG_LEVEL=INFO

# API (测试服务器)
APP_API__BASE_URL=http://test-api.example.com

# 数据库 (测试数据库)
APP_DB__HOST=test-db.example.com
APP_DB__PASSWORD=test_password
```

### .env.local.example (本地覆盖模板)

```bash
# ========== .env.local.example ==========
# 本地个人配置覆盖模板
# 复制为 .env.local 并修改

# 示例: 覆盖API地址
# APP_API__BASE_URL=http://localhost:3000/api

# 示例: 覆盖数据库
# APP_DB__HOST=localhost
# APP_DB__PASSWORD=my_local_password

# 示例: 开启调试
# APP_DEBUG=true
# APP_LOG_LEVEL=DEBUG
```

### .gitignore

```gitignore
# 环境配置
.env.local
.env.*.local
.env.prod            # 生产环境配置不提交

# 以下文件可以提交:
# .env (基础配置)
# .env.dev
# .env.test
# .env.example
# .env.local.example
```

---

## 使用方式

### 1. 基本使用

```python
from config.settings import settings

# 访问配置
print(settings.env)                    # test
print(settings.api.base_url)           # http://...
print(settings.db.host)                # localhost
print(settings.test.parallel_workers)  # 4

# 获取密钥
db_password = settings.db.password.get_secret_value()

# 使用计算属性
if settings.is_production:
    # 生产环境逻辑
    pass
```

### 2. 在conftest.py中使用

```python
# tests/conftest.py
import pytest
from config.settings import settings
from df_test_framework import HttpClient, Database

@pytest.fixture(scope="session")
def http_client() -> HttpClient:
    """HTTP客户端fixture"""
    client = HttpClient(
        base_url=settings.api.base_url,
        timeout=settings.api.timeout,
    )
    yield client
    client.close()

@pytest.fixture(scope="session")
def db() -> Database:
    """数据库连接fixture"""
    database = Database(settings.db.connection_string)
    yield database
    database.close()
```

### 3. 测试时使用工厂函数

```python
# tests/test_user.py
import pytest
from config.settings import create_settings

@pytest.fixture
def test_settings():
    """测试配置fixture"""
    return create_settings(
        env="test",
        api__base_url="http://mock-api.com",
        db__host="test-db",
        db__port=3307,
    )

def test_with_custom_config(test_settings):
    assert test_settings.api.base_url == "http://mock-api.com"
    assert test_settings.db.port == 3307
```

### 4. 环境切换

```bash
# 方式1: ENV环境变量
ENV=dev uv run pytest          # 加载 .env.dev
ENV=test uv run pytest         # 加载 .env.test
ENV=prod uv run pytest         # 加载 .env.prod

# 方式2: 直接覆盖配置
APP_API__BASE_URL=http://other-api.com uv run pytest

# 方式3: 组合使用
ENV=test APP_LOG_LEVEL=DEBUG uv run pytest
```

### 5. CI/CD中使用

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Install uv
        run: pip install uv

      - name: Run tests
        env:
          ENV: test
          APP_API__BASE_URL: ${{ secrets.TEST_API_URL }}
          APP_DB__PASSWORD: ${{ secrets.TEST_DB_PASSWORD }}
        run: |
          uv run pytest
```

---

## 最佳实践

### ✅ DO - 推荐做法

#### 1. 使用类型注解和验证

```python
# ✅ 好
class Settings(BaseSettings):
    port: int = Field(ge=1, le=65535)  # 带验证
    env: Literal["dev", "test", "prod"]  # 枚举限制
    timeout: int = Field(default=30, ge=1)  # 合理默认值
```

#### 2. 使用SecretStr保护密钥

```python
# ✅ 好
password: SecretStr = Field(default=SecretStr(""))

# 使用时显式获取
pwd = settings.password.get_secret_value()
```

#### 3. 使用嵌套配置组织复杂配置

```python
# ✅ 好 - 清晰的层级结构
class Settings(BaseSettings):
    api: APIConfig = Field(default_factory=APIConfig)
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)

# 访问: settings.db.host
```

#### 4. 使用@property计算衍生配置

```python
# ✅ 好
@property
def db_connection_string(self) -> str:
    pwd = self.password.get_secret_value()
    return f"mysql+pymysql://{self.user}:{pwd}@{self.host}:{self.port}/{self.name}"
```

#### 5. 生产环境安全检查

```python
# ✅ 好
def model_post_init(self, __context) -> None:
    if self.is_production:
        if self.db.password.get_secret_value() == "default_password":
            raise ValueError("生产环境禁止使用默认密码")
```

### ❌ DON'T - 避免的做法

#### 1. 硬编码敏感信息

```python
# ❌ 坏
api_key: str = "sk_live_xxxxxxxx"  # 不要硬编码密钥

# ✅ 好
api_key: SecretStr = Field(default=SecretStr(""))  # 从环境变量读取
```

#### 2. 缺少类型注解

```python
# ❌ 坏
timeout = 30  # 没有类型提示

# ✅ 好
timeout: int = 30  # 清晰的类型
```

#### 3. 配置名不清晰

```python
# ❌ 坏
url: str = "..."  # 什么URL?

# ✅ 好
api_base_url: str = "..."  # 清晰明确
```

#### 4. 没有验证逻辑

```python
# ❌ 坏
port: int = 8080  # 可能被设置为负数或超大值

# ✅ 好
port: int = Field(default=8080, ge=1, le=65535)
```

---

## 常见问题

### Q1: 为什么不用YAML配置?

**A**: YAML适合复杂嵌套配置,但缺点明显:
- ❌ 无类型检查
- ❌ 需要手动解析
- ❌ 没有IDE支持
- ❌ 不支持环境变量覆盖

**pydantic-settings的优势**:
- ✅ 类型安全
- ✅ 自动验证
- ✅ IDE支持
- ✅ 环境变量优先级

### Q2: .env文件应该提交到git吗?

**A**: 分情况:
- ✅ **提交**: `.env` (基础配置,不含真实密码), `.env.dev`, `.env.test`, `.env.example`
- ❌ **不提交**: `.env.local` (个人配置), `.env.prod` (生产密钥)

### Q3: 如何在测试中覆盖配置?

**A**: 使用 `create_settings()` 工厂函数:

```python
@pytest.fixture
def test_settings():
    return create_settings(
        env="test",
        api__base_url="http://mock-api.com",
    )
```

### Q4: ENV环境变量不生效怎么办?

**A**: 检查加载顺序:

```python
model_config = SettingsConfigDict(
    env_file=(
        ".env",
        f".env.{os.getenv('ENV', 'test')}",  # ← 确保这里读取ENV
    )
)
```

### Q5: 如何调试配置加载?

**A**: 添加配置摘要方法:

```python
class Settings(BaseSettings):
    def get_config_summary(self) -> dict:
        return {
            "env": self.env,
            "api_base_url": self.api.base_url,
            "db_host": self.db.host,
            # 不要输出密钥!
        }

# 使用
print(settings.get_config_summary())
```

### Q6: 支持热重载配置吗?

**A**: 支持,使用 `force_reload`:

```python
settings = get_settings(force_reload=True)
```

### Q7: 如何在Docker中使用?

**A**: 通过环境变量或挂载配置:

```dockerfile
# 方式1: 环境变量
ENV APP_API__BASE_URL=http://api.prod.com
ENV APP_DB__PASSWORD=prod_password

# 方式2: 挂载配置文件
COPY .env.prod /app/.env.prod
ENV ENV=prod
```

### Q8: pydantic v1 vs v2有什么区别?

**A**: pydantic-settings 2.0+ 需要 pydantic v2:

| 特性 | v1 | v2 |
|-----|----|----|
| 性能 | 慢 | 快(5-50倍) |
| 配置 | Config类 | model_config字典 |
| 验证 | validator | field_validator |
| 安装 | pydantic | pydantic>=2.0 |

**升级命令**:
```bash
uv add "pydantic>=2.0.0"
uv add "pydantic-settings>=2.0.0"
```

---

## 总结

### 核心要点

1. ✅ **使用pydantic-settings 2.0+** - 类型安全、自动验证
2. ✅ **嵌套配置** - 使用 `__` 分隔符组织复杂配置
3. ✅ **环境变量优先** - 生产环境通过环境变量覆盖
4. ✅ **密钥保护** - 使用 SecretStr 保护敏感信息
5. ✅ **多环境支持** - .env.dev、.env.test、.env.prod
6. ✅ **启动时验证** - 配置错误立即发现,不等到运行时

### 参考资源

- [Pydantic Settings官方文档](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [gift-card-test完整示例](../../../gift-card-test/config/settings.py)
- [12-Factor App配置管理](https://12factor.net/config)

---

**文档版本**: v3.5
**更新时间**: 2025-11
**适用框架**: df-test-framework v3.5+
**主要更新**:
- ✅ 添加HTTP配置和中间件（v3.5+ 声明式配置）章节
- ✅ 展示HTTPSettings、SignatureMiddlewareSettings和BearerTokenMiddlewareSettings用法
- ✅ 完全声明式配置，零手动代码
