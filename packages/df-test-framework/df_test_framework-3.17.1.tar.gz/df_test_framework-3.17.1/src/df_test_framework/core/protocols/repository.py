"""
Repository 和 UnitOfWork 协议定义
"""

from collections.abc import Sequence
from typing import Any, Protocol, TypeVar

T = TypeVar("T")


class IRepository[T](Protocol):
    """Repository 协议

    泛型仓储接口，定义基础 CRUD 操作。
    """

    def find_by_id(self, id: Any) -> T | None:
        """根据 ID 查找"""
        ...

    def find_all(self) -> Sequence[T]:
        """查找所有"""
        ...

    def find_by(self, **kwargs: Any) -> Sequence[T]:
        """根据条件查找"""
        ...

    def create(self, entity: T) -> T:
        """创建实体"""
        ...

    def update(self, entity: T) -> T:
        """更新实体"""
        ...

    def delete(self, entity: T) -> None:
        """删除实体"""
        ...

    def delete_by_id(self, id: Any) -> bool:
        """根据 ID 删除"""
        ...


class IUnitOfWork(Protocol):
    """Unit of Work 协议

    工作单元模式接口，管理事务边界。
    """

    async def __aenter__(self) -> "IUnitOfWork":
        """进入上下文"""
        ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        """退出上下文"""
        ...

    async def commit(self) -> None:
        """提交事务"""
        ...

    async def rollback(self) -> None:
        """回滚事务"""
        ...

    def register_repository(
        self,
        name: str,
        repo_class: type[IRepository[Any]],
    ) -> None:
        """注册 Repository"""
        ...
