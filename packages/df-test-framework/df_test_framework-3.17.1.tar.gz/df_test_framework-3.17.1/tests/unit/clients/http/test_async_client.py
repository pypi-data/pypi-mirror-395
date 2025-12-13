"""测试 async_client.py - 异步HTTP客户端

测试覆盖:
- 异步HTTP方法(GET/POST/PUT/DELETE/PATCH)
- 上下文管理器
- 并发请求
- 拦截器集成
- 错误处理
- 性能基准测试
"""

import asyncio
from unittest.mock import AsyncMock, Mock, patch

import httpx
import pytest

from df_test_framework.capabilities.clients.http.core import Request, Response
from df_test_framework.capabilities.clients.http.rest.httpx import AsyncHttpClient


class TestAsyncHttpClientBasic:
    """测试异步HTTP客户端基础功能"""

    @pytest.fixture
    def client(self):
        """测试客户端fixture"""
        return AsyncHttpClient(
            base_url="https://api.test.com",
            timeout=30,
            http2=True,
        )

    @pytest.mark.asyncio
    async def test_client_initialization(self, client):
        """测试客户端初始化"""
        assert client.base_url == "https://api.test.com"
        assert client.timeout == 30
        assert client.http2 is True
        assert isinstance(client.client, httpx.AsyncClient)

        await client.close()

    @pytest.mark.asyncio
    async def test_context_manager(self):
        """测试上下文管理器"""
        async with AsyncHttpClient("https://api.test.com") as client:
            assert isinstance(client, AsyncHttpClient)
            assert isinstance(client.client, httpx.AsyncClient)

        # 验证客户端已关闭（无法直接验证，但不应抛异常）

    @pytest.mark.asyncio
    async def test_set_auth_token(self, client):
        """测试设置认证token"""
        client.set_auth_token("test_token_123", "Bearer")

        assert client.client.headers["Authorization"] == "Bearer test_token_123"

        await client.close()


class TestAsyncHttpClientMethods:
    """测试异步HTTP方法"""

    @pytest.fixture
    def mock_response(self):
        """模拟HTTP响应"""
        response = Mock(spec=httpx.Response)
        response.status_code = 200
        response.headers = {"Content-Type": "application/json"}
        response.text = '{"message": "success"}'
        response.json.return_value = {"message": "success"}
        return response

    @pytest.mark.asyncio
    async def test_get_request(self, mock_response):
        """测试GET请求"""
        async with AsyncHttpClient("https://api.test.com") as client:
            with patch.object(client.client, "request", new_callable=AsyncMock) as mock_request:
                mock_request.return_value = mock_response

                response = await client.get("/users")

                assert response.status_code == 200
                assert response.json_data == {"message": "success"}
                mock_request.assert_called_once()

    @pytest.mark.asyncio
    async def test_post_request(self, mock_response):
        """测试POST请求"""
        async with AsyncHttpClient("https://api.test.com") as client:
            with patch.object(client.client, "request", new_callable=AsyncMock) as mock_request:
                mock_request.return_value = mock_response

                response = await client.post("/users", json={"name": "Alice"})

                assert response.status_code == 200
                mock_request.assert_called_once()

    @pytest.mark.asyncio
    async def test_put_request(self, mock_response):
        """测试PUT请求"""
        async with AsyncHttpClient("https://api.test.com") as client:
            with patch.object(client.client, "request", new_callable=AsyncMock) as mock_request:
                mock_request.return_value = mock_response

                response = await client.put("/users/1", json={"name": "Bob"})

                assert response.status_code == 200
                mock_request.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_request(self, mock_response):
        """测试DELETE请求"""
        async with AsyncHttpClient("https://api.test.com") as client:
            with patch.object(client.client, "request", new_callable=AsyncMock) as mock_request:
                mock_request.return_value = mock_response

                response = await client.delete("/users/1")

                assert response.status_code == 200
                mock_request.assert_called_once()

    @pytest.mark.asyncio
    async def test_patch_request(self, mock_response):
        """测试PATCH请求"""
        async with AsyncHttpClient("https://api.test.com") as client:
            with patch.object(client.client, "request", new_callable=AsyncMock) as mock_request:
                mock_request.return_value = mock_response

                response = await client.patch("/users/1", json={"age": 30})

                assert response.status_code == 200
                mock_request.assert_called_once()


class TestAsyncHttpClientConcurrency:
    """测试并发请求"""

    @pytest.fixture
    def mock_response(self):
        """模拟HTTP响应"""
        response = Mock(spec=httpx.Response)
        response.status_code = 200
        response.headers = {"Content-Type": "application/json"}
        response.text = '{"id": 1}'
        response.json.return_value = {"id": 1}
        return response

    @pytest.mark.asyncio
    async def test_concurrent_get_requests(self, mock_response):
        """测试并发GET请求"""
        async with AsyncHttpClient("https://api.test.com") as client:
            with patch.object(client.client, "request", new_callable=AsyncMock) as mock_request:
                mock_request.return_value = mock_response

                # 并发10个请求
                tasks = [client.get(f"/users/{i}") for i in range(10)]
                responses = await asyncio.gather(*tasks)

                assert len(responses) == 10
                for response in responses:
                    assert response.status_code == 200
                    assert response.json_data == {"id": 1}

                # 验证调用次数
                assert mock_request.call_count == 10

    @pytest.mark.asyncio
    async def test_concurrent_mixed_requests(self, mock_response):
        """测试并发混合请求"""
        async with AsyncHttpClient("https://api.test.com") as client:
            with patch.object(client.client, "request", new_callable=AsyncMock) as mock_request:
                mock_request.return_value = mock_response

                # 混合GET/POST/PUT/DELETE
                tasks = [
                    client.get("/users/1"),
                    client.post("/users", json={"name": "Alice"}),
                    client.put("/users/1", json={"name": "Bob"}),
                    client.delete("/users/1"),
                ]

                responses = await asyncio.gather(*tasks)

                assert len(responses) == 4
                for response in responses:
                    assert response.status_code == 200


class TestAsyncHttpClientErrorHandling:
    """测试错误处理"""

    @pytest.mark.asyncio
    async def test_http_error(self):
        """测试HTTP错误"""
        async with AsyncHttpClient("https://api.test.com") as client:
            with patch.object(client.client, "request", new_callable=AsyncMock) as mock_request:
                mock_request.side_effect = httpx.HTTPError("Network error")

                with pytest.raises(httpx.HTTPError, match="Network error"):
                    await client.get("/users")

    @pytest.mark.asyncio
    async def test_timeout_error(self):
        """测试超时错误"""
        async with AsyncHttpClient("https://api.test.com", timeout=1) as client:
            with patch.object(client.client, "request", new_callable=AsyncMock) as mock_request:
                mock_request.side_effect = httpx.TimeoutException("Request timeout")

                with pytest.raises(httpx.TimeoutException):
                    await client.get("/slow-endpoint")


class TestAsyncHttpClientConfig:
    """测试配置优先级 (v3.9.0+)"""

    @pytest.mark.asyncio
    async def test_explicit_params_override_config(self):
        """测试显式参数覆盖HTTPConfig配置

        v3.9.0 修复: 配置优先级为 显式参数 > HTTPConfig > 默认值
        """
        from df_test_framework.infrastructure.config.schema import HTTPConfig

        # HTTPConfig 提供默认配置
        config = HTTPConfig(
            base_url="https://config.example.com",
            timeout=30,
            verify_ssl=True,
            max_connections=100,
        )

        # 显式参数覆盖部分配置
        client = AsyncHttpClient(
            base_url="https://explicit.example.com",  # 应该覆盖config
            timeout=60,  # 应该覆盖config
            # verify_ssl 未指定，应该使用config的值
            # max_connections 未指定，应该使用config的值
            config=config,
        )

        try:
            # 验证显式参数优先
            assert client.base_url == "https://explicit.example.com"
            assert client.timeout == 60

            # 验证未指定的参数使用HTTPConfig的值
            assert client.verify_ssl is True

            # 验证httpx客户端配置正确
            assert client.client.timeout.connect == 60
        finally:
            await client.close()

    @pytest.mark.asyncio
    async def test_config_provides_defaults(self):
        """测试HTTPConfig提供默认值"""
        from df_test_framework.infrastructure.config.schema import HTTPConfig

        config = HTTPConfig(
            base_url="https://config.example.com",
            timeout=45,
            verify_ssl=False,
            max_connections=200,
            max_keepalive_connections=50,
        )

        # 只提供config，不提供显式参数
        client = AsyncHttpClient(config=config)

        try:
            # 所有配置都应该来自HTTPConfig
            assert client.base_url == "https://config.example.com"
            assert client.timeout == 45
            assert client.verify_ssl is False
        finally:
            await client.close()

    @pytest.mark.asyncio
    async def test_default_values_without_config(self):
        """测试无HTTPConfig时使用默认值"""
        # 只提供base_url，其他使用默认值
        client = AsyncHttpClient(base_url="https://test.example.com")

        try:
            assert client.base_url == "https://test.example.com"
            assert client.timeout == 30  # 默认值
            assert client.verify_ssl is True  # 默认值
            assert client.http2 is True  # 默认值
        finally:
            await client.close()


class TestAsyncHttpClientHelperMethods:
    """测试辅助方法"""

    @pytest.mark.asyncio
    async def test_prepare_request_object(self):
        """测试准备Request对象"""
        async with AsyncHttpClient("https://api.test.com") as client:
            request = client._prepare_request_object(
                method="POST",
                url="/users",
                headers={"X-Token": "abc"},
                params={"page": 1},
                json={"name": "Alice"},
            )

            assert isinstance(request, Request)
            assert request.method == "POST"
            assert request.url == "/users"
            assert request.headers == {"X-Token": "abc"}
            assert request.params == {"page": 1}
            assert request.json == {"name": "Alice"}

    @pytest.mark.asyncio
    async def test_parse_response(self):
        """测试解析HTTP响应"""
        async with AsyncHttpClient("https://api.test.com") as client:
            httpx_response = Mock(spec=httpx.Response)
            httpx_response.status_code = 201
            httpx_response.headers = {"Content-Type": "application/json"}
            httpx_response.text = '{"id": 123}'
            httpx_response.json.return_value = {"id": 123}

            response = client._parse_response(httpx_response)

            assert isinstance(response, Response)
            assert response.status_code == 201
            assert response.json_data == {"id": 123}


__all__ = [
    "TestAsyncHttpClientBasic",
    "TestAsyncHttpClientMethods",
    "TestAsyncHttpClientConcurrency",
    "TestAsyncHttpClientErrorHandling",
    "TestAsyncHttpClientConfig",
    "TestAsyncHttpClientHelperMethods",
]
