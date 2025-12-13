# 测试数据工具使用指南

> 本指南介绍 df-test-framework 提供的测试数据生成和加载工具。
>
> **版本**: v3.10.0+
> **更新**: 2025-11-25

---

## 概述

测试数据工具包含三大模块：

| 模块 | 功能 | 使用场景 |
|------|------|---------|
| **Factories** | 数据生成器 | 快速生成测试数据 |
| **Loaders** | 数据加载器 | 从文件加载测试数据 |
| **Assertions** | 断言辅助 | 简化响应验证 |

---

## 1. 数据工厂 (Factories)

### 1.1 预置工厂

框架提供8个开箱即用的数据工厂：

```python
from df_test_framework.testing.factories import (
    UserFactory,      # 用户数据
    OrderFactory,     # 订单数据
    ProductFactory,   # 商品数据
    AddressFactory,   # 地址数据
    PaymentFactory,   # 支付数据
    CardFactory,      # 卡券数据
    ApiResponseFactory,   # API响应
    PaginationFactory,    # 分页数据
)
```

### 1.2 基础用法

```python
from df_test_framework.testing.factories import UserFactory, OrderFactory

# 生成单个对象
user = UserFactory.build()
print(user)
# {
#     'id': 1,
#     'user_id': 'a1b2c3d4-...',
#     'username': 'user_1',
#     'email': 'user_1@example.com',
#     'phone': '13812345678',
#     'name': '张三',
#     'status': 'active',
#     'role': 'user',
#     'created_at': datetime(2025, 11, 25, 10, 30, 0)
# }

# 批量生成
users = UserFactory.build_batch(100)
print(len(users))  # 100

# 覆盖默认值
admin = UserFactory.build(
    username="admin",
    role="admin",
    is_superuser=True
)
```

### 1.3 订单示例

```python
from df_test_framework.testing.factories import OrderFactory
from datetime import datetime

# 待支付订单
pending_order = OrderFactory.build()

# 已支付订单
paid_order = OrderFactory.build(
    status="paid",
    paid_at=datetime.now()
)

# 批量生成订单
orders = OrderFactory.build_batch(50)
```

### 1.4 自定义工厂

```python
from df_test_framework.testing.factories import (
    Factory,
    Sequence,
    LazyAttribute,
    FakerAttribute,
)

class CustomerFactory(Factory):
    """自定义客户工厂"""

    id = Sequence()
    customer_no = Sequence(lambda n: f"CUST-{str(n).zfill(6)}")
    name = FakerAttribute("name")
    company = FakerAttribute("company")
    email = LazyAttribute(lambda obj: f"{obj.customer_no.lower()}@example.com")
    level = "silver"
    created_at = LazyAttribute(lambda _: datetime.now())

# 使用
customer = CustomerFactory.build()
vip_customer = CustomerFactory.build(level="gold")
```

### 1.5 API响应模拟

```python
from df_test_framework.testing.factories import ApiResponseFactory, PaginationFactory

# 成功响应
success_resp = ApiResponseFactory.build(
    code=0,
    message="success",
    data={"user_id": 123}
)

# 错误响应
error_resp = ApiResponseFactory.build(
    code=400,
    message="参数错误",
    data=None
)

# 分页响应
page = PaginationFactory.build(
    total=100,
    page=1,
    page_size=20,
    items=UserFactory.build_batch(20)
)
```

---

## 2. 数据加载器 (Loaders)

### 2.1 支持格式

| 格式 | 加载器 | 依赖 |
|------|-------|------|
| JSON | `JSONLoader` | 内置 |
| CSV/TSV | `CSVLoader` | 内置 |
| YAML | `YAMLLoader` | pyyaml |

### 2.2 JSON加载

```python
from df_test_framework.testing.data import JSONLoader

# 加载JSON文件
users = JSONLoader.load("tests/data/users.json")

# 加载单条数据
first_user = JSONLoader.load_one("tests/data/users.json", index=0)

# 从字符串解析
data = JSONLoader.loads('{"name": "Alice", "age": 25}')

# 加载JSON Lines (.jsonl)
logs = JSONLoader.load_lines("tests/data/logs.jsonl")

# 保存数据
JSONLoader.save(users, "output/users.json")
```

### 2.3 CSV加载

```python
from df_test_framework.testing.data import CSVLoader

# 加载CSV（带表头）
products = CSVLoader.load("tests/data/products.csv")

# 加载TSV（制表符分隔）
data = CSVLoader.load("data.tsv", delimiter="\t")

# 类型转换
users = CSVLoader.load(
    "users.csv",
    type_hints={
        "age": int,
        "score": float,
        "active": bool
    }
)

# 加载为元组（适合pytest参数化）
test_cases = CSVLoader.load_as_tuples("test_data.csv")
# [('input1', 'expected1'), ('input2', 'expected2'), ...]

# 在pytest中使用
@pytest.mark.parametrize("input_val,expected", CSVLoader.load_as_tuples("test_data.csv"))
def test_calculation(input_val, expected):
    assert calculate(int(input_val)) == int(expected)
```

### 2.4 YAML加载

```python
from df_test_framework.testing.data import YAMLLoader

# 加载YAML配置
config = YAMLLoader.load("config.yaml")

# 加载多文档YAML
docs = YAMLLoader.load_all("multi.yaml")

# 环境变量替换
# config.yaml:
# database:
#   host: ${DB_HOST:localhost}
#   password: ${DB_PASSWORD}
config = YAMLLoader.load("config.yaml", expand_env=True)

# 合并多个配置文件
config = YAMLLoader.merge(
    "config/base.yaml",
    "config/dev.yaml"  # 后面的覆盖前面的
)
```

### 2.5 数据驱动测试

```python
import pytest
from df_test_framework.testing.data import JSONLoader, CSVLoader

# 方式1: JSON数据驱动
test_data = JSONLoader.load("tests/data/login_cases.json")

@pytest.mark.parametrize("case", test_data)
def test_login(case, http_client):
    response = http_client.post("/auth/login", json={
        "username": case["username"],
        "password": case["password"]
    })
    assert response.status_code == case["expected_status"]


# 方式2: CSV数据驱动
@pytest.mark.parametrize(
    "username,password,expected",
    CSVLoader.load_as_tuples("tests/data/login_cases.csv")
)
def test_login_csv(username, password, expected, http_client):
    response = http_client.post("/auth/login", json={
        "username": username,
        "password": password
    })
    assert response.status_code == int(expected)
```

---

## 3. 断言辅助 (Assertions)

### 3.1 响应断言

```python
from df_test_framework.testing.assertions import (
    ResponseAssertions,
    assert_status,
    assert_success,
    assert_json_has,
    assert_json_equals,
    assert_content_type,
)

# 状态码断言
assert_status(response, 200)
assert_status(response, 201)

# 成功响应断言 (2xx)
assert_success(response)

# JSON字段断言
assert_json_has(response, "user_id", "name", "email")

# JSON值断言
assert_json_equals(response, {"code": 0, "message": "success"})

# 严格模式（完全匹配）
assert_json_equals(response, expected_data, strict=True)

# Content-Type断言
assert_content_type(response, "application/json")
```

### 3.2 链式断言

```python
from df_test_framework.testing.assertions import ResponseAssertions

# 链式调用多个断言
ResponseAssertions(response) \
    .status(200) \
    .success() \
    .json_has("user_id", "name") \
    .json_equals({"code": 0}) \
    .header_has("Content-Type", "application/json") \
    .response_time_lt(1000)  # 响应时间小于1秒
```

### 3.3 高级断言

```python
from df_test_framework.testing.assertions import ResponseAssertions

# 响应时间断言
ResponseAssertions.assert_response_time_lt(response, 500)  # <500ms

# 响应头断言
ResponseAssertions.assert_header_has(response, "X-Request-Id")
ResponseAssertions.assert_header_has(response, "Content-Type", "application/json")

# 客户端/服务端错误断言
ResponseAssertions.assert_client_error(response)  # 4xx
ResponseAssertions.assert_server_error(response)  # 5xx

# 字段不存在断言
ResponseAssertions.assert_json_not_has(response, "password", "secret")

# JSONPath断言（需要jsonpath-ng）
ResponseAssertions.assert_json_path_equals(response, "$.data.user.name", "Alice")

# JSON Schema断言（需要jsonschema）
schema = {
    "type": "object",
    "required": ["id", "name"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"}
    }
}
ResponseAssertions.assert_json_schema(response, schema)
```

---

## 4. 完整示例

### 4.1 API测试示例

```python
"""用户API测试示例"""
import pytest
from df_test_framework.testing.factories import UserFactory, ApiResponseFactory
from df_test_framework.testing.assertions import ResponseAssertions, assert_status, assert_json_has
from df_test_framework.testing.data import JSONLoader


class TestUserAPI:
    """用户API测试"""

    def test_create_user(self, http_client):
        """测试创建用户"""
        # 准备测试数据
        user_data = UserFactory.build_dict()
        del user_data["id"]  # 移除自动生成的ID

        # 发送请求
        response = http_client.post("/api/users", json=user_data)

        # 断言响应
        ResponseAssertions(response) \
            .status(201) \
            .json_has("id", "username", "email") \
            .response_time_lt(1000)

    def test_get_user(self, http_client, created_user):
        """测试获取用户"""
        response = http_client.get(f"/api/users/{created_user['id']}")

        assert_status(response, 200)
        assert_json_has(response, "id", "username")

    @pytest.mark.parametrize("case", JSONLoader.load("tests/data/user_validation_cases.json"))
    def test_create_user_validation(self, http_client, case):
        """测试用户创建验证"""
        response = http_client.post("/api/users", json=case["input"])

        assert response.status_code == case["expected_status"]
        if case.get("expected_message"):
            assert case["expected_message"] in response.json().get("message", "")
```

### 4.2 数据驱动测试示例

```python
"""数据驱动测试示例"""
import pytest
from df_test_framework.testing.data import CSVLoader, YAMLLoader


# 从CSV加载测试用例
class TestCalculator:
    """计算器测试（CSV数据驱动）"""

    @pytest.mark.parametrize(
        "a,b,expected",
        CSVLoader.load_as_tuples("tests/data/add_cases.csv")
    )
    def test_add(self, a, b, expected):
        assert int(a) + int(b) == int(expected)


# 从YAML加载复杂测试用例
class TestOrderProcess:
    """订单处理测试（YAML数据驱动）"""

    test_cases = YAMLLoader.load("tests/data/order_cases.yaml")

    @pytest.mark.parametrize("case", test_cases)
    def test_order_flow(self, http_client, case):
        # 创建订单
        response = http_client.post("/api/orders", json=case["order_data"])
        assert response.status_code == case["expected"]["create_status"]

        if case.get("pay"):
            # 支付订单
            order_id = response.json()["id"]
            pay_response = http_client.post(f"/api/orders/{order_id}/pay")
            assert pay_response.status_code == case["expected"]["pay_status"]
```

---

## 5. 最佳实践

### 5.1 测试数据组织

```
tests/
├── data/
│   ├── users.json          # 用户测试数据
│   ├── products.csv        # 商品测试数据
│   ├── config.yaml         # 测试配置
│   └── cases/
│       ├── login_cases.json    # 登录测试用例
│       └── order_cases.yaml    # 订单测试用例
├── factories/
│   └── custom_factories.py # 自定义工厂
└── conftest.py            # pytest配置
```

### 5.2 自定义工厂放置

```python
# tests/factories/custom_factories.py
from df_test_framework.testing.factories import Factory, Sequence, FakerAttribute

class MyCustomFactory(Factory):
    """项目特定的数据工厂"""
    ...

# tests/conftest.py
from tests.factories.custom_factories import MyCustomFactory

@pytest.fixture
def custom_data():
    return MyCustomFactory.build()
```

### 5.3 重置序列计数器

```python
from df_test_framework.testing.factories import Sequence, UserFactory

class TestUser:
    def setup_method(self):
        """每个测试前重置序列"""
        Sequence.reset()

    def test_user_id_starts_from_1(self):
        user = UserFactory.build()
        assert user["id"] == 1
```

---

## 6. 依赖说明

| 功能 | 依赖 | 安装命令 |
|------|------|---------|
| Faker数据生成 | faker | `pip install faker` |
| YAML加载 | pyyaml | `pip install pyyaml` |
| JSONPath查询 | jsonpath-ng | `pip install jsonpath-ng` |
| JSON Schema验证 | jsonschema | `pip install jsonschema` |

框架已包含faker和pyyaml作为默认依赖，无需额外安装。

---

## 7. API参考

### 7.1 Factory方法

| 方法 | 描述 |
|------|------|
| `build(**overrides)` | 构建单个对象 |
| `build_batch(size, **overrides)` | 批量构建 |
| `build_dict(**overrides)` | 构建字典 |
| `reset_sequences()` | 重置序列计数器 |

### 7.2 Loader方法

| 方法 | 描述 |
|------|------|
| `load(file_path)` | 加载文件 |
| `loads(content)` | 从字符串解析 |
| `load_one(file_path, index)` | 加载单条数据 |
| `load_all(file_path)` | 加载所有数据（返回列表） |
| `save(data, file_path)` | 保存数据 |
| `exists(file_path)` | 检查文件是否存在 |

### 7.3 ResponseAssertions方法

| 方法 | 描述 |
|------|------|
| `assert_status(response, expected)` | 状态码断言 |
| `assert_success(response)` | 2xx断言 |
| `assert_json_has(response, *keys)` | 字段存在断言 |
| `assert_json_equals(response, expected)` | JSON值断言 |
| `assert_json_schema(response, schema)` | Schema断言 |
| `assert_header_has(response, name, value)` | 响应头断言 |
| `assert_response_time_lt(response, max_ms)` | 响应时间断言 |

---

**文档结束**

如有问题，请查阅[API参考](../api-reference/)或提交[Issue](https://github.com/yourorg/df-test-framework/issues)。
