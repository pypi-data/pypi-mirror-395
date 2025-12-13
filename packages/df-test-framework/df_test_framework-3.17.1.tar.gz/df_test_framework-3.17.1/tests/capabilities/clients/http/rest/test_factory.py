"""测试RestClientFactory

验证Factory类正确创建HttpClient实例，修复HTTPConfig参数传递bug
"""

import pytest

from df_test_framework.capabilities.clients.http.rest.factory import RestClientFactory
from df_test_framework.capabilities.clients.http.rest.httpx.client import HttpClient
from df_test_framework.infrastructure.config.schema import HTTPConfig


class TestRestClientFactory:
    """测试RestClientFactory"""

    def test_create_with_default_config(self):
        """测试使用默认配置创建客户端"""
        client = RestClientFactory.create()

        assert isinstance(client, HttpClient)
        # ✅ Bug修复验证: 确保base_url正确设置（默认值）
        assert client.base_url == "http://localhost:8000"
        assert client.timeout == 30
        assert client.verify_ssl is True
        assert client.max_retries == 3

    def test_create_with_http_config(self):
        """测试使用HTTPConfig创建客户端"""
        config = HTTPConfig(
            base_url="https://api.example.com",
            timeout=60,
            verify_ssl=False,
            max_retries=5,
            max_connections=100,
            max_keepalive_connections=50,
        )

        client = RestClientFactory.create(config=config)

        assert isinstance(client, HttpClient)
        # ✅ Bug修复验证: 确保所有参数正确传递
        assert client.base_url == "https://api.example.com"
        assert client.timeout == 60
        assert client.verify_ssl is False
        assert client.max_retries == 5

    def test_create_with_http_config_none_base_url(self):
        """测试HTTPConfig的base_url为None时使用默认值"""
        config = HTTPConfig(
            base_url=None,  # base_url可以为None
            timeout=45,
        )

        client = RestClientFactory.create(config=config)

        assert isinstance(client, HttpClient)
        # ✅ Bug修复验证: 当base_url为None时，使用默认值
        assert client.base_url == "http://localhost"
        assert client.timeout == 45

    def test_create_httpx_with_default_config(self):
        """测试create_httpx便捷方法（默认配置）"""
        client = RestClientFactory.create_httpx()

        assert isinstance(client, HttpClient)
        assert client.base_url == "http://localhost:8000"
        assert client.timeout == 30

    def test_create_httpx_with_http_config(self):
        """测试create_httpx便捷方法（自定义配置）"""
        config = HTTPConfig(
            base_url="https://test.example.com",
            timeout=90,
        )

        client = RestClientFactory.create_httpx(config=config)

        assert isinstance(client, HttpClient)
        assert client.base_url == "https://test.example.com"
        assert client.timeout == 90

    def test_create_requests_not_implemented(self):
        """测试requests客户端未实现"""
        with pytest.raises(NotImplementedError, match="requests客户端尚未实现"):
            RestClientFactory.create(client_type="requests")

    def test_create_requests_method_not_implemented(self):
        """测试create_requests方法未实现"""
        with pytest.raises(NotImplementedError, match="requests客户端尚未实现"):
            RestClientFactory.create_requests()

    def test_create_with_invalid_client_type(self):
        """测试使用无效的客户端类型"""
        with pytest.raises(ValueError, match="不支持的客户端类型"):
            RestClientFactory.create(client_type="invalid")

    def test_create_with_middlewares(self):
        """测试HTTPConfig包含中间件时正确传递

        v3.16.0: 从 interceptors 迁移到 middlewares
        """
        from df_test_framework.infrastructure.config.middleware_schema import (
            SignatureMiddlewareConfig,
        )

        config = HTTPConfig(
            base_url="https://api.example.com",
            middlewares=[
                SignatureMiddlewareConfig(
                    type="signature",
                    algorithm="md5",
                    secret="test_secret",
                    header_name="X-Sign",
                )
            ],
        )

        client = RestClientFactory.create(config=config)

        assert isinstance(client, HttpClient)
        # ✅ Bug修复验证: 确保config正确传递，中间件会被加载
        assert client.base_url == "https://api.example.com"
        # 验证 HttpClient 创建成功（中间件通过配置加载）
        assert client is not None
