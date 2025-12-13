"""
Repository Pattern v3.7.0 变更说明

v3.7.0 对 Repository 进行了重大重构：
- 🔴 Breaking Change: Repository 构造函数参数变更
- ✅ 从 Database 改为 Session
- ✅ 与 UnitOfWork 模式配合

本示例演示：
1. v3.6 vs v3.7 Repository 实现对比
2. 为什么要这样改？
3. 如何迁移现有代码
4. v3.7 Repository 的最佳实践

学习要点：
- 🔴 v3.7 Repository 必须接收 Session
- ✅ 使用 SQLAlchemy ORM 风格
- ✅ 更简洁的 CRUD 方法
- ✅ 与 UoW 无缝集成
"""

from decimal import Decimal
from typing import Any

from sqlalchemy.orm import Session

from df_test_framework import BaseRepository


# ========== ❌ v3.6 Repository 实现（已废弃）==========
class UserRepositoryV36(BaseRepository):
    """v3.6 Repository 实现（已废弃）

    问题：
    1. 接收 Database 对象，事务管理不清晰
    2. 需要手动管理事务
    3. 测试数据需要手动清理
    """

    def __init__(self, database):  # ❌ 接收 Database
        """v3.6 构造函数"""
        super().__init__(database, table_name="users")

    def find_by_id(self, user_id: int) -> dict | None:
        """根据ID查找"""
        return self.find_one({"id": user_id})


# ========== ✅ v3.7 Repository 实现 ==========
class UserRepositoryV37(BaseRepository):
    """v3.7 Repository 实现

    优势：
    1. 接收 Session，事务边界清晰
    2. 与 UnitOfWork 无缝集成
    3. 支持自动回滚
    """

    def __init__(self, session: Session):  # ✅ 接收 Session
        """v3.7 构造函数

        Args:
            session: SQLAlchemy Session 对象
        """
        super().__init__(session, table_name="users")

    def find_by_id(self, user_id: int) -> dict | None:
        """根据ID查找用户"""
        return self.find_one({"id": user_id})

    def find_by_username(self, username: str) -> dict | None:
        """根据用户名查找"""
        return self.find_one({"username": username})

    def find_active_users(self) -> list[dict[str, Any]]:
        """查找所有激活用户"""
        return self.find_all({"status": "active"})

    def update_balance(self, user_id: int, amount: Decimal) -> int:
        """更新用户余额

        Args:
            user_id: 用户ID
            amount: 新余额

        Returns:
            更新的行数
        """
        return self.update(
            conditions={"id": user_id},
            data={"balance": amount}
        )

    def deactivate_user(self, user_id: int) -> int:
        """停用用户"""
        return self.update(
            conditions={"id": user_id},
            data={"status": "inactive"}
        )


# ========== 对比示例 ==========
def compare_v36_vs_v37():
    """对比 v3.6 和 v3.7 的使用方式"""
    print("\n" + "=" * 60)
    print("📊 v3.6 vs v3.7 对比")
    print("=" * 60)

    print("\n❌ v3.6 使用方式（已废弃）:")
    print("-" * 60)
    print("""
# 1. 创建 Repository（接收 database）
def test_create_user(database):
    repo = UserRepositoryV36(database)

    # 2. 执行操作
    user_id = repo.create({"username": "alice"})

    # 3. 手动清理（必须！）
    try:
        # 测试逻辑...
        pass
    finally:
        repo.delete(user_id)  # ❌ 必须手动清理

# 问题：
# - 手动清理容易遗漏
# - 异常时清理逻辑复杂
# - 测试数据可能污染数据库
    """)

    print("\n✅ v3.7 使用方式:")
    print("-" * 60)
    print("""
# 1. 通过 UoW 获取 Repository（接收 session）
def test_create_user(uow):
    repo = uow.repository(UserRepositoryV37)

    # 2. 执行操作
    user_id = repo.create({"username": "alice"})

    # 3. ✅ 自动回滚，无需清理！

# 优势：
# - 自动回滚，零清理代码
# - 测试完全隔离
# - 异常处理自动化
    """)


# ========== 迁移示例 ==========
def migration_example():
    """展示如何迁移 v3.6 代码到 v3.7"""
    print("\n" + "=" * 60)
    print("🔧 迁移步骤")
    print("=" * 60)

    print("\n步骤1: 修改 Repository 构造函数")
    print("-" * 60)
    print("""
# ❌ v3.6
class UserRepository(BaseRepository):
    def __init__(self, database):
        super().__init__(database, table_name="users")

# ✅ v3.7
from sqlalchemy.orm import Session

class UserRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session, table_name="users")
    """)

    print("\n步骤2: 修改测试代码")
    print("-" * 60)
    print("""
# ❌ v3.6
def test_create_user(database):
    repo = UserRepository(database)
    user_id = repo.create({"username": "test"})

    # 手动清理
    try:
        assert user_id is not None
    finally:
        repo.delete(user_id)

# ✅ v3.7
def test_create_user(uow):
    repo = uow.repository(UserRepository)
    user_id = repo.create({"username": "test"})

    # ✅ 自动回滚
    assert user_id is not None
    """)

    print("\n步骤3: 移除手动清理代码")
    print("-" * 60)
    print("""
# ❌ v3.6 需要手动清理
finally:
    repo.delete(user_id)
    repo.delete_many({"created_by": "test"})
    # ... 更多清理逻辑

# ✅ v3.7 自动回滚
# 无需任何清理代码！
    """)


# ========== 最佳实践 ==========
def best_practices():
    """v3.7 Repository 最佳实践"""
    print("\n" + "=" * 60)
    print("💡 v3.7 Repository 最佳实践")
    print("=" * 60)

    print("\n✅ 1. 始终使用类型提示")
    print("-" * 60)
    print("""
from sqlalchemy.orm import Session

class UserRepository(BaseRepository):
    def __init__(self, session: Session):  # ✅ 明确类型
        super().__init__(session, table_name="users")

    def find_by_id(self, user_id: int) -> dict | None:  # ✅ 返回类型
        return self.find_one({"id": user_id})
    """)

    print("\n✅ 2. 提供业务语义方法")
    print("-" * 60)
    print("""
class CardRepository(BaseRepository):
    def freeze_card(self, card_no: str) -> int:
        \"\"\"冻结卡片 - 业务语义清晰\"\"\"
        return self.update(
            conditions={"card_no": card_no},
            data={"status": 2}  # 2=已冻结
        )

    def is_card_active(self, card_no: str) -> bool:
        \"\"\"检查卡片是否激活\"\"\"
        card = self.find_one({"card_no": card_no})
        return card and card["status"] == 1
    """)

    print("\n✅ 3. 配合 UoW 使用")
    print("-" * 60)
    print("""
# 测试中使用
def test_freeze_card(uow):
    card_repo = uow.repository(CardRepository)

    # 创建测试卡片
    card_no = card_repo.create({"card_no": "TEST123", "status": 1})

    # 冻结卡片
    card_repo.freeze_card("TEST123")

    # 验证状态
    assert not card_repo.is_card_active("TEST123")

    # ✅ 测试结束自动回滚
    """)

    print("\n✅ 4. 使用项目级 UoW 简化调用")
    print("-" * 60)
    print("""
# src/project_name/uow.py
class ProjectUoW(BaseUnitOfWork):
    @property
    def users(self) -> UserRepository:
        return self.repository(UserRepository)

    @property
    def cards(self) -> CardRepository:
        return self.repository(CardRepository)

# 测试中使用
def test_example(uow: ProjectUoW):
    # ✅ IDE 自动补全
    user = uow.users.find_by_id(1)
    card = uow.cards.find_by_card_no("CARD123")
    """)


# ========== API 变更总结 ==========
def api_changes_summary():
    """总结 v3.7 API 变更"""
    print("\n" + "=" * 60)
    print("📋 API 变更总结")
    print("=" * 60)

    changes = [
        ("Repository 构造", "Repository(database)", "Repository(session)", "🔴 Breaking"),
        ("获取 Repository", "Repo(database)", "uow.repository(Repo)", "✅ 新增"),
        ("事务管理", "with database.transaction()", "with uow:", "✅ 简化"),
        ("提交更改", "无需显式", "uow.commit()", "✅ 显式"),
        ("测试清理", "手动 delete", "自动 rollback", "✅ 自动"),
        ("多表操作", "独立事务", "统一事务", "✅ 改进"),
    ]

    print(f"\n{'功能':<15} {'v3.6':<25} {'v3.7':<25} {'类型':<10}")
    print("-" * 80)
    for feature, v36, v37, change_type in changes:
        print(f"{feature:<15} {v36:<25} {v37:<25} {change_type:<10}")


# ========== 主函数 ==========
if __name__ == "__main__":
    print("\n" + "🚀 Repository Pattern v3.7.0 变更说明")
    print("=" * 60)

    # 对比说明
    compare_v36_vs_v37()

    # 迁移指南
    migration_example()

    # 最佳实践
    best_practices()

    # API 变更总结
    api_changes_summary()

    print("\n" + "=" * 60)
    print("🎯 总结")
    print("=" * 60)
    print("""
v3.7.0 Repository 核心变更：

1. 🔴 Breaking Change: 构造函数接收 Session 而非 Database
2. ✅ 与 UnitOfWork 无缝集成
3. ✅ 支持自动回滚
4. ✅ 事务边界更清晰

迁移成本：低（仅需修改构造函数和测试fixture）
迁移收益：高（自动回滚、代码简化、测试隔离）

推荐：立即迁移到 v3.7！
    """)

    print("\n" + "=" * 60)
    print("✅ 示例代码说明完成！")
    print("=" * 60)
    print("下一步：运行 03_auto_rollback_testing.py 体验自动回滚")
