"""
测试HttpClient

验证HTTP客户端的请求方法、重试机制和上下文管理。
"""

from unittest.mock import Mock, patch

import httpx
import pytest

from df_test_framework.capabilities.clients.http.rest.httpx.client import HttpClient, sanitize_url


class TestSanitizeUrl:
    """测试URL脱敏功能"""

    def test_sanitize_token_param(self):
        """测试脱敏token参数"""
        url = "/api/users?token=abc123&id=1"
        result = sanitize_url(url)

        assert result == "/api/users?token=****&id=1"
        assert "abc123" not in result

    def test_sanitize_api_key_param(self):
        """测试脱敏api_key参数"""
        url = "/api/pay?amount=100&api_key=xyz789"
        result = sanitize_url(url)

        assert result == "/api/pay?amount=100&api_key=****"
        assert "xyz789" not in result

    def test_sanitize_password_param(self):
        """测试脱敏password参数"""
        url = "/api/login?username=admin&password=secret123"
        result = sanitize_url(url)

        assert result == "/api/login?username=admin&password=****"
        assert "secret123" not in result

    def test_sanitize_multiple_sensitive_params(self):
        """测试脱敏多个敏感参数"""
        url = "/api/auth?token=abc&password=pwd123&id=1"
        result = sanitize_url(url)

        assert result == "/api/auth?token=****&password=****&id=1"
        assert "abc" not in result
        assert "pwd123" not in result

    def test_sanitize_no_sensitive_params(self):
        """测试无敏感参数的URL不变"""
        url = "/api/users?id=1&name=test"
        result = sanitize_url(url)

        assert result == url


class TestHttpClientInit:
    """测试HttpClient初始化"""

    def test_client_creation(self):
        """测试创建HttpClient"""
        client = HttpClient(base_url="https://api.example.com")

        assert client.base_url == "https://api.example.com"
        assert client.timeout == 30
        assert client.max_retries == 3
        assert client.verify_ssl is True
        assert client.client is not None

        client.close()

    def test_client_with_custom_settings(self):
        """测试使用自定义配置创建"""
        headers = {"X-Custom": "value"}
        client = HttpClient(
            base_url="https://api.example.com",
            timeout=60,
            headers=headers,
            verify_ssl=False,
            max_retries=5,
        )

        assert client.timeout == 60
        assert client.max_retries == 5
        assert client.verify_ssl is False
        assert "X-Custom" in client.default_headers

        client.close()


class TestHttpClientAuthToken:
    """测试认证token设置"""

    def test_set_auth_token_bearer(self):
        """测试设置Bearer Token"""
        client = HttpClient(base_url="https://api.example.com")

        client.set_auth_token("test_token_123")

        assert client.client.headers["Authorization"] == "Bearer test_token_123"

        client.close()

    def test_set_auth_token_basic(self):
        """测试设置Basic Token"""
        client = HttpClient(base_url="https://api.example.com")

        client.set_auth_token("base64_credentials", token_type="Basic")

        assert client.client.headers["Authorization"] == "Basic base64_credentials"

        client.close()


class TestHttpClientRequest:
    """测试request方法"""

    def test_request_success(self):
        """测试成功的请求"""
        client = HttpClient(base_url="https://api.example.com")

        # Mock httpx.Client.request
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.text = '{"result": "ok"}'
        mock_response.headers = {"content-type": "application/json"}  # v3.5: 添加headers

        with patch.object(client.client, "request", return_value=mock_response):
            response = client.request("GET", "/users")

            assert response.status_code == 200

        client.close()

    def test_request_with_params(self):
        """测试带参数的请求"""
        client = HttpClient(base_url="https://api.example.com")

        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.text = '{"result": "ok"}'
        mock_response.headers = {"content-type": "application/json"}  # v3.5: 添加headers

        with patch.object(client.client, "request", return_value=mock_response) as mock_req:
            client.request("GET", "/users", params={"id": 1})

            # 验证params被传递
            mock_req.assert_called_once()
            call_kwargs = mock_req.call_args[1]
            assert call_kwargs.get("params") == {"id": 1}

        client.close()


class TestHttpClientRetry:
    """测试重试机制"""

    @patch("time.sleep")  # Mock sleep避免实际等待
    def test_retry_on_timeout(self, mock_sleep):
        """测试超时重试"""
        client = HttpClient(base_url="https://api.example.com", max_retries=2)

        # 前2次超时，第3次成功
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.text = '{"result": "ok"}'
        mock_response.headers = {"content-type": "application/json"}  # v3.5: 添加headers

        attempts = [
            httpx.TimeoutException("Timeout"),
            httpx.TimeoutException("Timeout"),
            mock_response,
        ]

        with patch.object(client.client, "request", side_effect=attempts):
            response = client.request("GET", "/users")

            assert response.status_code == 200
            # 应该调用了2次sleep（重试2次）
            assert mock_sleep.call_count == 2

        client.close()

    @patch("time.sleep")
    def test_retry_on_5xx_error(self, mock_sleep):
        """测试5xx错误重试"""
        client = HttpClient(base_url="https://api.example.com", max_retries=2)

        # 前2次返回500，第3次成功
        error_response = Mock(spec=httpx.Response)
        error_response.status_code = 500
        error_response.text = "Internal Server Error"
        error_response.headers = {}  # v3.5: 添加headers

        success_response = Mock(spec=httpx.Response)
        success_response.status_code = 200
        success_response.text = '{"result": "ok"}'
        success_response.headers = {"content-type": "application/json"}  # v3.5: 添加headers

        with patch.object(
            client.client, "request", side_effect=[error_response, error_response, success_response]
        ):
            response = client.request("GET", "/users")

            assert response.status_code == 200
            # 应该调用了2次sleep
            assert mock_sleep.call_count == 2

        client.close()

    def test_no_retry_on_4xx_error(self):
        """测试4xx错误不重试"""
        client = HttpClient(base_url="https://api.example.com", max_retries=3)

        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_response.headers = {}  # v3.5: 添加headers

        with patch.object(client.client, "request", return_value=mock_response):
            response = client.request("GET", "/users/999")

            # 不应该重试，直接返回404
            assert response.status_code == 404

        client.close()

    @patch("time.sleep")
    def test_max_retries_exceeded(self, mock_sleep):
        """测试超过最大重试次数"""
        client = HttpClient(base_url="https://api.example.com", max_retries=2)

        # 所有尝试都超时
        with patch.object(client.client, "request", side_effect=httpx.TimeoutException("Timeout")):
            with pytest.raises(httpx.TimeoutException):
                client.request("GET", "/users")

            # 应该调用了2次sleep（max_retries=2）
            assert mock_sleep.call_count == 2

        client.close()


class TestHttpClientConvenienceMethods:
    """测试便捷方法（GET、POST等）"""

    def setup_method(self):
        """每个测试前创建client"""
        self.client = HttpClient(base_url="https://api.example.com")

    def teardown_method(self):
        """每个测试后关闭client"""
        self.client.close()

    def test_get_method(self):
        """测试GET方法"""
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 200

        with patch.object(self.client, "request", return_value=mock_response) as mock_req:
            response = self.client.get("/users", params={"id": 1})

            mock_req.assert_called_once_with("GET", "/users", params={"id": 1})
            assert response.status_code == 200

    def test_post_method(self):
        """测试POST方法"""
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 201

        with patch.object(self.client, "request", return_value=mock_response) as mock_req:
            response = self.client.post("/users", json={"name": "Alice"})

            mock_req.assert_called_once_with("POST", "/users", json={"name": "Alice"}, data=None)
            assert response.status_code == 201

    def test_put_method(self):
        """测试PUT方法"""
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 200

        with patch.object(self.client, "request", return_value=mock_response) as mock_req:
            response = self.client.put("/users/1", json={"name": "Alice Updated"})

            mock_req.assert_called_once_with("PUT", "/users/1", json={"name": "Alice Updated"})
            assert response.status_code == 200

    def test_patch_method(self):
        """测试PATCH方法"""
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 200

        with patch.object(self.client, "request", return_value=mock_response) as mock_req:
            response = self.client.patch("/users/1", json={"age": 26})

            mock_req.assert_called_once_with("PATCH", "/users/1", json={"age": 26})
            assert response.status_code == 200

    def test_delete_method(self):
        """测试DELETE方法"""
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 204

        with patch.object(self.client, "request", return_value=mock_response) as mock_req:
            response = self.client.delete("/users/1")

            mock_req.assert_called_once_with("DELETE", "/users/1")
            assert response.status_code == 204


class TestHttpClientContextManager:
    """测试上下文管理器"""

    def test_context_manager_closes_client(self):
        """测试上下文管理器自动关闭客户端"""
        with HttpClient(base_url="https://api.example.com") as client:
            assert client.client is not None

        # 退出上下文后，client应该被关闭
        # 注意：httpx.Client关闭后仍可访问，但不应再使用

    def test_context_manager_usage(self):
        """测试在上下文管理器中使用"""
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.text = '{"result": "ok"}'
        mock_response.headers = {"content-type": "application/json"}  # v3.5: 添加headers

        with HttpClient(base_url="https://api.example.com") as client:
            with patch.object(client.client, "request", return_value=mock_response):
                response = client.get("/users")
                assert response.status_code == 200


class TestHttpClientPydanticSerialization:
    """测试 Pydantic 模型自动序列化（v3.6新增）"""

    def setup_method(self):
        """每个测试前创建client"""
        self.client = HttpClient(base_url="https://api.example.com")

    def teardown_method(self):
        """每个测试后关闭client"""
        self.client.close()

    def test_post_with_pydantic_model_basic(self):
        """测试使用 Pydantic 模型发送 POST 请求"""
        from pydantic import BaseModel

        class UserRequest(BaseModel):
            name: str
            age: int

        request_model = UserRequest(name="Alice", age=25)

        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 201
        mock_response.text = '{"id":1}'
        mock_response.headers = {"content-type": "application/json"}

        with patch.object(self.client.client, "request", return_value=mock_response) as mock_req:
            response = self.client.post("/users", json=request_model)

            assert response.status_code == 201
            # 验证请求参数
            call_kwargs = mock_req.call_args[1]
            assert call_kwargs["data"] == '{"name":"Alice","age":25}'
            assert call_kwargs["headers"]["Content-Type"] == "application/json"

    def test_post_with_decimal_field(self):
        """测试 Decimal 字段自动序列化为字符串"""
        from decimal import Decimal

        from pydantic import BaseModel

        class PaymentRequest(BaseModel):
            amount: Decimal
            currency: str

        request_model = PaymentRequest(amount=Decimal("123.45"), currency="CNY")

        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.text = '{"success":true}'
        mock_response.headers = {"content-type": "application/json"}

        with patch.object(self.client.client, "request", return_value=mock_response) as mock_req:
            response = self.client.post("/payment", json=request_model)

            assert response.status_code == 200
            # 验证 Decimal 被序列化为字符串
            call_kwargs = mock_req.call_args[1]
            assert call_kwargs["data"] == '{"amount":"123.45","currency":"CNY"}'

    def test_post_with_decimal_as_float(self):
        """测试 DecimalAsFloat 序列化为浮点数"""
        from decimal import Decimal

        from pydantic import BaseModel

        from df_test_framework import DecimalAsFloat

        class LegacyRequest(BaseModel):
            price: DecimalAsFloat

        request_model = LegacyRequest(price=Decimal("99.99"))

        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.text = '{"success":true}'
        mock_response.headers = {"content-type": "application/json"}

        with patch.object(self.client.client, "request", return_value=mock_response) as mock_req:
            response = self.client.post("/legacy", json=request_model)

            assert response.status_code == 200
            # 验证 DecimalAsFloat 被序列化为浮点数
            call_kwargs = mock_req.call_args[1]
            assert call_kwargs["data"] == '{"price":99.99}'

    def test_post_with_decimal_as_currency(self):
        """测试 DecimalAsCurrency 序列化为货币格式"""
        from decimal import Decimal

        from pydantic import BaseModel

        from df_test_framework import DecimalAsCurrency

        class DisplayRequest(BaseModel):
            total: DecimalAsCurrency

        request_model = DisplayRequest(total=Decimal("123.45"))

        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.text = '{"success":true}'
        mock_response.headers = {"content-type": "application/json"}

        with patch.object(self.client.client, "request", return_value=mock_response) as mock_req:
            response = self.client.post("/display", json=request_model)

            assert response.status_code == 200
            # 验证 DecimalAsCurrency 被序列化为货币格式
            call_kwargs = mock_req.call_args[1]
            assert call_kwargs["data"] == '{"total":"$123.45"}'

    def test_put_with_pydantic_model(self):
        """测试 PUT 请求支持 Pydantic 模型"""
        from pydantic import BaseModel

        class UpdateRequest(BaseModel):
            name: str

        request_model = UpdateRequest(name="Bob")

        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.text = '{"success":true}'
        mock_response.headers = {"content-type": "application/json"}

        with patch.object(self.client.client, "request", return_value=mock_response) as mock_req:
            response = self.client.put("/users/1", json=request_model)

            assert response.status_code == 200
            call_kwargs = mock_req.call_args[1]
            assert call_kwargs["data"] == '{"name":"Bob"}'

    def test_patch_with_pydantic_model(self):
        """测试 PATCH 请求支持 Pydantic 模型"""
        from pydantic import BaseModel

        class PatchRequest(BaseModel):
            age: int

        request_model = PatchRequest(age=30)

        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.text = '{"success":true}'
        mock_response.headers = {"content-type": "application/json"}

        with patch.object(self.client.client, "request", return_value=mock_response) as mock_req:
            response = self.client.patch("/users/1", json=request_model)

            assert response.status_code == 200
            call_kwargs = mock_req.call_args[1]
            assert call_kwargs["data"] == '{"age":30}'

    def test_post_with_dict_still_works(self):
        """测试使用字典仍然正常工作（向后兼容）"""
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.text = '{"success":true}'
        mock_response.headers = {"content-type": "application/json"}

        with patch.object(self.client.client, "request", return_value=mock_response) as mock_req:
            response = self.client.post("/users", json={"name": "Charlie", "age": 35})

            assert response.status_code == 200
            # 验证字典仍然通过 json 参数传递
            call_kwargs = mock_req.call_args[1]
            assert call_kwargs["json"] == {"name": "Charlie", "age": 35}
