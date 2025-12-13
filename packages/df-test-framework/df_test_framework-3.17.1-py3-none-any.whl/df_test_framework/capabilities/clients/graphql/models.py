"""GraphQL 数据模型"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class GraphQLError(BaseModel):
    """GraphQL 错误模型"""

    message: str = Field(..., description="错误消息")
    locations: list[dict[str, int]] | None = Field(None, description="错误位置")
    path: list[str | int] | None = Field(None, description="错误路径")
    extensions: dict[str, Any] | None = Field(None, description="扩展信息")

    def __str__(self) -> str:
        """格式化错误消息"""
        parts = [f"GraphQL Error: {self.message}"]
        if self.path:
            parts.append(f"Path: {'.'.join(str(p) for p in self.path)}")
        if self.locations:
            parts.append(f"Location: {self.locations}")
        return "\n".join(parts)


class GraphQLRequest(BaseModel):
    """GraphQL 请求模型"""

    query: str = Field(..., description="GraphQL 查询或变更语句")
    variables: dict[str, Any] | None = Field(None, description="查询变量")
    operation_name: str | None = Field(None, description="操作名称")

    model_config = {"frozen": False}


class GraphQLResponse(BaseModel):
    """GraphQL 响应模型"""

    data: dict[str, Any] | None = Field(None, description="响应数据")
    errors: list[GraphQLError] | None = Field(None, description="错误列表")
    extensions: dict[str, Any] | None = Field(None, description="扩展信息")

    model_config = {"frozen": False}

    @property
    def is_success(self) -> bool:
        """是否成功（无错误）"""
        return self.errors is None or len(self.errors) == 0

    @property
    def has_data(self) -> bool:
        """是否包含数据"""
        return self.data is not None

    def get_field(self, field_name: str) -> Any:
        """获取响应数据中的字段"""
        if not self.has_data:
            return None
        return self.data.get(field_name)  # type: ignore

    def raise_for_errors(self) -> None:
        """如果有错误则抛出异常"""
        if not self.is_success:
            error_messages = "\n".join(str(e) for e in self.errors)  # type: ignore
            raise RuntimeError(f"GraphQL request failed:\n{error_messages}")
