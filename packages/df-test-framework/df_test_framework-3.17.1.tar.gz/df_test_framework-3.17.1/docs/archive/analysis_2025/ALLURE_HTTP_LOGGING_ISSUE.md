# Allure HTTP 日志缺失问题说明

> **问题**: 使用 BaseAPI 调用时,Allure 报告中缺少 HTTP 请求/响应详情
> **日期**: 2025-12-05
> **框架版本**: df-test-framework v3.16.0

---

## 🔍 问题现象

当使用 BaseAPI 调用 API 时(如 `master_card_api.create_cards()`),Allure 报告中**不会**自动记录 HTTP 请求详情:

```bash
# 运行测试
uv run pytest tests/api/1_master/test_create_cards.py::TestMasterCardCreation::test_create_single_card_success -v

# 生成 Allure 报告
allure serve reports/allure-results
```

**结果**: Allure 报告中没有 HTTP 请求/响应的详细信息(Request/Response 附件)。

---

## 🧐 根本原因分析

### 1. Allure 集成机制

框架的 Allure 集成分为两个部分:

#### 1.1 AllureObserver (观察者模式)

**位置**: `df_test_framework/testing/reporting/allure/observer.py`

```python
class AllureObserver:
    """Allure测试观察者

    通过 EventBus 订阅以下事件:
    - HttpRequestStartEvent  # HTTP 请求开始
    - HttpRequestEndEvent    # HTTP 请求结束
    - DatabaseQueryStartEvent
    - DatabaseQueryEndEvent

    然后记录到 Allure 报告中。
    """

    def on_http_request_start(self, request: "Request") -> str | None:
        """创建 Allure step: 🌐 POST /api/users"""
        # 附加 Request Details JSON
        ...

    def on_http_request_end(self, response: "Response", duration: float):
        """完成 Allure step,附加 Response JSON"""
        ...
```

#### 1.2 自动注入机制

**位置**: `df_test_framework/testing/fixtures/allure.py`

```python
@pytest.fixture(scope="function", autouse=True)
def _auto_allure_observer(request):
    """零配置自动注入 AllureObserver

    - autouse=True: 每个测试自动创建 observer
    - 通过 ContextVar 全局可访问
    - HttpClient/Middleware 调用 observer 记录操作
    """
    observer = AllureObserver(test_name=request.node.name)
    set_current_observer(observer)

    yield observer

    observer.cleanup()
    set_current_observer(None)
```

### 2. HTTP 请求的两种执行路径

#### 路径 1: 使用中间件系统 ✅

**条件**: HttpClient 配置了中间件(`config.middlewares` 不为空)

```python
# HttpClient.request() 方法
def request(self, method: str, url: str, **kwargs) -> httpx.Response:
    # ✅ v3.16.0: 如果配置了中间件,使用中间件系统
    if self._middlewares:
        response = self.request_with_middleware(method, url, **kwargs)
        return self._convert_to_httpx_response(response, request_obj)

    # ❌ 没有中间件,使用基础请求逻辑(不触发 Allure 记录)
    return self._send_without_middleware(method, url, **kwargs)
```

**request_with_middleware() 流程**:

```python
def request_with_middleware(self, method: str, url: str, **kwargs) -> Response:
    # 1. 准备请求对象
    request_obj = self._prepare_request_object(method, url, **kwargs)

    # 2. ✅ 发布事件: HttpRequestStartEvent
    self._publish_event(HttpRequestStartEvent(method=method, url=url))

    # 3. 执行中间件链
    chain = self._build_middleware_chain()
    response = loop.run_until_complete(chain.execute(request_obj))

    # 4. ✅ 发布事件: HttpRequestEndEvent
    self._publish_event(HttpRequestEndEvent(...))

    return response
```

**AllureObserver 订阅事件并记录到 Allure**:

```python
# EventBus 自动调用
observer.on_http_request_start(request)  # 创建 Allure step
observer.on_http_request_end(response)   # 完成 Allure step,附加响应
```

#### 路径 2: 不使用中间件 ❌

**条件**: HttpClient **没有**配置中间件

```python
def _send_without_middleware(self, method: str, url: str, **kwargs):
    """基础请求发送（无中间件）

    ❌ 不发布任何事件
    ❌ AllureObserver 无法捕获
    ❌ Allure 报告中无 HTTP 详情
    """
    full_url = f"{self.base_url}{url}" if not url.startswith("http") else url

    # 直接调用 httpx.client.request()
    response = self.client.request(method, full_url, **kwargs)

    return response  # 直接返回,无事件发布
```

### 3. BaseAPI 的调用链

```python
# 测试代码
master_card_api.create_cards(request)
    ↓
# MasterCardAPI.create_cards()
self.post(endpoint="/master/card/create", json=request)
    ↓
# BaseAPI.post()
response = self.http_client.post(url, **kwargs)
    ↓
# HttpClient.post()
return self.request("POST", url, **kwargs)
    ↓
# HttpClient.request()
if self._middlewares:  # ✅ 走中间件路径(有 Allure 记录)
    return self.request_with_middleware(...)
else:  # ❌ 走基础路径(无 Allure 记录)
    return self._send_without_middleware(...)
```

---

## ✅ 解决方案

### 方案 1: 确保项目配置了中间件(推荐)

**检查**: `src/gift_card_test/config/settings.py`

```python
def create_http_config() -> HTTPConfig:
    return HTTPConfig(
        base_url="https://qifu-mall-api-test.jucai365.com/gift-card/api",
        timeout=30,
        max_retries=3,
        middlewares=[  # ✅ 必须配置中间件
            SignatureMiddlewareConfig(
                enabled=True,
                priority=10,
                algorithm=SignatureAlgorithm.MD5,
                secret="TU3PxhJxKW8BqobiMDjNaf9HdXW5udN6",
                header="X-Sign",
                include_paths=["/master/**", "/h5/**"],
            ),
        ],
    )
```

**验证中间件是否生效**:

```bash
# 运行测试,查看日志
uv run pytest tests/api/1_master/test_create_cards.py::TestMasterCardCreation::test_create_single_card_success -v -s

# 应该看到类似日志:
# [HttpClient] 已加载中间件: type=signature, priority=10, name=SignatureMiddleware
# [HttpClient] 中间件加载完成: total=1
```

### 方案 2: 添加最小的日志中间件

如果不需要签名等功能,可以添加一个最小的日志中间件:

```python
from df_test_framework.infrastructure.config import LoggingMiddlewareConfig

def create_http_config() -> HTTPConfig:
    return HTTPConfig(
        base_url="...",
        middlewares=[
            # 最小中间件配置(仅为触发 Allure 记录)
            LoggingMiddlewareConfig(
                enabled=True,
                priority=50,
                log_request=False,  # 不输出到控制台
                log_response=False,  # 不输出到控制台
            ),
        ],
    )
```

### 方案 3: 框架级别改进(需要框架修改)

**建议框架修改**: 在 `_send_without_middleware()` 中也发布事件

```python
# df_test_framework/capabilities/clients/http/rest/httpx/client.py

def _send_without_middleware(self, method: str, url: str, **kwargs):
    """不使用中间件的基础请求发送

    ✅ 改进: 仍然发布事件,让 AllureObserver 可以记录
    """
    # ✅ 发布请求开始事件
    start_time = time.time()
    self._publish_event(HttpRequestStartEvent(method=method, url=url))

    try:
        full_url = f"{self.base_url}{url}" if not url.startswith("http") else url
        response = self.client.request(method, full_url, **kwargs)

        # ✅ 发布请求完成事件
        duration = time.time() - start_time
        self._publish_event(HttpRequestEndEvent(
            method=method,
            url=url,
            status_code=response.status_code,
            duration=duration,
        ))

        return response

    except Exception as e:
        # ✅ 发布错误事件
        duration = time.time() - start_time
        self._publish_event(HttpRequestErrorEvent(
            method=method,
            url=url,
            error=str(e),
            duration=duration,
        ))
        raise
```

---

## 📊 当前项目状态

### ✅ 已配置中间件

**文件**: `src/gift_card_test/config/settings.py:69`

```python
middlewares=[
    # ✅ 签名中间件配置正确
    SignatureMiddlewareConfig(
        enabled=True,
        priority=10,
        algorithm=SignatureAlgorithm.MD5,
        secret="TU3PxhJxKW8BqobiMDjNaf9HdXW5udN6",
        header="X-Sign",
        include_paths=["/master/**", "/h5/**"],
        exclude_paths=["/health", "/metrics", "/actuator/**"],
    ),
]
```

### ⚠️ 可能的问题

#### 问题 1: 路径过滤导致中间件未生效

**症状**: 配置了中间件,但某些 API 路径仍无 Allure 记录

**原因**: `include_paths` 或 `exclude_paths` 过滤规则不匹配

**示例**:

```python
# 中间件配置
SignatureMiddlewareConfig(
    include_paths=["/master/**", "/h5/**"],  # 只对这些路径生效
)

# ✅ 会记录到 Allure
master_card_api.create_cards(...)  # POST /master/card/create

# ❌ 不会记录到 Allure
admin_template_api.query_templates(...)  # POST /admin/template/query
# 因为 /admin/** 不在 include_paths 中
```

**解决方案**:

```python
# 方式 1: 移除路径过滤(全局生效)
SignatureMiddlewareConfig(
    enabled=True,
    priority=10,
    # include_paths=[],  # 留空或不设置 = 全局生效
    # exclude_paths=[],
)

# 方式 2: 添加 Admin 路径
SignatureMiddlewareConfig(
    include_paths=["/master/**", "/h5/**", "/admin/**"],  # ✅ 包含 admin
)

# 方式 3: 添加单独的日志中间件(无路径限制)
middlewares=[
    SignatureMiddlewareConfig(
        include_paths=["/master/**", "/h5/**"],  # 签名仅对部分路径
    ),
    LoggingMiddlewareConfig(
        enabled=True,
        priority=100,  # 最低优先级
        # 无路径限制,所有请求都触发 Allure 记录
    ),
]
```

#### 问题 2: 中间件优先级和路径包装

**框架逻辑** (`HttpClient._load_middlewares_from_config`):

```python
# 如果中间件有路径规则,会被包装为 PathFilteredMiddleware
if has_path_rules:
    middleware = PathFilteredMiddleware(
        middleware=middleware,
        include_paths=config.include_paths,
        exclude_paths=config.exclude_paths,
    )
```

**PathFilteredMiddleware 的判断逻辑**:

```python
class PathFilteredMiddleware:
    async def __call__(self, request, call_next):
        # 检查路径是否匹配
        if not self._should_apply(request.path):
            # ❌ 不匹配,直接跳过此中间件
            return await call_next(request)

        # ✅ 匹配,执行实际中间件
        return await self.middleware(request, call_next)
```

**关键点**: 如果路径不匹配,中间件链仍然存在(不会退化为 `_send_without_middleware`),但该中间件会被跳过。

**因此**: 只要配置了**任何**中间件,就会走 `request_with_middleware()` 路径,从而触发 EventBus 事件发布。

---

## 🔧 验证步骤

### 1. 检查中间件是否加载

```python
# tests/conftest.py 或任意测试文件
def test_check_middlewares(http_client):
    """检查中间件是否加载"""
    print(f"\n✅ 中间件数量: {len(http_client._middlewares)}")
    for mw in http_client._middlewares:
        print(f"  - {mw.name} (priority={mw.priority})")
```

运行:

```bash
uv run pytest tests/api/1_master/test_create_cards.py::test_check_middlewares -v -s
```

**预期输出**:

```
✅ 中间件数量: 1
  - PathFilteredMiddleware(SignatureMiddleware) (priority=10)
```

### 2. 检查 Allure Observer 是否注入

```python
def test_check_allure_observer():
    """检查 AllureObserver 是否注入"""
    from df_test_framework.testing.reporting.allure import get_current_observer

    observer = get_current_observer()
    print(f"\n✅ AllureObserver: {observer}")
    assert observer is not None, "AllureObserver 未注入"
```

### 3. 手动触发 HTTP 请求并检查 Allure

```bash
# 1. 清理旧报告
rm -rf reports/allure-results

# 2. 运行测试
uv run pytest tests/api/1_master/test_create_cards.py::TestMasterCardCreation::test_create_single_card_success -v --alluredir=reports/allure-results

# 3. 查看 Allure 报告
allure serve reports/allure-results
```

**预期**: 在 Allure 报告中看到:

```
🌐 POST /master/card/create
  ├─ 📤 Request Details (JSON 附件)
  ├─ ⚙️ SignatureMiddleware (sub-step)
  └─ ✅ Response (200) - 234ms (JSON 附件)
```

---

## 📝 总结

### 核心原因

**Allure HTTP 日志依赖中间件系统**:
- ✅ 配置中间件 → 走 `request_with_middleware()` → 发布事件 → AllureObserver 记录
- ❌ 无中间件 → 走 `_send_without_middleware()` → 无事件发布 → AllureObserver 无法记录

### 当前项目状态

- ✅ **已配置 SignatureMiddleware**
- ✅ **应该可以自动记录到 Allure**
- ⚠️ **如果仍然缺失**,检查路径过滤规则

### 推荐配置

```python
# src/gift_card_test/config/settings.py

def create_http_config() -> HTTPConfig:
    return HTTPConfig(
        base_url="...",
        middlewares=[
            # 签名中间件(针对特定路径)
            SignatureMiddlewareConfig(
                enabled=True,
                priority=10,
                algorithm=SignatureAlgorithm.MD5,
                secret="...",
                include_paths=["/master/**", "/h5/**"],
            ),
            # 日志中间件(全局,确保 Allure 记录)
            LoggingMiddlewareConfig(
                enabled=True,
                priority=100,  # 最低优先级,最后执行
                log_request=False,  # 不输出到控制台
                log_response=False,
                # 无路径限制,所有请求都记录到 Allure
            ),
        ],
    )
```

---

**文档创建时间**: 2025-12-05 16:35:00
**下次更新**: 验证问题解决后更新状态