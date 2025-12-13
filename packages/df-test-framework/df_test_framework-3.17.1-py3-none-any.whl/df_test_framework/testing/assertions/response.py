"""HTTP响应断言辅助

提供HTTP响应的专用断言方法，简化API测试

特性:
- 状态码断言
- JSON Schema验证
- 响应字段检查
- 响应时间断言
- 链式调用支持

使用示例:
    >>> from df_test_framework.testing.assertions import ResponseAssertions
    >>>
    >>> # 基础断言
    >>> ResponseAssertions.assert_status(response, 200)
    >>> ResponseAssertions.assert_success(response)
    >>>
    >>> # JSON断言
    >>> ResponseAssertions.assert_json_has(response, "user_id", "name")
    >>> ResponseAssertions.assert_json_equals(response, {"code": 0})
    >>>
    >>> # 链式断言
    >>> ResponseAssertions(response) \\
    ...     .status(200) \\
    ...     .json_has("user_id") \\
    ...     .json_path_equals("$.data.name", "Alice")

v3.10.0 新增 - P2.2 测试数据工具增强
"""

from __future__ import annotations

from typing import Any


class ResponseAssertions:
    """HTTP响应断言类

    支持两种使用方式:
    1. 静态方法: ResponseAssertions.assert_status(response, 200)
    2. 链式调用: ResponseAssertions(response).status(200).json_has("id")

    示例:
        >>> # 静态方法
        >>> ResponseAssertions.assert_status(response, 200)
        >>> ResponseAssertions.assert_json_has(response, "user_id")

        >>> # 链式调用
        >>> assertions = ResponseAssertions(response)
        >>> assertions.status(200).json_has("user_id", "name").response_time_lt(1000)
    """

    def __init__(self, response: Any):
        """初始化断言对象

        Args:
            response: HTTP响应对象（需要有status_code和json()方法）
        """
        self._response = response
        self._json_cache: dict[str, Any] | None = None

    @property
    def response(self) -> Any:
        """获取响应对象"""
        return self._response

    def _get_json(self) -> dict[str, Any]:
        """获取响应JSON（带缓存）"""
        if self._json_cache is None:
            self._json_cache = self._response.json()
        return self._json_cache

    # ============ 链式方法 ============

    def status(self, expected: int) -> ResponseAssertions:
        """断言状态码（链式）

        Args:
            expected: 期望的状态码

        Returns:
            self，支持链式调用

        Raises:
            AssertionError: 状态码不匹配
        """
        self.assert_status(self._response, expected)
        return self

    def success(self) -> ResponseAssertions:
        """断言成功响应（2xx）

        Returns:
            self

        Raises:
            AssertionError: 非2xx响应
        """
        self.assert_success(self._response)
        return self

    def json_has(self, *keys: str) -> ResponseAssertions:
        """断言响应包含指定字段（链式）

        Args:
            *keys: 字段名列表

        Returns:
            self

        Raises:
            AssertionError: 缺少字段
        """
        self.assert_json_has(self._response, *keys)
        return self

    def json_equals(self, expected: dict, strict: bool = False) -> ResponseAssertions:
        """断言响应JSON等于预期（链式）

        Args:
            expected: 期望的JSON
            strict: 是否严格匹配（True=完全相等，False=包含即可）

        Returns:
            self
        """
        self.assert_json_equals(self._response, expected, strict=strict)
        return self

    def json_path_equals(self, path: str, expected: Any) -> ResponseAssertions:
        """断言JSONPath路径的值（链式）

        Args:
            path: JSONPath表达式
            expected: 期望值

        Returns:
            self
        """
        self.assert_json_path_equals(self._response, path, expected)
        return self

    def response_time_lt(self, max_ms: int) -> ResponseAssertions:
        """断言响应时间小于指定毫秒（链式）

        Args:
            max_ms: 最大响应时间（毫秒）

        Returns:
            self
        """
        self.assert_response_time_lt(self._response, max_ms)
        return self

    def header_has(self, header_name: str, expected_value: str | None = None) -> ResponseAssertions:
        """断言响应头存在（链式）

        Args:
            header_name: 响应头名称
            expected_value: 期望值（可选）

        Returns:
            self
        """
        self.assert_header_has(self._response, header_name, expected_value)
        return self

    # ============ 静态断言方法 ============

    @staticmethod
    def assert_status(response: Any, expected: int) -> None:
        """断言HTTP状态码

        Args:
            response: HTTP响应对象
            expected: 期望的状态码

        Raises:
            AssertionError: 状态码不匹配

        示例:
            >>> ResponseAssertions.assert_status(response, 200)
            >>> ResponseAssertions.assert_status(response, 201)
        """
        actual = response.status_code
        assert actual == expected, (
            f"状态码不匹配\n期望: {expected}\n实际: {actual}\n响应: {_safe_response_text(response)}"
        )

    @staticmethod
    def assert_success(response: Any) -> None:
        """断言成功响应（2xx状态码）

        Args:
            response: HTTP响应对象

        Raises:
            AssertionError: 非2xx响应
        """
        actual = response.status_code
        assert 200 <= actual < 300, (
            f"期望2xx成功响应，实际: {actual}\n响应: {_safe_response_text(response)}"
        )

    @staticmethod
    def assert_client_error(response: Any) -> None:
        """断言客户端错误（4xx状态码）

        Args:
            response: HTTP响应对象

        Raises:
            AssertionError: 非4xx响应
        """
        actual = response.status_code
        assert 400 <= actual < 500, f"期望4xx客户端错误，实际: {actual}"

    @staticmethod
    def assert_server_error(response: Any) -> None:
        """断言服务端错误（5xx状态码）

        Args:
            response: HTTP响应对象

        Raises:
            AssertionError: 非5xx响应
        """
        actual = response.status_code
        assert 500 <= actual < 600, f"期望5xx服务端错误，实际: {actual}"

    @staticmethod
    def assert_json_has(response: Any, *keys: str) -> None:
        """断言响应JSON包含指定字段

        Args:
            response: HTTP响应对象
            *keys: 字段名列表

        Raises:
            AssertionError: 缺少字段

        示例:
            >>> ResponseAssertions.assert_json_has(response, "user_id", "name", "email")
        """
        data = response.json()

        missing = [key for key in keys if key not in data]
        if missing:
            raise AssertionError(f"响应缺少字段: {missing}\n实际字段: {list(data.keys())}")

    @staticmethod
    def assert_json_not_has(response: Any, *keys: str) -> None:
        """断言响应JSON不包含指定字段

        Args:
            response: HTTP响应对象
            *keys: 不应存在的字段名列表

        Raises:
            AssertionError: 存在不应有的字段
        """
        data = response.json()

        present = [key for key in keys if key in data]
        if present:
            raise AssertionError(f"响应不应包含字段: {present}")

    @staticmethod
    def assert_json_equals(response: Any, expected: dict, strict: bool = False) -> None:
        """断言响应JSON等于预期

        Args:
            response: HTTP响应对象
            expected: 期望的JSON
            strict: 严格模式（True=完全相等，False=包含即可）

        Raises:
            AssertionError: JSON不匹配

        示例:
            >>> # 非严格模式：只要包含expected的所有键值对即可
            >>> ResponseAssertions.assert_json_equals(response, {"code": 0})

            >>> # 严格模式：必须完全相等
            >>> ResponseAssertions.assert_json_equals(response, {"code": 0, "data": None}, strict=True)
        """
        actual = response.json()

        if strict:
            assert actual == expected, f"JSON不匹配（严格模式）\n期望: {expected}\n实际: {actual}"
        else:
            # 非严格模式：检查expected中的每个键值对
            for key, value in expected.items():
                assert key in actual, f"缺少字段: {key}"
                assert actual[key] == value, (
                    f"字段 '{key}' 值不匹配\n期望: {value}\n实际: {actual[key]}"
                )

    @staticmethod
    def assert_json_path_equals(response: Any, path: str, expected: Any) -> None:
        """断言JSONPath路径的值

        需要安装jsonpath-ng: pip install jsonpath-ng

        Args:
            response: HTTP响应对象
            path: JSONPath表达式
            expected: 期望值

        Raises:
            AssertionError: 值不匹配
            ImportError: 未安装jsonpath-ng

        示例:
            >>> ResponseAssertions.assert_json_path_equals(response, "$.data.user.name", "Alice")
            >>> ResponseAssertions.assert_json_path_equals(response, "$.items[0].id", 1)
        """
        try:
            from jsonpath_ng import parse
        except ImportError:
            raise ImportError("JSONPath断言需要jsonpath-ng库: pip install jsonpath-ng")

        data = response.json()
        expr = parse(path)
        matches = expr.find(data)

        if not matches:
            raise AssertionError(f"JSONPath '{path}' 未匹配任何值\n响应数据: {data}")

        actual = matches[0].value
        assert actual == expected, f"JSONPath '{path}' 值不匹配\n期望: {expected}\n实际: {actual}"

    @staticmethod
    def assert_json_schema(response: Any, schema: dict) -> None:
        """断言响应符合JSON Schema

        需要安装jsonschema: pip install jsonschema

        Args:
            response: HTTP响应对象
            schema: JSON Schema定义

        Raises:
            AssertionError: Schema验证失败
            ImportError: 未安装jsonschema

        示例:
            >>> schema = {
            ...     "type": "object",
            ...     "required": ["id", "name"],
            ...     "properties": {
            ...         "id": {"type": "integer"},
            ...         "name": {"type": "string"}
            ...     }
            ... }
            >>> ResponseAssertions.assert_json_schema(response, schema)
        """
        try:
            import jsonschema
        except ImportError:
            raise ImportError("JSON Schema验证需要jsonschema库: pip install jsonschema")

        data = response.json()

        try:
            jsonschema.validate(data, schema)
        except jsonschema.ValidationError as e:
            raise AssertionError(
                f"JSON Schema验证失败\n"
                f"错误: {e.message}\n"
                f"路径: {list(e.path)}\n"
                f"实际值: {e.instance}"
            ) from e

    @staticmethod
    def assert_response_time_lt(response: Any, max_ms: int) -> None:
        """断言响应时间小于指定毫秒

        Args:
            response: HTTP响应对象（需要有elapsed属性）
            max_ms: 最大响应时间（毫秒）

        Raises:
            AssertionError: 响应时间超时
            AttributeError: 响应对象不支持elapsed属性

        示例:
            >>> ResponseAssertions.assert_response_time_lt(response, 1000)  # 小于1秒
        """
        if not hasattr(response, "elapsed"):
            raise AttributeError("响应对象不支持elapsed属性")

        actual_ms = response.elapsed.total_seconds() * 1000
        assert actual_ms < max_ms, f"响应时间超时\n期望: <{max_ms}ms\n实际: {actual_ms:.2f}ms"

    @staticmethod
    def assert_header_has(
        response: Any, header_name: str, expected_value: str | None = None
    ) -> None:
        """断言响应头存在

        Args:
            response: HTTP响应对象
            header_name: 响应头名称（不区分大小写）
            expected_value: 期望值（可选）

        Raises:
            AssertionError: 响应头不存在或值不匹配

        示例:
            >>> ResponseAssertions.assert_header_has(response, "Content-Type")
            >>> ResponseAssertions.assert_header_has(response, "Content-Type", "application/json")
        """
        headers = response.headers

        # 不区分大小写查找
        actual_value = None
        for name, value in headers.items():
            if name.lower() == header_name.lower():
                actual_value = value
                break

        if actual_value is None:
            raise AssertionError(
                f"响应头 '{header_name}' 不存在\n实际响应头: {list(headers.keys())}"
            )

        if expected_value is not None:
            assert expected_value in actual_value, (
                f"响应头 '{header_name}' 值不匹配\n期望包含: {expected_value}\n实际: {actual_value}"
            )

    @staticmethod
    def assert_content_type(response: Any, expected: str) -> None:
        """断言Content-Type

        Args:
            response: HTTP响应对象
            expected: 期望的Content-Type（可以是部分匹配）

        示例:
            >>> ResponseAssertions.assert_content_type(response, "application/json")
        """
        ResponseAssertions.assert_header_has(response, "Content-Type", expected)


def _safe_response_text(response: Any, max_length: int = 500) -> str:
    """安全获取响应文本（截断过长内容）"""
    try:
        text = response.text
        if len(text) > max_length:
            return text[:max_length] + "...(truncated)"
        return text
    except Exception:
        return "<无法获取响应内容>"


# 便捷别名
assert_status = ResponseAssertions.assert_status
assert_success = ResponseAssertions.assert_success
assert_json_has = ResponseAssertions.assert_json_has
assert_json_equals = ResponseAssertions.assert_json_equals
assert_json_schema = ResponseAssertions.assert_json_schema
assert_json_path_equals = ResponseAssertions.assert_json_path_equals
assert_response_time_lt = ResponseAssertions.assert_response_time_lt
assert_header_has = ResponseAssertions.assert_header_has
assert_content_type = ResponseAssertions.assert_content_type

__all__ = [
    "ResponseAssertions",
    "assert_status",
    "assert_success",
    "assert_json_has",
    "assert_json_equals",
    "assert_json_schema",
    "assert_json_path_equals",
    "assert_response_time_lt",
    "assert_header_has",
    "assert_content_type",
]
