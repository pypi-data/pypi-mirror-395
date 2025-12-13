"""查询构建器 - 支持复杂SQL查询条件

v1.4.0 新增 - 提供灵活的查询条件构建能力

支持的操作:
- 精确匹配 (==, !=)
- 大小比较 (>, >=, <, <=)
- 模糊查询 (LIKE)
- 列表查询 (IN)
- 范围查询 (BETWEEN)
- NULL检查 (IS NULL, IS NOT NULL)
- 逻辑组合 (AND, OR)

示例:
    spec = (QuerySpec("status") == "ACTIVE") & (QuerySpec("amount").between(100, 500))
    spec = spec | (QuerySpec("is_deleted") == True)
    results = repo.find_all(spec)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any


class Operator(str, Enum):
    """SQL操作符"""

    EQ = "="
    NE = "!="
    GT = ">"
    GE = ">="
    LT = "<"
    LE = "<="
    LIKE = "LIKE"
    IN = "IN"
    BETWEEN = "BETWEEN"
    IS_NULL = "IS NULL"
    IS_NOT_NULL = "IS NOT NULL"


@dataclass
class WhereClause:
    """WHERE子句"""

    sql: str  # WHERE后的SQL表达式
    params: dict[str, Any]  # 参数字典


class QueryCondition(ABC):
    """查询条件抽象基类"""

    @abstractmethod
    def to_where_clause(self, param_prefix: str = "param") -> WhereClause:
        """转换为WHERE子句

        Args:
            param_prefix: 参数名前缀

        Returns:
            WHERE子句
        """
        pass


class SimpleCondition(QueryCondition):
    """简单条件（单列操作）"""

    def __init__(self, column: str, operator: Operator, value: Any):
        """
        初始化简单条件

        Args:
            column: 列名
            operator: 操作符
            value: 值（对于BETWEEN是(start, end)元组，对于IN是列表）
        """
        self.column = column
        self.operator = operator
        self.value = value

    def to_where_clause(self, param_prefix: str = "param") -> WhereClause:
        """转换为WHERE子句"""
        if self.operator == Operator.IS_NULL:
            return WhereClause(f"{self.column} IS NULL", {})
        elif self.operator == Operator.IS_NOT_NULL:
            return WhereClause(f"{self.column} IS NOT NULL", {})
        elif self.operator == Operator.BETWEEN:
            start, end = self.value
            param_start = f"{param_prefix}_start"
            param_end = f"{param_prefix}_end"
            sql = f"{self.column} BETWEEN :{param_start} AND :{param_end}"
            params = {param_start: start, param_end: end}
            return WhereClause(sql, params)
        elif self.operator == Operator.IN:
            placeholders = [f":{param_prefix}_{i}" for i in range(len(self.value))]
            params = {f"{param_prefix}_{i}": v for i, v in enumerate(self.value)}
            sql = f"{self.column} IN ({','.join(placeholders)})"
            return WhereClause(sql, params)
        else:
            param_name = param_prefix
            sql = f"{self.column} {self.operator.value} :{param_name}"
            params = {param_name: self.value}
            return WhereClause(sql, params)


class CompoundCondition(QueryCondition):
    """复合条件（AND/OR）"""

    def __init__(self, left: QueryCondition, operator: str, right: QueryCondition):
        """
        初始化复合条件

        Args:
            left: 左条件
            operator: AND或OR
            right: 右条件
        """
        self.left = left
        self.operator = operator  # "AND" or "OR"
        self.right = right

    def to_where_clause(self, param_prefix: str = "param") -> WhereClause:
        """转换为WHERE子句"""
        left_clause = self.left.to_where_clause(f"{param_prefix}_l")
        right_clause = self.right.to_where_clause(f"{param_prefix}_r")

        sql = f"({left_clause.sql}) {self.operator} ({right_clause.sql})"
        params = {**left_clause.params, **right_clause.params}

        return WhereClause(sql, params)


class QuerySpec:
    """
    查询规范 - 支持链式调用构建复杂查询条件

    示例:
        spec = QuerySpec("status") == "ACTIVE"
        spec = spec & (QuerySpec("amount").between(100, 500))
        spec = spec | (QuerySpec("is_deleted") == True)
    """

    def __init__(self, column: str):
        """
        初始化查询规范

        Args:
            column: 列名
        """
        self.column = column
        self._condition: QueryCondition | None = None

    def __eq__(self, value: Any) -> "QuerySpec":
        """
        相等比较: column = value

        Args:
            value: 值

        Returns:
            QuerySpec实例
        """
        result = QuerySpec(self.column)
        result._condition = SimpleCondition(self.column, Operator.EQ, value)
        return result

    def __ne__(self, value: Any) -> "QuerySpec":
        """不等比较: column != value"""
        result = QuerySpec(self.column)
        result._condition = SimpleCondition(self.column, Operator.NE, value)
        return result

    def __gt__(self, value: Any) -> "QuerySpec":
        """大于: column > value"""
        result = QuerySpec(self.column)
        result._condition = SimpleCondition(self.column, Operator.GT, value)
        return result

    def __ge__(self, value: Any) -> "QuerySpec":
        """大于等于: column >= value"""
        result = QuerySpec(self.column)
        result._condition = SimpleCondition(self.column, Operator.GE, value)
        return result

    def __lt__(self, value: Any) -> "QuerySpec":
        """小于: column < value"""
        result = QuerySpec(self.column)
        result._condition = SimpleCondition(self.column, Operator.LT, value)
        return result

    def __le__(self, value: Any) -> "QuerySpec":
        """小于等于: column <= value"""
        result = QuerySpec(self.column)
        result._condition = SimpleCondition(self.column, Operator.LE, value)
        return result

    def like(self, pattern: str) -> "QuerySpec":
        """
        模糊查询: column LIKE pattern

        Args:
            pattern: 模式，如 '%test%'

        Returns:
            QuerySpec实例

        Examples:
            spec = QuerySpec("name").like("%test%")
        """
        result = QuerySpec(self.column)
        result._condition = SimpleCondition(self.column, Operator.LIKE, pattern)
        return result

    def in_list(self, values: list[Any]) -> "QuerySpec":
        """
        列表查询: column IN (...)

        Args:
            values: 值列表

        Returns:
            QuerySpec实例

        Examples:
            spec = QuerySpec("status").in_list(["ACTIVE", "PENDING"])
        """
        result = QuerySpec(self.column)
        result._condition = SimpleCondition(self.column, Operator.IN, values)
        return result

    def between(self, start: Any, end: Any) -> "QuerySpec":
        """
        范围查询: column BETWEEN start AND end

        Args:
            start: 起始值
            end: 结束值

        Returns:
            QuerySpec实例

        Examples:
            spec = QuerySpec("amount").between(100, 500)
        """
        result = QuerySpec(self.column)
        result._condition = SimpleCondition(self.column, Operator.BETWEEN, (start, end))
        return result

    def is_null(self) -> "QuerySpec":
        """
        NULL检查: column IS NULL

        Returns:
            QuerySpec实例

        Examples:
            spec = QuerySpec("deleted_at").is_null()
        """
        result = QuerySpec(self.column)
        result._condition = SimpleCondition(self.column, Operator.IS_NULL, None)
        return result

    def is_not_null(self) -> "QuerySpec":
        """
        非NULL检查: column IS NOT NULL

        Returns:
            QuerySpec实例

        Examples:
            spec = QuerySpec("deleted_at").is_not_null()
        """
        result = QuerySpec(self.column)
        result._condition = SimpleCondition(self.column, Operator.IS_NOT_NULL, None)
        return result

    def __and__(self, other: "QuerySpec") -> "QuerySpec":
        """
        AND逻辑组合: spec1 AND spec2

        Args:
            other: 另一个QuerySpec

        Returns:
            QuerySpec实例

        Examples:
            spec = (QuerySpec("status") == "ACTIVE") & (QuerySpec("amount") > 100)
        """
        if not self._condition or not other._condition:
            raise ValueError("不能对未初始化的QuerySpec进行AND操作")

        result = QuerySpec("")
        result._condition = CompoundCondition(self._condition, "AND", other._condition)
        return result

    def __or__(self, other: "QuerySpec") -> "QuerySpec":
        """
        OR逻辑组合: spec1 OR spec2

        Args:
            other: 另一个QuerySpec

        Returns:
            QuerySpec实例

        Examples:
            spec = (QuerySpec("status") == "DELETED") | (QuerySpec("status") == "ARCHIVED")
        """
        if not self._condition or not other._condition:
            raise ValueError("不能对未初始化的QuerySpec进行OR操作")

        result = QuerySpec("")
        result._condition = CompoundCondition(self._condition, "OR", other._condition)
        return result

    def to_where_clause(self, param_prefix: str = "param") -> WhereClause:
        """
        转换为WHERE子句

        Args:
            param_prefix: 参数名前缀

        Returns:
            WHERE子句

        Examples:
            clause = spec.to_where_clause()
            sql = f"SELECT * FROM table WHERE {clause.sql}"
        """
        if not self._condition:
            raise ValueError("QuerySpec未初始化")
        return self._condition.to_where_clause(param_prefix)

    def get_where_sql_and_params(self) -> tuple[str, dict[str, Any]]:
        """
        获取WHERE SQL和参数

        Returns:
            (SQL字符串, 参数字典) 元组

        Examples:
            sql, params = spec.get_where_sql_and_params()
        """
        clause = self.to_where_clause()
        return clause.sql, clause.params


__all__ = [
    "QuerySpec",
    "QueryCondition",
    "SimpleCondition",
    "CompoundCondition",
    "Operator",
    "WhereClause",
]
