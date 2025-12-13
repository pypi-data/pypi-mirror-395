"""gRPC 数据模型"""

from __future__ import annotations

from enum import Enum
from typing import Any, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class GrpcStatusCode(int, Enum):
    """gRPC 状态码

    参考: https://grpc.github.io/grpc/core/md_doc_statuscodes.html
    """

    OK = 0
    CANCELLED = 1
    UNKNOWN = 2
    INVALID_ARGUMENT = 3
    DEADLINE_EXCEEDED = 4
    NOT_FOUND = 5
    ALREADY_EXISTS = 6
    PERMISSION_DENIED = 7
    RESOURCE_EXHAUSTED = 8
    FAILED_PRECONDITION = 9
    ABORTED = 10
    OUT_OF_RANGE = 11
    UNIMPLEMENTED = 12
    INTERNAL = 13
    UNAVAILABLE = 14
    DATA_LOSS = 15
    UNAUTHENTICATED = 16


class GrpcError(Exception):
    """gRPC 错误"""

    def __init__(
        self,
        code: GrpcStatusCode,
        message: str,
        details: str | None = None,
    ) -> None:
        self.code = code
        self.message = message
        self.details = details
        super().__init__(f"[{code.name}] {message}")

    def __str__(self) -> str:
        parts = [f"gRPC Error [{self.code.name}]: {self.message}"]
        if self.details:
            parts.append(f"Details: {self.details}")
        return "\n".join(parts)


class GrpcResponse[T](BaseModel):
    """gRPC 响应模型"""

    data: T | None = Field(None, description="响应数据")
    status_code: GrpcStatusCode = Field(GrpcStatusCode.OK, description="状态码")
    message: str = Field("", description="状态消息")
    metadata: dict[str, str] = Field(default_factory=dict, description="响应元数据")
    trailing_metadata: dict[str, str] = Field(default_factory=dict, description="尾部元数据")

    model_config = {"arbitrary_types_allowed": True}

    @property
    def is_success(self) -> bool:
        """是否成功"""
        return self.status_code == GrpcStatusCode.OK

    def raise_for_status(self) -> None:
        """如果失败则抛出异常"""
        if not self.is_success:
            raise GrpcError(
                code=self.status_code,
                message=self.message,
            )


class ChannelOptions(BaseModel):
    """gRPC 通道选项"""

    max_send_message_length: int = Field(-1, description="最大发送消息长度（字节），-1 表示无限制")
    max_receive_message_length: int = Field(
        -1, description="最大接收消息长度（字节），-1 表示无限制"
    )
    keepalive_time_ms: int = Field(60000, description="keepalive 时间（毫秒）")
    keepalive_timeout_ms: int = Field(20000, description="keepalive 超时（毫秒）")
    keepalive_permit_without_calls: bool = Field(True, description="是否允许无调用时发送 keepalive")
    http2_initial_sequence_number: int = Field(0, description="HTTP/2 初始序列号")

    def to_grpc_options(self) -> list[tuple[str, Any]]:
        """转换为 gRPC 选项格式"""
        return [
            ("grpc.max_send_message_length", self.max_send_message_length),
            ("grpc.max_receive_message_length", self.max_receive_message_length),
            ("grpc.keepalive_time_ms", self.keepalive_time_ms),
            ("grpc.keepalive_timeout_ms", self.keepalive_timeout_ms),
            (
                "grpc.keepalive_permit_without_calls",
                1 if self.keepalive_permit_without_calls else 0,
            ),
            (
                "grpc.http2.initial_sequence_number",
                self.http2_initial_sequence_number,
            ),
        ]
