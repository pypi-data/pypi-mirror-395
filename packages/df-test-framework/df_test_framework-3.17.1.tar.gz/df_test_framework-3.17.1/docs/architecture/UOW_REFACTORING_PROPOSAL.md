# UnitOfWork 架构重构方案

> v3.13.0 架构重构 | 2025-12-03

## 问题分析

### 当前架构的复杂性来源

从 CHANGELOG 可以看到演进路径：

```
v3.5.0  Repository 基类（基础 CRUD）
   ↓
v3.6.2  测试数据清理控制（发现需要控制清理）
   ↓
v3.7.0  UnitOfWork（解决 v3.6.2 的事务隔离问题）
   ↓
v3.11.1 CleanupManager 重构（统一 API 数据清理）
   ↓
v3.12.1 统一 keep_test_data（发现 UoW 和 Cleanup 配置不一致）
```

**每个版本都是在修复上一个版本的问题**，导致了：

| 问题 | 具体表现 |
|------|----------|
| 多个 UoW 类 | `UnitOfWork` + `BaseUnitOfWork`（已移除）职责不清 |
| 需要继承 | 项目必须创建 `GiftCardUoW` 继承 `BaseUnitOfWork`（已移除） |
| 需要覆盖 fixture | 项目必须覆盖 `uow` fixture 来使用自定义 UoW |
| 容易遗漏功能 | 覆盖时遗漏 `should_keep_test_data()` 检查 |
| 配置分散 | `repository_package` 在代码中，`keep_test_data` 在配置中 |

### 重构前使用方式（复杂）

```python
# 1. 项目需要创建自定义 UoW 类（已不需要）
class GiftCardUoW(BaseUnitOfWork):  # BaseUnitOfWork 已移除
    def __init__(self, session_factory):
        super().__init__(
            session_factory,
            repository_package="gift_card_test.repositories",  # 硬编码
        )

# 2. 项目需要覆盖 uow fixture
@pytest.fixture
def uow(database, request):
    auto_commit = should_keep_test_data(request)  # 容易遗漏！
    with GiftCardUoW(database.session_factory) as uow_instance:
        yield uow_instance
        if auto_commit and not uow_instance._committed:
            uow_instance.commit()

# 3. 测试代码
def test_create_card(uow):
    uow.cards.create({"card_no": "TEST001"})
```

---

## 理想架构设计

### 核心原则

1. **配置驱动** - 不需要继承，通过配置指定 `repository_package`
2. **单一实现** - 只有一个 `UnitOfWork` 类
3. **无需覆盖** - 框架 fixture 足够灵活，用户无需覆盖
4. **职责清晰** - UoW 管事务和 Repository，配置检查统一处理

### 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    配置层（Settings）                            │
│   test.keep_test_data: bool = False                             │
│   test.repository_package: str | None = None   # ← 配置化       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    UnitOfWork（唯一实现）                        │
│   __init__(session_factory, repository_package, auto_commit)    │
│   - 支持 Repository 自动发现                                     │
│   - 支持懒加载和缓存                                             │
│   - 根据 auto_commit 决定是否提交                                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    框架 Fixture（无需覆盖）                       │
│   @pytest.fixture                                               │
│   def uow(database, request, runtime):                          │
│       repo_package = runtime.settings.test.repository_package   │
│       auto_commit = should_keep_test_data(request)              │
│       with UnitOfWork(...) as uow:                              │
│           yield uow                                             │
└─────────────────────────────────────────────────────────────────┘
```

### 理想使用方式（简洁）

```toml
# pyproject.toml
[tool.pytest.ini_options]
df_repository_package = "gift_card_test.repositories"
```

或

```env
# .env
TEST__REPOSITORY_PACKAGE=gift_card_test.repositories
TEST__KEEP_TEST_DATA=false
```

```python
# 测试代码 - 零配置使用
def test_create_card(uow):  # ← 框架 fixture，无需覆盖
    uow.cards.create({"card_no": "TEST001"})  # ← 自动发现
    # 测试结束自动回滚（除非配置 keep_test_data）
```

---

## 重构方案

### 重构前后对比

| 维度 | 重构前 | 重构后 |
|------|--------|--------|
| UoW 类数量 | 2 个（`UnitOfWork` + `BaseUnitOfWork`） | 1 个（`UnitOfWork`） |
| 项目自定义类 | 需要（`GiftCardUoW`） | 不需要 |
| 覆盖 fixture | 需要 | 不需要 |
| repository_package | 代码硬编码 | 配置文件 |
| keep_test_data | fixture 中检查 | UoW 内部处理 |

### 具体改动

#### 1. 合并 UoW 类

```python
# databases/uow.py - 重构后
class UnitOfWork:
    """统一的工作单元实现

    支持：
    - Repository 自动发现（通过 repository_package 配置）
    - 事务管理（自动回滚或提交）
    - 懒加载和缓存
    """

    def __init__(
        self,
        session_factory: sessionmaker[Session],
        repository_package: str | None = None,
        auto_commit: bool = False,
    ):
        self._session_factory = session_factory
        self._repository_package = repository_package
        self._auto_commit = auto_commit
        self._session: Session | None = None
        self._repositories: dict[str, BaseRepository] = {}
        self._committed = False

    def __getattr__(self, name: str) -> BaseRepository:
        """懒加载 Repository"""
        if name.startswith("_"):
            raise AttributeError(name)

        if name not in self._repositories:
            self._repositories[name] = self._get_or_create_repository(name)
        return self._repositories[name]

    def __enter__(self) -> Self:
        self._session = self._session_factory()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._session is None:
            return

        try:
            if exc_type is None and self._auto_commit and not self._committed:
                self._session.commit()
            else:
                self._session.rollback()
        finally:
            self._session.close()
            self._session = None
```

#### 2. 更新配置 Schema

```python
# infrastructure/config/schema.py
class TestExecutionConfig(BaseModel):
    keep_test_data: bool = False
    repository_package: str | None = None  # 新增
```

#### 3. 更新 uow fixture

```python
# testing/fixtures/core.py
@pytest.fixture
def uow(
    database: Database,
    request: pytest.FixtureRequest,
    runtime: Runtime,
) -> Generator[UnitOfWork, None, None]:
    """UnitOfWork fixture - 配置驱动，无需覆盖"""

    # 从配置读取
    settings = runtime.settings
    repo_package = None
    if settings.test:
        repo_package = settings.test.repository_package

    # 统一配置检查
    auto_commit = should_keep_test_data(request)

    with UnitOfWork(
        database.session_factory,
        repository_package=repo_package,
        auto_commit=auto_commit,
    ) as unit_of_work:
        yield unit_of_work
```

#### 4. 移除的代码

- `BaseUnitOfWork` 类（合并到 `UnitOfWork`）
- 项目的 `GiftCardUoW` 类（不再需要）
- 项目的 `uow` fixture 覆盖（不再需要）

---

## 迁移指南

### 项目迁移步骤

1. **更新配置文件**

```env
# .env
TEST__REPOSITORY_PACKAGE=gift_card_test.repositories
```

2. **删除自定义 UoW 类**

```python
# 删除 gift_card_test/uow.py
# class GiftCardUoW(BaseUnitOfWork): ...
```

3. **删除自定义 fixture**

```python
# 删除 conftest.py 中的 uow fixture
# @pytest.fixture
# def uow(database, request): ...
```

4. **测试代码无需修改**

```python
# 保持不变
def test_create_card(uow):
    uow.cards.create({"card_no": "TEST001"})
```

### IDE 类型提示（可选）

如果需要 IDE 自动补全，可以创建类型存根：

```python
# gift_card_test/stubs/uow.pyi
from df_test_framework.databases import UnitOfWork as _UnitOfWork
from gift_card_test.repositories import CardRepository, OrderRepository

class UnitOfWork(_UnitOfWork):
    cards: CardRepository
    orders: OrderRepository
```

---

## 版本规划

- **v3.13.0**: UnitOfWork 架构重构 ✅ 已完成
  - ✅ 移除 `BaseUnitOfWork`（直接使用 `UnitOfWork`）
  - ✅ 新增 `TestExecutionConfig.repository_package` 配置
  - ✅ 更新 `uow` fixture 支持配置驱动
  - ✅ 更新示范项目 gift-card-test
  - ✅ 更新 CLI 模板

---

## 实施结果

### 框架变更

1. **databases/uow.py**
   - 移除 `BaseUnitOfWork`（直接使用 `UnitOfWork`）
   - 如需继承，直接继承 `UnitOfWork`

2. **infrastructure/config/schema.py**
   - `TestExecutionConfig` 新增 `repository_package: str | None` 字段

3. **testing/fixtures/core.py**
   - `uow` fixture 从 `runtime.settings.test.repository_package` 读取配置
   - 无需覆盖即可支持 Repository 自动发现

### 示范项目变更 (gift-card-test)

1. **.env** 新增配置:
   ```env
   TEST__REPOSITORY_PACKAGE=gift_card_test.repositories
   ```

2. **删除文件**（不再需要）:
   - `src/gift_card_test/uow.py` - 已删除
   - `src/gift_card_test/fixtures/uow_fixture.py` - 已删除

3. **fixtures/__init__.py**
   - 移除 `uow` 导出

4. **conftest.py**
   - 移除 `uow` 导入

### 代码量变化

| 文件 | 变更前 | 变更后 | 减少 |
|------|--------|--------|------|
| uow.py | 95 行 | 0 行（删除） | -95 行 |
| uow_fixture.py | 70 行 | 0 行（删除） | -70 行 |
| conftest.py | 1 行导入 | 0 行 | -1 行 |
| **总计** | **166 行** | **0 行** | **-166 行** |

---

## 总结

这次重构遵循 **"正确架构优先"** 原则：

1. **简化** - 从 2 个类变为 1 个类
2. **配置化** - 从代码硬编码变为配置文件
3. **减少覆盖** - 用户无需覆盖框架 fixture
4. **统一职责** - UoW 内部处理所有逻辑

重构后的架构更加清晰、易用、不容易出错。
