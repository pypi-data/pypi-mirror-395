"""utils/validators.py 工具模块模板"""

UTILS_VALIDATORS_TEMPLATE = """\"\"\"数据验证工具

提供常用的数据验证函数。
\"\"\"

import re
from typing import Any


def is_valid_email(email: str) -> bool:
    \"\"\"验证邮箱格式

    Args:
        email: 邮箱地址

    Returns:
        bool: 是否为有效邮箱
    \"\"\"
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_valid_phone(phone: str) -> bool:
    \"\"\"验证手机号格式（中国大陆）

    Args:
        phone: 手机号

    Returns:
        bool: 是否为有效手机号
    \"\"\"
    pattern = r'^1[3-9]\\d{9}$'
    return bool(re.match(pattern, phone))


def is_valid_id_card(id_card: str) -> bool:
    \"\"\"验证身份证号格式（中国大陆）

    Args:
        id_card: 身份证号

    Returns:
        bool: 是否为有效身份证号
    \"\"\"
    pattern = r'^[1-9]\\d{5}(18|19|20)\\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\\d{3}[0-9Xx]$'
    return bool(re.match(pattern, id_card))


def is_not_empty(value: Any) -> bool:
    \"\"\"验证值不为空

    Args:
        value: 待验证的值

    Returns:
        bool: 是否不为空
    \"\"\"
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict, tuple)):
        return len(value) > 0
    return True


__all__ = [
    "is_valid_email",
    "is_valid_phone",
    "is_valid_id_card",
    "is_not_empty",
]
"""

__all__ = ["UTILS_VALIDATORS_TEMPLATE"]
