# DF Test Framework v3.7 新特性示例

> **框架版本**: df-test-framework v3.7.0+
> **最后更新**: 2025-11-24
> **示例总数**: 6个

---

## 🎯 v3.7.0 核心特性

v3.7.0 是一个**重大架构升级**版本，引入了 **Unit of Work (UoW)** 模式，彻底改变了数据库操作和事务管理方式。

### 核心变更

| 特性 | v3.6及之前 | v3.7.0 | 影响 |
|------|-----------|--------|------|
| **Repository构造** | `Repository(database)` | `Repository(session)` | 🔴 Breaking Change |
| **事务管理** | 手动`with database.transaction()` | 自动`with uow:` | ✅ 简化代码 |
| **测试数据清理** | 手动清理 | `uow` fixture自动回滚 | ✅ 零代码清理 |
| **多表操作** | 多个Repository独立 | UoW统一管理 | ✅ 事务一致性 |

---

## 📚 示例目录

### 01 - Unit of Work 基础用法 ⭐
**文件**: `01_unit_of_work_basics.py`

演示 UoW 的基本概念和使用方法。

**学习要点**:
- ✅ UoW 的创建和上下文管理
- ✅ 显式 commit 和自动 rollback
- ✅ Repository 通过 UoW 访问
- ✅ 事务边界的概念

**关键代码**:
```python
from df_test_framework.databases import BaseUnitOfWork

# 1. 创建 UoW
with BaseUnitOfWork(session_factory) as uow:
    # 2. 通过 UoW 获取 Repository
    repo = uow.repository(UserRepository)

    # 3. 执行数据库操作
    user_id = repo.create({"name": "Alice"})

    # 4. 显式提交（可选，退出上下文时自动提交）
    uow.commit()
```

---

### 02 - Repository Pattern v3.7 ⭐
**文件**: `02_repository_v37.py`

对比 v3.6 和 v3.7 的 Repository 实现差异。

**学习要点**:
- 🔴 v3.7 Repository **必须接收 Session 而非 Database**
- ✅ Repository 与 UoW 配合使用
- ✅ 使用 SQLAlchemy ORM 风格
- ✅ 更简洁的 CRUD 方法

**迁移对比**:
```python
# ❌ v3.6 写法（已废弃）
class UserRepository(BaseRepository):
    def __init__(self, database):
        super().__init__(database, table_name="users")

# ✅ v3.7 写法
class UserRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session, table_name="users")
```

---

### 03 - 自动数据回滚与测试隔离 🔥
**文件**: `03_auto_rollback_testing.py`

展示 v3.7 最强大的特性：测试数据自动清理。

**学习要点**:
- ✅ `uow` fixture 自动回滚测试数据
- ✅ 无需手动清理，测试完全隔离
- ✅ 多测试并行运行无污染
- ✅ 异常场景同样自动回滚

**Pytest 使用**:
```python
def test_create_user(uow):
    """测试创建用户 - 数据自动回滚"""
    repo = uow.repository(UserRepository)
    user_id = repo.create({"name": "Test User"})

    # ✅ 测试结束自动回滚，无需清理
```

---

### 04 - 多Repository事务一致性 ⭐
**文件**: `04_multi_repository_transactions.py`

演示 UoW 如何保证跨多个 Repository 的事务一致性。

**学习要点**:
- ✅ 多个 Repository 共享同一事务
- ✅ 一次 commit 提交所有更改
- ✅ 出错时全部回滚（原子性）
- ✅ 典型业务场景：订单+库存+支付

**业务场景示例**:
```python
with uow:
    # 场景：用户支付订单
    order_repo = uow.repository(OrderRepository)
    payment_repo = uow.repository(PaymentRepository)
    card_repo = uow.repository(CardRepository)

    # 1. 创建订单
    order_id = order_repo.create({...})

    # 2. 创建支付记录
    payment_id = payment_repo.create({...})

    # 3. 扣减卡片余额
    card_repo.update({"card_no": "..."}, {"balance": 50.0})

    # ✅ 一次 commit 全部生效，或全部回滚
    uow.commit()
```

---

### 05 - 项目级 UoW 封装 🔥
**文件**: `05_project_uow.py`

展示如何为项目创建专用的 UoW 类（最佳实践）。

**学习要点**:
- ✅ 继承 `BaseUnitOfWork` 创建项目 UoW
- ✅ 使用 `@property` 暴露 Repository
- ✅ 提供类型提示，IDE 友好
- ✅ 简化测试代码

**最佳实践**:
```python
# src/gift_card_test/uow.py
class GiftCardUoW(BaseUnitOfWork):
    """Gift Card 项目专用 Unit of Work"""

    @property
    def cards(self) -> CardRepository:
        """卡片 Repository"""
        return self.repository(CardRepository)

    @property
    def orders(self) -> OrderRepository:
        """订单 Repository"""
        return self.repository(OrderRepository)

    @property
    def payments(self) -> PaymentRepository:
        """支付记录 Repository"""
        return self.repository(PaymentRepository)

# 测试中使用
def test_payment(uow: GiftCardUoW):
    card = uow.cards.find_by_card_no("CARD123")
    payment = uow.payments.create({...})
    # ✅ 简洁、类型安全、IDE自动补全
```

---

### 06 - 异常场景测试与 UoW 🔥
**文件**: `06_exception_handling_with_uow.py`

展示如何使用 UoW 测试异常场景（余额不足、卡片冻结等）。

**学习要点**:
- ✅ 使用 Repository 直接修改数据库状态
- ✅ 模拟异常场景（冻结卡片、清空余额）
- ✅ 验证业务错误处理
- ✅ 测试结束自动回滚，无污染

**测试模式**:
```python
def test_payment_insufficient_balance(h5_card_api, uow):
    """测试余额不足场景"""
    # 1. 创建卡片
    card_no = create_test_card()

    # 2. 使用 Repository 修改状态
    uow.cards.update(
        conditions={"card_no": card_no},
        data={"balance": Decimal("10.0")}  # 设置余额不足
    )

    # 3. 验证支付失败
    with pytest.raises(BusinessError) as exc:
        h5_card_api.pay(amount=Decimal("100.0"), card=card_no)

    assert exc.value.code != 200
    # ✅ 测试结束自动回滚，卡片状态恢复
```

---

## 🚀 快速开始

### 环境要求
```bash
# Python 3.12+
# df-test-framework v3.7.0+

pip install "df-test-framework>=3.7.0"
```

### 运行示例

**按顺序学习（推荐）**:
```bash
# 1. UoW 基础（必看）
python examples/08-v37-features/01_unit_of_work_basics.py

# 2. Repository v3.7（理解变更）
python examples/08-v37-features/02_repository_v37.py

# 3. 自动回滚（最强特性）
python examples/08-v37-features/03_auto_rollback_testing.py

# 4. 多Repository事务
python examples/08-v37-features/04_multi_repository_transactions.py

# 5. 项目级UoW封装（最佳实践）
python examples/08-v37-features/05_project_uow.py

# 6. 异常场景测试
python examples/08-v37-features/06_exception_handling_with_uow.py
```

---

## 📖 v3.6 → v3.7 迁移要点

### 1. Repository 构造函数变更 🔴

```python
# ❌ v3.6
class UserRepository(BaseRepository):
    def __init__(self, database):
        super().__init__(database, table_name="users")

# ✅ v3.7
from sqlalchemy.orm import Session

class UserRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session, table_name="users")
```

### 2. 数据库操作方式变更 🔴

```python
# ❌ v3.6
def test_create_user(database):
    repo = UserRepository(database)
    user_id = repo.create({"name": "Alice"})
    # 手动清理
    repo.delete(user_id)

# ✅ v3.7
def test_create_user(uow):
    repo = uow.repository(UserRepository)
    user_id = repo.create({"name": "Alice"})
    # ✅ 自动回滚，无需清理
```

### 3. 事务管理变更 ✅

```python
# ❌ v3.6
with database.transaction():
    repo1 = Repo1(database)
    repo2 = Repo2(database)
    repo1.create({...})
    repo2.update({...})

# ✅ v3.7
with uow:
    repo1 = uow.repository(Repo1)
    repo2 = uow.repository(Repo2)
    repo1.create({...})
    repo2.update({...})
    uow.commit()
```

### 4. conftest.py 配置变更 ✅

```python
# v3.7 新增 uow fixture（框架已提供）
@pytest.fixture
def uow(session_factory):
    """UnitOfWork fixture with auto-rollback"""
    with BaseUnitOfWork(session_factory) as uow:
        yield uow
        # ✅ 自动回滚
```

---

## 🎯 学习路径

### 路径1: 快速上手（30分钟）
1. 阅读 `01_unit_of_work_basics.py`（10分钟）
2. 运行 `03_auto_rollback_testing.py`（10分钟）
3. 查看 `05_project_uow.py` 最佳实践（10分钟）

### 路径2: 深入理解（1小时）
1. 对比学习 `02_repository_v37.py`（15分钟）
2. 理解事务一致性 `04_multi_repository_transactions.py`（20分钟）
3. 掌握异常测试 `06_exception_handling_with_uow.py`（25分钟）

### 路径3: 实战迁移（2小时）
1. 学习所有示例（1小时）
2. 阅读[迁移指南](../../docs/migration/v3.6-to-v3.7.md)（30分钟）
3. 改造现有项目（30分钟）

---

## 💡 最佳实践总结

### ✅ DO - 推荐做法

1. **使用项目级 UoW 类**
   ```python
   # src/project_name/uow.py
   class ProjectUoW(BaseUnitOfWork):
       @property
       def users(self) -> UserRepository:
           return self.repository(UserRepository)
   ```

2. **Repository 接收 Session**
   ```python
   from sqlalchemy.orm import Session

   class UserRepository(BaseRepository):
       def __init__(self, session: Session):
           super().__init__(session, table_name="users")
   ```

3. **测试使用 uow fixture**
   ```python
   def test_create_user(uow):
       repo = uow.repository(UserRepository)
       # ✅ 自动回滚
   ```

4. **多表操作使用同一 UoW**
   ```python
   with uow:
       uow.orders.create({...})
       uow.payments.create({...})
       uow.cards.update({...})
       uow.commit()  # 一次性提交
   ```

### ❌ DON'T - 避免做法

1. ❌ **不要在 Repository 中接收 Database**
   ```python
   # ❌ 错误：v3.6 旧写法
   def __init__(self, database):
       ...
   ```

2. ❌ **不要手动清理测试数据**
   ```python
   # ❌ 不需要
   repo.delete(user_id)
   ```

3. ❌ **不要使用多个 UoW 实例操作同一业务**
   ```python
   # ❌ 错误：事务不一致
   with BaseUnitOfWork(sf) as uow1:
       uow1.orders.create({...})

   with BaseUnitOfWork(sf) as uow2:
       uow2.payments.create({...})
   ```

4. ❌ **不要忘记 commit**
   ```python
   # ❌ 忘记 commit，数据不会保存
   with uow:
       uow.cards.create({...})
       # 缺少 uow.commit()
   ```

---

## 📚 相关文档

- [v3.6→v3.7 迁移指南](../../docs/migration/v3.6-to-v3.7.md)
- [UnitOfWork API 文档](../../docs/api-reference/databases.md#unitofwork)
- [Repository API 文档](../../docs/api-reference/databases.md#repository)
- [完整用户手册](../../docs/user-guide/USER_MANUAL.md)

---

## ❓ 常见问题

### Q1: 为什么要引入 UoW？

**A**: 解决v3.6及之前版本的3个痛点:
1. ❌ Repository 需要手动管理事务
2. ❌ 测试数据需要手动清理
3. ❌ 多表操作事务一致性难以保证

### Q2: v3.7 是否向后兼容？

**A**: 🔴 **不完全兼容**，Repository 构造函数有 Breaking Change：
- v3.6: `Repository(database)`
- v3.7: `Repository(session)`

但迁移成本低，参考[迁移指南](../../docs/migration/v3.6-to-v3.7.md)。

### Q3: 必须使用 UoW 吗？

**A**: **强烈推荐**使用，但不强制：
- ✅ 使用 UoW: 自动回滚、事务一致性、代码更简洁
- ⚠️ 不使用: 需要手动管理事务和数据清理

### Q4: uow fixture 从哪来？

**A**: 框架已内置 `uow` fixture（v3.7.0+），自动提供：
```python
# 在 conftest.py 中无需定义，直接使用
def test_example(uow):
    # uow 由框架自动注入
    pass
```

### Q5: 如何查看 UoW 源码？

**A**: 查看框架源码：
```bash
# BaseUnitOfWork
df-test-framework/src/df_test_framework/databases/uow.py

# uow fixture
df-test-framework/src/df_test_framework/testing/fixtures.py
```

---

## 🎯 总结

v3.7.0 的 **Unit of Work** 模式带来：

| 特性 | 价值 |
|------|------|
| ✅ 自动回滚 | 测试数据零清理，100%隔离 |
| ✅ 事务一致性 | 多表操作原子性保证 |
| ✅ 代码简化 | 无需手动管理事务和清理 |
| ✅ 类型安全 | 项目级UoW提供IDE自动补全 |

**下一步**:
1. 运行所有示例代码
2. 阅读[迁移指南](../../docs/migration/v3.6-to-v3.7.md)
3. 迁移现有项目到 v3.7

---

**示例代码版本**: v3.7.0
**最后更新**: 2025-11-24
**维护者**: df-test-framework团队

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
