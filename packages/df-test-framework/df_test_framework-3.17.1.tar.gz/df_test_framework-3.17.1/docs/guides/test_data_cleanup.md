# 测试数据清理指南

> 本指南介绍如何在 API 测试中正确管理和清理测试数据。
>
> **版本**: v3.12.1+
> **更新**: 2025-12-02

---

## 概述

API 测试中的数据来源有两种，清理方式不同：

| 数据来源 | 事务归属 | 清理方式 |
|---------|---------|---------|
| Repository 直接创建 | 测试代码事务 | UoW 自动回滚 |
| API 调用创建 | 被测系统事务 | 需显式清理 |

**核心问题**：API 调用创建的数据已被后端事务提交，测试代码的 UoW 回滚无法影响这些数据。

---

## 1. 统一配置

v3.12.1 起，使用统一的 `should_keep_test_data()` 检查配置，同时控制 **UoW 回滚** 和 **API 数据清理**：

| 优先级 | 方式 | 用法 | 说明 |
|-------|-----|------|-----|
| 1 | 测试标记 | `@pytest.mark.keep_data` | 保留该测试的数据 |
| 2 | 命令行参数 | `pytest --keep-test-data` | 保留所有测试数据 |
| 3 | Settings 配置 | `.env` 中 `TEST__KEEP_TEST_DATA=1` | 本地开发推荐 |

```bash
# 正常运行（默认清理数据）
pytest tests/

# 调试模式（保留所有数据）
pytest tests/ --keep-test-data

# .env 文件配置（本地开发推荐）
# 在 .env 文件中添加：
TEST__KEEP_TEST_DATA=1

# 系统环境变量（需要 APP_ 前缀）
APP_TEST__KEEP_TEST_DATA=1 pytest tests/
```

> **注意**: `.env` 文件使用双下划线 `__` 表示嵌套配置，如 `TEST__KEEP_TEST_DATA` 对应 `settings.test.keep_test_data`

---

## 2. 框架提供的能力

### 2.1 should_keep_test_data() - 配置检查

```python
from df_test_framework.testing.fixtures import should_keep_test_data

@pytest.fixture
def cleanup_data(request, database):
    items = []
    yield items

    if should_keep_test_data(request):
        logger.info(f"保留测试数据: {items}")
        return

    # 执行清理...
```

### 2.2 DataGenerator - 测试数据生成

使用 `DataGenerator` 生成测试数据标识符：

```python
from df_test_framework import DataGenerator

# 方式1: 类方法（无需实例化，推荐）
order_no = DataGenerator.test_id("TEST_ORD")   # "TEST_ORD20251128123456789012"
user_id = DataGenerator.test_id("TEST_USER")   # "TEST_USER20251128123456789012"
payment_no = DataGenerator.test_id("TEST_PAY") # "TEST_PAY20251128123456789012"

# 方式2: 实例方法
gen = DataGenerator()
order_no = gen.order_id(prefix="TEST_ORD")
card_no = gen.card_number()
uid = gen.uuid()
```

### 2.3 CleanupManager - 清理管理器基类

内置配置检查，自动根据 `--keep-test-data` 决定是否清理：

```python
from df_test_framework.testing.fixtures import CleanupManager

class MyCleanupManager(CleanupManager):
    def _do_cleanup(self):
        for order_no in self.get_items("orders"):
            self.db.execute(
                "DELETE FROM orders WHERE order_no = :order_no",
                {"order_no": order_no}
            )

@pytest.fixture
def cleanup(request, database):
    manager = MyCleanupManager(request, database)
    yield manager
    manager.cleanup()  # 自动检查配置
```

### 2.4 SimpleCleanupManager - 回调函数模式

```python
from df_test_framework.testing.fixtures import SimpleCleanupManager

@pytest.fixture
def cleanup(request, database):
    manager = SimpleCleanupManager(request, database)

    manager.register_cleanup("orders", lambda ids: database.execute(
        "DELETE FROM orders WHERE order_no IN :ids", {"ids": tuple(ids)}
    ))

    yield manager
    manager.cleanup()
```

### 2.5 ListCleanup - 最简单用法

```python
from df_test_framework.testing.fixtures import ListCleanup

@pytest.fixture
def cleanup_orders(request, database):
    orders = ListCleanup(request)
    yield orders

    # 推荐: 使用 should_do_cleanup()，自动打印保留日志
    if orders.should_do_cleanup():
        for order_no in orders:
            database.execute(
                "DELETE FROM orders WHERE order_no = :order_no",
                {"order_no": order_no}
            )
```

---

## 3. 项目实现示例

### 3.1 简单列表模式

```python
@pytest.fixture
def cleanup_api_test_data(request, database):
    """清理 API 测试数据"""
    from df_test_framework.testing.fixtures import should_keep_test_data

    order_nos = []
    yield order_nos

    if should_keep_test_data(request):
        if order_nos:
            logger.info(f"保留测试数据: {order_nos}")
        return

    for order_no in order_nos:
        database.execute(
            "DELETE FROM orders WHERE order_no = :order_no",
            {"order_no": order_no}
        )
```

### 3.2 继承 CleanupManager

```python
from df_test_framework.testing.fixtures import CleanupManager

class GiftCardCleanupManager(CleanupManager):
    def _do_cleanup(self):
        # 清理订单
        for order_no in self.get_items("orders"):
            self._cleanup_order(order_no)

        # 清理支付
        for payment_no in self.get_items("payments"):
            self._cleanup_payment(payment_no)

    def _cleanup_order(self, order_no):
        self.db.execute(
            "DELETE FROM card_inventory WHERE order_no = :order_no",
            {"order_no": order_no}
        )
        self.db.execute(
            "DELETE FROM card_order WHERE customer_order_no = :order_no",
            {"order_no": order_no}
        )

    def _cleanup_payment(self, payment_no):
        self.db.execute(
            "DELETE FROM consumption_record WHERE payment_no = :payment_no",
            {"payment_no": payment_no}
        )
        self.db.execute(
            "DELETE FROM card_payment WHERE payment_no = :payment_no",
            {"payment_no": payment_no}
        )


@pytest.fixture
def cleanup(request, database):
    manager = GiftCardCleanupManager(request, database)
    yield manager
    manager.cleanup()
```

使用：

```python
from df_test_framework import DataGenerator

def test_complete_flow(master_api, h5_api, cleanup):
    order_no = DataGenerator.test_id("TEST_ORD")
    master_api.create_order(order_no)
    cleanup.add("orders", order_no)

    payment_no = DataGenerator.test_id("TEST_PAY")
    h5_api.pay(payment_no)
    cleanup.add("payments", payment_no)

    # 测试逻辑...
    # ✅ 测试结束后自动清理（除非 --keep-test-data）
```

---

## 4. 最佳实践

### 4.1 使用 DataGenerator 生成标识符

```python
from df_test_framework import DataGenerator

def test_create_order(api, cleanup):
    # ✅ 推荐：使用 DataGenerator
    order_no = DataGenerator.test_id("TEST_ORD")

    # ❌ 不推荐：手动拼接
    # order_no = f"TEST_{int(time.time() * 1000)}"
```

### 4.2 清理顺序

按依赖关系倒序清理（先删子表，再删主表）：

```python
def _do_cleanup(self):
    # 1. 先删除消费记录
    # 2. 再删除卡片
    # 3. 最后删除订单
```

### 4.3 清理失败处理

```python
try:
    database.execute(
        "DELETE FROM orders WHERE id = :order_id",
        {"order_id": order_id}
    )
except Exception as e:
    logger.warning(f"清理失败 {order_id}: {e}")
    # 不抛出异常，继续清理其他数据
```

---

## 5. 配置参考

### 测试标记（优先级最高）

```python
@pytest.mark.keep_data
def test_debug():
    # 此测试的数据会保留
    ...
```

### 命令行参数

```bash
pytest tests/ --keep-test-data  # 保留所有测试数据
```

### Settings 配置（v3.12.1+）

```bash
# .env 文件（本地开发推荐）
TEST__KEEP_TEST_DATA=1

# 系统环境变量（需要 APP_ 前缀）
APP_TEST__KEEP_TEST_DATA=1 pytest tests/
```

---

## 6. API 参考

### should_keep_test_data(request)

检查是否应该保留测试数据。

```python
def should_keep_test_data(request: pytest.FixtureRequest) -> bool
```

### DataGenerator

| 方法 | 说明 | 返回示例 |
|------|------|---------|
| `test_id("TEST_ORD")` | 类方法，生成测试标识符 | `TEST_ORD20251128123456789012` |
| `order_id(prefix="ORD")` | 实例方法，生成订单号 | `ORD20251128123456789012` |
| `uuid()` | 生成 UUID | `a1b2c3d4-e5f6-...` |
| `card_number()` | 生成卡号 | `1234567890123456` |

### CleanupManager

| 方法 | 说明 |
|------|------|
| `add(type, id)` | 添加清理项 |
| `add_many(type, ids)` | 批量添加 |
| `get_items(type)` | 获取指定类型的项 |
| `cleanup()` | 执行清理（自动检查配置） |

---

**文档结束**
