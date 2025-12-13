"""
Unit of Work 基础用法

v3.7.0 核心特性：Unit of Work (UoW) 模式

本示例演示：
1. UoW 的基本概念和创建方式
2. 显式 commit 和自动 rollback
3. Repository 通过 UoW 访问
4. 事务边界的概念

学习要点：
- ✅ UoW 是事务的边界
- ✅ with 语句管理 UoW 生命周期
- ✅ 显式 commit() 提交更改
- ✅ 异常时自动 rollback
"""

from decimal import Decimal

from sqlalchemy.orm import Session

from df_test_framework import BaseRepository
from df_test_framework.databases import BaseUnitOfWork


# ========== 示例：定义一个 Repository ==========
class UserRepository(BaseRepository):
    """用户数据仓库

    v3.7.0 变更：
    - ✅ 接收 Session 而非 Database
    - ✅ 配合 UnitOfWork 使用
    """

    def __init__(self, session: Session):
        super().__init__(session, table_name="users")

    def find_by_username(self, username: str) -> dict | None:
        """根据用户名查找"""
        return self.find_one({"username": username})


# ========== 示例1：基础 UoW 使用 ==========
def example_1_basic_uow(session_factory):
    """示例1：基础 UoW 使用 - 显式 commit"""
    print("\n" + "=" * 60)
    print("示例1：基础 UoW 使用 - 显式 commit")
    print("=" * 60)

    # ✅ 使用 with 语句管理 UoW 生命周期
    with BaseUnitOfWork(session_factory) as uow:
        print("\n1️⃣  创建 UoW（事务开始）")

        # ✅ 通过 UoW 获取 Repository
        user_repo = uow.repository(UserRepository)
        print("2️⃣  通过 UoW 获取 UserRepository")

        # ✅ 执行数据库操作
        user_data = {
            "username": "alice",
            "email": "alice@example.com",
            "balance": Decimal("100.00")
        }
        user_id = user_repo.create(user_data)
        print(f"3️⃣  创建用户: ID={user_id}, username={user_data['username']}")

        # ✅ 显式提交
        uow.commit()
        print("4️⃣  显式 commit() - 事务提交成功")

    print("5️⃣  退出 with 块 - UoW 自动关闭")
    print("✅ 数据已持久化到数据库")


# ========== 示例2：自动 Rollback ==========
def example_2_auto_rollback(session_factory):
    """示例2：异常时自动 rollback"""
    print("\n" + "=" * 60)
    print("示例2：异常时自动 rollback")
    print("=" * 60)

    try:
        with BaseUnitOfWork(session_factory) as uow:
            user_repo = uow.repository(UserRepository)

            # 创建用户
            user_id = user_repo.create({
                "username": "bob",
                "email": "bob@example.com",
                "balance": Decimal("50.00")
            })
            print(f"1️⃣  创建用户: ID={user_id}, username=bob")

            # ❌ 模拟异常发生
            print("2️⃣  模拟异常...")
            raise ValueError("模拟业务异常")

    except ValueError as e:
        print(f"3️⃣  捕获异常: {e}")
        print("4️⃣  UoW 自动 rollback - 用户创建被撤销")
        print("✅ 数据库状态恢复到事务开始前")


# ========== 示例3：无 commit 的行为 ==========
def example_3_no_commit(session_factory):
    """示例3：忘记 commit 会怎样？"""
    print("\n" + "=" * 60)
    print("示例3：忘记 commit 会怎样？")
    print("=" * 60)

    with BaseUnitOfWork(session_factory) as uow:
        user_repo = uow.repository(UserRepository)

        user_id = user_repo.create({
            "username": "charlie",
            "email": "charlie@example.com",
            "balance": Decimal("75.00")
        })
        print(f"1️⃣  创建用户: ID={user_id}, username=charlie")
        print("2️⃣  忘记调用 uow.commit()")

    print("3️⃣  退出 with 块")
    print("⚠️  数据未提交，自动 rollback")
    print("❌ 用户创建失败（数据丢失）")


# ========== 示例4：多次操作后统一 commit ==========
def example_4_batch_commit(session_factory):
    """示例4：多次操作后统一 commit"""
    print("\n" + "=" * 60)
    print("示例4：多次操作后统一 commit")
    print("=" * 60)

    with BaseUnitOfWork(session_factory) as uow:
        user_repo = uow.repository(UserRepository)

        # 创建多个用户
        print("1️⃣  批量创建用户...")
        users = [
            {"username": "dave", "email": "dave@example.com", "balance": Decimal("100")},
            {"username": "eve", "email": "eve@example.com", "balance": Decimal("200")},
            {"username": "frank", "email": "frank@example.com", "balance": Decimal("300")},
        ]

        for user_data in users:
            user_id = user_repo.create(user_data)
            print(f"   - 创建用户: {user_data['username']}, ID={user_id}")

        # 统一提交
        print("\n2️⃣  统一 commit() 提交所有操作")
        uow.commit()

    print("✅ 所有用户创建成功")


# ========== 示例5：查询操作（无需 commit） ==========
def example_5_read_operations(session_factory):
    """示例5：只读操作无需 commit"""
    print("\n" + "=" * 60)
    print("示例5：只读操作无需 commit")
    print("=" * 60)

    # 先写入测试数据
    with BaseUnitOfWork(session_factory) as uow:
        user_repo = uow.repository(UserRepository)
        user_repo.create({
            "username": "grace",
            "email": "grace@example.com",
            "balance": Decimal("150.00")
        })
        uow.commit()
        print("1️⃣  准备数据：创建用户 grace")

    # 只读操作
    with BaseUnitOfWork(session_factory) as uow:
        user_repo = uow.repository(UserRepository)

        # 查询操作
        user = user_repo.find_by_username("grace")
        print(f"\n2️⃣  查询用户: {user}")

        all_users = user_repo.find_all()
        print(f"3️⃣  查询所有用户: 共 {len(all_users)} 个")

        # ✅ 只读操作无需 commit
        print("\n4️⃣  只读操作无需 commit")

    print("✅ 查询操作完成")


# ========== 主函数 ==========
if __name__ == "__main__":
    print("\n" + "🚀 Unit of Work 基础用法")
    print("=" * 60)
    print("本示例使用内存数据库演示 UoW 基本概念")
    print("实际项目中使用 session_factory fixture")

    # 注意：这里使用伪代码，实际项目中通过 fixture 获取
    print("\n⚠️  示例代码说明：")
    print("   实际使用时，session_factory 由框架 fixture 提供")
    print("   示例代码仅用于演示 UoW 的使用模式")

    # 伪代码演示
    session_factory = None  # 实际由 fixture 提供

    try:
        # 示例1：基础用法
        # example_1_basic_uow(session_factory)

        # 示例2：自动回滚
        # example_2_auto_rollback(session_factory)

        # 示例3：忘记 commit
        # example_3_no_commit(session_factory)

        # 示例4：批量操作
        # example_4_batch_commit(session_factory)

        # 示例5：只读操作
        # example_5_read_operations(session_factory)

        print("\n" + "=" * 60)
        print("💡 关键要点总结")
        print("=" * 60)
        print("1. UoW 是事务边界，使用 with 语句管理")
        print("2. 必须显式 commit() 才能持久化更改")
        print("3. 异常时自动 rollback，保证数据一致性")
        print("4. 多次操作可以统一 commit")
        print("5. 只读操作无需 commit")

        print("\n" + "=" * 60)
        print("📚 实际使用示例")
        print("=" * 60)
        print("""
# conftest.py 中定义 fixture（框架已内置）
@pytest.fixture
def uow(session_factory):
    with BaseUnitOfWork(session_factory) as uow:
        yield uow
        # 测试结束自动 rollback

# 测试中使用
def test_create_user(uow):
    repo = uow.repository(UserRepository)
    user_id = repo.create({"username": "test"})
    assert user_id is not None
    # ✅ 测试结束自动回滚
        """)

    except Exception as e:
        print(f"\n❌ 示例执行失败: {e}")
        print("请在实际项目中使用 session_factory fixture")

    print("\n" + "=" * 60)
    print("✅ 示例代码说明完成！")
    print("=" * 60)
    print("下一步：运行 02_repository_v37.py 了解 Repository 变更")
