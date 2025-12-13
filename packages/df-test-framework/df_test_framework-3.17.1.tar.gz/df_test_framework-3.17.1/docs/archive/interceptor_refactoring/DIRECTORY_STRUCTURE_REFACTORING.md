# HTTP模块目录结构重构方案

> **问题**: 当前`clients/http/auth/`目录名称不合理
> **原因**:
> - "auth"暗示只处理认证，但实际包含签名、日志等非认证功能
> - SignatureInterceptor不是认证，是请求签名
> - LoggingInterceptor不是认证，是日志记录
>
> **目标**: 重新设计更合理的目录结构

---

## 🔍 当前目录结构分析

### 当前结构（不合理）

```
src/df_test_framework/clients/http/
├── auth/                           # ❌ 名称不准确
│   ├── signature/                  # 签名策略（不是认证）
│   │   ├── strategies.py
│   │   └── protocols.py
│   ├── interceptors/               # 拦截器（不全是认证）
│   │   ├── signature.py           # ❌ 签名不是认证
│   │   ├── bearer_token.py        # ✅ 这才是认证
│   │   └── logging.py             # ❌ 日志不是认证
│   └── __init__.py
└── rest/
    └── httpx/
        ├── client.py
        └── base_api.py
```

**问题**:
1. `auth/`目录暗示"认证"，但包含了非认证功能
2. `signature/`是请求签名，不是身份认证
3. `logging/`是日志记录，与认证无关
4. 目录结构与功能不匹配

---

## ✅ 重构方案

### 方案A: 按功能分类（推荐）⭐

```
src/df_test_framework/clients/http/
├── core/                           # 核心抽象
│   ├── __init__.py
│   ├── request.py                 # Request对象
│   ├── response.py                # Response对象
│   ├── interceptor.py             # Interceptor接口
│   └── chain.py                   # InterceptorChain
│
├── interceptors/                   # 🆕 拦截器目录（更准确）
│   ├── __init__.py
│   ├── auth/                      # 认证相关拦截器
│   │   ├── __init__.py
│   │   ├── bearer_token.py       # Bearer Token认证
│   │   ├── basic_auth.py         # Basic认证
│   │   └── api_key.py            # API Key认证
│   ├── signature/                 # 签名相关拦截器
│   │   ├── __init__.py
│   │   ├── interceptor.py        # SignatureInterceptor
│   │   ├── strategies.py         # 签名策略
│   │   └── protocols.py          # 签名协议
│   ├── logging.py                # 日志拦截器
│   ├── retry.py                  # 重试拦截器（未来）
│   ├── rate_limit.py             # 限流拦截器（未来）
│   └── factory.py                # InterceptorFactory
│
└── rest/                          # REST客户端
    └── httpx/
        ├── client.py
        └── base_api.py
```

**优点**:
- ✅ 目录名称准确（interceptors/而不是auth/）
- ✅ 按功能分类清晰（auth/signature/logging）
- ✅ 易于扩展（添加retry/rate_limit等）
- ✅ 符合单一职责原则

**导入路径**:
```python
from df_test_framework.clients.http.core import Request, Response, Interceptor
from df_test_framework.clients.http.interceptors.auth import BearerTokenInterceptor
from df_test_framework.clients.http.interceptors.signature import SignatureInterceptor
from df_test_framework.clients.http.interceptors import LoggingInterceptor
```

---

### 方案B: 扁平化结构（更简单）

```
src/df_test_framework/clients/http/
├── core/                           # 核心抽象
│   ├── request.py
│   ├── response.py
│   ├── interceptor.py
│   └── chain.py
│
├── interceptors/                   # 🆕 拦截器（扁平）
│   ├── __init__.py
│   ├── bearer_token.py            # 认证拦截器
│   ├── basic_auth.py              # 认证拦截器
│   ├── api_key.py                 # 认证拦截器
│   ├── signature.py               # 签名拦截器
│   ├── logging.py                 # 日志拦截器
│   ├── retry.py                   # 重试拦截器
│   └── factory.py                 # 工厂
│
├── signature/                      # 签名策略（独立）
│   ├── strategies.py
│   └── protocols.py
│
└── rest/
    └── httpx/
        ├── client.py
        └── base_api.py
```

**优点**:
- ✅ 结构简单
- ✅ 导入路径更短

**缺点**:
- ❌ 拦截器数量增多后会混乱
- ❌ 没有分类

---

### 方案C: 保持当前结构，只改名

```
src/df_test_framework/clients/http/
├── extensions/                     # 🆕 重命名（扩展功能）
│   ├── signature/
│   ├── interceptors/
│   └── __init__.py
│
└── rest/
    └── httpx/
```

**优点**:
- ✅ 改动最小

**缺点**:
- ❌ "extensions"名称仍然不够准确
- ❌ 没有解决根本问题

---

## 🎯 推荐方案：方案A（按功能分类）

### 详细目录结构

```
src/df_test_framework/clients/http/
│
├── core/                           # HTTP核心抽象
│   ├── __init__.py
│   ├── request.py                 # Request对象（不可变）
│   ├── response.py                # Response对象（不可变）
│   ├── interceptor.py             # Interceptor接口
│   └── chain.py                   # InterceptorChain（责任链）
│
├── interceptors/                   # 拦截器目录
│   ├── __init__.py                # 导出所有拦截器
│   │
│   ├── auth/                      # 认证拦截器子目录
│   │   ├── __init__.py
│   │   ├── bearer_token.py       # Bearer Token认证
│   │   ├── basic_auth.py         # HTTP Basic认证
│   │   └── api_key.py            # API Key认证
│   │
│   ├── signature/                 # 签名拦截器子目录
│   │   ├── __init__.py
│   │   ├── interceptor.py        # SignatureInterceptor
│   │   ├── strategies.py         # 签名策略实现
│   │   └── protocols.py          # 签名策略协议
│   │
│   ├── logging.py                # 日志拦截器
│   ├── retry.py                  # 重试拦截器（未来）
│   ├── timeout.py                # 超时拦截器（未来）
│   ├── rate_limit.py             # 限流拦截器（未来）
│   ├── cache.py                  # 缓存拦截器（未来）
│   │
│   └── factory.py                # InterceptorFactory
│
├── rest/                          # REST客户端实现
│   └── httpx/
│       ├── __init__.py
│       ├── client.py             # HttpClient
│       └── base_api.py           # BaseAPI
│
└── __init__.py                    # HTTP模块导出
```

---

## 📝 迁移步骤

### Step 1: 创建新目录结构

```bash
# 创建interceptors目录
mkdir -p src/df_test_framework/clients/http/interceptors/auth
mkdir -p src/df_test_framework/clients/http/interceptors/signature
```

### Step 2: 移动文件

```bash
# 移动签名相关文件
mv src/df_test_framework/clients/http/auth/signature/strategies.py \
   src/df_test_framework/clients/http/interceptors/signature/
mv src/df_test_framework/clients/http/auth/signature/protocols.py \
   src/df_test_framework/clients/http/interceptors/signature/

# 移动拦截器文件
mv src/df_test_framework/clients/http/auth/interceptors/signature.py \
   src/df_test_framework/clients/http/interceptors/signature/interceptor.py
mv src/df_test_framework/clients/http/auth/interceptors/bearer_token.py \
   src/df_test_framework/clients/http/interceptors/auth/
mv src/df_test_framework/clients/http/auth/interceptors/logging.py \
   src/df_test_framework/clients/http/interceptors/
```

### Step 3: 更新导入路径

```python
# 旧导入路径
from df_test_framework.clients.http.auth.interceptors import SignatureInterceptor
from df_test_framework.clients.http.auth.interceptors import BearerTokenInterceptor

# 新导入路径
from df_test_framework.clients.http.interceptors.signature import SignatureInterceptor
from df_test_framework.clients.http.interceptors.auth import BearerTokenInterceptor
from df_test_framework.clients.http.interceptors import LoggingInterceptor
```

### Step 4: 删除旧目录

```bash
# 删除旧的auth目录
rm -rf src/df_test_framework/clients/http/auth
```

---

## 🎨 新的导入示例

### 框架级导出

```python
# src/df_test_framework/__init__.py
from .clients.http.core import (
    Request,
    Response,
    Interceptor,
    BaseInterceptor,
    InterceptorChain,
)

from .clients.http.interceptors import (
    # 认证拦截器
    BearerTokenInterceptor,
    BasicAuthInterceptor,
    APIKeyInterceptor,
    # 签名拦截器
    SignatureInterceptor,
    # 其他拦截器
    LoggingInterceptor,
)
```

### 用户使用

```python
# 简洁导入
from df_test_framework import (
    HttpClient,
    SignatureInterceptor,
    BearerTokenInterceptor,
    LoggingInterceptor,
)

# 创建拦截器
signature = SignatureInterceptor(algorithm="md5", secret="xxx")
bearer = BearerTokenInterceptor(token_source="login", login_url="/login")
logging = LoggingInterceptor(level="DEBUG")

# 使用
client = HttpClient(base_url="http://api.example.com")
client.use(signature).use(bearer).use(logging)
```

---

## ✅ 优势总结

### 1. 语义清晰

| 旧结构 | 新结构 | 说明 |
|--------|--------|------|
| `auth/interceptors/signature.py` | `interceptors/signature/interceptor.py` | 签名不是认证 |
| `auth/interceptors/bearer_token.py` | `interceptors/auth/bearer_token.py` | 认证拦截器归类 |
| `auth/interceptors/logging.py` | `interceptors/logging.py` | 日志拦截器独立 |

### 2. 易于扩展

添加新拦截器时，目录结构很清晰：

```
interceptors/
├── auth/           # 认证相关 → 添加oauth.py
├── signature/      # 签名相关 → 添加新策略
├── logging.py      # 日志
├── retry.py        # 🆕 重试
├── rate_limit.py   # 🆕 限流
└── cache.py        # 🆕 缓存
```

### 3. 符合单一职责

每个目录都有明确的职责：
- `core/` - 核心抽象
- `interceptors/auth/` - 认证功能
- `interceptors/signature/` - 签名功能
- `interceptors/*.py` - 其他拦截器

---

## 🔄 版本策略

### 建议：保持v3.x

**理由**:
1. 目录结构调整**不影响API**
2. 用户导入路径调整可以通过**兼容层**过渡
3. 主版本号变化（v3→v4）给用户压力太大

**版本号建议**:
- **v3.3.0** - 重构拦截器架构（破坏性变更）
- 或 **v3.2.1** - 如果提供完整兼容层

### 兼容层示例

```python
# src/df_test_framework/clients/http/auth/__init__.py（兼容层）
"""
兼容层：保持v3.0的导入路径

⚠️ Deprecated: 此模块已废弃，请使用新路径
- df_test_framework.clients.http.interceptors.signature
- df_test_framework.clients.http.interceptors.auth
"""
import warnings

# 重定向到新位置
from ..interceptors.signature import SignatureInterceptor
from ..interceptors.auth import BearerTokenInterceptor

# 发出废弃警告
warnings.warn(
    "从 df_test_framework.clients.http.auth 导入已废弃，"
    "请改用 df_test_framework.clients.http.interceptors",
    DeprecationWarning,
    stacklevel=2
)

__all__ = ["SignatureInterceptor", "BearerTokenInterceptor"]
```

---

## 🎯 最终建议

### 推荐：方案A + v3.3.0 + 兼容层

1. **采用方案A目录结构** - 按功能分类，清晰易扩展
2. **版本号v3.3.0** - 保持v3大版本，减少用户迁移压力
3. **提供兼容层** - 旧导入路径保留一个版本周期（v3.3.x）
4. **v4.0.0时移除兼容层** - 完全清理旧路径

### 迁移时间表

- **v3.3.0** - 新目录结构 + 兼容层 + DeprecationWarning
- **v3.4.0** - 移除兼容层（或直接到v4.0.0）
- **v4.0.0** - 完全清理，只保留新结构

---

**总结**: `auth/`目录名称确实不合理，应该改为`interceptors/`并按功能分类。版本号建议保持v3.x，通过兼容层平滑过渡。
