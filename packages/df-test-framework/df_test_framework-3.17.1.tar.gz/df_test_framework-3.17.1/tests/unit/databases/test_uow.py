"""Unit of Work 模式单元测试

测试覆盖：
- ✅ 事务提交(commit)
- ✅ 事务回滚(rollback)
- ✅ Repository懒加载
- ✅ Repository缓存机制
- ✅ Session共享机制
- ✅ 上下文管理器(__enter__/__exit__)
- ✅ 多Repository协作
- ✅ 异常处理
- ✅ UnitOfWork 属性扩展

v3.13.0 更新：移除 BaseUnitOfWork，使用 UnitOfWork
"""

from __future__ import annotations

import pytest
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from df_test_framework.capabilities.databases.repositories.base import BaseRepository
from df_test_framework.capabilities.databases.uow import UnitOfWork

# 测试用ORM模型
Base = declarative_base()


class User(Base):
    """测试用户表"""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    email = Column(String(100))


class Order(Base):
    """测试订单表"""

    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    amount = Column(Integer)


# 测试用Repository
class UserRepository(BaseRepository):
    """用户Repository"""

    def __init__(self, session: Session):
        super().__init__(session, table_name="users")

    def find_by_name(self, name: str) -> dict | None:
        """按名称查找用户"""
        return self.find_one({"name": name})


class OrderRepository(BaseRepository):
    """订单Repository"""

    def __init__(self, session: Session):
        super().__init__(session, table_name="orders")

    def find_by_user_id(self, user_id: int) -> list[dict]:
        """查找用户的所有订单"""
        return self.find_all({"user_id": user_id})


# 测试用项目级UoW（v3.13.0: 直接继承 UnitOfWork）
class ProjectTestUoW(UnitOfWork):
    """测试专用 UnitOfWork"""

    @property
    def users(self) -> UserRepository:
        return self.repository(UserRepository)

    @property
    def orders(self) -> OrderRepository:
        return self.repository(OrderRepository)


@pytest.fixture(scope="function")
def engine():
    """创建内存数据库引擎"""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture(scope="function")
def session_factory(engine):
    """创建Session工厂"""
    return sessionmaker(bind=engine)


class TestUnitOfWorkBasic:
    """UnitOfWork基础功能测试"""

    def test_context_manager_creates_session(self, session_factory):
        """测试上下文管理器创建Session"""
        with UnitOfWork(session_factory) as uow:
            assert uow.session is not None
            assert isinstance(uow.session, Session)

    def test_session_property_outside_context_raises_error(self, session_factory):
        """测试在上下文外访问session抛出异常"""
        uow = UnitOfWork(session_factory)
        with pytest.raises(RuntimeError, match="UnitOfWork 必须在 with 语句中使用"):
            _ = uow.session

    def test_repository_creation(self, session_factory):
        """测试Repository创建"""
        with UnitOfWork(session_factory) as uow:
            user_repo = uow.repository(UserRepository)
            assert user_repo is not None
            assert isinstance(user_repo, UserRepository)

    def test_repository_caching(self, session_factory):
        """测试Repository缓存机制"""
        with UnitOfWork(session_factory) as uow:
            repo1 = uow.repository(UserRepository)
            repo2 = uow.repository(UserRepository)
            # 应该返回同一个实例
            assert repo1 is repo2

    def test_session_sharing_across_repositories(self, session_factory):
        """测试Repository共享Session"""
        with UnitOfWork(session_factory) as uow:
            user_repo = uow.repository(UserRepository)
            order_repo = uow.repository(OrderRepository)

            # 所有Repository应该共享同一个Session
            assert user_repo.session is uow.session
            assert order_repo.session is uow.session
            assert user_repo.session is order_repo.session


class TestUnitOfWorkTransaction:
    """UnitOfWork事务管理测试"""

    def test_commit_persists_data(self, session_factory):
        """测试commit持久化数据"""
        # 第一个UoW: 创建并提交
        with UnitOfWork(session_factory) as uow:
            user_repo = uow.repository(UserRepository)
            user_id = user_repo.create({"name": "alice", "email": "alice@example.com"})
            uow.commit()

        # 第二个UoW: 验证数据已持久化
        with UnitOfWork(session_factory) as uow:
            user_repo = uow.repository(UserRepository)
            user = user_repo.find_by_id(user_id)
            assert user is not None
            assert user["name"] == "alice"

    def test_rollback_without_commit(self, session_factory):
        """测试未commit自动回滚"""
        # 第一个UoW: 创建但不提交
        user_id = None
        with UnitOfWork(session_factory) as uow:
            user_repo = uow.repository(UserRepository)
            user_id = user_repo.create({"name": "bob", "email": "bob@example.com"})
            # 不调用 commit()

        # 第二个UoW: 验证数据已回滚
        with UnitOfWork(session_factory) as uow:
            user_repo = uow.repository(UserRepository)
            user = user_repo.find_by_id(user_id)
            assert user is None

    def test_explicit_rollback(self, session_factory):
        """测试显式回滚"""
        with UnitOfWork(session_factory) as uow:
            user_repo = uow.repository(UserRepository)
            user_id = user_repo.create({"name": "charlie", "email": "charlie@example.com"})

            # 显式回滚
            uow.rollback()

            # 同一Session中查询，应该找不到（已回滚）
            user = user_repo.find_by_id(user_id)
            assert user is None

    def test_exception_triggers_rollback(self, session_factory):
        """测试异常触发自动回滚"""
        user_id = None
        try:
            with UnitOfWork(session_factory) as uow:
                user_repo = uow.repository(UserRepository)
                user_id = user_repo.create({"name": "david", "email": "david@example.com"})
                raise ValueError("模拟异常")
        except ValueError:
            pass

        # 验证数据已回滚
        with UnitOfWork(session_factory) as uow:
            user_repo = uow.repository(UserRepository)
            user = user_repo.find_by_id(user_id)
            assert user is None


class TestUnitOfWorkMultiRepository:
    """UnitOfWork多Repository协作测试"""

    def test_multiple_repositories_share_transaction(self, session_factory):
        """测试多个Repository共享事务"""
        with UnitOfWork(session_factory) as uow:
            user_repo = uow.repository(UserRepository)
            order_repo = uow.repository(OrderRepository)

            # 创建用户
            user_id = user_repo.create({"name": "alice", "email": "alice@example.com"})

            # 创建订单
            order_repo.create({"user_id": user_id, "amount": 100})

            # 提交事务
            uow.commit()

        # 验证数据已持久化
        with UnitOfWork(session_factory) as uow:
            user_repo = uow.repository(UserRepository)
            order_repo = uow.repository(OrderRepository)

            user = user_repo.find_by_id(user_id)
            assert user["name"] == "alice"

            orders = order_repo.find_by_user_id(user_id)
            assert len(orders) == 1
            assert orders[0]["amount"] == 100

    def test_multi_repository_rollback_atomicity(self, session_factory):
        """测试多Repository回滚的原子性"""
        user_id = None
        order_id = None

        with UnitOfWork(session_factory) as uow:
            user_repo = uow.repository(UserRepository)
            order_repo = uow.repository(OrderRepository)

            # 创建用户和订单
            user_id = user_repo.create({"name": "bob", "email": "bob@example.com"})
            order_id = order_repo.create({"user_id": user_id, "amount": 200})

            # 不提交，自动回滚

        # 验证用户和订单都已回滚
        with UnitOfWork(session_factory) as uow:
            user_repo = uow.repository(UserRepository)
            order_repo = uow.repository(OrderRepository)

            user = user_repo.find_by_id(user_id)
            assert user is None

            order = order_repo.find_by_id(order_id)
            assert order is None


class TestBaseUnitOfWork:
    """UnitOfWork 属性扩展测试"""

    def test_custom_uow_with_properties(self, session_factory):
        """测试自定义UoW的属性访问"""
        with ProjectTestUoW(session_factory) as uow:
            # 通过属性访问Repository
            assert hasattr(uow, "users")
            assert hasattr(uow, "orders")

            assert isinstance(uow.users, UserRepository)
            assert isinstance(uow.orders, OrderRepository)

    def test_custom_uow_property_caching(self, session_factory):
        """测试自定义UoW的属性缓存"""
        with ProjectTestUoW(session_factory) as uow:
            users1 = uow.users
            users2 = uow.users

            # 应该返回同一个实例
            assert users1 is users2

    def test_custom_uow_transaction_control(self, session_factory):
        """测试自定义UoW的事务控制"""
        with ProjectTestUoW(session_factory) as uow:
            # 使用属性创建数据
            user_id = uow.users.create({"name": "alice", "email": "alice@example.com"})
            order_id = uow.orders.create({"user_id": user_id, "amount": 100})

            uow.commit()

        # 验证数据已持久化
        with ProjectTestUoW(session_factory) as uow:
            user = uow.users.find_by_id(user_id)
            order = uow.orders.find_by_id(order_id)

            assert user["name"] == "alice"
            assert order["amount"] == 100


class TestUnitOfWorkExecuteSQL:
    """UnitOfWork原生SQL执行测试"""

    def test_execute_sql(self, session_factory):
        """测试执行原生SQL"""
        with UnitOfWork(session_factory) as uow:
            # 插入数据
            uow.execute(
                "INSERT INTO users (name, email) VALUES (:name, :email)",
                {"name": "test", "email": "test@example.com"},
            )
            uow.commit()

        # 验证数据
        with UnitOfWork(session_factory) as uow:
            result = uow.execute("SELECT * FROM users WHERE name = :name", {"name": "test"})
            user = result.fetchone()
            assert user is not None
            assert user.name == "test"

    def test_execute_sql_with_rollback(self, session_factory):
        """测试SQL执行的回滚"""
        with UnitOfWork(session_factory) as uow:
            uow.execute(
                "INSERT INTO users (name, email) VALUES (:name, :email)",
                {"name": "rollback_test", "email": "rollback@example.com"},
            )
            # 不提交

        # 验证数据已回滚
        with UnitOfWork(session_factory) as uow:
            result = uow.execute(
                "SELECT * FROM users WHERE name = :name", {"name": "rollback_test"}
            )
            user = result.fetchone()
            assert user is None


class TestUnitOfWorkEdgeCases:
    """UnitOfWork边缘情况测试"""

    def test_multiple_commits(self, session_factory):
        """测试多次commit"""
        with UnitOfWork(session_factory) as uow:
            user_repo = uow.repository(UserRepository)

            # 第一次提交
            user_repo.create({"name": "alice", "email": "alice@example.com"})
            uow.commit()

            # 第二次提交
            user_repo.create({"name": "bob", "email": "bob@example.com"})
            uow.commit()

        # 验证两次数据都持久化
        with UnitOfWork(session_factory) as uow:
            user_repo = uow.repository(UserRepository)
            users = user_repo.find_all()
            assert len(users) == 2

    def test_commit_after_rollback(self, session_factory):
        """测试回滚后提交"""
        with UnitOfWork(session_factory) as uow:
            user_repo = uow.repository(UserRepository)

            # 创建并回滚
            user_repo.create({"name": "alice", "email": "alice@example.com"})
            uow.rollback()

            # 再次创建并提交
            user_repo.create({"name": "bob", "email": "bob@example.com"})
            uow.commit()

        # 验证只有bob被保留
        with UnitOfWork(session_factory) as uow:
            user_repo = uow.repository(UserRepository)
            users = user_repo.find_all()
            assert len(users) == 1
            assert users[0]["name"] == "bob"

    def test_repository_with_table_name(self, session_factory):
        """测试Repository指定表名"""
        with UnitOfWork(session_factory) as uow:
            # 使用table_name参数
            user_repo = uow.repository(BaseRepository, table_name="users")
            user_id = user_repo.create({"name": "test", "email": "test@example.com"})
            uow.commit()

        # 验证数据
        with UnitOfWork(session_factory) as uow:
            user_repo = uow.repository(BaseRepository, table_name="users")
            user = user_repo.find_by_id(user_id)
            assert user["name"] == "test"
