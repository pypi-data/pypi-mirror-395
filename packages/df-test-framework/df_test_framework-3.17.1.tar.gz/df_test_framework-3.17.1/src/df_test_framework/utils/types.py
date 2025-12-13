"""常用类型工具

提供测试中常用的类型定义和序列化器。

v3.6新增:
- DecimalAsFloat: Decimal 序列化为浮点数
- DecimalAsCurrency: Decimal 序列化为货币格式

使用场景:
- 99%的场景：直接使用标准 Decimal，HttpClient 自动处理
- 1%的场景：需要特殊格式时使用本模块提供的类型
"""

from decimal import Decimal
from typing import Annotated

from pydantic import PlainSerializer

__all__ = [
    "Decimal",
    "DecimalAsFloat",
    "DecimalAsCurrency",
]


# ========== 场景 1: 序列化为浮点数 ==========

DecimalAsFloat = Annotated[
    Decimal,
    PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
]
"""Decimal 序列化为浮点数

使用场景：某些 API 要求金额字段为数字类型而不是字符串

Example:
    >>> from pydantic import BaseModel
    >>> from df_test_framework.utils.types import DecimalAsFloat
    >>>
    >>> class PriceRequest(BaseModel):
    ...     price: DecimalAsFloat  # 序列化为浮点数
    >>>
    >>> request = PriceRequest(price=Decimal("99.99"))
    >>> request.model_dump_json()
    '{"price":99.99}'  # 数字类型，不是字符串

Warning:
    浮点数有精度问题，金融场景慎用！推荐使用默认的字符串序列化。
"""


# ========== 场景 2: 序列化为货币格式 ==========


def _format_currency(value: Decimal) -> str:
    """格式化为货币格式：$123.45"""
    return f"${value:.2f}"


DecimalAsCurrency = Annotated[
    Decimal,
    PlainSerializer(_format_currency, return_type=str, when_used="json"),
]
"""Decimal 序列化为货币格式

使用场景：显示层需要格式化的金额字符串

Example:
    >>> from pydantic import BaseModel
    >>> from df_test_framework.utils.types import DecimalAsCurrency
    >>>
    >>> class DisplayRequest(BaseModel):
    ...     amount: DecimalAsCurrency  # 序列化为货币格式
    >>>
    >>> request = DisplayRequest(amount=Decimal("123.45"))
    >>> request.model_dump_json()
    '{"amount":"$123.45"}'

Note:
    - 默认使用美元符号 ($)
    - 保留2位小数
    - 如需自定义格式，请使用 @field_serializer 装饰器
"""
