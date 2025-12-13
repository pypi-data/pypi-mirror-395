# Core API 参考

> ⚠️ **v3架构说明**: 此文档为v2遗留内容，提供向后兼容参考。v3架构中:
> - **HTTP客户端** 已迁移至 [`clients/`](clients.md) 模块
> - **Database** 已迁移至 [`databases/`](databases.md) 模块
> - **RedisClient** 已迁移至 [`databases/`](databases.md) 模块
>
> 建议使用**顶层导入**（如下所示），无需关心内部路径变化。
>
> 📖 完整迁移指南: [v2-to-v3 迁移文档](../migration/v2-to-v3.md)

核心功能层的完整API参考，包含HTTP客户端、数据库和Redis客户端。

---

## 📦 模块导入

```python
# HTTP客户端
from df_test_framework import HttpClient

# 数据库
from df_test_framework import Database

# Redis客户端
from df_test_framework import RedisClient

# 或者从具体模块导入（v3架构路径）
from df_test_framework.clients.http.rest.httpx import HttpClient
from df_test_framework.databases.database import Database
from df_test_framework.databases.redis.redis_client import RedisClient
```

---

## 🌐 HttpClient - HTTP客户端

统一的HTTP客户端封装，基于httpx实现，提供请求/响应拦截、自动重试、认证管理等功能。

### 初始化

```python
client = HttpClient(
    base_url="https://api.example.com",
    timeout=30,
    headers={"User-Agent": "MyApp/1.0"},
    verify_ssl=True,
    max_retries=3,
    max_connections=50,
    max_keepalive_connections=20,
)
```

#### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|-----|------|-------|------|
| `base_url` | `str` | **必填** | API基础URL，例如 `https://api.example.com` |
| `timeout` | `int` | `30` | 请求超时时间（秒） |
| `headers` | `Dict[str, str]` | `None` | 默认请求头 |
| `verify_ssl` | `bool` | `True` | 是否验证SSL证书 |
| `max_retries` | `int` | `3` | 最大重试次数 |
| `max_connections` | `int` | `50` | 最大连接数 |
| `max_keepalive_connections` | `int` | `20` | Keep-Alive连接数 |

---

### 🔧 核心方法

#### request()

**功能**: 发送HTTP请求（支持自动重试）

**签名**:
```python
def request(
    method: str,
    url: str,
    **kwargs,
) -> httpx.Response
```

**参数**:
- `method`: 请求方法（GET, POST, PUT, DELETE等）
- `url`: 请求路径（相对于base_url）
- `**kwargs`: 其他请求参数（params, json, data, headers等）

**返回**: `httpx.Response` 对象

**异常**:
- `httpx.TimeoutException`: 请求超时（重试max_retries次后仍失败）
- `httpx.HTTPStatusError`: HTTP状态错误
- `httpx.RequestError`: 请求错误

**重试策略**:
- ✅ **自动重试**: 超时异常和5xx服务器错误
- ❌ **不重试**: 4xx客户端错误
- 📈 **退避策略**: 指数退避（1s, 2s, 4s, 8s...）

**示例**:
```python
# 发送GET请求
response = client.request(
    "GET",
    "/users/1",
    params={"include": "profile"}
)

# 发送POST请求
response = client.request(
    "POST",
    "/users",
    json={"name": "张三", "email": "zhangsan@example.com"},
    headers={"Content-Type": "application/json"}
)
```

---

#### get()

**功能**: 发送GET请求

**签名**:
```python
def get(
    url: str,
    params: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> httpx.Response
```

**示例**:
```python
# 简单GET请求
response = client.get("/users/1")

# 带查询参数
response = client.get("/users", params={"page": 1, "size": 10})

# 带自定义请求头
response = client.get(
    "/users/1",
    headers={"X-Custom-Header": "value"}
)
```

---

#### post()

**功能**: 发送POST请求

**签名**:
```python
def post(
    url: str,
    json: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> httpx.Response
```

**示例**:
```python
# JSON格式
response = client.post(
    "/users",
    json={
        "name": "张三",
        "email": "zhangsan@example.com"
    }
)

# 表单格式
response = client.post(
    "/login",
    data={
        "username": "zhangsan",
        "password": "secret"
    }
)
```

---

#### put()

**功能**: 发送PUT请求

**签名**:
```python
def put(
    url: str,
    json: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> httpx.Response
```

**示例**:
```python
response = client.put(
    "/users/1",
    json={"name": "李四"}
)
```

---

#### patch()

**功能**: 发送PATCH请求

**签名**:
```python
def patch(
    url: str,
    json: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> httpx.Response
```

**示例**:
```python
response = client.patch(
    "/users/1",
    json={"status": "active"}
)
```

---

#### delete()

**功能**: 发送DELETE请求

**签名**:
```python
def delete(
    url: str,
    **kwargs,
) -> httpx.Response
```

**示例**:
```python
response = client.delete("/users/1")
```

---

#### set_auth_token()

**功能**: 设置认证token

**签名**:
```python
def set_auth_token(token: str, token_type: str = "Bearer") -> None
```

**参数**:
- `token`: 认证令牌
- `token_type`: 令牌类型（Bearer, Basic等）

**示例**:
```python
# Bearer Token认证
client.set_auth_token("eyJhbGciOiJIUzI1NiIs...")

# Basic认证
client.set_auth_token("dXNlcjpwYXNzd29yZA==", token_type="Basic")

# 后续请求会自动携带Authorization头
response = client.get("/protected/resource")
```

---

#### close()

**功能**: 关闭客户端连接

**签名**:
```python
def close() -> None
```

**示例**:
```python
client.close()

# 或使用上下文管理器（推荐）
with HttpClient(base_url="https://api.example.com") as client:
    response = client.get("/users/1")
# 自动关闭连接
```

---

### 🎯 完整使用示例

```python
from df_test_framework import HttpClient

def test_http_client_example():
    """HttpClient完整使用示例"""

    # 1. 创建客户端
    client = HttpClient(
        base_url="https://jsonplaceholder.typicode.com",
        timeout=30,
        max_retries=3
    )

    try:
        # 2. 设置认证（可选）
        client.set_auth_token("your-token-here")

        # 3. 发送请求
        # GET请求
        response = client.get("/users/1")
        assert response.status_code == 200
        user = response.json()
        print(f"用户: {user['name']}")

        # POST请求
        response = client.post(
            "/users",
            json={
                "name": "张三",
                "email": "zhangsan@example.com"
            }
        )
        assert response.status_code == 201

        # PUT请求
        response = client.put(
            "/users/1",
            json={"name": "李四"}
        )

        # DELETE请求
        response = client.delete("/users/1")

    finally:
        # 4. 关闭连接
        client.close()
```

---

### 🔒 URL敏感参数脱敏

HttpClient会自动脱敏URL中的敏感参数，保护密码、token等信息不被记录到日志。

**自动脱敏的参数**:
- `token`, `access_token`, `refresh_token`
- `key`, `api_key`, `secret`, `secret_key`
- `password`, `passwd`
- `authorization`, `auth`

**示例**:
```python
# 原始URL
url = "/api/users?token=abc123&id=1"

# 日志中显示
# [GET] /api/users?token=****&id=1
```

---

## 💾 Database - 数据库客户端

数据库操作封装，基于SQLAlchemy实现，提供连接管理、事务支持、常用CRUD操作。

### 初始化

```python
db = Database(
    connection_string="mysql+pymysql://user:password@localhost:3306/testdb?charset=utf8mb4",
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=3600,
    pool_pre_ping=True,
    echo=False,
    allowed_tables=None,  # None表示允许所有表
)
```

#### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|-----|------|-------|------|
| `connection_string` | `str` | **必填** | 数据库连接字符串 |
| `pool_size` | `int` | `10` | 连接池大小 |
| `max_overflow` | `int` | `20` | 连接池最大溢出数 |
| `pool_timeout` | `int` | `30` | 连接池超时时间（秒） |
| `pool_recycle` | `int` | `3600` | 连接回收时间（秒），防止连接过期 |
| `pool_pre_ping` | `bool` | `True` | 是否检测连接有效性 |
| `echo` | `bool` | `False` | 是否打印SQL语句（调试用） |
| `allowed_tables` | `Optional[Set[str]]` | `None` | 允许操作的表名白名单 |

**连接字符串格式**:
```python
# MySQL
"mysql+pymysql://user:password@host:port/database?charset=utf8mb4"

# PostgreSQL
"postgresql://user:password@host:port/database"

# SQLite
"sqlite:///./test.db"
```

**表名白名单**:
```python
# 开发/测试环境：允许所有表（默认）
db = Database(connection_string)

# 生产环境：限制表名白名单
db = Database(
    connection_string,
    allowed_tables={"users", "orders", "products"}
)

# 特殊场景：禁止所有表操作
db = Database(
    connection_string,
    allowed_tables=set()  # 空集禁止所有表
)
```

---

### 🔧 查询方法

#### query_one()

**功能**: 查询单条记录

**签名**:
```python
def query_one(
    sql: Union[str, Executable],
    params: Optional[Dict[str, Any]] = None,
) -> Optional[Dict[str, Any]]
```

**参数**:
- `sql`: SQL查询语句
- `params`: 参数字典（防SQL注入）

**返回**: 单条记录的字典，如果没有结果则返回`None`

**示例**:
```python
# 查询单个用户
user = db.query_one(
    "SELECT * FROM users WHERE id = :id",
    {"id": 1}
)

if user:
    print(f"用户名: {user['name']}")
else:
    print("用户不存在")
```

---

#### query_all()

**功能**: 查询多条记录

**签名**:
```python
def query_all(
    sql: Union[str, Executable],
    params: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]
```

**返回**: 记录列表

**示例**:
```python
# 查询所有活跃用户
users = db.query_all(
    "SELECT * FROM users WHERE status = :status",
    {"status": "ACTIVE"}
)

print(f"找到 {len(users)} 个活跃用户")
for user in users:
    print(f"- {user['name']}")
```

---

### 🔧 执行方法

#### execute()

**功能**: 执行SQL语句（INSERT/UPDATE/DELETE）

**签名**:
```python
def execute(
    sql: Union[str, Executable],
    params: Optional[Dict[str, Any]] = None,
) -> int
```

**返回**: 影响的行数

**示例**:
```python
# 更新用户状态
affected_rows = db.execute(
    "UPDATE users SET status = :status WHERE id = :id",
    {"status": "INACTIVE", "id": 1}
)
print(f"影响了 {affected_rows} 行")
```

---

### 🔧 CRUD操作

#### insert()

**功能**: 插入记录

**签名**:
```python
def insert(
    table: str,
    data: Dict[str, Any],
) -> int
```

**参数**:
- `table`: 表名
- `data`: 数据字典

**返回**: 插入的记录ID

**异常**:
- `ValueError`: 表名不在白名单中
- `IntegrityError`: 违反唯一性约束
- `OperationalError`: 数据库操作错误

**示例**:
```python
# 插入用户
user_id = db.insert(
    "users",
    {
        "name": "张三",
        "email": "zhangsan@example.com",
        "age": 25
    }
)
print(f"新用户ID: {user_id}")
```

---

#### batch_insert()

**功能**: 批量插入记录

**签名**:
```python
def batch_insert(
    table: str,
    data_list: List[Dict[str, Any]],
    chunk_size: int = 1000,
) -> int
```

**参数**:
- `table`: 表名
- `data_list`: 数据字典列表
- `chunk_size`: 每批次插入数量（默认1000）

**返回**: 插入的总记录数

**示例**:
```python
# 批量插入用户
users_data = [
    {"name": "张三", "age": 20},
    {"name": "李四", "age": 25},
    {"name": "王五", "age": 30},
    # ... 更多数据
]

count = db.batch_insert("users", users_data, chunk_size=500)
print(f"成功插入 {count} 条记录")
```

---

#### update()

**功能**: 更新记录

**签名**:
```python
def update(
    table: str,
    data: Dict[str, Any],
    where: str,
    where_params: Optional[Dict[str, Any]] = None,
) -> int
```

**参数**:
- `table`: 表名
- `data`: 要更新的数据字典
- `where`: WHERE条件
- `where_params`: WHERE条件参数

**返回**: 影响的行数

**示例**:
```python
# 更新用户信息
affected_rows = db.update(
    "users",
    data={"status": "ACTIVE", "last_login": "2025-11-01"},
    where="id = :id",
    where_params={"id": 1}
)
print(f"更新了 {affected_rows} 条记录")
```

---

#### delete()

**功能**: 删除记录

**签名**:
```python
def delete(
    table: str,
    where: str,
    where_params: Optional[Dict[str, Any]] = None,
) -> int
```

**参数**:
- `table`: 表名
- `where`: WHERE条件
- `where_params`: WHERE条件参数

**返回**: 删除的行数

**示例**:
```python
# 删除用户
deleted_rows = db.delete(
    "users",
    where="id = :id",
    where_params={"id": 1}
)
print(f"删除了 {deleted_rows} 条记录")
```

---

### 🔧 事务管理

#### session()

**功能**: 获取数据库会话上下文管理器

**签名**:
```python
@contextmanager
def session() -> Session
```

**示例**:
```python
from sqlalchemy import text

with db.session() as session:
    result = session.execute(text("SELECT * FROM users"))
    users = result.fetchall()
# 自动提交或回滚
```

---

#### transaction()

**功能**: 事务上下文管理器 - 支持原子操作

**签名**:
```python
@contextmanager
def transaction() -> Session
```

**示例**:
```python
# 原子操作：要么都成功，要么都回滚
with db.transaction():
    db.insert("users", {"name": "张三"})
    db.insert("orders", {"user_id": 1})
    # 如果任何一个失败，都会回滚
```

---

#### savepoint()

**功能**: 保存点 - 支持部分回滚

**签名**:
```python
@contextmanager
def savepoint(name: str = "sp1") -> Savepoint
```

**示例**:
```python
with db.transaction():
    db.insert("users", {"name": "张三"})

    try:
        with db.savepoint("sp1"):
            db.insert("orders", {"user_id": 1})
            raise ValueError("订单验证失败")
    except ValueError:
        # 只回滚到保存点，users已插入
        pass

    # 继续操作
    db.insert("logs", {"message": "处理完成"})
```

---

### 🎯 完整使用示例

```python
from df_test_framework import Database

def test_database_example():
    """Database完整使用示例"""

    # 1. 创建数据库连接
    db = Database(
        connection_string="sqlite:///./test.db",
        pool_size=5,
        echo=True  # 打印SQL（调试用）
    )

    try:
        # 2. 插入数据
        user_id = db.insert(
            "users",
            {
                "name": "张三",
                "email": "zhangsan@example.com",
                "age": 25,
                "status": "ACTIVE"
            }
        )
        print(f"新用户ID: {user_id}")

        # 3. 查询单条记录
        user = db.query_one(
            "SELECT * FROM users WHERE id = :id",
            {"id": user_id}
        )
        assert user is not None
        assert user["name"] == "张三"

        # 4. 查询多条记录
        active_users = db.query_all(
            "SELECT * FROM users WHERE status = :status",
            {"status": "ACTIVE"}
        )
        print(f"活跃用户数: {len(active_users)}")

        # 5. 更新记录
        affected_rows = db.update(
            "users",
            data={"status": "INACTIVE"},
            where="id = :id",
            where_params={"id": user_id}
        )
        print(f"更新了 {affected_rows} 条记录")

        # 6. 批量插入
        users_data = [
            {"name": "李四", "age": 30, "status": "ACTIVE"},
            {"name": "王五", "age": 28, "status": "ACTIVE"},
        ]
        count = db.batch_insert("users", users_data)
        print(f"批量插入 {count} 条记录")

        # 7. 使用事务
        with db.transaction():
            db.insert("users", {"name": "赵六", "age": 35})
            db.insert("logs", {"message": "创建用户成功"})
            # 两个操作要么都成功，要么都回滚

        # 8. 删除记录
        deleted_rows = db.delete(
            "users",
            where="id = :id",
            where_params={"id": user_id}
        )
        print(f"删除了 {deleted_rows} 条记录")

    finally:
        # 9. 关闭连接
        db.close()
```

---

## 🔴 RedisClient - Redis客户端

Redis客户端封装，基于redis-py实现，提供常用的Redis操作。

### 初始化

```python
redis_client = RedisClient(
    host="localhost",
    port=6379,
    db=0,
    password=None,
    max_connections=50,
    decode_responses=True,
)
```

#### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|-----|------|-------|------|
| `host` | `str` | `"localhost"` | Redis主机地址 |
| `port` | `int` | `6379` | Redis端口 |
| `db` | `int` | `0` | 数据库编号 |
| `password` | `Optional[str]` | `None` | 密码 |
| `max_connections` | `int` | `50` | 连接池最大连接数 |
| `decode_responses` | `bool` | `True` | 是否自动解码响应为字符串 |

---

### 🔧 字符串操作

#### set()

**功能**: 设置键值

**签名**:
```python
def set(
    key: str,
    value: Any,
    ex: Optional[int] = None,
    nx: bool = False,
) -> bool
```

**参数**:
- `key`: 键
- `value`: 值
- `ex`: 过期时间（秒）
- `nx`: 如果键不存在才设置

**示例**:
```python
# 设置键值
redis_client.set("user:1:name", "张三")

# 设置带过期时间的键
redis_client.set("session:abc123", "token_data", ex=3600)  # 1小时后过期

# 仅当键不存在时设置（NX模式）
success = redis_client.set("lock:order:1", "locked", nx=True)
```

---

#### get()

**功能**: 获取值

**签名**:
```python
def get(key: str) -> Optional[str]
```

**示例**:
```python
name = redis_client.get("user:1:name")
if name:
    print(f"用户名: {name}")
else:
    print("键不存在")
```

---

#### delete()

**功能**: 删除键

**签名**:
```python
def delete(*keys: str) -> int
```

**返回**: 删除的键数量

**示例**:
```python
# 删除单个键
count = redis_client.delete("user:1:name")

# 删除多个键
count = redis_client.delete("key1", "key2", "key3")
print(f"删除了 {count} 个键")
```

---

#### exists()

**功能**: 检查键是否存在

**签名**:
```python
def exists(*keys: str) -> int
```

**返回**: 存在的键数量

**示例**:
```python
if redis_client.exists("user:1:name"):
    print("键存在")

# 检查多个键
count = redis_client.exists("key1", "key2", "key3")
print(f"{count} 个键存在")
```

---

#### expire()

**功能**: 设置键的过期时间

**签名**:
```python
def expire(key: str, seconds: int) -> bool
```

**示例**:
```python
# 设置键在60秒后过期
redis_client.expire("session:abc123", 60)
```

---

#### ttl()

**功能**: 获取键的剩余过期时间

**签名**:
```python
def ttl(key: str) -> int
```

**返回**: 剩余秒数，-1表示永久，-2表示不存在

**示例**:
```python
ttl = redis_client.ttl("session:abc123")
if ttl > 0:
    print(f"还剩 {ttl} 秒过期")
elif ttl == -1:
    print("永久键")
else:
    print("键不存在")
```

---

### 🔧 哈希操作

#### hset()

**功能**: 设置哈希字段

**签名**:
```python
def hset(name: str, key: str, value: Any) -> int
```

**示例**:
```python
redis_client.hset("user:1", "name", "张三")
redis_client.hset("user:1", "age", "25")
```

---

#### hget()

**功能**: 获取哈希字段

**签名**:
```python
def hget(name: str, key: str) -> Optional[str]
```

**示例**:
```python
name = redis_client.hget("user:1", "name")
print(f"用户名: {name}")
```

---

#### hgetall()

**功能**: 获取哈希所有字段

**签名**:
```python
def hgetall(name: str) -> dict
```

**示例**:
```python
user = redis_client.hgetall("user:1")
print(f"用户信息: {user}")
# 输出: {"name": "张三", "age": "25"}
```

---

#### hdel()

**功能**: 删除哈希字段

**签名**:
```python
def hdel(name: str, *keys: str) -> int
```

**示例**:
```python
count = redis_client.hdel("user:1", "age")
```

---

### 🔧 列表操作

#### lpush() / rpush()

**功能**: 推入列表（左边/右边）

**签名**:
```python
def lpush(name: str, *values: Any) -> int
def rpush(name: str, *values: Any) -> int
```

**示例**:
```python
# 从左边推入
redis_client.lpush("queue", "task1", "task2")

# 从右边推入
redis_client.rpush("queue", "task3", "task4")
```

---

#### lpop() / rpop()

**功能**: 弹出元素（左边/右边）

**签名**:
```python
def lpop(name: str) -> Optional[str]
def rpop(name: str) -> Optional[str]
```

**示例**:
```python
# 从左边弹出
task = redis_client.lpop("queue")
if task:
    print(f"处理任务: {task}")
```

---

#### lrange()

**功能**: 获取列表范围

**签名**:
```python
def lrange(name: str, start: int, end: int) -> list
```

**示例**:
```python
# 获取所有元素
tasks = redis_client.lrange("queue", 0, -1)
print(f"队列中的任务: {tasks}")

# 获取前3个
tasks = redis_client.lrange("queue", 0, 2)
```

---

### 🔧 集合操作

#### sadd()

**功能**: 添加到集合

**签名**:
```python
def sadd(name: str, *values: Any) -> int
```

**示例**:
```python
redis_client.sadd("tags", "python", "testing", "automation")
```

---

#### smembers()

**功能**: 获取集合所有成员

**签名**:
```python
def smembers(name: str) -> set
```

**示例**:
```python
tags = redis_client.smembers("tags")
print(f"标签: {tags}")
```

---

#### srem()

**功能**: 从集合移除

**签名**:
```python
def srem(name: str, *values: Any) -> int
```

**示例**:
```python
redis_client.srem("tags", "python")
```

---

### 🔧 有序集合操作

#### zadd()

**功能**: 添加到有序集合

**签名**:
```python
def zadd(name: str, mapping: dict) -> int
```

**示例**:
```python
# 添加用户积分排行
redis_client.zadd(
    "leaderboard",
    {"user:1": 100, "user:2": 200, "user:3": 150}
)
```

---

#### zrange()

**功能**: 获取有序集合范围

**签名**:
```python
def zrange(
    name: str,
    start: int,
    end: int,
    withscores: bool = False
) -> list
```

**示例**:
```python
# 获取前3名
top3 = redis_client.zrange("leaderboard", 0, 2, withscores=True)
print(f"排行榜前3名: {top3}")
```

---

### 🔧 通用操作

#### ping()

**功能**: 测试连接

**签名**:
```python
def ping() -> bool
```

**示例**:
```python
if redis_client.ping():
    print("Redis连接正常")
```

---

#### keys()

**功能**: 获取匹配的键列表

**签名**:
```python
def keys(pattern: str = "*") -> list
```

**示例**:
```python
# 获取所有用户键
user_keys = redis_client.keys("user:*")

# 获取所有键
all_keys = redis_client.keys("*")
```

---

#### flushdb()

**功能**: 清空当前数据库

**签名**:
```python
def flushdb() -> bool
```

**示例**:
```python
redis_client.flushdb()  # ⚠️ 慎用！会删除当前db的所有数据
```

---

#### close()

**功能**: 关闭连接

**签名**:
```python
def close() -> None
```

**示例**:
```python
redis_client.close()
```

---

### 🎯 完整使用示例

```python
from df_test_framework import RedisClient

def test_redis_example():
    """RedisClient完整使用示例"""

    # 1. 创建Redis客户端
    redis_client = RedisClient(
        host="localhost",
        port=6379,
        db=0,
        password=None
    )

    try:
        # 2. 测试连接
        assert redis_client.ping(), "Redis连接失败"

        # 3. 字符串操作
        redis_client.set("user:1:name", "张三", ex=3600)
        name = redis_client.get("user:1:name")
        assert name == "张三"

        # 4. 哈希操作
        redis_client.hset("user:1", "name", "张三")
        redis_client.hset("user:1", "age", "25")
        user = redis_client.hgetall("user:1")
        print(f"用户信息: {user}")

        # 5. 列表操作（队列）
        redis_client.rpush("tasks", "task1", "task2", "task3")
        task = redis_client.lpop("tasks")
        print(f"处理任务: {task}")

        # 6. 集合操作（标签）
        redis_client.sadd("tags", "python", "testing")
        tags = redis_client.smembers("tags")
        print(f"标签: {tags}")

        # 7. 有序集合（排行榜）
        redis_client.zadd(
            "leaderboard",
            {"user:1": 100, "user:2": 200}
        )
        top_users = redis_client.zrange("leaderboard", 0, -1, withscores=True)
        print(f"排行榜: {top_users}")

        # 8. 清理测试数据
        redis_client.delete("user:1:name", "user:1", "tasks", "tags", "leaderboard")

    finally:
        # 9. 关闭连接
        redis_client.close()
```

---

## 🔗 相关文档

- [Testing API](testing.md) - Pytest Fixtures和测试辅助工具
- [Patterns API](patterns.md) - Builder和Repository模式
- [Infrastructure API](infrastructure.md) - Bootstrap和Runtime
- [快速入门](../getting-started/quickstart.md) - 5分钟上手指南

---

**返回**: [API参考首页](README.md) | [文档首页](../README.md)
