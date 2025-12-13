"""断言助手"""

from typing import Any

from assertpy import assert_that
from loguru import logger


class AssertHelper:
    """
    断言助手

    提供常用的断言方法和增强功能
    """

    @staticmethod
    def assert_response_success(
        response_data: dict[str, Any],
        expected_code: str = "200",
    ) -> None:
        """
        断言响应成功

        Args:
            response_data: 响应数据字典
            expected_code: 期望的响应码
        """
        logger.info(f"断言响应成功: code={expected_code}")
        assert_that(response_data).contains_key("success", "code", "message")
        assert_that(response_data["success"]).is_true()
        assert_that(response_data["code"]).is_equal_to(expected_code)

    @staticmethod
    def assert_response_error(
        response_data: dict[str, Any],
        expected_code: str,
        expected_message: str | None = None,
    ) -> None:
        """
        断言响应错误

        Args:
            response_data: 响应数据字典
            expected_code: 期望的错误码
            expected_message: 期望的错误消息(可选)
        """
        logger.info(f"断言响应错误: code={expected_code}")
        assert_that(response_data).contains_key("success", "code", "message")
        assert_that(response_data["success"]).is_false()
        assert_that(response_data["code"]).is_equal_to(expected_code)

        if expected_message:
            assert_that(response_data["message"]).contains(expected_message)

    @staticmethod
    def assert_field_equals(
        actual: dict[str, Any],
        field: str,
        expected: Any,
    ) -> None:
        """
        断言字段值相等

        Args:
            actual: 实际数据字典
            field: 字段名
            expected: 期望值
        """
        logger.info(f"断言字段 '{field}' = {expected}")
        assert_that(actual).contains_key(field)
        assert_that(actual[field]).is_equal_to(expected)

    @staticmethod
    def assert_field_not_none(
        actual: dict[str, Any],
        field: str,
    ) -> None:
        """
        断言字段不为空

        Args:
            actual: 实际数据字典
            field: 字段名
        """
        logger.info(f"断言字段 '{field}' 不为空")
        assert_that(actual).contains_key(field)
        assert_that(actual[field]).is_not_none()

    @staticmethod
    def assert_list_length(
        actual: list[Any],
        expected_length: int,
    ) -> None:
        """
        断言列表长度

        Args:
            actual: 实际列表
            expected_length: 期望长度
        """
        logger.info(f"断言列表长度 = {expected_length}")
        assert_that(actual).is_length(expected_length)

    @staticmethod
    def assert_list_not_empty(actual: list[Any]) -> None:
        """
        断言列表不为空

        Args:
            actual: 实际列表
        """
        logger.info("断言列表不为空")
        assert_that(actual).is_not_empty()

    @staticmethod
    def assert_dict_contains_keys(
        actual: dict[str, Any],
        *keys: str,
    ) -> None:
        """
        断言字典包含指定的键

        Args:
            actual: 实际字典
            *keys: 期望包含的键
        """
        logger.info(f"断言字典包含键: {keys}")
        assert_that(actual).contains_key(*keys)

    @staticmethod
    def assert_value_in_range(
        actual: float,
        min_value: float,
        max_value: float,
    ) -> None:
        """
        断言值在范围内

        Args:
            actual: 实际值
            min_value: 最小值
            max_value: 最大值
        """
        logger.info(f"断言值在范围 [{min_value}, {max_value}]")
        assert_that(actual).is_between(min_value, max_value)

    @staticmethod
    def assert_string_contains(
        actual: str,
        *substrings: str,
    ) -> None:
        """
        断言字符串包含子串

        Args:
            actual: 实际字符串
            *substrings: 期望包含的子串
        """
        logger.info(f"断言字符串包含: {substrings}")
        for substring in substrings:
            assert_that(actual).contains(substring)

    @staticmethod
    def assert_regex_match(
        actual: str,
        pattern: str,
    ) -> None:
        """
        断言字符串匹配正则表达式

        Args:
            actual: 实际字符串
            pattern: 正则表达式模式
        """
        logger.info(f"断言正则匹配: {pattern}")
        assert_that(actual).matches(pattern)


__all__ = ["AssertHelper"]
