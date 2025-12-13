# Patterns API 参考

> ⚠️ **v3架构说明**: 此文档为v2遗留内容，提供向后兼容参考。v3架构中:
> - **Builder模式** 已迁移至 [`testing/data/builders/`](testing.md#builders) 模块（测试数据构建）
> - **Repository模式** 已迁移至 [`databases/repositories/`](databases.md#repository) 模块（数据访问）
>
> 建议使用**顶层导入**（如下所示），无需关心内部路径变化。
>
> 📖 完整迁移指南: [v2-to-v3 迁移文档](../migration/v2-to-v3.md)

设计模式层的完整API参考，包含Builder模式和Repository模式的实现。

---

## 📦 模块导入

```python
# Builder模式
from df_test_framework import BaseBuilder, DictBuilder

# Repository模式
from df_test_framework import BaseRepository

# 查询构建器
from df_test_framework import QuerySpec

# 或者从具体模块导入（v3架构路径）
from df_test_framework.testing.data.builders import BaseBuilder, DictBuilder
from df_test_framework.databases.repositories import BaseRepository, QuerySpec
```

---

## 🏗️ Builder模式

Builder模式用于构建测试数据，提供流畅的链式API，使测试数据构建更清晰、更易维护。

### BaseBuilder - 抽象Builder基类

**说明**: Builder基类，定义Builder模式的标准接口。子类需要实现`build()`方法。

**泛型**: `BaseBuilder[T]` - T为构建的目标类型

#### 核心方法

##### build()

**功能**: 构建最终对象（抽象方法，子类必须实现）

**签名**:
```python
@abstractmethod
def build(self) -> T
```

---

##### reset()

**功能**: 重置Builder到初始状态

**签名**:
```python
def reset() -> BaseBuilder
```

**返回**: self（支持链式调用）

---

#### 使用示例 - 自定义Builder

```python
from df_test_framework import BaseBuilder
from pydantic import BaseModel

# 1. 定义数据模型
class CardRequest(BaseModel):
    user_id: str
    template_id: str
    quantity: int

# 2. 实现Builder
class CardRequestBuilder(BaseBuilder[CardRequest]):
    """卡片请求Builder"""

    def __init__(self):
        # 设置默认值
        self._user_id = "default_user"
        self._template_id = "default_template"
        self._quantity = 1

    def with_user(self, user_id: str) -> "CardRequestBuilder":
        """设置用户ID"""
        self._user_id = user_id
        return self

    def with_template(self, template_id: str) -> "CardRequestBuilder":
        """设置模板ID"""
        self._template_id = template_id
        return self

    def with_quantity(self, quantity: int) -> "CardRequestBuilder":
        """设置数量"""
        self._quantity = quantity
        return self

    def build(self) -> CardRequest:
        """构建CardRequest对象"""
        return CardRequest(
            user_id=self._user_id,
            template_id=self._template_id,
            quantity=self._quantity
        )

# 3. 使用Builder
request = (
    CardRequestBuilder()
    .with_user("user_001")
    .with_quantity(5)
    .build()
)

assert request.user_id == "user_001"
assert request.quantity == 5
```

---

### DictBuilder - 字典Builder

**说明**: 简化版Builder，直接构建字典对象，适用于简单的测试数据构建场景。

#### 初始化

```python
builder = DictBuilder()

# 或使用初始数据
builder = DictBuilder(initial_data={"user_id": "user_001"})
```

**参数**:
- `initial_data`: 初始数据字典（会被深拷贝）

---

#### 核心方法

##### set()

**功能**: 设置字段值

**签名**:
```python
def set(key: str, value: Any) -> DictBuilder
```

**参数**:
- `key`: 字段名
- `value`: 字段值

**返回**: self（支持链式调用）

**示例**:
```python
builder.set("user_id", "user_001").set("quantity", 5)
```

---

##### set_many()

**功能**: 批量设置字段值

**签名**:
```python
def set_many(**kwargs: Any) -> DictBuilder
```

**参数**:
- `**kwargs`: 字段名和值的键值对

**示例**:
```python
builder.set_many(
    user_id="user_001",
    quantity=5,
    status="ACTIVE"
)
```

---

##### get()

**功能**: 获取字段值

**签名**:
```python
def get(key: str, default: Any = None) -> Any
```

**参数**:
- `key`: 字段名
- `default`: 默认值

**示例**:
```python
user_id = builder.get("user_id", "default_user")
```

---

##### has()

**功能**: 检查字段是否存在

**签名**:
```python
def has(key: str) -> bool
```

**示例**:
```python
if builder.has("optional_field"):
    print("字段存在")
```

---

##### remove()

**功能**: 移除字段

**签名**:
```python
def remove(key: str) -> DictBuilder
```

**示例**:
```python
builder.remove("optional_field")
```

---

##### merge()

**功能**: 合并其他字典数据

**签名**:
```python
def merge(other_data: Dict[str, Any]) -> DictBuilder
```

**参数**:
- `other_data`: 要合并的字典（会覆盖同名字段）

**示例**:
```python
builder.merge({
    "status": "ACTIVE",
    "balance": 100.0
})
```

---

##### build()

**功能**: 构建字典对象

**签名**:
```python
def build() -> Dict[str, Any]
```

**返回**: 构建的字典（深拷贝的副本）

**示例**:
```python
data = builder.build()
```

---

##### clone()

**功能**: 克隆当前Builder

**签名**:
```python
def clone() -> DictBuilder
```

**返回**: 新的DictBuilder实例（包含当前数据的深拷贝）

**示例**:
```python
# 基于现有Builder创建新Builder
builder2 = builder.clone().set("user_id", "user_002")
```

---

#### 完整使用示例

```python
from df_test_framework import DictBuilder

def test_dict_builder_example():
    """DictBuilder完整使用示例"""

    # 1. 创建Builder
    builder = DictBuilder()

    # 2. 设置字段
    data = (
        builder
        .set("user_id", "user_001")
        .set("template_id", "tpl_001")
        .set("quantity", 5)
        .set("status", "ACTIVE")
        .build()
    )

    assert data == {
        "user_id": "user_001",
        "template_id": "tpl_001",
        "quantity": 5,
        "status": "ACTIVE"
    }

    # 3. 批量设置
    builder2 = (
        DictBuilder()
        .set_many(
            name="张三",
            age=25,
            email="zhangsan@example.com"
        )
    )

    # 4. 获取字段
    name = builder2.get("name")
    assert name == "张三"

    # 5. 检查字段
    assert builder2.has("email")
    assert not builder2.has("phone")

    # 6. 合并数据
    builder2.merge({"status": "ACTIVE", "balance": 100.0})

    # 7. 移除字段
    builder2.remove("balance")

    # 8. 克隆Builder
    builder3 = builder2.clone().set("name", "李四")

    # 9. 构建最终数据
    user = builder3.build()
    print(f"用户: {user}")
```

---

#### 实战场景 - 测试数据变体

```python
def test_create_card_variants():
    """使用DictBuilder创建测试数据变体"""

    # 基础数据模板
    base_request = (
        DictBuilder()
        .set("user_id", "user_001")
        .set("template_id", "tpl_001")
        .set("quantity", 1)
        .set("status", "ACTIVE")
    )

    # 场景1: 正常卡片
    normal_card = base_request.clone().build()

    # 场景2: 批量卡片
    batch_card = base_request.clone().set("quantity", 100).build()

    # 场景3: 停用状态卡片
    inactive_card = base_request.clone().set("status", "INACTIVE").build()

    # 场景4: 特殊用户卡片
    vip_card = (
        base_request.clone()
        .set("user_id", "vip_user")
        .merge({"vip_level": 5, "discount": 0.8})
        .build()
    )
```

---

## 💾 Repository模式

Repository模式封装数据访问逻辑，提供统一的CRUD接口，隔离业务逻辑和数据访问细节。

### BaseRepository - Repository基类

**说明**: Repository基类，封装通用的数据库CRUD操作。子类继承后可扩展业务特定的查询方法。

#### 初始化

```python
from df_test_framework import Database, BaseRepository

class UserRepository(BaseRepository):
    def __init__(self, db: Database):
        super().__init__(db, table_name="users")

# 使用
db = Database(connection_string="...")
repo = UserRepository(db)
```

**参数**:
- `db`: 数据库实例
- `table_name`: 表名

---

### 查询方法

#### find_by_id()

**功能**: 根据ID查找记录

**签名**:
```python
def find_by_id(
    id_value: Any,
    id_column: str = "id"
) -> Optional[Dict[str, Any]]
```

**参数**:
- `id_value`: ID值
- `id_column`: ID列名（默认`"id"`）

**返回**: 记录字典，如果不存在返回`None`

**示例**:
```python
# 查找ID=123的记录
record = repo.find_by_id(123)

# 使用自定义ID列
user = repo.find_by_id("user_001", id_column="user_id")
```

---

#### find_one()

**功能**: 根据条件查找单条记录

**签名**:
```python
def find_one(conditions: Dict[str, Any]) -> Optional[Dict[str, Any]]
```

**参数**:
- `conditions`: 查询条件字典

**示例**:
```python
# 查找单个用户
user = repo.find_one({"email": "zhangsan@example.com"})

# 多条件查询
card = repo.find_one({
    "card_no": "CARD001",
    "status": "ACTIVE"
})
```

---

#### find_all()

**功能**: 根据条件查找多条记录

**签名**:
```python
def find_all(
    conditions: Optional[Dict[str, Any]] = None,
    order_by: Optional[str] = None,
    limit: Optional[int] = None,
) -> List[Dict[str, Any]]
```

**参数**:
- `conditions`: 查询条件字典（`None`表示查询所有）
- `order_by`: 排序字段（如`"created_at DESC"`）
- `limit`: 限制返回记录数

**示例**:
```python
# 查询所有激活用户
active_users = repo.find_all({"status": "ACTIVE"})

# 带排序和限制
recent_users = repo.find_all(
    conditions={"status": "ACTIVE"},
    order_by="created_at DESC",
    limit=100
)

# 查询所有记录
all_users = repo.find_all()
```

---

#### find_by_ids()

**功能**: 根据ID列表批量查找记录

**签名**:
```python
def find_by_ids(
    id_values: List[Any],
    id_column: str = "id"
) -> List[Dict[str, Any]]
```

**参数**:
- `id_values`: ID值列表
- `id_column`: ID列名（默认`"id"`）

**示例**:
```python
# 批量查找卡片
cards = repo.find_by_ids(
    ["CARD001", "CARD002", "CARD003"],
    id_column="card_no"
)
```

---

#### count()

**功能**: 统计记录数

**签名**:
```python
def count(conditions: Optional[Dict[str, Any]] = None) -> int
```

**参数**:
- `conditions`: 查询条件字典（`None`表示统计所有）

**示例**:
```python
# 统计总用户数
total = repo.count()

# 统计活跃用户数
active_count = repo.count({"status": "ACTIVE"})
```

---

#### exists()

**功能**: 检查记录是否存在

**签名**:
```python
def exists(conditions: Dict[str, Any]) -> bool
```

**示例**:
```python
# 检查卡号是否已存在
exists = repo.exists({"card_no": "CARD001"})
if exists:
    print("卡号已存在")
```

---

### 写入方法

#### create()

**功能**: 创建记录

**签名**:
```python
def create(data: Dict[str, Any]) -> int
```

**参数**:
- `data`: 记录数据字典

**返回**: 插入的记录ID（如果数据库支持）

**示例**:
```python
card_id = repo.create({
    "card_no": "CARD001",
    "user_id": "user_001",
    "status": "ACTIVE",
    "balance": 100.0
})
print(f"新卡片ID: {card_id}")
```

---

#### batch_create()

**功能**: 批量创建记录

**签名**:
```python
def batch_create(
    data_list: List[Dict[str, Any]],
    chunk_size: int = 1000
) -> int
```

**参数**:
- `data_list`: 记录数据列表
- `chunk_size`: 每批次大小（默认1000）

**返回**: 插入的总记录数

**示例**:
```python
cards_data = [
    {"card_no": "CARD001", "status": "ACTIVE"},
    {"card_no": "CARD002", "status": "ACTIVE"},
    {"card_no": "CARD003", "status": "ACTIVE"},
]

count = repo.batch_create(cards_data, chunk_size=500)
print(f"批量创建 {count} 条记录")
```

---

#### update()

**功能**: 更新记录

**签名**:
```python
def update(
    conditions: Dict[str, Any],
    data: Dict[str, Any]
) -> int
```

**参数**:
- `conditions`: 更新条件字典
- `data`: 更新数据字典

**返回**: 影响的行数

**示例**:
```python
# 更新卡号为CARD001的记录状态
affected = repo.update(
    conditions={"card_no": "CARD001"},
    data={"status": "INACTIVE"}
)
print(f"更新了 {affected} 条记录")
```

---

#### delete()

**功能**: 删除记录

**签名**:
```python
def delete(conditions: Dict[str, Any]) -> int
```

**参数**:
- `conditions`: 删除条件字典

**返回**: 影响的行数

**示例**:
```python
deleted = repo.delete({"card_no": "CARD001"})
print(f"删除了 {deleted} 条记录")
```

---

#### delete_by_ids()

**功能**: 根据ID列表批量删除记录

**签名**:
```python
def delete_by_ids(
    id_values: List[Any],
    id_column: str = "id"
) -> int
```

**参数**:
- `id_values`: ID值列表
- `id_column`: ID列名（默认`"id"`）

**示例**:
```python
deleted = repo.delete_by_ids(
    ["CARD001", "CARD002"],
    id_column="card_no"
)
print(f"批量删除 {deleted} 条记录")
```

---

### 完整使用示例

```python
from df_test_framework import Database, BaseRepository
from typing import Optional, List, Dict, Any

# 1. 定义Repository
class CardRepository(BaseRepository):
    """卡片数据仓库"""

    def __init__(self, db: Database):
        super().__init__(db, table_name="card_inventory")

    # 扩展业务特定方法
    def find_by_card_no(self, card_no: str) -> Optional[Dict[str, Any]]:
        """根据卡号查找卡片"""
        return self.find_one({"card_no": card_no})

    def find_active_cards(self) -> List[Dict[str, Any]]:
        """查找所有激活的卡片"""
        return self.find_all(
            conditions={"status": "ACTIVE"},
            order_by="created_at DESC"
        )

    def find_by_user(self, user_id: str) -> List[Dict[str, Any]]:
        """查找用户的所有卡片"""
        return self.find_all({"user_id": user_id})

    def activate_card(self, card_no: str) -> int:
        """激活卡片"""
        return self.update(
            conditions={"card_no": card_no},
            data={"status": "ACTIVE"}
        )

# 2. 使用Repository
def test_card_repository():
    """卡片Repository使用示例"""

    db = Database(connection_string="sqlite:///./test.db")
    repo = CardRepository(db)

    # 创建卡片
    card_id = repo.create({
        "card_no": "CARD001",
        "user_id": "user_001",
        "status": "ACTIVE",
        "balance": 100.0
    })

    # 查找卡片
    card = repo.find_by_card_no("CARD001")
    assert card is not None
    assert card["status"] == "ACTIVE"

    # 查找用户的所有卡片
    user_cards = repo.find_by_user("user_001")
    assert len(user_cards) > 0

    # 更新卡片
    affected = repo.update(
        conditions={"card_no": "CARD001"},
        data={"balance": 200.0}
    )

    # 批量创建
    cards_data = [
        {"card_no": f"CARD{i:03d}", "user_id": "user_001", "status": "ACTIVE"}
        for i in range(2, 11)
    ]
    count = repo.batch_create(cards_data)
    print(f"批量创建 {count} 张卡片")

    # 统计
    total = repo.count()
    active_count = repo.count({"status": "ACTIVE"})
    print(f"总卡片数: {total}, 激活卡片数: {active_count}")

    # 删除
    repo.delete({"card_no": "CARD001"})
```

---

## 🔍 QuerySpec - 查询构建器

**说明**: 高级查询构建器，支持复杂SQL查询条件的链式构建。

> **注意**: QuerySpec是高级特性，适用于复杂查询场景。简单查询可直接使用`find_one()`/`find_all()`。

### 支持的操作

- **精确匹配**: `==`, `!=`
- **大小比较**: `>`, `>=`, `<`, `<=`
- **模糊查询**: `like()`
- **列表查询**: `in_list()`
- **范围查询**: `between()`
- **NULL检查**: `is_null()`, `is_not_null()`
- **逻辑组合**: `&` (AND), `|` (OR)

---

### 基础用法

```python
from df_test_framework.patterns.repositories import QuerySpec

# 1. 相等查询
spec = QuerySpec("status") == "ACTIVE"

# 2. 大小比较
spec = QuerySpec("amount") > 100

# 3. 范围查询
spec = QuerySpec("amount").between(100, 500)

# 4. 模糊查询
spec = QuerySpec("name").like("%test%")

# 5. 列表查询
spec = QuerySpec("status").in_list(["ACTIVE", "PENDING"])

# 6. NULL检查
spec = QuerySpec("deleted_at").is_null()
```

---

### 逻辑组合

```python
# AND组合（使用 & 运算符）
spec = (
    (QuerySpec("status") == "ACTIVE") &
    (QuerySpec("amount") > 100)
)

# OR组合（使用 | 运算符）
spec = (
    (QuerySpec("status") == "ACTIVE") |
    (QuerySpec("status") == "PENDING")
)

# 复杂组合
spec = (
    (QuerySpec("status") == "ACTIVE") &
    (
        (QuerySpec("amount").between(100, 500)) |
        (QuerySpec("vip_level") >= 5)
    )
)
```

---

### 获取SQL和参数

```python
# 方式1: 获取WHERE子句
clause = spec.to_where_clause()
sql = f"SELECT * FROM users WHERE {clause.sql}"
params = clause.params

# 方式2: 直接获取SQL和参数
sql, params = spec.get_where_sql_and_params()
```

---

### 与Repository集成（需要扩展）

由于BaseRepository默认接受字典条件，要使用QuerySpec需要扩展Repository：

```python
from df_test_framework import BaseRepository
from df_test_framework.patterns.repositories import QuerySpec

class AdvancedRepository(BaseRepository):
    """支持QuerySpec的Repository"""

    def find_by_spec(
        self,
        spec: QuerySpec,
        order_by: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """使用QuerySpec查询"""
        # 获取WHERE SQL和参数
        clause = spec.to_where_clause()

        # 构建完整SQL
        sql = f"SELECT * FROM {self.table_name} WHERE {clause.sql}"

        if order_by:
            sql += f" ORDER BY {order_by}"
        if limit:
            sql += f" LIMIT {limit}"

        # 执行查询
        return self.db.query_all(sql, clause.params)

# 使用示例
class CardRepository(AdvancedRepository):
    def __init__(self, db):
        super().__init__(db, table_name="cards")

# 查询
repo = CardRepository(db)
spec = (
    (QuerySpec("status") == "ACTIVE") &
    (QuerySpec("balance").between(100, 500))
)
cards = repo.find_by_spec(spec, order_by="created_at DESC")
```

---

### 完整使用示例

```python
from df_test_framework.patterns.repositories import QuerySpec

def test_query_spec_examples():
    """QuerySpec完整使用示例"""

    # 1. 简单查询
    spec1 = QuerySpec("status") == "ACTIVE"
    sql, params = spec1.get_where_sql_and_params()
    # SQL: status = :param
    # params: {'param': 'ACTIVE'}

    # 2. 范围查询
    spec2 = QuerySpec("amount").between(100, 500)
    sql, params = spec2.get_where_sql_and_params()
    # SQL: amount BETWEEN :param_start AND :param_end
    # params: {'param_start': 100, 'param_end': 500}

    # 3. 列表查询
    spec3 = QuerySpec("status").in_list(["ACTIVE", "PENDING", "PROCESSING"])
    sql, params = spec3.get_where_sql_and_params()
    # SQL: status IN (:param_0,:param_1,:param_2)
    # params: {'param_0': 'ACTIVE', 'param_1': 'PENDING', 'param_2': 'PROCESSING'}

    # 4. 模糊查询
    spec4 = QuerySpec("name").like("%test%")
    sql, params = spec4.get_where_sql_and_params()
    # SQL: name LIKE :param
    # params: {'param': '%test%'}

    # 5. NULL检查
    spec5 = QuerySpec("deleted_at").is_null()
    sql, params = spec5.get_where_sql_and_params()
    # SQL: deleted_at IS NULL
    # params: {}

    # 6. AND组合
    spec6 = (
        (QuerySpec("status") == "ACTIVE") &
        (QuerySpec("amount") > 100)
    )
    sql, params = spec6.get_where_sql_and_params()
    # SQL: (status = :param_l) AND (amount > :param_r)

    # 7. OR组合
    spec7 = (
        (QuerySpec("status") == "DELETED") |
        (QuerySpec("status") == "ARCHIVED")
    )

    # 8. 复杂组合
    spec8 = (
        (QuerySpec("status") == "ACTIVE") &
        (QuerySpec("amount").between(100, 500)) &
        (QuerySpec("user_level") >= 5)
    )

    # 9. 实战场景：查找VIP用户的高价值订单
    spec9 = (
        (QuerySpec("user_level") >= 5) &  # VIP用户
        (QuerySpec("order_amount") > 1000) &  # 高价值订单
        (QuerySpec("status").in_list(["PAID", "PROCESSING"])) &  # 有效状态
        (QuerySpec("deleted_at").is_null())  # 未删除
    )
```

---

## 🎯 Builder + Repository组合使用

Builder和Repository常配合使用，构建完整的测试数据流程：

```python
from df_test_framework import Database, BaseRepository, DictBuilder

def test_builder_repository_integration():
    """Builder + Repository组合使用"""

    db = Database(connection_string="sqlite:///./test.db")
    repo = CardRepository(db)

    # 1. 使用DictBuilder构建测试数据
    card_data = (
        DictBuilder()
        .set("card_no", "CARD001")
        .set("user_id", "user_001")
        .set("status", "ACTIVE")
        .set("balance", 100.0)
        .build()
    )

    # 2. 使用Repository创建数据
    card_id = repo.create(card_data)

    # 3. 使用Repository查询数据
    card = repo.find_by_card_no("CARD001")
    assert card is not None

    # 4. 使用Builder创建批量数据
    cards_data = [
        DictBuilder()
        .set("card_no", f"CARD{i:03d}")
        .set("user_id", "user_001")
        .set("status", "ACTIVE")
        .build()
        for i in range(2, 11)
    ]

    # 5. 批量创建
    count = repo.batch_create(cards_data)
    assert count == 9

    # 6. 查询验证
    user_cards = repo.find_by_user("user_001")
    assert len(user_cards) == 10
```

---

## 🔗 相关文档

- [Core API](core.md) - HttpClient、Database、RedisClient
- [Testing API](testing.md) - Pytest Fixtures和测试辅助工具
- [Infrastructure API](infrastructure.md) - Bootstrap和Runtime
- [快速入门](../getting-started/quickstart.md) - 5分钟上手指南

---

**返回**: [API参考首页](README.md) | [文档首页](../README.md)
