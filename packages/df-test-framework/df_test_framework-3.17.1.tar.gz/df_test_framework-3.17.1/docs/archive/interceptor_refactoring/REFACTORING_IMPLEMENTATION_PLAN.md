# 拦截器架构重构实施计划

> **目标**: 按照理想架构设计重构拦截器系统
> **版本**: v4.0.0
> **原则**: 不保留向后兼容代码，彻底重构
> **创建时间**: 2025-11-06

---

## 🎯 重构目标

1. ✅ 实现不可变的Request/Response对象
2. ✅ 实现简洁的Interceptor接口
3. ✅ 实现InterceptorChain责任链
4. ✅ HttpClient单一拦截器入口
5. ✅ 删除BaseAPI的拦截器功能
6. ✅ 配置系统与拦截器集成
7. ✅ 所有测试通过

---

## 📋 实施步骤

### Phase 1: 清理旧代码 🗑️

**目标**: 删除旧的拦截器实现，为新架构腾出空间

#### 1.1 删除BaseAPI的拦截器相关代码

```bash
# 需要修改的文件
src/df_test_framework/clients/http/rest/httpx/base_api.py
```

**删除内容**:
- `RequestInterceptor` Protocol
- `ResponseInterceptor` Protocol
- `BaseAPI.request_interceptors` 属性
- `BaseAPI.response_interceptors` 属性
- `BaseAPI._apply_request_interceptors()` 方法
- `BaseAPI._apply_response_interceptors()` 方法
- `BaseAPI.add_request_interceptor()` 方法
- `BaseAPI.add_response_interceptor()` 方法

**保留**:
- `BaseAPI.__init__(http_client)` - 只接受http_client参数
- `BaseAPI.get/post/put/delete()` - 简化为直接调用http_client

---

#### 1.2 删除HttpClient的旧拦截器代码

```bash
# 需要修改的文件
src/df_test_framework/clients/http/rest/httpx/client.py
```

**删除内容**:
- `HttpClient.request_interceptors` 列表
- `HttpClient._load_interceptors_from_config()` 方法
- `HttpClient.request()` 中的拦截器执行代码（172-179行）

---

#### 1.3 删除旧的拦截器实现

```bash
# 需要删除的目录和文件
src/df_test_framework/clients/http/auth/interceptors/
├── signature.py          # 删除BaseSignatureInterceptor和SignatureInterceptor
├── token.py              # 删除
├── basic_auth.py         # 删除
├── api_key.py            # 删除
└── factory.py            # 删除（后面会重新实现）
```

**保留**:
```bash
src/df_test_framework/clients/http/auth/signature/
├── strategies.py         # 保留（签名策略）
└── protocols.py          # 保留（签名策略协议）
```

---

#### 1.4 删除旧的配置schema

```bash
# 需要修改的文件
src/df_test_framework/infrastructure/config/schema.py
```

**删除内容**:
- `SignatureInterceptorConfig` (旧版本)
- `TokenInterceptorConfig`
- `AdminAuthInterceptorConfig` (旧版本)
- `CustomInterceptorConfig` (旧版本)

**注意**: 后面会重新实现这些Config类

---

### Phase 2: 实现核心抽象 🏗️

**目标**: 实现Request/Response/Interceptor/InterceptorChain

#### 2.1 创建Request对象

```bash
# 新文件
src/df_test_framework/clients/http/core/request.py
```

```python
"""HTTP请求对象（不可变）"""
from dataclasses import dataclass, field, replace
from typing import Dict, Any, Optional

@dataclass(frozen=True)
class Request:
    """HTTP请求对象

    不可变设计：
    - 避免拦截器互相影响
    - 易于调试
    - 支持并发
    """
    method: str
    url: str
    headers: Dict[str, str] = field(default_factory=dict)
    params: Dict[str, Any] = field(default_factory=dict)
    json: Optional[Dict[str, Any]] = None
    data: Optional[Any] = None

    # 上下文（拦截器间传递数据）
    context: Dict[str, Any] = field(default_factory=dict)

    def with_header(self, key: str, value: str) -> "Request":
        """返回添加了新header的Request对象"""
        new_headers = {**self.headers, key: value}
        return replace(self, headers=new_headers)

    def with_headers(self, headers: Dict[str, str]) -> "Request":
        """返回合并了headers的Request对象"""
        new_headers = {**self.headers, **headers}
        return replace(self, headers=new_headers)

    def with_context(self, key: str, value: Any) -> "Request":
        """设置context值"""
        new_context = {**self.context, key: value}
        return replace(self, context=new_context)
```

---

#### 2.2 创建Response对象

```bash
# 新文件
src/df_test_framework/clients/http/core/response.py
```

```python
"""HTTP响应对象（不可变）"""
from dataclasses import dataclass, field, replace
from typing import Dict, Any, Optional

@dataclass(frozen=True)
class Response:
    """HTTP响应对象"""
    status_code: int
    headers: Dict[str, str]
    body: str
    json_data: Optional[Dict[str, Any]] = None

    # 继承request的context
    context: Dict[str, Any] = field(default_factory=dict)

    def with_context(self, key: str, value: Any) -> "Response":
        """设置context值"""
        new_context = {**self.context, key: value}
        return replace(self, context=new_context)
```

---

#### 2.3 创建Interceptor接口

```bash
# 新文件
src/df_test_framework/clients/http/core/interceptor.py
```

```python
"""拦截器接口"""
from abc import ABC
from typing import Optional
from .request import Request
from .response import Response

class Interceptor(ABC):
    """拦截器基类

    简单的生命周期钩子：
    - before_request: 请求前处理
    - after_response: 响应后处理
    - on_error: 错误处理
    """

    name: str = ""
    priority: int = 100

    def before_request(self, request: Request) -> Optional[Request]:
        """请求前处理

        Args:
            request: 原始请求对象

        Returns:
            - None: 不修改请求
            - Request: 修改后的新请求对象
        """
        return None

    def after_response(self, response: Response) -> Optional[Response]:
        """响应后处理

        Args:
            response: 原始响应对象

        Returns:
            - None: 不修改响应
            - Response: 修改后的新响应对象
        """
        return None

    def on_error(self, error: Exception, request: Request) -> None:
        """错误处理（可选）

        Args:
            error: 异常对象
            request: 请求对象
        """
        pass


class BaseInterceptor(Interceptor):
    """拦截器便捷基类"""

    def __init__(self, name: Optional[str] = None, priority: int = 100):
        self.name = name or self.__class__.__name__
        self.priority = priority


class InterceptorAbort(Exception):
    """拦截器主动终止请求的异常"""
    pass
```

---

#### 2.4 创建InterceptorChain

```bash
# 新文件
src/df_test_framework/clients/http/core/chain.py
```

```python
"""拦截器执行链"""
from typing import List
from loguru import logger

from .interceptor import Interceptor, InterceptorAbort
from .request import Request
from .response import Response


class InterceptorChain:
    """拦截器执行链

    责任链模式：
    - 自动按priority排序
    - 支持短路（InterceptorAbort）
    - 洋葱模型（响应拦截器逆序执行）
    """

    def __init__(self, interceptors: List[Interceptor] = None):
        self.interceptors = interceptors or []
        self._sort()

    def add(self, interceptor: Interceptor) -> None:
        """添加拦截器"""
        self.interceptors.append(interceptor)
        self._sort()

    def _sort(self) -> None:
        """按priority排序（数字越小越先执行）"""
        self.interceptors.sort(key=lambda i: i.priority)

    def execute_before_request(self, request: Request) -> Request:
        """执行所有before_request钩子"""
        current_request = request

        for interceptor in self.interceptors:
            try:
                modified_request = interceptor.before_request(current_request)
                if modified_request is not None:
                    current_request = modified_request

                logger.debug(
                    f"[拦截器] {interceptor.name} (priority={interceptor.priority}) "
                    f"执行成功"
                )

            except InterceptorAbort as e:
                logger.warning(
                    f"[拦截器] {interceptor.name} 主动终止请求: {e}"
                )
                raise

            except Exception as e:
                logger.error(
                    f"[拦截器] {interceptor.name} 执行失败: {e}",
                    exc_info=True
                )
                # 默认容错：继续执行下一个拦截器

        return current_request

    def execute_after_response(self, response: Response) -> Response:
        """执行所有after_response钩子（逆序）"""
        current_response = response

        # 响应拦截器逆序执行（洋葱模型）
        for interceptor in reversed(self.interceptors):
            try:
                modified_response = interceptor.after_response(current_response)
                if modified_response is not None:
                    current_response = modified_response

                logger.debug(
                    f"[拦截器] {interceptor.name} 响应处理成功"
                )

            except Exception as e:
                logger.error(
                    f"[拦截器] {interceptor.name} 响应处理失败: {e}",
                    exc_info=True
                )

        return current_response
```

---

### Phase 3: 重构HttpClient 🔧

**目标**: HttpClient使用新的拦截器架构

#### 3.1 修改HttpClient

```bash
# 修改文件
src/df_test_framework/clients/http/rest/httpx/client.py
```

**核心改动**:

```python
from df_test_framework.clients.http.core.request import Request
from df_test_framework.clients.http.core.response import Response
from df_test_framework.clients.http.core.chain import InterceptorChain
from df_test_framework.clients.http.core.interceptor import Interceptor


class HttpClient:
    """HTTP客户端"""

    def __init__(self, base_url: str, **kwargs):
        self.base_url = base_url
        self.client = httpx.Client(base_url=base_url, **kwargs)

        # 🆕 拦截器链
        self.chain = InterceptorChain()

    def use(self, interceptor: Interceptor) -> "HttpClient":
        """添加拦截器（链式调用）

        Example:
            >>> client = HttpClient("http://api.example.com")
            >>> client.use(SignatureInterceptor(secret="xxx"))
            >>> client.use(LogInterceptor())
        """
        self.chain.add(interceptor)
        return self

    @classmethod
    def from_config(cls, config: "HTTPConfig") -> "HttpClient":
        """从配置创建HttpClient

        Args:
            config: HTTP配置对象

        Returns:
            配置好拦截器的HttpClient实例
        """
        from df_test_framework.clients.http.auth.interceptors.factory import (
            InterceptorFactory
        )

        # 创建HttpClient实例
        client = cls(base_url=config.base_url)

        # 从config加载拦截器
        if config.interceptors:
            for interceptor_config in config.interceptors:
                if not interceptor_config.enabled:
                    continue

                interceptor = InterceptorFactory.create(interceptor_config)
                client.use(interceptor)

                logger.info(
                    f"[HttpClient] 加载拦截器: {interceptor.name} "
                    f"(priority={interceptor.priority})"
                )

        return client

    def request(
        self,
        method: str,
        url: str,
        **kwargs
    ) -> Response:
        """发送HTTP请求

        执行流程:
        1. 创建Request对象
        2. 执行before_request拦截器链
        3. 发送HTTP请求
        4. 创建Response对象
        5. 执行after_response拦截器链
        6. 返回Response对象
        """
        # 1. 创建Request对象
        request = Request(
            method=method,
            url=url,
            headers=kwargs.get("headers", {}),
            params=kwargs.get("params", {}),
            json=kwargs.get("json"),
            data=kwargs.get("data"),
            context={"base_url": self.base_url}  # 传递base_url给拦截器
        )

        # 2. 执行before_request拦截器链
        request = self.chain.execute_before_request(request)

        # 3. 发送HTTP请求
        http_response = self.client.request(
            method=request.method,
            url=request.url,
            headers=request.headers,
            params=request.params,
            json=request.json,
            data=request.data,
        )

        # 4. 创建Response对象
        json_data = None
        content_type = http_response.headers.get("content-type", "")
        if "application/json" in content_type:
            try:
                json_data = http_response.json()
            except:
                pass

        response = Response(
            status_code=http_response.status_code,
            headers=dict(http_response.headers),
            body=http_response.text,
            json_data=json_data,
            context=request.context,  # 继承request的context
        )

        # 5. 执行after_response拦截器链
        response = self.chain.execute_after_response(response)

        return response
```

---

### Phase 4: 重构BaseAPI 🔧

**目标**: 删除BaseAPI的拦截器功能

#### 4.1 简化BaseAPI

```bash
# 修改文件
src/df_test_framework/clients/http/rest/httpx/base_api.py
```

**核心改动**:

```python
class BaseAPI:
    """API基类（简化版）

    职责：
    - 管理HttpClient
    - 提供便捷的get/post/put/delete方法
    - 解析响应为Pydantic模型
    - 处理业务错误

    不再负责：
    - ❌ 拦截器管理（移到HttpClient）
    """

    def __init__(self, http_client: HttpClient):
        """初始化API客户端

        Args:
            http_client: HTTP客户端
        """
        self.http_client = http_client

    def get(
        self,
        endpoint: str,
        model: Optional[Type[T]] = None,
        **kwargs
    ) -> Any:
        """GET请求

        Args:
            endpoint: API端点路径
            model: 响应数据模型（可选）
            **kwargs: 其他请求参数

        Returns:
            解析后的响应数据
        """
        url = self._build_url(endpoint)
        response = self.http_client.get(url, **kwargs)
        return self._parse_response(response, model)

    def _build_url(self, endpoint: str) -> str:
        """构建完整URL"""
        if endpoint.startswith(("http://", "https://")):
            return endpoint
        return endpoint.lstrip("/")

    def _parse_response(
        self,
        response: Response,
        model: Optional[Type[T]] = None
    ) -> Any:
        """解析响应

        Args:
            response: Response对象
            model: Pydantic模型（可选）

        Returns:
            解析后的数据
        """
        # 检查业务错误
        self._check_business_error(response)

        # 解析为Pydantic模型
        if model and response.json_data:
            return model(**response.json_data)

        # 返回原始JSON
        return response.json_data

    def _check_business_error(self, response: Response) -> None:
        """检查业务错误（子类可覆盖）"""
        # 默认实现：检查HTTP状态码
        if response.status_code >= 400:
            raise BusinessError(
                message=response.body,
                code=response.status_code
            )
```

---

### Phase 5: 实现新的拦截器 🎨

**目标**: 实现SignatureInterceptor/AdminAuthInterceptor/LogInterceptor

#### 5.1 SignatureInterceptor

```bash
# 新文件
src/df_test_framework/clients/http/auth/interceptors/signature.py
```

```python
"""签名拦截器"""
from typing import Dict, Any
from loguru import logger

from df_test_framework.clients.http.core.interceptor import BaseInterceptor
from df_test_framework.clients.http.core.request import Request
from df_test_framework.clients.http.auth.signature.strategies import (
    MD5SortedValuesStrategy,
    SHA256SortedValuesStrategy,
    HMACSignatureStrategy,
)


class SignatureInterceptor(BaseInterceptor):
    """签名拦截器

    自动为请求添加签名Header
    """

    def __init__(
        self,
        algorithm: str = "md5",
        secret: str = "",
        header_name: str = "X-Sign",
        include_query: bool = True,
        include_body: bool = True,
        include_form: bool = False,
        priority: int = 10,
        name: str = None,
    ):
        super().__init__(name=name or "SignatureInterceptor", priority=priority)
        self.algorithm = algorithm
        self.secret = secret
        self.header_name = header_name
        self.include_query = include_query
        self.include_body = include_body
        self.include_form = include_form

        # 策略模式
        self.strategy = self._create_strategy(algorithm)

    def _create_strategy(self, algorithm: str):
        """根据算法创建签名策略"""
        strategies = {
            "md5": MD5SortedValuesStrategy(),
            "sha256": SHA256SortedValuesStrategy(),
            "hmac-sha256": HMACSignatureStrategy(algorithm="sha256"),
        }
        if algorithm not in strategies:
            raise ValueError(f"不支持的签名算法: {algorithm}")
        return strategies[algorithm]

    def before_request(self, request: Request) -> Request:
        """添加签名"""
        # 1. 提取参数
        params = self._extract_params(request)

        logger.debug(f"[签名拦截器] 待签名参数: {params}")

        # 2. 生成签名
        signature = self.strategy.generate_signature(params, self.secret)

        logger.info(f"[签名拦截器] 已生成签名: {signature[:16]}...")

        # 3. 添加到header
        return request.with_header(self.header_name, signature)

    def _extract_params(self, request: Request) -> Dict[str, Any]:
        """提取请求参数"""
        params = {}

        if self.include_query and request.params:
            params.update(request.params)

        if self.include_body and request.json:
            params.update(request.json)

        if self.include_form and request.data:
            if isinstance(request.data, dict):
                params.update(request.data)

        return params
```

---

#### 5.2 AdminAuthInterceptor

```bash
# 新文件
src/df_test_framework/clients/http/auth/interceptors/admin_auth.py
```

```python
"""Admin认证拦截器"""
from typing import Optional
from loguru import logger

from df_test_framework.clients.http.core.interceptor import BaseInterceptor
from df_test_framework.clients.http.core.request import Request


class AdminAuthInterceptor(BaseInterceptor):
    """Admin认证拦截器

    自动登录获取Token并添加到请求头
    """

    def __init__(
        self,
        login_url: str,
        username: str,
        password: str,
        token_field: str = "data.token",
        header_name: str = "Authorization",
        token_prefix: str = "Bearer",
        cache_enabled: bool = True,
        priority: int = 20,
        name: str = None,
    ):
        super().__init__(name=name or "AdminAuthInterceptor", priority=priority)
        self.login_url = login_url
        self.username = username
        self.password = password
        self.token_field = token_field
        self.header_name = header_name
        self.token_prefix = token_prefix

        # Token缓存
        self._token_cache = None if cache_enabled else None

        logger.info(
            f"[Admin认证拦截器] 已初始化: "
            f"login_url={login_url}, username={username}"
        )

    def before_request(self, request: Request) -> Request:
        """添加Token"""
        # 1. 获取Token
        base_url = request.context.get("base_url", "")
        token = self._get_token(base_url)

        # 2. 添加到header
        token_value = f"{self.token_prefix} {token}" if self.token_prefix else token

        logger.debug(f"[Admin认证] 已添加Authorization Header")

        return request.with_header(self.header_name, token_value)

    def _get_token(self, base_url: str) -> str:
        """获取Token（带缓存）"""
        if self._token_cache:
            logger.debug("[Admin认证] 使用缓存的Token")
            return self._token_cache

        # 调用登录接口
        import httpx
        full_login_url = f"{base_url}{self.login_url}"

        logger.info(f"[Admin认证] 调用登录接口: {full_login_url}")

        try:
            login_response = httpx.post(
                full_login_url,
                json={
                    "username": self.username,
                    "password": self.password,
                },
                timeout=30,
            )
            login_response.raise_for_status()
        except Exception as e:
            logger.error(f"[Admin认证] 登录失败: {e}")
            raise ValueError(f"Admin登录失败: {e}")

        # 提取Token
        data = login_response.json()
        token = data
        for field in self.token_field.split("."):
            if field not in token:
                raise ValueError(f"登录响应中未找到Token字段: {self.token_field}")
            token = token[field]

        self._token_cache = token
        logger.info("[Admin认证] 登录成功，Token已缓存")

        return token
```

---

#### 5.3 LogInterceptor

```bash
# 新文件
src/df_test_framework/clients/http/auth/interceptors/log.py
```

```python
"""日志拦截器"""
from loguru import logger

from df_test_framework.clients.http.core.interceptor import BaseInterceptor
from df_test_framework.clients.http.core.request import Request
from df_test_framework.clients.http.core.response import Response


class LogInterceptor(BaseInterceptor):
    """日志拦截器"""

    def __init__(
        self,
        level: str = "INFO",
        log_request_body: bool = True,
        log_response_body: bool = True,
        max_body_length: int = 500,
        priority: int = 100,
        name: str = None,
    ):
        super().__init__(name=name or "LogInterceptor", priority=priority)
        self.level = level
        self.log_request_body = log_request_body
        self.log_response_body = log_response_body
        self.max_body_length = max_body_length

    def before_request(self, request: Request) -> None:
        """记录请求"""
        body_str = ""
        if self.log_request_body and request.json:
            body_str = str(request.json)[:self.max_body_length]

        logger.log(
            self.level,
            f"→ {request.method} {request.url}",
            extra={
                "headers": request.headers,
                "params": request.params,
                "body": body_str,
            }
        )
        return None  # 不修改请求

    def after_response(self, response: Response) -> None:
        """记录响应"""
        body_str = ""
        if self.log_response_body:
            body_str = response.body[:self.max_body_length]

        logger.log(
            self.level,
            f"← {response.status_code}",
            extra={
                "headers": response.headers,
                "body": body_str,
            }
        )
        return None  # 不修改响应
```

---

### Phase 6: 更新配置系统 ⚙️

**目标**: 更新InterceptorConfig和InterceptorFactory

#### 6.1 更新InterceptorConfig

```bash
# 修改文件
src/df_test_framework/infrastructure/config/schema.py
```

**实现内容**: 参考`CONFIG_AND_INTERCEPTOR_INTEGRATION.md`中的设计

---

#### 6.2 更新InterceptorFactory

```bash
# 新文件
src/df_test_framework/clients/http/auth/interceptors/factory.py
```

**实现内容**: 参考`CONFIG_AND_INTERCEPTOR_INTEGRATION.md`中的设计

---

### Phase 7: 更新导出 📦

**目标**: 更新__init__.py导出新的类

#### 7.1 更新框架主__init__.py

```bash
# 修改文件
src/df_test_framework/__init__.py
```

```python
# HTTP Core
from .clients.http.core.request import Request
from .clients.http.core.response import Response
from .clients.http.core.interceptor import (
    Interceptor,
    BaseInterceptor,
    InterceptorAbort,
)
from .clients.http.core.chain import InterceptorChain

# HTTP Client
from .clients.http.rest.httpx.client import HttpClient
from .clients.http.rest.httpx.base_api import BaseAPI, BusinessError

# Interceptors
from .clients.http.auth.interceptors.signature import SignatureInterceptor
from .clients.http.auth.interceptors.admin_auth import AdminAuthInterceptor
from .clients.http.auth.interceptors.log import LogInterceptor

# Interceptor Configs
from .infrastructure.config.schema import (
    InterceptorConfig,
    SignatureInterceptorConfig,
    AdminAuthInterceptorConfig,
    LogInterceptorConfig,
    CustomInterceptorConfig,
)

# ... 其他导出
```

---

### Phase 8: 测试验证 ✅

**目标**: 确保所有测试通过

#### 8.1 运行框架测试

```bash
cd D:\Git\DF\qa\test-framework
uv run pytest tests/ -v
```

**预期**:
- 删除BaseAPI拦截器相关测试
- 添加新的Request/Response/Interceptor测试
- 添加InterceptorChain测试
- 更新HttpClient测试

---

#### 8.2 更新gift-card-test项目

```bash
# 修改文件
D:\Git\DF\qa\gift-card-test\src\gift_card_test\fixtures\apis.py
```

**改动**:

```python
# 删除旧的拦截器fixture
# ❌ 删除 signature_config
# ❌ 删除 signature_interceptor
# ❌ 删除 create_admin_auth_interceptor
# ❌ 删除 admin_auth_interceptor

# 简化API fixtures
@pytest.fixture
def master_card_api(http_client) -> MasterCardAPI:
    """Master系统卡片API - 自动应用签名"""
    return MasterCardAPI(http_client)  # ✅ 零代码

@pytest.fixture
def admin_order_api(http_client) -> AdminOrderAPI:
    """Admin系统订单API - 自动应用认证"""
    return AdminOrderAPI(http_client)  # ✅ 零代码
```

```bash
# 修改文件
D:\Git\DF\qa\gift-card-test\src\gift_card_test\config\settings.py
```

**取消注释自动配置**:

```python
http: HTTPConfig = Field(
    default_factory=lambda: HTTPConfig(
        base_url=os.getenv("APP_HTTP__BASE_URL", "http://47.94.57.99:8088/api"),
        interceptors=[
            # 🆕 启用自动配置
            SignatureInterceptorConfig(
                type="signature",
                enabled=True,
                priority=10,
                algorithm="md5",
                secret=os.getenv("BUSINESS_APP_SECRET", "TU3PxhJxKW8BqobiMDjNaf9HdXW5udN6"),
                header_name="X-Sign",
            ),
            AdminAuthInterceptorConfig(
                type="admin_auth",
                enabled=True,
                priority=20,
                login_url="/admin/auth/login",
                username=os.getenv("BUSINESS_ADMIN_USERNAME", "admin"),
                password=os.getenv("BUSINESS_ADMIN_PASSWORD", "admin123"),
                token_field="data.token",
                header_name="Authorization",
                token_prefix="Bearer",
            ),
        ],
    )
)
```

```bash
# 修改文件
D:\Git\DF\qa\gift-card-test\conftest.py
```

```python
@pytest.fixture(scope="session")
def http_client(settings):
    """创建HTTP客户端（自动加载拦截器）"""
    # 🆕 使用from_config加载拦截器
    return HttpClient.from_config(settings.http)
```

---

#### 8.3 运行gift-card-test测试

```bash
cd D:\Git\DF\qa\gift-card-test
uv run pytest tests/api/ -v
```

---

## 📊 实施检查清单

### Phase 1: 清理 ✅
- [ ] 删除BaseAPI拦截器代码
- [ ] 删除HttpClient旧拦截器代码
- [ ] 删除旧的拦截器实现文件
- [ ] 删除旧的InterceptorConfig

### Phase 2: 核心抽象 ✅
- [ ] 实现Request对象
- [ ] 实现Response对象
- [ ] 实现Interceptor接口
- [ ] 实现InterceptorChain

### Phase 3: 重构HttpClient ✅
- [ ] 添加chain属性
- [ ] 实现use()方法
- [ ] 实现from_config()类方法
- [ ] 重构request()方法

### Phase 4: 重构BaseAPI ✅
- [ ] 删除拦截器相关代码
- [ ] 简化__init__()
- [ ] 简化get/post/put/delete()

### Phase 5: 实现拦截器 ✅
- [ ] 实现SignatureInterceptor
- [ ] 实现AdminAuthInterceptor
- [ ] 实现LogInterceptor

### Phase 6: 配置系统 ✅
- [ ] 更新InterceptorConfig
- [ ] 实现InterceptorFactory
- [ ] 更新HTTPConfig

### Phase 7: 导出 ✅
- [ ] 更新框架__init__.py
- [ ] 更新文档

### Phase 8: 测试 ✅
- [ ] 框架测试通过
- [ ] gift-card-test测试通过
- [ ] 性能测试（确保overhead <1%）

---

## 🎯 成功标准

1. ✅ 所有框架测试通过（317/317）
2. ✅ gift-card-test所有测试通过
3. ✅ 没有重复执行拦截器的问题
4. ✅ 配置系统正常工作
5. ✅ 性能影响 <1%
6. ✅ 代码简洁清晰

---

**准备开始实施！**
