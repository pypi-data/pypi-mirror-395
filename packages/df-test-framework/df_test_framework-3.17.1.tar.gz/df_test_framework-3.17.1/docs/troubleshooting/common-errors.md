# 常见错误与解决方案

本文档列出使用DF Test Framework时的常见错误及其解决方案。

## 📋 目录

- [启动与配置错误](#启动与配置错误)
- [连接与网络错误](#连接与网络错误)
- [数据库错误](#数据库错误)
- [Redis错误](#redis错误)
- [测试执行错误](#测试执行错误)
- [扩展与插件错误](#扩展与插件错误)

## 🚀 启动与配置错误

### 错误1: SettingsAlreadyConfiguredError

**错误信息**:
```
SettingsAlreadyConfiguredError: Settings for namespace 'default' are already configured
```

**原因**: 同一个namespace的Settings被配置了多次

**场景**:
```python
# 错误示例
runtime1 = Bootstrap().with_settings(MySettings).build().run()
runtime2 = Bootstrap().with_settings(MySettings).build().run()  # ❌ 错误
```

**解决方案**:

1. **使用不同的namespace**:
```python
runtime1 = Bootstrap().with_settings(MySettings, namespace="test1").build().run()
runtime2 = Bootstrap().with_settings(MySettings, namespace="test2").build().run()
```

2. **使用force_reload**:
```python
runtime = Bootstrap().with_settings(MySettings).build().run(force_reload=True)
```

3. **清理配置**:
```python
from df_test_framework import clear_settings

clear_settings("default")
runtime = Bootstrap().with_settings(MySettings).build().run()
```

### 错误2: ValidationError (Pydantic)

**错误信息**:
```
pydantic.ValidationError: 1 validation error for MySettings
database.url
  Field required [type=missing, input_value={'http': {...}}, input_type=dict]
```

**原因**: FrameworkSettings配置字段缺失或类型错误

**场景**:
```python
class MySettings(FrameworkSettings):
    api_key: str  # 没有默认值

# 未设置环境变量DF_API_KEY
runtime = Bootstrap().with_settings(MySettings).build().run()  # ❌ 错误
```

**解决方案**:

1. **设置环境变量**:
```bash
export DF_API_KEY="your-api-key"
```

2. **提供默认值**:
```python
class MySettings(FrameworkSettings):
    api_key: str = Field(default="")  # 添加默认值
```

3. **使用.env文件**:
```bash
# .env
DF_API_KEY=your-api-key
```

### 错误3: ValueError: Settings must be provided

**错误信息**:
```
ValueError: Settings must be provided to RuntimeBuilder
```

**原因**: RuntimeBuilder没有设置Settings

**场景**:
```python
# 错误示例
runtime = RuntimeBuilder().with_logger(logger).build()  # ❌ 缺少settings
```

**解决方案**:

**使用Bootstrap（推荐）**:
```python
runtime = Bootstrap().with_settings(MySettings).build().run()
```

**或手动设置Settings**:
```python
from df_test_framework import configure_settings, get_settings

configure_settings(MySettings)
settings = get_settings()

runtime = (
    RuntimeBuilder()
    .with_settings(settings)
    .with_logger(logger)
    .build()
)
```

## 🌐 连接与网络错误

### 错误4: httpx.ConnectError

**错误信息**:
```
httpx.ConnectError: [Errno 111] Connection refused
```

**原因**: 目标服务不可达

**排查步骤**:

1. **检查服务是否运行**:
```bash
# 检查服务端口
netstat -tuln | grep 8000
curl http://localhost:8000/health
```

2. **检查配置的URL**:
```python
# 打印实际URL
http = runtime.http_client()
print(f"Base URL: {http._client.base_url}")

# 检查Settings
print(f"Configured URL: {runtime.settings.http.base_url}")
```

3. **检查网络连通性**:
```bash
# Ping服务器
ping api.example.com

# Telnet测试端口
telnet api.example.com 8000
```

**解决方案**:

1. **启动目标服务**:
```bash
# 启动开发服务器
cd backend && python manage.py runserver
```

2. **修正URL配置**:
```python
class MySettings(FrameworkSettings):
    http: HTTPConfig = Field(default_factory=lambda: HTTPConfig(
        base_url="http://localhost:8000"  # 确保URL正确
    ))
```

### 错误5: httpx.TimeoutException

**错误信息**:
```
httpx.TimeoutException: Request timeout after 30.0 seconds
```

**原因**: 请求超时

**解决方案**:

1. **增加超时时间**:
```python
class MySettings(FrameworkSettings):
    http: HTTPConfig = Field(default_factory=lambda: HTTPConfig(
        timeout=60.0  # 增加到60秒
    ))
```

2. **为特定请求设置超时**:
```python
response = http_client.get("/api/slow-endpoint", timeout=120.0)
```

3. **检查服务性能**:
```python
import time

start = time.time()
response = http_client.get("/api/endpoint")
duration = time.time() - start
print(f"请求耗时: {duration:.2f}秒")
```

### 错误6: SSL Certificate Verification Failed

**错误信息**:
```
httpx.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed
```

**原因**: SSL证书验证失败

**解决方案**:

1. **禁用SSL验证（仅测试环境）**:
```python
import httpx

class MyHttpClient(HttpClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 禁用SSL验证
        self._client = httpx.Client(
            base_url=kwargs.get('base_url', ''),
            verify=False  # 仅用于测试环境
        )
```

2. **提供CA证书**:
```python
http_client = HttpClient(
    base_url="https://api.example.com",
    verify="/path/to/ca-bundle.crt"
)
```

## 🗄️ 数据库错误

### 错误7: sqlalchemy.exc.OperationalError

**错误信息**:
```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) FATAL: password authentication failed for user "testuser"
```

**原因**: 数据库连接失败

**排查步骤**:

1. **检查数据库配置**:
```python
print(f"Database URL: {runtime.settings.database.url}")
```

2. **测试数据库连接**:
```bash
# PostgreSQL
psql -h localhost -U testuser -d testdb

# MySQL
mysql -h localhost -u testuser -p testdb
```

**解决方案**:

1. **修正数据库URL**:
```bash
# .env
DF_DATABASE__URL=postgresql://testuser:testpass@localhost:5432/testdb
```

2. **检查数据库权限**:
```sql
-- PostgreSQL
GRANT ALL PRIVILEGES ON DATABASE testdb TO testuser;

-- MySQL
GRANT ALL PRIVILEGES ON testdb.* TO 'testuser'@'localhost';
```

### 错误8: sqlalchemy.exc.ProgrammingError

**错误信息**:
```
sqlalchemy.exc.ProgrammingError: (psycopg2.ProgrammingError) relation "users" does not exist
```

**原因**: 表不存在

**解决方案**:

1. **检查表是否存在**:
```python
result = database.execute(
    "SELECT tablename FROM pg_tables WHERE tablename = 'users'"
).first()
print(f"Table exists: {result is not None}")
```

2. **创建表**:
```python
database.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL
    )
""")
```

3. **使用Migration工具**:
```bash
# Alembic
alembic upgrade head
```

### 错误9: sqlalchemy.exc.IntegrityError

**错误信息**:
```
sqlalchemy.exc.IntegrityError: (psycopg2.IntegrityError) duplicate key value violates unique constraint "users_email_key"
```

**原因**: 违反唯一性约束

**解决方案**:

1. **清理测试数据**:
```python
@pytest.fixture(autouse=True)
def clean_users(database):
    yield
    database.execute("DELETE FROM users WHERE email LIKE '%@test.com'")
```

2. **使用唯一的测试数据**:
```python
import uuid

def test_create_user(database):
    email = f"user_{uuid.uuid4().hex[:8]}@test.com"  # 唯一email
    database.execute(
        "INSERT INTO users (username, email) VALUES (:u, :e)",
        {"u": "testuser", "e": email}
    )
```

3. **使用事务回滚**:
```python
@pytest.fixture
def db_transaction(database):
    connection = database.engine.connect()
    transaction = connection.begin()
    yield connection
    transaction.rollback()
    connection.close()
```

## 📦 Redis错误

### 错误10: redis.exceptions.ConnectionError

**错误信息**:
```
redis.exceptions.ConnectionError: Error 111 connecting to localhost:6379. Connection refused.
```

**原因**: Redis服务未运行

**排查步骤**:

1. **检查Redis是否运行**:
```bash
# 检查进程
ps aux | grep redis

# 检查端口
netstat -tuln | grep 6379

# 测试连接
redis-cli ping
```

**解决方案**:

1. **启动Redis**:
```bash
# Linux/Mac
redis-server

# Docker
docker run -d -p 6379:6379 redis:latest
```

2. **修正Redis配置**:
```bash
# .env
DF_REDIS__HOST=localhost
DF_REDIS__PORT=6379
DF_REDIS__DB=0
```

### 错误11: redis.exceptions.ResponseError

**错误信息**:
```
redis.exceptions.ResponseError: WRONGTYPE Operation against a key holding the wrong kind of value
```

**原因**: 对错误类型的键执行操作

**场景**:
```python
redis.set("key", "string_value")
redis.lpush("key", "list_value")  # ❌ 错误：key是string类型，不是list
```

**解决方案**:

1. **删除旧键**:
```python
redis.delete("key")
redis.lpush("key", "list_value")  # ✅ 成功
```

2. **检查键类型**:
```python
key_type = redis.type("key")
print(f"Key type: {key_type}")  # string, list, hash, set, zset

if key_type == "string":
    value = redis.get("key")
elif key_type == "list":
    value = redis.lrange("key", 0, -1)
```

## 🧪 测试执行错误

### 错误12: pytest fixture not found

**错误信息**:
```
fixture 'http_client' not found
```

**原因**: 未导入fixtures或conftest.py位置错误

**解决方案**:

1. **导入fixtures**:
```python
# tests/conftest.py
from df_test_framework.testing.fixtures import *  # 导入所有fixtures
```

2. **检查conftest.py位置**:
```
tests/
├── conftest.py         # ✅ 正确位置
├── api/
│   └── test_users.py
└── database/
    └── test_repos.py
```

3. **自定义fixture**:
```python
# tests/conftest.py
import pytest
from df_test_framework import Bootstrap
from my_project.config import MySettings

@pytest.fixture(scope="session")
def runtime():
    rt = Bootstrap().with_settings(MySettings).build().run()
    yield rt
    rt.close()

@pytest.fixture
def http_client(runtime):
    return runtime.http_client()
```

### 错误13: Tests hanging/blocking

**现象**: 测试一直运行不结束

**可能原因**:

1. **未关闭连接**:
```python
# ❌ 错误：未关闭runtime
def test_something():
    runtime = Bootstrap().build().run()
    # ... 测试
    # 缺少 runtime.close()
```

**解决方案**:
```python
# ✅ 正确：使用fixture自动管理
@pytest.fixture(scope="session")
def runtime():
    rt = Bootstrap().build().run()
    yield rt
    rt.close()  # 自动关闭
```

2. **死锁**:
```python
# 检查日志
pytest -s -v tests/  # -s显示print输出

# 添加超时
pytest --timeout=60 tests/  # 60秒超时
```

### 错误14: AssertionError with no message

**错误信息**:
```
AssertionError
```

**原因**: 断言失败但没有提供错误信息

**改进方案**:

```python
# ❌ 不好：没有错误信息
assert response.status_code == 200

# ✅ 好：有明确的错误信息
assert response.status_code == 200, \
    f"Expected 200, got {response.status_code}. Response: {response.text}"

# ✅ 更好：使用pytest的断言重写
import pytest

response = http_client.get("/api/users")
assert response.status_code == 200  # pytest会自动显示详细信息
```

## 🔌 扩展与插件错误

### 错误15: Plugin not found

**错误信息**:
```
AttributeError: 'ExtensionManager' object has no attribute 'my_plugin'
```

**原因**: 插件未注册或注册失败

**排查步骤**:

1. **检查插件是否注册**:
```python
runtime = (
    Bootstrap()
    .with_settings(MySettings)
    .with_plugin(MyPlugin())  # 确保调用了with_plugin
    .build()
    .run()
)
```

2. **检查插件实现**:
```python
class MyPlugin:
    @hookimpl  # ← 确保有这个装饰器
    def df_post_bootstrap(self, runtime):
        runtime.logger.info("Plugin loaded")
```

**解决方案**:

```python
# 验证插件已加载
if runtime.extensions:
    plugins = runtime.extensions.manager.get_plugins()
    print(f"Loaded plugins: {plugins}")
```

### 错误16: Hook implementation error

**错误信息**:
```
TypeError: df_providers() missing 1 required positional argument: 'logger'
```

**原因**: Hook实现签名不匹配

**错误示例**:
```python
class MyPlugin:
    @hookimpl
    def df_providers(self, settings):  # ❌ 缺少logger参数
        return {}
```

**正确实现**:
```python
class MyPlugin:
    @hookimpl
    def df_providers(self, settings, logger):  # ✅ 签名匹配
        return {}
```

**Hook签名参考**:
```python
# Hook 1
def df_config_sources(self, settings_cls: type[FrameworkSettings]) -> Iterable[ConfigSource]:
    ...

# Hook 2
def df_providers(self, settings: FrameworkSettings, logger) -> Dict[str, Provider]:
    ...

# Hook 3
def df_post_bootstrap(self, runtime: RuntimeContext) -> None:
    ...
```

## 🔍 通用排查技巧

### 1. 启用详细日志

```python
import logging

# 启用DEBUG级别日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 或通过配置
class MySettings(FrameworkSettings):
    logging: LoggingConfig = Field(default_factory=lambda: LoggingConfig(
        level="DEBUG"
    ))
```

### 2. 使用Python调试器

```python
# 在测试中设置断点
def test_something(http_client):
    response = http_client.get("/api/users")
    import pdb; pdb.set_trace()  # ← 断点
    assert response.status_code == 200
```

### 3. 检查环境变量

```python
import os

# 打印所有DF_开头的环境变量
df_vars = {k: v for k, v in os.environ.items() if k.startswith('DF_')}
print(f"DF Environment Variables: {df_vars}")
```

### 4. 验证配置加载

```python
from df_test_framework import get_settings

settings = get_settings()
print(f"Settings: {settings.model_dump()}")
```

### 5. 使用pytest -vv

```bash
# 显示更详细的测试输出
pytest -vv tests/

# 显示完整的diff
pytest -vv --tb=long tests/

# 显示print输出
pytest -s tests/
```

## 📞 获取帮助

如果遇到未在此列出的错误：

1. **查看日志**: 检查完整的错误堆栈
2. **搜索文档**: [用户指南](../user-guide/)、[API参考](../api-reference/)
3. **检查示例**: [示例项目](../../examples/)
4. **提交Issue**: [GitHub Issues](https://github.com/your-org/df-test-framework/issues)

## 🔗 相关文档

- [调试指南](debugging-guide.md)
- [性能调优](performance-tuning.md)
- [配置管理](../user-guide/configuration.md)

---

**返回**: [故障排查](README.md) | [文档首页](../README.md)
