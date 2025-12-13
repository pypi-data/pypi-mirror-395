# 拦截器命名标准规范

> **目标**: 制定框架级别的拦截器命名标准，去除业务耦合
> **原则**: 通用、标准、易理解
> **创建时间**: 2025-11-06

---

## 🎯 命名原则

### 原则1: 框架级别 vs 业务级别

**框架级别** - 通用的技术能力
- ✅ 签名（Signature）
- ✅ 认证（Authentication/Auth）
- ✅ 日志（Logging）
- ✅ 重试（Retry）
- ✅ 限流（RateLimit）

**业务级别** - 特定业务场景
- ❌ AdminAuth（特定于Admin系统）
- ❌ MasterSign（特定于Master系统）
- ❌ H5Token（特定于H5系统）

### 原则2: 使用标准的HTTP/REST术语

参考业界标准：
- **OAuth 2.0**: Bearer Token, Client Credentials
- **HTTP规范**: Authorization, Authentication
- **Spring Framework**: Interceptor, Filter
- **Express.js**: Middleware

---

## 📋 重新命名方案

### 1. 认证拦截器（Authentication）

#### 当前命名（有业务耦合）
```
❌ AdminAuthInterceptor
❌ AdminAuthInterceptorConfig
```

#### 标准命名方案

**方案A: BearerTokenInterceptor**（推荐）
```python
class BearerTokenInterceptor(BaseInterceptor):
    """Bearer Token认证拦截器

    自动获取Token并添加到请求头
    支持多种Token获取方式:
    - login: 通过登录接口获取
    - static: 使用静态Token
    - custom: 自定义获取方式
    """

    def __init__(
        self,
        # Token获取方式
        token_source: Literal["login", "static", "custom"] = "login",

        # 登录方式配置
        login_url: Optional[str] = None,
        login_credentials: Optional[Dict[str, str]] = None,  # {"username": "...", "password": "..."}

        # 静态Token配置
        static_token: Optional[str] = None,

        # 自定义Token获取函数
        custom_token_getter: Optional[Callable[[], str]] = None,

        # Token提取配置
        token_field_path: str = "data.token",  # 支持嵌套: "data.access_token"

        # Header配置
        header_name: str = "Authorization",
        token_prefix: str = "Bearer",

        # 缓存配置
        cache_enabled: bool = True,

        # 通用配置
        priority: int = 20,
        name: Optional[str] = None,
    ):
        ...
```

**使用示例**:
```python
# 场景1: 登录获取Token（原AdminAuth场景）
interceptor = BearerTokenInterceptor(
    token_source="login",
    login_url="/admin/auth/login",
    login_credentials={
        "username": "admin",
        "password": "admin123",
    },
    token_field_path="data.token",
)

# 场景2: 静态Token
interceptor = BearerTokenInterceptor(
    token_source="static",
    static_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
)

# 场景3: 自定义获取方式
def get_token_from_cache():
    return redis_client.get("api_token")

interceptor = BearerTokenInterceptor(
    token_source="custom",
    custom_token_getter=get_token_from_cache,
)
```

**配置类命名**:
```python
class BearerTokenInterceptorConfig(InterceptorConfig):
    type: Literal["bearer_token"] = "bearer_token"

    token_source: Literal["login", "static", "custom"] = "login"
    login_url: Optional[str] = None
    login_credentials: Optional[Dict[str, str]] = None
    static_token: Optional[str] = None
    token_field_path: str = "data.token"
    header_name: str = "Authorization"
    token_prefix: str = "Bearer"
    cache_enabled: bool = True
    priority: int = 20
```

---

**方案B: AuthTokenInterceptor**（备选）
```python
class AuthTokenInterceptor(BaseInterceptor):
    """认证Token拦截器（通用）"""
    ...
```

---

**方案C: TokenAuthenticationInterceptor**（更明确）
```python
class TokenAuthenticationInterceptor(BaseInterceptor):
    """Token认证拦截器（完整命名）"""
    ...
```

---

### 2. 签名拦截器（Signature）

#### 当前命名（已经很标准）
```
✅ SignatureInterceptor
✅ SignatureInterceptorConfig
```

**保持不变**，已经是标准命名。

---

### 3. 日志拦截器（Logging）

#### 当前命名
```
❌ LogInterceptor  # 太简短
```

#### 标准命名
```python
✅ LoggingInterceptor
✅ LoggingInterceptorConfig
```

**理由**:
- 与Python标准库的`logging`模块对齐
- 更清晰（Log可能被理解为"日志对象"）

---

### 4. 其他常见拦截器命名

#### 4.1 重试拦截器
```python
✅ RetryInterceptor
✅ RetryInterceptorConfig
```

#### 4.2 限流拦截器
```python
✅ RateLimitInterceptor
✅ RateLimitInterceptorConfig
```

#### 4.3 超时拦截器
```python
✅ TimeoutInterceptor
✅ TimeoutInterceptorConfig
```

#### 4.4 缓存拦截器
```python
✅ CacheInterceptor
✅ CacheInterceptorConfig
```

#### 4.5 压缩拦截器
```python
✅ CompressionInterceptor
✅ CompressionInterceptorConfig
```

#### 4.6 基础认证拦截器
```python
✅ BasicAuthInterceptor
✅ BasicAuthInterceptorConfig
```

#### 4.7 API Key拦截器
```python
✅ APIKeyInterceptor
✅ APIKeyInterceptorConfig
```

---

## 📊 完整的拦截器命名对照表

| 功能 | ❌ 旧命名 | ✅ 新命名 | 配置type |
|------|---------|----------|----------|
| 签名 | SignatureInterceptor | SignatureInterceptor | `signature` |
| Bearer Token认证 | AdminAuthInterceptor | **BearerTokenInterceptor** | `bearer_token` |
| 日志 | LogInterceptor | **LoggingInterceptor** | `logging` |
| 重试 | - | RetryInterceptor | `retry` |
| 限流 | - | RateLimitInterceptor | `rate_limit` |
| 超时 | - | TimeoutInterceptor | `timeout` |
| 缓存 | - | CacheInterceptor | `cache` |
| 压缩 | - | CompressionInterceptor | `compression` |
| Basic认证 | - | BasicAuthInterceptor | `basic_auth` |
| API Key | - | APIKeyInterceptor | `api_key` |

---

## 🎨 配置示例（重命名后）

### settings.py

```python
from df_test_framework import (
    FrameworkSettings,
    HTTPConfig,
    SignatureInterceptorConfig,
    BearerTokenInterceptorConfig,  # 🆕 重命名
    LoggingInterceptorConfig,      # 🆕 重命名
)

class GiftCardSettings(FrameworkSettings):
    http: HTTPConfig = Field(
        default_factory=lambda: HTTPConfig(
            base_url=os.getenv("API_BASE_URL"),
            interceptors=[
                # 签名拦截器
                SignatureInterceptorConfig(
                    type="signature",
                    priority=10,
                    algorithm="md5",
                    secret=os.getenv("BUSINESS_APP_SECRET"),
                ),

                # Bearer Token认证拦截器（原AdminAuth）
                BearerTokenInterceptorConfig(
                    type="bearer_token",
                    priority=20,
                    token_source="login",
                    login_url="/admin/auth/login",
                    login_credentials={
                        "username": os.getenv("ADMIN_USERNAME"),
                        "password": os.getenv("ADMIN_PASSWORD"),
                    },
                    token_field_path="data.token",
                ),

                # 日志拦截器
                LoggingInterceptorConfig(
                    type="logging",
                    priority=100,
                    level="DEBUG",
                ),
            ],
        )
    )
```

---

### YAML配置

```yaml
http:
  base_url: http://api.example.com
  interceptors:
    # 签名拦截器
    - type: signature
      priority: 10
      algorithm: md5
      secret: ${BUSINESS_APP_SECRET}

    # Bearer Token认证拦截器
    - type: bearer_token
      priority: 20
      token_source: login
      login_url: /admin/auth/login
      login_credentials:
        username: ${ADMIN_USERNAME}
        password: ${ADMIN_PASSWORD}
      token_field_path: data.token

    # 日志拦截器
    - type: logging
      priority: 100
      level: DEBUG
```

---

## 🔑 业务层的扩展方式

### 方式1: 继承框架拦截器（推荐）

```python
# gift-card-test项目中
from df_test_framework import BearerTokenInterceptor

class AdminAuthInterceptor(BearerTokenInterceptor):
    """Admin系统认证拦截器（业务封装）"""

    def __init__(self, settings):
        super().__init__(
            token_source="login",
            login_url="/admin/auth/login",
            login_credentials={
                "username": settings.business.admin_username,
                "password": settings.business.admin_password,
            },
            token_field_path="data.token",
            name="AdminAuthInterceptor",
        )
```

**优势**:
- ✅ 框架通用
- ✅ 业务封装
- ✅ 易于维护

---

### 方式2: 工厂方法

```python
# gift-card-test项目中
from df_test_framework import BearerTokenInterceptor

def create_admin_auth_interceptor(settings) -> BearerTokenInterceptor:
    """创建Admin认证拦截器（工厂方法）"""
    return BearerTokenInterceptor(
        token_source="login",
        login_url="/admin/auth/login",
        login_credentials={
            "username": settings.business.admin_username,
            "password": settings.business.admin_password,
        },
        token_field_path="data.token",
    )

# 使用
@pytest.fixture(scope="session")
def admin_auth_interceptor(settings):
    return create_admin_auth_interceptor(settings)
```

---

### 方式3: 配置别名（最简单）

```python
# gift-card-test项目的settings.py
class GiftCardSettings(FrameworkSettings):

    @property
    def admin_auth_config(self) -> BearerTokenInterceptorConfig:
        """Admin认证配置（业务别名）"""
        return BearerTokenInterceptorConfig(
            type="bearer_token",
            token_source="login",
            login_url="/admin/auth/login",
            login_credentials={
                "username": self.business.admin_username,
                "password": self.business.admin_password,
            },
        )

    http: HTTPConfig = Field(
        default_factory=lambda: HTTPConfig(
            interceptors=[
                self.admin_auth_config,  # 使用业务别名
            ]
        )
    )
```

---

## 📝 命名标准总结

### 拦截器类命名规则

```
<功能><类型>Interceptor

示例:
- SignatureInterceptor（签名拦截器）
- BearerTokenInterceptor（Bearer Token拦截器）
- BasicAuthInterceptor（Basic认证拦截器）
- LoggingInterceptor（日志拦截器）
- RetryInterceptor（重试拦截器）
```

### 配置类命名规则

```
<功能><类型>InterceptorConfig

示例:
- SignatureInterceptorConfig
- BearerTokenInterceptorConfig
- LoggingInterceptorConfig
```

### 配置type字段命名规则

```
<功能>_<类型> (小写+下划线)

示例:
- signature
- bearer_token
- basic_auth
- logging
- retry
- rate_limit
```

---

## ✅ 重命名清单

### 需要重命名的类

1. **AdminAuthInterceptor** → **BearerTokenInterceptor**
2. **AdminAuthInterceptorConfig** → **BearerTokenInterceptorConfig**
3. **LogInterceptor** → **LoggingInterceptor**
4. **LogInterceptorConfig** → **LoggingInterceptorConfig**

### 需要更新的type字段

1. `"admin_auth"` → `"bearer_token"`
2. `"log"` → `"logging"`

### 需要更新的文件

1. `src/df_test_framework/clients/http/auth/interceptors/admin_auth.py` → `bearer_token.py`
2. `src/df_test_framework/clients/http/auth/interceptors/log.py` → `logging.py`
3. `src/df_test_framework/infrastructure/config/schema.py`
4. `src/df_test_framework/__init__.py`
5. `docs/REFACTORING_IMPLEMENTATION_PLAN.md`
6. `docs/CONFIG_AND_INTERCEPTOR_INTEGRATION.md`
7. `docs/INTERCEPTOR_IDEAL_DESIGN.md`

---

## 🎯 重命名的好处

1. **框架通用性** ✅
   - 不绑定特定业务（Admin/Master/H5）
   - 适用于任何使用Bearer Token的场景

2. **标准化** ✅
   - 符合HTTP/OAuth标准术语
   - 易于理解和维护

3. **扩展性** ✅
   - 业务层可以继承或封装
   - 不影响框架核心

4. **一致性** ✅
   - 所有拦截器命名风格统一
   - type字段命名规范统一

---

**建议**: 立即采用新的命名标准，在实施时直接使用标准命名。
