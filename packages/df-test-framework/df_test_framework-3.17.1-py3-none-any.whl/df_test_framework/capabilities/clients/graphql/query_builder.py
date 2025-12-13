"""GraphQL 查询构建器

提供流畅的 API 来构建 GraphQL 查询、变更和订阅
"""

from __future__ import annotations

from enum import Enum
from typing import Any


class OperationType(str, Enum):
    """操作类型"""

    QUERY = "query"
    MUTATION = "mutation"
    SUBSCRIPTION = "subscription"


class QueryBuilder:
    """GraphQL 查询构建器

    Examples:
        >>> # 简单查询
        >>> query = (QueryBuilder()
        ...     .query("getUser")
        ...     .field("id")
        ...     .field("name")
        ...     .field("email")
        ...     .build())

        >>> # 带参数的查询
        >>> query = (QueryBuilder()
        ...     .query("getUser", {"id": "$userId"})
        ...     .field("id")
        ...     .field("name")
        ...     .variable("userId", "ID!")
        ...     .build())

        >>> # 嵌套字段
        >>> query = (QueryBuilder()
        ...     .query("getUser")
        ...     .field("id")
        ...     .field("posts", ["id", "title", "content"])
        ...     .build())

        >>> # Mutation
        >>> mutation = (QueryBuilder()
        ...     .mutation("createUser", {"input": "$input"})
        ...     .field("id")
        ...     .field("name")
        ...     .variable("input", "CreateUserInput!")
        ...     .build())
    """

    def __init__(self) -> None:
        self._operation_type: OperationType = OperationType.QUERY
        self._operation_name: str = ""
        self._operation_args: dict[str, Any] = {}
        self._fields: list[str | dict] = []
        self._variables: dict[str, str] = {}
        self._fragments: list[str] = []

    def query(self, name: str, args: dict[str, Any] | None = None) -> QueryBuilder:
        """设置查询操作

        Args:
            name: 查询名称
            args: 查询参数

        Returns:
            自身，支持链式调用
        """
        self._operation_type = OperationType.QUERY
        self._operation_name = name
        self._operation_args = args or {}
        return self

    def mutation(self, name: str, args: dict[str, Any] | None = None) -> QueryBuilder:
        """设置变更操作

        Args:
            name: 变更名称
            args: 变更参数

        Returns:
            自身，支持链式调用
        """
        self._operation_type = OperationType.MUTATION
        self._operation_name = name
        self._operation_args = args or {}
        return self

    def subscription(self, name: str, args: dict[str, Any] | None = None) -> QueryBuilder:
        """设置订阅操作

        Args:
            name: 订阅名称
            args: 订阅参数

        Returns:
            自身，支持链式调用
        """
        self._operation_type = OperationType.SUBSCRIPTION
        self._operation_name = name
        self._operation_args = args or {}
        return self

    def field(self, name: str, subfields: list[str] | None = None) -> QueryBuilder:
        """添加字段

        Args:
            name: 字段名称
            subfields: 子字段列表（用于嵌套对象）

        Returns:
            自身，支持链式调用
        """
        if subfields:
            self._fields.append({name: subfields})
        else:
            self._fields.append(name)
        return self

    def variable(self, name: str, var_type: str) -> QueryBuilder:
        """添加变量声明

        Args:
            name: 变量名（不带$）
            var_type: 变量类型（如 "ID!", "String", "[Int]"）

        Returns:
            自身，支持链式调用
        """
        self._variables[name] = var_type
        return self

    def fragment(self, fragment: str) -> QueryBuilder:
        """添加片段

        Args:
            fragment: 片段定义字符串

        Returns:
            自身，支持链式调用
        """
        self._fragments.append(fragment)
        return self

    def build(self) -> str:
        """构建 GraphQL 查询字符串

        Returns:
            完整的 GraphQL 查询
        """
        parts = []

        # 构建操作声明
        operation_def = self._operation_type.value
        if self._variables:
            var_declarations = ", ".join(
                f"${name}: {var_type}" for name, var_type in self._variables.items()
            )
            operation_def += f"({var_declarations})"

        parts.append(operation_def + " {")

        # 构建操作调用
        operation_call = self._operation_name
        if self._operation_args:
            args_str = ", ".join(
                f"{k}: {self._format_value(v)}" for k, v in self._operation_args.items()
            )
            operation_call += f"({args_str})"

        # 添加字段
        fields_str = self._build_fields(self._fields)
        parts.append(f"  {operation_call} {fields_str}")

        parts.append("}")

        # 添加片段
        if self._fragments:
            parts.extend(self._fragments)

        return "\n".join(parts)

    def _build_fields(self, fields: list[str | dict], indent: int = 2) -> str:
        """递归构建字段字符串"""
        if not fields:
            return ""

        lines = ["{"]
        indent_str = " " * (indent + 2)

        for field in fields:
            if isinstance(field, str):
                lines.append(f"{indent_str}{field}")
            elif isinstance(field, dict):
                for field_name, subfields in field.items():
                    subfields_str = self._build_fields(subfields, indent + 2)  # type: ignore
                    lines.append(f"{indent_str}{field_name} {subfields_str}")

        lines.append(" " * indent + "}")
        return "\n".join(lines)

    def _format_value(self, value: Any) -> str:
        """格式化参数值"""
        if isinstance(value, str):
            # 如果是变量引用（以$开头），直接返回
            if value.startswith("$"):
                return value
            # 否则作为字符串处理，加引号
            return f'"{value}"'
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif value is None:
            return "null"
        elif isinstance(value, (list, tuple)):
            formatted_items = [self._format_value(item) for item in value]
            return f"[{', '.join(formatted_items)}]"
        elif isinstance(value, dict):
            formatted_pairs = [f"{k}: {self._format_value(v)}" for k, v in value.items()]
            return "{" + ", ".join(formatted_pairs) + "}"
        else:
            return str(value)
