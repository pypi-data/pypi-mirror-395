"""
上下文载体实现

支持在不同传输协议中传播 ExecutionContext。
"""

from df_test_framework.infrastructure.context.carriers.grpc import GrpcContextCarrier
from df_test_framework.infrastructure.context.carriers.http import HttpContextCarrier
from df_test_framework.infrastructure.context.carriers.mq import MqContextCarrier

__all__ = [
    "HttpContextCarrier",
    "GrpcContextCarrier",
    "MqContextCarrier",
]
