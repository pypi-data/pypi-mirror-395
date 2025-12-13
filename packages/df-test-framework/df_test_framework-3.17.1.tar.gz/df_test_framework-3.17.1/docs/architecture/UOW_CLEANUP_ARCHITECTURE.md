# UoW、Cleanup 与 Repository 自动发现架构设计

> v3.12.1 架构文档 | 2024-12-02

## 问题背景

### 遇到的问题

在实现 `KEEP_TEST_DATA` 配置时，发现以下问题：

1. **配置不生效**：`.env` 中配置 `TEST__KEEP_TEST_DATA=1`，`cleanup_api_test_data` 正常工作，但 UoW 仍然回滚数据

2. **Fixture 覆盖问题**：测试项目有自己的 `uow` fixture，覆盖了框架的 fixture，但没有调用 `should_keep_test_data()`

3. **架构疑问**：为什么项目需要自定义 UoW 类和 fixture？框架能否提供更好的支持？

### 问题排查过程

```
问题现象：
- cleanup_api_test_data ✅ 正常跳过清理
- uow ❌ 仍然回滚数据

排查步骤：
1. 检查 Settings 配置读取 → 正常，keep_test_data = True
2. 检查框架 uow fixture → 已添加 should_keep_test_data()
3. 发现项目有自己的 uow fixture → 覆盖了框架实现
4. 项目 fixture 缺少 should_keep_test_data() 检查

根本原因：
- 项目需要使用 GiftCardUoW（带 repository_package）
- 因此必须覆盖框架的 uow fixture
- 覆盖时遗漏了配置检查逻辑
```

## 当前架构设计

### 组件职责

```
┌─────────────────────────────────────────────────────────────────┐
│                         配置检查层                               │
│   should_keep_test_data(request) → bool                         │
│   - 统一的配置检查函数                                            │
│   - 优先级：@pytest.mark.keep_data > --keep-test-data > Settings │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      测试框架 (df-test-framework)                │
├─────────────────────────────────────────────────────────────────┤
│  cleanup.py                                                      │
│  ├── should_keep_test_data()    # 统一配置检查                   │
│  ├── CleanupManager             # 清理管理器基类                  │
│  └── SimpleCleanupManager       # API 数据清理                   │
├─────────────────────────────────────────────────────────────────┤
│  uow.py                                                          │
│  ├── UnitOfWork                 # 支持 repository_package        │
│  └── UnitOfWork             # 可扩展基类                      │
├─────────────────────────────────────────────────────────────────┤
│  core.py (fixtures)                                              │
│  └── uow fixture                # 基础 UoW（无 repository_package）│
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      测试项目 (gift-card-test)                   │
├─────────────────────────────────────────────────────────────────┤
│  uow.py                                                          │
│  └── GiftCardUoW                # 指定 repository_package        │
├─────────────────────────────────────────────────────────────────┤
│  uow_fixture.py                                                  │
│  └── uow fixture (override)     # 使用 GiftCardUoW + 配置检查    │
└─────────────────────────────────────────────────────────────────┘
```

### 职责边界

| 组件 | 职责 | 清理的数据 |
|------|------|-----------|
| **UoW** | 事务管理、Session 生命周期 | 测试代码通过 Repository 创建的数据（自动回滚） |
| **CleanupManager** | API 数据清理注册与执行 | API 调用创建的数据（由后端提交，需手动清理） |
| **should_keep_test_data()** | 统一配置检查 | 控制两者是否清理 |

### 数据清理的两种场景

```python
# 场景1: 测试代码直接操作数据库（通过 Repository）
def test_create_card_via_repository(uow):
    # 通过 Repository 创建数据
    uow.cards.create({"card_no": "TEST001", ...})
    # 测试结束后自动回滚（除非配置保留）
    # ✅ UoW 负责清理

# 场景2: 测试代码调用 API（后端提交事务）
def test_create_card_via_api(http_client, cleanup_api_test_data):
    # 通过 API 创建数据（后端事务已提交）
    response = http_client.post("/cards", json={...})
    card_no = response.json()["card_no"]

    # 注册清理
    cleanup_api_test_data.add("cards", card_no)
    # 测试结束后 CleanupManager 负责清理
    # ✅ CleanupManager 负责清理
```

## 为什么项目需要自定义 UoW

### 框架 uow fixture 的限制

框架的 `uow` fixture 创建基础 `UnitOfWork`，不支持 Repository 自动发现：

```python
# 框架 core.py
@pytest.fixture
def uow(database, request):
    # 没有传 repository_package
    unit_of_work = UnitOfWork(database.session_factory)
    ...
```

### 项目需要 Repository 自动发现

项目希望使用自动发现功能，简化代码：

```python
# 有自动发现
with GiftCardUoW(session_factory) as uow:
    card = uow.cards.find_by_card_no("CARD001")  # ✅ 自动可用
    order = uow.orders.find_by_order_no("ORD001")  # ✅ 自动可用

# 无自动发现
with UnitOfWork(session_factory) as uow:
    card_repo = CardRepository(uow.session)  # ❌ 手动创建
    card = card_repo.find_by_card_no("CARD001")
```

### 项目的解决方案

1. **创建 GiftCardUoW 类**：指定 `repository_package`
2. **创建自定义 uow fixture**：使用 `GiftCardUoW` 并添加配置检查

```python
# 项目 uow.py
class GiftCardUoW(UnitOfWork):
    def __init__(self, session_factory):
        super().__init__(
            session_factory,
            repository_package="gift_card_test.repositories",  # 启用自动发现
        )

# 项目 uow_fixture.py
@pytest.fixture
def uow(database, request):
    # 配置检查（关键！）
    auto_commit = should_keep_test_data(request)

    with GiftCardUoW(database.session_factory) as uow_instance:
        yield uow_instance

        # 根据配置决定是否提交
        if auto_commit and not uow_instance._committed:
            uow_instance.commit()
```

## 配置优先级

```
优先级（从高到低）:
1. @pytest.mark.keep_data - 测试标记（单个测试）
2. --keep-test-data - 命令行参数（整个运行）
3. TEST__KEEP_TEST_DATA=1 - Settings 配置（本地开发）
```

### 配置示例

```python
# 方式1: 测试标记
@pytest.mark.keep_data
def test_debug():
    ...

# 方式2: 命令行
pytest tests/ --keep-test-data

# 方式3: .env 文件
TEST__KEEP_TEST_DATA=1
```

## 未来改进方向

### 方案：支持配置化的 repository_package

在 pyproject.toml 或 Settings 中配置 repository_package，让框架的 uow fixture 直接支持自动发现：

```toml
# pyproject.toml
[tool.pytest.ini_options]
df_repository_package = "gift_card_test.repositories"
```

```python
# 或 Settings 配置
class TestExecutionConfig(BaseModel):
    keep_test_data: bool = False
    repository_package: str | None = None  # 新增
```

框架 fixture 改进：

```python
@pytest.fixture
def uow(database, request, runtime):
    auto_commit = should_keep_test_data(request)

    # 从配置读取 repository_package
    repo_package = None
    if runtime.settings.test:
        repo_package = runtime.settings.test.repository_package

    unit_of_work = UnitOfWork(
        database.session_factory,
        repository_package=repo_package,  # 自动传入
    )
    ...
```

**优点**：
- 简单项目无需创建自定义 UoW 类
- 无需创建自定义 uow fixture
- 配置集中管理

**何时需要自定义**：
- 需要额外的业务逻辑
- 需要类型提示支持（IDE 自动补全）
- 复杂的 Repository 初始化

## 最佳实践总结

### 1. 使用统一配置检查

所有涉及测试数据清理的 fixture 都应使用 `should_keep_test_data()`：

```python
from df_test_framework.testing.fixtures.cleanup import should_keep_test_data

@pytest.fixture
def my_cleanup_fixture(request):
    items = []
    yield items

    if should_keep_test_data(request):
        logger.info(f"保留测试数据: {items}")
        return

    # 执行清理...
```

### 2. 覆盖框架 fixture 时保持功能完整

如果项目需要覆盖框架的 fixture，确保：
- 保留原有功能（如配置检查）
- 参考框架实现的文档字符串
- 测试覆盖配置生效的场景

### 3. 区分 UoW 数据和 API 数据

- **UoW 数据**：通过 Repository 直接创建，UoW 自动回滚
- **API 数据**：通过 HTTP 调用创建，需要 CleanupManager 清理

### 4. 本地开发推荐配置

在 `.env` 文件中启用数据保留，方便调试：

```env
# .env
TEST__KEEP_TEST_DATA=1
```

提交代码前记得关闭或删除此配置。

## 相关文件

- `df_test_framework/testing/fixtures/cleanup.py` - 清理管理器和配置检查
- `df_test_framework/testing/fixtures/core.py` - 核心 fixtures
- `df_test_framework/databases/uow.py` - UnitOfWork 实现
- `df_test_framework/infrastructure/config/schema.py` - Settings 配置

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v3.12.1 | 2024-12-02 | 添加 Settings 配置支持，统一 UoW 和 Cleanup 的配置检查 |
| v3.11.1 | 2024-11 | 添加 --keep-test-data 命令行参数 |
| v3.7.0 | 2024 | 引入 UnitOfWork 和 Repository 自动发现 |
