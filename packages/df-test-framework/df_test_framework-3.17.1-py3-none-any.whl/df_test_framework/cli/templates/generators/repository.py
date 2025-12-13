"""Repository类生成模板"""

GEN_REPOSITORY_TEMPLATE = """\"\"\"Repository: {entity_name}

使用Repository模式封装{entity_name}的数据库操作。

v3.8.0+ 特性：
- ✅ 接收 Session 而非 Database
- ✅ 配合 UnitOfWork 使用
- ✅ 支持自动事务管理和回滚
\"\"\"

from typing import Any

from sqlalchemy.orm import Session

from df_test_framework import BaseRepository


class {EntityName}Repository(BaseRepository):
    \"\"\"{EntityName}数据仓库

    封装{entity_name}的数据库CRUD操作。

    v3.8.0+ 变更：
    - 🔴 构造函数接收 Session 而非 Database
    - ✅ 与 UnitOfWork 配合使用
    - ✅ 支持自动回滚

    使用示例：
        >>> # 通过 UnitOfWork 使用
        >>> with uow:
        ...     repo = uow.repository({EntityName}Repository)
        ...     # 查询
        ...     item = repo.find_by_id(1)
        ...     items = repo.find_all()
        ...     # 创建
        ...     new_id = repo.create({{"name": "test"}})
        ...     # 更新
        ...     repo.update(conditions={{"id": 1}}, data={{"status": "inactive"}})
        ...     # 删除
        ...     repo.delete(1)
        ...     uow.commit()
    \"\"\"

    def __init__(self, session: Session):
        \"\"\"初始化Repository

        Args:
            session: SQLAlchemy Session 对象
        \"\"\"
        super().__init__(session, table_name="{table_name}")

    def find_by_name(self, name: str) -> dict[str, Any] | None:
        \"\"\"根据名称查询

        Args:
            name: 名称

        Returns:
            Dict或None: 查询结果
        \"\"\"
        return self.find_one({{"name": name}})

    def find_by_status(self, status: str) -> list[dict[str, Any]]:
        \"\"\"根据状态查询

        Args:
            status: 状态

        Returns:
            List[Dict]: 查询结果列表
        \"\"\"
        return self.find_all({{"status": status}})

    def count_by_status(self, status: str) -> int:
        \"\"\"统计指定状态的数量

        Args:
            status: 状态

        Returns:
            int: 数量
        \"\"\"
        return self.count({{"status": status}})

    # TODO: 添加更多业务查询方法


__all__ = ["{EntityName}Repository"]
"""

__all__ = ["GEN_REPOSITORY_TEMPLATE"]
