"""测试断言辅助

提供丰富的断言辅助方法，简化测试代码

模块:
- response: HTTP响应断言
- data: 数据断言（开发中）

使用示例:
    >>> from df_test_framework.testing.assertions import (
    ...     ResponseAssertions,
    ...     assert_status,
    ...     assert_json_has,
    ... )
    >>>
    >>> # 静态方法
    >>> assert_status(response, 200)
    >>> assert_json_has(response, "user_id", "name")
    >>>
    >>> # 链式调用
    >>> ResponseAssertions(response).status(200).json_has("id")

v3.10.0 新增 - P2.2 测试数据工具增强
"""

from .response import (
    ResponseAssertions,
    assert_content_type,
    assert_header_has,
    assert_json_equals,
    assert_json_has,
    assert_json_path_equals,
    assert_json_schema,
    assert_response_time_lt,
    assert_status,
    assert_success,
)

__all__ = [
    # 响应断言类
    "ResponseAssertions",
    # 便捷函数
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
