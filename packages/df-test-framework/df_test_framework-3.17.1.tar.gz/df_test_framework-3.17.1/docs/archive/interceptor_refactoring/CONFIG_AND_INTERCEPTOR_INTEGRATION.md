# 配置系统与拦截器架构集成设计

> **目标**: 梳理配置系统如何加载和管理拦截器
> **版本**: v4.0.0 (重构版)
> **创建时间**: 2025-11-06

---

## 🎯 核心问题

**配置系统需要解决的问题**:
1. 如何从`settings.py`/`settings.yaml`加载拦截器配置？
2. 如何将配置转换为拦截器实例？
3. 如何传递给`HttpClient`？
4. 如何支持环境变量替换？
5. 如何支持多环境配置（dev/test/prod）？

---

## 🏗️ 配置系统架构

### 1. 配置层级

```
settings.yaml (可选)
    ↓
settings.py (Python配置)
    ↓
HTTPConfig (Pydantic模型)
    ↓
InterceptorConfig (拦截器配置)
    ↓
InterceptorFactory (工厂创建)
    ↓
Interceptor实例
    ↓
HttpClient
```

---

### 2. 配置对象设计

#### 2.1 InterceptorConfig (基类)

```python
from pydantic import BaseModel, Field
from typing import Literal, Optional

class InterceptorConfig(BaseModel):
    """拦截器配置基类"""

    type: str = Field(..., description="拦截器类型")
    enabled: bool = Field(default=True, description="是否启用")
    priority: int = Field(default=100, description="优先级（数字越小越先执行）")
    name: Optional[str] = Field(default=None, description="拦截器名称（用于调试）")

    class Config:
        extra = "allow"  # 允许子类添加额外字段
```

---

#### 2.2 SignatureInterceptorConfig

```python
class SignatureInterceptorConfig(InterceptorConfig):
    """签名拦截器配置"""

    type: Literal["signature"] = "signature"

    # 签名相关配置
    algorithm: str = Field(..., description="签名算法: md5, sha256, hmac-sha256")
    secret: str = Field(..., description="签名密钥")
    header_name: str = Field(default="X-Sign", description="签名Header名称")

    # 签名参数来源
    include_query: bool = Field(default=True, description="是否包含URL参数")
    include_body: bool = Field(default=True, description="是否包含请求体")
    include_form: bool = Field(default=False, description="是否包含表单数据")

    # 优先级建议
    priority: int = Field(default=10, description="建议priority=10")

    # 示例
    class Config:
        json_schema_extra = {
            "example": {
                "type": "signature",
                "enabled": True,
                "priority": 10,
                "algorithm": "md5",
                "secret": "${BUSINESS_APP_SECRET}",
                "header_name": "X-Sign"
            }
        }
```

---

#### 2.3 AdminAuthInterceptorConfig

```python
class AdminAuthInterceptorConfig(InterceptorConfig):
    """Admin认证拦截器配置"""

    type: Literal["admin_auth"] = "admin_auth"

    # 登录配置
    login_url: str = Field(..., description="登录接口路径")
    username: str = Field(..., description="登录用户名")
    password: str = Field(..., description="登录密码")

    # Token配置
    token_field: str = Field(default="data.token", description="Token在响应中的字段路径")
    header_name: str = Field(default="Authorization", description="Token Header名称")
    token_prefix: str = Field(default="Bearer", description="Token前缀")

    # 缓存配置
    cache_enabled: bool = Field(default=True, description="是否启用Token缓存")

    # 优先级建议
    priority: int = Field(default=20, description="建议priority=20（在签名之后）")

    class Config:
        json_schema_extra = {
            "example": {
                "type": "admin_auth",
                "enabled": True,
                "priority": 20,
                "login_url": "/admin/auth/login",
                "username": "${ADMIN_USERNAME}",
                "password": "${ADMIN_PASSWORD}",
                "token_field": "data.token"
            }
        }
```

---

#### 2.4 LogInterceptorConfig

```python
class LogInterceptorConfig(InterceptorConfig):
    """日志拦截器配置"""

    type: Literal["log"] = "log"

    level: str = Field(default="INFO", description="日志级别")
    log_request_body: bool = Field(default=True, description="是否记录请求体")
    log_response_body: bool = Field(default=True, description="是否记录响应体")
    max_body_length: int = Field(default=500, description="最大记录长度")

    priority: int = Field(default=100, description="建议priority=100（较低优先级）")
```

---

#### 2.5 CustomInterceptorConfig

```python
class CustomInterceptorConfig(InterceptorConfig):
    """自定义拦截器配置"""

    type: Literal["custom"] = "custom"

    class_path: str = Field(..., description="拦截器类的完整路径")
    params: Dict[str, Any] = Field(default_factory=dict, description="传递给拦截器的参数")

    class Config:
        json_schema_extra = {
            "example": {
                "type": "custom",
                "class_path": "my_project.interceptors.MyInterceptor",
                "params": {
                    "foo": "bar"
                }
            }
        }
```

---

### 3. HTTPConfig设计

```python
from typing import List, Union

# 拦截器配置联合类型
InterceptorConfigUnion = Union[
    SignatureInterceptorConfig,
    AdminAuthInterceptorConfig,
    LogInterceptorConfig,
    CustomInterceptorConfig,
]

class HTTPConfig(BaseModel):
    """HTTP客户端配置"""

    # 基础配置
    base_url: str = Field(..., description="API基础URL")
    timeout: int = Field(default=30, description="请求超时时间（秒）")
    max_retries: int = Field(default=3, description="最大重试次数")
    verify_ssl: bool = Field(default=True, description="是否验证SSL证书")

    # 🆕 拦截器配置（使用discriminator自动识别类型）
    interceptors: List[InterceptorConfigUnion] = Field(
        default_factory=list,
        description="拦截器配置列表"
    )

    class Config:
        # 使用discriminator自动识别拦截器类型
        discriminator = "type"
```

---

### 4. FrameworkSettings设计

```python
from pydantic_settings import BaseSettings

class FrameworkSettings(BaseSettings):
    """框架配置基类"""

    # HTTP配置
    http: HTTPConfig = Field(
        default_factory=HTTPConfig,
        description="HTTP客户端配置"
    )

    # 数据库配置
    db: Optional[DatabaseConfig] = None

    # Redis配置
    redis: Optional[RedisConfig] = None

    # 日志配置
    logging: LoggingConfig = Field(default_factory=LoggingConfig)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"  # 支持嵌套配置 APP_HTTP__BASE_URL
        extra = "ignore"
```

---

## 🔄 配置加载流程

### 流程图

```
1. 加载.env文件
    ↓
2. 解析settings.py (FrameworkSettings)
    ↓
3. HTTPConfig.interceptors (List[InterceptorConfig])
    ↓
4. InterceptorFactory.create_from_config()
    ↓
5. 创建Interceptor实例
    ↓
6. 添加到HttpClient.chain
```

---

### 详细流程

#### Step 1: 定义配置

```python
# settings.py
import os
from pydantic import Field
from df_test_framework import FrameworkSettings, HTTPConfig
from df_test_framework.clients.http.auth.interceptors.configs import (
    SignatureInterceptorConfig,
    AdminAuthInterceptorConfig,
)

class GiftCardSettings(FrameworkSettings):
    """礼品卡项目配置"""

    http: HTTPConfig = Field(
        default_factory=lambda: HTTPConfig(
            base_url=os.getenv("API_BASE_URL", "http://api.example.com"),
            timeout=int(os.getenv("HTTP_TIMEOUT", "30")),
            interceptors=[
                # 签名拦截器
                SignatureInterceptorConfig(
                    type="signature",
                    enabled=True,
                    priority=10,
                    algorithm="md5",
                    secret=os.getenv("BUSINESS_APP_SECRET", "default_secret"),
                    header_name="X-Sign",
                ),
                # Admin认证拦截器
                AdminAuthInterceptorConfig(
                    type="admin_auth",
                    enabled=True,
                    priority=20,
                    login_url="/admin/auth/login",
                    username=os.getenv("ADMIN_USERNAME", "admin"),
                    password=os.getenv("ADMIN_PASSWORD", "admin123"),
                ),
            ]
        )
    )
```

---

#### Step 2: 框架初始化（在conftest.py中）

```python
# conftest.py
import pytest
from df_test_framework import HttpClient
from gift_card_test.config.settings import GiftCardSettings

@pytest.fixture(scope="session")
def settings():
    """加载配置"""
    return GiftCardSettings()

@pytest.fixture(scope="session")
def http_client(settings):
    """创建HTTP客户端（自动加载拦截器）"""
    # 🆕 HttpClient从config加载拦截器
    return HttpClient.from_config(settings.http)
```

---

#### Step 3: HttpClient加载拦截器

```python
# clients/http/rest/httpx/client.py
from df_test_framework.clients.http.auth.interceptors.factory import InterceptorFactory

class HttpClient:

    @classmethod
    def from_config(cls, config: HTTPConfig) -> "HttpClient":
        """从配置创建HttpClient

        Args:
            config: HTTP配置对象

        Returns:
            配置好拦截器的HttpClient实例
        """
        # 1. 创建HttpClient实例
        client = cls(base_url=config.base_url)

        # 2. 从config加载拦截器
        if config.interceptors:
            for interceptor_config in config.interceptors:
                if not interceptor_config.enabled:
                    continue

                # 🔑 使用InterceptorFactory创建拦截器实例
                interceptor = InterceptorFactory.create(interceptor_config)

                # 添加到拦截器链
                client.use(interceptor)

                logger.info(
                    f"[HttpClient] 加载拦截器: {interceptor.name} "
                    f"(priority={interceptor.priority})"
                )

        return client
```

---

#### Step 4: InterceptorFactory实现

```python
# clients/http/auth/interceptors/factory.py
from typing import Type, Dict
from .configs import InterceptorConfig
from .signature import SignatureInterceptor
from .admin_auth import AdminAuthInterceptor
from .log import LogInterceptor

class InterceptorFactory:
    """拦截器工厂"""

    # 内置拦截器映射
    _registry: Dict[str, Type[Interceptor]] = {
        "signature": SignatureInterceptor,
        "admin_auth": AdminAuthInterceptor,
        "log": LogInterceptor,
    }

    @classmethod
    def create(cls, config: InterceptorConfig) -> Interceptor:
        """从配置创建拦截器实例

        Args:
            config: 拦截器配置对象

        Returns:
            拦截器实例

        Raises:
            ValueError: 未知的拦截器类型
        """
        # 1. 查找拦截器类
        if config.type not in cls._registry:
            if config.type == "custom":
                return cls._create_custom(config)
            raise ValueError(f"未知的拦截器类型: {config.type}")

        interceptor_class = cls._registry[config.type]

        # 2. 提取参数（排除基类字段）
        params = config.dict(exclude={"type", "enabled"})

        # 3. 创建实例
        return interceptor_class(**params)

    @classmethod
    def _create_custom(cls, config: CustomInterceptorConfig) -> Interceptor:
        """创建自定义拦截器"""
        import importlib

        # 动态导入类
        module_path, class_name = config.class_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        interceptor_class = getattr(module, class_name)

        # 创建实例
        return interceptor_class(**config.params)

    @classmethod
    def register(cls, name: str, interceptor_class: Type[Interceptor]):
        """注册自定义拦截器类型

        Args:
            name: 拦截器类型名称
            interceptor_class: 拦截器类

        Example:
            >>> InterceptorFactory.register("my_interceptor", MyInterceptor)
        """
        cls._registry[name] = interceptor_class
```

---

## 🎨 使用示例

### 示例1: 纯配置（推荐）

```python
# settings.py
class GiftCardSettings(FrameworkSettings):
    http: HTTPConfig = Field(
        default_factory=lambda: HTTPConfig(
            base_url=os.getenv("API_BASE_URL"),
            interceptors=[
                SignatureInterceptorConfig(
                    algorithm="md5",
                    secret=os.getenv("BUSINESS_APP_SECRET"),
                    priority=10,
                ),
            ]
        )
    )

# conftest.py
@pytest.fixture(scope="session")
def http_client(settings):
    return HttpClient.from_config(settings.http)  # ✅ 自动加载拦截器
```

---

### 示例2: 配置 + 手工添加

```python
# settings.py - 配置全局拦截器
class GiftCardSettings(FrameworkSettings):
    http: HTTPConfig = Field(
        default_factory=lambda: HTTPConfig(
            base_url=os.getenv("API_BASE_URL"),
            interceptors=[
                SignatureInterceptorConfig(algorithm="md5", priority=10),
            ]
        )
    )

# conftest.py - 手工添加额外拦截器
@pytest.fixture(scope="session")
def http_client(settings):
    client = HttpClient.from_config(settings.http)  # 加载全局拦截器

    # 手工添加日志拦截器
    client.use(LogInterceptor(level="DEBUG", priority=100))

    return client
```

---

### 示例3: 不同环境不同配置

```python
# settings.py
class GiftCardSettings(FrameworkSettings):

    env: str = Field(default=os.getenv("ENV", "test"))

    @property
    def http(self) -> HTTPConfig:
        """根据环境返回不同的HTTP配置"""
        base_config = HTTPConfig(
            base_url=self._get_base_url(),
            interceptors=self._get_interceptors(),
        )
        return base_config

    def _get_base_url(self) -> str:
        urls = {
            "dev": "http://dev.api.example.com",
            "test": "http://test.api.example.com",
            "prod": "http://api.example.com",
        }
        return urls[self.env]

    def _get_interceptors(self) -> List[InterceptorConfig]:
        interceptors = [
            SignatureInterceptorConfig(
                algorithm="md5",
                secret=os.getenv("BUSINESS_APP_SECRET"),
                priority=10,
            ),
        ]

        # 生产环境禁用日志拦截器
        if self.env != "prod":
            interceptors.append(
                LogInterceptorConfig(level="DEBUG", priority=100)
            )

        return interceptors
```

---

### 示例4: YAML配置（可选）

```yaml
# settings.yaml
http:
  base_url: http://api.example.com
  timeout: 30
  interceptors:
    - type: signature
      enabled: true
      priority: 10
      algorithm: md5
      secret: ${BUSINESS_APP_SECRET}
      header_name: X-Sign

    - type: admin_auth
      enabled: true
      priority: 20
      login_url: /admin/auth/login
      username: ${ADMIN_USERNAME}
      password: ${ADMIN_PASSWORD}
```

```python
# settings.py
import yaml
from pathlib import Path

class GiftCardSettings(FrameworkSettings):

    @classmethod
    def from_yaml(cls, yaml_file: str) -> "GiftCardSettings":
        """从YAML文件加载配置"""
        with open(yaml_file) as f:
            config_dict = yaml.safe_load(f)

        # 环境变量替换
        config_dict = cls._replace_env_vars(config_dict)

        return cls(**config_dict)

    @staticmethod
    def _replace_env_vars(config: dict) -> dict:
        """递归替换环境变量 ${VAR_NAME}"""
        import re

        if isinstance(config, dict):
            return {k: GiftCardSettings._replace_env_vars(v) for k, v in config.items()}
        elif isinstance(config, list):
            return [GiftCardSettings._replace_env_vars(item) for item in config]
        elif isinstance(config, str):
            pattern = r'\$\{([^}]+)\}'
            matches = re.findall(pattern, config)
            for var_name in matches:
                config = config.replace(f"${{{var_name}}}", os.getenv(var_name, ""))
            return config
        else:
            return config

# conftest.py
@pytest.fixture(scope="session")
def settings():
    return GiftCardSettings.from_yaml("settings.yaml")
```

---

## 🔑 关键设计决策

### 1. 为什么使用Pydantic的discriminator？

```python
# HTTPConfig中使用Union + discriminator
interceptors: List[
    Annotated[
        Union[
            SignatureInterceptorConfig,
            AdminAuthInterceptorConfig,
            LogInterceptorConfig,
            CustomInterceptorConfig,
        ],
        Field(discriminator="type")
    ]
]
```

**优势**:
- ✅ 自动类型识别（根据`type`字段）
- ✅ 类型安全（IDE自动补全）
- ✅ 自动验证（Pydantic验证）

---

### 2. 为什么配置对象不直接包含Interceptor实例？

**错误的设计**:
```python
class HTTPConfig(BaseModel):
    interceptors: List[Interceptor]  # ❌ 不能序列化
```

**正确的设计**:
```python
class HTTPConfig(BaseModel):
    interceptors: List[InterceptorConfig]  # ✅ 可以序列化

# 在HttpClient中才创建实例
client = HttpClient.from_config(config)
```

**原因**:
- 配置对象需要可序列化（JSON/YAML）
- 拦截器实例不能序列化（包含闭包、状态等）
- 职责分离：配置负责"描述"，工厂负责"创建"

---

### 3. 为什么需要InterceptorFactory？

**职责分离**:
- `InterceptorConfig` - 描述拦截器的配置
- `InterceptorFactory` - 根据配置创建拦截器实例
- `Interceptor` - 实际执行拦截逻辑

**优势**:
- ✅ 单一职责
- ✅ 易于扩展（注册新类型）
- ✅ 易于测试（Mock工厂）

---

### 4. 为什么HttpClient.from_config()是类方法？

```python
# ✅ 推荐
client = HttpClient.from_config(settings.http)

# ❌ 不推荐
client = HttpClient(base_url=..., config=...)
```

**原因**:
- 清晰的语义（从配置创建）
- 避免参数混乱（base_url重复）
- 工厂方法模式

---

## 📊 配置系统与拦截器的关系

```
┌─────────────────────────────────────┐
│   settings.py (配置定义)             │
│   ┌─────────────────────────────┐   │
│   │ HTTPConfig                  │   │
│   │   interceptors: [           │   │
│   │     SignatureConfig,        │   │
│   │     AdminAuthConfig,        │   │
│   │   ]                         │   │
│   └─────────────────────────────┘   │
└─────────────────────────────────────┘
            ↓
┌─────────────────────────────────────┐
│   HttpClient.from_config()          │
│   ┌─────────────────────────────┐   │
│   │ for config in interceptors: │   │
│   │   interceptor = Factory     │   │
│   │     .create(config)         │   │
│   │   client.use(interceptor)   │   │
│   └─────────────────────────────┘   │
└─────────────────────────────────────┘
            ↓
┌─────────────────────────────────────┐
│   InterceptorChain                  │
│   ┌─────────────────────────────┐   │
│   │ SignatureInterceptor        │   │
│   │ AdminAuthInterceptor        │   │
│   │ (按priority排序)             │   │
│   └─────────────────────────────┘   │
└─────────────────────────────────────┘
            ↓
┌─────────────────────────────────────┐
│   HttpClient.request()              │
│   执行拦截器链                       │
└─────────────────────────────────────┘
```

---

## ✅ 总结

### 配置系统的职责

1. **定义配置结构** - `HTTPConfig`, `InterceptorConfig`
2. **加载配置** - 从`.env`, `settings.py`, `settings.yaml`
3. **验证配置** - Pydantic自动验证
4. **环境变量替换** - `${VAR_NAME}`支持

### 拦截器系统的职责

1. **定义拦截器接口** - `Interceptor`基类
2. **实现具体拦截器** - `SignatureInterceptor`, `AdminAuthInterceptor`
3. **管理执行顺序** - `InterceptorChain`
4. **执行拦截逻辑** - `HttpClient.request()`

### 两者集成

- **配置 → 工厂 → 实例 → 链 → 执行**
- `InterceptorFactory`是桥梁
- `HttpClient.from_config()`是入口

---

**下一步**: 按照这个设计实施代码重构
