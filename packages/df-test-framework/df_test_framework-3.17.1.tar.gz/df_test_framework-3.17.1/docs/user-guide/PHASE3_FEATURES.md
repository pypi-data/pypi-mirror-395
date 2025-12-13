# Phase 3 配置API增强 - 用户指南

> **v3.5 Phase 3 新功能**: Profile支持 + 运行时配置覆盖

---

## 目录

1. [功能概述](#功能概述)
2. [Profile环境配置](#profile环境配置)
3. [运行时配置覆盖](#运行时配置覆盖)
4. [最佳实践](#最佳实践)
5. [常见问题](#常见问题)

---

## 功能概述

Phase 3为框架添加了两个关键功能：

### 1. Profile环境配置
- **问题**: 不同环境（dev/test/staging/prod）需要不同配置
- **解决方案**: 通过`profile`参数明确指定环境，自动加载对应的`.env.{profile}`文件
- **优势**: 配置管理更规范，环境切换更简单

### 2. 运行时配置覆盖
- **问题**: 测试场景需要临时修改配置（如超时、URL等）
- **解决方案**: `RuntimeContext.with_overrides()`创建临时配置上下文
- **优势**: 不影响全局配置，测试隔离更好

---

## Profile环境配置

### 基本用法

#### 方式1: Bootstrap API

```python
from df_test_framework.infrastructure import Bootstrap

# 明确指定使用dev环境配置
app = (
    Bootstrap()
    .with_settings(MySettings, profile="dev")
    .build()
    .run()
)
```

#### 方式2: configure_settings直接调用

```python
from df_test_framework.infrastructure import configure_settings, get_settings

# 注册配置时指定profile
configure_settings(MySettings, profile="staging")

# 获取配置
settings = get_settings()
```

### 配置文件组织

#### 推荐的文件结构

```
project/
├── .env              # 基础配置（所有环境共享）
├── .env.dev          # 开发环境
├── .env.test         # 测试环境
├── .env.staging      # 预发布环境
├── .env.prod         # 生产环境
├── .env.local        # 个人本地覆盖（不提交到git）
└── .gitignore        # 排除.env.local
```

#### .env（基础配置）

```bash
# 所有环境共享的配置
APP_NAME=MyTestFramework
APP_VERSION=1.0.0
APP_DEBUG=false
APP_LOG_LEVEL=INFO
```

#### .env.dev（开发环境）

```bash
# 开发环境特定配置
APP_ENV=dev
APP_DEBUG=true
APP_LOG_LEVEL=DEBUG

# 开发环境HTTP配置
APP_HTTP__BASE_URL=http://localhost:8000
APP_HTTP__TIMEOUT=30

# 开发数据库
APP_DB__HOST=localhost
APP_DB__PORT=3306
APP_DB__NAME=test_dev
APP_DB__USER=dev_user
APP_DB__PASSWORD=dev_password
```

#### .env.prod（生产环境）

```bash
# 生产环境特定配置
APP_ENV=prod
APP_DEBUG=false
APP_LOG_LEVEL=WARNING

# 生产环境HTTP配置
APP_HTTP__BASE_URL=https://api.prod.com
APP_HTTP__TIMEOUT=10
APP_HTTP__MAX_RETRIES=3

# 生产数据库
APP_DB__HOST=db.prod.com
APP_DB__PORT=3306
APP_DB__NAME=production
APP_DB__USER=prod_user
APP_DB__PASSWORD=${DB_PASSWORD}  # 从环境变量获取
```

#### .env.local（本地覆盖，不提交）

```bash
# 个人开发环境覆盖
APP_HTTP__BASE_URL=http://192.168.1.100:8000
APP_DB__HOST=127.0.0.1
APP_DB__PASSWORD=my_local_password
```

### 配置优先级

配置加载顺序（优先级从低到高）：

1. `.env` - 基础配置
2. `.env.{profile}` - 环境特定配置
3. `.env.local` - 本地覆盖
4. 系统环境变量
5. 命令行参数

**Profile参数优先级**:
```python
# 优先级: profile参数 > ENV环境变量 > 默认值"test"

# 1. 代码明确指定（最高优先级）
Bootstrap().with_settings(MySettings, profile="dev")

# 2. 环境变量
os.environ["ENV"] = "staging"
Bootstrap().with_settings(MySettings)  # 使用staging

# 3. 默认值
Bootstrap().with_settings(MySettings)  # 使用test
```

### 实际使用示例

#### 示例1: 开发环境启动

```python
# conftest.py
import pytest
from df_test_framework.infrastructure import Bootstrap

@pytest.fixture(scope="session")
def runtime_ctx():
    """开发环境的RuntimeContext"""
    app = (
        Bootstrap()
        .with_settings(TestSettings, profile="dev")
        .build()
        .run()
    )
    yield app
    app.close()
```

#### 示例2: 多环境测试

```python
# tests/test_environments.py
import pytest
from df_test_framework.infrastructure import Bootstrap, clear_settings

@pytest.mark.parametrize("env_profile", ["dev", "test", "staging"])
def test_different_environments(env_profile):
    """测试不同环境配置"""
    clear_settings("env_test")

    runtime = (
        Bootstrap()
        .with_settings(TestSettings, namespace="env_test", profile=env_profile)
        .build()
        .run()
    )

    try:
        assert runtime.settings.app_env == env_profile
        # 验证环境特定配置
    finally:
        runtime.close()
        clear_settings("env_test")
```

---

## 运行时配置覆盖

### 基本用法

```python
# 获取原始RuntimeContext
runtime_ctx = ...

# 创建临时配置覆盖的新上下文
test_ctx = runtime_ctx.with_overrides({
    "http": {"timeout": 5},
    "db.host": "localhost"
})

# 使用新上下文
client = test_ctx.http_client()  # 使用5秒超时
```

### 支持的语法

#### 1. 嵌套字典语法

```python
test_ctx = runtime_ctx.with_overrides({
    "http": {
        "timeout": 5,
        "max_retries": 1,
        "base_url": "http://mock.local"
    },
    "db": {
        "host": "localhost",
        "port": 3307
    }
})
```

#### 2. 点号路径语法

```python
test_ctx = runtime_ctx.with_overrides({
    "http.timeout": 5,
    "http.max_retries": 1,
    "http.base_url": "http://mock.local",
    "db.host": "localhost",
    "db.port": 3307
})
```

#### 3. 混合语法

```python
test_ctx = runtime_ctx.with_overrides({
    "app_env": "test",
    "http": {"timeout": 5},      # 嵌套字典
    "db.host": "localhost",      # 点号路径
})
```

### 实际使用场景

#### 场景1: 测试超时处理

```python
def test_http_timeout_handling(runtime_ctx):
    """测试HTTP超时场景"""
    # 创建1秒超时的临时上下文
    test_ctx = runtime_ctx.with_overrides({
        "http.timeout": 5  # 最小5秒
    })

    client = test_ctx.http_client()

    # 测试超时场景
    with pytest.raises(TimeoutError):
        client.get("/slow-endpoint")
```

#### 场景2: 测试不同环境URL

```python
def test_staging_environment(runtime_ctx):
    """测试staging环境"""
    test_ctx = runtime_ctx.with_overrides({
        "http.base_url": "https://api.staging.com"
    })

    client = test_ctx.http_client()
    response = client.get("/api/v1/health")
    assert response.status_code == 200
```

#### 场景3: 测试数据库连接

```python
def test_local_database(runtime_ctx):
    """测试本地数据库连接"""
    test_ctx = runtime_ctx.with_overrides({
        "db": {
            "host": "localhost",
            "port": 3306,
            "name": "test_db",
            "user": "test_user",
            "password": "test_password"
        }
    })

    db = test_ctx.database()
    # 测试数据库操作
```

#### 场景4: 并行测试隔离

```python
@pytest.mark.parametrize("timeout", [5, 10, 15])
def test_different_timeouts(runtime_ctx, timeout):
    """测试不同超时配置（并行运行）"""
    # 每个测试用例使用独立的配置上下文
    test_ctx = runtime_ctx.with_overrides({
        "http.timeout": timeout
    })

    client = test_ctx.http_client()
    # 测试逻辑
```

### 重要特性

#### 1. 不可变性

```python
original_ctx = runtime_ctx
test_ctx1 = runtime_ctx.with_overrides({"app_name": "Test1"})
test_ctx2 = runtime_ctx.with_overrides({"app_name": "Test2"})

# 原上下文未修改
assert original_ctx.settings.app_name == "MyApp"

# 每个新上下文独立
assert test_ctx1.settings.app_name == "Test1"
assert test_ctx2.settings.app_name == "Test2"

# 它们是不同的实例
assert test_ctx1 is not test_ctx2
assert test_ctx1 is not original_ctx
```

#### 2. 资源共享

```python
test_ctx = runtime_ctx.with_overrides({"http.timeout": 5})

# logger和providers在新旧上下文间共享（避免重复初始化）
assert test_ctx.logger is runtime_ctx.logger
assert test_ctx.providers is runtime_ctx.providers
```

#### 3. 深度合并

```python
# v3.5+ 注意：http 是通过 @property 从 http_settings 自动转换的
# 在 v3.5+ 中，应该在 settings.py 中使用 HTTPSettings 声明式配置
# 以下示例展示配置覆盖功能（无论配置来源如何，覆盖功能都有效）

# 原配置（v3.5+ 中来自 HTTPSettings）
# runtime_ctx.settings.http_settings = HTTPSettings(...)
# runtime_ctx.settings.http  # 自动转换为 HTTPConfig

# 部分覆盖
test_ctx = runtime_ctx.with_overrides({
    "http": {"timeout": 5}
})

# 深度合并：只修改timeout，其他保持不变
assert test_ctx.settings.http.timeout == 5
assert test_ctx.settings.http.base_url == "http://prod.com"  # 未修改
assert test_ctx.settings.http.max_retries == 3  # 未修改
```

---

## 最佳实践

### 1. 配置文件管理

✅ **推荐做法**:
```bash
# .gitignore
.env.local
.env.*.local
```

```bash
# 提交到git的文件
git add .env .env.dev .env.test .env.staging .env.prod

# 不提交的文件
.env.local  # 个人本地配置
```

❌ **避免做法**:
- 不要在`.env.{profile}`中存储敏感信息（使用环境变量或Secret管理）
- 不要提交`.env.local`到git

### 2. Profile使用

✅ **推荐做法**:
```python
# 代码中明确指定profile，清晰可控
Bootstrap().with_settings(MySettings, profile="dev")
```

❌ **避免做法**:
```python
# 依赖环境变量，容易出错
os.environ["ENV"] = "dev"  # 可能被其他代码修改
Bootstrap().with_settings(MySettings)
```

### 3. 运行时覆盖

✅ **推荐做法**:
```python
# 测试中使用with_overrides，不影响其他测试
def test_feature(runtime_ctx):
    test_ctx = runtime_ctx.with_overrides({"http.timeout": 5})
    # 测试逻辑
```

❌ **避免做法**:
```python
# 修改全局配置，影响其他测试
def test_feature(runtime_ctx):
    runtime_ctx.settings.http.timeout = 5  # ❌ 不可变，会抛出异常
```

### 4. 测试隔离

✅ **推荐做法**:
```python
@pytest.fixture
def isolated_runtime(base_runtime_ctx):
    """为每个测试创建隔离的配置上下文"""
    return base_runtime_ctx.with_overrides({
        "http.timeout": 10,
        "db.host": "localhost"
    })

def test_1(isolated_runtime):
    # 使用隔离的配置
    pass

def test_2(isolated_runtime):
    # 每个测试都有独立的配置
    pass
```

---

## 常见问题

### Q1: profile参数和ENV环境变量的区别？

**A**:
- **profile参数**: 代码明确指定，优先级最高，推荐使用
- **ENV环境变量**: 系统环境变量，优先级次之
- **默认值**: `"test"`，最低优先级

```python
# 优先级演示
os.environ["ENV"] = "staging"

# profile参数优先于ENV变量
Bootstrap().with_settings(MySettings, profile="dev")  # 使用dev而非staging
```

### Q2: with_overrides会影响原RuntimeContext吗？

**A**: 不会。`with_overrides()`返回新实例，原RuntimeContext保持不变。

```python
original = runtime_ctx
modified = runtime_ctx.with_overrides({"http.timeout": 5})

assert original is not modified
assert original.settings.http.timeout == 30  # 原配置未修改
assert modified.settings.http.timeout == 5   # 新配置已覆盖
```

### Q3: 可以多次调用with_overrides吗？

**A**: 可以。每次调用都返回新实例。

```python
ctx1 = runtime_ctx.with_overrides({"http.timeout": 5})
ctx2 = ctx1.with_overrides({"db.host": "localhost"})
ctx3 = ctx2.with_overrides({"app_env": "test"})

# 每个都是独立的实例
assert ctx1 is not ctx2 is not ctx3
```

### Q4: with_overrides支持哪些数据类型？

**A**: 支持所有Pydantic支持的数据类型，包括：
- 基本类型（str, int, bool等）
- 嵌套对象（自动深度合并）
- 列表
- 字典

```python
test_ctx = runtime_ctx.with_overrides({
    "app_name": "Test",           # 字符串
    "http": {                     # 嵌套对象
        "timeout": 5,             # 整数
        "verify_ssl": False       # 布尔值
    },
    "db.port": 3307               # 点号路径
})
```

### Q5: 如何在pytest中为每个测试创建独立配置？

**A**: 使用fixture和with_overrides：

```python
@pytest.fixture
def test_runtime(base_runtime_ctx, request):
    """为每个测试创建独立的配置上下文"""
    # 从test marker获取配置覆盖
    overrides = request.node.get_closest_marker("config_override")
    if overrides:
        return base_runtime_ctx.with_overrides(overrides.kwargs)
    return base_runtime_ctx

@pytest.mark.config_override(http={"timeout": 5})
def test_with_custom_timeout(test_runtime):
    client = test_runtime.http_client()
    # 使用5秒超时
```

### Q6: profile文件不存在会报错吗？

**A**: 不会。框架会尝试加载`.env.{profile}`，如果文件不存在则跳过，继续加载其他配置源。

```python
# .env.dev不存在也不会报错
Bootstrap().with_settings(MySettings, profile="dev")
```

### Q7: 如何调试配置加载问题？

**A**: 检查配置加载日志（框架会记录每个配置源的加载情况）：

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# 会输出详细的配置加载日志
runtime = Bootstrap().with_settings(MySettings, profile="dev").build().run()
```

---

## 相关文档

- [Phase 3完成报告](../PHASE3_COMPLETION_REPORT.md) - 技术实现细节
- [配置管理指南](./configuration.md) - 配置系统完整文档
- [测试编写指南](./testing.md) - 测试最佳实践

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
