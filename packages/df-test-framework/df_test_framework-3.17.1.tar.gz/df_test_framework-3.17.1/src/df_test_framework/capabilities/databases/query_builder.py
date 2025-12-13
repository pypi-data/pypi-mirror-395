"""Query Builder - 流式查询构建器

提供 Fluent API 风格的 SQL 查询构建器，类型安全且易于使用。

P2-2 新增特性：
- ✅ 流式 API（Fluent Interface）
- ✅ 类型安全的查询构建
- ✅ 支持复杂 WHERE 条件
- ✅ 支持 JOIN 操作
- ✅ 自动参数化（防止 SQL 注入）

使用示例：
    >>> # 简单查询
    >>> query = QueryBuilder("users").select("id", "name").where("status", 1)
    >>> sql, params = query.build()
    >>> # SELECT id, name FROM users WHERE status = :status_0
    >>> # params: {"status_0": 1}

    >>> # 复杂查询
    >>> query = (
    ...     QueryBuilder("orders")
    ...     .select("orders.id", "users.name", "orders.amount")
    ...     .join("users", "orders.user_id", "users.id")
    ...     .where("orders.status", "paid")
    ...     .where_in("orders.type", ["online", "offline"])
    ...     .order_by("orders.created_at", "DESC")
    ...     .limit(10)
    ...     .offset(20)
    ... )
    >>> sql, params = query.build()
"""

from __future__ import annotations

from typing import Any


class QueryBuilder:
    """SQL 查询构建器

    使用 Fluent API 风格构建 SQL 查询。

    特性：
    - 自动参数化（防止 SQL 注入）
    - 链式调用
    - 类型提示支持
    - 可复用的查询条件

    Example:
        >>> # 基础查询
        >>> query = QueryBuilder("users").select("id", "name").where("status", 1)
        >>> sql, params = query.build()

        >>> # 使用数据库执行
        >>> from df_test_framework import Database
        >>> db = Database(...)
        >>> sql, params = query.build()
        >>> result = db.query_one(sql, params)
    """

    def __init__(self, table: str, database: Any = None):
        """初始化查询构建器

        Args:
            table: 表名
            database: Database 实例（可选）。如果提供，可以使用 get() 和 first() 方法直接执行查询
        """
        self._table = table
        self._database = database
        self._select_columns: list[str] = []
        self._where_conditions: list[tuple[str, str, Any]] = []  # (column, operator, value)
        self._where_in_conditions: list[tuple[str, list[Any]]] = []  # (column, values)
        self._where_not_in_conditions: list[tuple[str, list[Any]]] = []
        self._where_null_conditions: list[tuple[str, bool]] = []  # (column, is_null)
        self._joins: list[
            tuple[str, str, str, str, str]
        ] = []  # (join_type, table, left_col, right_col)
        self._order_by: list[tuple[str, str]] = []  # (column, direction)
        self._limit_value: int | None = None
        self._offset_value: int | None = None
        self._param_counter = 0

    def select(self, *columns: str) -> QueryBuilder:
        """指定查询列

        Args:
            *columns: 列名（支持表名前缀，如 "users.id"）

        Returns:
            QueryBuilder: 返回自身，支持链式调用

        Example:
            >>> query.select("id", "name", "email")
            >>> query.select("users.id", "orders.amount")
        """
        self._select_columns.extend(columns)
        return self

    def where(self, column: str, value: Any, operator: str = "=") -> QueryBuilder:
        """添加 WHERE 条件

        Args:
            column: 列名
            value: 值
            operator: 操作符，默认 "="（支持: =, !=, >, <, >=, <=, LIKE）

        Returns:
            QueryBuilder: 返回自身，支持链式调用

        Example:
            >>> query.where("status", 1)
            >>> query.where("age", 18, ">")
            >>> query.where("name", "%test%", "LIKE")
        """
        self._where_conditions.append((column, operator, value))
        return self

    def where_in(self, column: str, values: list[Any]) -> QueryBuilder:
        """添加 WHERE IN 条件

        Args:
            column: 列名
            values: 值列表

        Returns:
            QueryBuilder: 返回自身，支持链式调用

        Example:
            >>> query.where_in("status", [1, 2, 3])
            >>> query.where_in("type", ["online", "offline"])
        """
        self._where_in_conditions.append((column, values))
        return self

    def where_not_in(self, column: str, values: list[Any]) -> QueryBuilder:
        """添加 WHERE NOT IN 条件

        Args:
            column: 列名
            values: 值列表

        Returns:
            QueryBuilder: 返回自身，支持链式调用

        Example:
            >>> query.where_not_in("status", [0, -1])
        """
        self._where_not_in_conditions.append((column, values))
        return self

    def where_null(self, column: str) -> QueryBuilder:
        """添加 WHERE column IS NULL 条件

        Args:
            column: 列名

        Returns:
            QueryBuilder: 返回自身，支持链式调用

        Example:
            >>> query.where_null("deleted_at")
        """
        self._where_null_conditions.append((column, True))
        return self

    def where_not_null(self, column: str) -> QueryBuilder:
        """添加 WHERE column IS NOT NULL 条件

        Args:
            column: 列名

        Returns:
            QueryBuilder: 返回自身，支持链式调用

        Example:
            >>> query.where_not_null("email")
        """
        self._where_null_conditions.append((column, False))
        return self

    def join(
        self,
        table: str,
        left_column: str,
        right_column: str,
        join_type: str = "INNER",
    ) -> QueryBuilder:
        """添加 JOIN 子句

        Args:
            table: 要连接的表名
            left_column: 左表列名（通常是主表的列）
            right_column: 右表列名（要连接的表的列）
            join_type: JOIN 类型（INNER, LEFT, RIGHT, FULL），默认 INNER

        Returns:
            QueryBuilder: 返回自身，支持链式调用

        Example:
            >>> query.join("users", "orders.user_id", "users.id")
            >>> query.join("profiles", "users.id", "profiles.user_id", "LEFT")
        """
        self._joins.append((join_type, table, left_column, right_column))
        return self

    def left_join(self, table: str, left_column: str, right_column: str) -> QueryBuilder:
        """添加 LEFT JOIN 子句（便捷方法）

        Args:
            table: 要连接的表名
            left_column: 左表列名
            right_column: 右表列名

        Returns:
            QueryBuilder: 返回自身，支持链式调用

        Example:
            >>> query.left_join("profiles", "users.id", "profiles.user_id")
        """
        return self.join(table, left_column, right_column, "LEFT")

    def order_by(self, column: str, direction: str = "ASC") -> QueryBuilder:
        """添加 ORDER BY 子句

        Args:
            column: 列名
            direction: 排序方向（ASC 或 DESC），默认 ASC

        Returns:
            QueryBuilder: 返回自身，支持链式调用

        Example:
            >>> query.order_by("created_at", "DESC")
            >>> query.order_by("name").order_by("age", "DESC")
        """
        self._order_by.append((column, direction.upper()))
        return self

    def limit(self, value: int) -> QueryBuilder:
        """添加 LIMIT 子句

        Args:
            value: 限制数量

        Returns:
            QueryBuilder: 返回自身，支持链式调用

        Example:
            >>> query.limit(10)
        """
        self._limit_value = value
        return self

    def offset(self, value: int) -> QueryBuilder:
        """添加 OFFSET 子句

        Args:
            value: 偏移量

        Returns:
            QueryBuilder: 返回自身，支持链式调用

        Example:
            >>> query.offset(20)
        """
        self._offset_value = value
        return self

    def build(self) -> tuple[str, dict[str, Any]]:
        """构建 SQL 查询和参数

        Returns:
            tuple: (SQL 语句, 参数字典)

        Example:
            >>> sql, params = query.build()
            >>> result = database.query_all(sql, params)
        """
        params: dict[str, Any] = {}

        # SELECT 子句
        if self._select_columns:
            select_clause = f"SELECT {', '.join(self._select_columns)}"
        else:
            select_clause = "SELECT *"

        # FROM 子句
        from_clause = f"FROM {self._table}"

        # JOIN 子句
        join_clause = ""
        for join_type, table, left_col, right_col in self._joins:
            join_clause += f" {join_type} JOIN {table} ON {left_col} = {right_col}"

        # WHERE 子句
        where_parts = []

        # 普通 WHERE 条件
        for column, operator, value in self._where_conditions:
            param_name = self._get_param_name(column)
            where_parts.append(f"{column} {operator} :{param_name}")
            params[param_name] = value

        # WHERE IN 条件
        for column, values in self._where_in_conditions:
            placeholders = []
            for i, value in enumerate(values):
                param_name = f"{column.replace('.', '_')}_in_{i}"
                placeholders.append(f":{param_name}")
                params[param_name] = value
            where_parts.append(f"{column} IN ({', '.join(placeholders)})")

        # WHERE NOT IN 条件
        for column, values in self._where_not_in_conditions:
            placeholders = []
            for i, value in enumerate(values):
                param_name = f"{column.replace('.', '_')}_not_in_{i}"
                placeholders.append(f":{param_name}")
                params[param_name] = value
            where_parts.append(f"{column} NOT IN ({', '.join(placeholders)})")

        # WHERE NULL 条件
        for column, is_null in self._where_null_conditions:
            if is_null:
                where_parts.append(f"{column} IS NULL")
            else:
                where_parts.append(f"{column} IS NOT NULL")

        where_clause = ""
        if where_parts:
            where_clause = f"WHERE {' AND '.join(where_parts)}"

        # ORDER BY 子句
        order_by_clause = ""
        if self._order_by:
            order_parts = [f"{col} {direction}" for col, direction in self._order_by]
            order_by_clause = f"ORDER BY {', '.join(order_parts)}"

        # LIMIT 子句
        limit_clause = ""
        if self._limit_value is not None:
            limit_clause = f"LIMIT {self._limit_value}"

        # OFFSET 子句
        offset_clause = ""
        if self._offset_value is not None:
            offset_clause = f"OFFSET {self._offset_value}"

        # 组装 SQL
        sql_parts = [
            select_clause,
            from_clause,
            join_clause,
            where_clause,
            order_by_clause,
            limit_clause,
            offset_clause,
        ]

        sql = " ".join(part for part in sql_parts if part)

        return sql, params

    def _get_param_name(self, column: str) -> str:
        """生成参数名称

        Args:
            column: 列名

        Returns:
            str: 参数名称
        """
        # 移除表名前缀（如果有）
        column_name = column.split(".")[-1]
        param_name = f"{column_name}_{self._param_counter}"
        self._param_counter += 1
        return param_name

    def get(self) -> list[dict[str, Any]]:
        """执行查询并返回所有结果

        需要在初始化时提供 database 参数才能使用此方法。

        Returns:
            list[dict[str, Any]]: 查询结果列表

        Raises:
            ValueError: 如果未提供 database 实例

        Example:
            >>> # 使用 Database.table() 方法（推荐）
            >>> results = database.table("users").where("status", 1).get()

            >>> # 或者手动传入 database
            >>> from df_test_framework.capabilities.databases import QueryBuilder, Database
            >>> db = Database(...)
            >>> results = QueryBuilder("users", db).where("status", 1).get()
        """
        if not self._database:
            raise ValueError(
                "需要 Database 实例才能使用 get() 方法。"
                "请使用 database.table() 创建 QueryBuilder，或在构造时传入 database 参数"
            )

        sql, params = self.build()
        return self._database.query_all(sql, params)

    def first(self) -> dict[str, Any] | None:
        """执行查询并返回第一条结果

        需要在初始化时提供 database 参数才能使用此方法。

        Returns:
            dict[str, Any] | None: 第一条记录，如果没有结果则返回 None

        Raises:
            ValueError: 如果未提供 database 实例

        Example:
            >>> # 使用 Database.table() 方法（推荐）
            >>> user = database.table("users").where("user_id", "123").first()

            >>> # 或者手动传入 database
            >>> from df_test_framework.capabilities.databases import QueryBuilder, Database
            >>> db = Database(...)
            >>> user = QueryBuilder("users", db).where("user_id", "123").first()
        """
        if not self._database:
            raise ValueError(
                "需要 Database 实例才能使用 first() 方法。"
                "请使用 database.table() 创建 QueryBuilder，或在构造时传入 database 参数"
            )

        sql, params = self.build()
        return self._database.query_one(sql, params)


__all__ = ["QueryBuilder"]
