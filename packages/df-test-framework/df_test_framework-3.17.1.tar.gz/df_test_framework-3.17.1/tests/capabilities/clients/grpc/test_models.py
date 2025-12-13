"""测试 gRPC 数据模型"""

import pytest

from df_test_framework.capabilities.clients.grpc.models import (
    ChannelOptions,
    GrpcError,
    GrpcResponse,
    GrpcStatusCode,
)


class TestGrpcStatusCode:
    """测试 GrpcStatusCode 枚举"""

    def test_status_code_values(self) -> None:
        """测试状态码值"""
        assert GrpcStatusCode.OK == 0
        assert GrpcStatusCode.CANCELLED == 1
        assert GrpcStatusCode.UNKNOWN == 2
        assert GrpcStatusCode.INVALID_ARGUMENT == 3
        assert GrpcStatusCode.NOT_FOUND == 5
        assert GrpcStatusCode.UNAUTHENTICATED == 16

    def test_status_code_names(self) -> None:
        """测试状态码名称"""
        assert GrpcStatusCode.OK.name == "OK"
        assert GrpcStatusCode.NOT_FOUND.name == "NOT_FOUND"


class TestGrpcError:
    """测试 GrpcError"""

    def test_create_error(self) -> None:
        """测试创建错误"""
        error = GrpcError(
            code=GrpcStatusCode.NOT_FOUND,
            message="Service not found",
        )

        assert error.code == GrpcStatusCode.NOT_FOUND
        assert error.message == "Service not found"
        assert error.details is None

    def test_error_with_details(self) -> None:
        """测试带详情的错误"""
        error = GrpcError(
            code=GrpcStatusCode.INVALID_ARGUMENT,
            message="Invalid input",
            details="Field 'email' is required",
        )

        assert error.details == "Field 'email' is required"

    def test_error_string_representation(self) -> None:
        """测试错误字符串表示"""
        error = GrpcError(
            code=GrpcStatusCode.PERMISSION_DENIED,
            message="Access denied",
            details="User does not have permission",
        )

        error_str = str(error)
        assert "gRPC Error [PERMISSION_DENIED]" in error_str
        assert "Access denied" in error_str
        assert "Details: User does not have permission" in error_str


class TestGrpcResponse:
    """测试 GrpcResponse"""

    def test_create_successful_response(self) -> None:
        """测试创建成功响应"""
        response = GrpcResponse(
            data={"id": "123", "name": "Test"},
            status_code=GrpcStatusCode.OK,
        )

        assert response.data == {"id": "123", "name": "Test"}
        assert response.status_code == GrpcStatusCode.OK
        assert response.is_success is True

    def test_create_error_response(self) -> None:
        """测试创建错误响应"""
        response = GrpcResponse(
            data=None,
            status_code=GrpcStatusCode.NOT_FOUND,
            message="Resource not found",
        )

        assert response.is_success is False
        assert response.message == "Resource not found"

    def test_response_with_metadata(self) -> None:
        """测试带元数据的响应"""
        response = GrpcResponse(
            data={"result": "ok"},
            metadata={"request-id": "abc123"},
            trailing_metadata={"server-timing": "100ms"},
        )

        assert response.metadata == {"request-id": "abc123"}
        assert response.trailing_metadata == {"server-timing": "100ms"}

    def test_raise_for_status_success(self) -> None:
        """测试成功响应不抛出异常"""
        response = GrpcResponse(data={"ok": True})
        response.raise_for_status()  # 不应抛出异常

    def test_raise_for_status_error(self) -> None:
        """测试错误响应抛出异常"""
        response = GrpcResponse(
            status_code=GrpcStatusCode.INTERNAL,
            message="Internal server error",
        )

        with pytest.raises(GrpcError) as exc_info:
            response.raise_for_status()

        assert exc_info.value.code == GrpcStatusCode.INTERNAL
        assert "Internal server error" in str(exc_info.value)


class TestChannelOptions:
    """测试 ChannelOptions"""

    def test_default_options(self) -> None:
        """测试默认选项"""
        options = ChannelOptions()

        assert options.max_send_message_length == -1
        assert options.max_receive_message_length == -1
        assert options.keepalive_time_ms == 60000
        assert options.keepalive_timeout_ms == 20000
        assert options.keepalive_permit_without_calls is True

    def test_custom_options(self) -> None:
        """测试自定义选项"""
        options = ChannelOptions(
            max_send_message_length=1024 * 1024,
            max_receive_message_length=1024 * 1024,
            keepalive_time_ms=30000,
        )

        assert options.max_send_message_length == 1024 * 1024
        assert options.keepalive_time_ms == 30000

    def test_to_grpc_options(self) -> None:
        """测试转换为 gRPC 选项格式"""
        options = ChannelOptions(
            max_send_message_length=1024,
            keepalive_time_ms=30000,
        )

        grpc_options = options.to_grpc_options()

        assert isinstance(grpc_options, list)
        assert len(grpc_options) == 6
        assert ("grpc.max_send_message_length", 1024) in grpc_options
        assert ("grpc.keepalive_time_ms", 30000) in grpc_options

    def test_keepalive_permit_conversion(self) -> None:
        """测试 keepalive_permit_without_calls 转换为 0/1"""
        options_true = ChannelOptions(keepalive_permit_without_calls=True)
        options_false = ChannelOptions(keepalive_permit_without_calls=False)

        grpc_options_true = options_true.to_grpc_options()
        grpc_options_false = options_false.to_grpc_options()

        # 检查转换后的值
        permit_option_true = [
            opt for opt in grpc_options_true if opt[0] == "grpc.keepalive_permit_without_calls"
        ][0]
        permit_option_false = [
            opt for opt in grpc_options_false if opt[0] == "grpc.keepalive_permit_without_calls"
        ][0]

        assert permit_option_true[1] == 1
        assert permit_option_false[1] == 0
