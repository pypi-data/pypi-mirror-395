# 测试框架使用示例

> **版本**: v2.0.0
> **最后更新**: 2026-01-15
> **框架状态**: ✅ 生产就绪

本文档提供测试框架的实际使用示例,涵盖所有核心功能和 v2.0.0 的新增特性。

## 🎯 使用前准备

### 确认框架已安装

```bash
python -c "from df_test_framework import __version__; print(f'框架版本: {__version__}')"
# 输出: 框架版本: 1.4.0
```

### 本文档涵盖的功能

- ✅ **核心功能**: HTTP、数据库、Redis、日志、装饰器
- ✅ **扩展能力**: Repository 模式、Builder 模式、QueryBuilder、性能监控
- ✅ **v2.0.0新增**: Bootstrap + RuntimeContext、插件系统、CLI 脚手架
- ✅ **实战示例**: 完整的测试用例编写

---

## 📖 目录

1. [HTTP客户端使用](#1-http客户端使用)
2. [API封装使用](#2-api封装使用)
3. [Repository模式](#3-repository模式) ⭐ v1.3.0新增
4. [Builder模式](#4-builder模式) ⭐ v1.3.0新增
5. [QueryBuilder查询条件构建](#5-querybuilder查询条件构建) ⭐ v1.4.0新增
6. [数据库操作](#6-数据库操作)
7. [日志系统](#7-日志系统)
8. [性能监控](#8-性能监控) ⭐ v1.3.0新增
9. [装饰器使用](#9-装饰器使用)
10. [类型和枚举](#10-类型和枚举)
11. [配置管理](#11-配置管理)
12. [Pytest Fixtures](#12-pytest-fixtures)
13. [完整测试示例](#13-完整测试示例)

---

## 1. HTTP客户端使用

### 基本使用

```python
from df_test_framework.core import HttpClient

# 方式一: 使用上下文管理器(推荐)
with HttpClient(
    base_url="https://api.example.com",
    timeout=30,
    max_retries=3
) as client:
    # GET请求
    response = client.get("/users")
    print(response.json())

    # POST请求
    response = client.post(
        "/users",
        json={"name": "张三", "email": "zhangsan@example.com"}
    )

    # 设置认证token
    client.set_auth_token("your_token_here")
    response = client.get("/protected/resource")

# 方式二: 手动管理
client = HttpClient(base_url="https://api.example.com")
try:
    response = client.get("/users")
finally:
    client.close()
```

### 高级配置

```python
# 自定义请求头
client = HttpClient(
    base_url="https://api.example.com",
    headers={
        "User-Agent": "MyTestFramework/1.0",
        "Accept-Language": "zh-CN"
    },
    verify_ssl=False  # 跳过SSL验证(仅用于测试环境)
)

# 自动重试配置 (v2.0.0增强特性)
client = HttpClient(
    base_url="https://api.example.com",
    max_retries=5,  # 最多重试5次
    timeout=60  # 60秒超时
)
```

> **✨ v2.0.0增强**: HTTP自动重试机制
>
> **功能**: 框架内置智能重试，自动处理临时性网络故障
>
> **工作原理**:
> - **最大重试次数**: max_retries=3 (默认)
> - **触发条件**: 自动重试以下错误
>   - `ConnectionError`: 网络连接失败
>   - `HTTP 502`: 网关错误
>   - `HTTP 503`: 服务不可用
>   - `HTTP 504`: 网关超时
> - **退避策略**: 指数退避 (exponential backoff)
>   - 第1次重试: 等待1秒
>   - 第2次重试: 等待2秒
>   - 第3次重试: 等待4秒
>
> **示例**:
> ```python
> # 自动重试示例
> client = HttpClient(
>     base_url="https://api.example.com",
>     max_retries=3,  # 3次重试
>     timeout=30
> )
>
> # 若服务返回502/503/504或网络故障，框架自动重试
> response = client.get("/users")  # 失败时自动重试，无需手动处理
> ```
>
> **最佳实践**:
> - 用于生产环境: `max_retries=3` (推荐)
> - 用于快速测试: `max_retries=1` (减少等待时间)
> - 禁用重试: `max_retries=0`

---

## 2. API封装使用

> **⚠️ 重要**: BaseAPI采用**依赖注入模式**,请参考 [BaseAPI最佳实践指南](../archive/v1/BaseAPI最佳实践指南.md) 了解详细设计理念。

### 创建API类 (依赖注入模式)

```python
# api/user_api.py
from df_test_framework.core import BaseAPI, HttpClient
from pydantic import BaseModel
from typing import List

# 定义响应模型
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: str

class UserListResponse(BaseModel):
    users: List[UserResponse]
    total: int

# 创建API封装类
class UserAPI(BaseAPI):
    """用户API封装

    设计模式: 依赖注入
    - 通过构造函数注入HttpClient实例
    - 支持多个API实例共享同一个HttpClient连接池
    - 便于测试时注入mock对象
    """

    def __init__(self, http_client: HttpClient):
        """初始化UserAPI

        Args:
            http_client: HTTP客户端实例(由外部创建和管理)

        Example:
            >>> client = HttpClient(base_url="http://api.example.com")
            >>> api = UserAPI(client)
        """
        super().__init__(http_client)
        self.base_path = "/users"

    def get_user(self, user_id: int) -> UserResponse:
        """获取单个用户"""
        response = self.client.get(f"{self.base_path}/{user_id}")
        return self._parse_response(response, UserResponse)

    def list_users(self, page: int = 1, size: int = 10) -> UserListResponse:
        """获取用户列表"""
        response = self.client.get(
            self.base_path,
            params={"page": page, "size": size}
        )
        return self._parse_response(response, UserListResponse)

    def create_user(self, name: str, email: str) -> UserResponse:
        """创建用户"""
        response = self.client.post(
            self.base_path,
            json={"name": name, "email": email}
        )
        return self._parse_response(response, UserResponse)

    def delete_user(self, user_id: int) -> dict:
        """删除用户"""
        response = self.client.delete(f"{self.base_path}/{user_id}")
        return self._parse_response(response)  # 返回字典
```

### 使用API类 - 方式1: 在pytest中使用fixtures (推荐)

```python
# tests/conftest.py
import pytest
from df_test_framework import HttpClient
from api.user_api import UserAPI

@pytest.fixture(scope="session")
def http_client() -> HttpClient:
    """提供共享的HTTP客户端 (session级别)"""
    client = HttpClient(base_url="https://api.example.com", timeout=30)
    yield client
    client.close()

@pytest.fixture(scope="function")
def user_api(http_client) -> UserAPI:
    """提供UserAPI实例 (function级别,注入session级别的http_client)"""
    return UserAPI(http_client)


# tests/test_user.py
def test_user_operations(user_api):
    """使用fixture自动注入API实例"""
    # 创建用户
    user = user_api.create_user(name="张三", email="zhangsan@test.com")
    assert user.name == "张三"

    # 获取用户
    user = user_api.get_user(user.id)
    assert user.email == "zhangsan@test.com"

    # 删除用户
    result = user_api.delete_user(user.id)
    assert result["success"] is True


def test_multiple_apis(user_api, order_api):
    """多个API共享同一个HttpClient"""
    # user_api和order_api共享底层连接池
    user = user_api.create_user(name="李四", email="lisi@test.com")
    order = order_api.create_order(user_id=user.id, amount=100.0)

    assert user.id == order.user_id
```

### 使用API类 - 方式2: 在脚本中手动管理

```python
# scripts/init_data.py
from df_test_framework import HttpClient
from api.user_api import UserAPI

def main():
    # 创建HttpClient
    http_client = HttpClient(base_url="https://api.example.com", timeout=30)

    try:
        # 注入HttpClient创建API实例
        user_api = UserAPI(http_client)

        # 使用API
        for i in range(10):
            user = user_api.create_user(
                name=f"用户{i}",
                email=f"user{i}@test.com"
            )
            print(f"创建用户: {user.name}")

    finally:
        # 关闭连接
        http_client.close()

if __name__ == "__main__":
    main()
```

### ✨ v2.0.0增强: 自动业务错误检查

> **功能**: BaseAPI内置自动错误检查机制，简化错误处理逻辑
>
> **工作原理**:
> - 当API返回 `code != 200` 时，框架自动抛出 `BusinessError` 异常
> - 无需手动检查 `response.success` 或 `response.code`
> - 异常包含完整的错误信息：code、message、data等
>
> **对比示例**:
> ```python
> # v1.x - 需要手动检查错误
> def create_user(self, name: str, email: str) -> UserResponse:
>     response = self.client.post(
>         self.base_path,
>         json={"name": name, "email": email}
>     )
>     # ❌ 需要手动检查
>     if response.get("code") != 200:
>         raise ValueError(f"创建失败: {response.get('message')}")
>     return self._parse_response(response, UserResponse)
>
> # v2.0.0 - 自动检查，无需手动处理
> def create_user(self, name: str, email: str) -> UserResponse:
>     response = self.client.post(
>         self.base_path,
>         json={"name": name, "email": email}
>     )
>     # ✅ code != 200自动抛出BusinessError，无需assert
>     return self._parse_response(response, UserResponse)
> ```
>
> **异常处理**:
> ```python
> from df_test_framework.exceptions import BusinessError
>
> try:
>     user = user_api.create_user(name="张三", email="invalid-email")
> except BusinessError as e:
>     print(f"业务错误: {e.code} - {e.message}")
>     # code: 400, message: "邮箱格式不正确"
> ```

### ⚠️ 常见错误示例

```python
# ❌ 错误: 不要在API类内部创建HttpClient
class UserAPI(BaseAPI):
    def __init__(self, base_url: str):
        # 错误: 违反依赖注入原则
        http_client = HttpClient(base_url=base_url)
        super().__init__(http_client)

# ❌ 错误: 每次都创建新的HttpClient
for i in range(100):
    client = HttpClient(base_url="http://api.example.com")
    api = UserAPI(client)
    api.create_user(...)
    client.close()  # 资源浪费!

# ✅ 正确: 共享HttpClient
client = HttpClient(base_url="http://api.example.com")
for i in range(100):
    api = UserAPI(client)  # 共享连接池
    api.create_user(...)
client.close()
```

> **💡 提示**: 详细了解依赖注入的优势和最佳实践,请阅读 [BaseAPI最佳实践指南](../archive/v1/BaseAPI最佳实践指南.md)

---

## 3. Repository模式 ⭐ v1.3.0新增

> **Repository模式**用于数据访问层抽象，将数据库操作封装，提升可测试性和代码可维护性。

### 创建Repository类

```python
from df_test_framework.repositories import BaseRepository
from df_test_framework.core import Database

class CardRepository(BaseRepository):
    """卡片数据仓库"""

    def __init__(self, db: Database):
        super().__init__(db, table_name="gift_cards")

    def find_by_card_no(self, card_no: str):
        """根据卡号查找卡片"""
        return self.find_one({"card_no": card_no})

    def find_active_cards(self):
        """查找所有激活的卡片"""
        return self.find_all({"status": "ACTIVE"})

    def activate_card(self, card_no: str):
        """激活卡片"""
        return self.update(
            {"card_no": card_no},
            {"status": "ACTIVE", "activated_at": "NOW()"}
        )

    def find_by_user(self, user_id: str):
        """查找用户的所有卡片"""
        return self.find_all({"user_id": user_id})
```

### 在测试中使用

```python
def test_card_operations(db_transaction):
    # 使用Repository访问数据库
    repo = CardRepository(db_transaction)

    # 查找卡片 - 返回 Dict[str, Any]
    card = repo.find_by_card_no("CARD001")
    assert card is not None
    assert isinstance(card, dict)  # 返回字典，非ORM对象
    assert card["status"] == "INACTIVE"

    # 激活卡片
    repo.activate_card("CARD001")

    # 验证
    card = repo.find_by_card_no("CARD001")
    assert card["status"] == "ACTIVE"

    # 查找用户的卡片 - 返回 List[Dict[str, Any]]
    cards = repo.find_by_user("user_123")
    assert len(cards) > 0
```

### ✨ v2.0.0增强: Repository返回字典类型

> **功能**: Repository查询返回 `Dict[str, Any]` 而非ORM对象，避免序列化问题
>
> **工作原理**:
> - 所有Repository的查询方法都返回字典而非SQLAlchemy/Django ORM对象
> - 字典使用列名作为键，可直接用于JSON序列化
> - 避免ORM对象序列化时的复杂性（lazy loading、循环引用等）
>
> **最佳实践**:
> ```python
> # 正确: 直接访问字典键
> card = repo.find_by_card_no("CARD001")
> card_no = card["card_no"]  # 字典访问
> status = card["status"]
>
> # 序列化JSON (字典自然支持)
> import json
> json_str = json.dumps(card)  # 无需特殊处理
> ```

### Repository的CRUD操作

```python
repo = CardRepository(db)

# Create - 创建单条
card_id = repo.create({"card_no": "CARD001", "amount": 100.0})

# Read - 读取单条
card = repo.find_by_id(card_id)
card = repo.find_one({"card_no": "CARD001"})
cards = repo.find_all({"status": "ACTIVE"})

# Update - 更新
repo.update({"card_no": "CARD001"}, {"status": "ACTIVE"})

# Delete - 删除
repo.delete({"card_no": "CARD001"})

# 批量操作 (v1.2.0+)
cards = [{"card_no": f"CARD{i}", "amount": 100.0} for i in range(10)]
repo.batch_create(cards)

repo.delete_by_ids([card_id1, card_id2, card_id3])
```

---

## 4. Builder模式 ⭐ v1.3.0新增

> **Builder模式**提供流畅的API来构建测试数据，提高代码可读性。

### 使用DictBuilder构建字典

```python
from df_test_framework.builders import DictBuilder

# 基础使用
request = (
    DictBuilder()
    .set("user_id", "user_001")
    .set("template_id", "template_001")
    .set("quantity", 5)
    .set("options", {"color": "red", "size": "large"})
    .build()
)
# 结果: {"user_id": "user_001", "template_id": "template_001", "quantity": 5, "options": {...}}

# set_many批量设置
request = (
    DictBuilder()
    .set("user_id", "user_001")
    .set_many({
        "template_id": "template_001",
        "quantity": 5,
        "priority": "high"
    })
    .build()
)
```

### 创建自定义Builder

```python
from df_test_framework.builders import BaseBuilder
from models.request.card_models import CreateCardRequest

class CardRequestBuilder(BaseBuilder):
    """礼品卡请求Builder"""

    def __init__(self):
        self.data = {
            "amount": 100.0,
            "card_type": "PHYSICAL",
            "quantity": 1,
            "description": "Default card"
        }

    def with_amount(self, amount: float):
        """设置金额"""
        self.data["amount"] = amount
        return self

    def with_card_type(self, card_type: str):
        """设置卡片类型"""
        self.data["card_type"] = card_type
        return self

    def with_quantity(self, quantity: int):
        """设置数量"""
        self.data["quantity"] = quantity
        return self

    def with_description(self, description: str):
        """设置描述"""
        self.data["description"] = description
        return self

    def build(self) -> CreateCardRequest:
        """构建请求对象"""
        return CreateCardRequest(**self.data)


# 使用自定义Builder
def test_create_cards():
    # 场景1: 创建单张卡片
    request = CardRequestBuilder().build()
    card = api.create_card(request)

    # 场景2: 创建多张高面值卡片
    request = (
        CardRequestBuilder()
        .with_amount(500.0)
        .with_quantity(10)
        .with_description("High value cards")
        .build()
    )
    cards = api.create_cards(request)

    # 场景3: 创建虚拟卡
    request = (
        CardRequestBuilder()
        .with_card_type("VIRTUAL")
        .with_amount(50.0)
        .build()
    )
    card = api.create_card(request)
```

### 使用场景化Builder

```python
class CardRequestBuilder(BaseBuilder):
    """支持场景化构建的Builder"""

    @classmethod
    def small_card(cls):
        """构建小额卡 (50元)"""
        builder = cls()
        builder.data["amount"] = 50.0
        builder.data["description"] = "Small card"
        return builder

    @classmethod
    def medium_card(cls):
        """构建中额卡 (100元)"""
        builder = cls()
        builder.data["amount"] = 100.0
        builder.data["description"] = "Medium card"
        return builder

    @classmethod
    def large_card(cls):
        """构建大额卡 (500元)"""
        builder = cls()
        builder.data["amount"] = 500.0
        builder.data["description"] = "Large card"
        return builder


# 使用场景化构建
def test_card_sizes():
    small_req = CardRequestBuilder.small_card().build()
    medium_req = CardRequestBuilder.medium_card().build()
    large_req = CardRequestBuilder.large_card().build()

    assert small_req.amount == 50.0
    assert medium_req.amount == 100.0
    assert large_req.amount == 500.0
```

---

## 5. QueryBuilder查询条件构建 ⭐ v1.4.0新增

> **QueryBuilder**用于灵活构建复杂的数据库查询条件，支持多种SQL操作符和逻辑组合。

### 基本使用

```python
from df_test_framework.repositories import QueryBuilder

# 方式一: 使用QueryBuilder
query = (
    QueryBuilder()
    .with_field("status").equals("ACTIVE")
    .with_field("amount").greater_than(100)
    .build()
)

# 方式二: 获取构建的SQL和参数
sql_conditions = query.get_conditions()
params = query.get_params()

# 使用在数据库查询中
result = db.query_all(
    f"SELECT * FROM cards WHERE {sql_conditions}",
    params
)
```

### 支持的操作符

```python
query = QueryBuilder()

# 等于操作
.with_field("status").equals("ACTIVE")

# 不等于操作
.with_field("status").not_equals("INACTIVE")

# 大于/小于
.with_field("amount").greater_than(100)
.with_field("amount").less_than(1000)
.with_field("amount").greater_than_or_equal(50)
.with_field("amount").less_than_or_equal(500)

# LIKE模糊查询
.with_field("name").like("%张%")
.with_field("email").like("%@example.com")

# IN操作
.with_field("status").in_list(["ACTIVE", "PENDING"])
.with_field("card_type").in_list(["PHYSICAL", "VIRTUAL"])

# BETWEEN范围查询
.with_field("created_at").between("2025-01-01", "2025-12-31")
.with_field("amount").between(50, 500)

# NULL检查
.with_field("deleted_at").is_null()
.with_field("updated_at").is_not_null()

.build()
```

### 逻辑操作组合

```python
from df_test_framework.repositories import QueryBuilder, QuerySpec

# AND操作 (默认)
query = (
    QueryBuilder()
    .with_field("status").equals("ACTIVE")
    .with_field("amount").greater_than(100)
    .build()
)
# 生成: status = 'ACTIVE' AND amount > 100

# OR操作
query = (
    QueryBuilder()
    .with_spec(
        QuerySpec.or_condition(
            QuerySpec("status", "equals", "ACTIVE"),
            QuerySpec("status", "equals", "PENDING")
        )
    )
    .build()
)
# 生成: (status = 'ACTIVE' OR status = 'PENDING')

# 复杂组合
query = (
    QueryBuilder()
    .with_field("status").equals("ACTIVE")
    .with_spec(
        QuerySpec.or_condition(
            QuerySpec("amount", "greater_than", 100),
            QuerySpec("amount", "less_than", 50)
        )
    )
    .build()
)
# 生成: status = 'ACTIVE' AND (amount > 100 OR amount < 50)
```

### 在Repository中使用

```python
class CardRepository(BaseRepository):
    """卡片仓库"""

    def __init__(self, db: Database):
        super().__init__(db, table_name="cards")

    def find_high_value_active_cards(self):
        """查找高面值活跃卡片"""
        query = (
            QueryBuilder()
            .with_field("status").equals("ACTIVE")
            .with_field("amount").greater_than(500)
            .build()
        )

        sql_conditions = query.get_conditions()
        params = query.get_params()

        return self.db.query_all(
            f"SELECT * FROM {self.table_name} WHERE {sql_conditions}",
            params
        )

    def find_cards_by_date_range(self, start_date, end_date):
        """按日期范围查找卡片"""
        query = (
            QueryBuilder()
            .with_field("created_at").between(start_date, end_date)
            .with_field("status").in_list(["ACTIVE", "COMPLETED"])
            .build()
        )

        return self.find_all_by_query(query)

    def find_cards_by_search(self, search_text, status=None):
        """搜索卡片"""
        query = QueryBuilder()

        # 模糊查询
        query.with_field("card_no").like(f"%{search_text}%")

        # 可选的状态过滤
        if status:
            query.with_field("status").equals(status)

        return self.find_all_by_query(query.build())
```

### 实际应用示例

```python
def test_find_cards_with_complex_conditions():
    """测试复杂查询条件"""
    repo = CardRepository(db)

    # 场景1: 查找一周内创建的高面值活跃卡片
    query = (
        QueryBuilder()
        .with_field("created_at").between("2025-10-24", "2025-10-30")
        .with_field("amount").greater_than(100)
        .with_field("status").equals("ACTIVE")
        .build()
    )

    cards = repo.find_all_by_query(query)
    assert len(cards) > 0

    # 场景2: 查找特定类型的卡片
    query = (
        QueryBuilder()
        .with_field("card_type").in_list(["PHYSICAL", "VIRTUAL"])
        .with_field("status").not_equals("DELETED")
        .build()
    )

    cards = repo.find_all_by_query(query)

    # 场景3: 查找未删除且有备注的卡片
    query = (
        QueryBuilder()
        .with_field("deleted_at").is_null()
        .with_field("remarks").is_not_null()
        .build()
    )

    cards = repo.find_all_by_query(query)

    # 场景4: 复杂的OR和AND组合
    query = (
        QueryBuilder()
        .with_field("status").equals("ACTIVE")
        .with_spec(
            QuerySpec.or_condition(
                QuerySpec("amount", "greater_than", 500),
                QuerySpec("user_vip_level", "equals", "GOLD")
            )
        )
        .build()
    )

    cards = repo.find_all_by_query(query)
```

---

## 6. 数据库操作

### 基本使用

```python
from df_test_framework.core import Database

# 创建数据库连接
db = Database(
    connection_string="mysql+pymysql://user:password@localhost:3306/testdb?charset=utf8mb4",
    pool_size=5,
    max_overflow=10
)

# 方式一: 使用上下文管理器
with db.session() as session:
    from sqlalchemy import text

    # 执行查询(参数化)
    result = session.execute(
        text("SELECT * FROM users WHERE id = :user_id"),
        {"user_id": 1}
    )
    user = result.fetchone()

# 方式二: 使用便捷方法
# 查询单条
user = db.query_one(
    "SELECT * FROM users WHERE id = :id",
    {"id": 1}
)

# 查询多条
users = db.query_all(
    "SELECT * FROM users WHERE status = :status",
    {"status": "active"}
)

# 插入数据
user_id = db.insert(
    "users",
    {
        "name": "张三",
        "email": "zhangsan@test.com",
        "status": "active"
    }
)

# 更新数据
affected = db.update(
    "users",
    data={"status": "inactive"},
    where="id = :id",
    where_params={"id": user_id}
)

# 删除数据
deleted = db.delete(
    "users",
    where="id = :id",
    where_params={"id": user_id}
)

# 关闭连接
db.close()
```

### 在pytest fixture中使用

```python
import pytest
from df_test_framework.core import Database

@pytest.fixture(scope="session")
def db_engine(settings):
    """数据库引擎(session级别,共享连接池)"""
    db = Database(settings.db_url)
    yield db
    db.close()

@pytest.fixture
def db_session(db_engine):
    """数据库会话(每个测试独立事务)"""
    with db_engine.session() as session:
        yield session
        # 自动回滚,保证测试隔离
        session.rollback()
```

---

## 7. 日志系统

### 配置日志

```python
from df_test_framework.logging import LoguruStructuredStrategy
from config.settings import get_settings

settings = get_settings()
strategy = LoguruStructuredStrategy()
logger = strategy.configure(settings.logging)
```

通常无需手动调用，Bootstrap 或 pytest 插件会在运行时自动配置日志。

### 使用日志

```python
from df_test_framework.core import logger

# 不同级别的日志
logger.debug("调试信息")
logger.info("普通信息")
logger.warning("警告信息")
logger.error("错误信息")
logger.critical("严重错误")

# 结构化日志
logger.info("用户登录", extra={
    "user_id": 123,
    "ip_address": "192.168.1.1"
})

# 敏感信息会自动脱敏
logger.info(f"password={password}")  # 输出: password=******
logger.info(f"token={token}")        # 输出: token=******
```

---

## 8. 性能监控 ⭐ v1.3.0新增

### 使用装饰器

```python
from df_test_framework.utils import track_performance

@track_performance(threshold_ms=500)
def test_api_performance():
    """测试API性能 - 应在500ms内完成"""
    response = api.get("/users")
    assert response.status_code == 200
    # 超过500ms会自动记录警告
```

### 使用计时器

```python
from df_test_framework.utils import PerformanceTimer

def test_database_performance():
    # 方式一: 上下文管理器
    with PerformanceTimer("数据库查询", threshold_ms=100) as timer:
        users = db.query_all("SELECT * FROM users")

    print(f"查询耗时: {timer.duration_ms}ms")

    # 方式二: 手动计时
    timer = PerformanceTimer("复杂操作", threshold_ms=1000)
    timer.__enter__()

    # 执行操作
    result = complex_operation()

    timer.__exit__(None, None, None)
    assert timer.duration_ms < 1000
```

### 使用收集器

```python
from df_test_framework.utils import PerformanceCollector

def test_batch_performance():
    collector = PerformanceCollector("批量API请求")

    # 执行100次请求
    for i in range(100):
        with collector.measure():
            response = api.get(f"/users/{i}")

    # 获取统计信息
    summary = collector.summary()
    print(f"总次数: {summary['count']}")
    print(f"平均耗时: {summary['avg_ms']}ms")
    print(f"最小耗时: {summary['min_ms']}ms")
    print(f"最大耗时: {summary['max_ms']}ms")

    # 记录到日志
    collector.log_summary()
```

---

## 9. 装饰器使用

### 重试装饰器

```python
from df_test_framework.utils import retry_on_failure
import httpx

@retry_on_failure(
    max_retries=3,
    delay=1.0,
    backoff=2.0,
    exceptions=(httpx.RequestError, httpx.TimeoutException)
)
def call_unstable_api():
    """调用不稳定的外部API"""
    return requests.get("https://unstable-api.com/data")

# 使用
try:
    data = call_unstable_api()
except Exception as e:
    print(f"重试3次后仍然失败: {e}")
```

### 执行日志装饰器

```python
from df_test_framework.utils import log_execution

@log_execution(log_args=True, log_result=True)
def process_user_data(user_id, action):
    """处理用户数据"""
    # 自动记录参数和返回值
    return {"user_id": user_id, "action": action, "status": "success"}
```

### 缓存装饰器

```python
from df_test_framework.utils import cache_result

@cache_result(ttl=60)
def get_config_from_remote():
    """从远程获取配置(60秒缓存)"""
    response = requests.get("https://api.com/config")
    return response.json()

# 第一次调用,从远程获取
config = get_config_from_remote()

# 60秒内再次调用,直接返回缓存
config = get_config_from_remote()

# 手动清除缓存
get_config_from_remote.clear_cache()
```

### 废弃标记

```python
from df_test_framework.utils import deprecated

@deprecated(message="请使用 new_function 替代", version="2.0.0")
def old_function():
    """已废弃的函数"""
    pass

# 调用时会记录警告日志
old_function()
```

---

## 10. 类型和枚举

### HTTP相关

```python
from df_test_framework.models import HttpMethod, HttpStatus

# 使用HTTP方法枚举
def make_request(method: HttpMethod, url: str):
    if method == HttpMethod.GET:
        return client.get(url)
    elif method == HttpMethod.POST:
        return client.post(url)

# 使用HTTP状态码枚举
def test_api_response():
    response = api.get("/users")
    assert response.status_code == HttpStatus.OK

    # 创建用户
    response = api.post("/users", json=data)
    assert response.status_code == HttpStatus.CREATED
```

### 测试相关

```python
from df_test_framework.models import TestPriority, TestType
import pytest
import allure

@pytest.mark.smoke
@allure.severity(TestPriority.CRITICAL)
class TestUserLogin:
    """用户登录测试"""

    def test_login_success(self):
        """测试登录成功"""
        pass

# 环境枚举
from df_test_framework.models import Environment

if settings.env == Environment.PROD:
    pytest.skip("生产环境跳过此测试")
```

---

## 11. 配置管理

### 注册与读取

```python
from df_test_framework import FrameworkSettings, configure_settings, get_settings


class ProjectSettings(FrameworkSettings):
    pass


configure_settings(ProjectSettings)
settings = get_settings()
print(settings.http.base_url)
```

### pytest 中的配置

```python
# tests/conftest.py
pytest_plugins = ["df_test_framework.fixtures.core"]

import pytest
from config.settings import get_settings


@pytest.fixture(scope="session")
def settings():
    return get_settings()
```

在 `pytest.ini` 或命令行指定配置类与插件：

```ini
[pytest]
df_settings_class = config.settings.ProjectSettings
df_plugins = my_project.plugins.metrics
```

```bash
pytest --df-settings-class=config.settings.ProjectSettings \
       --df-plugin my_project.plugins.metrics
```

### 多环境与覆盖

- `.env`：基础配置
- `.env.{ENV}`：环境特定配置（`ENV` 或 `APP_ENV` 控制）
- `.env.local`：个人覆盖，不提交

如需在测试中构造独立实例：

```python
from df_test_framework.config import create_settings
from config.settings import ProjectSettings

mock_settings = create_settings(
    settings_cls=ProjectSettings,
    overrides={"http": {"base_url": "http://mock-server"}},
)
```

---

## 12. Pytest Fixtures

> **✨ v2.0.0增强**: 引入 `db_transaction` fixture实现自动事务回滚
>
> **功能**: 在测试执行后自动回滚数据库事务，确保测试隔离
>
> **工作原理**:
> - 每个测试方法开启一个新事务
> - 测试执行完成后自动ROLLBACK
> - 避免手动数据清理，减少测试维护成本
> - 替代v1.x的 `data_cleaner` fixture
>
> **v1.x vs v2.0.0对比**:
> ```python
> # v1.x - 手动数据清理
> def test_create_card(api, data_cleaner):
>     card = api.create_card(amount=100)
>     data_cleaner.register("card_nos", card.card_no)  # 需要手动注册
>     assert card.amount == 100
>
> # v2.0.0 - 自动事务回滚，无需清理
> def test_create_card(api, db_transaction):
>     card = api.create_card(amount=100)  # 无需手动注册清理
>     assert card.amount == 100
>     # 测试结束自动ROLLBACK，数据库自动恢复
> ```

启用官方插件后，可直接使用内置 fixture：

- `runtime` → `RuntimeContext`
- `http_client` → 基于配置的 `HttpClient`
- `database` / `redis_client`
- `db_transaction` → **自动事务回滚** (v2.0.0新增)

```python
def test_health(http_client):
    resp = http_client.get("/health")
    assert resp.status_code == 200


def test_db(database):
    row = database.query_one("SELECT 1 AS num")
    assert row["num"] == 1
```

也可以在此基础上继续封装：

```python
import pytest


@pytest.fixture
def user_api(http_client):
    return UserAPI(http_client)


@pytest.fixture
def make_user(database, user_api):
    created_ids = []

    def _create(**payload):
        user = user_api.create_user(**payload)
        created_ids.append(user.id)
        return user

    yield _create

    for user_id in created_ids:
        database.delete("users", where="id = :id", where_params={"id": user_id})
```

## 13. 完整测试示例

### 完整的API测试

```python
import pytest
import allure
from decimal import Decimal
from df_test_framework.utils import track_performance
from df_test_framework.models import HttpStatus, TestPriority

@allure.epic("礼品卡系统")
@allure.feature("礼品卡管理")
class TestGiftCard:
    """礼品卡测试套件"""

    @allure.story("创建礼品卡")
    @allure.severity(TestPriority.CRITICAL)
    @pytest.mark.smoke
    @track_performance(threshold_ms=500)
    def test_create_gift_card_success(self, gift_card_api):
        """测试创建礼品卡 - 正常场景"""

        with allure.step("准备测试数据"):
            amount = Decimal("100.00")
            card_type = "PHYSICAL"

        with allure.step("调用创建API"):
            response = gift_card_api.create_card(
                amount=amount,
                card_type=card_type
            )

        with allure.step("验证响应"):
            assert response.status_code == HttpStatus.CREATED
            assert response.data.amount == amount
            assert response.data.card_type == card_type
            assert response.data.status == "INACTIVE"

        with allure.step("验证数据库"):
            card = db.query_one(
                "SELECT * FROM gift_cards WHERE id = :id",
                {"id": response.data.id}
            )
            assert card is not None
            assert card["amount"] == amount

    @allure.story("激活礼品卡")
    @pytest.mark.regression
    def test_activate_gift_card(self, gift_card_api, create_test_card):
        """测试激活礼品卡"""

        # 创建测试卡片
        card = create_test_card(amount=Decimal("100"))

        # 激活
        response = gift_card_api.activate_card(card.id)

        # 验证
        assert response.data.status == "ACTIVE"
        assert response.data.activated_at is not None

    @allure.story("查询礼品卡")
    @pytest.mark.parametrize("amount,expected", [
        (Decimal("50"), "SMALL"),
        (Decimal("100"), "MEDIUM"),
        (Decimal("500"), "LARGE"),
    ])
    def test_query_card_by_amount(
        self,
        gift_card_api,
        create_test_card,
        amount,
        expected
    ):
        """测试按金额查询礼品卡"""

        # 创建卡片
        card = create_test_card(amount=amount)

        # 查询
        cards = gift_card_api.query_cards(amount=amount)

        # 验证
        assert len(cards) > 0
        assert cards[0].size_category == expected
```

### 集成测试示例

```python
@allure.epic("端到端测试")
@allure.feature("购买流程")
class TestE2EPurchase:
    """端到端购买流程测试"""

    @pytest.mark.e2e
    @allure.story("完整购买流程")
    def test_complete_purchase_flow(
        self,
        user_api,
        gift_card_api,
        order_api,
        payment_api,
        db
    ):
        """测试完整的购买流程"""

        with allure.step("1. 创建用户"):
            user = user_api.create_user(
                name="测试用户",
                email="test@example.com"
            )
            allure.attach(str(user.dict()), "用户信息", allure.attachment_type.JSON)

        with allure.step("2. 创建礼品卡"):
            card = gift_card_api.create_card(amount=Decimal("100"))
            allure.attach(str(card.dict()), "卡片信息", allure.attachment_type.JSON)

        with allure.step("3. 创建订单"):
            order = order_api.create_order(
                user_id=user.id,
                card_id=card.id
            )
            assert order.status == "PENDING"

        with allure.step("4. 支付订单"):
            payment = payment_api.pay_order(
                order_id=order.id,
                payment_method="WECHAT"
            )
            assert payment.status == "SUCCESS"

        with allure.step("5. 验证订单状态"):
            order = order_api.get_order(order.id)
            assert order.status == "PAID"

        with allure.step("6. 验证卡片已激活"):
            card = gift_card_api.get_card(card.id)
            assert card.status == "ACTIVE"

        with allure.step("7. 清理测试数据"):
            # 自动清理由fixture处理
            pass
```

---

## 📝 更多示例

更多示例请参考:
- [架构设计](../archive/v1/architecture.md) - 完整的架构设计和最佳实践
- [优化报告](../archive/v1/optimization-report.md) - v1.x版本优化总结
- [代码示例目录](../../examples/) - 21个可运行的示例文件
- gift-card-test项目 - 实际测试项目示例

---

## 版本历史

### v1.4.0 (2025-10-30)
- ✅ 新增QueryBuilder灵活查询条件构建
- ✅ QueryBuilder完整使用示例和最佳实践
- ✅ QueryBuilder在Repository中的应用
- ✅ 复杂查询场景的实际应用示例

### v1.3.1 (2025-10-30)
- ✅ 完全更新所有示例到v1.3.1
- ✅ 新增Repository模式和Builder模式文档
- ✅ 更新database.execute()使用方式
- ✅ 新增v1.3.0/v1.3.1特性说明

### v1.3.0 (2025-10-29)
- ✅ Repository模式支持
- ✅ Builder模式支持
- ✅ 性能监控功能

### v1.2.0
- ✅ 中间件机制
- ✅ 嵌套配置模型
- ✅ 数据库批量操作

---

**文档版本**: v1.4.0
**最后更新**: 2025-10-30
**维护者**: DF QA Team
