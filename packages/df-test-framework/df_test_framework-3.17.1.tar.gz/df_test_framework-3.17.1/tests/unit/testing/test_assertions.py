"""断言辅助单元测试

测试HTTP响应断言功能

v3.10.0 - P2.2 测试数据工具增强
"""

from dataclasses import dataclass
from datetime import timedelta

import pytest

from df_test_framework.testing.assertions import (
    ResponseAssertions,
    assert_content_type,
    assert_header_has,
    assert_json_equals,
    assert_json_has,
    assert_status,
    assert_success,
)


@dataclass
class MockResponse:
    """模拟HTTP响应"""

    status_code: int
    _json: dict
    headers: dict
    text: str = ""
    elapsed: timedelta = None

    def json(self):
        return self._json


class TestAssertStatus:
    """状态码断言测试"""

    def test_assert_status_success(self):
        """测试状态码匹配"""
        response = MockResponse(status_code=200, _json={}, headers={})

        # 不应该抛出异常
        assert_status(response, 200)

    def test_assert_status_failure(self):
        """测试状态码不匹配"""
        response = MockResponse(status_code=404, _json={}, headers={}, text="Not Found")

        with pytest.raises(AssertionError) as exc_info:
            assert_status(response, 200)

        assert "状态码不匹配" in str(exc_info.value)
        assert "期望: 200" in str(exc_info.value)
        assert "实际: 404" in str(exc_info.value)

    def test_assert_success(self):
        """测试2xx成功断言"""
        for status in [200, 201, 204]:
            response = MockResponse(status_code=status, _json={}, headers={})
            assert_success(response)

    def test_assert_success_failure(self):
        """测试非2xx失败"""
        response = MockResponse(status_code=400, _json={}, headers={}, text="Bad Request")

        with pytest.raises(AssertionError) as exc_info:
            assert_success(response)

        assert "期望2xx成功响应" in str(exc_info.value)


class TestAssertJson:
    """JSON断言测试"""

    def test_assert_json_has_success(self):
        """测试字段存在"""
        response = MockResponse(
            status_code=200, _json={"id": 1, "name": "Alice", "email": "alice@test.com"}, headers={}
        )

        # 不应该抛出异常
        assert_json_has(response, "id", "name", "email")

    def test_assert_json_has_missing_field(self):
        """测试缺少字段"""
        response = MockResponse(status_code=200, _json={"id": 1, "name": "Alice"}, headers={})

        with pytest.raises(AssertionError) as exc_info:
            assert_json_has(response, "id", "email")

        assert "缺少字段" in str(exc_info.value)
        assert "email" in str(exc_info.value)

    def test_assert_json_equals_non_strict(self):
        """测试非严格模式JSON匹配"""
        response = MockResponse(
            status_code=200, _json={"id": 1, "name": "Alice", "extra": "data"}, headers={}
        )

        # 非严格模式：只要包含期望的键值对即可
        assert_json_equals(response, {"id": 1, "name": "Alice"})

    def test_assert_json_equals_strict(self):
        """测试严格模式JSON匹配"""
        response = MockResponse(status_code=200, _json={"id": 1, "name": "Alice"}, headers={})

        # 严格模式：必须完全相等
        assert_json_equals(response, {"id": 1, "name": "Alice"}, strict=True)

    def test_assert_json_equals_strict_failure(self):
        """测试严格模式不匹配"""
        response = MockResponse(
            status_code=200, _json={"id": 1, "name": "Alice", "extra": "data"}, headers={}
        )

        with pytest.raises(AssertionError):
            assert_json_equals(response, {"id": 1, "name": "Alice"}, strict=True)


class TestAssertHeaders:
    """响应头断言测试"""

    def test_assert_header_exists(self):
        """测试响应头存在"""
        response = MockResponse(
            status_code=200,
            _json={},
            headers={"Content-Type": "application/json", "X-Request-Id": "123"},
        )

        assert_header_has(response, "Content-Type")
        assert_header_has(response, "X-Request-Id")

    def test_assert_header_case_insensitive(self):
        """测试响应头不区分大小写"""
        response = MockResponse(
            status_code=200, _json={}, headers={"Content-Type": "application/json"}
        )

        # 不同大小写都应该匹配
        assert_header_has(response, "content-type")
        assert_header_has(response, "CONTENT-TYPE")

    def test_assert_header_value(self):
        """测试响应头值匹配"""
        response = MockResponse(
            status_code=200, _json={}, headers={"Content-Type": "application/json; charset=utf-8"}
        )

        assert_header_has(response, "Content-Type", "application/json")

    def test_assert_header_missing(self):
        """测试响应头不存在"""
        response = MockResponse(
            status_code=200, _json={}, headers={"Content-Type": "application/json"}
        )

        with pytest.raises(AssertionError) as exc_info:
            assert_header_has(response, "X-Custom-Header")

        assert "不存在" in str(exc_info.value)

    def test_assert_content_type(self):
        """测试Content-Type快捷断言"""
        response = MockResponse(
            status_code=200, _json={}, headers={"Content-Type": "application/json; charset=utf-8"}
        )

        assert_content_type(response, "application/json")


class TestChainedAssertions:
    """链式断言测试"""

    def test_chained_assertions(self):
        """测试链式调用"""
        response = MockResponse(
            status_code=200,
            _json={"id": 1, "name": "Alice"},
            headers={"Content-Type": "application/json"},
            elapsed=timedelta(milliseconds=100),
        )

        # 链式调用多个断言
        assertions = ResponseAssertions(response)
        assertions.status(200).success().json_has("id", "name")

    def test_chained_assertions_failure(self):
        """测试链式调用失败"""
        response = MockResponse(status_code=200, _json={"id": 1}, headers={})

        with pytest.raises(AssertionError):
            ResponseAssertions(response).status(200).json_has("id", "nonexistent")


class TestResponseTimeAssertion:
    """响应时间断言测试"""

    def test_response_time_success(self):
        """测试响应时间在限制内"""
        response = MockResponse(
            status_code=200, _json={}, headers={}, elapsed=timedelta(milliseconds=100)
        )

        ResponseAssertions.assert_response_time_lt(response, 500)

    def test_response_time_exceeded(self):
        """测试响应时间超时"""
        response = MockResponse(
            status_code=200, _json={}, headers={}, elapsed=timedelta(milliseconds=1500)
        )

        with pytest.raises(AssertionError) as exc_info:
            ResponseAssertions.assert_response_time_lt(response, 1000)

        assert "响应时间超时" in str(exc_info.value)


class TestClientServerErrors:
    """客户端/服务端错误断言测试"""

    def test_assert_client_error(self):
        """测试4xx客户端错误"""
        for status in [400, 401, 403, 404]:
            response = MockResponse(status_code=status, _json={}, headers={})
            ResponseAssertions.assert_client_error(response)

    def test_assert_server_error(self):
        """测试5xx服务端错误"""
        for status in [500, 502, 503]:
            response = MockResponse(status_code=status, _json={}, headers={})
            ResponseAssertions.assert_server_error(response)


class TestJsonNotHas:
    """JSON字段不存在断言测试"""

    def test_assert_json_not_has_success(self):
        """测试字段不存在"""
        response = MockResponse(status_code=200, _json={"id": 1, "name": "Alice"}, headers={})

        ResponseAssertions.assert_json_not_has(response, "password", "secret")

    def test_assert_json_not_has_failure(self):
        """测试存在不应有的字段"""
        response = MockResponse(status_code=200, _json={"id": 1, "password": "secret"}, headers={})

        with pytest.raises(AssertionError) as exc_info:
            ResponseAssertions.assert_json_not_has(response, "password")

        assert "不应包含" in str(exc_info.value)
