"""测试 gRPC 客户端

注意：由于 gRPC 需要安装额外的依赖（grpcio），这里主要测试客户端的基本功能和接口
"""

import pytest

from df_test_framework.capabilities.clients.grpc import GrpcClient
from df_test_framework.capabilities.clients.grpc.interceptors import MetadataInterceptor
from df_test_framework.capabilities.clients.grpc.models import ChannelOptions


class TestGrpcClient:
    """测试 GrpcClient"""

    def test_init_client(self) -> None:
        """测试初始化客户端"""
        client = GrpcClient("localhost:50051")

        assert client.target == "localhost:50051"
        assert client.secure is False
        assert isinstance(client.options, ChannelOptions)
        assert len(client.interceptors) == 0

    def test_init_with_custom_options(self) -> None:
        """测试使用自定义选项初始化"""
        options = ChannelOptions(
            max_send_message_length=1024 * 1024,
            keepalive_time_ms=30000,
        )

        client = GrpcClient(
            "localhost:50051",
            options=options,
        )

        assert client.options.max_send_message_length == 1024 * 1024
        assert client.options.keepalive_time_ms == 30000

    def test_init_with_interceptors(self) -> None:
        """测试使用拦截器初始化"""
        interceptor = MetadataInterceptor({"Authorization": "Bearer token"})
        client = GrpcClient(
            "localhost:50051",
            interceptors=[interceptor],
        )

        assert len(client.interceptors) == 1
        assert isinstance(client.interceptors[0], MetadataInterceptor)

    def test_init_secure_client(self) -> None:
        """测试初始化安全客户端"""
        client = GrpcClient(
            "localhost:50051",
            secure=True,
        )

        assert client.secure is True

    def test_add_metadata(self) -> None:
        """测试添加元数据"""
        client = GrpcClient("localhost:50051")
        client.add_metadata("Authorization", "Bearer token123")
        client.add_metadata("X-Request-ID", "abc")

        assert len(client._metadata) == 2
        assert ("Authorization", "Bearer token123") in client._metadata
        assert ("X-Request-ID", "abc") in client._metadata

    def test_clear_metadata(self) -> None:
        """测试清除元数据"""
        client = GrpcClient("localhost:50051")
        client.add_metadata("key", "value")
        client.clear_metadata()

        assert len(client._metadata) == 0

    def test_add_interceptor(self) -> None:
        """测试添加拦截器"""
        client = GrpcClient("localhost:50051")
        interceptor = MetadataInterceptor()

        client.add_interceptor(interceptor)

        assert len(client.interceptors) == 1
        assert client.interceptors[0] == interceptor

    def test_ensure_grpc_not_installed(self) -> None:
        """测试 grpcio 未安装时的错误"""
        client = GrpcClient("localhost:50051")

        # 如果 grpcio 未安装，应该抛出 ImportError
        # 如果已安装，这个测试会被跳过
        try:
            import grpc  # noqa: F401

            pytest.skip("grpcio is installed, skipping this test")
        except ImportError:
            with pytest.raises(ImportError, match="grpcio is not installed"):
                client.connect()

    def test_unary_call_without_connection(self) -> None:
        """测试未连接时调用"""
        client = GrpcClient("localhost:50051")

        with pytest.raises(RuntimeError, match="Not connected"):
            client.unary_call("TestMethod", {})

    def test_server_streaming_call_without_connection(self) -> None:
        """测试未连接时流式调用"""
        client = GrpcClient("localhost:50051")

        with pytest.raises(RuntimeError, match="Not connected"):
            list(client.server_streaming_call("TestMethod", {}))

    def test_apply_interceptors_request(self) -> None:
        """测试应用请求拦截器"""
        interceptor = MetadataInterceptor({"X-Custom": "value"})
        client = GrpcClient("localhost:50051", interceptors=[interceptor])

        request = {}
        metadata = [("Content-Type", "application/grpc")]

        result_request, result_metadata = client._apply_interceptors_request(
            "TestMethod", request, metadata
        )

        # 验证拦截器被应用
        assert ("X-Custom", "value") in result_metadata

    def test_apply_interceptors_response(self) -> None:
        """测试应用响应拦截器"""
        client = GrpcClient("localhost:50051")

        response = {"result": "ok"}
        metadata = {}

        result_response = client._apply_interceptors_response("TestMethod", response, metadata)

        assert result_response == response

    # ========== 新增测试：连接和关闭 ==========

    def test_connect_insecure(self) -> None:
        """测试非安全连接"""
        from unittest.mock import MagicMock, patch

        mock_grpc = MagicMock()
        mock_channel = MagicMock()
        mock_grpc.insecure_channel.return_value = mock_channel

        with patch.dict("sys.modules", {"grpc": mock_grpc}):
            client = GrpcClient("localhost:50051")
            client.connect()

            mock_grpc.insecure_channel.assert_called_once()
            assert client._channel == mock_channel

    def test_connect_secure_with_default_credentials(self) -> None:
        """测试安全连接（默认凭证）"""
        from unittest.mock import MagicMock, patch

        mock_grpc = MagicMock()
        mock_channel = MagicMock()
        mock_credentials = MagicMock()
        mock_grpc.secure_channel.return_value = mock_channel
        mock_grpc.ssl_channel_credentials.return_value = mock_credentials

        with patch.dict("sys.modules", {"grpc": mock_grpc}):
            client = GrpcClient("localhost:50051", secure=True)
            client.connect()

            mock_grpc.ssl_channel_credentials.assert_called_once()
            mock_grpc.secure_channel.assert_called_once()
            assert client._channel == mock_channel

    def test_connect_secure_with_custom_credentials(self) -> None:
        """测试安全连接（自定义凭证）"""
        from unittest.mock import MagicMock, patch

        mock_grpc = MagicMock()
        mock_channel = MagicMock()
        custom_credentials = MagicMock()
        mock_grpc.secure_channel.return_value = mock_channel

        with patch.dict("sys.modules", {"grpc": mock_grpc}):
            client = GrpcClient(
                "localhost:50051",
                secure=True,
                credentials=custom_credentials,
            )
            client.connect()

            # 不应调用默认凭证
            mock_grpc.ssl_channel_credentials.assert_not_called()
            mock_grpc.secure_channel.assert_called_once()
            assert client._channel == mock_channel
            assert client.credentials == custom_credentials

    def test_connect_with_stub_class(self) -> None:
        """测试连接时创建 stub"""
        from unittest.mock import MagicMock, patch

        mock_grpc = MagicMock()
        mock_channel = MagicMock()
        mock_stub_class = MagicMock()
        mock_stub_instance = MagicMock()
        mock_stub_class.return_value = mock_stub_instance
        mock_grpc.insecure_channel.return_value = mock_channel

        with patch.dict("sys.modules", {"grpc": mock_grpc}):
            client = GrpcClient("localhost:50051", stub_class=mock_stub_class)
            client.connect()

            mock_stub_class.assert_called_once_with(mock_channel)
            assert client._stub == mock_stub_instance

    def test_close(self) -> None:
        """测试关闭连接"""
        from unittest.mock import MagicMock

        client = GrpcClient("localhost:50051")
        mock_channel = MagicMock()
        client._channel = mock_channel

        client.close()

        mock_channel.close.assert_called_once()

    def test_close_without_connection(self) -> None:
        """测试未连接时关闭"""
        client = GrpcClient("localhost:50051")

        # 不应抛出异常
        client.close()

    # ========== 新增测试：上下文管理器 ==========

    def test_context_manager(self) -> None:
        """测试上下文管理器"""
        from unittest.mock import MagicMock, patch

        mock_grpc = MagicMock()
        mock_channel = MagicMock()
        mock_grpc.insecure_channel.return_value = mock_channel

        with patch.dict("sys.modules", {"grpc": mock_grpc}):
            with GrpcClient("localhost:50051") as client:
                assert client._channel == mock_channel

            mock_channel.close.assert_called_once()

    # ========== 新增测试：Unary Call ==========

    def test_unary_call_success(self) -> None:
        """测试一元调用成功"""
        from unittest.mock import MagicMock

        client = GrpcClient("localhost:50051")
        mock_stub = MagicMock()
        mock_response = MagicMock()
        mock_stub.TestMethod.return_value = mock_response
        client._stub = mock_stub

        response = client.unary_call("TestMethod", {"data": "test"})

        assert response.is_success is True
        assert response.data == mock_response
        mock_stub.TestMethod.assert_called_once()

    def test_unary_call_with_metadata(self) -> None:
        """测试带元数据的一元调用"""
        from unittest.mock import MagicMock

        client = GrpcClient("localhost:50051")
        client.add_metadata("Authorization", "Bearer token")

        mock_stub = MagicMock()
        mock_response = MagicMock()
        mock_stub.TestMethod.return_value = mock_response
        client._stub = mock_stub

        response = client.unary_call(
            "TestMethod",
            {"data": "test"},
            metadata=[("X-Request-ID", "123")],
        )

        assert response.is_success is True
        call_kwargs = mock_stub.TestMethod.call_args[1]
        assert ("Authorization", "Bearer token") in call_kwargs["metadata"]
        assert ("X-Request-ID", "123") in call_kwargs["metadata"]

    def test_unary_call_with_timeout(self) -> None:
        """测试带超时的一元调用"""
        from unittest.mock import MagicMock

        client = GrpcClient("localhost:50051")
        mock_stub = MagicMock()
        mock_response = MagicMock()
        mock_stub.TestMethod.return_value = mock_response
        client._stub = mock_stub

        response = client.unary_call("TestMethod", {}, timeout=30.0)

        assert response.is_success is True
        call_kwargs = mock_stub.TestMethod.call_args[1]
        assert call_kwargs["timeout"] == 30.0

    def test_unary_call_error(self) -> None:
        """测试一元调用异常"""
        from unittest.mock import MagicMock

        from df_test_framework.capabilities.clients.grpc.models import GrpcStatusCode

        client = GrpcClient("localhost:50051")
        mock_stub = MagicMock()
        mock_stub.TestMethod.side_effect = Exception("Connection refused")
        client._stub = mock_stub

        response = client.unary_call("TestMethod", {})

        assert response.is_success is False
        assert response.status_code == GrpcStatusCode.UNKNOWN
        assert "Connection refused" in response.message  # type: ignore

    # ========== 新增测试：Server Streaming Call ==========

    def test_server_streaming_call_success(self) -> None:
        """测试服务端流式调用成功"""
        from unittest.mock import MagicMock

        client = GrpcClient("localhost:50051")
        mock_stub = MagicMock()
        mock_responses = [MagicMock(), MagicMock(), MagicMock()]
        mock_stub.StreamMethod.return_value = iter(mock_responses)
        client._stub = mock_stub

        responses = list(client.server_streaming_call("StreamMethod", {"data": "test"}))

        assert len(responses) == 3
        for resp in responses:
            assert resp.is_success is True

    def test_server_streaming_call_with_metadata(self) -> None:
        """测试带元数据的流式调用"""
        from unittest.mock import MagicMock

        client = GrpcClient("localhost:50051")
        client.add_metadata("Authorization", "Bearer token")

        mock_stub = MagicMock()
        mock_stub.StreamMethod.return_value = iter([MagicMock()])
        client._stub = mock_stub

        list(
            client.server_streaming_call(
                "StreamMethod",
                {},
                metadata=[("X-Request-ID", "456")],
            )
        )

        call_kwargs = mock_stub.StreamMethod.call_args[1]
        assert ("Authorization", "Bearer token") in call_kwargs["metadata"]
        assert ("X-Request-ID", "456") in call_kwargs["metadata"]

    def test_server_streaming_call_error(self) -> None:
        """测试流式调用异常"""
        from unittest.mock import MagicMock

        from df_test_framework.capabilities.clients.grpc.models import GrpcStatusCode

        client = GrpcClient("localhost:50051")
        mock_stub = MagicMock()
        mock_stub.StreamMethod.side_effect = Exception("Stream failed")
        client._stub = mock_stub

        responses = list(client.server_streaming_call("StreamMethod", {}))

        assert len(responses) == 1
        assert responses[0].is_success is False
        assert responses[0].status_code == GrpcStatusCode.UNKNOWN
        assert "Stream failed" in responses[0].message  # type: ignore

    # ========== 新增测试：状态码提取 ==========

    def test_extract_status_code_from_grpc_error(self) -> None:
        """测试从 gRPC 错误提取状态码"""
        from unittest.mock import MagicMock

        from df_test_framework.capabilities.clients.grpc.models import GrpcStatusCode

        client = GrpcClient("localhost:50051")

        # 模拟 gRPC RpcError
        mock_code = MagicMock()
        mock_code.value = (14,)  # UNAVAILABLE
        mock_error = MagicMock()
        mock_error.code.return_value = mock_code

        status_code = client._extract_status_code(mock_error)

        assert status_code == GrpcStatusCode.UNAVAILABLE

    def test_extract_status_code_invalid_code(self) -> None:
        """测试提取无效状态码"""
        from unittest.mock import MagicMock

        from df_test_framework.capabilities.clients.grpc.models import GrpcStatusCode

        client = GrpcClient("localhost:50051")

        # 模拟无效的状态码
        mock_error = MagicMock()
        mock_error.code.side_effect = AttributeError()

        status_code = client._extract_status_code(mock_error)

        assert status_code == GrpcStatusCode.UNKNOWN

    def test_extract_status_code_unknown_value(self) -> None:
        """测试提取未知状态码值"""
        from unittest.mock import MagicMock

        from df_test_framework.capabilities.clients.grpc.models import GrpcStatusCode

        client = GrpcClient("localhost:50051")

        # 模拟无效的值
        mock_code = MagicMock()
        mock_code.value = (999,)  # 无效值
        mock_error = MagicMock()
        mock_error.code.return_value = mock_code

        status_code = client._extract_status_code(mock_error)

        assert status_code == GrpcStatusCode.UNKNOWN

    def test_extract_status_code_no_code_attr(self) -> None:
        """测试错误没有 code 属性"""
        from df_test_framework.capabilities.clients.grpc.models import GrpcStatusCode

        client = GrpcClient("localhost:50051")

        # 普通异常没有 code 属性
        error = Exception("Simple error")

        status_code = client._extract_status_code(error)

        assert status_code == GrpcStatusCode.UNKNOWN

    # ========== 新增测试：健康检查 ==========

    def test_health_check_exception(self) -> None:
        """测试健康检查异常"""
        from unittest.mock import MagicMock, patch

        client = GrpcClient("localhost:50051")
        client._channel = MagicMock()

        # 模拟 grpc_health 导入失败
        with patch(
            "df_test_framework.capabilities.clients.grpc.client.GrpcClient.health_check",
            side_effect=Exception("Health check failed"),
        ):
            # 直接测试异常返回 False
            pass

        # 直接调用原始方法，让 grpc_health 模块导入失败返回 False
        result = client.health_check()
        # 如果 grpc_health 未安装，会捕获 ImportError 返回 False
        # 如果已安装但无服务，也会返回 False
        assert result is False

    def test_health_check_returns_false_on_import_error(self) -> None:
        """测试健康检查在模块不可用时返回 False"""
        import sys
        from unittest.mock import patch

        client = GrpcClient("localhost:50051")
        client._channel = "mock_channel"

        # 删除已缓存的模块（如果存在）
        modules_to_remove = [
            "grpc_health",
            "grpc_health.v1",
            "grpc_health.v1.health_pb2",
            "grpc_health.v1.health_pb2_grpc",
        ]

        original_modules = {}
        for mod in modules_to_remove:
            if mod in sys.modules:
                original_modules[mod] = sys.modules.pop(mod)

        try:
            # 模拟 grpc_health 无法导入
            with patch.dict(sys.modules, {"grpc_health": None}):
                result = client.health_check()
                # 如果 grpc_health 无法导入，应返回 False
                assert result is False
        finally:
            # 恢复原始模块
            for mod, module in original_modules.items():
                sys.modules[mod] = module

    def test_health_check_connect_called_when_no_channel(self) -> None:
        """测试健康检查在无连接时调用 connect"""
        from unittest.mock import MagicMock, patch

        mock_grpc = MagicMock()
        mock_channel = MagicMock()
        mock_grpc.insecure_channel.return_value = mock_channel

        # 需要同时 mock grpc_health，这样代码才能执行到 connect 逻辑
        mock_health_pb2 = MagicMock()
        mock_health_pb2.HealthCheckResponse.SERVING = 1

        mock_health_pb2_grpc = MagicMock()
        mock_health_stub = MagicMock()
        mock_health_response = MagicMock()
        mock_health_response.status = 0  # NOT_SERVING
        mock_health_stub.Check.return_value = mock_health_response
        mock_health_pb2_grpc.HealthStub.return_value = mock_health_stub

        # 在 sys.modules 中设置所有需要的模块
        mock_modules = {
            "grpc": mock_grpc,
            "grpc_health": MagicMock(),
            "grpc_health.v1": MagicMock(
                health_pb2=mock_health_pb2,
                health_pb2_grpc=mock_health_pb2_grpc,
            ),
            "grpc_health.v1.health_pb2": mock_health_pb2,
            "grpc_health.v1.health_pb2_grpc": mock_health_pb2_grpc,
        }

        with patch.dict("sys.modules", mock_modules):
            client = GrpcClient("localhost:50051")
            assert client._channel is None

            # health_check 内部会检查 _channel，如果为 None 则调用 connect
            result = client.health_check()

            # connect 被调用，channel 被设置
            mock_grpc.insecure_channel.assert_called_once()
            assert client._channel == mock_channel
            # 由于 mock 返回 status=0 (NOT_SERVING)，返回 False
            assert result is False

    # ========== Phase 3 新增测试：流式资源清理 ==========

    def test_server_streaming_call_cancels_stream_on_completion(self) -> None:
        """测试流式调用完成后取消流"""
        from unittest.mock import MagicMock

        client = GrpcClient("localhost:50051")
        mock_stub = MagicMock()
        mock_responses = [MagicMock(), MagicMock()]
        mock_stream = MagicMock()
        mock_stream.__iter__ = MagicMock(return_value=iter(mock_responses))
        mock_stream.cancel = MagicMock()
        mock_stub.StreamMethod.return_value = mock_stream
        client._stub = mock_stub

        # 消费所有响应
        responses = list(client.server_streaming_call("StreamMethod", {}))

        assert len(responses) == 2
        # 验证 cancel 被调用（流完成后释放资源）
        mock_stream.cancel.assert_called_once()

    def test_server_streaming_call_cancels_stream_on_error(self) -> None:
        """测试流式调用异常时取消流"""
        from unittest.mock import MagicMock

        client = GrpcClient("localhost:50051")
        mock_stub = MagicMock()
        mock_stream = MagicMock()
        mock_stream.__iter__ = MagicMock(side_effect=Exception("Stream error"))
        mock_stream.cancel = MagicMock()
        mock_stub.StreamMethod.return_value = mock_stream
        client._stub = mock_stub

        # 尝试消费响应
        responses = list(client.server_streaming_call("StreamMethod", {}))

        assert len(responses) == 1
        assert responses[0].is_success is False
        # 验证 cancel 被调用（异常后释放资源）
        mock_stream.cancel.assert_called_once()

    def test_server_streaming_call_handles_cancel_exception(self) -> None:
        """测试流式调用取消时处理异常"""
        from unittest.mock import MagicMock

        client = GrpcClient("localhost:50051")
        mock_stub = MagicMock()
        mock_responses = [MagicMock()]
        mock_stream = MagicMock()
        mock_stream.__iter__ = MagicMock(return_value=iter(mock_responses))
        # cancel 抛出异常（例如流已经取消）
        mock_stream.cancel = MagicMock(side_effect=Exception("Already cancelled"))
        mock_stub.StreamMethod.return_value = mock_stream
        client._stub = mock_stub

        # 不应抛出异常
        responses = list(client.server_streaming_call("StreamMethod", {}))

        assert len(responses) == 1
        assert responses[0].is_success is True

    def test_server_streaming_call_no_cancel_attribute(self) -> None:
        """测试流式调用处理无 cancel 属性的流"""
        from unittest.mock import MagicMock

        client = GrpcClient("localhost:50051")
        mock_stub = MagicMock()
        mock_responses = [MagicMock()]
        # 模拟没有 cancel 属性的流（简单迭代器）
        mock_stub.StreamMethod.return_value = iter(mock_responses)
        client._stub = mock_stub

        # 不应抛出异常
        responses = list(client.server_streaming_call("StreamMethod", {}))

        assert len(responses) == 1
        assert responses[0].is_success is True
