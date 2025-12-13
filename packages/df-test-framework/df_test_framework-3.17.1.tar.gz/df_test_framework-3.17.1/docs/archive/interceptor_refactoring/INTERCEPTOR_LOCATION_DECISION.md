# 拦截器位置决策

> **核心问题**: 拦截器应该放在哪里？
> - `clients/http/interceptors/` - HTTP专属拦截器
> - `common/interceptors/` - 通用拦截器
> - `infrastructure/interceptors/` - 基础设施层拦截器

---

## 🤔 问题分析

### 当前假设（需要验证）

**假设**: 拦截器只用于HTTP请求
- ✅ SignatureInterceptor - HTTP请求签名
- ✅ BearerTokenInterceptor - HTTP认证
- ✅ LoggingInterceptor - HTTP请求日志

**但是**...

### 拦截器的本质是什么？

**拦截器 = AOP（面向切面编程）的实现**

它是一个**通用的设计模式**，不应该绑定到HTTP：

```python
# 拦截器的核心接口
class Interceptor:
    def before(self, context): ...
    def after(self, context): ...
    def on_error(self, error, context): ...
```

**可能的应用场景**:
1. **HTTP请求拦截器** - 当前已实现
2. **数据库操作拦截器** - 慢查询监控、SQL注入检测
3. **Redis操作拦截器** - 缓存失效、性能监控
4. **消息队列拦截器** - 消息序列化、错误重试
5. **WebSocket拦截器** - 连接管理、心跳检测
6. **gRPC拦截器** - Metadata注入、链路追踪

---

## 🎯 设计原则

### 原则1: 通用的抽象应该在通用的位置

**拦截器接口**（Interceptor/InterceptorChain）应该是**通用的**：
- ❌ 不应该绑定到HTTP
- ✅ 应该在`common/`或`infrastructure/`

### 原则2: 具体的实现应该在具体的位置

**HTTP拦截器实现**（SignatureInterceptor）应该是**HTTP专属的**：
- ✅ 应该在`clients/http/`

---

## 📐 架构设计

### 方案A: 通用接口 + HTTP实现（推荐）⭐

```
src/df_test_framework/
│
├── common/                          # 通用抽象
│   ├── protocols/
│   │   ├── __init__.py
│   │   ├── interceptor.py          # 🆕 通用Interceptor协议
│   │   └── chain.py                # 🆕 通用InterceptorChain
│   └── exceptions.py
│
├── clients/http/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── request.py              # HTTP专属Request
│   │   └── response.py             # HTTP专属Response
│   │
│   └── interceptors/                # HTTP拦截器实现
│       ├── auth/
│       │   └── bearer_token.py     # 实现common.protocols.Interceptor
│       ├── signature/
│       │   └── interceptor.py
│       └── logging.py
│
├── databases/
│   └── interceptors/                # 🔮 未来：数据库拦截器
│       └── slow_query.py
│
└── infrastructure/
    └── config/
        └── schema.py
```

**优点**:
- ✅ 拦截器接口通用，可复用到DB/Redis/MQ等
- ✅ HTTP实现在HTTP目录，语义清晰
- ✅ 易于扩展到其他领域

**实现示例**:
```python
# common/protocols/interceptor.py
from abc import ABC
from typing import Any, Optional

class Interceptor(ABC):
    """通用拦截器协议（不绑定HTTP）"""

    name: str
    priority: int

    def before(self, context: Any) -> Optional[Any]:
        """前置处理"""
        return None

    def after(self, context: Any) -> Optional[Any]:
        """后置处理"""
        return None

# clients/http/interceptors/signature/interceptor.py
from df_test_framework.common.protocols.interceptor import Interceptor
from df_test_framework.clients.http.core.request import Request

class SignatureInterceptor(Interceptor):
    """HTTP签名拦截器（实现通用接口）"""

    def before(self, context: Request) -> Request:
        # context是HTTP专属的Request
        return context.with_header("X-Sign", self._sign(context))
```

---

### 方案B: HTTP专属（当前实现）

```
src/df_test_framework/
└── clients/http/
    ├── core/
    │   ├── request.py
    │   ├── response.py
    │   ├── interceptor.py          # ❌ HTTP专属的Interceptor
    │   └── chain.py
    └── interceptors/
        ├── auth/
        ├── signature/
        └── logging.py
```

**优点**:
- ✅ 实现简单

**缺点**:
- ❌ 拦截器接口绑定到HTTP
- ❌ 无法复用到DB/Redis等
- ❌ 违反"通用抽象应该在通用位置"原则

---

### 方案C: 完全在infrastructure（过度设计）

```
src/df_test_framework/
└── infrastructure/
    └── interceptors/
        ├── protocols.py             # 通用协议
        ├── http/                    # HTTP实现
        │   ├── signature.py
        │   └── bearer_token.py
        └── database/                # DB实现
            └── slow_query.py
```

**缺点**:
- ❌ infrastructure是"基础设施"，放具体业务逻辑不合适
- ❌ HTTP拦截器离HttpClient太远

---

## ✅ 最终决策

### 推荐：方案A（通用接口 + 领域实现）

**核心思想**:
- **通用的抽象** → `common/protocols/`
- **HTTP的实现** → `clients/http/interceptors/`
- **DB的实现** → `databases/interceptors/`（未来）

### 完整目录结构

```
src/df_test_framework/
│
├── common/                          # 通用抽象层
│   ├── protocols/                  # 🆕 通用协议
│   │   ├── __init__.py
│   │   ├── interceptor.py          # 通用Interceptor协议
│   │   └── chain.py                # 通用InterceptorChain
│   └── exceptions.py
│
├── clients/http/                    # HTTP客户端
│   ├── core/                       # HTTP核心对象
│   │   ├── __init__.py
│   │   ├── request.py              # Request（继承/实现通用协议）
│   │   └── response.py             # Response
│   │
│   ├── interceptors/                # HTTP拦截器实现
│   │   ├── __init__.py
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   ├── bearer_token.py    # 实现common.protocols.Interceptor
│   │   │   ├── basic_auth.py
│   │   │   └── api_key.py
│   │   ├── signature/
│   │   │   ├── __init__.py
│   │   │   ├── interceptor.py     # SignatureInterceptor
│   │   │   ├── strategies.py
│   │   │   └── protocols.py
│   │   ├── logging.py             # LoggingInterceptor
│   │   └── factory.py             # InterceptorFactory
│   │
│   └── rest/httpx/
│       ├── client.py
│       └── base_api.py
│
├── databases/                       # 数据库访问
│   ├── database.py
│   └── interceptors/                # 🔮 未来：数据库拦截器
│       └── slow_query.py
│
└── infrastructure/                  # 基础设施
    └── config/
        └── schema.py
```

---

## 🔄 实施步骤

### Step 1: 创建通用协议

```python
# common/protocols/interceptor.py
from abc import ABC
from typing import TypeVar, Generic, Optional

T = TypeVar('T')  # 上下文类型（Request/DBQuery/RedisCommand等）

class Interceptor(ABC, Generic[T]):
    """通用拦截器协议

    可用于HTTP、数据库、Redis、消息队列等任何需要拦截的场景
    """

    name: str = ""
    priority: int = 100

    def before(self, context: T) -> Optional[T]:
        """前置处理

        Args:
            context: 上下文对象（Request/DBQuery/等）

        Returns:
            - None: 不修改上下文
            - T: 修改后的新上下文
        """
        return None

    def after(self, context: T) -> Optional[T]:
        """后置处理"""
        return None

    def on_error(self, error: Exception, context: T) -> None:
        """错误处理"""
        pass
```

### Step 2: HTTP拦截器实现通用协议

```python
# clients/http/interceptors/signature/interceptor.py
from df_test_framework.common.protocols.interceptor import Interceptor
from df_test_framework.clients.http.core.request import Request

class SignatureInterceptor(Interceptor[Request]):
    """HTTP签名拦截器

    实现通用的Interceptor[Request]协议
    """

    def before(self, context: Request) -> Request:
        # context是HTTP专属的Request对象
        signature = self.strategy.generate_signature(...)
        return context.with_header("X-Sign", signature)
```

### Step 3: HTTP专属命名

为了向后兼容和语义清晰，HTTP拦截器可以保留`before_request`别名：

```python
class SignatureInterceptor(Interceptor[Request]):

    def before(self, context: Request) -> Request:
        # 实现通用协议
        ...

    # 为HTTP场景提供语义化别名
    def before_request(self, request: Request) -> Request:
        return self.before(request)
```

---

## 🎨 使用示例

### HTTP拦截器

```python
from df_test_framework import HttpClient
from df_test_framework.clients.http.interceptors import SignatureInterceptor

client = HttpClient(base_url="...")
client.use(SignatureInterceptor(algorithm="md5", secret="xxx"))
```

### 未来：数据库拦截器

```python
from df_test_framework import Database
from df_test_framework.databases.interceptors import SlowQueryInterceptor

db = Database(connection_string="...")
db.use(SlowQueryInterceptor(threshold_ms=1000))
```

### 未来：Redis拦截器

```python
from df_test_framework import RedisClient
from df_test_framework.databases.interceptors import CacheMetricsInterceptor

redis = RedisClient(host="...")
redis.use(CacheMetricsInterceptor())
```

---

## ✅ 优势总结

1. **通用性** ✅
   - Interceptor协议可复用到任何领域
   - 统一的拦截器模式

2. **清晰性** ✅
   - 通用抽象在`common/protocols/`
   - HTTP实现在`clients/http/interceptors/`
   - 各司其职

3. **扩展性** ✅
   - 添加DB拦截器 → `databases/interceptors/`
   - 添加Redis拦截器 → `databases/interceptors/`
   - 不影响现有代码

4. **类型安全** ✅
   - `Interceptor[Request]` - HTTP拦截器
   - `Interceptor[DBQuery]` - 数据库拦截器
   - 泛型保证类型安全

---

## 🎯 最终答案

**拦截器应该这样组织**:

1. **通用接口** → `common/protocols/interceptor.py`
   - `Interceptor[T]` 协议
   - `InterceptorChain[T]` 责任链

2. **HTTP实现** → `clients/http/interceptors/`
   - 实现 `Interceptor[Request]`
   - 不放在`http/`目录外

3. **其他领域实现** → `{domain}/interceptors/`
   - 数据库 → `databases/interceptors/`
   - Redis → `databases/interceptors/`（或单独目录）

**总结**: 拦截器**接口通用**，**实现领域专属**，HTTP拦截器应该留在`clients/http/`目录下。
