"""测试 LoggingMiddleware - 日志中间件

测试覆盖:
- 初始化配置
- 请求日志记录
- 响应日志记录
- 错误日志记录
- 各种配置选项

v3.16.0: 迁移到 Middleware 系统
"""

import logging
from unittest.mock import AsyncMock, Mock

import pytest

from df_test_framework.capabilities.clients.http.core.request import Request
from df_test_framework.capabilities.clients.http.core.response import Response
from df_test_framework.capabilities.clients.http.middleware.logging import LoggingMiddleware


class TestLoggingMiddlewareInit:
    """测试 LoggingMiddleware 初始化"""

    def test_init_with_defaults(self):
        """测试使用默认参数初始化"""
        middleware = LoggingMiddleware()
        assert middleware.name == "LoggingMiddleware"
        assert middleware.priority == 100
        assert middleware.log_request is True
        assert middleware.log_response is True
        assert middleware.log_headers is False
        assert middleware.log_body is True
        assert middleware.max_body_length == 1000

    def test_init_with_custom_logger(self):
        """测试自定义 logger"""
        custom_logger = logging.getLogger("custom")
        middleware = LoggingMiddleware(logger=custom_logger)
        assert middleware._logger is custom_logger

    def test_init_with_custom_level(self):
        """测试自定义日志级别"""
        middleware = LoggingMiddleware(level="INFO")
        assert middleware._level == logging.INFO

    def test_init_with_custom_priority(self):
        """测试自定义优先级"""
        middleware = LoggingMiddleware(priority=200)
        assert middleware.priority == 200

    def test_init_without_request_logging(self):
        """测试禁用请求日志"""
        middleware = LoggingMiddleware(log_request=False)
        assert middleware.log_request is False

    def test_init_without_response_logging(self):
        """测试禁用响应日志"""
        middleware = LoggingMiddleware(log_response=False)
        assert middleware.log_response is False

    def test_init_with_custom_max_body_length(self):
        """测试自定义最大体长度"""
        middleware = LoggingMiddleware(max_body_length=500)
        assert middleware.max_body_length == 500


class TestLoggingMiddlewareRequestLogging:
    """测试 LoggingMiddleware 请求日志"""

    @pytest.fixture
    def middleware(self):
        """默认中间件实例"""
        return LoggingMiddleware()

    @pytest.fixture
    def mock_request(self):
        """Mock 请求对象"""
        request = Mock(spec=Request)
        request.method = "GET"
        request.path = "/api/users"
        request.url = "https://api.example.com/api/users"
        request.headers = {"Content-Type": "application/json"}
        request.params = {"page": 1}
        request.json = None
        return request

    def test_log_request_basic(self, middleware, mock_request, caplog):
        """测试基本请求日志"""
        with caplog.at_level(logging.DEBUG):
            middleware._log_request(mock_request)

        # 验证日志包含方法和路径
        assert "GET" in caplog.text
        assert "/api/users" in caplog.text

    def test_log_request_with_json_body(self, middleware, mock_request, caplog):
        """测试带 JSON 体的请求日志"""
        mock_request.json = {"name": "Alice", "age": 25}

        with caplog.at_level(logging.DEBUG):
            middleware._log_request(mock_request)

        # 验证日志包含 body
        assert "Alice" in caplog.text

    def test_log_request_without_body_logging(self, mock_request, caplog):
        """测试禁用 body 日志"""
        middleware = LoggingMiddleware(log_body=False)
        mock_request.json = {"name": "Alice"}

        with caplog.at_level(logging.DEBUG):
            middleware._log_request(mock_request)

        # 验证不记录 body
        assert "Alice" not in caplog.text

    def test_log_request_with_long_body(self, mock_request, caplog):
        """测试超长 body 被截断"""
        middleware = LoggingMiddleware(max_body_length=50)
        mock_request.json = {"data": "x" * 100}

        with caplog.at_level(logging.DEBUG):
            middleware._log_request(mock_request)

        # 验证有截断标记
        assert "..." in caplog.text


class TestLoggingMiddlewareResponseLogging:
    """测试 LoggingMiddleware 响应日志"""

    @pytest.fixture
    def middleware(self):
        """默认中间件实例"""
        return LoggingMiddleware()

    @pytest.fixture
    def mock_request(self):
        """Mock 请求对象"""
        request = Mock(spec=Request)
        request.method = "GET"
        request.path = "/api/users"
        return request

    @pytest.fixture
    def mock_response(self):
        """Mock 响应对象"""
        response = Mock(spec=Response)
        response.status_code = 200
        response.is_success = True
        response.headers = {"Content-Type": "application/json"}
        response.text = '{"success": true}'
        return response

    def test_log_response_success(self, middleware, mock_request, mock_response, caplog):
        """测试成功响应日志"""
        with caplog.at_level(logging.DEBUG):
            middleware._log_response(mock_request, mock_response, 0.123)

        # 验证日志包含状态码
        assert "200" in caplog.text
        assert "0.123" in caplog.text

    def test_log_response_with_body(self, middleware, mock_request, mock_response, caplog):
        """测试响应体日志"""
        with caplog.at_level(logging.DEBUG):
            middleware._log_response(mock_request, mock_response, 0.1)

        # 验证日志包含 body
        assert "success" in caplog.text

    def test_log_response_error_status(self, middleware, mock_request, mock_response, caplog):
        """测试错误响应日志"""
        mock_response.status_code = 500
        mock_response.is_success = False

        with caplog.at_level(logging.DEBUG):
            middleware._log_response(mock_request, mock_response, 0.1)

        assert "500" in caplog.text


class TestLoggingMiddlewareErrorLogging:
    """测试 LoggingMiddleware 错误日志"""

    @pytest.fixture
    def middleware(self):
        """默认中间件实例"""
        return LoggingMiddleware()

    @pytest.fixture
    def mock_request(self):
        """Mock 请求对象"""
        request = Mock(spec=Request)
        request.method = "POST"
        request.path = "/api/users"
        return request

    def test_log_error(self, middleware, mock_request, caplog):
        """测试错误日志"""
        error = Exception("Connection timeout")

        with caplog.at_level(logging.ERROR):
            middleware._log_error(mock_request, error, 5.0)

        assert "ERROR" in caplog.text
        assert "Connection timeout" in caplog.text
        assert "5.0" in caplog.text


class TestLoggingMiddlewareIntegration:
    """测试 LoggingMiddleware 集成"""

    @pytest.fixture
    def middleware(self):
        """默认中间件实例"""
        return LoggingMiddleware()

    @pytest.fixture
    def mock_request(self):
        """Mock 请求对象"""
        request = Mock(spec=Request)
        request.method = "GET"
        request.path = "/api/users"
        request.headers = {}
        request.json = None
        return request

    @pytest.fixture
    def mock_response(self):
        """Mock 响应对象"""
        response = Mock(spec=Response)
        response.status_code = 200
        response.is_success = True
        response.headers = {}
        response.text = "{}"
        return response

    @pytest.mark.asyncio
    async def test_middleware_call(self, middleware, mock_request, mock_response, caplog):
        """测试中间件完整调用流程"""
        call_next = AsyncMock(return_value=mock_response)

        with caplog.at_level(logging.DEBUG):
            result = await middleware(mock_request, call_next)

        # 验证调用了 call_next
        call_next.assert_called_once_with(mock_request)

        # 验证返回响应
        assert result is mock_response

        # 验证记录了请求和响应
        assert "GET" in caplog.text
        assert "200" in caplog.text

    @pytest.mark.asyncio
    async def test_middleware_with_error(self, middleware, mock_request, caplog):
        """测试中间件处理异常"""
        call_next = AsyncMock(side_effect=Exception("Network error"))

        with caplog.at_level(logging.ERROR):
            with pytest.raises(Exception, match="Network error"):
                await middleware(mock_request, call_next)

        # 验证记录了错误
        assert "ERROR" in caplog.text
        assert "Network error" in caplog.text


__all__ = [
    "TestLoggingMiddlewareInit",
    "TestLoggingMiddlewareRequestLogging",
    "TestLoggingMiddlewareResponseLogging",
    "TestLoggingMiddlewareErrorLogging",
    "TestLoggingMiddlewareIntegration",
]
