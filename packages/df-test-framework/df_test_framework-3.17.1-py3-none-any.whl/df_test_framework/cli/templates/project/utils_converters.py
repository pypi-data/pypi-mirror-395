"""utils/converters.py 工具模块模板"""

UTILS_CONVERTERS_TEMPLATE = """\"\"\"数据转换工具

提供常用的数据类型转换函数。
\"\"\"

from typing import Any, Optional
from datetime import datetime, date


def to_int(value: Any, default: int = 0) -> int:
    \"\"\"转换为整数

    Args:
        value: 待转换的值
        default: 默认值

    Returns:
        int: 转换后的整数
    \"\"\"
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def to_float(value: Any, default: float = 0.0) -> float:
    \"\"\"转换为浮点数

    Args:
        value: 待转换的值
        default: 默认值

    Returns:
        float: 转换后的浮点数
    \"\"\"
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def to_bool(value: Any) -> bool:
    \"\"\"转换为布尔值

    Args:
        value: 待转换的值

    Returns:
        bool: 转换后的布尔值
    \"\"\"
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ('true', '1', 'yes', 'on')
    return bool(value)


def to_date_str(dt: datetime, fmt: str = "%Y-%m-%d") -> str:
    \"\"\"将日期时间转换为字符串

    Args:
        dt: 日期时间对象
        fmt: 格式化字符串

    Returns:
        str: 格式化后的日期字符串
    \"\"\"
    if isinstance(dt, datetime):
        return dt.strftime(fmt)
    elif isinstance(dt, date):
        return dt.strftime(fmt)
    return str(dt)


def parse_date(date_str: str, fmt: str = "%Y-%m-%d") -> Optional[datetime]:
    \"\"\"解析日期字符串

    Args:
        date_str: 日期字符串
        fmt: 格式化字符串

    Returns:
        Optional[datetime]: 解析后的日期时间对象
    \"\"\"
    try:
        return datetime.strptime(date_str, fmt)
    except ValueError:
        return None


__all__ = [
    "to_int",
    "to_float",
    "to_bool",
    "to_date_str",
    "parse_date",
]
"""

__all__ = ["UTILS_CONVERTERS_TEMPLATE"]
