# Databases API 参考

> 📖 **能力层3: Databases** - 数据访问模式
>
> 适用场景: MySQL、PostgreSQL、Redis、MongoDB等数据库访问

---

## 🎯 模块概述

**databases/** 模块提供数据访问能力，采用**扁平化**结构:

| 子模块 | 数据库类型 | 实现 | 状态 |
|--------|----------|------|------|
| `databases/database.py` | SQL通用 | SQLAlchemy | ✅ 已实现 |
| `databases/redis/` | Redis | redis-py | ✅ 已实现 |
| `databases/repositories/` | Repository模式 | - | ✅ 已实现 |
| `databases/mysql/` | MySQL专用 | - | 🔄 规划中 |
| `databases/postgresql/` | PostgreSQL | - | 🔄 规划中 |
| `databases/mongodb/` | MongoDB | - | 🔄 规划中 |

### v3架构优势

**扁平化设计**（无sql/nosql中间层）:
```
✅ v3: databases/redis/          # 简洁直观
❌ v2: engines/nosql/redis/     # 多余嵌套
```

---

## 📦 导入方式

### 推荐导入（顶层）

```python
from df_test_framework import (
    Database,
    RedisClient,
    BaseRepository,
    QuerySpec,
    UnitOfWork,  # v3.13.0+
)
```

### 完整路径导入

```python
from df_test_framework.databases.database import Database
from df_test_framework.databases.redis.redis_client import RedisClient
from df_test_framework.databases.repositories import BaseRepository, QuerySpec
from df_test_framework.databases.uow import UnitOfWork  # v3.13.0+
```

---

## 💾 Database - SQL数据库客户端

### 功能特性

- ✅ 基于SQLAlchemy实现
- ✅ 支持MySQL、PostgreSQL、SQLite
- ✅ 连接池管理
- ✅ 事务支持（transaction/savepoint）
- ✅ CRUD操作封装
- ✅ 批量插入优化
- ✅ 表名白名单保护

### 快速开始

```python
from df_test_framework import Database

# 创建数据库连接
db = Database(
    connection_string="mysql+pymysql://user:pass@localhost:3306/testdb",
    pool_size=10
)

# 插入数据
user_id = db.insert("users", {"name": "张三", "age": 25})

# 查询数据
user = db.query_one("SELECT * FROM users WHERE id = :id", {"id": user_id})
print(f"用户: {user['name']}")

# 更新数据
db.update("users", {"status": "ACTIVE"}, "id = :id", {"id": user_id})

# 删除数据
db.delete("users", "id = :id", {"id": user_id})

# 关闭连接
db.close()
```

### 核心方法

#### 查询方法
- `query_one(sql, params=None)` - 查询单条记录
- `query_all(sql, params=None)` - 查询多条记录

#### CRUD操作
- `insert(table, data)` - 插入记录，返回ID
- `batch_insert(table, data_list, chunk_size=1000)` - 批量插入
- `update(table, data, where, where_params)` - 更新记录
- `delete(table, where, where_params)` - 删除记录
- `execute(sql, params)` - 执行SQL

#### 事务管理
- `session()` - 获取会话上下文
- `transaction()` - 事务上下文
- `savepoint(name)` - 保存点

### 完整文档

详细API文档请参考: [core.md#Database](core.md#database)

---

## 🔴 RedisClient - Redis客户端

### 功能特性

- ✅ 基于redis-py实现
- ✅ 连接池管理
- ✅ 支持所有Redis数据类型
- ✅ 字符串、哈希、列表、集合、有序集合操作

### 快速开始

```python
from df_test_framework import RedisClient

# 创建Redis客户端
redis_client = RedisClient(
    host="localhost",
    port=6379,
    db=0
)

# 字符串操作
redis_client.set("user:1:name", "张三", ex=3600)  # 1小时过期
name = redis_client.get("user:1:name")

# 哈希操作
redis_client.hset("user:1", "name", "张三")
redis_client.hset("user:1", "age", "25")
user = redis_client.hgetall("user:1")

# 列表操作（队列）
redis_client.rpush("tasks", "task1", "task2")
task = redis_client.lpop("tasks")

# 集合操作
redis_client.sadd("tags", "python", "testing")
tags = redis_client.smembers("tags")

# 有序集合（排行榜）
redis_client.zadd("leaderboard", {"user:1": 100, "user:2": 200})
top_users = redis_client.zrange("leaderboard", 0, -1, withscores=True)

# 关闭连接
redis_client.close()
```

### 核心方法

#### 字符串操作
- `set(key, value, ex=None, nx=False)` - 设置键值
- `get(key)` - 获取值
- `delete(*keys)` - 删除键
- `exists(*keys)` - 检查键是否存在
- `expire(key, seconds)` - 设置过期时间
- `ttl(key)` - 获取剩余过期时间

#### 哈希操作
- `hset(name, key, value)` - 设置哈希字段
- `hget(name, key)` - 获取哈希字段
- `hgetall(name)` - 获取所有字段
- `hdel(name, *keys)` - 删除字段

#### 列表操作
- `lpush(name, *values)` / `rpush(name, *values)` - 推入
- `lpop(name)` / `rpop(name)` - 弹出
- `lrange(name, start, end)` - 获取范围

#### 集合操作
- `sadd(name, *values)` - 添加成员
- `smembers(name)` - 获取所有成员
- `srem(name, *values)` - 移除成员

#### 有序集合操作
- `zadd(name, mapping)` - 添加成员
- `zrange(name, start, end, withscores=False)` - 获取范围

#### 通用操作
- `ping()` - 测试连接
- `keys(pattern="*")` - 获取匹配键
- `flushdb()` - 清空数据库
- `close()` - 关闭连接

### 完整文档

详细API文档请参考: [core.md#RedisClient](core.md#redisclient)

---

## 🔄 UnitOfWork - Unit of Work模式 (v3.13.0+)

### 功能特性

**核心职责**:
- ✅ 统一管理事务边界
- ✅ 协调多个 Repository 操作
- ✅ 保证事务原子性（全部成功或全部失败）
- ✅ 支持自动回滚（测试场景）

**v3.13.0 重大更新**:
- 🔥 **配置驱动**: 无需自定义 UoW 类，只需配置 `TEST__REPOSITORY_PACKAGE`
- 🔥 **零样板代码**: 无需继承、无需覆盖 fixture
- 🔥 **Repository 自动发现**: 框架自动注册所有 Repository
- 🔥 **测试数据自动清理**: 测试结束自动回滚

### 快速开始 (v3.13.0)

#### 1. 配置 Repository 包路径

```env
# .env 文件
TEST__REPOSITORY_PACKAGE=your_project.repositories
```

#### 2. 在测试中直接使用

```python
# 无需任何自定义代码！
def test_create_user(uow):
    """测试创建用户 - 数据自动回滚"""
    # 创建用户（uow.users 自动发现 UserRepository）
    user_id = uow.users.create({
        "username": "test_user",
        "email": "test@example.com"
    })

    # 验证
    user = uow.users.find_by_id(user_id)
    assert user["username"] == "test_user"

    # ✅ 测试结束自动回滚，无需清理
```

#### 3. 手动创建 UnitOfWork（可选）

```python
from df_test_framework.databases import UnitOfWork

def create_order_with_payment(session_factory, user_id, amount):
    """创建订单并扣款"""
    with UnitOfWork(
        session_factory,
        repository_package="your_project.repositories"
    ) as uow:
        # 1. 创建订单
        order_id = uow.orders.create({
            "user_id": user_id,
            "amount": amount,
            "status": "pending"
        })

        # 2. 扣减用户余额
        uow.users.update(
            conditions={"id": user_id},
            data={"balance": uow.users.find_by_id(user_id)["balance"] - amount}
        )

        # 3. 提交事务
        uow.commit()

        return order_id
```

### 核心方法

#### `__init__(session_factory)`

初始化 UnitOfWork。

**参数**:
- `session_factory`: SQLAlchemy session factory

**示例**:
```python
from sqlalchemy.orm import sessionmaker

session_factory = sessionmaker(bind=engine)
uow = ProjectUoW(session_factory)
```

#### `repository(repository_class)`

获取 Repository 实例。

**参数**:
- `repository_class`: Repository 类

**返回**: Repository 实例

**示例**:
```python
with uow:
    user_repo = uow.repository(UserRepository)
    order_repo = uow.repository(OrderRepository)
```

#### `commit()`

提交事务，持久化所有更改。

**示例**:
```python
with uow:
    uow.users.create({"username": "alice"})
    uow.commit()  # ✅ 持久化到数据库
```

#### `rollback()`

回滚事务，撤销所有更改。

**示例**:
```python
with uow:
    try:
        uow.users.create({"username": "bob"})
        raise Exception("出错了")
    except:
        uow.rollback()  # 回滚创建操作
```

### 最佳实践

#### ✅ DO - 推荐做法

**1. 使用配置驱动（v3.13.0 推荐）**
```env
# .env
TEST__REPOSITORY_PACKAGE=your_project.repositories
```

**2. 测试使用框架 uow fixture**
```python
def test_example(uow):
    # ✅ 自动发现 Repository，自动回滚
    uow.users.create({"username": "test"})
```

**3. 多表操作使用同一 UoW**
```python
def test_multi_table(uow):
    uow.orders.create({...})
    uow.payments.create({...})
    # ✅ 测试结束自动回滚
```

#### ❌ DON'T - 避免做法

**1. 不要忘记 commit**
```python
# ❌ 错误：忘记 commit，数据不会保存
with uow:
    uow.users.create({"username": "alice"})
    # 缺少 uow.commit()
```

**2. 不要在测试中 commit**
```python
# ❌ 错误：测试中 commit 会持久化数据
def test_example(uow):
    uow.users.create({"username": "test"})
    uow.commit()  # ❌ 不要在测试中 commit
```

**3. 不要使用多个 UoW 操作同一业务**
```python
# ❌ 错误：事务不一致
with ProjectUoW(sf) as uow1:
    uow1.orders.create({...})

with ProjectUoW(sf) as uow2:
    uow2.payments.create({...})
```

### 与 v3.6 的区别

| 特性 | v3.6 | v3.7 |
|------|------|------|
| Repository 构造 | `Repository(database)` | `Repository(session)` |
| 事务管理 | 手动 `with database.transaction()` | 自动 `with uow:` |
| 测试清理 | 手动清理 | 自动回滚 |
| 多表操作 | 独立事务 | 统一事务 |

**迁移指南**: [v3.6→v3.7迁移指南](../../docs/migration/v3.6-to-v3.7.md)

### 完整文档

- [v3.7 示例代码](../../examples/08-v37-features/)
- [迁移指南](../../docs/migration/v3.6-to-v3.7.md)
- [用户手册 - 测试数据管理](../user-guide/USER_MANUAL.md#7-测试数据管理)

---

## 🏛️ BaseRepository - Repository模式

### 功能特性

- ✅ 封装数据访问逻辑
- ✅ 统一CRUD接口
- ✅ 参数化查询（防SQL注入）
- ✅ 批量操作优化
- ✅ 返回字典类型（不返回模型）

> ⭐ **已验证**: BaseRepository的设计模式已通过gift-card-test项目验证。详见 [已验证最佳实践](../user-guide/VERIFIED_BEST_PRACTICES.md#3-baserepository最佳实践)

### 核心设计原则（已验证）

**来自框架源码** (`databases/repositories/base.py:291`):

```python
"""Repository基类

封装数据访问逻辑,提供统一的CRUD接口

所有查询方法返回字典(Dict[str, Any])或字典列表(List[Dict[str, Any]])
子类可以根据需要在自己的方法中转换为Pydantic模型

v2.0.0 简化设计 - 移除无用的泛型声明,所有方法直接返回字典类型
"""
```

**关键原则**:
1. ✅ **返回字典**: 所有方法返回`Dict[str, Any]`或`List[Dict[str, Any]]`
2. ✅ **不返回模型**: Repository不负责对象映射
3. ✅ **防止SQL注入**: 使用参数化查询（`:key`占位符）
4. ✅ **不处理事务**: 事务由`db_transaction` fixture管理

### 快速开始（推荐模式）

```python
from typing import Optional, List, Dict, Any
from df_test_framework import Database, BaseRepository


class UserRepository(BaseRepository):
    """用户Repository

    对应数据表: users

    ✅ 已验证特性:
    - 返回Dict[str, Any]类型
    - 参数化查询防止SQL注入
    - 使用内置方法优先
    """

    def __init__(self, db: Database):
        super().__init__(db, table_name="users")

    # ===== 简单查询（使用内置方法）=====

    def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """根据邮箱查找用户

        Returns:
            Dict: 用户数据字典，或None
        """
        return self.find_one({"email": email})

    def find_active_users(self) -> List[Dict[str, Any]]:
        """查找所有活跃用户

        Returns:
            List[Dict]: 用户列表
        """
        return self.find_all(
            conditions={"status": "ACTIVE"},
            order_by="created_at DESC"
        )

    def count_active_users(self) -> int:
        """统计活跃用户数量

        Returns:
            int: 用户数量
        """
        return self.count({"status": "ACTIVE"})

    # ===== 复杂查询（自定义SQL）=====

    def find_by_age_range(
        self,
        min_age: int,
        max_age: int
    ) -> List[Dict[str, Any]]:
        """查找年龄范围内的用户

        Args:
            min_age: 最小年龄
            max_age: 最大年龄

        Returns:
            List[Dict]: 用户列表
        """
        sql = """
            SELECT *
            FROM users
            WHERE age BETWEEN :min_age AND :max_age
              AND status = 'ACTIVE'
            ORDER BY age ASC
        """
        return self.db.query_all(sql, {
            "min_age": min_age,
            "max_age": max_age,
        })

    def get_user_statistics(self) -> Dict[str, Any]:
        """获取用户统计信息（聚合查询）

        Returns:
            Dict: 统计数据
            {
                "total": 100,
                "active": 80,
                "inactive": 20,
                "avg_age": 28.5
            }
        """
        sql = """
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN status = 'ACTIVE' THEN 1 ELSE 0 END) as active,
                SUM(CASE WHEN status = 'INACTIVE' THEN 1 ELSE 0 END) as inactive,
                AVG(age) as avg_age
            FROM users
        """
        result = self.db.query_one(sql)
        return result if result else {}


# 使用
db = Database("mysql+pymysql://user:pass@localhost:3306/testdb")
repo = UserRepository(db)

# 查询（返回字典）
user = repo.find_by_email("zhangsan@example.com")  # Dict[str, Any]
print(f"用户名: {user['name']}")  # 直接访问字典

active_users = repo.find_active_users()  # List[Dict[str, Any]]
for user in active_users:
    print(f"用户: {user['name']}, 年龄: {user['age']}")

# 统计
count = repo.count_active_users()  # int
print(f"活跃用户数: {count}")
```

### 核心方法（内置）

BaseRepository提供**9个内置方法**（已验证）:

#### 查询方法

```python
# 主键查询
user = repo.find_by_id(1)  # Optional[Dict[str, Any]]
user = repo.find_by_id(1, id_column="user_id")  # 自定义主键列名

# 条件查询（单条）
user = repo.find_one({"email": "test@example.com"})

# 条件查询（多条）
users = repo.find_all()  # 全部
users = repo.find_all({"status": "ACTIVE"})  # 条件
users = repo.find_all(
    conditions={"status": "ACTIVE"},
    order_by="created_at DESC",
    limit=10
)

# IN查询
users = repo.find_by_ids([1, 2, 3])  # List[Dict[str, Any]]
users = repo.find_by_ids([1, 2, 3], id_column="user_id")
```

#### 统计方法

```python
# 统计数量
count = repo.count()  # 全部
count = repo.count({"status": "ACTIVE"})  # 条件统计

# 检查存在
exists = repo.exists({"email": "test@example.com"})  # bool
```

#### 写入方法

```python
# 创建（返回ID）
user_id = repo.create({
    "name": "张三",
    "email": "zhangsan@example.com",
    "age": 25,
})

# 批量创建
affected = repo.batch_create([
    {"name": "张三", "email": "zhangsan@example.com"},
    {"name": "李四", "email": "lisi@example.com"},
], chunk_size=1000)

# 更新
affected = repo.update(
    conditions={"email": "zhangsan@example.com"},
    data={"status": "INACTIVE"}
)

# 删除
affected = repo.delete({"email": "zhangsan@example.com"})
affected = repo.delete_by_ids([1, 2, 3])
```

### 实际验证案例

以下是经过gift-card-test项目验证的完整Repository实现：

```python
# 来自: gift-card-test/src/gift_card_test/repositories/template_repository.py

from typing import Optional, List, Dict, Any
from decimal import Decimal
from df_test_framework import Database, BaseRepository


class TemplateRepository(BaseRepository):
    """卡模板Repository

    对应数据表: card_template

    ✅ 已验证:
    - 所有方法返回Dict[str, Any]
    - 参数化查询防止SQL注入
    - 不处理事务（由db_transaction管理）
    """

    def __init__(self, db: Database):
        super().__init__(db, table_name="card_template")

    def find_by_template_id(self, template_id: str) -> Optional[Dict[str, Any]]:
        """根据模板编号查找

        Returns:
            Dict: 模板数据
            {
                "id": 1,
                "template_id": "TMPL001",
                "name": "通用礼品卡",
                "face_value": Decimal("100.00"),
                "status": 1,
                ...
            }
        """
        return self.find_one({"template_id": template_id})

    def find_active_templates(self) -> List[Dict[str, Any]]:
        """查找所有启用的模板"""
        return self.find_all(
            conditions={"status": 1},
            order_by="created_at DESC"
        )

    def count_active_templates(self) -> int:
        """统计启用的模板数量"""
        return self.count({"status": 1})

    def find_by_face_value_range(
        self,
        min_value: Decimal,
        max_value: Decimal
    ) -> List[Dict[str, Any]]:
        """查找指定面值范围的模板（复杂查询示例）

        ✅ 已验证: 参数化查询防止SQL注入
        """
        sql = """
            SELECT *
            FROM card_template
            WHERE face_value BETWEEN :min_value AND :max_value
              AND status = 1
            ORDER BY face_value ASC
        """
        return self.db.query_all(sql, {
            "min_value": str(min_value),
            "max_value": str(max_value),
        })

    def get_template_statistics(self) -> Dict[str, Any]:
        """获取模板统计信息（聚合查询示例）

        ✅ 已验证: 聚合查询和空值处理

        Returns:
            Dict: 统计数据
            {
                "total": 100,
                "active": 80,
                "inactive": 20,
                "avg_face_value": "125.50"
            }
        """
        sql = """
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN status = 1 THEN 1 ELSE 0 END) as active,
                SUM(CASE WHEN status = 0 THEN 1 ELSE 0 END) as inactive,
                AVG(face_value) as avg_face_value
            FROM card_template
        """
        result = self.db.query_one(sql)
        return result if result else {}


# 在测试中使用（配合db_transaction）
def test_query_templates(template_repository, db_transaction):
    """测试查询模板

    ✅ 已验证: Repository + db_transaction 自动回滚
    """
    # 查询模板（返回字典）
    template = template_repository.find_by_template_id("TMPL001")
    assert template is not None
    assert template["name"] == "通用礼品卡"  # 直接访问字典

    # 统计
    count = template_repository.count_active_templates()
    assert count > 0

    # 测试结束后自动回滚（db_transaction）
```

### 事务管理（重要）⚠️

**重要**: Repository本身**不处理事务**，事务由`db_transaction` fixture管理。

```python
# ✅ 正确：使用db_transaction
def test_create_template(
    template_repository,
    db_transaction,  # ✅ 添加此参数
):
    """测试创建模板（自动回滚）"""
    template_id = template_repository.create({
        "template_id": "TEST001",
        "name": "测试模板",
    })
    assert template_id > 0
    # 测试结束后自动回滚，数据不保留


# ❌ 错误：不使用db_transaction
def test_create_template(template_repository):
    """数据会真实写入，不会回滚"""
    template_id = template_repository.create({...})
    # ❌ 数据会保留在数据库中


# ❌ 错误：在Repository中自己管理事务
class TemplateRepository(BaseRepository):
    def create_with_transaction(self, data):
        with self.db.session() as session:  # ❌ 不要这样做
            trans = session.begin()
            # ...
            trans.commit()
```

**db_transaction** (v3.6.2 框架内置，无需手动定义):

```python
# tests/conftest.py
# 只需导入框架插件，db_transaction 由框架提供
pytest_plugins = ["df_test_framework.testing.fixtures.core"]

# db_transaction 返回 SQLAlchemy Session，默认自动回滚
# 支持三种方式保留数据：
# 1. @pytest.mark.keep_data 标记
# 2. --keep-test-data 命令行参数
# 3. KEEP_TEST_DATA=1 环境变量
```

详见: [FRAMEWORK_ARCHITECTURE_v3.6.2.md](../architecture/FRAMEWORK_ARCHITECTURE_v3.6.2.md)

### 完整文档

- 详细用法: [已验证最佳实践](../user-guide/VERIFIED_BEST_PRACTICES.md#3-baserepository最佳实践)
- 事务管理: [已验证最佳实践](../user-guide/VERIFIED_BEST_PRACTICES.md#4-fixtures和事务管理最佳实践)

---

## 🔍 QuerySpec - 查询构建器

### 功能特性

- ✅ 类型安全的查询构建
- ✅ 支持所有SQL操作符
- ✅ 可组合查询条件

### 快速开始

```python
from df_test_framework import QuerySpec

# 相等查询
spec = QuerySpec("status", QuerySpec.Operator.EQ, "ACTIVE")

# 范围查询
spec = QuerySpec("age", QuerySpec.Operator.BETWEEN, (20, 30))

# 模糊查询
spec = QuerySpec("name", QuerySpec.Operator.LIKE, "%张%")

# IN查询
spec = QuerySpec("role", QuerySpec.Operator.IN, ["admin", "user"])

# 组合查询（AND）
spec1 = QuerySpec("status", QuerySpec.Operator.EQ, "ACTIVE")
spec2 = QuerySpec("age", QuerySpec.Operator.GT, 18)
combined_spec = spec1 & spec2

# 组合查询（OR）
combined_spec = spec1 | spec2
```

### 支持的操作符

- `EQ` (=) - 等于
- `NE` (!=) - 不等于
- `GT` (>) - 大于
- `GTE` (>=) - 大于等于
- `LT` (<) - 小于
- `LTE` (<=) - 小于等于
- `LIKE` - 模糊匹配
- `IN` - 包含于
- `NOT_IN` - 不包含于
- `BETWEEN` - 范围
- `IS_NULL` - 为空
- `IS_NOT_NULL` - 不为空

### 完整文档

详细API文档请参考: [patterns.md#QuerySpec](patterns.md#queryspec)

---

## 🔗 相关文档

### 架构设计
- [v3架构设计](../architecture/V3_ARCHITECTURE.md) - databases扁平化设计
- [数据访问模式](../architecture/V3_ARCHITECTURE.md#数据访问) - 为什么统一为databases

### 其他能力层
- [Clients API](clients.md) - 请求-响应模式
- [Drivers API](drivers.md) - 会话式交互模式

### 测试支持
- [Testing API](testing.md) - database fixture和数据清理
- [Infrastructure API](infrastructure.md) - DatabaseConfig配置

### v2兼容
- [Core API](core.md) - v2版Database/Redis文档
- [Patterns API](patterns.md) - v2版Repository文档

---

**返回**: [API参考首页](README.md) | [文档首页](../README.md)
