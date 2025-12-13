"""测试 GraphQL 客户端"""

from unittest.mock import MagicMock, Mock, patch

import httpx
import pytest

from df_test_framework.capabilities.clients.graphql import GraphQLClient


class TestGraphQLClient:
    """测试 GraphQLClient"""

    @pytest.fixture
    def mock_httpx_client(self):
        """Mock httpx.Client"""
        with patch("df_test_framework.capabilities.clients.graphql.client.httpx.Client") as mock:
            yield mock

    def test_init_client(self, mock_httpx_client):
        """测试初始化客户端"""
        client = GraphQLClient("https://api.example.com/graphql")

        assert client.url == "https://api.example.com/graphql"
        assert client.timeout == 30
        assert client.verify_ssl is True
        assert client.headers["Content-Type"] == "application/json"

    def test_init_with_custom_headers(self, mock_httpx_client):
        """测试使用自定义请求头初始化"""
        headers = {"Authorization": "Bearer token123"}
        client = GraphQLClient(
            "https://api.example.com/graphql",
            headers=headers,
        )

        assert "Authorization" in client.headers
        assert client.headers["Authorization"] == "Bearer token123"

    def test_set_header(self, mock_httpx_client):
        """测试设置请求头"""
        client = GraphQLClient("https://api.example.com/graphql")
        client.set_header("X-Custom-Header", "value")

        assert client.headers["X-Custom-Header"] == "value"

    def test_remove_header(self, mock_httpx_client):
        """测试移除请求头"""
        client = GraphQLClient("https://api.example.com/graphql")
        client.set_header("X-Custom-Header", "value")
        client.remove_header("X-Custom-Header")

        assert "X-Custom-Header" not in client.headers

    def test_execute_success(self, mock_httpx_client):
        """测试成功执行查询"""
        # Mock HTTP 响应
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"user": {"id": "123", "name": "Alice"}}}
        mock_response.raise_for_status = MagicMock()

        mock_client_instance = mock_httpx_client.return_value
        mock_client_instance.post.return_value = mock_response

        client = GraphQLClient("https://api.example.com/graphql")
        query = "{ user { id name } }"
        response = client.execute(query)

        assert response.is_success is True
        assert response.data == {"user": {"id": "123", "name": "Alice"}}
        mock_client_instance.post.assert_called_once()

    def test_execute_with_variables(self, mock_httpx_client):
        """测试执行带变量的查询"""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"user": {"id": "123", "name": "Alice"}}}
        mock_response.raise_for_status = MagicMock()

        mock_client_instance = mock_httpx_client.return_value
        mock_client_instance.post.return_value = mock_response

        client = GraphQLClient("https://api.example.com/graphql")
        query = "query GetUser($id: ID!) { user(id: $id) { name } }"
        variables = {"id": "123"}

        response = client.execute(query, variables)

        assert response.is_success is True
        # 验证请求参数
        call_args = mock_client_instance.post.call_args
        assert call_args[1]["json"]["variables"] == {"id": "123"}

    def test_execute_with_errors(self, mock_httpx_client):
        """测试执行返回错误"""
        mock_response = Mock()
        mock_response.json.return_value = {"errors": [{"message": "Field not found"}]}
        mock_response.raise_for_status = MagicMock()

        mock_client_instance = mock_httpx_client.return_value
        mock_client_instance.post.return_value = mock_response

        client = GraphQLClient("https://api.example.com/graphql")
        query = "{ user { invalidField } }"
        response = client.execute(query)

        assert response.is_success is False
        assert len(response.errors) == 1  # type: ignore
        assert response.errors[0].message == "Field not found"  # type: ignore

    def test_execute_http_error(self, mock_httpx_client):
        """测试 HTTP 请求错误"""
        mock_client_instance = mock_httpx_client.return_value
        mock_client_instance.post.side_effect = httpx.HTTPError("Connection error")

        client = GraphQLClient("https://api.example.com/graphql")
        query = "{ user { id } }"

        with pytest.raises(httpx.HTTPError):
            client.execute(query)

    def test_execute_batch(self, mock_httpx_client):
        """测试批量执行查询"""
        mock_response = Mock()
        mock_response.json.return_value = [
            {"data": {"user": {"id": "1", "name": "Alice"}}},
            {"data": {"user": {"id": "2", "name": "Bob"}}},
        ]
        mock_response.raise_for_status = MagicMock()

        mock_client_instance = mock_httpx_client.return_value
        mock_client_instance.post.return_value = mock_response

        client = GraphQLClient("https://api.example.com/graphql")
        operations = [
            ("{ user(id: 1) { id name } }", None),
            ("{ user(id: 2) { id name } }", None),
        ]

        responses = client.execute_batch(operations)

        assert len(responses) == 2
        assert responses[0].data == {"user": {"id": "1", "name": "Alice"}}
        assert responses[1].data == {"user": {"id": "2", "name": "Bob"}}

    def test_context_manager(self, mock_httpx_client):
        """测试上下文管理器"""
        mock_client_instance = mock_httpx_client.return_value

        with GraphQLClient("https://api.example.com/graphql") as client:
            assert client is not None

        mock_client_instance.close.assert_called_once()

    def test_close(self, mock_httpx_client):
        """测试关闭客户端"""
        mock_client_instance = mock_httpx_client.return_value

        client = GraphQLClient("https://api.example.com/graphql")
        client.close()

        mock_client_instance.close.assert_called_once()

    def test_upload_file_success(self, mock_httpx_client):
        """测试文件上传成功"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "data": {"uploadFile": {"url": "https://cdn.example.com/file.pdf"}}
        }
        mock_response.raise_for_status = MagicMock()

        mock_client_instance = mock_httpx_client.return_value
        mock_client_instance.post.return_value = mock_response

        client = GraphQLClient("https://api.example.com/graphql")
        mutation = "mutation Upload($file: Upload!) { uploadFile(file: $file) { url } }"
        variables = {"file": None}
        files = {"file": ("test.pdf", b"PDF content", "application/pdf")}

        response = client.upload_file(mutation, variables, files)

        assert response.is_success is True
        assert response.data["uploadFile"]["url"] == "https://cdn.example.com/file.pdf"
        # 验证使用了 files 参数
        call_args = mock_client_instance.post.call_args
        assert "files" in call_args[1]

    def test_upload_file_http_error(self, mock_httpx_client):
        """测试文件上传 HTTP 错误"""
        mock_client_instance = mock_httpx_client.return_value
        mock_client_instance.post.side_effect = httpx.HTTPError("Upload failed")

        client = GraphQLClient("https://api.example.com/graphql")
        mutation = "mutation Upload($file: Upload!) { uploadFile(file: $file) { url } }"

        with pytest.raises(httpx.HTTPError):
            client.upload_file(
                mutation, {"file": None}, {"file": ("test.pdf", b"data", "application/pdf")}
            )

    def test_upload_file_preserves_headers(self, mock_httpx_client):
        """测试文件上传不修改原始 headers（并发安全）"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "data": {"uploadFile": {"url": "https://cdn.example.com/file.pdf"}}
        }
        mock_response.raise_for_status = MagicMock()

        mock_client_instance = mock_httpx_client.return_value
        mock_client_instance.post.return_value = mock_response

        client = GraphQLClient("https://api.example.com/graphql")
        original_content_type = client.headers.get("Content-Type")

        client.upload_file(
            "mutation { upload }",
            {"file": None},
            {"file": ("test.txt", b"content", "text/plain")},
        )

        # 验证原始 headers 未被修改
        assert client.headers.get("Content-Type") == original_content_type

    def test_execute_batch_http_error(self, mock_httpx_client):
        """测试批量查询 HTTP 错误"""
        mock_client_instance = mock_httpx_client.return_value
        mock_client_instance.post.side_effect = httpx.HTTPError("Batch request failed")

        client = GraphQLClient("https://api.example.com/graphql")
        operations = [("{ user { id } }", None)]

        with pytest.raises(httpx.HTTPError):
            client.execute_batch(operations)

    # ========== Phase 3 新增测试：敏感信息过滤 ==========

    def test_sanitize_variables_filters_sensitive_fields(self, mock_httpx_client):
        """测试敏感变量过滤"""
        client = GraphQLClient("https://api.example.com/graphql")

        variables = {
            "username": "alice",
            "password": "secret123",
            "token": "abc-token",
            "api_key": "key-123",
            "email": "alice@example.com",
        }

        sanitized = client._sanitize_variables(variables)

        assert sanitized["username"] == "alice"
        assert sanitized["password"] == "***"
        assert sanitized["token"] == "***"
        assert sanitized["api_key"] == "***"
        assert sanitized["email"] == "alice@example.com"

    def test_sanitize_variables_handles_nested_dict(self, mock_httpx_client):
        """测试敏感变量过滤（嵌套字典）"""
        client = GraphQLClient("https://api.example.com/graphql")

        variables = {
            "user": {
                "name": "alice",
                "credentials": {
                    "password": "secret",
                    "api_key": "key-123",
                },
            }
        }

        sanitized = client._sanitize_variables(variables)

        assert sanitized["user"]["name"] == "alice"
        assert sanitized["user"]["credentials"]["password"] == "***"
        assert sanitized["user"]["credentials"]["api_key"] == "***"

    def test_sanitize_variables_handles_list(self, mock_httpx_client):
        """测试敏感变量过滤（列表）"""
        client = GraphQLClient("https://api.example.com/graphql")

        variables = {
            "tokens": ["token1", "token2"],
            "users": [{"name": "alice", "password": "secret"}],
        }

        sanitized = client._sanitize_variables(variables)

        # 列表中的普通值不过滤
        assert sanitized["tokens"] == ["token1", "token2"]
        # 列表中的字典会递归过滤
        assert sanitized["users"][0]["name"] == "alice"
        assert sanitized["users"][0]["password"] == "***"

    def test_sanitize_variables_handles_none(self, mock_httpx_client):
        """测试敏感变量过滤（空值）"""
        client = GraphQLClient("https://api.example.com/graphql")

        assert client._sanitize_variables(None) is None
        assert client._sanitize_variables({}) == {}

    # ========== Phase 3 新增测试：JSON 解析错误处理 ==========

    def test_parse_response_handles_json_error(self, mock_httpx_client):
        """测试 JSON 解析失败处理"""
        import json

        client = GraphQLClient("https://api.example.com/graphql")

        mock_response = Mock()
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_response.text = "Not a valid JSON response"

        response = client._parse_response(mock_response, "Test operation")

        assert response.is_success is False
        assert len(response.errors) == 1
        assert "Invalid JSON" in response.errors[0].message

    def test_execute_json_error(self, mock_httpx_client):
        """测试 execute 方法处理 JSON 错误"""
        import json

        mock_response = Mock()
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_response.text = "Not a valid JSON"
        mock_response.raise_for_status = MagicMock()

        mock_client_instance = mock_httpx_client.return_value
        mock_client_instance.post.return_value = mock_response

        client = GraphQLClient("https://api.example.com/graphql")
        response = client.execute("{ user { id } }")

        assert response.is_success is False
        assert len(response.errors) == 1
        assert "Invalid JSON" in response.errors[0].message

    def test_execute_batch_json_error(self, mock_httpx_client):
        """测试 execute_batch 方法处理 JSON 错误"""
        import json

        mock_response = Mock()
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_response.text = "Not a valid JSON"
        mock_response.raise_for_status = MagicMock()

        mock_client_instance = mock_httpx_client.return_value
        mock_client_instance.post.return_value = mock_response

        client = GraphQLClient("https://api.example.com/graphql")
        responses = client.execute_batch([("{ user { id } }", None)])

        assert len(responses) == 1
        assert responses[0].is_success is False
        assert "Invalid JSON" in responses[0].errors[0].message
