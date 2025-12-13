# 签名验证 - 框架能力设计

## 🎯 设计原则

**框架应该提供**: 通用的、可复用的、标准化的能力
**测试项目应该提供**: 业务特定的、定制化的实现

---

## 📦 框架应该提供的能力

### 1. 签名协议和抽象 (Protocol & Base Classes)

**位置**: `df_test_framework/clients/http/auth/signature/`

#### 1.1 SignatureStrategy 协议

```python
# df_test_framework/clients/http/auth/signature/protocols.py

from typing import Protocol, Dict, Any

class SignatureStrategy(Protocol):
    """签名策略协议 - 定义签名算法的标准接口"""

    def generate_signature(
        self,
        params: Dict[str, Any],
        secret: str
    ) -> str:
        """生成签名"""
        ...

    def verify_signature(
        self,
        params: Dict[str, Any],
        secret: str,
        signature: str
    ) -> bool:
        """验证签名"""
        ...
```

**为什么框架提供**:
- ✅ 定义标准接口，确保所有签名实现的一致性
- ✅ 支持多种签名算法的扩展（MD5、SHA256、HMAC等）
- ✅ 测试项目可以直接实现此协议

---

#### 1.2 常用签名算法实现

```python
# df_test_framework/clients/http/auth/signature/strategies.py

class MD5SortedValuesStrategy:
    """MD5排序值签名策略 - 通用实现"""

class SHA256SortedValuesStrategy:
    """SHA256排序值签名策略 - 通用实现"""

class HMACSignatureStrategy:
    """HMAC签名策略 - 支持多种哈希算法"""

class RSASignatureStrategy:
    """RSA非对称签名策略"""
```

**为什么框架提供**:
- ✅ 这些是行业标准算法，很多项目都会用到
- ✅ 避免每个测试项目重复实现相同的算法
- ✅ 框架统一维护，确保安全性和正确性

**什么时候测试项目自己实现**:
- ❌ 业务特定的签名逻辑（如特殊的参数排序规则）
- ❌ 公司内部的定制签名算法

---

### 2. 签名拦截器基类

**位置**: `df_test_framework/clients/http/auth/interceptors/`

#### 2.1 BaseSignatureInterceptor

```python
# df_test_framework/clients/http/auth/interceptors/signature.py

from typing import Dict, Any, Optional, Callable
from pydantic import BaseModel, Field

class SignatureConfig(BaseModel):
    """签名配置 - 框架提供的标准配置"""

    enabled: bool = Field(default=True, description="是否启用签名")
    algorithm: str = Field(default="md5", description="签名算法")
    secret: str = Field(description="签名密钥")
    header_name: str = Field(default="X-Sign", description="签名Header名称")

    # 参数提取配置
    include_query_params: bool = Field(default=True, description="是否包含URL参数")
    include_json_body: bool = Field(default=True, description="是否包含JSON Body")
    include_form_data: bool = Field(default=False, description="是否包含表单数据")

    # 高级配置
    param_filter: Optional[Callable] = Field(default=None, description="参数过滤函数")
    custom_header_builder: Optional[Callable] = Field(default=None, description="自定义Header构建函数")


class BaseSignatureInterceptor:
    """签名拦截器基类 - 框架提供的通用实现"""

    def __init__(
        self,
        config: SignatureConfig,
        strategy: SignatureStrategy
    ):
        self.config = config
        self.strategy = strategy

    def __call__(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """拦截器入口 - 框架实现核心逻辑"""

        if not self.config.enabled:
            return kwargs

        # 1. 提取参数（框架提供通用逻辑）
        all_params = self._extract_params(params, json, kwargs)

        # 2. 应用参数过滤（如果有）
        if self.config.param_filter:
            all_params = self.config.param_filter(all_params)

        # 3. 生成签名
        signature = self.strategy.generate_signature(
            all_params,
            self.config.secret
        )

        # 4. 添加到Header
        if headers is None:
            headers = {}

        # 支持自定义Header构建
        if self.config.custom_header_builder:
            headers = self.config.custom_header_builder(headers, signature)
        else:
            headers[self.config.header_name] = signature

        return {
            "headers": headers,
            "params": params,
            "json": json,
            **kwargs
        }

    def _extract_params(
        self,
        params: Optional[Dict[str, Any]],
        json: Optional[Dict[str, Any]],
        kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """提取请求参数 - 框架提供的通用逻辑"""

        all_params = {}

        if self.config.include_query_params and params:
            all_params.update(params)

        if self.config.include_json_body and json:
            all_params.update(json)

        if self.config.include_form_data and "data" in kwargs:
            # 处理表单数据
            all_params.update(kwargs["data"])

        return all_params
```

**为什么框架提供**:
- ✅ 参数提取逻辑是通用的（query、body、form）
- ✅ 拦截器调用接口是标准的（callable interface）
- ✅ 提供配置开关，支持灵活定制
- ✅ 减少测试项目的重复代码

**测试项目如何使用**:
```python
# gift-card-test/src/gift_card_test/auth/interceptors/signature_interceptor.py

from df_test_framework.clients.http.auth.interceptors import BaseSignatureInterceptor
from df_test_framework.clients.http.auth.signature import MD5SortedValuesStrategy

class GiftCardSignatureInterceptor(BaseSignatureInterceptor):
    """礼品卡项目的签名拦截器 - 只需继承框架基类"""

    def __init__(self, config):
        # 使用框架提供的MD5策略
        strategy = MD5SortedValuesStrategy()
        super().__init__(config, strategy)

    # 如果有特殊逻辑，可以覆盖方法
    def _extract_params(self, params, json, kwargs):
        # 礼品卡项目的特殊参数处理
        all_params = super()._extract_params(params, json, kwargs)
        # ... 业务特定逻辑
        return all_params
```

---

### 3. 常用工具函数

**位置**: `df_test_framework/clients/http/auth/signature/utils.py`

```python
# df_test_framework/clients/http/auth/signature/utils.py

def sort_params_by_key(params: Dict[str, Any]) -> Dict[str, Any]:
    """按key排序参数 - 很多签名算法都需要"""
    from collections import OrderedDict
    return OrderedDict(sorted(params.items()))


def filter_empty_values(params: Dict[str, Any]) -> Dict[str, Any]:
    """过滤空值参数 - 很多签名算法都需要"""
    return {
        k: v for k, v in params.items()
        if v is not None and str(v)
    }


def concat_values(params: Dict[str, Any]) -> str:
    """拼接参数值 - 很多签名算法都需要"""
    return "".join(str(v) for v in params.values())


def build_query_string(params: Dict[str, Any], encoding: str = "utf-8") -> str:
    """构建查询字符串 - 用于URL签名"""
    from urllib.parse import urlencode
    return urlencode(params, encoding=encoding)
```

**为什么框架提供**:
- ✅ 这些是签名生成的常用操作
- ✅ 避免每个项目重复实现
- ✅ 框架统一维护，确保正确性

---

### 4. 认证拦截器集合

**位置**: `df_test_framework/clients/http/auth/interceptors/`

除了签名拦截器，框架还应该提供其他常用的认证拦截器：

```python
# df_test_framework/clients/http/auth/interceptors/token.py

class BearerTokenInterceptor:
    """Bearer Token拦截器"""

    def __init__(self, token: str):
        self.token = token

    def __call__(self, method, url, headers=None, **kwargs):
        if headers is None:
            headers = {}
        headers["Authorization"] = f"Bearer {self.token}"
        return {"headers": headers, **kwargs}


class BasicAuthInterceptor:
    """Basic认证拦截器"""

    def __init__(self, username: str, password: str):
        import base64
        credentials = f"{username}:{password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        self.auth_header = f"Basic {encoded}"

    def __call__(self, method, url, headers=None, **kwargs):
        if headers is None:
            headers = {}
        headers["Authorization"] = self.auth_header
        return {"headers": headers, **kwargs}


class APIKeyInterceptor:
    """API Key拦截器"""

    def __init__(self, api_key: str, header_name: str = "X-API-Key"):
        self.api_key = api_key
        self.header_name = header_name

    def __call__(self, method, url, headers=None, **kwargs):
        if headers is None:
            headers = {}
        headers[self.header_name] = self.api_key
        return {"headers": headers, **kwargs}
```

**为什么框架提供**:
- ✅ Bearer Token、Basic Auth、API Key是最常见的认证方式
- ✅ 实现标准且简单，适合框架提供
- ✅ 测试项目可以直接使用，无需重复实现

---

### 5. Fixtures支持

**位置**: `df_test_framework/testing/fixtures/auth.py`

```python
# df_test_framework/testing/fixtures/auth.py

import pytest
from typing import Optional

@pytest.fixture(scope="session")
def signature_config(settings) -> Optional[SignatureConfig]:
    """签名配置fixture - 框架提供"""

    # 如果settings中有signature配置，自动创建
    if hasattr(settings, "signature"):
        return settings.signature

    return None


@pytest.fixture(scope="session")
def signature_interceptor(signature_config, signature_strategy):
    """签名拦截器fixture - 框架提供"""

    if signature_config is None:
        return None

    return BaseSignatureInterceptor(signature_config, signature_strategy)
```

**为什么框架提供**:
- ✅ 提供标准的fixture命名和scope
- ✅ 自动集成到框架的配置系统
- ✅ 测试项目可以直接使用或覆盖

---

## 🏢 测试项目应该提供的能力

### 1. 业务特定的签名策略

如果业务有特殊的签名算法（不是标准的MD5/SHA256），测试项目需要自己实现：

```python
# gift-card-test/src/gift_card_test/auth/signature/strategies.py

from df_test_framework.clients.http.auth.signature import SignatureStrategy

class GiftCardCustomSignatureStrategy:
    """礼品卡项目的自定义签名策略"""

    def generate_signature(self, params, secret):
        # 业务特定的签名逻辑
        # 例如：特殊的参数排序、特殊的字符串拼接规则等
        ...
```

### 2. 业务特定的配置

```python
# gift-card-test/src/gift_card_test/config/settings.py

class SignatureSettings(BaseModel):
    """礼品卡项目的签名配置"""

    enabled: bool = True
    algorithm: str = "md5"
    app_secret: str = Field(..., env="GIFT_CARD_APP_SECRET")

    # 业务特定配置
    include_timestamp: bool = True  # 签名是否包含时间戳
    timestamp_tolerance: int = 300   # 时间戳容差（秒）
```

### 3. 业务特定的拦截器定制

```python
# gift-card-test/src/gift_card_test/auth/interceptors/signature_interceptor.py

from df_test_framework.clients.http.auth.interceptors import BaseSignatureInterceptor

class GiftCardSignatureInterceptor(BaseSignatureInterceptor):
    """礼品卡项目的签名拦截器"""

    def _extract_params(self, params, json, kwargs):
        all_params = super()._extract_params(params, json, kwargs)

        # 礼品卡特殊逻辑：添加时间戳
        if self.config.include_timestamp:
            import time
            all_params["timestamp"] = int(time.time())

        return all_params
```

---

## 📊 能力划分对比表

| 能力 | 框架提供 | 测试项目提供 | 原因 |
|------|---------|------------|------|
| **SignatureStrategy协议** | ✅ | | 定义标准接口 |
| **MD5/SHA256/HMAC策略** | ✅ | | 通用算法实现 |
| **业务特定签名策略** | | ✅ | 业务逻辑 |
| **BaseSignatureInterceptor** | ✅ | | 通用拦截器逻辑 |
| **参数提取逻辑** | ✅ | | 通用HTTP参数处理 |
| **业务特定拦截器** | | ✅ | 业务定制需求 |
| **SignatureConfig基类** | ✅ | | 标准配置字段 |
| **业务配置扩展** | | ✅ | 业务特定配置 |
| **工具函数(sort/filter)** | ✅ | | 常用操作 |
| **Bearer/Basic/APIKey拦截器** | ✅ | | 标准认证方式 |
| **signature_config fixture** | ✅ | | 标准fixture |
| **业务特定fixture** | | ✅ | 业务集成 |

---

## 🎯 框架能力总结

### 核心价值

**框架应该提供的核心价值**:
1. ✅ **标准化**: 定义签名验证的标准接口和协议
2. ✅ **可复用**: 提供常用签名算法的实现
3. ✅ **易扩展**: 通过Protocol支持自定义签名策略
4. ✅ **开箱即用**: 提供常用认证拦截器（Bearer、Basic、APIKey）
5. ✅ **配置驱动**: 通过Pydantic配置灵活控制行为

### 目录结构建议

```
df-test-framework/
└── src/df_test_framework/
    └── clients/http/
        └── auth/
            ├── __init__.py
            ├── signature/
            │   ├── __init__.py
            │   ├── protocols.py          # SignatureStrategy协议
            │   ├── strategies.py         # MD5/SHA256/HMAC等实现
            │   ├── config.py             # SignatureConfig
            │   └── utils.py              # 工具函数
            └── interceptors/
                ├── __init__.py
                ├── signature.py          # BaseSignatureInterceptor
                ├── token.py              # BearerTokenInterceptor等
                └── api_key.py            # APIKeyInterceptor
```

### 测试项目集成

```python
# 测试项目只需要：
from df_test_framework.clients.http.auth.signature import (
    SignatureStrategy,
    MD5SortedValuesStrategy,  # 直接使用框架提供的
    SignatureConfig,
)
from df_test_framework.clients.http.auth.interceptors import (
    BaseSignatureInterceptor,
)

# 1. 使用框架提供的策略（无需自己实现）
config = SignatureConfig(
    algorithm="md5",
    secret="my_secret",
)
strategy = MD5SortedValuesStrategy()
interceptor = BaseSignatureInterceptor(config, strategy)

# 2. 或者实现业务特定的策略
class MyCustomStrategy:
    def generate_signature(self, params, secret):
        # 业务特定逻辑
        ...

strategy = MyCustomStrategy()
interceptor = BaseSignatureInterceptor(config, strategy)
```

---

## 🚀 下一步行动

### 框架侧

1. **创建auth模块结构**
   ```bash
   mkdir -p src/df_test_framework/clients/http/auth/{signature,interceptors}
   ```

2. **移植通用代码**
   - 从gift-card-test移植`SignatureStrategy`协议
   - 移植`MD5SortedValuesStrategy`和`SHA256SortedValuesStrategy`
   - 创建`BaseSignatureInterceptor`

3. **添加文档和测试**
   - 为每个签名策略添加单元测试
   - 创建使用示例文档

4. **发布到框架**
   - 添加到`__init__.py`导出
   - 更新框架版本号
   - 更新CHANGELOG

### 测试项目侧

1. **重构为使用框架能力**
   ```python
   # 从
   from gift_card_test.auth.signature import MD5SortedValuesStrategy

   # 改为
   from df_test_framework.clients.http.auth.signature import MD5SortedValuesStrategy
   ```

2. **删除重复代码**
   - 删除通用签名策略实现
   - 保留业务特定的定制逻辑

3. **简化配置**
   - 使用框架提供的`SignatureConfig`
   - 只扩展业务特定的配置字段

---

## 💡 设计哲学

> **框架提供骨架，测试项目填充血肉**

- **框架**: 提供可复用的、标准化的基础能力
- **测试项目**: 实现业务特定的逻辑和定制

这样做的好处：
- ✅ 避免重复造轮子
- ✅ 统一的代码风格和接口
- ✅ 框架统一维护，确保质量
- ✅ 测试项目更简洁，专注业务逻辑
