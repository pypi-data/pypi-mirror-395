# 调试指南

> **版本**: v3.17.0 | **更新**: 2025-12-05

本文档提供DF Test Framework的调试技巧和工具使用方法。

## 📋 目录

- [日志调试](#日志调试)
- [Python调试器](#python调试器)
- [HTTP请求调试](#http请求调试)
- [数据库查询调试](#数据库查询调试)
- [事件系统调试](#事件系统调试) ⚡ v3.17+
- [Allure报告调试](#allure报告调试) ⚡ v3.17+
- [测试隔离调试](#测试隔离调试)
- [扩展调试](#扩展调试)
- [IDE集成调试](#ide集成调试)

## 📝 日志调试

### 配置日志级别

#### 方法1: 通过Settings配置

```python
from df_test_framework import FrameworkSettings, LoggingConfig
from pydantic import Field

class MySettings(FrameworkSettings):
    logging: LoggingConfig = Field(default_factory=lambda: LoggingConfig(
        level="DEBUG",          # DEBUG, INFO, WARNING, ERROR
        format="json",          # json, text
        output="stdout"         # stdout, file
    ))
```

#### 方法2: 通过环境变量

```bash
# .env
DF_LOGGING__LEVEL=DEBUG
DF_LOGGING__FORMAT=text
```

#### 方法3: 运行时修改

```python
import logging

# 修改框架日志级别
logging.getLogger("df_test_framework").setLevel(logging.DEBUG)

# 修改特定模块日志级别
logging.getLogger("df_test_framework.core.http").setLevel(logging.DEBUG)
```

### 查看不同组件的日志

```python
def test_with_detailed_logging(runtime):
    logger = runtime.logger

    # 记录不同级别的日志
    logger.debug("调试信息")
    logger.info("普通信息")
    logger.warning("警告信息")
    logger.error("错误信息")

    # 结构化日志（JSON格式）
    logger.info(
        "用户登录",
        extra={
            "user_id": 123,
            "username": "testuser",
            "ip": "192.168.1.1"
        }
    )
```

### HTTP请求日志

HttpClient会自动记录请求和响应：

```python
# 自动记录的日志内容
def test_http_logging(http_client, runtime):
    runtime.settings.logging.level = "DEBUG"

    response = http_client.post("/api/users", json={
        "username": "testuser",
        "password": "secret123"
    })

    # 日志输出示例:
    # [DEBUG] HTTP Request: POST /api/users
    # [DEBUG] Request Headers: {'Content-Type': 'application/json', ...}
    # [DEBUG] Request Body: {"username": "testuser", "password": "***SANITIZED***"}
    # [DEBUG] Response Status: 200
    # [DEBUG] Response Body: {"id": 1, "username": "testuser"}
```

**自定义日志**:

```python
class VerboseHttpClient(HttpClient):
    def request(self, method: str, url: str, **kwargs):
        self._logger.info(f"➡️  {method} {url}")
        self._logger.debug(f"Request kwargs: {kwargs}")

        start_time = time.time()
        response = super().request(method, url, **kwargs)
        duration = time.time() - start_time

        self._logger.info(
            f"⬅️  {method} {url} - {response.status_code} ({duration:.3f}s)"
        )

        return response
```

### 数据库查询日志

#### 方法1: SQLAlchemy echo

```python
from sqlalchemy import create_engine

class DatabaseConfig(BaseModel):
    url: str = "postgresql://..."
    echo: bool = True  # ← 启用SQL日志

# 日志输出示例:
# [DEBUG] SELECT * FROM users WHERE id = 1
# [DEBUG] INSERT INTO users (username, email) VALUES ('test', 'test@example.com')
```

#### 方法2: 自定义查询日志

```python
class LoggingDatabase(Database):
    def execute(self, query: str, params: dict = None):
        self.logger.debug(f"SQL: {query}")
        self.logger.debug(f"Params: {params}")

        start_time = time.time()
        result = super().execute(query, params)
        duration = time.time() - start_time

        self.logger.debug(f"Query executed in {duration:.3f}s")

        return result
```

### 日志过滤

**只查看特定组件的日志**:

```bash
# 只显示HTTP相关日志
pytest tests/ --log-cli-level=DEBUG --log-cli-format="%(message)s" 2>&1 | grep "HTTP"

# 只显示数据库相关日志
pytest tests/ --log-cli-level=DEBUG 2>&1 | grep -i "sql\|database"
```

**Python代码过滤**:

```python
import logging

# 创建过滤器
class ComponentFilter(logging.Filter):
    def __init__(self, component):
        self.component = component

    def filter(self, record):
        return self.component in record.name

# 应用过滤器
handler = logging.StreamHandler()
handler.addFilter(ComponentFilter("http"))
logging.getLogger().addHandler(handler)
```

## 🐛 Python调试器

### pdb - Python内置调试器

#### 基础使用

```python
def test_user_creation(http_client, database):
    # 设置断点
    import pdb; pdb.set_trace()

    response = http_client.post("/api/users", json={"username": "test"})

    # 执行到这里会暂停，可以交互式调试
```

**常用pdb命令**:

```
(Pdb) h          # 显示帮助
(Pdb) l          # 列出当前代码
(Pdb) n          # 下一行
(Pdb) s          # 进入函数
(Pdb) c          # 继续执行
(Pdb) p variable # 打印变量
(Pdb) pp obj     # 美化打印
(Pdb) w          # 显示调用栈
(Pdb) q          # 退出调试
```

**示例调试会话**:

```python
def test_debug_example(http_client):
    import pdb; pdb.set_trace()

    response = http_client.get("/api/users/1")
    user = response.json()

# 调试会话:
(Pdb) l                           # 列出代码
(Pdb) p response.status_code      # 打印状态码: 200
(Pdb) pp response.json()          # 美化打印JSON
{
    'id': 1,
    'username': 'john',
    'email': 'john@example.com'
}
(Pdb) user['username']            # 访问字典: 'john'
(Pdb) c                           # 继续执行
```

### ipdb - 增强版pdb

**安装**:
```bash
pip install ipdb
```

**使用**:
```python
def test_with_ipdb(http_client):
    import ipdb; ipdb.set_trace()  # 彩色输出、自动补全

    response = http_client.get("/api/users")
```

### breakpoint() - Python 3.7+

```python
def test_with_breakpoint(http_client):
    breakpoint()  # 等价于 import pdb; pdb.set_trace()

    response = http_client.get("/api/users")
```

**配置默认调试器**:
```bash
# 使用ipdb
export PYTHONBREAKPOINT=ipdb.set_trace

# 禁用breakpoint
export PYTHONBREAKPOINT=0
```

### 条件断点

```python
def test_conditional_breakpoint(http_client):
    for i in range(100):
        response = http_client.get(f"/api/users/{i}")

        # 只在特定条件下暂停
        if response.status_code != 200:
            import pdb; pdb.set_trace()

        assert response.status_code == 200
```

### Post-mortem调试

**测试失败后进入调试器**:

```bash
# pytest --pdb: 测试失败时自动进入pdb
pytest --pdb tests/test_users.py

# pytest --pdbcls: 使用ipdb
pytest --pdb --pdbcls=IPython.terminal.debugger:Pdb tests/
```

**代码中使用**:

```python
import sys

def test_with_postmortem(http_client):
    try:
        response = http_client.get("/api/users/999")
        assert response.status_code == 200
    except AssertionError:
        # 进入post-mortem调试
        import pdb
        pdb.post_mortem(sys.exc_info()[2])
```

## 🌐 HTTP请求调试

### 查看原始请求/响应

```python
def test_inspect_http(http_client, runtime):
    # 启用详细日志
    runtime.settings.logging.level = "DEBUG"

    response = http_client.post(
        "/api/users",
        json={"username": "test"},
        headers={"X-Custom-Header": "value"}
    )

    # 查看请求详情
    print(f"Request URL: {response.request.url}")
    print(f"Request Method: {response.request.method}")
    print(f"Request Headers: {dict(response.request.headers)}")

    # 查看响应详情
    print(f"Response Status: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Body: {response.text}")
```

### 使用HTTP代理调试

**配置代理（如Fiddler、Charles）**:

```python
class MySettings(FrameworkSettings):
    http: HTTPConfig = Field(default_factory=lambda: HTTPConfig(
        proxies={
            "http://": "http://localhost:8888",
            "https://": "http://localhost:8888"
        }
    ))

# 或运行时配置
http_client._client.proxies = {
    "http://": "http://localhost:8888",
    "https://": "http://localhost:8888"
}
```

**查看代理中的请求**:
1. 启动Fiddler（默认端口8888）
2. 运行测试
3. 在Fiddler中查看所有HTTP请求/响应

### Mock HTTP响应

**使用pytest-httpx**:

```bash
pip install pytest-httpx
```

```python
import pytest
from httpx import Response

def test_with_mock_http(httpx_mock):
    # Mock响应
    httpx_mock.add_response(
        url="http://api.example.com/users/1",
        json={"id": 1, "username": "mocked_user"},
        status_code=200
    )

    http = HttpClient(base_url="http://api.example.com")
    response = http.get("/users/1")

    assert response.json()["username"] == "mocked_user"
```

### 保存请求/响应到文件

```python
import json

def test_save_http_artifacts(http_client, tmp_path):
    response = http_client.get("/api/users/1")

    # 保存请求
    request_file = tmp_path / "request.json"
    request_file.write_text(json.dumps({
        "method": response.request.method,
        "url": str(response.request.url),
        "headers": dict(response.request.headers)
    }, indent=2))

    # 保存响应
    response_file = tmp_path / "response.json"
    response_file.write_text(json.dumps({
        "status_code": response.status_code,
        "headers": dict(response.headers),
        "body": response.json()
    }, indent=2))

    print(f"Artifacts saved to: {tmp_path}")
```

## 🗄️ 数据库查询调试

### 打印生成的SQL

```python
def test_inspect_sql(database):
    from sqlalchemy import text

    query = text("""
        SELECT u.*, COUNT(o.id) as order_count
        FROM users u
        LEFT JOIN orders o ON u.id = o.user_id
        WHERE u.status = :status
        GROUP BY u.id
    """)

    # 查看编译后的SQL
    compiled = query.compile(compile_kwargs={"literal_binds": True})
    print(f"SQL: {compiled}")

    result = database.execute(query, {"status": "active"})
```

### 查看查询计划

**PostgreSQL**:

```python
def test_explain_query(database):
    result = database.execute("""
        EXPLAIN ANALYZE
        SELECT * FROM users WHERE email LIKE '%@example.com'
    """)

    for row in result:
        print(row[0])

# 输出示例:
# Seq Scan on users  (cost=0.00..15.50 rows=100 width=100)
#   Filter: (email ~~ '%@example.com'::text)
```

**MySQL**:

```python
def test_explain_mysql(database):
    result = database.execute("""
        EXPLAIN
        SELECT * FROM users WHERE email LIKE '%@example.com'
    """)

    for row in result:
        print(dict(row))
```

### 监控慢查询

```python
from df_test_framework.extensions import hookimpl
import time

class SlowQueryLogger:
    def __init__(self, threshold=0.5):
        self.threshold = threshold

    @hookimpl
    def df_post_bootstrap(self, runtime):
        db = runtime.database()
        original_execute = db.execute

        def logged_execute(query, params=None):
            start = time.time()
            result = original_execute(query, params)
            duration = time.time() - start

            if duration > self.threshold:
                runtime.logger.warning(
                    f"🐌 慢查询 ({duration:.3f}s): {query[:100]}"
                )

            return result

        db.execute = logged_execute

# 使用
runtime = Bootstrap().with_plugin(SlowQueryLogger(0.5)).build().run()
```

### 查看数据库状态

```python
def test_database_stats(database):
    # PostgreSQL连接数
    result = database.execute("""
        SELECT count(*) as connections
        FROM pg_stat_activity
        WHERE datname = current_database()
    """).first()
    print(f"Active connections: {result.connections}")

    # 表大小
    result = database.execute("""
        SELECT
            pg_size_pretty(pg_total_relation_size('users')) as size
    """).first()
    print(f"Users table size: {result.size}")
```

## 📡 事件系统调试

> ⚡ **v3.17.0 新特性**: 事件关联、OpenTelemetry 追踪、测试隔离

### 调试事件发布和订阅

```python
from df_test_framework import EventBus, HttpRequestStartEvent, HttpRequestEndEvent

def test_debug_events():
    """调试事件流"""
    bus = EventBus()
    events_log = []

    # 订阅所有 HTTP 事件并记录
    @bus.on(HttpRequestStartEvent)
    def on_start(event):
        events_log.append(("START", event.url, event.event_id, event.correlation_id))
        print(f"[START] {event.url}")
        print(f"  event_id: {event.event_id}")
        print(f"  correlation_id: {event.correlation_id}")

    @bus.on(HttpRequestEndEvent)
    def on_end(event):
        events_log.append(("END", event.url, event.event_id, event.correlation_id))
        print(f"[END] {event.url} - {event.status_code}")
        print(f"  event_id: {event.event_id}")
        print(f"  correlation_id: {event.correlation_id}")
        print(f"  duration: {event.duration}s")

    # 发起请求
    client = HttpClient(base_url="https://api.example.com", event_bus=bus)
    response = client.get("/users")

    # 验证事件
    assert len(events_log) == 2  # START + END
    start_event = events_log[0]
    end_event = events_log[1]

    # 验证关联 ID 相同
    assert start_event[3] == end_event[3]  # correlation_id
```

### 调试事件关联（correlation_id）

```python
def test_trace_request_lifecycle():
    """追踪完整请求生命周期"""
    bus = EventBus()
    request_map = {}

    @bus.on(HttpRequestStartEvent)
    def on_start(event):
        request_map[event.correlation_id] = {
            "url": event.url,
            "start_time": event.timestamp,
            "start_event_id": event.event_id,
        }
        print(f"[{event.correlation_id}] Request started: {event.url}")

    @bus.on(HttpRequestEndEvent)
    def on_end(event):
        if event.correlation_id in request_map:
            req = request_map[event.correlation_id]
            duration = (event.timestamp - req["start_time"]).total_seconds()
            print(f"[{event.correlation_id}] Request completed in {duration}s")
            print(f"  Start Event ID: {req['start_event_id']}")
            print(f"  End Event ID: {event.event_id}")
        else:
            print(f"[WARNING] Unmatched END event: {event.correlation_id}")

    client = HttpClient(base_url="https://api.example.com", event_bus=bus)
    client.get("/users")
```

### 调试 OpenTelemetry 追踪

```python
from opentelemetry import trace

def test_debug_otel_tracing():
    """调试 OpenTelemetry 追踪信息"""
    bus = EventBus()
    tracer = trace.get_tracer(__name__)

    @bus.on(HttpRequestEndEvent)
    def on_request(event):
        print(f"Request: {event.url}")
        print(f"  Trace ID: {event.trace_id}")  # W3C TraceContext 格式
        print(f"  Span ID: {event.span_id}")
        print(f"  Format: 32-hex trace_id, 16-hex span_id")

        # 验证格式
        if event.trace_id:
            assert len(event.trace_id) == 32  # 32 字符十六进制
        if event.span_id:
            assert len(event.span_id) == 16   # 16 字符十六进制

    # 在 Span 上下文中发起请求
    with tracer.start_as_current_span("test-request") as span:
        client = HttpClient(base_url="https://api.example.com", event_bus=bus)
        response = client.get("/users")
        # ✅ 事件自动包含当前 Span 的 trace_id 和 span_id
```

### 调试测试隔离

```python
from df_test_framework.infrastructure.events import set_test_event_bus, EventBus

def test_event_isolation():
    """验证事件不会跨测试泄漏"""
    # 创建测试专用的 EventBus
    test_bus = EventBus()
    set_test_event_bus(test_bus)

    event_count = [0]

    @test_bus.on(HttpRequestEndEvent)
    def count_requests(event):
        event_count[0] += 1
        print(f"Test-specific event: {event.url}")

    # 这些请求只会触发当前测试的订阅者
    client = HttpClient(base_url="https://api.example.com")
    client.get("/users")

    assert event_count[0] == 1
    print("✅ Events are properly isolated to this test")
```

## 📊 Allure报告调试

> ⚡ **v3.17.0 新特性**: AllureObserver 自动集成

### 自动记录 HTTP 请求到 Allure

```python
def test_with_allure_debug(allure_observer, http_client):
    """使用 allure_observer 自动记录所有请求

    只需注入 allure_observer fixture，无需手动附加。
    """
    # 发起请求
    response = http_client.get("/users/123")

    # ✅ 以下内容已自动记录到 Allure:
    # - 请求方法、URL、Headers、Body
    # - 响应状态码、Headers、Body
    # - OpenTelemetry trace_id/span_id
    # - 响应时间

    assert response.status_code == 200

    # 可以手动添加额外附件
    import allure
    allure.attach("额外信息", "调试数据", allure.attachment_type.TEXT)
```

### 调试 Allure 附件

```python
import allure
from df_test_framework.testing.plugins import attach_json

def test_allure_attachments(allure_observer, http_client):
    """调试 Allure 附件功能"""

    # 附加 JSON 数据
    test_data = {"user_id": 123, "username": "test"}
    attach_json(test_data, name="测试数据")

    # 附加文本
    allure.attach("调试信息", "详细日志", allure.attachment_type.TEXT)

    # 附加 HTML
    allure.attach(
        "<h1>调试报告</h1><p>详细信息...</p>",
        "HTML报告",
        allure.attachment_type.HTML
    )

    # 发起请求（自动记录）
    response = http_client.post("/users", json=test_data)

    # 验证 Allure 报告生成
    # allure serve allure-results
```

### 查看完整的请求/响应详情

```python
def test_verbose_http_logging(allure_observer, http_client):
    """Allure 自动记录完整的请求和响应详情"""

    # 发起请求
    response = http_client.post(
        "/api/users",
        json={"username": "test", "password": "secret"},
        headers={"X-Custom-Header": "value"}
    )

    # ✅ Allure 报告中将包含:
    # 1. 请求步骤:
    #    - Method: POST
    #    - URL: /api/users
    #    - Headers: {...}
    #    - Body: {"username": "test", "password": "***"}  # 敏感字段已脱敏
    #
    # 2. 响应步骤:
    #    - Status: 201
    #    - Headers: {...}
    #    - Body: {"id": 1, "username": "test"}
    #
    # 3. 追踪信息（如果有）:
    #    - trace_id: 4bf92f3577b34da6a3ce929d0e0e4736
    #    - span_id: 00f067aa0ba902b7
    #
    # 4. 时间信息:
    #    - Duration: 0.234s

    assert response.status_code == 201
```

### Allure 命令行调试

```bash
# 运行测试并生成 Allure 报告
pytest --alluredir=allure-results

# 查看报告
allure serve allure-results

# 生成静态 HTML 报告
allure generate allure-results -o allure-report --clean

# 打开静态报告
# Windows
start allure-report/index.html

# macOS/Linux
open allure-report/index.html
```

## 🔬 测试隔离调试

### 检测测试间数据污染

```python
@pytest.fixture(autouse=True)
def verify_clean_state(database):
    """每个测试前后验证数据库状态"""

    # 测试前
    before_count = database.execute("SELECT COUNT(*) FROM users").scalar()
    print(f"Users before test: {before_count}")

    yield

    # 测试后
    after_count = database.execute("SELECT COUNT(*) FROM users").scalar()
    print(f"Users after test: {after_count}")

    if after_count != before_count:
        print(f"⚠️  数据污染检测: 用户数量变化 {before_count} → {after_count}")
```

### 隔离测试运行

```bash
# 单独运行某个测试
pytest tests/test_users.py::test_create_user -v

# 运行失败的测试
pytest --lf  # last-failed

# 先运行失败的，再运行其他
pytest --ff  # failed-first

# 随机顺序运行（检测依赖）
pytest --random-order tests/
```

### 检测共享状态

```python
# 检测全局状态
import gc

def test_no_global_state():
    """确保没有意外的全局状态"""

    # 运行一些操作
    runtime = Bootstrap().build().run()
    http = runtime.http_client()
    http.get("/api/users")
    runtime.close()

    # 检查对象是否被正确释放
    gc.collect()
    objects = gc.get_objects()

    http_clients = [obj for obj in objects if isinstance(obj, HttpClient)]
    print(f"HttpClient instances: {len(http_clients)}")

    assert len(http_clients) == 0, "HttpClient未被释放"
```

## 🔌 扩展调试

### 查看已加载的扩展

```python
def test_list_extensions(runtime):
    if runtime.extensions:
        plugins = runtime.extensions.manager.get_plugins()
        print(f"Loaded plugins: {len(plugins)}")

        for plugin in plugins:
            print(f"  - {plugin.__class__.__name__}")

            # 查看Hook实现
            hooks = [
                name for name in dir(plugin)
                if name.startswith('df_')
            ]
            print(f"    Hooks: {hooks}")
```

### 调试Hook调用

```python
class DebugExtension:
    @hookimpl
    def df_config_sources(self, settings_cls):
        print(f"🔧 df_config_sources called with {settings_cls.__name__}")
        import traceback
        traceback.print_stack()
        return []

    @hookimpl
    def df_providers(self, settings, logger):
        print(f"🔧 df_providers called")
        print(f"   Settings: {settings.__class__.__name__}")
        print(f"   Logger: {logger}")
        return {}

    @hookimpl
    def df_post_bootstrap(self, runtime):
        print(f"🔧 df_post_bootstrap called")
        print(f"   Runtime providers: {list(runtime.providers._providers.keys())}")
```

### 验证Hook执行顺序

```python
execution_order = []

class Plugin1:
    @hookimpl
    def df_post_bootstrap(self, runtime):
        execution_order.append("Plugin1")

class Plugin2:
    @hookimpl
    def df_post_bootstrap(self, runtime):
        execution_order.append("Plugin2")

runtime = (
    Bootstrap()
    .with_plugin(Plugin1())
    .with_plugin(Plugin2())
    .build()
    .run()
)

print(f"Execution order: {execution_order}")
# 输出: ['Plugin1', 'Plugin2']
```

## 💻 IDE集成调试

### VSCode调试配置

**.vscode/launch.json**:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Pytest Current File",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": [
                "${file}",
                "-v",
                "-s"
            ],
            "console": "integratedTerminal",
            "justMyCode": false
        },
        {
            "name": "Pytest with Coverage",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": [
                "tests/",
                "--cov=src",
                "--cov-report=html"
            ],
            "console": "integratedTerminal"
        }
    ]
}
```

**使用方法**:
1. 在测试文件中设置断点（点击行号左侧）
2. 按F5或点击"Run and Debug"
3. 选择"Pytest Current File"
4. 代码会在断点处暂停

### PyCharm调试配置

**配置pytest**:
1. Run → Edit Configurations
2. Add New Configuration → Python tests → pytest
3. 设置:
   - Target: Script path
   - Script path: `tests/`
   - Working directory: 项目根目录
   - Additional arguments: `-v -s`

**使用断点**:
1. 在代码行左侧点击设置断点
2. 右键测试函数 → Debug 'test_xxx'
3. 使用调试工具栏控制执行

### 远程调试

**使用debugpy**:

```bash
pip install debugpy
```

```python
# tests/conftest.py
import debugpy

@pytest.fixture(scope="session", autouse=True)
def enable_remote_debugging():
    debugpy.listen(("0.0.0.0", 5678))
    print("⏳ 等待调试器连接...")
    debugpy.wait_for_client()
    print("✅ 调试器已连接")
```

**VSCode连接配置**:

```json
{
    "name": "Attach to Pytest",
    "type": "python",
    "request": "attach",
    "connect": {
        "host": "localhost",
        "port": 5678
    }
}
```

## 🔍 高级调试技巧

### 1. 时间旅行调试

**使用pytest-replay**:

```bash
pip install pytest-replay
```

```bash
# 记录测试执行
pytest --replay-record=session.replay tests/

# 回放测试执行
pytest --replay=session.replay tests/
```

### 2. 内存调试

```python
import tracemalloc

def test_memory_usage(http_client):
    tracemalloc.start()

    # 执行操作
    for i in range(1000):
        response = http_client.get(f"/api/users/{i}")

    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory: {current / 1024 / 1024:.2f} MB")
    print(f"Peak memory: {peak / 1024 / 1024:.2f} MB")

    tracemalloc.stop()
```

### 3. 性能分析

```python
import cProfile
import pstats

def test_with_profiling(http_client):
    profiler = cProfile.Profile()
    profiler.enable()

    # 执行操作
    for i in range(100):
        http_client.get("/api/users")

    profiler.disable()

    # 输出统计
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)  # 显示前10个最慢的函数
```

## 🔗 相关文档

- [常见错误](common-errors.md)
- [性能调优](performance-tuning.md)
- [配置管理](../user-guide/configuration.md)

---

**返回**: [故障排查](README.md) | [文档首页](../README.md)
