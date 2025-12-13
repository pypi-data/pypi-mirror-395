# Mock 工具使用指南

> 版本: v3.11.0+
> 模块: `df_test_framework.testing.mocking`

## 概述

框架提供多种 Mock 工具，支持：
- **DatabaseMocker** - 数据库操作 Mock
- **RedisMocker** - Redis 操作 Mock
- **HttpMocker** - HTTP 请求 Mock（基于 pytest-httpx）
- **TimeMocker** - 时间 Mock（基于 freezegun）

## DatabaseMocker

用于 Mock 数据库操作，无需真实数据库连接。

### 基本用法

```python
from df_test_framework.testing.mocking import DatabaseMocker

def test_user_service():
    mocker = DatabaseMocker()

    # 设置查询结果
    mocker.add_query_result(
        "SELECT * FROM users WHERE id = :id",
        [{"id": 1, "name": "Alice", "email": "alice@example.com"}]
    )

    # 启动 Mock
    with mocker.mock_db() as mock_session:
        # 执行查询
        result = mock_session.execute(
            "SELECT * FROM users WHERE id = :id",
            {"id": 1}
        )

        # 验证结果
        users = result.fetchall()
        assert len(users) == 1
        assert users[0]["name"] == "Alice"

    # 验证调用
    assert mocker.query_count == 1
    mocker.assert_called_with("SELECT * FROM users")
```

### API 详解

#### DatabaseMocker

| 方法 | 描述 |
|------|------|
| `add_query_result(sql, result)` | 添加查询结果映射 |
| `mock_db()` | 获取 Mock 上下文管理器 |
| `assert_called_with(sql_pattern)` | 断言是否调用了匹配的 SQL |
| `assert_not_called_with(sql_pattern)` | 断言没有调用匹配的 SQL |
| `get_call_history()` | 获取调用历史 |
| `reset()` | 重置 Mock 状态 |

#### 属性

| 属性 | 类型 | 描述 |
|------|------|------|
| `query_count` | `int` | 查询次数 |
| `call_history` | `list` | 调用历史记录 |

### 进阶用法

#### 多个查询结果

```python
mocker = DatabaseMocker()

# 设置不同查询的结果
mocker.add_query_result(
    "SELECT * FROM users",
    [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
)

mocker.add_query_result(
    "SELECT * FROM orders WHERE user_id = :user_id",
    [{"id": 101, "amount": 100.0}]
)

with mocker.mock_db() as session:
    users = session.execute("SELECT * FROM users").fetchall()
    orders = session.execute(
        "SELECT * FROM orders WHERE user_id = :user_id",
        {"user_id": 1}
    ).fetchall()
```

#### SQL 标准化

DatabaseMocker 会自动标准化 SQL 进行匹配：

```python
# 这些 SQL 会匹配同一个结果
mocker.add_query_result("SELECT * FROM users WHERE id = :id", result)

# 以下查询都会匹配：
"SELECT * FROM users WHERE id = :id"
"select * from users where id = :id"  # 大小写不敏感
"SELECT  *  FROM  users  WHERE  id = :id"  # 空格标准化
```

#### 调用历史分析

```python
with mocker.mock_db() as session:
    session.execute("SELECT * FROM users")
    session.execute("INSERT INTO logs (msg) VALUES (:msg)", {"msg": "test"})

# 获取调用历史
history = mocker.get_call_history()
for call in history:
    print(f"SQL: {call['sql']}")
    print(f"Params: {call['params']}")

# 断言
mocker.assert_called_with("SELECT")
mocker.assert_called_with("INSERT INTO logs")
mocker.assert_not_called_with("DELETE")
```

## RedisMocker

用于 Mock Redis 操作，支持常用命令。

### 基本用法

```python
from df_test_framework.testing.mocking import RedisMocker

def test_cache_service():
    mocker = RedisMocker()

    with mocker.mock_redis() as redis:
        # 字符串操作
        redis.set("key1", "value1")
        assert redis.get("key1") == "value1"

        # 设置过期时间
        redis.setex("temp_key", 60, "temp_value")

        # 哈希操作
        redis.hset("user:1", "name", "Alice")
        assert redis.hget("user:1", "name") == "Alice"

        # 列表操作
        redis.lpush("queue", "item1", "item2")
        assert redis.llen("queue") == 2
```

### 支持的操作

#### 字符串操作

| 命令 | 描述 |
|------|------|
| `get(key)` | 获取值 |
| `set(key, value)` | 设置值 |
| `setex(key, time, value)` | 设置值和过期时间 |
| `delete(*keys)` | 删除键 |
| `exists(key)` | 检查键是否存在 |
| `incr(key)` | 自增 |
| `decr(key)` | 自减 |

#### 哈希操作

| 命令 | 描述 |
|------|------|
| `hget(name, key)` | 获取哈希字段 |
| `hset(name, key, value)` | 设置哈希字段 |
| `hgetall(name)` | 获取所有哈希字段 |
| `hdel(name, *keys)` | 删除哈希字段 |

#### 列表操作

| 命令 | 描述 |
|------|------|
| `lpush(name, *values)` | 左侧插入 |
| `rpush(name, *values)` | 右侧插入 |
| `lpop(name)` | 左侧弹出 |
| `rpop(name)` | 右侧弹出 |
| `llen(name)` | 获取长度 |
| `lrange(name, start, end)` | 获取范围 |

#### 集合操作

| 命令 | 描述 |
|------|------|
| `sadd(name, *values)` | 添加成员 |
| `srem(name, *values)` | 删除成员 |
| `smembers(name)` | 获取所有成员 |
| `sismember(name, value)` | 检查成员是否存在 |

### 进阶用法

#### 使用 fakeredis

如果安装了 `fakeredis`，RedisMocker 会自动使用它提供更完整的 Redis 模拟：

```bash
pip install fakeredis
```

```python
mocker = RedisMocker()

# 自动检测并使用 fakeredis
with mocker.mock_redis() as redis:
    # 支持更多 Redis 命令
    redis.expire("key", 60)
    redis.ttl("key")
```

#### 预设数据

```python
mocker = RedisMocker()

with mocker.mock_redis() as redis:
    # 预设测试数据
    redis.set("config:api_url", "https://api.example.com")
    redis.hset("user:1", mapping={
        "name": "Alice",
        "email": "alice@example.com",
    })

    # 测试代码
    service = MyService(redis)
    result = service.get_config("api_url")
    assert result == "https://api.example.com"
```

## HttpMocker

基于 `pytest-httpx` 的 HTTP Mock 工具。

### 基本用法

```python
import pytest

def test_api_client(httpx_mock):
    """使用 pytest-httpx fixture"""
    # 设置 Mock 响应
    httpx_mock.add_response(
        url="https://api.example.com/users/1",
        json={"id": 1, "name": "Alice"},
    )

    # 测试代码
    import httpx
    response = httpx.get("https://api.example.com/users/1")

    assert response.json()["name"] == "Alice"
```

### 进阶用法

#### 匹配请求方法

```python
httpx_mock.add_response(
    method="POST",
    url="https://api.example.com/users",
    json={"id": 2, "name": "Bob"},
    status_code=201,
)
```

#### 匹配请求头

```python
httpx_mock.add_response(
    url="https://api.example.com/protected",
    match_headers={"Authorization": "Bearer TOKEN"},
    json={"data": "secret"},
)
```

#### 模拟错误

```python
httpx_mock.add_response(
    url="https://api.example.com/error",
    status_code=500,
    json={"error": "Internal Server Error"},
)
```

#### 多次响应

```python
# 第一次返回空列表
httpx_mock.add_response(
    url="https://api.example.com/items",
    json=[],
)

# 第二次返回数据
httpx_mock.add_response(
    url="https://api.example.com/items",
    json=[{"id": 1}],
)
```

## TimeMocker

基于 `freezegun` 的时间 Mock 工具。

### 基本用法

```python
from df_test_framework.testing.mocking import TimeMocker

def test_time_sensitive_code():
    mocker = TimeMocker()

    # 冻结到指定时间
    with mocker.freeze("2025-01-15 10:00:00"):
        from datetime import datetime
        now = datetime.now()
        assert now.year == 2025
        assert now.month == 1
        assert now.day == 15
```

### 进阶用法

#### 时间推移

```python
with mocker.freeze("2025-01-15 10:00:00") as frozen_time:
    # 当前是 10:00
    assert datetime.now().hour == 10

    # 推进 2 小时
    frozen_time.tick(timedelta(hours=2))

    # 现在是 12:00
    assert datetime.now().hour == 12
```

#### 测试过期逻辑

```python
def test_token_expiration():
    mocker = TimeMocker()

    with mocker.freeze("2025-01-15 10:00:00") as frozen_time:
        # 创建 1 小时后过期的 token
        token = create_token(expires_in=3600)

        # 验证未过期
        assert is_token_valid(token)

        # 推进 2 小时
        frozen_time.tick(timedelta(hours=2))

        # 验证已过期
        assert not is_token_valid(token)
```

## 测试示例

### 综合使用

```python
import pytest
from df_test_framework.testing.mocking import (
    DatabaseMocker,
    RedisMocker,
    TimeMocker,
)

@pytest.fixture
def db_mocker():
    mocker = DatabaseMocker()
    mocker.add_query_result(
        "SELECT * FROM users WHERE id = :id",
        [{"id": 1, "name": "Alice"}]
    )
    return mocker

@pytest.fixture
def redis_mocker():
    return RedisMocker()

@pytest.fixture
def time_mocker():
    return TimeMocker()

def test_user_cache_service(db_mocker, redis_mocker, time_mocker):
    """测试用户缓存服务"""
    with db_mocker.mock_db() as db, \
         redis_mocker.mock_redis() as redis, \
         time_mocker.freeze("2025-01-15 10:00:00"):

        # 首次获取 - 从数据库
        service = UserCacheService(db, redis)
        user = service.get_user(1)

        assert user["name"] == "Alice"
        assert db_mocker.query_count == 1

        # 再次获取 - 从缓存
        user = service.get_user(1)
        assert db_mocker.query_count == 1  # 没有新查询
```

### 与框架 Fixture 集成

```python
@pytest.fixture
def mock_database(request):
    """数据库 Mock fixture"""
    mocker = DatabaseMocker()
    yield mocker

@pytest.fixture
def mock_redis(request):
    """Redis Mock fixture"""
    mocker = RedisMocker()
    yield mocker

def test_with_fixtures(mock_database, mock_redis):
    mock_database.add_query_result("SELECT 1", [{"1": 1}])

    with mock_database.mock_db() as db, \
         mock_redis.mock_redis() as redis:
        # 测试代码
        pass
```

## 最佳实践

### 1. 隔离 Mock 范围

```python
# ✅ 好：每个测试独立的 Mock
def test_case_1():
    mocker = DatabaseMocker()
    # ...

def test_case_2():
    mocker = DatabaseMocker()  # 新实例
    # ...

# ❌ 差：共享 Mock 状态
mocker = DatabaseMocker()

def test_case_1():
    mocker.add_query_result(...)

def test_case_2():
    # 可能受 test_case_1 影响
    pass
```

### 2. 明确设置预期

```python
# ✅ 好：明确设置所有需要的响应
mocker.add_query_result("SELECT * FROM users", users_data)
mocker.add_query_result("SELECT * FROM orders", orders_data)

# ❌ 差：依赖默认行为
# 未设置的查询可能返回意外结果
```

### 3. 验证调用

```python
with mocker.mock_db() as db:
    service.process(db)

# ✅ 验证关键操作被执行
mocker.assert_called_with("INSERT INTO audit_log")
mocker.assert_not_called_with("DELETE")
```

### 4. 使用 Fixture 简化

```python
@pytest.fixture
def mock_external_services(db_mocker, redis_mocker, httpx_mock):
    """统一设置外部服务 Mock"""
    db_mocker.add_query_result("SELECT config", [{"value": "test"}])
    httpx_mock.add_response(url="https://api.example.com/health", json={"status": "ok"})

    return {
        "db": db_mocker,
        "redis": redis_mocker,
        "http": httpx_mock,
    }
```

## 常见问题

### Q: Mock 的查询没有匹配？

检查 SQL 是否完全匹配（注意参数格式）：

```python
# 设置时
mocker.add_query_result("SELECT * FROM users WHERE id = :id", result)

# 调用时必须匹配
session.execute("SELECT * FROM users WHERE id = :id", {"id": 1})  # ✅
session.execute("SELECT * FROM users WHERE id = ?", [1])  # ❌ 参数格式不同
```

### Q: 如何 Mock 事务？

```python
with mocker.mock_db() as session:
    # Mock session 支持基本的事务操作
    session.begin()
    session.execute("INSERT ...")
    session.commit()  # 或 session.rollback()
```

### Q: RedisMocker 缺少某个命令？

安装 fakeredis 获得更完整的支持：

```bash
pip install fakeredis
```

或者提交 Issue 请求添加命令支持。

## 参考

- [pytest-httpx 文档](https://colin-b.github.io/pytest_httpx/)
- [freezegun 文档](https://github.com/spulec/freezegun)
- [fakeredis 文档](https://github.com/cunla/fakeredis-py)
