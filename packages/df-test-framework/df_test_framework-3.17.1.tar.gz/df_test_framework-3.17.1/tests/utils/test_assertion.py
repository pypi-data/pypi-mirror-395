"""测试 assertion.py - 断言助手

测试覆盖:
- AssertHelper类的所有静态方法
- 成功和失败断言场景
"""

import pytest

from df_test_framework.utils.assertion import AssertHelper


class TestAssertResponseSuccess:
    """测试响应成功断言"""

    def test_assert_response_success_with_default_code(self):
        """测试使用默认响应码断言成功"""
        response = {"success": True, "code": "200", "message": "操作成功"}
        # 不应抛出异常
        AssertHelper.assert_response_success(response)

    def test_assert_response_success_with_custom_code(self):
        """测试使用自定义响应码断言成功"""
        response = {"success": True, "code": "0", "message": "操作成功"}
        AssertHelper.assert_response_success(response, expected_code="0")

    def test_assert_response_success_fails_on_missing_key(self):
        """测试缺少关键字段时断言失败"""
        response = {
            "success": True,
            "message": "操作成功",
            # 缺少 code
        }
        with pytest.raises(AssertionError):
            AssertHelper.assert_response_success(response)

    def test_assert_response_success_fails_on_wrong_success(self):
        """测试success为False时断言失败"""
        response = {"success": False, "code": "200", "message": "操作失败"}
        with pytest.raises(AssertionError):
            AssertHelper.assert_response_success(response)

    def test_assert_response_success_fails_on_wrong_code(self):
        """测试响应码不匹配时断言失败"""
        response = {"success": True, "code": "500", "message": "操作成功"}
        with pytest.raises(AssertionError):
            AssertHelper.assert_response_success(response)


class TestAssertResponseError:
    """测试响应错误断言"""

    def test_assert_response_error_without_message(self):
        """测试不检查消息的错误断言"""
        response = {"success": False, "code": "400", "message": "参数错误"}
        AssertHelper.assert_response_error(response, expected_code="400")

    def test_assert_response_error_with_message(self):
        """测试检查消息的错误断言"""
        response = {"success": False, "code": "401", "message": "用户未登录，请先登录"}
        AssertHelper.assert_response_error(response, expected_code="401", expected_message="未登录")

    def test_assert_response_error_fails_on_success_true(self):
        """测试success为True时断言失败"""
        response = {"success": True, "code": "400", "message": "参数错误"}
        with pytest.raises(AssertionError):
            AssertHelper.assert_response_error(response, expected_code="400")

    def test_assert_response_error_fails_on_wrong_code(self):
        """测试错误码不匹配时断言失败"""
        response = {"success": False, "code": "500", "message": "服务器错误"}
        with pytest.raises(AssertionError):
            AssertHelper.assert_response_error(response, expected_code="400")

    def test_assert_response_error_fails_on_wrong_message(self):
        """测试错误消息不匹配时断言失败"""
        response = {"success": False, "code": "400", "message": "参数错误"}
        with pytest.raises(AssertionError):
            AssertHelper.assert_response_error(
                response, expected_code="400", expected_message="权限不足"
            )


class TestAssertFieldEquals:
    """测试字段值相等断言"""

    def test_assert_field_equals_success(self):
        """测试字段值相等断言成功"""
        data = {"name": "Alice", "age": 25}
        AssertHelper.assert_field_equals(data, "name", "Alice")
        AssertHelper.assert_field_equals(data, "age", 25)

    def test_assert_field_equals_fails_on_missing_field(self):
        """测试字段不存在时断言失败"""
        data = {"name": "Alice"}
        with pytest.raises(AssertionError):
            AssertHelper.assert_field_equals(data, "age", 25)

    def test_assert_field_equals_fails_on_wrong_value(self):
        """测试字段值不匹配时断言失败"""
        data = {"name": "Alice"}
        with pytest.raises(AssertionError):
            AssertHelper.assert_field_equals(data, "name", "Bob")


class TestAssertFieldNotNone:
    """测试字段不为空断言"""

    def test_assert_field_not_none_success(self):
        """测试字段不为空断言成功"""
        data = {"name": "Alice", "age": 0, "active": False}
        AssertHelper.assert_field_not_none(data, "name")
        AssertHelper.assert_field_not_none(data, "age")
        AssertHelper.assert_field_not_none(data, "active")

    def test_assert_field_not_none_fails_on_missing_field(self):
        """测试字段不存在时断言失败"""
        data = {"name": "Alice"}
        with pytest.raises(AssertionError):
            AssertHelper.assert_field_not_none(data, "age")

    def test_assert_field_not_none_fails_on_none_value(self):
        """测试字段值为None时断言失败"""
        data = {"name": None}
        with pytest.raises(AssertionError):
            AssertHelper.assert_field_not_none(data, "name")


class TestAssertListLength:
    """测试列表长度断言"""

    def test_assert_list_length_success(self):
        """测试列表长度断言成功"""
        data = [1, 2, 3, 4, 5]
        AssertHelper.assert_list_length(data, 5)

    def test_assert_list_length_empty_list(self):
        """测试空列表长度断言"""
        data = []
        AssertHelper.assert_list_length(data, 0)

    def test_assert_list_length_fails_on_wrong_length(self):
        """测试长度不匹配时断言失败"""
        data = [1, 2, 3]
        with pytest.raises(AssertionError):
            AssertHelper.assert_list_length(data, 5)


class TestAssertListNotEmpty:
    """测试列表不为空断言"""

    def test_assert_list_not_empty_success(self):
        """测试列表不为空断言成功"""
        data = [1, 2, 3]
        AssertHelper.assert_list_not_empty(data)

    def test_assert_list_not_empty_single_element(self):
        """测试单元素列表不为空"""
        data = [1]
        AssertHelper.assert_list_not_empty(data)

    def test_assert_list_not_empty_fails_on_empty_list(self):
        """测试空列表时断言失败"""
        data = []
        with pytest.raises(AssertionError):
            AssertHelper.assert_list_not_empty(data)


class TestAssertDictContainsKeys:
    """测试字典包含键断言"""

    def test_assert_dict_contains_keys_single_key(self):
        """测试字典包含单个键"""
        data = {"name": "Alice", "age": 25}
        AssertHelper.assert_dict_contains_keys(data, "name")

    def test_assert_dict_contains_keys_multiple_keys(self):
        """测试字典包含多个键"""
        data = {"name": "Alice", "age": 25, "email": "alice@test.com"}
        AssertHelper.assert_dict_contains_keys(data, "name", "age", "email")

    def test_assert_dict_contains_keys_fails_on_missing_key(self):
        """测试缺少键时断言失败"""
        data = {"name": "Alice"}
        with pytest.raises(AssertionError):
            AssertHelper.assert_dict_contains_keys(data, "name", "age")


class TestAssertValueInRange:
    """测试值范围断言"""

    def test_assert_value_in_range_success(self):
        """测试值在范围内断言成功"""
        AssertHelper.assert_value_in_range(5.0, 1.0, 10.0)
        AssertHelper.assert_value_in_range(1.0, 1.0, 10.0)  # 边界值
        AssertHelper.assert_value_in_range(10.0, 1.0, 10.0)  # 边界值

    def test_assert_value_in_range_integer(self):
        """测试整数值在范围内"""
        AssertHelper.assert_value_in_range(50, 0, 100)

    def test_assert_value_in_range_fails_below_min(self):
        """测试值小于最小值时断言失败"""
        with pytest.raises(AssertionError):
            AssertHelper.assert_value_in_range(0.5, 1.0, 10.0)

    def test_assert_value_in_range_fails_above_max(self):
        """测试值大于最大值时断言失败"""
        with pytest.raises(AssertionError):
            AssertHelper.assert_value_in_range(10.5, 1.0, 10.0)


class TestAssertStringContains:
    """测试字符串包含断言"""

    def test_assert_string_contains_single_substring(self):
        """测试字符串包含单个子串"""
        text = "Hello World"
        AssertHelper.assert_string_contains(text, "Hello")

    def test_assert_string_contains_multiple_substrings(self):
        """测试字符串包含多个子串"""
        text = "The quick brown fox jumps over the lazy dog"
        AssertHelper.assert_string_contains(text, "quick", "fox", "lazy")

    def test_assert_string_contains_chinese(self):
        """测试中文字符串包含"""
        text = "你好，世界！"
        AssertHelper.assert_string_contains(text, "你好", "世界")

    def test_assert_string_contains_fails_on_missing_substring(self):
        """测试子串不存在时断言失败"""
        text = "Hello World"
        with pytest.raises(AssertionError):
            AssertHelper.assert_string_contains(text, "Hello", "Python")


class TestAssertRegexMatch:
    """测试正则匹配断言"""

    def test_assert_regex_match_success(self):
        """测试正则匹配成功"""
        email = "test@example.com"
        AssertHelper.assert_regex_match(email, r"^\w+@\w+\.\w+$")

    def test_assert_regex_match_phone_number(self):
        """测试手机号正则匹配"""
        phone = "13812345678"
        AssertHelper.assert_regex_match(phone, r"^1\d{10}$")

    def test_assert_regex_match_fails_on_no_match(self):
        """测试正则不匹配时断言失败"""
        text = "not an email"
        with pytest.raises(AssertionError):
            AssertHelper.assert_regex_match(text, r"^\w+@\w+\.\w+$")


__all__ = [
    "TestAssertResponseSuccess",
    "TestAssertResponseError",
    "TestAssertFieldEquals",
    "TestAssertFieldNotNone",
    "TestAssertListLength",
    "TestAssertListNotEmpty",
    "TestAssertDictContainsKeys",
    "TestAssertValueInRange",
    "TestAssertStringContains",
    "TestAssertRegexMatch",
]
