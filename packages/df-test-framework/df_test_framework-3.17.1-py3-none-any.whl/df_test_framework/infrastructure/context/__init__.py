"""
上下文载体

实现上下文在不同传输协议中的注入和提取。
"""

from df_test_framework.infrastructure.context.carriers import (
    GrpcContextCarrier,
    HttpContextCarrier,
    MqContextCarrier,
)

__all__ = [
    "HttpContextCarrier",
    "GrpcContextCarrier",
    "MqContextCarrier",
]
