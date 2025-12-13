# HTTP拦截器配置最佳实践

> **版本**: v3.4.0
> **更新日期**: 2025-11-06
> **状态**: 最终设计

---

## 🎯 核心问题

**拦截器配置应该放在哪里？**

这个问题困扰了很多框架设计者。本文档总结了v3.4.0的最终设计决策和最佳实践。

---

## 📚 设计演进历程

### v3.4.0 初版（已废弃）
```python
# ❌ HTTPConfigBuilder - 违背Pydantic理念
data['http'] = (
    HTTPConfigBuilder()
    .add_signature_auth(...)
    .add_bearer_token(...)
    .build()
)
```

**问题**:
- 违背Pydantic声明式配置理念
- 无法序列化
- 配置在`__init__`中，不在字段级别

### v3.4.0 最终版（推荐）
```python
# ✅ 纯Pydantic + 业务配置分离 + 组合模式
class AuthConfig(BaseModel):
    signature_secret: str
    admin_username: str

class BusinessConfig(BaseSettings):
    auth: AuthConfig

class GiftCardSettings(FrameworkSettings):
    business: BusinessConfig

    @model_validator(mode='after')
    def setup_http_interceptors(self):
        self.http.interceptors = [
            SignatureInterceptorConfig(secret=self.business.auth.signature_secret),
            BearerTokenInterceptorConfig(username=self.business.auth.admin_username),
        ]
        return self
```

**优势**:
- ✅ 完全符合Pydantic理念
- ✅ 完全可序列化
- ✅ 业务配置分离
- ✅ 符合现代测试框架模式

---

## 🏗️ 推荐架构：三层配置模式

```
┌──────────────────────────────────────────┐
│  Framework层 (df_test_framework)         │
│  ┌────────────────────────────────────┐  │
│  │ HTTPConfig                         │  │
│  │ - base_url: str                    │  │
│  │ - timeout: int                     │  │
│  │ - max_retries: int                 │  │
│  │ - interceptors: List[InterceptorConfig]│  │
│  └────────────────────────────────────┘  │
│  只关心: "怎么发HTTP请求"                 │
└──────────────────────────────────────────┘
                  ↓
┌──────────────────────────────────────────┐
│  Business层 (项目业务配置)                │
│  ┌────────────────────────────────────┐  │
│  │ AuthConfig                         │  │
│  │ - signature_secret: str            │  │
│  │ - signature_algorithm: str         │  │
│  │ - admin_username: str              │  │
│  │ - admin_password: str              │  │
│  └────────────────────────────────────┘  │
│  ┌────────────────────────────────────┐  │
│  │ BusinessConfig                     │  │
│  │ - auth: AuthConfig                 │  │
│  │ - test_data: ...                   │  │
│  └────────────────────────────────────┘  │
│  只关心: "认证数据是什么"                 │
└──────────────────────────────────────────┘
                  ↓
┌──────────────────────────────────────────┐
│  Integration层 (项目设置)                 │
│  ┌────────────────────────────────────┐  │
│  │ ProjectSettings(FrameworkSettings) │  │
│  │   business: BusinessConfig         │  │
│  │                                    │  │
│  │   @model_validator(mode='after')   │  │
│  │   def setup_http_interceptors():   │  │
│  │     # 将business.auth转换为        │  │
│  │     # http.interceptors             │  │
│  └────────────────────────────────────┘  │
│  负责: "组合框架和业务"                   │
└──────────────────────────────────────────┘
```

---

## 💡 最佳实践

### 1. 创建独立的AuthConfig

```python
from pydantic import BaseModel, Field

class AuthConfig(BaseModel):
    """认证配置 - 业务级别

    ✅ 关注点分离: 认证配置独立出来
    ✅ 易于复用: 可以在多个项目间共享
    ✅ 类型安全: Pydantic自动验证
    """

    # 签名认证
    signature_secret: str = Field(description="API签名密钥")
    signature_algorithm: str = Field(default="md5", description="签名算法")
    signature_header: str = Field(default="X-Sign", description="签名Header名称")

    # Bearer Token认证
    admin_username: str = Field(description="管理员用户名")
    admin_password: str = Field(description="管理员密码")
    admin_login_url: str = Field(default="/admin/auth/login", description="登录接口")
    admin_token_path: str = Field(default="data.token", description="Token字段路径")
```

### 2. 在BusinessConfig中组合AuthConfig

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class BusinessConfig(BaseSettings):
    """业务配置

    ✅ 配置分层: auth独立，test_data独立
    ✅ 环境变量: BUSINESS_AUTH__SIGNATURE_SECRET
    """

    # 认证配置
    auth: AuthConfig = Field(default_factory=AuthConfig, description="认证配置")

    # 测试数据
    test_user_id: str = Field(default="test_user_001", description="测试用户ID")
    test_template_id: str = Field(default="TMPL_001", description="测试模板ID")

    model_config = SettingsConfigDict(
        env_prefix="BUSINESS_",
        env_file=".env",
        extra="ignore",
    )
```

### 3. 在ProjectSettings中组合拦截器

```python
from df_test_framework import FrameworkSettings
from df_test_framework.infrastructure.config import (
    SignatureInterceptorConfig,
    BearerTokenInterceptorConfig,
)
from pydantic import Field, model_validator

class ProjectSettings(FrameworkSettings):
    """项目配置 - 集成层

    ✅ 组合模式: 将business.auth转换为http.interceptors
    ✅ 职责单一: 只负责"翻译"两者
    ✅ 测试友好: 可以Mock BusinessConfig
    """

    business: BusinessConfig = Field(default_factory=BusinessConfig)

    @model_validator(mode='after')
    def setup_http_interceptors(self) -> 'ProjectSettings':
        """组合框架和业务配置

        为什么在这里:
        1. 框架层不知道业务规则
        2. 业务层不依赖框架
        3. 集成层负责"翻译"

        类似模式:
        - Pytest: conftest.py组合fixtures
        - Spring: @BeforeEach组装配置
        - Playwright: setup.ts组合config
        """
        if not self.http.interceptors:
            auth = self.business.auth

            self.http.interceptors = [
                # 签名拦截器
                SignatureInterceptorConfig(
                    type="signature",
                    priority=10,
                    algorithm=auth.signature_algorithm,
                    secret=auth.signature_secret,
                    header_name=auth.signature_header,
                    include_paths=["/api/**"],
                    exclude_paths=["/health"],
                ),
                # Bearer Token拦截器
                BearerTokenInterceptorConfig(
                    type="bearer_token",
                    priority=20,
                    token_source="login",
                    login_url=auth.admin_login_url,
                    login_credentials={
                        "username": auth.admin_username,
                        "password": auth.admin_password,
                    },
                    token_field_path=auth.admin_token_path,
                    include_paths=["/admin/**"],
                ),
            ]

        return self
```

---

## 🌟 设计原则

### 1. 关注点分离 (Separation of Concerns)

| 层次 | 职责 | 不负责 |
|------|------|--------|
| Framework (HTTPConfig) | HTTP传输配置 | ❌ 不知道业务认证规则 |
| Business (AuthConfig) | 认证数据 | ❌ 不知道如何创建拦截器 |
| Integration (ProjectSettings) | 组合两者 | ❌ 不定义具体规则 |

### 2. 组合优于继承 (Composition over Inheritance)

```python
# ✅ 推荐: 组合
class ProjectSettings(FrameworkSettings):
    business: BusinessConfig  # 组合

    @model_validator(mode='after')
    def setup_http_interceptors(self):
        # 将business组合到http
        self.http.interceptors = create_from(self.business.auth)

# ❌ 不推荐: 继承
class ProjectHTTPConfig(HTTPConfig):
    def __init__(self, business: BusinessConfig):
        super().__init__(
            interceptors=create_from(business.auth)
        )
```

### 3. 依赖倒置 (Dependency Inversion)

```python
# ✅ 框架不依赖业务细节
class HTTPConfig:
    interceptors: List[InterceptorConfig]  # 抽象接口

# ✅ 业务不依赖框架实现
class AuthConfig:
    signature_secret: str  # 纯数据

# ✅ 集成层依赖抽象
class ProjectSettings:
    def setup_http_interceptors(self):
        # 依赖InterceptorConfig接口，不依赖具体实现
        self.http.interceptors = [SignatureInterceptorConfig(...)]
```

---

## 📊 对比业界框架

### Pytest
```python
# pytest.ini - 框架配置
[pytest]
addopts = --strict-markers

# conftest.py - 业务逻辑组合
@pytest.fixture
def api_client(config):
    return APIClient(
        base_url=config.api_url,
        auth=BearerAuth(token=config.api_token)  # ← 组合
    )
```

### Spring Boot Test
```java
@SpringBootTest  // 框架配置
class ApiTest {
    @Value("${api.secret}")  // 业务配置
    private String apiSecret;

    @BeforeEach  // 组合
    void setup() {
        webClient.mutate()
            .filter(new SignatureFilter(apiSecret))
            .build();
    }
}
```

### Playwright
```typescript
// playwright.config.ts - 框架配置
export default defineConfig({
  use: { baseURL: process.env.BASE_URL },
});

// setup.ts - 业务逻辑组合
test.beforeAll(async ({ request }) => {
  await request.post('/api/login', {
    data: { username: process.env.USER }  // ← 组合
  });
});
```

**共同点**: 框架管传输，业务管数据，在setup/fixture中组合

---

## ✅ 优势总结

### 1. 复用性 ⭐⭐⭐⭐⭐
```python
# AuthConfig可以跨项目复用
class ProjectA(FrameworkSettings):
    business: BusinessConfig  # 复用

class ProjectB(FrameworkSettings):
    business: BusinessConfig  # 复用
```

### 2. 易用性 ⭐⭐⭐⭐⭐
```bash
# 环境变量清晰直观
BUSINESS_AUTH__SIGNATURE_SECRET=xxx
BUSINESS_AUTH__ADMIN_USERNAME=admin
APP_HTTP__BASE_URL=https://...
```

### 3. 测试友好 ⭐⭐⭐⭐⭐
```python
# 容易Mock业务配置
settings = ProjectSettings(
    business=BusinessConfig(
        auth=AuthConfig(signature_secret="test_secret")
    )
)
```

### 4. 直观性 ⭐⭐⭐⭐⭐
```yaml
business:
  auth:  # 一看就懂
    signature_secret: xxx
    admin_username: admin
```

### 5. 可维护性 ⭐⭐⭐⭐⭐
- 认证逻辑变更：只改AuthConfig
- HTTP传输变更：只改HTTPConfig
- 组合策略变更：只改setup_http_interceptors

---

## 🚫 反模式（避免）

### ❌ 反模式1: 拦截器配置在HTTPConfig中

```python
# ❌ 不推荐
http: HTTPConfig = Field(
    default_factory=lambda: HTTPConfig(
        base_url="...",
        interceptors=[
            SignatureInterceptorConfig(
                secret=os.getenv("BUSINESS_SECRET")  # 业务配置泄漏到框架层
            )
        ]
    )
)
```

**问题**:
- 框架层知道了业务细节
- 无法复用BusinessConfig
- 环境变量命名混乱

### ❌ 反模式2: Builder模式

```python
# ❌ 不推荐
data['http'] = (
    HTTPConfigBuilder()
    .add_signature_auth(...)
    .build()
)
```

**问题**:
- 违背Pydantic理念
- 无法序列化
- 配置在__init__中

### ❌ 反模式3: 独立的InterceptorsConfig

```python
# ❌ 不推荐
class InterceptorsConfig(BaseModel):
    signature: SignatureInterceptorConfig
    bearer_token: BearerTokenInterceptorConfig
```

**问题**:
- 拦截器配置和认证数据重复
- 多一层抽象，复杂度增加
- 环境变量命名更复杂

---

## 📖 示例项目

完整示例请参考: `gift-card-test/src/gift_card_test/config/settings.py`

```python
# 完整示例
class AuthConfig(BaseModel):
    signature_secret: str = "default_secret"
    admin_username: str = "admin"

class BusinessConfig(BaseSettings):
    auth: AuthConfig = Field(default_factory=AuthConfig)
    model_config = SettingsConfigDict(env_prefix="BUSINESS_")

class GiftCardSettings(FrameworkSettings):
    business: BusinessConfig = Field(default_factory=BusinessConfig)

    @model_validator(mode='after')
    def setup_http_interceptors(self):
        if not self.http.interceptors:
            auth = self.business.auth
            self.http.interceptors = [
                SignatureInterceptorConfig(secret=auth.signature_secret),
                BearerTokenInterceptorConfig(username=auth.admin_username),
            ]
        return self
```

---

## 🎓 总结

**拦截器配置应该放在哪？**

✅ **最佳答案**:
1. 认证**数据**放在`BusinessConfig.auth`
2. 在`ProjectSettings.setup_http_interceptors()`中**组合**
3. 转换为`http.interceptors`

**核心理念**:
- 框架管传输，业务管数据，集成层组合
- 符合Pydantic理念
- 符合现代测试框架模式
- 符合SOLID设计原则

---

**参考文档**:
- `docs/migration/v3.3-to-v3.4.md` - 迁移指南
- `docs/architecture/V3_ARCHITECTURE.md` - 架构设计
- `gift-card-test/src/gift_card_test/config/settings.py` - 完整示例
