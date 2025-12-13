"""测试 GraphQL 数据模型"""

import pytest

from df_test_framework.capabilities.clients.graphql.models import (
    GraphQLError,
    GraphQLRequest,
    GraphQLResponse,
)


class TestGraphQLError:
    """测试 GraphQLError 模型"""

    def test_create_error_with_message(self) -> None:
        """测试创建基本错误"""
        error = GraphQLError(message="Field not found")
        assert error.message == "Field not found"
        assert error.locations is None
        assert error.path is None
        assert error.extensions is None

    def test_create_error_with_location(self) -> None:
        """测试创建带位置的错误"""
        error = GraphQLError(
            message="Syntax error",
            locations=[{"line": 1, "column": 5}],
        )
        assert error.message == "Syntax error"
        assert error.locations == [{"line": 1, "column": 5}]

    def test_create_error_with_path(self) -> None:
        """测试创建带路径的错误"""
        error = GraphQLError(
            message="Cannot return null",
            path=["user", "email"],
        )
        assert error.path == ["user", "email"]

    def test_error_string_representation(self) -> None:
        """测试错误字符串表示"""
        error = GraphQLError(
            message="Field not found",
            path=["user", "posts", 0, "title"],
            locations=[{"line": 2, "column": 10}],
        )
        error_str = str(error)
        assert "GraphQL Error: Field not found" in error_str
        assert "Path: user.posts.0.title" in error_str


class TestGraphQLRequest:
    """测试 GraphQLRequest 模型"""

    def test_create_simple_request(self) -> None:
        """测试创建简单请求"""
        request = GraphQLRequest(query="{ user { id name } }")
        assert request.query == "{ user { id name } }"
        assert request.variables is None
        assert request.operation_name is None

    def test_create_request_with_variables(self) -> None:
        """测试创建带变量的请求"""
        request = GraphQLRequest(
            query="query GetUser($id: ID!) { user(id: $id) { name } }",
            variables={"id": "123"},
        )
        assert request.variables == {"id": "123"}

    def test_create_request_with_operation_name(self) -> None:
        """测试创建带操作名的请求"""
        request = GraphQLRequest(
            query="query GetUser { user { id } }",
            operation_name="GetUser",
        )
        assert request.operation_name == "GetUser"


class TestGraphQLResponse:
    """测试 GraphQLResponse 模型"""

    def test_create_successful_response(self) -> None:
        """测试创建成功响应"""
        response = GraphQLResponse(data={"user": {"id": "123", "name": "Alice"}})
        assert response.data == {"user": {"id": "123", "name": "Alice"}}
        assert response.errors is None
        assert response.is_success is True
        assert response.has_data is True

    def test_create_error_response(self) -> None:
        """测试创建错误响应"""
        response = GraphQLResponse(errors=[GraphQLError(message="Field not found")])
        assert response.is_success is False
        assert response.has_data is False

    def test_get_field(self) -> None:
        """测试获取字段"""
        response = GraphQLResponse(data={"user": {"id": "123", "name": "Alice"}})
        assert response.get_field("user") == {"id": "123", "name": "Alice"}
        assert response.get_field("nonexistent") is None

    def test_get_field_without_data(self) -> None:
        """测试在无数据时获取字段"""
        response = GraphQLResponse(data=None)
        assert response.get_field("user") is None

    def test_raise_for_errors_success(self) -> None:
        """测试成功响应不抛出异常"""
        response = GraphQLResponse(data={"user": {"id": "123"}})
        response.raise_for_errors()  # 不应抛出异常

    def test_raise_for_errors_with_errors(self) -> None:
        """测试错误响应抛出异常"""
        response = GraphQLResponse(errors=[GraphQLError(message="Field not found")])
        with pytest.raises(RuntimeError, match="GraphQL request failed"):
            response.raise_for_errors()

    def test_response_with_extensions(self) -> None:
        """测试带扩展信息的响应"""
        response = GraphQLResponse(
            data={"user": {"id": "123"}},
            extensions={"tracing": {"duration": 123}},
        )
        assert response.extensions == {"tracing": {"duration": 123}}
