# Allure集成设计方案 (v3.5)

> **目标**: 优雅集成Allure Report，提供现代化的测试报告和调试能力

---

## 1. 架构设计

### 1.1 核心理念

```
用户测试代码（零改动）
         ↓
  pytest自动注入
         ↓
  AllureObserver（监听器）
         ↓
  自动记录HTTP/DB/拦截器
         ↓
  生成Allure报告
```

**关键特性**：
- ✅ **零配置** - 用户只需安装allure-pytest
- ✅ **自动记录** - HTTP/DB/拦截器操作自动转为Allure步骤
- ✅ **智能附件** - 失败时自动附加请求/响应详情
- ✅ **兼容现有** - 不影响现有测试代码

### 1.2 组件架构

```python
┌─────────────────────────────────────────────────┐
│          pytest (用户测试)                       │
│  def test_create_user(http_client):             │
│      response = http_client.post("/users", ...) │
│      assert response.status_code == 201         │
└─────────────────────────────────────────────────┘
                    ↓ (自动注入)
┌─────────────────────────────────────────────────┐
│   AllureObserver (观察者模式)                   │
│   - 监听HTTP请求                                │
│   - 监听拦截器执行                              │
│   - 监听DB查询                                  │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│   AllureReporter (报告生成)                     │
│   - 转换为allure.step()                        │
│   - 添加allure.attach()                        │
│   - 生成HTML报告                               │
└─────────────────────────────────────────────────┘
```

---

## 2. 实现方案

### 2.1 AllureObserver（核心）

```python
# src/df_test_framework/testing/observers/allure_observer.py

from typing import Optional, Dict, Any
import allure
import json
from contextvars import ContextVar

# 当前激活的observer（线程安全）
_current_observer: ContextVar[Optional['AllureObserver']] = ContextVar(
    'allure_observer', default=None
)


class AllureObserver:
    """Allure观察者 - 自动记录测试操作到Allure报告

    设计模式：Observer Pattern
    - 监听测试框架的各种事件
    - 自动转换为Allure步骤和附件
    - 零侵入用户代码
    """

    def __init__(self, test_name: str):
        self.test_name = test_name
        self.request_counter = 0
        self.db_query_counter = 0
        self._current_step_context = None

    def start(self):
        """激活observer"""
        _current_observer.set(self)

    def stop(self):
        """停用observer"""
        _current_observer.set(None)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # HTTP相关
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def on_http_request_start(self, request: 'Request') -> str:
        """HTTP请求开始

        Returns:
            request_id: 用于关联后续事件
        """
        self.request_counter += 1
        request_id = f"req-{self.request_counter:03d}"

        # 创建Allure步骤
        step_title = f"🌐 {request.method} {request.url}"
        self._current_step_context = allure.step(step_title)
        self._current_step_context.__enter__()

        # 附加请求详情
        request_details = {
            "method": request.method,
            "url": request.url,
            "headers": self._sanitize_headers(request.headers),
            "params": request.params,
            "body": request.json or request.data,
        }

        allure.attach(
            json.dumps(request_details, indent=2, ensure_ascii=False),
            name="📤 Request",
            attachment_type=allure.attachment_type.JSON
        )

        return request_id

    def on_interceptor_executed(
        self,
        request_id: str,
        interceptor_name: str,
        changes: Dict[str, Any]
    ):
        """拦截器执行完成

        在当前HTTP步骤中添加子步骤
        """
        if not changes:
            return

        # 添加拦截器子步骤
        with allure.step(f"🔧 {interceptor_name}"):
            changes_text = "\n".join(
                f"  • {key}: {value}"
                for key, value in changes.items()
            )
            allure.attach(
                changes_text,
                name="Changes",
                attachment_type=allure.attachment_type.TEXT
            )

    def on_http_request_end(
        self,
        request_id: str,
        response: 'Response',
        duration_ms: float
    ):
        """HTTP请求结束"""
        # 附加响应详情
        response_details = {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": response.body,
            "duration_ms": duration_ms,
        }

        # 根据状态码选择图标
        if response.status_code < 400:
            icon = "✅"
        elif response.status_code < 500:
            icon = "⚠️"
        else:
            icon = "❌"

        allure.attach(
            json.dumps(response_details, indent=2, ensure_ascii=False),
            name=f"{icon} Response ({response.status_code})",
            attachment_type=allure.attachment_type.JSON
        )

        # 退出HTTP步骤
        if self._current_step_context:
            self._current_step_context.__exit__(None, None, None)
            self._current_step_context = None

    def on_http_request_error(
        self,
        request_id: str,
        error: Exception
    ):
        """HTTP请求错误"""
        allure.attach(
            f"Error Type: {type(error).__name__}\n"
            f"Error Message: {str(error)}",
            name="❌ Error",
            attachment_type=allure.attachment_type.TEXT
        )

        # 退出HTTP步骤
        if self._current_step_context:
            self._current_step_context.__exit__(None, None, None)
            self._current_step_context = None

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 数据库相关
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def on_db_query_start(self, query: str, params: Dict[str, Any]):
        """数据库查询开始"""
        self.db_query_counter += 1

        with allure.step(f"🗄️ Query #{self.db_query_counter}"):
            allure.attach(
                query,
                name="SQL",
                attachment_type=allure.attachment_type.TEXT
            )
            if params:
                allure.attach(
                    json.dumps(params, indent=2, ensure_ascii=False),
                    name="Parameters",
                    attachment_type=allure.attachment_type.JSON
                )

    def on_db_query_end(self, result_count: int, duration_ms: float):
        """数据库查询结束"""
        allure.attach(
            f"Result Count: {result_count}\n"
            f"Duration: {duration_ms:.2f}ms",
            name="✅ Result",
            attachment_type=allure.attachment_type.TEXT
        )

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 工具方法
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def _sanitize_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
        """脱敏敏感headers"""
        sanitized = {}
        for key, value in headers.items():
            if key.lower() in ['authorization', 'x-api-key', 'cookie']:
                if len(value) > 20:
                    sanitized[key] = value[:10] + "..." + value[-8:]
                else:
                    sanitized[key] = "***"
            else:
                sanitized[key] = value
        return sanitized


def get_current_observer() -> Optional[AllureObserver]:
    """获取当前激活的observer（供框架内部使用）"""
    return _current_observer.get()
```

### 2.2 pytest fixture自动注入

```python
# src/df_test_framework/testing/fixtures/allure.py

import pytest
import allure
from ..observers.allure_observer import AllureObserver


@pytest.fixture(scope="function", autouse=True)
def _auto_allure_observer(request):
    """自动启用Allure Observer

    autouse=True: 对所有测试自动生效
    """
    # 检查是否安装了allure-pytest
    if not hasattr(allure, 'step'):
        # 未安装allure，跳过
        yield
        return

    # 创建observer
    observer = AllureObserver(test_name=request.node.name)
    observer.start()

    yield observer

    observer.stop()
```

### 2.3 HttpClient集成

```python
# src/df_test_framework/clients/http/rest/httpx/client.py

class HttpClient:
    def request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """发送HTTP请求（v3.5: 集成Allure）"""
        from df_test_framework.testing.observers.allure_observer import (
            get_current_observer
        )

        observer = get_current_observer()
        request_id = None
        start_time = time.time()

        # 1. 创建Request对象
        request_obj = Request(
            method=method,
            url=url,
            headers=kwargs.get('headers', {}),
            params=kwargs.get('params'),
            json=kwargs.get('json'),
            data=kwargs.get('data'),
        )

        # 2. 通知observer: 请求开始
        if observer:
            request_id = observer.on_http_request_start(request_obj)

        # 3. 执行拦截器链
        try:
            modified_request = self.interceptor_chain.execute_before_request(
                request_obj,
                request_id=request_id  # 传递给拦截器链
            )
            if modified_request:
                request_obj = modified_request
        except Exception as e:
            # 通知observer: 错误
            if observer and request_id:
                observer.on_http_request_error(request_id, e)
            raise

        # 4. 发送请求
        try:
            httpx_response = self.client.request(
                method, url,
                headers=dict(request_obj.headers),
                params=request_obj.params,
                json=request_obj.json,
                data=request_obj.data,
            )
        except Exception as e:
            # 通知observer: 错误
            if observer and request_id:
                observer.on_http_request_error(request_id, e)
            raise

        # 5. 通知observer: 请求结束
        if observer and request_id:
            duration_ms = (time.time() - start_time) * 1000
            response_obj = Response(
                status_code=httpx_response.status_code,
                headers=dict(httpx_response.headers),
                body=httpx_response.text,
                json_data=None,  # 稍后处理
            )
            observer.on_http_request_end(request_id, response_obj, duration_ms)

        return httpx_response
```

### 2.4 InterceptorChain集成

```python
# src/df_test_framework/clients/http/core/chain.py

class InterceptorChain:
    def execute_before_request(
        self,
        request: Request,
        request_id: Optional[str] = None
    ) -> Optional[Request]:
        """执行before_request拦截器链（v3.5: 集成Allure）"""
        from df_test_framework.testing.observers.allure_observer import (
            get_current_observer
        )

        observer = get_current_observer()

        for interceptor in self.interceptors:
            original_request = request

            # 执行拦截器
            modified = interceptor.before_request(request)

            # 如果有变化，通知observer
            if observer and request_id and modified:
                changes = self._diff_request(original_request, modified)
                if changes:
                    observer.on_interceptor_executed(
                        request_id,
                        interceptor.name,
                        changes
                    )
                request = modified

        return request

    def _diff_request(
        self,
        original: Request,
        modified: Request
    ) -> Dict[str, Any]:
        """对比请求变化"""
        changes = {}

        # 对比headers
        new_headers = set(modified.headers.keys()) - set(original.headers.keys())
        if new_headers:
            changes["Added Headers"] = {
                k: modified.headers[k] for k in new_headers
            }

        # 对比params
        if modified.params != original.params:
            changes["Modified Params"] = modified.params

        return changes
```

---

## 3. 使用示例

### 3.1 零配置使用

```python
# tests/test_api.py

def test_create_user(http_client):
    """完全零配置 - Allure自动记录"""
    response = http_client.post(
        "/api/users",
        json={"name": "John", "email": "john@example.com"}
    )
    assert response.status_code == 201
```

**生成的Allure报告**：

```
测试步骤:
  🌐 POST /api/users
    📤 Request (附件)
      {
        "method": "POST",
        "url": "/api/users",
        "body": {"name": "John", "email": "john@example.com"}
      }

    🔧 SignatureInterceptor (子步骤)
      • Added Headers: {"X-Sign": "md5_abc..."}

    🔧 TokenInterceptor (子步骤)
      • Added Headers: {"Authorization": "Bearer tok..."}

    ✅ Response (201) (附件)
      {
        "status_code": 201,
        "body": {"id": 123, "name": "John"}
      }
```

### 3.2 手动添加步骤（高级）

```python
import allure

def test_complex_flow(http_client):
    """可以混合使用自动和手动步骤"""

    with allure.step("📋 Step 1: 准备测试数据"):
        test_data = {"name": "John"}
        allure.attach(
            json.dumps(test_data),
            name="Test Data",
            attachment_type=allure.attachment_type.JSON
        )

    # HTTP请求自动记录
    response = http_client.post("/api/users", json=test_data)

    with allure.step("✓ Step 2: 验证结果"):
        assert response.status_code == 201
        user_id = response.json()["id"]
        allure.attach(str(user_id), name="Created User ID")
```

### 3.3 失败时的输出

**终端输出**（简洁）：
```bash
$ pytest tests/test_api.py

tests/test_api.py::test_create_user FAILED                [100%]

========================= FAILURES =========================
test_create_user - AssertionError: assert 400 == 201

📊 查看详细报告：
   allure serve allure-results

1 failed in 0.52s
```

**Allure HTML报告**（详细）：
- 展开失败的测试
- 查看完整的HTTP请求步骤
- 查看请求/响应附件（JSON格式）
- 查看拦截器执行详情

---

## 4. 配置选项

### 4.1 pytest.ini配置

```ini
[pytest]
# Allure结果目录
allure_results_dir = allure-results

# 自动启用Allure observer
df_allure_enabled = true

# 是否记录请求/响应body（大文件时可关闭）
df_allure_attach_bodies = true

# Body最大长度（超过则截断）
df_allure_max_body_length = 10000
```

### 4.2 conftest.py全局配置

```python
# conftest.py

import pytest

@pytest.fixture(scope="session")
def configure_allure():
    """配置Allure行为"""
    from df_test_framework.testing.observers import configure_allure_observer

    configure_allure_observer(
        attach_bodies=True,
        max_body_length=10000,
        sanitize_headers=True,
    )
```

---

## 5. 运行和查看报告

### 5.1 运行测试生成报告

```bash
# 运行测试
pytest tests/ --alluredir=allure-results

# 查看报告（启动本地服务器）
allure serve allure-results

# 或生成静态HTML
allure generate allure-results -o allure-report --clean
```

### 5.2 CI集成

```yaml
# .github/workflows/test.yml

- name: Run tests with Allure
  run: |
    pytest tests/ --alluredir=allure-results

- name: Generate Allure Report
  if: always()
  run: |
    allure generate allure-results -o allure-report --clean

- name: Upload Allure Report
  uses: actions/upload-artifact@v3
  if: always()
  with:
    name: allure-report
    path: allure-report/
```

---

## 6. 优势对比

### 6.1 Before（HTTPDebugger）

```python
def test_api(http_debugger):
    http_debugger.start()  # ❌ 需要手动启动

    response = client.post("/users", ...)

    http_debugger.print_summary()  # ❌ 手动打印
```

**输出**（终端）：
```
[HTTP DEBUG] POST /users
[HTTP DEBUG] Response: 201 ✅
```

### 6.2 After（Allure集成）

```python
def test_api(http_client):
    # ✅ 零配置
    response = http_client.post("/users", ...)
```

**输出**（终端）：
```
tests/test_api.py::test_api PASSED
```

**输出**（Allure报告 - 可视化）：
- 时间线图表
- 请求/响应详情（JSON格式）
- 拦截器执行步骤
- 可搜索、可过滤

---

## 7. 实施计划

### Phase 2: Allure集成 (2天)

**Day 1: 核心实现**
- ✅ Task 2.1: 实现AllureObserver
- ✅ Task 2.2: pytest fixture自动注入
- ✅ Task 2.3: HttpClient集成

**Day 2: 完善和测试**
- ✅ Task 2.4: InterceptorChain集成
- ✅ Task 2.5: 数据库查询集成（可选）
- ✅ Task 2.6: 文档和示例

### 验收标准

- ✅ 零配置即可使用
- ✅ 测试通过时终端简洁
- ✅ Allure报告包含HTTP详情
- ✅ 拦截器操作可见
- ✅ 所有现有测试通过

---

## 8. 扩展性

### 8.1 支持其他组件

```python
# 数据库查询
class Database:
    def query(self, sql: str, params: Dict):
        observer = get_current_observer()

        if observer:
            observer.on_db_query_start(sql, params)

        result = self._execute(sql, params)

        if observer:
            observer.on_db_query_end(len(result), duration_ms)

        return result
```

### 8.2 自定义步骤

```python
# 业务层也可以添加步骤
from df_test_framework.testing.observers import allure_step

@allure_step("创建订单")
def create_order(order_data):
    # 自动作为Allure步骤
    ...
```

---

**总结**：这个方案完美融合pytest生态，提供现代化的可视化报告，零配置使用，完全符合行业最佳实践。
