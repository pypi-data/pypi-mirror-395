"""HTTPDebugger 单元测试"""

import pytest

from df_test_framework.testing.debugging import (
    HTTPDebugger,
    disable_http_debug,
    enable_http_debug,
    get_global_debugger,
)


class TestHTTPDebugger:
    """HTTPDebugger 基本功能测试"""

    def test_init_default(self):
        """测试默认初始化"""
        debugger = HTTPDebugger()
        assert debugger.enabled is True
        assert debugger.max_body_length == 1000
        assert debugger.requests == []

    def test_init_custom(self):
        """测试自定义初始化"""
        debugger = HTTPDebugger(enabled=False, max_body_length=500)
        assert debugger.enabled is False
        assert debugger.max_body_length == 500

    def test_start_stop(self):
        """测试启动和停止"""
        debugger = HTTPDebugger(enabled=False)
        assert debugger.enabled is False

        debugger.start()
        assert debugger.enabled is True

        debugger.stop()
        assert debugger.enabled is False

    def test_clear(self):
        """测试清空记录"""
        debugger = HTTPDebugger()
        debugger.log_request("GET", "http://example.com")
        debugger.log_response(200, body={"ok": True})

        assert len(debugger.requests) == 1

        debugger.clear()
        assert len(debugger.requests) == 0
        assert debugger.current_request is None


class TestHTTPDebuggerLogging:
    """HTTPDebugger 日志记录测试"""

    def test_log_request_basic(self, capsys):
        """测试基本请求日志"""
        debugger = HTTPDebugger()
        debugger.log_request("GET", "http://example.com/api/users")

        captured = capsys.readouterr()
        assert "[HTTP DEBUG] GET http://example.com/api/users" in captured.out

    def test_log_request_with_params(self, capsys):
        """测试带参数的请求日志"""
        debugger = HTTPDebugger()
        debugger.log_request(
            "GET",
            "http://example.com/api/users",
            params={"page": 1, "size": 10},
        )

        captured = capsys.readouterr()
        assert "[HTTP DEBUG] Params:" in captured.out
        assert "page" in captured.out

    def test_log_request_with_headers(self, capsys):
        """测试带请求头的日志（敏感信息脱敏）"""
        debugger = HTTPDebugger()
        long_token = "Bearer " + "x" * 50
        debugger.log_request(
            "POST",
            "http://example.com/api",
            headers={
                "Content-Type": "application/json",
                "Authorization": long_token,
            },
        )

        captured = capsys.readouterr()
        assert "[HTTP DEBUG] Headers:" in captured.out
        assert "Content-Type" in captured.out
        # 长 token 应该被脱敏
        assert "..." in captured.out

    def test_log_request_with_body(self, capsys):
        """测试带请求体的日志"""
        debugger = HTTPDebugger()
        debugger.log_request(
            "POST",
            "http://example.com/api",
            body={"name": "Alice", "age": 25},
        )

        captured = capsys.readouterr()
        assert "[HTTP DEBUG] Body:" in captured.out
        assert "Alice" in captured.out

    def test_log_response_success(self, capsys):
        """测试成功响应日志"""
        debugger = HTTPDebugger()
        debugger.log_request("GET", "http://example.com/api")
        debugger.log_response(200, body={"id": 1, "name": "Alice"})

        captured = capsys.readouterr()
        assert "Response: 200" in captured.out
        assert "✅" in captured.out

    def test_log_response_client_error(self, capsys):
        """测试客户端错误响应日志"""
        debugger = HTTPDebugger()
        debugger.log_request("GET", "http://example.com/api")
        debugger.log_response(404, body={"error": "Not found"})

        captured = capsys.readouterr()
        assert "Response: 404" in captured.out
        assert "⚠️" in captured.out

    def test_log_response_server_error(self, capsys):
        """测试服务端错误响应日志"""
        debugger = HTTPDebugger()
        debugger.log_request("GET", "http://example.com/api")
        debugger.log_response(500, body={"error": "Internal error"})

        captured = capsys.readouterr()
        assert "Response: 500" in captured.out
        assert "❌" in captured.out

    def test_log_error(self):
        """测试错误日志"""
        debugger = HTTPDebugger()
        debugger.log_request("GET", "http://example.com/api")
        debugger.log_error(ConnectionError("Connection refused"))

        assert len(debugger.requests) == 1
        assert "error" in debugger.requests[0]["response"]
        assert debugger.requests[0]["response"]["error_type"] == "ConnectionError"

    def test_disabled_logging(self):
        """测试禁用状态不记录日志"""
        debugger = HTTPDebugger(enabled=False)
        debugger.log_request("GET", "http://example.com/api")
        debugger.log_response(200)

        assert len(debugger.requests) == 0


class TestHTTPDebuggerQueries:
    """HTTPDebugger 查询功能测试"""

    @pytest.fixture
    def debugger_with_data(self):
        """创建带数据的调试器"""
        debugger = HTTPDebugger()

        # 成功请求
        debugger.log_request("GET", "http://example.com/api/users")
        debugger.log_response(200, body={"users": []})

        # 404 错误
        debugger.log_request("GET", "http://example.com/api/notfound")
        debugger.log_response(404, body={"error": "Not found"})

        # 500 错误
        debugger.log_request("POST", "http://example.com/api/error")
        debugger.log_response(500, body={"error": "Server error"})

        # 连接错误
        debugger.log_request("GET", "http://example.com/api/timeout")
        debugger.log_error(TimeoutError("Request timeout"))

        return debugger

    def test_get_requests(self, debugger_with_data):
        """测试获取所有请求"""
        requests = debugger_with_data.get_requests()
        assert len(requests) == 4

    def test_get_failed_requests(self, debugger_with_data):
        """测试获取失败请求"""
        failed = debugger_with_data.get_failed_requests()
        assert len(failed) == 3  # 404, 500, timeout

    def test_print_summary(self, debugger_with_data, capsys):
        """测试打印摘要"""
        debugger_with_data.print_summary()

        captured = capsys.readouterr()
        assert "HTTP调试摘要" in captured.out
        assert "总请求数: 4" in captured.out
        assert "失败: 3" in captured.out

    def test_print_summary_empty(self, capsys):
        """测试空摘要"""
        debugger = HTTPDebugger()
        debugger.print_summary()

        captured = capsys.readouterr()
        assert "无请求记录" in captured.out


class TestHTTPDebuggerTruncation:
    """HTTPDebugger 截断功能测试"""

    def test_truncate_long_body(self):
        """测试截断长 body"""
        debugger = HTTPDebugger(max_body_length=50)
        long_body = {"data": "x" * 100}

        debugger.log_request("POST", "http://example.com", body=long_body)
        debugger.log_response(200)

        assert "truncated" in str(debugger.requests[0]["body"])

    def test_truncate_long_dict_value(self):
        """测试截断字典中的长值"""
        debugger = HTTPDebugger()
        long_headers = {"X-Long-Header": "x" * 300}

        result = debugger._truncate_dict(long_headers)
        assert result["X-Long-Header"].endswith("...")


class TestGlobalDebugger:
    """全局调试器测试"""

    def setup_method(self):
        """每个测试前重置全局调试器"""
        import df_test_framework.testing.debugging.http as http_module

        http_module._global_debugger = None

    def test_enable_disable(self):
        """测试启用和禁用全局调试器"""
        debugger = enable_http_debug()
        assert debugger is not None
        assert debugger.enabled is True

        disable_http_debug()
        assert debugger.enabled is False

    def test_get_global_debugger(self):
        """测试获取全局调试器"""
        enable_http_debug()
        debugger = get_global_debugger()
        assert debugger is not None

    def test_enable_with_custom_length(self):
        """测试自定义 body 长度"""
        debugger = enable_http_debug(max_body_length=500)
        assert debugger.max_body_length == 500
