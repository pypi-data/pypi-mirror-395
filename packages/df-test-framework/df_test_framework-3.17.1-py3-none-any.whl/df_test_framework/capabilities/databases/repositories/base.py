"""基础Repository类

v1.3.0 新增 - Repository模式实现
提供通用的数据访问方法,子类可继承扩展

v2.0.0 更新 - 简化泛型设计
移除无用的泛型声明,所有方法直接返回字典类型

v3.7.0 更新 - 现代化架构重构
Repository 接收 Session 而非 Database，配合 UnitOfWork 使用
"""

import re
from abc import ABC
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


class BaseRepository(ABC):
    """Repository基类

    封装数据访问逻辑,提供统一的CRUD接口

    所有查询方法返回字典(Dict[str, Any])或字典列表(List[Dict[str, Any]])
    子类可以根据需要在自己的方法中转换为Pydantic模型

    v3.7.0 重要变更:
    - Repository 现在接收 Session 而非 Database
    - 配合 UnitOfWork 使用，共享同一事务
    - 所有操作在 UoW 的事务边界内执行

    v3.9.0 安全增强:
    - 表名/列名验证防止SQL注入
    - 仅支持简单标识符 (字母、数字、下划线，以字母或下划线开头)
    - 不支持带schema前缀的表名 (如 "public.users")，如需使用请通过 extra_config 或原生SQL

    示例:
        class CardRepository(BaseRepository):
            def __init__(self, session: Session):
                super().__init__(session, table_name="card_inventory")

            def find_by_card_no(self, card_no: str) -> Optional[Dict[str, Any]]:
                '''根据卡号查找卡片'''
                return self.find_one({"card_no": card_no})

            def find_active_cards(self) -> List[Dict[str, Any]]:
                '''查找所有激活的卡片'''
                return self.find_all({"status": "ACTIVE"})

        # 配合 UnitOfWork 使用
        with UnitOfWork(session_factory) as uow:
            repo = CardRepository(uow.session)
            card = repo.find_by_card_no("CARD001")
    """

    _IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
    _ORDER_BY_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(\s+(ASC|DESC))?$", re.IGNORECASE)

    def __init__(self, session: Session, table_name: str):
        """初始化Repository

        Args:
            session: SQLAlchemy Session 实例
            table_name: 表名
        """
        self.session = session
        self.table_name = self._validate_identifier(table_name, kind="table name")

    def _query_one(self, sql: str, params: dict[str, Any] | None = None) -> dict[str, Any] | None:
        """执行查询并返回单条记录

        Args:
            sql: SQL 语句
            params: 参数字典

        Returns:
            记录字典，如果不存在返回 None
        """
        result = self.session.execute(text(sql), params or {})
        row = result.mappings().first()
        return dict(row) if row else None

    def _query_all(self, sql: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """执行查询并返回多条记录

        Args:
            sql: SQL 语句
            params: 参数字典

        Returns:
            记录列表
        """
        result = self.session.execute(text(sql), params or {})
        return [dict(row) for row in result.mappings().all()]

    def _execute(self, sql: str, params: dict[str, Any] | None = None) -> int:
        """执行 SQL 语句

        Args:
            sql: SQL 语句
            params: 参数字典

        Returns:
            影响的行数
        """
        result = self.session.execute(text(sql), params or {})
        return result.rowcount

    def find_by_id(self, id_value: Any, id_column: str = "id") -> dict[str, Any] | None:
        """根据ID查找记录

        Args:
            id_value: ID值
            id_column: ID列名,默认为"id"

        Returns:
            记录字典,如果不存在返回None

        示例:
            record = repo.find_by_id(123)
            user = repo.find_by_id("user_001", id_column="user_id")
        """
        self._validate_identifier(id_column, kind="id column")
        sql = f"SELECT * FROM {self.table_name} WHERE {id_column} = :id_value"
        return self._query_one(sql, {"id_value": id_value})

    def find_one(self, conditions: dict[str, Any]) -> dict[str, Any] | None:
        """根据条件查找单条记录

        Args:
            conditions: 查询条件字典

        Returns:
            记录字典,如果不存在返回None

        示例:
            card = repo.find_one({"card_no": "CARD001", "status": "ACTIVE"})
        """
        for key in conditions.keys():
            self._validate_identifier(key, kind="column")

        where_clauses = [f"{key} = :{key}" for key in conditions.keys()]
        where_sql = " AND ".join(where_clauses)
        sql = f"SELECT * FROM {self.table_name} WHERE {where_sql}"
        return self._query_one(sql, conditions)

    def find_all(
        self,
        conditions: dict[str, Any] | None = None,
        order_by: str | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        """根据条件查找多条记录

        Args:
            conditions: 查询条件字典,None表示查询所有
            order_by: 排序字段,如"created_at DESC"
            limit: 限制返回记录数

        Returns:
            记录列表

        示例:
            # 查询所有激活的卡片,按创建时间倒序,最多100条
            cards = repo.find_all(
                conditions={"status": "ACTIVE"},
                order_by="created_at DESC",
                limit=100
            )
        """
        sql = f"SELECT * FROM {self.table_name}"
        params = {}

        if conditions:
            for key in conditions.keys():
                self._validate_identifier(key, kind="column")
            where_clauses = [f"{key} = :{key}" for key in conditions.keys()]
            where_sql = " AND ".join(where_clauses)
            sql += f" WHERE {where_sql}"
            params = conditions

        if order_by:
            sql += f" ORDER BY {self._validate_order_by(order_by)}"

        if limit:
            limit_int = int(limit)
            if limit_int < 0:
                raise ValueError("limit must be non-negative")
            sql += f" LIMIT {limit_int}"

        return self._query_all(sql, params)

    def find_by_ids(self, id_values: list[Any], id_column: str = "id") -> list[dict[str, Any]]:
        """根据ID列表批量查找记录

        Args:
            id_values: ID值列表
            id_column: ID列名,默认为"id"

        Returns:
            记录列表

        示例:
            cards = repo.find_by_ids(["CARD001", "CARD002"], id_column="card_no")
        """
        if not id_values:
            return []

        self._validate_identifier(id_column, kind="id column")
        placeholders = ",".join([f":id_{i}" for i in range(len(id_values))])
        params = {f"id_{i}": val for i, val in enumerate(id_values)}
        sql = f"SELECT * FROM {self.table_name} WHERE {id_column} IN ({placeholders})"
        return self._query_all(sql, params)

    def count(self, conditions: dict[str, Any] | None = None) -> int:
        """统计记录数

        Args:
            conditions: 查询条件字典,None表示统计所有

        Returns:
            记录总数

        示例:
            total = repo.count()
            active_count = repo.count({"status": "ACTIVE"})
        """
        sql = f"SELECT COUNT(*) as count FROM {self.table_name}"
        params = {}

        if conditions:
            for key in conditions.keys():
                self._validate_identifier(key, kind="column")
            where_clauses = [f"{key} = :{key}" for key in conditions.keys()]
            where_sql = " AND ".join(where_clauses)
            sql += f" WHERE {where_sql}"
            params = conditions

        result = self._query_one(sql, params)
        return result["count"] if result else 0

    def exists(self, conditions: dict[str, Any]) -> bool:
        """检查记录是否存在

        Args:
            conditions: 查询条件字典

        Returns:
            是否存在

        示例:
            exists = repo.exists({"card_no": "CARD001"})
        """
        return self.count(conditions) > 0

    def create(self, data: dict[str, Any]) -> int:
        """创建记录

        Args:
            data: 记录数据字典

        Returns:
            插入的记录ID (如果数据库支持)

        示例:
            card_id = repo.create({
                "card_no": "CARD001",
                "user_id": "user_001",
                "status": "ACTIVE"
            })
        """
        for key in data.keys():
            self._validate_identifier(key, kind="column")

        columns = ", ".join(data.keys())
        placeholders = ", ".join([f":{key}" for key in data.keys()])
        sql = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"

        result = self.session.execute(text(sql), data)
        # 返回最后插入的 ID
        return result.lastrowid or 0

    def batch_create(self, data_list: list[dict[str, Any]], chunk_size: int = 1000) -> int:
        """批量创建记录

        Args:
            data_list: 记录数据列表
            chunk_size: 每批次大小,默认1000

        Returns:
            插入的记录总数

        示例:
            count = repo.batch_create([
                {"card_no": "CARD001", "status": "ACTIVE"},
                {"card_no": "CARD002", "status": "ACTIVE"},
            ])
        """
        if not data_list:
            return 0

        total = 0
        for i in range(0, len(data_list), chunk_size):
            chunk = data_list[i : i + chunk_size]
            for data in chunk:
                self.create(data)
                total += 1

        return total

    def update(self, conditions: dict[str, Any], data: dict[str, Any]) -> int:
        """更新记录

        Args:
            conditions: 更新条件字典
            data: 更新数据字典

        Returns:
            影响的行数

        示例:
            # 更新卡号为CARD001的记录状态为INACTIVE
            affected = repo.update(
                conditions={"card_no": "CARD001"},
                data={"status": "INACTIVE"}
            )
        """
        for key in data.keys():
            self._validate_identifier(key, kind="column")
        for key in conditions.keys():
            self._validate_identifier(key, kind="column")

        set_clauses = [f"{key} = :{key}" for key in data.keys()]
        set_sql = ", ".join(set_clauses)

        where_clauses = [f"{key} = :where_{key}" for key in conditions.keys()]
        where_sql = " AND ".join(where_clauses)

        sql = f"UPDATE {self.table_name} SET {set_sql} WHERE {where_sql}"

        # 合并参数,条件参数加上where_前缀避免冲突
        params = {**data, **{f"where_{k}": v for k, v in conditions.items()}}

        return self._execute(sql, params)

    def delete(self, conditions: dict[str, Any]) -> int:
        """删除记录

        Args:
            conditions: 删除条件字典

        Returns:
            影响的行数

        示例:
            deleted = repo.delete({"card_no": "CARD001"})
        """
        for key in conditions.keys():
            self._validate_identifier(key, kind="column")

        where_clauses = [f"{key} = :{key}" for key in conditions.keys()]
        where_sql = " AND ".join(where_clauses)
        sql = f"DELETE FROM {self.table_name} WHERE {where_sql}"
        return self._execute(sql, conditions)

    def delete_by_ids(self, id_values: list[Any], id_column: str = "id") -> int:
        """根据ID列表批量删除记录

        Args:
            id_values: ID值列表
            id_column: ID列名,默认为"id"

        Returns:
            影响的行数

        示例:
            deleted = repo.delete_by_ids(["CARD001", "CARD002"], id_column="card_no")
        """
        if not id_values:
            return 0

        self._validate_identifier(id_column, kind="id column")
        placeholders = ",".join([f":id_{i}" for i in range(len(id_values))])
        params = {f"id_{i}": val for i, val in enumerate(id_values)}
        sql = f"DELETE FROM {self.table_name} WHERE {id_column} IN ({placeholders})"
        return self._execute(sql, params)

    def _validate_identifier(self, name: str, *, kind: str = "identifier") -> str:
        """验证表名/列名，防止SQL注入"""
        if not self._IDENTIFIER_PATTERN.fullmatch(name or ""):
            raise ValueError(f"Invalid {kind}: {name}")
        return name

    def _validate_order_by(self, order_by: str) -> str:
        """验证 ORDER BY 子句（仅允许简单列 + 可选ASC/DESC）"""
        clauses = [part.strip() for part in order_by.split(",")]
        for clause in clauses:
            if not clause:
                raise ValueError("order_by contains empty clause")
            if not self._ORDER_BY_PATTERN.fullmatch(clause):
                raise ValueError(f"Invalid order_by clause: {clause}")
        return ", ".join(clauses)
