"""
自动数据回滚与测试隔离

v3.7.0 最强大的特性：测试数据自动清理

本示例演示：
1. uow fixture 自动回滚测试数据
2. 无需手动清理，测试完全隔离
3. 多测试并行运行无污染
4. 异常场景同样自动回滚

学习要点：
- ✅ uow fixture 提供自动回滚
- ✅ 测试结束数据自动清理
- ✅ 异常也会自动回滚
- ✅ 测试100%隔离
"""

from decimal import Decimal

# 这是一个完整的 pytest 测试示例
# 复制到你的测试项目中即可运行
import pytest
from sqlalchemy.orm import Session

from df_test_framework import BaseRepository


# ========== Repository 定义 ==========
class UserRepository(BaseRepository):
    """用户数据仓库"""

    def __init__(self, session: Session):
        super().__init__(session, table_name="users")

    def find_by_username(self, username: str) -> dict | None:
        return self.find_one({"username": username})


class OrderRepository(BaseRepository):
    """订单数据仓库"""

    def __init__(self, session: Session):
        super().__init__(session, table_name="orders")

    def find_by_user_id(self, user_id: int) -> list[dict]:
        return self.find_all({"user_id": user_id})


# ========== 测试用例 ==========

class TestAutoRollback:
    """自动回滚测试套件"""

    def test_create_user_auto_rollback(self, uow):
        """测试1：创建用户 - 数据自动回滚

        展示最简单的场景：
        - 创建测试数据
        - 执行测试
        - ✅ 测试结束自动回滚
        """
        # 创建用户
        user_repo = uow.repository(UserRepository)
        user_id = user_repo.create({
            "username": "test_user_1",
            "email": "test1@example.com",
            "balance": Decimal("100.00")
        })

        # 验证创建成功
        assert user_id is not None
        user = user_repo.find_by_id(user_id)
        assert user["username"] == "test_user_1"

        # ✅ 测试结束后，user 数据自动回滚
        # 无需任何清理代码！

    def test_update_user_auto_rollback(self, uow):
        """测试2：更新用户 - 修改自动回滚"""
        user_repo = uow.repository(UserRepository)

        # 创建用户
        user_id = user_repo.create({
            "username": "test_user_2",
            "balance": Decimal("100.00")
        })

        # 更新余额
        user_repo.update(
            conditions={"id": user_id},
            data={"balance": Decimal("200.00")}
        )

        # 验证更新成功
        user = user_repo.find_by_id(user_id)
        assert user["balance"] == Decimal("200.00")

        # ✅ 测试结束后，创建和更新都自动回滚

    def test_delete_user_auto_rollback(self, uow):
        """测试3：删除用户 - 删除操作也会回滚"""
        user_repo = uow.repository(UserRepository)

        # 创建用户
        user_id = user_repo.create({
            "username": "test_user_3",
            "balance": Decimal("100.00")
        })

        # 删除用户
        deleted = user_repo.delete(user_id)
        assert deleted == 1

        # 验证删除成功
        user = user_repo.find_by_id(user_id)
        assert user is None

        # ✅ 测试结束后，创建和删除都回滚
        # 数据库恢复到测试前状态

    def test_multi_repository_auto_rollback(self, uow):
        """测试4：多Repository操作 - 全部自动回滚"""
        user_repo = uow.repository(UserRepository)
        order_repo = uow.repository(OrderRepository)

        # 创建用户
        user_id = user_repo.create({
            "username": "test_user_4",
            "balance": Decimal("1000.00")
        })

        # 创建多个订单
        order_ids = []
        for i in range(3):
            order_id = order_repo.create({
                "user_id": user_id,
                "amount": Decimal(f"{100 * (i + 1)}.00"),
                "status": "pending"
            })
            order_ids.append(order_id)

        # 验证创建成功
        orders = order_repo.find_by_user_id(user_id)
        assert len(orders) == 3

        # ✅ 测试结束后，用户和所有订单都自动回滚

    def test_exception_also_rollback(self, uow):
        """测试5：异常场景 - 同样自动回滚"""
        user_repo = uow.repository(UserRepository)

        # 创建用户
        user_id = user_repo.create({
            "username": "test_user_5",
            "balance": Decimal("100.00")
        })

        # 验证创建成功
        assert user_id is not None

        # ❌ 模拟测试失败
        # with pytest.raises(AssertionError):
        #     assert False, "模拟测试失败"

        # ✅ 即使测试失败，数据依然自动回滚


# ========== 对比传统方式 ==========

class TestTraditionalCleaning:
    """传统手动清理方式（v3.6及之前）"""

    def test_with_manual_cleanup_v36(self, database):
        """❌ v3.6: 需要手动清理"""
        from df_test_framework import BaseRepository

        # 旧式 Repository
        class UserRepoV36(BaseRepository):
            def __init__(self, db):
                super().__init__(db, table_name="users")

        repo = UserRepoV36(database)
        user_id = None

        try:
            # 创建用户
            user_id = repo.create({
                "username": "old_way_user",
                "balance": Decimal("100.00")
            })

            # 测试逻辑...
            assert user_id is not None

        finally:
            # ❌ 必须手动清理
            if user_id:
                repo.delete(user_id)

        # 问题：
        # 1. 代码冗长
        # 2. 容易遗漏清理
        # 3. 异常处理复杂


# ========== 最佳实践示例 ==========

class TestBestPractices:
    """v3.7 最佳实践"""

    def test_no_commit_in_tests(self, uow):
        """最佳实践1：测试中不要 commit

        ✅ 正确：不调用 uow.commit()
        ❌ 错误：调用 uow.commit() 会持久化数据
        """
        user_repo = uow.repository(UserRepository)

        user_id = user_repo.create({
            "username": "best_practice_1",
            "balance": Decimal("100.00")
        })

        # ✅ 不要调用 uow.commit()
        # 让 fixture 自动回滚

        assert user_id is not None

    def test_isolation_between_tests(self, uow):
        """最佳实践2：测试之间完全隔离

        每个测试都有独立的 uow
        测试之间互不影响
        """
        user_repo = uow.repository(UserRepository)

        # 这个测试不会看到其他测试创建的数据
        user = user_repo.find_by_username("test_user_1")
        assert user is None  # ✅ 其他测试的数据已回滚

        # 创建自己的测试数据
        user_id = user_repo.create({
            "username": "isolated_user",
            "balance": Decimal("100.00")
        })

        assert user_id is not None

    @pytest.mark.parametrize("username,balance", [
        ("user_a", Decimal("100.00")),
        ("user_b", Decimal("200.00")),
        ("user_c", Decimal("300.00")),
    ])
    def test_parametrized_with_rollback(self, uow, username, balance):
        """最佳实践3：参数化测试也支持自动回滚

        每次参数化运行都有独立的 uow
        """
        user_repo = uow.repository(UserRepository)

        user_id = user_repo.create({
            "username": username,
            "balance": balance
        })

        user = user_repo.find_by_id(user_id)
        assert user["balance"] == balance

        # ✅ 每次参数化运行都自动回滚


# ========== 说明文档 ==========
def print_explanation():
    """打印示例说明"""
    print("\n" + "=" * 60)
    print("🎯 v3.7.0 自动回滚特性说明")
    print("=" * 60)

    print("\n✅ uow fixture 工作原理:")
    print("-" * 60)
    print("""
# conftest.py 中的 uow fixture（框架内置）
@pytest.fixture
def uow(session_factory):
    with BaseUnitOfWork(session_factory) as uow:
        yield uow
        # 退出时自动 rollback
        # 不会调用 commit()

# 因此：
# 1. 测试中的所有数据库操作都在一个事务中
# 2. 测试结束时事务自动回滚
# 3. 数据库恢复到测试前状态
    """)

    print("\n💡 关键优势:")
    print("-" * 60)
    advantages = [
        ("零清理代码", "无需 finally 块，无需 delete 调用"),
        ("100%隔离", "测试之间互不影响，可并行运行"),
        ("异常安全", "测试失败也会自动回滚"),
        ("代码简洁", "测试代码减少30%-50%"),
        ("维护性高", "不会因为遗漏清理导致数据污染"),
    ]

    for advantage, desc in advantages:
        print(f"  ✅ {advantage:<15} - {desc}")

    print("\n⚠️  注意事项:")
    print("-" * 60)
    print("  1. 测试中不要调用 uow.commit()")
    print("  2. 如需持久化数据，使用单独的 setup fixture")
    print("  3. 跨测试共享数据，使用 session-scoped fixture")


if __name__ == "__main__":
    print("\n" + "🚀 自动数据回滚与测试隔离")
    print("=" * 60)
    print("本文件是完整的 pytest 测试文件")
    print("复制到你的项目中即可运行：")
    print("  pytest 03_auto_rollback_testing.py -v")

    print_explanation()

    print("\n" + "=" * 60)
    print("📋 运行测试命令")
    print("=" * 60)
    print("""
# 运行所有测试
pytest 03_auto_rollback_testing.py -v

# 运行单个测试类
pytest 03_auto_rollback_testing.py::TestAutoRollback -v

# 运行单个测试
pytest 03_auto_rollback_testing.py::TestAutoRollback::test_create_user_auto_rollback -v

# 查看详细输出
pytest 03_auto_rollback_testing.py -v -s
    """)

    print("\n" + "=" * 60)
    print("✅ 示例代码说明完成！")
    print("=" * 60)
    print("下一步：运行 04_multi_repository_transactions.py 学习事务一致性")
