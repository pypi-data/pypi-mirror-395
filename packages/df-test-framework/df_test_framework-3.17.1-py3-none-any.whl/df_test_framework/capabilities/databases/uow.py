"""Unit of Work 模式实现

v3.7.0 新增 - 现代化数据访问架构

Unit of Work 模式提供:
- 统一的事务边界管理
- 多个 Repository 共享同一 Session
- 显式的提交/回滚控制
- 测试友好的数据隔离

v3.14.0 新增:
- 集成 EventBus 发布事务事件
- 支持 event_bus 参数

v3.17.1 更新:
- commit() 和 rollback() 发布事务事件
- 改为同步事件发布（publish_sync）

使用示例:
    >>> with UnitOfWork(session_factory) as uow:
    ...     card = uow.cards.find_by_no("CARD001")
    ...     uow.orders.create({...})
    ...     uow.commit()  # 显式提交，否则自动回滚
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from loguru import logger
from sqlalchemy.orm import Session

if TYPE_CHECKING:
    from collections.abc import Callable

    from df_test_framework.infrastructure.events import EventBus


class UnitOfWork:
    """工作单元 - 管理事务边界和 Repository 生命周期

    核心职责:
    1. 管理数据库 Session 生命周期
    2. 提供统一的事务边界（commit/rollback）
    3. 延迟创建 Repository 实例（共享同一 Session）

    设计原则:
    - Repository 只负责数据访问，不管理事务
    - UnitOfWork 负责事务边界，不负责具体查询
    - 所有 Repository 在同一 UoW 中共享 Session

    使用模式:
        # 作为上下文管理器（推荐）
        with UnitOfWork(session_factory) as uow:
            card = uow.cards.find_by_no("CARD001")
            uow.commit()

        # 在 pytest fixture 中
        @pytest.fixture
        def uow(database):
            with UnitOfWork(database.session_factory) as uow:
                yield uow
                # 自动回滚（除非已 commit）
    """

    def __init__(
        self,
        session_factory: Callable[[], Session],
        repository_package: str | None = None,
        event_bus: EventBus | None = None,
    ):
        """初始化 UnitOfWork

        Args:
            session_factory: Session 工厂函数，通常是 database.session_factory
            repository_package: Repository 包路径，启用自动发现（可选）
                               例如: "gift_card_test.repositories"
            event_bus: 🆕 v3.14.0 事件总线（可选，用于发布事务事件）

        设计说明:
            为什么使用 session_factory 而不是 runtime?
            1. **依赖倒置**: UoW 只依赖最小接口，不依赖整个 RuntimeContext
            2. **单一职责**: UoW 只负责事务管理，不关心配置、日志等基础设施
            3. **灵活性**: 可在 pytest、生产代码、脚本中复用
            4. **测试友好**: 容易 Mock 和隔离测试

        在 pytest fixture 中的正确用法:
            @pytest.fixture
            def uow(database):
                with YourProjectUoW(database.session_factory) as uow:
                    yield uow

        P1-2 自动发现示例:
            class GiftCardUoW(UnitOfWork):
                def __init__(self, session_factory):
                    super().__init__(
                        session_factory,
                        repository_package="gift_card_test.repositories"
                    )
                    # ✅ 自动发现并注册所有 Repository
                    # uow.cards, uow.orders 等自动可用
        """
        self._session_factory = session_factory
        self._session: Session | None = None
        self._repositories: dict[str, Any] = {}
        self._committed = False
        self._registered_repo_attrs: dict[str, tuple[type, str | None]] = {}
        self._event_bus = event_bus

        # P1-2: 自动发现 Repository
        if repository_package:
            self._auto_discover_repositories(repository_package)

    def _publish_event_sync(self, event: Any) -> None:
        """同步发布事件到 EventBus

        v3.14.0: 初始实现（未使用）
        v3.17.1: 改为同步发布，使用 publish_sync()
        """
        if self._event_bus:
            self._event_bus.publish_sync(event)

    def __enter__(self) -> UnitOfWork:
        """进入上下文，创建 Session"""
        self._session = self._session_factory()
        self._committed = False
        self._repositories.clear()  # 重置Repository缓存
        # 注意: _registered_repo_attrs 不重置，允许在进入上下文前注册
        logger.debug("UnitOfWork: Session 已创建")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """退出上下文，处理事务"""
        if exc_type is not None:
            # 发生异常，回滚
            self.rollback(reason="exception")
            logger.error(f"UnitOfWork: 发生异常，数据已回滚: {exc_val}")
        elif not self._committed:
            # 未提交，回滚（默认行为）
            self.rollback(reason="auto")
            logger.info("✅ UnitOfWork: 数据已回滚（自动清理）")

        self._close()

    @property
    def session(self) -> Session:
        """获取当前 Session

        Returns:
            SQLAlchemy Session 实例

        Raises:
            RuntimeError: 如果 UoW 未在上下文中使用
        """
        if self._session is None:
            raise RuntimeError("UnitOfWork 必须在 with 语句中使用")
        return self._session

    def commit(self) -> None:
        """提交事务

        显式调用 commit() 才会持久化数据，否则自动回滚。
        这是测试友好的设计：默认不保留测试数据。
        """
        self.session.commit()
        self._committed = True
        logger.info("⚠️ UnitOfWork: 数据已提交并保留到数据库")

        # v3.17.1: 发布事务提交事件
        if self._event_bus:
            from df_test_framework.core.events import TransactionCommitEvent

            event = TransactionCommitEvent.create(
                repository_count=len(self._repositories),
                session_id=str(id(self._session)) if self._session else None,
            )
            self._publish_event_sync(event)

    def rollback(self, reason: str = "manual") -> None:
        """回滚事务

        Args:
            reason: 回滚原因（auto/exception/manual）

        v3.17.1: 发布 TransactionRollbackEvent 事件
        """
        if self._session:
            self._session.rollback()

            # v3.17.1: 发布事务回滚事件
            if self._event_bus:
                from df_test_framework.core.events import TransactionRollbackEvent

                event = TransactionRollbackEvent.create(
                    repository_count=len(self._repositories),
                    reason=reason,
                    session_id=str(id(self._session)),
                )
                self._publish_event_sync(event)

    def _close(self) -> None:
        """关闭 Session"""
        if self._session:
            self._session.close()
            self._session = None
            self._repositories.clear()
            logger.debug("UnitOfWork: Session 已关闭")

    def repository(self, repo_class: type, table_name: str | None = None) -> Any:
        """获取或创建 Repository 实例

        Repository 实例会被缓存，同一 UoW 中多次获取返回相同实例。

        Args:
            repo_class: Repository 类
            table_name: 表名（可选，某些 Repository 需要）

        Returns:
            Repository 实例

        Example:
            >>> card_repo = uow.repository(CardRepository)
            >>> order_repo = uow.repository(OrderRepository)
        """
        key = repo_class.__name__
        if key not in self._repositories:
            if table_name:
                self._repositories[key] = repo_class(self.session, table_name)
            else:
                self._repositories[key] = repo_class(self.session)
        return self._repositories[key]

    def register_repository(
        self, name: str, repo_class: type, table_name: str | None = None
    ) -> None:
        """注册 Repository，使其可通过属性访问

        Args:
            name: 属性名
            repo_class: Repository 类
            table_name: 表名（可选）

        Example:
            >>> uow.register_repository("cards", CardRepository)
            >>> card = uow.cards.find_by_no("CARD001")
        """
        self._registered_repo_attrs[name] = (repo_class, table_name)

    def execute(self, sql, params=None):
        """执行原生 SQL

        Args:
            sql: SQL 语句（使用 text() 包装）
            params: 参数字典

        Returns:
            执行结果
        """
        from sqlalchemy import text

        if isinstance(sql, str):
            sql = text(sql)

        return self.session.execute(sql, params or {})

    def _auto_discover_repositories(self, package: str) -> None:
        """自动发现 Repository 类并注册（P1-2）

        扫描指定包，找到所有 BaseRepository 的子类，并自动注册为属性。

        约定规则:
        1. Repository 类必须继承 BaseRepository
        2. 类名以 Repository 结尾
        3. 自动生成属性名：CardRepository -> cards (去掉Repository + 复数)

        Args:
            package: Repository 包路径，例如 "gift_card_test.repositories"

        Example:
            # 包结构
            repositories/
            ├── __init__.py          # 导出所有 Repository
            ├── card_repository.py   → CardRepository -> uow.cards
            ├── order_repository.py  → OrderRepository -> uow.orders
            └── payment_repository.py → PaymentRepository -> uow.payments

            # v3.13.0 配置方式（推荐）
            # .env 文件中配置：
            # TEST__REPOSITORY_PACKAGE=my_project.repositories

            # 测试中直接使用框架 uow fixture
            def test_example(uow):
                card = uow.cards.find_by_no("CARD001")  # ✅ 自动发现

            # 手动创建 UnitOfWork（可选）
            with UnitOfWork(session_factory, repository_package="my_project.repositories") as uow:
                card = uow.cards.find_by_no("CARD001")  # ✅ 自动注册
        """
        import importlib
        import inspect

        try:
            # 导入包（Repository 必须在 __init__.py 中导出）
            module = importlib.import_module(package)
        except ImportError as e:
            logger.warning(f"无法导入 Repository 包 '{package}': {e}")
            return

        # 查找 BaseRepository 子类
        discovered_count = 0
        for name, obj in inspect.getmembers(module, inspect.isclass):
            # 跳过 BaseRepository 自身
            if name == "BaseRepository":
                continue

            # 检查是否继承 BaseRepository
            try:
                from df_test_framework.capabilities.databases.repositories.base import (
                    BaseRepository,
                )

                if issubclass(obj, BaseRepository) and obj != BaseRepository:
                    # 生成属性名称
                    attr_name = self._generate_repo_attr_name(name)

                    # 注册到 UoW
                    self.register_repository(attr_name, obj)
                    discovered_count += 1
                    logger.debug(f"[UoW 自动发现] {name} -> uow.{attr_name}")
            except (ImportError, TypeError):
                # 不是 BaseRepository 子类，跳过
                continue

        logger.info(f"✅ UoW 自动发现: 从 '{package}' 注册了 {discovered_count} 个 Repository")

    def _generate_repo_attr_name(self, class_name: str) -> str:
        """生成 Repository 属性名称

        规则:
        1. 移除 'Repository' 后缀
        2. 转换为 snake_case
        3. 添加复数形式（简单规则：+s）

        Args:
            class_name: Repository 类名，例如 "CardRepository"

        Returns:
            属性名，例如 "cards"

        Example:
            >>> _generate_repo_attr_name("CardRepository")
            'cards'
            >>> _generate_repo_attr_name("OrderRepository")
            'orders'
            >>> _generate_repo_attr_name("PaymentRepository")
            'payments'
        """
        import re

        # 移除 'Repository' 后缀
        name = class_name
        if name.endswith("Repository"):
            name = name[:-10]  # len("Repository") = 10

        # 转换为 snake_case
        # CamelCase -> snake_case
        name = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()

        # 简单复数规则
        # 注意：这是简化版本，只处理常见情况
        if name.endswith("y"):
            # category -> categories
            name = name[:-1] + "ies"
        elif name.endswith("s"):
            # address -> addresses
            name = name + "es"
        else:
            # card -> cards, order -> orders
            name = name + "s"

        return name

    def __getattr__(self, item: str) -> Any:
        """实例级 Repository 访问"""
        if item in self._registered_repo_attrs:
            repo_class, table_name = self._registered_repo_attrs[item]
            return self.repository(repo_class, table_name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")
